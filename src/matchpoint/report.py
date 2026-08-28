"""Renders the batch Audit Packet — the artifact the AP specialist actually
uses: one self-contained HTML file with every decision, its evidence, the
checks that passed, and the human-review trail.

Run:  python -m matchpoint.report --run agent_final
"""
from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone

from .config import OUT

BADGE = {
    "approve": ("READY TO PAY", "#0e6e3c", "#e7f5ec"),
    "hold": ("HOLD — INVESTIGATE", "#8a5a00", "#fdf3e0"),
    "reject": ("REJECT — DO NOT PAY", "#9c1f1f", "#fbe9e9"),
    "error": ("PIPELINE ERROR", "#555", "#eee"),
}

CSS = """
:root { --ink:#1a2233; --muted:#5b6472; --line:#e3e7ee; --bg:#f6f7fa; --card:#ffffff; --accent:#1f3a5f; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
.wrap { max-width:980px; margin:0 auto; padding:48px 28px 80px; }
header.masthead { border-bottom:3px solid var(--accent); padding-bottom:18px; margin-bottom:28px; }
.masthead h1 { margin:0; font-size:26px; letter-spacing:.2px; }
.masthead .sub { color:var(--muted); margin-top:6px; font-size:13.5px; }
.kpis { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin:26px 0 34px; }
.kpi { background:var(--card); border:1px solid var(--line); border-radius:10px; padding:14px 16px; }
.kpi .n { font-size:24px; font-weight:700; }
.kpi .l { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.6px; margin-top:2px; }
table.sum { width:100%; border-collapse:collapse; background:var(--card); border:1px solid var(--line);
  border-radius:10px; overflow:hidden; font-size:13.5px; }
table.sum th { text-align:left; background:var(--accent); color:#fff; padding:9px 12px; font-weight:600; }
table.sum td { padding:8px 12px; border-top:1px solid var(--line); }
.badge { display:inline-block; padding:2px 10px; border-radius:20px; font-size:11.5px; font-weight:700; letter-spacing:.4px; }
.inv { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:22px 24px; margin:18px 0; page-break-inside:avoid; }
.inv h3 { margin:0 0 4px; font-size:17px; }
.inv .meta { color:var(--muted); font-size:13px; margin-bottom:12px; }
.ev { margin:10px 0 0; padding:12px 14px; border-radius:8px; background:#fbf6ef; border:1px solid #eadfc8; }
.ev.clean { background:#f2f8f4; border-color:#d5e8dc; }
.ev b.code { font-family:ui-monospace,Menlo,monospace; font-size:12px; }
ul.checks { color:var(--muted); font-size:13px; margin:10px 0 0; padding-left:20px; }
.expl { margin-top:10px; font-size:14px; }
.hr { border:none; border-top:1px solid var(--line); margin:34px 0 26px; }
.sig { display:flex; gap:60px; margin-top:40px; }
.sig .line { flex:1; border-top:1px solid var(--ink); padding-top:6px; font-size:12.5px; color:var(--muted); }
footer { color:var(--muted); font-size:12px; margin-top:44px; }
@media print { body{background:#fff} .inv{border-color:#bbb} }
"""


def money(x, cur):
    if x is None:
        return "—"
    sym = {"USD": "$", "EUR": "€", "GBP": "£"}.get(cur or "USD", "")
    return f"{sym}{x:,.2f}"


