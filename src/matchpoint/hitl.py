"""Human-in-the-loop approval queue + sandboxed payment ledger.

No real payment ever happens. 'Executing' a payment appends a row to a
sandbox CSV ledger — and only after a human reviewer has signed off.

Flow:
  python -m matchpoint.hitl build --run agent_final     # build queue from a run
  python -m matchpoint.hitl review                      # interactive review CLI
  python -m matchpoint.hitl execute                     # post APPROVED items to sandbox ledger

Policy:
  - agent 'approve'  -> queued as ready-to-pay, still requires human confirm
  - agent 'hold'     -> queued for human investigation with the agent's evidence
  - agent 'reject'   -> queued for human confirmation of rejection
Every human action is timestamped and logged to the trajectory of record.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from datetime import datetime, timezone

from .config import OUT

QUEUE = OUT / "approval_queue.json"
LEDGER = OUT / "sandbox_ledger.csv"
AUDIT_LOG = OUT / "hitl_audit_log.jsonl"


def build(run: str) -> None:
    results = json.loads((OUT / "runs" / run / "results.json").read_text())
    queue = []
    for r in results:
        queue.append({
            "invoice_id": r["invoice_id"],
            "po_number": r.get("po_number"),
            "total": (r.get("extracted") or {}).get("total"),
            "currency": (r.get("extracted") or {}).get("currency"),
            "vendor": (r.get("extracted") or {}).get("vendor_name"),
            "agent_decision": r["decision"],
            "discrepancies": r.get("discrepancies", []),
            "explanation": r.get("explanation", ""),
            "evidence": r.get("engine_evidence", []),
            "human_status": "pending",
            "human_reviewer": None,
            "human_note": None,
            "reviewed_at": None,
            "source_run": run,
        })
    QUEUE.write_text(json.dumps(queue, indent=2))
    n_ok = sum(1 for q in queue if q["agent_decision"] == "approve")
    print(f"Queue built from run '{run}': {len(queue)} invoices "
          f"({n_ok} ready-to-pay, {len(queue) - n_ok} flagged for investigation). -> {QUEUE}")


def _log(action: dict) -> None:
    with AUDIT_LOG.open("a") as f:
        f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), **action}) + "\n")


def review() -> None:
    queue = json.loads(QUEUE.read_text())
    reviewer = input("Reviewer name: ").strip() or "reviewer"
    pending = [q for q in queue if q["human_status"] == "pending"]
    print(f"{len(pending)} invoices pending review.\n")
    for q in pending:
        print("=" * 72)
        print(f"Invoice {q['invoice_id']}  |  {q['vendor']}  |  PO {q['po_number']}  |  "
              f"{q['total']} {q['currency']}")
        print(f"AGENT: {q['agent_decision'].upper()}  {q['discrepancies']}")
        print(f"Reasoning: {q['explanation']}")
        for e in q["evidence"]:
            print(f"  - [{e['code']}] {e['evidence']}")
        ans = input("[a]pprove payment / [r]eject / [h]old for follow-up / [s]kip > ").strip().lower()
        status = {"a": "approved", "r": "rejected", "h": "held", "s": "pending"}.get(ans, "pending")
        if status != "pending":
            q["human_status"] = status
            q["human_reviewer"] = reviewer
            q["reviewed_at"] = datetime.now(timezone.utc).isoformat()
            if status != q["agent_decision"].replace("approve", "approved"):
                q["human_note"] = input("Note (why the change): ").strip()
            _log({"action": "review", "invoice_id": q["invoice_id"],
                  "agent_decision": q["agent_decision"], "human_status": status,
                  "reviewer": reviewer, "note": q["human_note"]})
    QUEUE.write_text(json.dumps(queue, indent=2))
    print("Queue saved.")


def execute() -> None:
    queue = json.loads(QUEUE.read_text())
    approved = [q for q in queue if q["human_status"] == "approved"]
    new_file = not LEDGER.exists()
    with LEDGER.open("a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["posted_at", "invoice_id", "vendor", "po_number", "amount",
                        "currency", "approved_by", "SANDBOX"])
        for q in approved:
            w.writerow([datetime.now(timezone.utc).isoformat(), q["invoice_id"], q["vendor"],
                        q["po_number"], q["total"], q["currency"], q["human_reviewer"],
                        "SIMULATED-NO-REAL-PAYMENT"])
            _log({"action": "sandbox_post", "invoice_id": q["invoice_id"], "amount": q["total"]})
            q["human_status"] = "posted"
    QUEUE.write_text(json.dumps(queue, indent=2))
    print(f"Posted {len(approved)} simulated payments to {LEDGER} (sandbox only).")


def auto_review(decisions_file: str) -> None:
    """Non-interactive review for reproducible demos: apply decisions from a JSON
    file {invoice_id: 'approved'|'rejected'|'held'}. Clearly logged as scripted."""
    queue = json.loads(QUEUE.read_text())
    decisions = json.loads(open(decisions_file).read())
    for q in queue:
        if q["invoice_id"] in decisions and q["human_status"] == "pending":
            q["human_status"] = decisions[q["invoice_id"]]
            q["human_reviewer"] = "scripted-demo-reviewer"
            q["reviewed_at"] = datetime.now(timezone.utc).isoformat()
            _log({"action": "scripted_review", "invoice_id": q["invoice_id"],
                  "human_status": q["human_status"]})
    QUEUE.write_text(json.dumps(queue, indent=2))
    print("Scripted review applied.")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--run", required=True)
    sub.add_parser("review")
    sub.add_parser("execute")
    a = sub.add_parser("auto-review"); a.add_argument("--decisions", required=True)
    args = ap.parse_args()
    if args.cmd == "build":
        build(args.run)
    elif args.cmd == "review":
        review()
    elif args.cmd == "execute":
        execute()
    elif args.cmd == "auto-review":
        auto_review(args.decisions)


if __name__ == "__main__":
    main()
