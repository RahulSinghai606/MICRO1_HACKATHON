"""Synthetic AP dataset generator for Matchpoint.

Generates a fully self-contained, shareable evaluation world:
  - data/erp/vendors.json        vendor master (bank details, terms, currency)
  - data/erp/pos.json            purchase orders
  - data/erp/grns.json           goods receipt notes (some partial, some missing)
  - data/erp/payments.json       payment history (for duplicate detection)
  - data/invoices/png/*.png      30 rendered invoice images (3 layout templates)
  - data/gold/labels.json        ground-truth decision + discrepancy codes per invoice
  - data/gold/cases.md           human-readable description of every seeded case

Everything is deterministic (seed 42). No real people, companies or data.

Run:  python data/generate.py
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ERP = ROOT / "data" / "erp"
PNG = ROOT / "data" / "invoices" / "png"
GOLD = ROOT / "data" / "gold"

rng = random.Random(42)

# ---------------------------------------------------------------- vendors ---

VENDORS = [
    # id, canonical name, invoice display name (sometimes an alias), city, currency, inv prefix, template
    ("V01", "Northgate Industrial Supply LLC", "Northgate Industrial Supply LLC", "Columbus, OH", "USD", "NIS-2025-", "A"),
    ("V02", "Bluefin Packaging Co.", "Bluefin Packaging Co.", "Savannah, GA", "USD", "INV-2025-0", "B"),
    ("V03", "Meridian Fasteners Inc.", "Meridian Fasteners Inc.", "Erie, PA", "USD", "MF/25/", "C"),
    ("V04", "Cascadia Chemical Works", "Cascadia Chemical Works", "Tacoma, WA", "USD", "CCW-", "A"),
    ("V05", "Helios Electrical Components", "Helios Electrical Components", "Tucson, AZ", "USD", "HEC-2025-", "B"),
    ("V06", "Auriga Logistics Services", "Auriga Logistics Services", "Memphis, TN", "USD", "ALS-INV-", "C"),
    ("V07", "Stellar Office Interiors", "Stellar Office Interiors", "Denver, CO", "USD", "SOI-25-", "A"),
    ("V08", "Granite Peak Safety Gear", "Granite Peak Safety Gear", "Boise, ID", "USD", "GP-", "B"),
    ("V09", "Vireo Print & Label GmbH", "Vireo Print & Label GmbH", "Hamburg, DE", "EUR", "VPL-2025-", "C"),
    ("V10", "Ashford Machine Tools Ltd.", "Ashford Machine Tools Ltd.", "Sheffield, UK", "USD", "AMT-", "A"),
]

CATALOG = {
    "V01": [("NG-4410", "Nitrile work gloves, box of 100", 18.40), ("NG-7720", "Safety goggles, anti-fog", 6.95),
            ("NG-1180", "Steel shelving unit 72in", 149.00), ("NG-3305", "Absorbent pads, case", 42.50)],
    "V02": [("BP-201", "Corrugated boxes 18x12x10, bundle 25", 31.25), ("BP-115", "Stretch wrap roll 80ga", 12.80),
            ("BP-330", "Packing tape, case of 36", 58.90), ("BP-450", "Foam inserts, custom cut", 4.15)],
    "V03": [("MF-M8-50", "Hex bolts M8x50 zinc, box 500", 44.00), ("MF-M8-NUT", "Hex nuts M8 zinc, box 1000", 27.60),
            ("MF-W-8", "Flat washers 8mm, box 1000", 15.30), ("MF-ANC-10", "Concrete anchors 10mm, box 100", 62.75)],
    "V04": [("CC-IPA-55", "Isopropyl alcohol 99%, 55gal drum", 612.00), ("CC-DEG-5", "Industrial degreaser, 5gal", 87.40),
            ("CC-COOL-55", "Machine coolant concentrate, 55gal", 744.50)],
    "V05": [("HE-CB-20", "Circuit breaker 20A DIN", 9.85), ("HE-REL-24", "Relay 24VDC 8-pin", 14.20),
            ("HE-CAB-14", "Copper cable 14AWG, 500ft spool", 118.00), ("HE-PSU-24", "PSU 24V 10A DIN rail", 96.30)],
    "V06": [("AL-LTL-STD", "LTL freight, standard lane", 425.00), ("AL-FUEL", "Fuel surcharge", 63.75),
            ("AL-LIFT", "Liftgate service", 45.00), ("AL-WHS-P", "Warehouse handling, per pallet", 18.50)],
    "V07": [("SO-CHR-T2", "Task chair, mesh back", 189.00), ("SO-DSK-60", "Sit-stand desk 60in", 415.00),
            ("SO-MON-ARM", "Dual monitor arm", 74.25), ("SO-FIL-3D", "File cabinet 3-drawer", 156.80)],
    "V08": [("GP-HH-CL2", "Hard hats class E, box 20", 196.00), ("GP-VIS-XL", "Hi-vis vests XL, pack 10", 84.50),
            ("GP-BOOT-10", "Steel toe boots size 10", 112.00), ("GP-EAR-200", "Ear plugs, box 200 pr", 38.90)],
    "V09": [("VP-LBL-4x6", "Thermal labels 4x6, roll 500", 21.40), ("VP-TAG-ASSET", "Asset tags, custom, 1000", 340.00),
            ("VP-RIB-110", "TTR ribbon 110mm", 9.60)],
    "V10": [("AM-END-12", "End mill 12mm carbide", 68.20), ("AM-VIS-6", "Machine vise 6in", 289.00),
            ("AM-CHK-125", "Lathe chuck 125mm", 412.60), ("AM-INS-CNMG", "Turning inserts CNMG, box 10", 94.80)],
}

BANKS = {
    "V01": ("First Commerce Bank", "021000021", "4402198837"),
    "V02": ("Coastal Georgia Bank", "061000104", "7719045512"),
    "V03": ("Keystone National", "031000503", "5583920164"),
    "V04": ("Puget Sound Trust", "125000024", "9027481133"),
    "V05": ("Desert West Bank", "122100024", "3348812706"),
    "V06": ("River City Bank", "084000026", "6650371928"),
    "V07": ("Front Range Credit Union", "107000233", "8812204575"),
    "V08": ("Sawtooth Community Bank", "123103729", "2290156841"),
    "V09": ("Hansa Handelsbank", "DE44 5001 0517", "5407 3249 31"),
    "V10": ("Pennine & Yorkshire Bank", "GB29 NWBK 6016", "1331 9268 19"),
}

TAX_RATES = {"V01": 0.0725, "V02": 0.07, "V03": 0.06, "V04": 0.095, "V05": 0.086,
             "V06": 0.0, "V07": 0.081, "V08": 0.06, "V09": 0.19, "V10": 0.0}


def money(x: float) -> float:
    return round(x + 1e-9, 2)


# ------------------------------------------------------------------- POs ----

def build_world():
    vendors = []
    for vid, name, disp, city, cur, prefix, tmpl in VENDORS:
        bank, routing, acct = BANKS[vid]
        vendors.append({
            "vendor_id": vid, "name": name, "city": city, "currency": cur,
            "payment_terms": rng.choice(["Net 30", "Net 45", "Net 60"]),
            "bank_name": bank, "bank_routing": routing, "bank_account": acct,
            "tax_rate": TAX_RATES[vid],
        })

    pos, grns = [], []
    po_seq = 4101
    grn_seq = 88301

    def add_po(vid: str, n_lines: int, qty_range=(2, 40)) -> dict:
        nonlocal po_seq
        items = rng.sample(CATALOG[vid], min(n_lines, len(CATALOG[vid])))
        lines = []
        for i, (sku, desc, price) in enumerate(items, 1):
            lines.append({"line_no": i, "sku": sku, "description": desc,
                          "qty": rng.randint(*qty_range), "unit_price": price})
        po = {"po_number": f"PO-2025-{po_seq}", "vendor_id": vid,
              "date": f"2025-{rng.randint(4, 6):02d}-{rng.randint(1, 28):02d}",
              "currency": next(v["currency"] for v in vendors if v["vendor_id"] == vid),
              "lines": lines, "status": "open"}
        pos.append(po)
        po_seq += 1
        return po

    def add_grn(po: dict, fraction=1.0, split=False):
        nonlocal grn_seq
        if split:
            # two partial receipts that sum to the full ordered qty
            for part in (0.5, 0.5):
                lines = []
                for ln in po["lines"]:
                    q = ln["qty"] // 2 if part == 0.5 and not lines_done(ln, grns, po) else ln["qty"] - ln["qty"] // 2
                    lines.append({"line_no": ln["line_no"], "sku": ln["sku"], "qty_received": q})
                grns.append({"grn_number": f"GRN-{grn_seq}", "po_number": po["po_number"],
                             "date": po["date"], "lines": lines})
                grn_seq += 1
            return
        lines = [{"line_no": ln["line_no"], "sku": ln["sku"],
                  "qty_received": int(ln["qty"] * fraction)} for ln in po["lines"]]
        grns.append({"grn_number": f"GRN-{grn_seq}", "po_number": po["po_number"],
                     "date": po["date"], "lines": lines})
        grn_seq += 1

    def lines_done(ln, grns, po):
        got = sum(g_ln["qty_received"] for g in grns if g["po_number"] == po["po_number"]
                  for g_ln in g["lines"] if g_ln["line_no"] == ln["line_no"])
        return got > 0

    return vendors, pos, grns, add_po, add_grn


# -------------------------------------------------------------- invoices ----

def invoice_from_po(po: dict, vendors: list, inv_no: str, date: str) -> dict:
    v = next(x for x in vendors if x["vendor_id"] == po["vendor_id"])
    lines = [{"sku": ln["sku"], "description": ln["description"],
              "qty": ln["qty"], "unit_price": ln["unit_price"],
              "amount": money(ln["qty"] * ln["unit_price"])} for ln in po["lines"]]
    subtotal = money(sum(ln["amount"] for ln in lines))
    tax = money(subtotal * v["tax_rate"])
    return {
        "invoice_no": inv_no, "vendor_id": v["vendor_id"], "vendor_display_name": v["name"],
        "date": date, "po_number": po["po_number"], "currency": po["currency"],
        "lines": lines, "subtotal": subtotal, "tax_rate": v["tax_rate"], "tax": tax,
        "total": money(subtotal + tax),
        "bank_name": v["bank_name"], "bank_routing": v["bank_routing"], "bank_account": v["bank_account"],
        "payment_terms": v["payment_terms"], "template": next(t for vid, *_r, t in
                                                              [(a, b, c, d, e, f, g) for a, b, c, d, e, f, g in VENDORS]
                                                              if vid == v["vendor_id"]),
    }


def main():
    vendors, pos, grns, add_po, add_grn = build_world()
    invoices, gold, case_notes = [], {}, []
    payments = []

    def note(inv_id, txt):
        case_notes.append((inv_id, txt))

    def gold_entry(inv_id, decision, discrepancies, po_number, explanation):
        gold[inv_id] = {"decision": decision, "discrepancies": sorted(discrepancies),
                        "po_number": po_number, "explanation": explanation}

    inv_counter = {vid: 101 for vid, *_ in VENDORS}

    def next_inv_no(vid):
        prefix = next(p for v, *_x, p, _t in [(a, b, c, d, e, f, g) for a, b, c, d, e, f, g in VENDORS] if v == vid)
        n = inv_counter[vid]
        inv_counter[vid] += 3
        return f"{prefix}{n}"

    def make(vid, n_lines=None, date=None):
        po = add_po(vid, n_lines or rng.randint(2, 4))
        d = date or f"2025-{rng.randint(6, 7):02d}-{rng.randint(1, 28):02d}"
        return po, invoice_from_po(po, vendors, next_inv_no(vid), d)

    # ---- 12 CLEAN invoices (some deliberately tricky-but-legitimate) -------
    clean_vids = ["V01", "V02", "V03", "V04", "V05", "V06", "V07", "V08", "V09", "V10", "V01", "V05"]
    for i, vid in enumerate(clean_vids):
        po, inv = make(vid)
        if i == 10:
            # CHALLENGING CLEAN #1: vendor invoices under a slightly different
            # trade name + goods arrived across two partial GRNs.
            inv["vendor_display_name"] = "Northgate Ind. Supply (a div. of NIS Holdings)"
            add_grn(po, split=True)
            note(inv["invoice_no"], "CHALLENGING: alias vendor name + two partial GRNs summing to full qty. Legitimate — must APPROVE.")
            gold_entry(inv["invoice_no"], "approve", [], po["po_number"],
                       "Alias trade name and split GRNs are legitimate; totals match PO within tolerance.")
        elif i == 11:
            # CHALLENGING CLEAN #2: 1-cent rounding difference on tax.
            inv["tax"] = money(inv["tax"] + 0.01)
            inv["total"] = money(inv["subtotal"] + inv["tax"])
            add_grn(po)
            note(inv["invoice_no"], "CHALLENGING: tax rounded up by $0.01 (within ±$0.02 tolerance). Must APPROVE.")
            gold_entry(inv["invoice_no"], "approve", [], po["po_number"],
                       "One-cent tax rounding is within policy tolerance (±$0.02).")
        else:
            add_grn(po)
            gold_entry(inv["invoice_no"], "approve", [], po["po_number"], "Clean 3-way match.")
        invoices.append(inv)

    # ---- 3 PRICE_MISMATCH ---------------------------------------------------
    for vid, bump in [("V03", 0.12), ("V07", 0.08), ("V10", 0.15)]:
        po, inv = make(vid)
        add_grn(po)
        ln = inv["lines"][0]
        ln["unit_price"] = money(ln["unit_price"] * (1 + bump))
        ln["amount"] = money(ln["qty"] * ln["unit_price"])
        inv["subtotal"] = money(sum(l["amount"] for l in inv["lines"]))
        inv["tax"] = money(inv["subtotal"] * inv["tax_rate"])
        inv["total"] = money(inv["subtotal"] + inv["tax"])
        note(inv["invoice_no"], f"Unit price on line 1 raised {int(bump*100)}% above PO.")
        gold_entry(inv["invoice_no"], "hold", ["PRICE_MISMATCH"], po["po_number"],
                   f"Line 1 unit price is {int(bump*100)}% above the PO price.")
        invoices.append(inv)

    # ---- 3 QTY_MISMATCH (billed > received) ---------------------------------
    for vid in ["V02", "V05", "V08"]:
        po, inv = make(vid)
        add_grn(po, fraction=0.6)  # only 60% of goods received
        note(inv["invoice_no"], "Invoice bills full PO qty but only ~60% received on GRN.")
        gold_entry(inv["invoice_no"], "hold", ["QTY_MISMATCH"], po["po_number"],
                   "Billed quantity exceeds received quantity on the goods receipt.")
        invoices.append(inv)

    # ---- 2 GRN_MISSING --------------------------------------------------------
    for vid in ["V04", "V06"]:
        po, inv = make(vid)
        # no GRN at all
        note(inv["invoice_no"], "No goods receipt exists for the referenced PO.")
        gold_entry(inv["invoice_no"], "hold", ["GRN_MISSING"], po["po_number"],
                   "No goods receipt note found for this PO; cannot verify delivery.")
        invoices.append(inv)

    # ---- 2 DUPLICATE ----------------------------------------------------------
    # (a) same vendor, same PO, already paid under differently-formatted number
    po, inv = make("V02")
    add_grn(po)
    paid_no = inv["invoice_no"].replace("INV-2025-0", "INV-25-")
    payments.append({"invoice_no": paid_no, "vendor_id": "V02", "po_number": po["po_number"],
                     "amount": inv["total"], "currency": inv["currency"], "paid_date": "2025-06-14"})
    note(inv["invoice_no"], f"CHALLENGING: duplicate of already-paid {paid_no} (same PO + amount, different number format).")
    gold_entry(inv["invoice_no"], "reject", ["DUPLICATE"], po["po_number"],
               f"Same vendor, PO and amount already paid on 2025-06-14 as {paid_no}.")
    invoices.append(inv)
    # (b) plain duplicate: identical number already in payment history
    po, inv = make("V06")
    add_grn(po)
    payments.append({"invoice_no": inv["invoice_no"], "vendor_id": "V06", "po_number": po["po_number"],
                     "amount": inv["total"], "currency": inv["currency"], "paid_date": "2025-07-02"})
    note(inv["invoice_no"], "Exact duplicate — same invoice number already paid.")
    gold_entry(inv["invoice_no"], "reject", ["DUPLICATE"], po["po_number"],
               "Invoice number already appears in payment history (paid 2025-07-02).")
    invoices.append(inv)

    # ---- 2 TAX_ERROR ----------------------------------------------------------
    for vid, delta in [("V01", 37.14), ("V09", 52.60)]:
        po, inv = make(vid)
        add_grn(po)
        inv["tax"] = money(inv["tax"] + delta)
        inv["total"] = money(inv["subtotal"] + inv["tax"])
        note(inv["invoice_no"], f"Tax overstated by {delta} vs rate x subtotal.")
        gold_entry(inv["invoice_no"], "hold", ["TAX_ERROR"], po["po_number"],
                   f"Tax amount exceeds tax_rate x subtotal by {delta}.")
        invoices.append(inv)

    # ---- 2 TOTAL_ERROR (line arithmetic wrong) --------------------------------
    for vid, delta in [("V07", 90.00), ("V03", 28.00)]:
        po, inv = make(vid)
        add_grn(po)
        ln = inv["lines"][-1]
        ln["amount"] = money(ln["amount"] + delta)  # qty x price no longer equals amount
        inv["subtotal"] = money(sum(l["amount"] for l in inv["lines"]))
        inv["tax"] = money(inv["subtotal"] * inv["tax_rate"])
        inv["total"] = money(inv["subtotal"] + inv["tax"])
        note(inv["invoice_no"], f"Last line amount inflated by {delta}; qty x unit_price no longer equals amount.")
        gold_entry(inv["invoice_no"], "hold", ["TOTAL_ERROR"], po["po_number"],
                   "Line amount does not equal qty x unit price; totals inflated.")
        invoices.append(inv)

    # ---- 2 BANK_CHANGE (fraud signal) -----------------------------------------
    for vid, acct in [("V05", "7791024468"), ("V08", "4456108823")]:
        po, inv = make(vid)
        add_grn(po)
        inv["bank_account"] = acct
        inv["bank_name"] = "Meridian Trust Bank"
        note(inv["invoice_no"], "Remit-to bank details differ from vendor master (classic fraud signal).")
        gold_entry(inv["invoice_no"], "hold", ["BANK_CHANGE"], po["po_number"],
                   "Remit-to bank account does not match vendor master record.")
        invoices.append(inv)

    # ---- 1 CURRENCY_MISMATCH ---------------------------------------------------
    po, inv = make("V09")
    add_grn(po)
    inv["currency"] = "USD"  # PO is EUR
    note(inv["invoice_no"], "Invoice issued in USD while PO/vendor currency is EUR.")
    gold_entry(inv["invoice_no"], "hold", ["CURRENCY_MISMATCH"], po["po_number"],
               "Invoice currency USD does not match PO currency EUR.")
    invoices.append(inv)

    # ---- 1 PO_NOT_FOUND ----------------------------------------------------------
    po, inv = make("V10")
    add_grn(po)
    inv["po_number"] = "PO-2025-9911"  # does not exist
    note(inv["invoice_no"], "References PO-2025-9911 which does not exist in the ERP.")
    gold_entry(inv["invoice_no"], "hold", ["PO_NOT_FOUND"], "PO-2025-9911",
               "Referenced PO does not exist in the purchase order system.")
    invoices.append(inv)

    # ---- 2 double-defect invoices (multi-label) ---------------------------------
    po, inv = make("V01")
    add_grn(po, fraction=0.5)
    ln = inv["lines"][0]
    ln["unit_price"] = money(ln["unit_price"] * 1.10)
    ln["amount"] = money(ln["qty"] * ln["unit_price"])
    inv["subtotal"] = money(sum(l["amount"] for l in inv["lines"]))
    inv["tax"] = money(inv["subtotal"] * inv["tax_rate"])
    inv["total"] = money(inv["subtotal"] + inv["tax"])
    note(inv["invoice_no"], "Double defect: price +10% AND only half the goods received.")
    gold_entry(inv["invoice_no"], "hold", ["PRICE_MISMATCH", "QTY_MISMATCH"], po["po_number"],
               "Line 1 price 10% above PO and billed qty exceeds received qty.")
    invoices.append(inv)

    po, inv = make("V04")
    add_grn(po)
    inv["bank_account"] = "6120087745"
    inv["bank_name"] = "Meridian Trust Bank"
    inv["tax"] = money(inv["tax"] + 44.10)
    inv["total"] = money(inv["subtotal"] + inv["tax"])
    note(inv["invoice_no"], "Double defect: changed bank account AND overstated tax.")
    gold_entry(inv["invoice_no"], "hold", ["BANK_CHANGE", "TAX_ERROR"], po["po_number"],
               "Remit-to bank differs from master and tax is overstated.")
    invoices.append(inv)

    # ---- decoy POs and payment history noise -------------------------------------
    for vid in ["V01", "V03", "V06", "V09"]:
        po = add_po(vid, 2)
        add_grn(po)
    for i, vid in enumerate(["V01", "V04", "V07"]):
        payments.append({"invoice_no": f"HIST-{7100 + i}", "vendor_id": vid,
                         "po_number": f"PO-2025-{4050 + i}", "amount": money(rng.uniform(500, 5000)),
                         "currency": "USD", "paid_date": f"2025-0{rng.randint(3, 5)}-{rng.randint(1, 28):02d}"})

    # vendor memory (used by iteration 4+): aliases + price history learned
    # from previous quarters of processing. Kept separate from the ERP master.
    vendor_memory = {
        "V01": {"known_aliases": ["Northgate Ind. Supply (a div. of NIS Holdings)",
                                   "NIS Holdings LLC", "Northgate Industrial"],
                "notes": "Invoices under NIS Holdings trade names since 2024 reorg. Split deliveries common."},
        "V02": {"known_aliases": ["Bluefin Packaging Company"],
                "notes": "Re-issued invoices previously arrived with reformatted numbers (INV-25-xxx vs INV-2025-0xxx)."},
        "V09": {"known_aliases": ["Vireo Print and Label"],
                "notes": "Always bills in EUR. Any USD invoice from this vendor is anomalous."},
    }

    # --------------------------- write world ------------------------------------
    ERP.mkdir(parents=True, exist_ok=True)
    GOLD.mkdir(parents=True, exist_ok=True)
    (ERP / "vendors.json").write_text(json.dumps(vendors, indent=2))
    (ERP / "pos.json").write_text(json.dumps(pos, indent=2))
    (ERP / "grns.json").write_text(json.dumps(grns, indent=2))
    (ERP / "payments.json").write_text(json.dumps(payments, indent=2))
    (ERP / "vendor_memory.json").write_text(json.dumps(vendor_memory, indent=2))
    (GOLD / "labels.json").write_text(json.dumps(gold, indent=2))

    lines = ["# Seeded evaluation cases\n"]
    for inv in invoices:
        g = gold[inv["invoice_no"]]
        extra = next((t for i_id, t in case_notes if i_id == inv["invoice_no"]), "")
        lines.append(f"- **{inv['invoice_no']}** ({inv['vendor_display_name']}, PO {g['po_number']}) — "
                     f"gold: `{g['decision']}` {g['discrepancies'] or ''} — {g['explanation']} {extra}")
    (GOLD / "cases.md").write_text("\n".join(lines) + "\n")

    # --------------------------- render PNGs ------------------------------------
    PNG.mkdir(parents=True, exist_ok=True)
    for inv in invoices:
        render_invoice(inv)

    manifest = [{"invoice_id": inv["invoice_no"],
                 "png": f"data/invoices/png/{safe(inv['invoice_no'])}.png"} for inv in invoices]
    (ROOT / "data" / "invoices" / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Generated {len(invoices)} invoices, {len(pos)} POs, {len(grns)} GRNs, "
          f"{len(payments)} payment records, {len(gold)} gold labels.")


# ---------------------------------------------------------------- render ----

def safe(inv_no: str) -> str:
    return inv_no.replace("/", "_").replace("#", "n")


def _font(size: int, bold=False, mono=False):
    candidates = (
        ["/System/Library/Fonts/Supplemental/Courier New Bold.ttf" if bold else
         "/System/Library/Fonts/Supplemental/Courier New.ttf"] if mono else
        ["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else
         "/System/Library/Fonts/Supplemental/Arial.ttf",
         "/System/Library/Fonts/Helvetica.ttc"]
    )
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_invoice(inv: dict) -> None:
    W, H = 1240, 1650
    img = Image.new("RGB", (W, H), "#ffffff")
    d = ImageDraw.Draw(img)
    tmpl = inv["template"]
    accent = {"A": "#1f3a5f", "B": "#0e6e5c", "C": "#5a3210"}[tmpl]
    f_h1, f_h2 = _font(44, bold=True), _font(26, bold=True)
    f, fb = _font(22), _font(22, bold=True)
    fm = _font(21, mono=True)
    sym = {"USD": "$", "EUR": "EUR ", "GBP": "GBP "}[inv["currency"]]

    if tmpl == "B":
        d.rectangle([0, 0, W, 130], fill=accent)
        d.text((40, 40), inv["vendor_display_name"], font=f_h1, fill="#ffffff")
        d.text((W - 320, 48), "TAX INVOICE", font=f_h2, fill="#ffffff")
        y = 170
    elif tmpl == "C":
        d.text((40, 40), inv["vendor_display_name"].upper(), font=_font(38, bold=True, mono=True), fill="#111111")
        d.line([40, 100, W - 40, 100], fill="#111111", width=3)
        d.text((W - 300, 115), "* INVOICE *", font=_font(26, bold=True, mono=True), fill="#111111")
        y = 160
    else:
        d.text((40, 40), inv["vendor_display_name"], font=f_h1, fill=accent)
        d.line([40, 105, W - 40, 105], fill=accent, width=4)
        d.text((W - 260, 120), "INVOICE", font=f_h2, fill=accent)
        y = 165

    meta = [
        ("Invoice No:", inv["invoice_no"]), ("Invoice Date:", inv["date"]),
        ("PO Reference:", inv["po_number"]), ("Currency:", inv["currency"]),
        ("Terms:", inv["payment_terms"]),
    ]
    for label, val in meta:
        d.text((W - 460, y), label, font=fb, fill="#333333")
        d.text((W - 240, y), str(val), font=f, fill="#111111")
        y += 34
    d.text((40, 175), "BILL TO:", font=fb, fill="#333333")
    for i, ln in enumerate(["Harborview Manufacturing Inc.", "Accounts Payable Dept.",
                            "2200 Dockside Ave, Suite 400", "Norfolk, VA 23501"]):
        d.text((40, 210 + i * 30), ln, font=f, fill="#111111")

    # table
    y = max(y + 30, 370)
    cols = [40, 200, 690, 790, 950, 1100]
    d.rectangle([40, y, W - 40, y + 44], fill=accent)
    for cx, h in zip(cols, ["SKU", "Description", "Qty", "Unit Price", "Amount", ""]):
        d.text((cx + 8, y + 9), h, font=fb, fill="#ffffff")
    y += 44
    for i, ln in enumerate(inv["lines"]):
        if i % 2 == 1:
            d.rectangle([40, y, W - 40, y + 42], fill="#f2f2f2")
        d.text((cols[0] + 8, y + 9), ln["sku"], font=fm, fill="#111111")
        d.text((cols[1] + 8, y + 9), ln["description"][:44], font=f, fill="#111111")
        d.text((cols[2] + 8, y + 9), str(ln["qty"]), font=f, fill="#111111")
        d.text((cols[3] + 8, y + 9), f"{sym}{ln['unit_price']:,.2f}", font=f, fill="#111111")
        d.text((cols[4] + 8, y + 9), f"{sym}{ln['amount']:,.2f}", font=f, fill="#111111")
        y += 42
    d.line([40, y, W - 40, y], fill="#999999", width=2)

    # totals
    y += 24
    trate = f"{inv['tax_rate']*100:.2f}".rstrip("0").rstrip(".")
    for label, val, bold in [("Subtotal", inv["subtotal"], False),
                             (f"Tax ({trate}%)", inv["tax"], False),
                             ("TOTAL DUE", inv["total"], True)]:
        d.text((870, y), label, font=fb if bold else f, fill="#111111")
        d.text((1050, y), f"{sym}{val:,.2f}", font=fb if bold else f, fill="#111111")
        y += 38
    if inv["template"] == "B":
        d.rectangle([850, y - 44, W - 40, y - 4], outline=accent, width=2)

    # remit-to
    y += 40
    d.text((40, y), "REMIT TO:", font=fb, fill="#333333")
    d.text((40, y + 32), f"Bank: {inv['bank_name']}", font=f, fill="#111111")
    d.text((40, y + 62), f"Routing: {inv['bank_routing']}   Account: {inv['bank_account']}", font=f, fill="#111111")
    d.text((40, y + 120), "Please reference the invoice number on all payments.", font=_font(19), fill="#555555")
    d.text((40, H - 60), f"{inv['vendor_display_name']}  -  Thank you for your business.",
           font=_font(19), fill="#888888")

    # light scan noise for OCR realism
    px = img.load()
    r = random.Random(inv["invoice_no"])
    for _ in range(2600):
        x, yy = r.randint(0, W - 1), r.randint(0, H - 1)
        g = r.randint(190, 235)
        px[x, yy] = (g, g, g)

    img.save(PNG / f"{safe(inv['invoice_no'])}.png")


if __name__ == "__main__":
    main()
