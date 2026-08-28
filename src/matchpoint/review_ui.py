"""Local web UI for the human approval queue (stdlib only, no dependencies).

Run:  python -m matchpoint.review_ui  [--port 8765]
Then open http://localhost:8765 — approve / hold / reject each invoice.
Actions write to out/approval_queue.json and out/hitl_audit_log.jsonl, same as
the CLI. Payments still only post via `python -m matchpoint.hitl execute`.
"""
from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from .config import OUT
from .hitl import QUEUE, _log

CSS = """
body{margin:0;background:#f6f7fa;color:#1a2233;font:15px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:36px 20px}
h1{font-size:22px;border-bottom:3px solid #1f3a5f;padding-bottom:12px}
.sub{color:#5b6472;font-size:13px;margin-bottom:20px}
.card{background:#fff;border:1px solid #e3e7ee;border-radius:12px;padding:18px 20px;margin:14px 0}
.badge{display:inline-block;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:700}
.b-approve{color:#0e6e3c;background:#e7f5ec}.b-hold{color:#8a5a00;background:#fdf3e0}
.b-reject{color:#9c1f1f;background:#fbe9e9}
.ev{font-size:13px;background:#fbf6ef;border:1px solid #eadfc8;border-radius:8px;padding:8px 12px;margin:8px 0}
.meta{color:#5b6472;font-size:13px}
form{display:inline}
button{border:0;border-radius:8px;padding:8px 16px;margin-right:8px;font-weight:600;cursor:pointer}
.ok{background:#0e6e3c;color:#fff}.hd{background:#8a5a00;color:#fff}.rj{background:#9c1f1f;color:#fff}
.done{color:#5b6472;font-size:13px;font-style:italic}
input[type=text]{border:1px solid #cfd6e0;border-radius:8px;padding:8px;width:280px;margin-right:8px}
.kpi{display:flex;gap:10px;margin:16px 0}
.kpi div{background:#fff;border:1px solid #e3e7ee;border-radius:10px;padding:10px 16px;font-size:13px}
"""


def page() -> str:
    queue = json.loads(QUEUE.read_text()) if QUEUE.exists() else []
    pend = [q for q in queue if q["human_status"] == "pending"]
    done = [q for q in queue if q["human_status"] != "pending"]
    cards = []
    for q in pend:
        ev = "".join(f"<div class='ev'><b>{html.escape(e['code'])}</b> — {html.escape(e['evidence'])}</div>"
                     for e in q.get("evidence") or [])
        badge = {"approve": "b-approve", "hold": "b-hold", "reject": "b-reject"}.get(q["agent_decision"], "b-hold")
        cards.append(f"""
<div class='card'>
 <b>{html.escape(q['invoice_id'])}</b>
 <span class='badge {badge}'>AGENT: {html.escape(q['agent_decision']).upper()}</span>
 <div class='meta'>{html.escape(str(q.get('vendor') or ''))} · PO {html.escape(str(q.get('po_number') or '—'))}
   · {q.get('total')} {html.escape(str(q.get('currency') or ''))} · {html.escape(', '.join(q.get('discrepancies') or []) or 'no discrepancies')}</div>
 <div class='meta' style='margin:6px 0'>{html.escape(q.get('explanation') or '')}</div>
 {ev}
 <form method='post' action='/act'>
   <input type='hidden' name='id' value='{html.escape(q['invoice_id'])}'>
   <input type='text' name='note' placeholder='note (required if overriding agent)'>
   <button class='ok' name='status' value='approved'>Approve payment</button>
   <button class='hd' name='status' value='held'>Hold</button>
   <button class='rj' name='status' value='rejected'>Reject</button>
 </form>
</div>""")
    hist = "".join(f"<div class='card done'>{html.escape(q['invoice_id'])} — {html.escape(q['human_status'])} "
                   f"by {html.escape(str(q.get('human_reviewer') or ''))}"
                   + (f" — “{html.escape(q['human_note'])}”" if q.get("human_note") else "") + "</div>"
                   for q in done)
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>Matchpoint — Approval Queue</title>
<style>{CSS}</style></head><body><div class='wrap'>
<h1>Matchpoint — Human Approval Queue</h1>
<div class='sub'>Qualified-reviewer checkpoint. Nothing is paid until approved here; payments post only to the sandbox ledger.</div>
<div class='kpi'><div><b>{len(pend)}</b> pending</div><div><b>{len(done)}</b> reviewed</div></div>
{''.join(cards) or "<div class='card done'>Queue empty — build it with: python -m matchpoint.hitl build --run agent_final</div>"}
<h1 style='font-size:17px;margin-top:34px'>Review history</h1>
{hist or "<div class='card done'>none yet</div>"}
</div></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = page().encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if urlparse(self.path).path != "/act":
            self.send_response(404); self.end_headers(); return
        length = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(length).decode())
        inv_id = form.get("id", [""])[0]
        status = form.get("status", [""])[0]
        note = form.get("note", [""])[0].strip() or None
        queue = json.loads(QUEUE.read_text())
        for q in queue:
            if q["invoice_id"] == inv_id and q["human_status"] == "pending":
                q["human_status"] = status
                q["human_reviewer"] = "web-reviewer"
                q["human_note"] = note
                q["reviewed_at"] = datetime.now(timezone.utc).isoformat()
                _log({"action": "web_review", "invoice_id": inv_id,
                      "agent_decision": q["agent_decision"], "human_status": status, "note": note})
        QUEUE.write_text(json.dumps(queue, indent=2))
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def log_message(self, *a):  # quiet
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    print(f"Approval queue UI: http://localhost:{args.port}  (Ctrl-C to stop)")
    HTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
