"""Deterministic ERP tools and the 3-way match engine.

Design principle: the LLM never does arithmetic. Extraction and judgment are
LLM work; lookups, sums, tolerances and duplicate detection are plain code
that returns auditable evidence.
"""
from __future__ import annotations

import re

PRICE_TOL = 0.005   # 0.5% relative
AMOUNT_TOL = 0.02   # $0.02 absolute


# ------------------------------------------------------------- lookups ------

def get_po(world: dict, po_number: str) -> dict | None:
    return next((p for p in world["pos"] if p["po_number"] == po_number), None)


def get_grns_for_po(world: dict, po_number: str) -> list[dict]:
    return [g for g in world["grns"] if g["po_number"] == po_number]


def received_totals(world: dict, po_number: str) -> dict[int, int]:
    """Total received qty per PO line_no across ALL GRNs (partial deliveries sum)."""
    totals: dict[int, int] = {}
    for g in get_grns_for_po(world, po_number):
        for ln in g["lines"]:
            totals[ln["line_no"]] = totals.get(ln["line_no"], 0) + ln["qty_received"]
    return totals


def get_vendor(world: dict, vendor_id: str) -> dict | None:
    return next((v for v in world["vendors"] if v["vendor_id"] == vendor_id), None)


def find_vendor_by_name(world: dict, name: str, memory: dict | None = None) -> dict | None:
    """Resolve a display name to a vendor. Exact, then memory aliases, then fuzzy."""
    norm = _norm_name(name)
    for v in world["vendors"]:
        if _norm_name(v["name"]) == norm:
            return v
    if memory:
        for vid, m in memory.items():
            if any(_norm_name(a) == norm for a in m.get("known_aliases", [])):
                return get_vendor(world, vid)
    # fuzzy: token overlap
    best, best_score = None, 0.0
    toks = set(norm.split())
    for v in world["vendors"]:
        vt = set(_norm_name(v["name"]).split())
        score = len(toks & vt) / max(len(toks | vt), 1)
        if score > best_score:
            best, best_score = v, score
    return best if best_score >= 0.4 else None


def _norm_name(s: str) -> str:
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    drop = {"llc", "inc", "co", "ltd", "gmbh", "corp", "company", "the", "a", "of", "div", "pvt"}
    return " ".join(t for t in s.split() if t and t not in drop)