def render(run: str) -> None:
    results = json.loads((OUT / "runs" / run / "results.json").read_text())
    queue_path = OUT / "approval_queue.json"
    human = {}
    if queue_path.exists():
        for q in json.loads(queue_path.read_text()):
            if q.get("source_run") == run:
                human[q["invoice_id"]] = q

    n = len(results)
    n_app = sum(1 for r in results if r["decision"] == "approve")
    n_hold = sum(1 for r in results if r["decision"] == "hold")
    n_rej = sum(1 for r in results if r["decision"] == "reject")
    val_ok = sum((r.get("extracted") or {}).get("total") or 0 for r in results
                 if r["decision"] == "approve" and (r.get("extracted") or {}).get("currency") == "USD")
    val_flag = sum((r.get("extracted") or {}).get("total") or 0 for r in results
                   if r["decision"] != "approve" and (r.get("extracted") or {}).get("currency") == "USD")

    now = datetime.now(timezone.utc).strftime("%B %d, %Y %H:%M UTC")
    rows, cards = [], []
    order = {"reject": 0, "hold": 1, "error": 2, "approve": 3}
    for r in sorted(results, key=lambda x: (order.get(x["decision"], 9), x["invoice_id"])):
        ex = r.get("extracted") or {}
        label, fg, bg = BADGE.get(r["decision"], BADGE["error"])
        h = human.get(r["invoice_id"], {})
        hstat = h.get("human_status", "—")
        rows.append(
            f"<tr><td><a href='#i{html.escape(r['invoice_id'])}' style='color:var(--accent)'>"
            f"{html.escape(r['invoice_id'])}</a></td>"
            f"<td>{html.escape(str(ex.get('vendor_name') or '—'))}</td>"
            f"<td>{html.escape(str(r.get('po_number') or ex.get('po_number') or '—'))}</td>"
            f"<td style='text-align:right'>{money(ex.get('total'), ex.get('currency'))}</td>"
            f"<td><span class='badge' style='color:{fg};background:{bg}'>{label}</span></td>"
            f"<td>{html.escape(', '.join(r.get('discrepancies') or []) or '—')}</td>"
            f"<td>{html.escape(str(hstat))}</td></tr>")

        ev_html = ""
        for e in r.get("engine_evidence") or []:
            ev_html += (f"<div class='ev'><b class='code'>{html.escape(e['code'])}</b> — "
                        f"{html.escape(e['evidence'])}</div>")
        if not ev_html and r["decision"] == "approve":
            ev_html = "<div class='ev clean'>All three-way-match checks passed. No discrepancies.</div>"
        checks = "".join(f"<li>{html.escape(c)}</li>" for c in (r.get("checks_passed") or [])[:10])
        hu = ""
        if h and h.get("human_status") not in (None, "pending"):
            hu = (f"<div class='expl'><b>Human review:</b> {html.escape(str(h.get('human_status')))} "
                  f"by {html.escape(str(h.get('human_reviewer')))} at {html.escape(str(h.get('reviewed_at') or ''))}"
                  + (f" — “{html.escape(h['human_note'])}”" if h.get("human_note") else "") + "</div>")
        cards.append(f"""
<div class='inv' id='i{html.escape(r['invoice_id'])}'>
  <h3>{html.escape(r['invoice_id'])} <span class='badge' style='color:{fg};background:{bg};margin-left:8px'>{label}</span></h3>
  <div class='meta'>{html.escape(str(ex.get('vendor_name') or ''))} &nbsp;·&nbsp; PO {html.escape(str(r.get('po_number') or '—'))}
   &nbsp;·&nbsp; Invoice date {html.escape(str(ex.get('date') or '—'))} &nbsp;·&nbsp; Total {money(ex.get('total'), ex.get('currency'))} {html.escape(str(ex.get('currency') or ''))}</div>
  {ev_html}
  <div class='expl'><b>Analyst summary:</b> {html.escape(r.get('explanation') or '')}</div>
  {f"<ul class='checks'>{checks}</ul>" if checks else ""}
  {hu}
</div>""")

    page = f"""<!doctype html><html><head><meta charset='utf-8'>
<title>AP Audit Packet — {html.escape(run)}</title><style>{CSS}</style></head><body><div class='wrap'>
<header class='masthead'>
  <h1>Accounts Payable — Invoice Audit Packet</h1>
  <div class='sub'>Harborview Manufacturing Inc. · Batch of {n} supplier invoices · Generated {now}
  · Pipeline run <b>{html.escape(run)}</b> · Every flag below is backed by a deterministic check; no payment is executed without human sign-off.</div>
</header>
<div class='kpis'>
  <div class='kpi'><div class='n'>{n}</div><div class='l'>Invoices</div></div>
  <div class='kpi'><div class='n' style='color:#0e6e3c'>{n_app}</div><div class='l'>Ready to pay</div></div>
  <div class='kpi'><div class='n' style='color:#8a5a00'>{n_hold}</div><div class='l'>On hold</div></div>
  <div class='kpi'><div class='n' style='color:#9c1f1f'>{n_rej}</div><div class='l'>Rejected</div></div>
  <div class='kpi'><div class='n'>{money(val_flag, 'USD')}</div><div class='l'>USD value flagged</div></div>
</div>
<table class='sum'>
<tr><th>Invoice</th><th>Vendor</th><th>PO</th><th style='text-align:right'>Total</th><th>Decision</th><th>Discrepancies</th><th>Human review</th></tr>
{''.join(rows)}
</table>
<hr class='hr'>
<h2 style='font-size:19px'>Case detail &amp; evidence</h2>
{''.join(cards)}
<div class='sig'>
  <div class='line'>AP Specialist — reviewed &amp; released</div>
  <div class='line'>AP Manager — batch approval</div>
  <div class='line'>Date</div>
</div>
<footer>Methodology: invoices OCR'd (Mistral OCR), structured by an extraction agent, matched 2-way/3-way
against PO, GRN, vendor master and payment history by a tool-using matching agent, independently recomputed
by a deterministic verification engine, and queued for human approval. Payments are simulated in a sandbox
ledger only. Generated by Matchpoint.</footer>
</div></body></html>"""
    out = OUT / f"audit_packet_{run}.html"
    out.write_text(page)
    print(f"Wrote {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    args = ap.parse_args()
    render(args.run)
