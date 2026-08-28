"""Matchpoint agent pipeline.

Stages (each one is a runnable config so every changelog entry can be re-run):

  v1     Extractor agent (OCR -> structured JSON) + decision LLM with SCOPED
         ERP context (only the referenced PO / its GRNs / that vendor / that
         vendor's payment history) instead of the full ERP dump.
  v2     v1 + the decision LLM becomes a MATCHER AGENT with deterministic
         function-calling tools (PO lookup, received totals, arithmetic check,
         payment search). The LLM stops doing arithmetic.
  v3     v2 + VERIFIER: an independent deterministic 3-way match engine
         recomputes everything from the extracted invoice. If it disagrees
         with the matcher, the matcher gets one feedback round; if they still
         disagree, the deterministic result wins and the case is flagged.
  final  v3 + vendor memory (aliases + history notes from prior quarters)
         + human approval queue for every hold/reject (sandboxed payments).

Run:  python -m matchpoint.agent --config final [--run-name agent_final] [--limit N]
"""
from __future__ import annotations

import argparse
import json
import time

from .config import OUT, TRAJ, load_env
from .llm import chat, extract_json
from .ocr import get_ocr_text
from .policy import POLICY
from .tools import (get_po, get_grns_for_po, received_totals, get_vendor,
                    find_vendor_by_name, search_payments, match_engine)
from .trajectory import Trajectory
from .world import load_world, load_manifest, load_vendor_memory

CONFIGS = {
    "v1": {"tools": False, "verifier": False, "memory": False},
    # v1cot: REMOVED EXPERIMENT — instead of tools, ask the model to recompute
    # all arithmetic step by step in-context. Kept here so the negative result
    # in the changelog stays reproducible.
    "v1cot": {"tools": False, "verifier": False, "memory": False, "cot": True},
    "v2": {"tools": True, "verifier": False, "memory": False},
    "v3": {"tools": True, "verifier": True, "memory": False},
    "final": {"tools": True, "verifier": True, "memory": True},
    # engine_only: ABLATION — extraction agent + deterministic match engine,
    # no matcher LLM at all. Measures what the matcher agent adds.
    "engine_only": {"tools": False, "verifier": False, "memory": True, "engine_only": True},
}

# ----------------------------------------------------------- extractor ------

EXTRACT_SYSTEM = """You are a precise invoice data extractor. You receive OCR text of a
supplier invoice (markdown). Return ONLY a JSON object with exactly these fields:
{
 "invoice_no": str, "vendor_name": str, "date": "YYYY-MM-DD", "po_number": str,
 "currency": "USD"|"EUR"|"GBP",
 "lines": [{"sku": str, "description": str, "qty": number, "unit_price": number, "amount": number}],
 "subtotal": number, "tax": number, "total": number,
 "bank_name": str, "bank_routing": str, "bank_account": str, "payment_terms": str
}
Rules:
- Copy numbers exactly as printed. NEVER recompute, correct or 'fix' any value —
  downstream systems check the printed numbers for errors.
- Strip currency symbols and thousands separators from numbers.
- If a field is genuinely absent, use null."""

REQUIRED = ["invoice_no", "vendor_name", "po_number", "currency", "lines",
            "subtotal", "tax", "total", "bank_account"]


def extract_invoice(invoice_id: str, traj: Trajectory) -> dict:
    ocr_text = get_ocr_text(invoice_id)
    messages = [{"role": "system", "content": EXTRACT_SYSTEM},
                {"role": "user", "content": ocr_text}]
    for attempt in range(2):
        msg = chat(messages, response_json=True, max_tokens=4000,
                   trajectory=traj, agent="extractor")
        data = extract_json(msg["content"])
        problems = validate_extraction(data)
        if not problems:
            traj.log_event("extraction_ok", {"invoice_no": data.get("invoice_no")})
            return data
        traj.log_event("extraction_retry", {"problems": problems})
        messages += [{"role": "assistant", "content": msg["content"]},
                     {"role": "user", "content": "Your JSON has problems, fix them and resend "
                                                  "the full corrected JSON only:\n- " + "\n- ".join(problems)}]
    raise ValueError(f"extraction failed after retry: {problems}")