def _norm_invno(s: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", s.upper())


def search_payments(world: dict, vendor_id: str | None, po_number: str | None,
                    total: float | None, invoice_no: str | None) -> list[dict]:
    """Return payment-history records that suggest this invoice was already paid."""
    hits = []
    for p in world["payments"]:
        reasons = []
        if invoice_no and _norm_invno(p["invoice_no"]) == _norm_invno(invoice_no):
            reasons.append("invoice number already paid (normalized match)")
        if (vendor_id and po_number and total is not None
                and p["vendor_id"] == vendor_id and p["po_number"] == po_number
                and abs(p["amount"] - total) <= AMOUNT_TOL):
            reasons.append("same vendor + PO + amount already paid")
        if reasons:
            hits.append({**p, "match_reasons": reasons})
    return hits


# --------------------------------------------------------- match engine -----

def match_engine(inv: dict, world: dict, memory: dict | None = None) -> dict:
    """Full deterministic 3-way match on an extracted invoice dict.

    Returns {vendor_id, decision, discrepancies: [{code, evidence}], checks: [...]}.
    Every discrepancy carries the concrete numbers that prove it.
    """
    disc: list[dict] = []
    checks: list[str] = []

    def add(code: str, evidence: str) -> None:
        disc.append({"code": code, "evidence": evidence})

    po = get_po(world, inv.get("po_number", ""))
    vendor = None
    if po:
        vendor = get_vendor(world, po["vendor_id"])
        checks.append(f"PO {po['po_number']} found (vendor {po['vendor_id']}).")
    else:
        add("PO_NOT_FOUND", f"PO '{inv.get('po_number')}' not present in the PO system.")
        vendor = find_vendor_by_name(world, inv.get("vendor_name", ""), memory)

    # vendor-name consistency note (aliases are legitimate per policy)
    if po and vendor:
        named = find_vendor_by_name(world, inv.get("vendor_name", ""), memory)
        if named and named["vendor_id"] != vendor["vendor_id"]:
            checks.append(f"NOTE: invoice name '{inv.get('vendor_name')}' resolved to "
                          f"{named['vendor_id']} but PO belongs to {vendor['vendor_id']}.")
        elif not named:
            checks.append(f"NOTE: invoice name '{inv.get('vendor_name')}' is not an exact "
                          f"vendor-master match; treating as trade name of {vendor['vendor_id']} "
                          f"based on PO linkage.")

    # ---- line-level checks --------------------------------------------------
    lines = inv.get("lines") or []
    if po:
        recv = received_totals(world, po["po_number"])
        grn_exists = bool(get_grns_for_po(world, po["po_number"]))
        if not grn_exists:
            add("GRN_MISSING", f"No goods receipt notes exist for {po['po_number']}.")
        po_by_sku = {ln["sku"]: ln for ln in po["lines"]}
        for ln in lines:
            pln = po_by_sku.get(ln.get("sku"))
            if not pln:
                checks.append(f"Line SKU {ln.get('sku')} not on PO — flagged as price check impossible.")
                add("PRICE_MISMATCH", f"SKU {ln.get('sku')} billed but not present on {po['po_number']}.")
                continue
            # price
            if pln["unit_price"] > 0:
                rel = abs(ln["unit_price"] - pln["unit_price"]) / pln["unit_price"]
                if rel > PRICE_TOL:
                    add("PRICE_MISMATCH",
                        f"SKU {ln['sku']}: billed {ln['unit_price']:.2f} vs PO {pln['unit_price']:.2f} "
                        f"({rel * 100:.1f}% > {PRICE_TOL * 100:.1f}% tolerance).")
                else:
                    checks.append(f"SKU {ln['sku']}: price OK ({ln['unit_price']:.2f}).")
            # qty vs received
            if grn_exists:
                got = recv.get(pln["line_no"], 0)
                if ln["qty"] > got:
                    add("QTY_MISMATCH",
                        f"SKU {ln['sku']}: billed qty {ln['qty']} > received {got} "
                        f"(summed across {len(get_grns_for_po(world, po['po_number']))} GRN(s)).")
                else:
                    checks.append(f"SKU {ln['sku']}: qty OK ({ln['qty']} <= received {got}).")

    # ---- arithmetic ---------------------------------------------------------
    for ln in lines:
        expect = round(ln["qty"] * ln["unit_price"], 2)
        if abs(expect - ln["amount"]) > AMOUNT_TOL:
            add("TOTAL_ERROR",
                f"Line {ln.get('sku')}: amount {ln['amount']:.2f} != qty {ln['qty']} x "
                f"unit price {ln['unit_price']:.2f} = {expect:.2f}.")
    line_sum = round(sum(ln["amount"] for ln in lines), 2)
    if inv.get("subtotal") is not None and abs(line_sum - inv["subtotal"]) > AMOUNT_TOL:
        add("TOTAL_ERROR", f"Subtotal {inv['subtotal']:.2f} != sum of line amounts {line_sum:.2f}.")
    if vendor and inv.get("subtotal") is not None and inv.get("tax") is not None:
        expect_tax = round(inv["subtotal"] * vendor["tax_rate"], 2)
        if abs(expect_tax - inv["tax"]) > AMOUNT_TOL:
            add("TAX_ERROR",
                f"Tax {inv['tax']:.2f} != tax_rate {vendor['tax_rate']:.4f} x subtotal "
                f"{inv['subtotal']:.2f} = {expect_tax:.2f} (tolerance $0.02).")
        else:
            checks.append(f"Tax OK ({inv['tax']:.2f} ~= {expect_tax:.2f}).")
    if inv.get("total") is not None and inv.get("subtotal") is not None and inv.get("tax") is not None:
        expect_total = round(inv["subtotal"] + inv["tax"], 2)
        if abs(expect_total - inv["total"]) > AMOUNT_TOL:
            add("TOTAL_ERROR", f"Total {inv['total']:.2f} != subtotal + tax = {expect_total:.2f}.")

    # ---- currency, bank, duplicates ------------------------------------------
    if po and inv.get("currency") and inv["currency"] != po["currency"]:
        add("CURRENCY_MISMATCH", f"Invoice currency {inv['currency']} != PO currency {po['currency']}.")
    if vendor:
        inv_acct = re.sub(r"\s", "", str(inv.get("bank_account") or ""))
        mast_acct = re.sub(r"\s", "", vendor["bank_account"])
        inv_rout = re.sub(r"\s", "", str(inv.get("bank_routing") or ""))
        mast_rout = re.sub(r"\s", "", vendor["bank_routing"])
        if inv_acct and inv_acct != mast_acct:
            add("BANK_CHANGE", f"Remit-to account {inv.get('bank_account')} != vendor master "
                               f"{vendor['bank_account']} — verify with vendor before payment.")
        elif inv_rout and inv_rout != mast_rout:
            add("BANK_CHANGE", f"Remit-to routing {inv.get('bank_routing')} != vendor master "
                               f"{vendor['bank_routing']}.")
        else:
            checks.append("Remit-to bank details match vendor master.")
        dups = search_payments(world, vendor["vendor_id"], inv.get("po_number"),
                               inv.get("total"), inv.get("invoice_no"))
        for d in dups:
            add("DUPLICATE", f"Paid {d['paid_date']} as {d['invoice_no']} "
                             f"({d['amount']:.2f} {d['currency']}): {'; '.join(d['match_reasons'])}.")

    codes = sorted({d["code"] for d in disc})
    decision = "reject" if "DUPLICATE" in codes else ("hold" if codes else "approve")
    return {
        "vendor_id": vendor["vendor_id"] if vendor else None,
        "decision": decision,
        "discrepancy_codes": codes,
        "discrepancies": disc,
        "checks_passed": checks,
    }
