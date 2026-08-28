"""BASELINE: one direct prompt with basic instructions.

This is the 'reasonable basic way' a capable person would wire this up today:
dump the OCR text and the full ERP data into a single LLM prompt together with
the AP policy, and ask for a decision. Same model, same policy, same cases as
the agent solution — the only difference is the workflow around the model.

Run:  python -m matchpoint.baseline [--run-name baseline] [--limit N]
"""
from __future__ import annotations

import argparse
import json
import time

from .config import OUT, TRAJ, load_env
from .llm import chat, extract_json
from .ocr import get_ocr_text
from .policy import POLICY
from .trajectory import Trajectory
from .world import load_world, load_manifest

SYSTEM = "You are an accounts-payable analyst. Follow the policy exactly and answer with a single JSON object."


def run_case(invoice_id: str, world: dict, traj: Trajectory) -> dict:
    ocr_text = get_ocr_text(invoice_id)
    prompt = f"""{POLICY}

=== ERP DATA ===

VENDOR MASTER:
{json.dumps(world['vendors'], indent=1)}

PURCHASE ORDERS:
{json.dumps(world['pos'], indent=1)}

GOODS RECEIPT NOTES:
{json.dumps(world['grns'], indent=1)}

PAYMENT HISTORY (already-paid invoices):
{json.dumps(world['payments'], indent=1)}

=== INVOICE (OCR text) ===

{ocr_text}

Apply the policy to this invoice and return the JSON decision object."""
    t0 = time.time()
    msg = chat(
        [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
        response_json=True, max_tokens=6000, trajectory=traj, agent="baseline",
    )
    out = extract_json(msg["content"])
    out["invoice_id"] = invoice_id
    out.setdefault("discrepancies", [])
    out["latency_s"] = round(time.time() - t0, 2)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-name", default="baseline")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    load_env()

    world = load_world()
    manifest = load_manifest()
    if args.limit:
        manifest = manifest[: args.limit]

    run_dir = OUT / "runs" / args.run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    traj_path = TRAJ / f"{args.run_name}.jsonl"
    if traj_path.exists():
        traj_path.unlink()

    results = []
    for i, entry in enumerate(manifest, 1):
        inv_id = entry["invoice_id"]
        traj = Trajectory(traj_path, args.run_name, inv_id)
        try:
            res = run_case(inv_id, world, traj)
        except Exception as e:  # record failures honestly — they count against us
            res = {"invoice_id": inv_id, "decision": "error", "discrepancies": [],
                   "explanation": f"PIPELINE ERROR: {e}", "latency_s": None}
            traj.log_event("pipeline_error", {"error": str(e)})
        results.append(res)
        print(f"[{i}/{len(manifest)}] {inv_id}: {res['decision']} {res['discrepancies']}")

    (run_dir / "results.json").write_text(json.dumps(results, indent=2))
    print(f"\nWrote {run_dir / 'results.json'} and {traj_path}")


if __name__ == "__main__":
    main()