def validate_extraction(d: dict) -> list[str]:
    problems = []
    for k in REQUIRED:
        if d.get(k) in (None, "", []):
            problems.append(f"missing field: {k}")
    for i, ln in enumerate(d.get("lines") or []):
        for k in ("sku", "qty", "unit_price", "amount"):
            if ln.get(k) in (None, ""):
                problems.append(f"line {i + 1} missing {k}")
        for k in ("qty", "unit_price", "amount"):
            if not isinstance(ln.get(k), (int, float)):
                problems.append(f"line {i + 1} field {k} is not numeric")
    for k in ("subtotal", "tax", "total"):
        if d.get(k) is not None and not isinstance(d.get(k), (int, float)):
            problems.append(f"{k} is not numeric")
    return problems


# ------------------------------------------------------- scoped context -----

def scoped_context(inv: dict, world: dict, memory: dict | None) -> str:
    """Only the ERP records relevant to this invoice — not the whole database."""
    po = get_po(world, inv.get("po_number", ""))
    vendor = get_vendor(world, po["vendor_id"]) if po else find_vendor_by_name(
        world, inv.get("vendor_name", ""), memory)
    parts = []
    if po:
        parts.append("PURCHASE ORDER:\n" + json.dumps(po, indent=1))
        grns = get_grns_for_po(world, po["po_number"])
        parts.append("GOODS RECEIPT NOTES for this PO:\n" +
                     (json.dumps(grns, indent=1) if grns else "NONE FOUND"))
    else:
        parts.append(f"PURCHASE ORDER: no PO named '{inv.get('po_number')}' exists.")
    if vendor:
        parts.append("VENDOR MASTER RECORD:\n" + json.dumps(vendor, indent=1))
        pays = [p for p in world["payments"] if p["vendor_id"] == vendor["vendor_id"]]
        parts.append("PAYMENT HISTORY for this vendor:\n" +
                     (json.dumps(pays, indent=1) if pays else "none"))
        if memory and vendor["vendor_id"] in memory:
            parts.append("VENDOR MEMORY (learned from prior quarters of processing):\n" +
                         json.dumps(memory[vendor["vendor_id"]], indent=1))
    else:
        parts.append("VENDOR: could not resolve the vendor name to the vendor master.")
    return "\n\n".join(parts)


# ------------------------------------------------------------- matcher ------

def tool_schemas() -> list[dict]:
    def fn(name, desc, params):
        return {"type": "function", "function": {"name": name, "description": desc,
                "parameters": {"type": "object", "properties": params,
                               "required": list(params)}}}
    return [
        fn("get_po", "Fetch a purchase order by number.", {"po_number": {"type": "string"}}),
        fn("get_received_totals", "Total received qty per PO line across all GRNs (partial deliveries are summed).",
           {"po_number": {"type": "string"}}),
        fn("get_vendor_by_name", "Resolve an invoice display name to a vendor master record (handles aliases).",
           {"name": {"type": "string"}}),
        fn("search_payments", "Search payment history for potential duplicates of this invoice.",
           {"vendor_id": {"type": "string"}, "po_number": {"type": "string"},
            "total": {"type": "number"}, "invoice_no": {"type": "string"}}),
        fn("arithmetic_check", "Deterministically verify all invoice arithmetic (line math, subtotal, tax at the vendor's master tax rate, total) against policy tolerances. ALWAYS use this instead of computing yourself.",
           {"vendor_id": {"type": "string"}}),
    ]


def run_tool(name: str, args: dict, inv: dict, world: dict, memory: dict | None) -> dict:
    if name == "get_po":
        po = get_po(world, args["po_number"])
        return po or {"error": f"PO {args['po_number']} not found"}
    if name == "get_received_totals":
        grns = get_grns_for_po(world, args["po_number"])
        if not grns:
            return {"error": f"no GRNs exist for {args['po_number']}"}
        return {"received_by_line_no": received_totals(world, args["po_number"]),
                "grn_count": len(grns), "grn_numbers": [g["grn_number"] for g in grns]}
    if name == "get_vendor_by_name":
        v = find_vendor_by_name(world, args["name"], memory)
        if not v:
            return {"error": f"no vendor matches '{args['name']}'"}
        out = dict(v)
        if memory and v["vendor_id"] in memory:
            out["memory"] = memory[v["vendor_id"]]
        return out
    if name == "search_payments":
        return {"potential_duplicates": search_payments(
            world, args.get("vendor_id"), args.get("po_number"),
            args.get("total"), args.get("invoice_no"))}
    if name == "arithmetic_check":
        vendor = get_vendor(world, args["vendor_id"])
        if not vendor:
            return {"error": f"vendor {args['vendor_id']} not found"}
        # pin vendor resolution to the caller-supplied id so alias display names
        # can't silently skip the tax/bank checks
        inv_pinned = {**inv, "vendor_name": vendor["name"]}
        sub = match_engine(inv_pinned, {**world, "pos": [], "grns": [], "payments": []}, memory)
        # engine with no PO/GRN/payments == pure arithmetic + bank check for this vendor
        return {"arithmetic_and_bank_findings":
                [d for d in sub["discrepancies"] if d["code"] in ("TAX_ERROR", "TOTAL_ERROR", "BANK_CHANGE")],
                "checks_passed": [c for c in sub["checks_passed"] if "OK" in c or "match" in c]}
    return {"error": f"unknown tool {name}"}


