"""Evaluation harness. Scores any run (baseline or agent) against gold labels.

Metrics
-------
- decision_accuracy   : share of invoices with the correct approve/hold/reject decision
- exact_match         : decision AND the full discrepancy set both correct
- discrepancy P/R/F1  : micro precision/recall/F1 over discrepancy codes
- false_hold_rate     : clean invoices incorrectly held/rejected (kills supplier trust
                        and creates manual review work — the metric AP managers feel)
- missed_defect_rate  : defective invoices incorrectly approved (money out the door)
- tokens / est. cost / latency per invoice

Usage:
  python eval/run_eval.py --run baseline
  python eval/run_eval.py --run baseline --run agent_final   (comparison table)
  python eval/run_eval.py --all                              (score every run in out/runs)
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from matchpoint.config import OUT, RESULTS, TRAJ, GOLD  # noqa: E402

# Price assumptions for cost-per-invoice (USD per 1M tokens). Adjust to your model.
PRICE_IN = 1.75
PRICE_OUT = 14.0


def token_usage(run: str) -> tuple[dict, dict]:
    """Sum prompt/completion tokens per case from the trajectory log."""
    tin: Counter = Counter()
    tout: Counter = Counter()
    p = TRAJ / f"{run}.jsonl"
    if p.exists():
        for line in p.read_text().splitlines():
            rec = json.loads(line)
            if rec["kind"] == "llm_call":
                tin[rec["case"]] += rec["usage"]["prompt_tokens"] or 0
                tout[rec["case"]] += rec["usage"]["completion_tokens"] or 0
    return dict(tin), dict(tout)


def score_run(run: str) -> dict:
    gold = json.loads((GOLD / "labels.json").read_text())
    results = json.loads((OUT / "runs" / run / "results.json").read_text())
    tin, tout = token_usage(run)

    n = len(results)
    dec_ok = exact_ok = 0
    tp = fp = fn = 0
    clean_total = clean_flagged = 0
    defect_total = defect_approved = 0
    per_case = []
    lat = []

    for r in results:
        g = gold[r["invoice_id"]]
        pred_dec = r.get("decision")
        pred_disc = set(r.get("discrepancies") or [])
        gold_disc = set(g["discrepancies"])

        d_ok = pred_dec == g["decision"]
        e_ok = d_ok and pred_disc == gold_disc
        dec_ok += d_ok
        exact_ok += e_ok
        tp += len(pred_disc & gold_disc)
        fp += len(pred_disc - gold_disc)
        fn += len(gold_disc - pred_disc)

        if g["decision"] == "approve":
            clean_total += 1
            if pred_dec != "approve":
                clean_flagged += 1
        else:
            defect_total += 1
            if pred_dec == "approve":
                defect_approved += 1
        if r.get("latency_s"):
            lat.append(r["latency_s"])

        per_case.append({
            "invoice_id": r["invoice_id"],
            "gold": {"decision": g["decision"], "discrepancies": sorted(gold_disc)},
            "pred": {"decision": pred_dec, "discrepancies": sorted(pred_disc)},
            "decision_correct": d_ok,
            "exact_match": e_ok,
            "explanation": r.get("explanation", ""),
            "tokens_in": tin.get(r["invoice_id"], 0),
            "tokens_out": tout.get(r["invoice_id"], 0),
        })

    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    total_in = sum(tin.values())
    total_out = sum(tout.values())
    cost = (total_in * PRICE_IN + total_out * PRICE_OUT) / 1e6

    summary = {
        "run": run,
        "n_cases": n,
        "decision_accuracy": round(dec_ok / n, 4),
        "exact_match": round(exact_ok / n, 4),
        "discrepancy_precision": round(prec, 4),
        "discrepancy_recall": round(rec, 4),
        "discrepancy_f1": round(f1, 4),
        "false_hold_rate": round(clean_flagged / clean_total, 4) if clean_total else None,
        "missed_defect_rate": round(defect_approved / defect_total, 4) if defect_total else None,
        "tokens_in_total": total_in,
        "tokens_out_total": total_out,
        "est_cost_usd_total": round(cost, 4),
        "est_cost_usd_per_invoice": round(cost / n, 4) if n else None,
        "avg_latency_s": round(sum(lat) / len(lat), 2) if lat else None,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{run}.json").write_text(json.dumps({"summary": summary, "cases": per_case}, indent=2))
    return summary


def comparison_table(summaries: list[dict]) -> str:
    cols = ["decision_accuracy", "exact_match", "discrepancy_f1", "discrepancy_precision",
            "discrepancy_recall", "false_hold_rate", "missed_defect_rate",
            "est_cost_usd_per_invoice", "avg_latency_s"]
    head = "| metric | " + " | ".join(s["run"] for s in summaries) + " |"
    sep = "|---" * (len(summaries) + 1) + "|"
    rows = [head, sep]
    for c in cols:
        rows.append(f"| {c} | " + " | ".join(str(s.get(c)) for s in summaries) + " |")
    return "\n".join(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="append", default=[])
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    runs = args.run
    if args.all:
        runs = sorted(p.name for p in (OUT / "runs").iterdir() if (p / "results.json").exists())
    if not runs:
        ap.error("pass --run <name> (repeatable) or --all")

    summaries = [score_run(r) for r in runs]
    for s in summaries:
        print(json.dumps(s, indent=2))
    if len(summaries) > 1:
        table = comparison_table(summaries)
        (RESULTS / "comparison.md").write_text("# Run comparison\n\n" + table + "\n")
        print("\n" + table)
        print(f"\nWrote {RESULTS / 'comparison.md'}")


if __name__ == "__main__":
    main()