MATCHER_SYSTEM = f"""You are the AP matching agent for Harborview Manufacturing.
{POLICY}
You are given the structured invoice (extracted from OCR) and scoped ERP context.
Use the tools to verify every check — do NOT do arithmetic yourself; call arithmetic_check.
Verify: PO existence, line prices, billed vs received quantities, arithmetic, currency,
remit-to bank vs master, duplicates. Then give the final JSON decision object with an
explanation an auditor could follow, citing the specific numbers."""


def matcher_decide(inv: dict, world: dict, memory: dict | None, cfg: dict,
                   traj: Trajectory, feedback: str | None = None) -> dict:
    ctx = scoped_context(inv, world, memory if cfg["memory"] else None)
    user = f"STRUCTURED INVOICE:\n{json.dumps(inv, indent=1)}\n\nSCOPED ERP CONTEXT:\n{ctx}"
    if feedback:
        user += f"\n\nVERIFIER FEEDBACK on your previous answer — re-check and give a corrected final JSON:\n{feedback}"
    messages = [{"role": "system", "content": MATCHER_SYSTEM},
                {"role": "user", "content": user}]

    if not cfg["tools"]:
        if cfg.get("cot"):
            messages[1]["content"] += (
                "\n\nBefore deciding, recompute every check yourself, digit by digit: "
                "each line qty x unit_price, the sum of line amounts vs subtotal, "
                "tax_rate x subtotal vs tax, and subtotal + tax vs total. Show the "
                "arithmetic in a 'workings' field of your JSON, then decide.")
        msg = chat(messages, response_json=True, max_tokens=5000, trajectory=traj, agent="matcher_v1")
        return extract_json(msg["content"])

    tools = tool_schemas()
    mem = memory if cfg["memory"] else None
    for _round in range(10):
        msg = chat(messages, tools=tools, max_tokens=5000, trajectory=traj, agent="matcher")
        if msg.get("tool_calls"):
            messages.append({"role": "assistant", "content": msg.get("content"),
                             "tool_calls": msg["tool_calls"]})
            for tc in msg["tool_calls"]:
                args = json.loads(tc["function"]["arguments"] or "{}")
                result = run_tool(tc["function"]["name"], args, inv, world, mem)
                traj.log_tool(tc["function"]["name"], args, result)
                messages.append({"role": "tool", "tool_call_id": tc["id"],
                                 "content": json.dumps(result)})
            continue
        return extract_json(msg["content"] or "{}")
    raise RuntimeError("matcher did not produce a final answer within 10 rounds")


# ------------------------------------------------------------ verifier ------

def verify(inv: dict, world: dict, memory: dict | None, matcher_out: dict,
           traj: Trajectory) -> tuple[dict, dict]:
    """Deterministic recomputation. Returns (verdict, engine_result)."""
    engine = match_engine(inv, world, memory)
    m_codes = sorted(set(matcher_out.get("discrepancies") or []))
    e_codes = engine["discrepancy_codes"]
    agree = (m_codes == e_codes and matcher_out.get("decision") == engine["decision"])
    verdict = {"agree": agree, "matcher_codes": m_codes, "engine_codes": e_codes,
               "matcher_decision": matcher_out.get("decision"),
               "engine_decision": engine["decision"]}
    traj.log_event("verifier", verdict)
    return verdict, engine


def verifier_feedback(engine: dict, matcher_out: dict) -> str:
    lines = ["The independent deterministic match engine disagrees with you.",
             f"Engine decision: {engine['decision']}; your decision: {matcher_out.get('decision')}.",
             f"Engine discrepancy codes: {engine['discrepancy_codes']}; yours: {sorted(set(matcher_out.get('discrepancies') or []))}.",
             "Engine evidence:"]
    lines += [f"- {d['code']}: {d['evidence']}" for d in engine["discrepancies"]]
    lines += ["Checks the engine passed:"] + [f"- {c}" for c in engine["checks_passed"][:12]]
    return "\n".join(lines)


# ------------------------------------------------------------- pipeline -----

def run_case(invoice_id: str, world: dict, memory: dict | None, cfg: dict,
             traj: Trajectory) -> dict:
    t0 = time.time()
    inv = extract_invoice(invoice_id, traj)

    if cfg.get("engine_only"):
        engine = match_engine(inv, world, memory)
        traj.log_event("engine_only_result", {"decision": engine["decision"],
                                              "codes": engine["discrepancy_codes"]})
        return {"invoice_id": invoice_id, "po_number": inv.get("po_number"),
                "decision": engine["decision"], "discrepancies": engine["discrepancy_codes"],
                "explanation": " | ".join(d["evidence"] for d in engine["discrepancies"])
                               or "All three-way-match checks passed.",
                "latency_s": round(time.time() - t0, 2), "extracted": inv,
                "engine_evidence": engine["discrepancies"],
                "checks_passed": engine["checks_passed"]}

    out = matcher_decide(inv, world, memory, cfg, traj)
    verifier_events = None
    engine = None

    if cfg["verifier"]:
        verdict, engine = verify(inv, world, memory if cfg["memory"] else None, out, traj)
        if not verdict["agree"]:
            out = matcher_decide(inv, world, memory, cfg, traj,
                                 feedback=verifier_feedback(engine, out))
            verdict2, engine = verify(inv, world, memory if cfg["memory"] else None, out, traj)
            if not verdict2["agree"]:
                # deterministic engine wins; keep the matcher's prose but flag override
                traj.log_event("verifier_override", {"engine": engine["discrepancy_codes"],
                                                     "matcher": out.get("discrepancies")})
                out = {"invoice_id": invoice_id,
                       "po_number": inv.get("po_number"),
                       "decision": engine["decision"],
                       "discrepancies": engine["discrepancy_codes"],
                       "explanation": "VERIFIER OVERRIDE — deterministic engine evidence: " +
                                      " | ".join(d["evidence"] for d in engine["discrepancies"]) ,
                       "verifier_override": True}
            verifier_events = {"initial_agree": verdict["agree"], "final_agree": verdict2["agree"] if not verdict["agree"] else True}
        else:
            verifier_events = {"initial_agree": True, "final_agree": True}

    out["invoice_id"] = invoice_id
    out.setdefault("discrepancies", [])
    out["discrepancies"] = sorted(set(out["discrepancies"]))
    out["latency_s"] = round(time.time() - t0, 2)
    out["extracted"] = inv
    if engine:
        out["engine_evidence"] = engine["discrepancies"]
        out["checks_passed"] = engine["checks_passed"]
    if verifier_events:
        out["verifier"] = verifier_events
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", choices=list(CONFIGS), default="final")
    ap.add_argument("--run-name", default=None)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    load_env()

    cfg = CONFIGS[args.config]
    run_name = args.run_name or f"agent_{args.config}"
    world = load_world()
    memory = load_vendor_memory() if cfg["memory"] else None
    manifest = load_manifest()
    if args.limit:
        manifest = manifest[: args.limit]

    run_dir = OUT / "runs" / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    traj_path = TRAJ / f"{run_name}.jsonl"
    if traj_path.exists():
        traj_path.unlink()

    results = []
    for i, entry in enumerate(manifest, 1):
        inv_id = entry["invoice_id"]
        traj = Trajectory(traj_path, run_name, inv_id)
        try:
            res = run_case(inv_id, world, memory, cfg, traj)
        except Exception as e:
            res = {"invoice_id": inv_id, "decision": "error", "discrepancies": [],
                   "explanation": f"PIPELINE ERROR: {e}", "latency_s": None}
            traj.log_event("pipeline_error", {"error": str(e)})
        results.append(res)
        flag = " [override]" if res.get("verifier_override") else ""
        print(f"[{i}/{len(manifest)}] {inv_id}: {res['decision']} {res['discrepancies']}{flag}")

    (run_dir / "results.json").write_text(json.dumps(results, indent=2))
    print(f"\nWrote {run_dir / 'results.json'} and {traj_path}")


if __name__ == "__main__":
    main()
