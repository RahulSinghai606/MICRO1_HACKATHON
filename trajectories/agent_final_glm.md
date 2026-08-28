# Agent trajectories — run `agent_final_glm`


## Case: NIS-2025-101

**Step 1 — LLM call** (agent: `extractor`, 616+820 tok, 12.27s)
- assistant said:

```
{
  "invoice_no": "NIS-2025-101",
  "vendor_name": "Northgate Industrial Supply LLC",
  "date": "2025-06-18",
  "po_number": "PO-2025-4101",
  "currency": "USD",
  "lines": [
    {"sku": "NG-4410", "description": "Nitrile work gloves, box of 100", "qty": 3, "unit_price": 18.40, "amount": 55.20},
    {"sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 7, "unit_price": 149.00, "amount": 1043.00},
    {"sku": "NG-7720", "description": "Safety goggles, anti-fog", "qty": 15, "unit_price": 6.95, "amount": 104.25},
    {"sku": "NG-3305", "description": "Absorbent pads, case", "qty": 16, "unit_price": 42.50, "amount": 680.00}
  ],
  "subtotal": 1882.45,
  "tax": 136.48,
  "total": 2018.93,
  "bank_name": "First Commerce Bank",
  "bank_routing": "021000021",
  "bank_account": "4402198837",
  "payment_terms": "Net 60"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-101"}`

**Step 3 — LLM call** (agent: `matcher`, 2085+1867 tok, 35.9s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4101"})`
- agent called `get_received_totals({"po_number":"PO-2025-4101"})`
- agent called `get_vendor_by_name({"name":"Northgate Industrial Supply LLC"})`
- agent called `arithmetic_check({"vendor_id":"V01"})`
- assistant said:

```
I'll verify this invoice against the PO, receipt totals, vendor master, and arithmetic. Starting with the independent lookups:
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4101", "vendor_id": "V01", "date": "2025-06-20", "currency": "USD", "lines": [{"line_no": 1, "sku": "NG-4410", "description": "Nitrile work gloves, box of 100", "qty": 3, "unit_price": 18.4}, {"line_no": 2, "sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 7, "unit_price": 149.0}, {"line_no": 3, "sku": "NG-7720", "description": "Safety goggles, anti-fog", "qty": 15, "unit_price": 6.95}, {"line_no": 4, "sku": "NG-3305", "description": "Absorbent pads, case", "qty": 16, "unit_price": 42.5}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 3, "2": 7, "3": 15, "4": 16}, "grn_count": 1, "grn_numbers": ["GRN-88301"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V01", "name": "Northgate Industrial Supply LLC", "city": "Columbus, OH", "currency": "USD", "payment_terms": "Net 60", "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "tax_rate": 0.0725, "memory": {"known_aliases": ["Northgate Ind. Supply (a div. of NIS Holdings)", "NIS Holdings LLC", "Northgate Industrial"], "notes": "Invoices under NIS Holdings trade names since 2024 reorg. Split deliveries common."}}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (136.48 ~= 136.48).", "Remit-to bank details match vendor master."]}
```

**Step 8 — LLM call** (agent: `matcher`, 2644+207 tok, 8.71s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"invoice_no":"NIS-2025-101","po_number":"PO-2025-4101","total":2018.93,"vendor_id":"V01"})`
- assistant said:

```
PO confirmed, quantities match the single GRN, arithmetic and bank details pass. Now checking payment history for duplicates:
```

**Step 9 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 10 — LLM call** (agent: `matcher`, 2727+698 tok, 14.42s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks complete. Summary of verification:

- **PO existence**: PO-2025-4101 exists (vendor V01, status open) — no PO_NOT_FOUND
- **Prices**: All 4 line unit prices match the PO exactly ($18.40, $149.00, $6.95, $42.50) — no PRICE_MISMATCH
- **Quantities**: Billed 3/7/15/16 vs. received 3/7/15/16 (GRN-88301) — no QTY_MISMATCH; GRN exists — no GRN_MISSING
- **Currency**: Invoice USD = PO USD — no CURRENCY_MISMATCH
- **Arithmetic**: Tax $136.48 = 7.25% × $1,882.45; subtotal and total all within tolerance — no TAX_ERROR/TOTAL_ERROR
- **Bank**: First Commerce Bank, routing 021000021, account 4402198837 — matches vendor master — no BANK_CHANGE
- **Duplicates**: No payments match this invoice number, PO, or total ($2,018.93) — no DUPLICATE

```json
{
  "invoice_id": "NIS-2025-101",
  "po_number": "PO-2025-4101",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "All four invoice lines match PO-2025-4101 unit prices exactly ($18.40, $149.00, $6.95, $42.50) and billed quantities (3/7/15/16) equal total received quantities on GRN-88301. Arithmetic passed: tax of $136.48 equals 7.25% x subtotal $1,882.45 and total $2,018.93 = subtotal + tax; remit-to bank (First Commerce Bank, routing 021000021, acct 4402198837) matches the vendor master, currency is USD on both PO and invoice, and payment history shows no duplicate for this invoice number, PO, or amount."
}
```
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: INV-2025-0101

**Step 1 — LLM call** (agent: `extractor`, 457+471 tok, 3.63s)
- assistant said:

```
{
 "invoice_no": "INV-2025-0101",
 "vendor_name": "Bluefin Packaging Co.",
 "date": "2025-06-25",
 "po_number": "PO-2025-4102",
 "currency": "USD",
 "lines": [
  {"sku": "BP-450", "description": "Foam inserts, custom cut", "qty": 30, "unit_price": 4.15, "amount": 124.50},
  {"sku": "BP-201", "description": "Corrugated boxes 18x12x10, bundle 25", "qty": 39, "unit_price": 31.25, "amount": 1218.75}
 ],
 "subtotal": 1343.25,
 "tax": 94.03,
 "total": 1437.28,
 "bank_name": "Coastal Georgia Bank",
 "bank_routing": "061000104",
 "bank_account": "7719045512",
 "payment_terms": "Net 30"
}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0101"}`

**Step 3 — LLM call** (agent: `matcher`, 1794+1076 tok, 21.71s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4102"})`
- agent called `get_received_totals({"po_number":"PO-2025-4102"})`
- agent called `get_vendor_by_name({"name":"Bluefin Packaging Co."})`
- agent called `search_payments({"invoice_no":"INV-2025-0101","po_number":"PO-2025-4102","total":1437.28,"vendor_id":"V02"})`
- agent called `arithmetic_check({"vendor_id":"V02"})`
- assistant said:

```
I'll verify all checks using the tools. Since I already have the vendor ID (V02) from the scoped PO, these calls are independent and I can run them together:
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4102", "vendor_id": "V02", "date": "2025-05-26", "currency": "USD", "lines": [{"line_no": 1, "sku": "BP-450", "description": "Foam inserts, custom cut", "qty": 30, "unit_price": 4.15}, {"line_no": 2, "sku": "BP-201", "description": "Corrugated boxes 18x12x10, bundle 25", "qty": 39, "unit_price": 31.25}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 30, "2": 39}, "grn_count": 1, "grn_numbers": ["GRN-88302"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V02", "name": "Bluefin Packaging Co.", "city": "Savannah, GA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Coastal Georgia Bank", "bank_routing": "061000104", "bank_account": "7719045512", "tax_rate": 0.07, "memory": {"known_aliases": ["Bluefin Packaging Company"], "notes": "Re-issued invoices previously arrived with reformatted numbers (INV-25-xxx vs INV-2025-0xxx)."}}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (94.03 ~= 94.03).", "Remit-to bank details match vendor master."]}
```

**Step 9 — LLM call** (agent: `matcher`, 2307+783 tok, 15.63s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the verification summary:

| Check | Result |
|---|---|
| PO existence | ✅ PO-2025-4102 exists, vendor V02, open |
| Line prices | ✅ BP-450: $4.15 = PO $4.15; BP-201: $31.25 = PO $31.25 |
| Billed vs received qty | ✅ BP-450: 30 billed vs 30 received (GRN-88302); BP-201: 39 billed vs 39 received |
| GRN present | ✅ GRN-88302 dated 2025-05-26 |
| Duplicates | ✅ No matches for invoice no., vendor+PO+total ($1,437.28) in payment history |
| Currency | ✅ Invoice USD = PO USD |
| Arithmetic | ✅ Tax $94.03 ≈ 7% × $1,343.25 ($94.0275); line amounts, subtotal, total all pass |
| Bank details | ✅ Coastal Georgia Bank / 061000104 / 7719045512 match vendor master |

Note: vendor memory flags reformatted invoice numbers (INV-25-xxx style), but search_payments confirms neither "INV-2025-0101" nor any normalized variant appears in payment history for V02.

```json
{
  "invoice_id": "INV-2025-0101",
  "po_number": "PO-2025-4102",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "All lines match the PO exactly (BP-450: 30 @ $4.15, BP-201: 39 @ $31.25) and billed quantities equal the received quantities on GRN-88302 (30 and 39). Arithmetic passes: subtotal $1,343.25, tax $94.03 = 7% rate ($94.0275, within $0.02 tolerance), total $1,437.28; currency (USD), bank details, and payment history (no duplicates) all verify clean."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: MF/25/101

**Step 1 — LLM call** (agent: `extractor`, 560+552 tok, 7.83s)
- assistant said:

```
{
  "invoice_no": "MF/25/101",
  "vendor_name": "Meridian Fasteners Inc.",
  "date": "2025-07-04",
  "po_number": "PO-2025-4103",
  "currency": "USD",
  "lines": [
    {
      "sku": "MF-ANC-10",
      "description": "Concrete anchors 10mm, box 100",
      "qty": 19,
      "unit_price": 62.75,
      "amount": 1192.25
    },
    {
      "sku": "MF-M8-NUT",
      "description": "Hex nuts M8 zinc, box 1000",
      "qty": 11,
      "unit_price": 27.60,
      "amount": 303.60
    }
  ],
  "subtotal": 1495.85,
  "tax": 89.75,
  "total": 1585.60,
  "bank_name": "Keystone National",
  "bank_routing": "031000503",
  "bank_account": "5583920164",
  "payment_terms": "Net 30"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/101"}`

**Step 3 — LLM call** (agent: `matcher`, 1674+536 tok, 11.68s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4103"})`
- agent called `get_received_totals({"po_number":"PO-2025-4103"})`
- agent called `get_vendor_by_name({"name":"Meridian Fasteners Inc."})`
- assistant said:

```
I'll verify this invoice against the ERP system. First, let me pull the PO, received totals, and resolve the vendor record — these are independent calls.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4103", "vendor_id": "V03", "date": "2025-04-25", "currency": "USD", "lines": [{"line_no": 1, "sku": "MF-ANC-10", "description": "Concrete anchors 10mm, box 100", "qty": 19, "unit_price": 62.75}, {"line_no": 2, "sku": "MF-M8-NUT", "description": "Hex nuts M8 zinc, box 1000", "qty": 11, "unit_price": 27.6}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 19, "2": 11}, "grn_count": 1, "grn_numbers": ["GRN-88303"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V03", "name": "Meridian Fasteners Inc.", "city": "Erie, PA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Keystone National", "bank_routing": "031000503", "bank_account": "5583920164", "tax_rate": 0.06}
```

**Step 7 — LLM call** (agent: `matcher`, 2034+141 tok, 3.33s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `arithmetic_check({"vendor_id":"V03"})`
- agent called `search_payments({"invoice_no":"MF/25/101","po_number":"PO-2025-4103","total":1585.6,"vendor_id":"V03"})`
- assistant said:

```
PO, GRNs, and vendor master all resolve cleanly. Now let me run the deterministic arithmetic check and screen payment history for duplicates — these are independent of each other.
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (89.75 ~= 89.75).", "Remit-to bank details match vendor master."]}
```

**Step 9 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 10 — LLM call** (agent: `matcher`, 2179+468 tok, 11.1s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks passed with no discrepancies found. Here is the final decision:

```json
{
  "invoice_id": "MF/25/101",
  "po_number": "PO-2025-4103",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO-2025-4103 exists and matches: both lines bill the exact PO prices (62.75 and 27.60) and quantities (19 and 11) fully received on GRN-88303, and currency is USD on both sides. Arithmetic check passed (subtotal 1495.85 = 1192.25 + 303.60; tax 89.75 = 6% of 1495.85; total 1585.60 = subtotal + tax) and remit-to bank (Keystone National, routing 031000503, acct 5583920164) matches vendor master V03. Payment history shows no duplicate for this invoice number, PO, or total amount, so the invoice is approved."
}
```
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: CCW-101

**Step 1 — LLM call** (agent: `extractor`, 564+590 tok, 7.79s)
- assistant said:

```
{
  "invoice_no": "CCW-101",
  "vendor_name": "Cascadia Chemical Works",
  "date": "2025-06-24",
  "po_number": "PO-2025-4104",
  "currency": "USD",
  "lines": [
    {
      "sku": "CC-DEG-5",
      "description": "Industrial degreaser, 5gal",
      "qty": 24,
      "unit_price": 87.40,
      "amount": 2097.60
    },
    {
      "sku": "CC-IPA-55",
      "description": "Isopropyl alcohol 99%, 55gal drum",
      "qty": 24,
      "unit_price": 612.00,
      "amount": 14688.00
    }
  ],
  "subtotal": 16785.60,
  "tax": 1594.63,
  "total": 18380.23,
  "bank_name": "Puget Sound Trust",
  "bank_routing": "125000024",
  "bank_account": "9027481133",
  "payment_terms": "Net 60"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1751+681 tok, 14.57s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4104"})`
- agent called `get_received_totals({"po_number":"PO-2025-4104"})`
- agent called `get_vendor_by_name({"name":"Cascadia Chemical Works"})`
- agent called `search_payments({"invoice_no":"CCW-101","po_number":"PO-2025-4104","total":18380.23,"vendor_id":"V04"})`
- agent called `arithmetic_check({"vendor_id":"V04"})`
- assistant said:

```
I'll verify this invoice against the PO, GRNs, vendor master, and payment history using the tools. All these checks are independent, so I'll run them together.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4104", "vendor_id": "V04", "date": "2025-06-09", "currency": "USD", "lines": [{"line_no": 1, "sku": "CC-DEG-5", "description": "Industrial degreaser, 5gal", "qty": 24, "unit_price": 87.4}, {"line_no": 2, "sku": "CC-IPA-55", "description": "Isopropyl alcohol 99%, 55gal drum", "qty": 24, "unit_price": 612.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 24, "2": 24}, "grn_count": 1, "grn_numbers": ["GRN-88304"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V04", "name": "Cascadia Chemical Works", "city": "Tacoma, WA", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Puget Sound Trust", "bank_routing": "125000024", "bank_account": "9027481133", "tax_rate": 0.095}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (1594.63 ~= 1594.63).", "Remit-to bank details match vendor master."]}
```

**Step 9 — LLM call** (agent: `matcher`, 2224+713 tok, 19.54s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks passed. Summary of verification:

| Check | Result |
|---|---|
| PO existence | PO-2025-4104 exists (vendor V04, USD, status open) |
| Line prices | Line 1: $87.40 = PO $87.40; Line 2: $612.00 = PO $612.00 — exact match |
| Billed vs received | Billed 24/24 vs GRN-88304 received 24/24 on both lines |
| GRN present | GRN-88304 exists for this PO |
| Arithmetic | Passed — tax $1,594.63 ≈ 9.5% × $16,785.60; line amounts, subtotal, and total all within tolerance |
| Currency | USD on invoice and PO |
| Bank details | Puget Sound Trust / 125000024 / 9027481133 match vendor master exactly |
| Duplicates | No matches in payment history (only prior payment is HIST-7101 for PO-2025-4051, $543.51) |

```json
{
  "invoice_id": "CCW-101",
  "po_number": "PO-2025-4104",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "Invoice CCW-101 matches PO-2025-4104 exactly: both line prices ($87.40 and $612.00) equal PO prices, billed quantities (24/24) equal total received on GRN-88304, and currency is USD on both. Arithmetic check passed (subtotal $16,785.60, tax $1,594.63 = 9.5% rate, total $18,380.23), remit-to bank details match vendor master V04, and no duplicates exist in payment history. No discrepancy codes apply, so the invoice is approved."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: HEC-2025-101

**Step 1 — LLM call** (agent: `extractor`, 494+685 tok, 10.33s)
- assistant said:

```
{
 "invoice_no": "HEC-2025-101",
 "vendor_name": "Helios Electrical Components",
 "date": "2025-06-02",
 "po_number": "PO-2025-4105",
 "currency": "USD",
 "lines": [
  {"sku": "HE-CB-20", "description": "Circuit breaker 20A DIN", "qty": 37, "unit_price": 9.85, "amount": 364.45},
  {"sku": "HE-REL-24", "description": "Relay 24VDC 8-pin", "qty": 20, "unit_price": 14.20, "amount": 284.00},
  {"sku": "HE-PSU-24", "description": "PSU 24V 10A DIN rail", "qty": 25, "unit_price": 96.30, "amount": 2407.50}
 ],
 "subtotal": 3055.95,
 "tax": 262.81,
 "total": 3318.76,
 "bank_name": "Desert West Bank",
 "bank_routing": "122100024",
 "bank_account": "3348812706",
 "payment_terms": "Net 45"
}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1818+753 tok, 14.7s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4105"})`
- agent called `get_received_totals({"po_number":"PO-2025-4105"})`
- agent called `get_vendor_by_name({"name":"Helios Electrical Components"})`
- agent called `arithmetic_check({"vendor_id":"V05"})`
- agent called `search_payments({"invoice_no":"HEC-2025-101","po_number":"PO-2025-4105","total":3318.76,"vendor_id":"V05"})`
- assistant said:

```
I'll run all verification checks in parallel — PO existence, received totals, vendor resolution, arithmetic, and duplicate screening (vendor_id V05 is known from the PO context).
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4105", "vendor_id": "V05", "date": "2025-06-07", "currency": "USD", "lines": [{"line_no": 1, "sku": "HE-CB-20", "description": "Circuit breaker 20A DIN", "qty": 37, "unit_price": 9.85}, {"line_no": 2, "sku": "HE-REL-24", "description": "Relay 24VDC 8-pin", "qty": 20, "unit_price": 14.2}, {"line_no": 3, "sku": "HE-PSU-24", "description": "PSU 24V 10A DIN rail", "qty": 25, "unit_price": 96.3}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 37, "2": 20, "3": 25}, "grn_count": 1, "grn_numbers": ["GRN-88305"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V05", "name": "Helios Electrical Components", "city": "Tucson, AZ", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Desert West Bank", "bank_routing": "122100024", "bank_account": "3348812706", "tax_rate": 0.086}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (262.81 ~= 262.81).", "Remit-to bank details match vendor master."]}
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — LLM call** (agent: `matcher`, 2341+939 tok, 18.2s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Summary of verification:

- **PO existence**: PO-2025-4105 exists (V05, USD, open) ✓
- **Prices**: All three line unit prices match the PO exactly (9.85 / 14.20 / 96.30) — within 0.5% tolerance ✓
- **Quantities**: Billed 37/20/25 vs. received (GRN-88305) 37/20/25 — all covered by receipts ✓
- **GRN**: GRN-88305 exists ✓
- **Arithmetic**: Tax 262.81 ≈ 0.086 × 3055.95 = 262.81 (within $0.02); line amounts, subtotal 3055.95, and total 3318.76 all verified ✓
- **Currency**: USD on both invoice and PO ✓
- **Bank**: Desert West Bank / 122100024 / 3348812706 matches vendor master exactly ✓
- **Duplicates**: No prior payments found for this vendor/PO/total or invoice number ✓

```json
{
  "invoice_id": "HEC-2025-101",
  "po_number": "PO-2025-4105",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "All three lines match PO-2025-4105 exactly on price (9.85/14.20/96.30) and billed quantities equal the total received on GRN-88305 (37/20/25). Arithmetic verified: subtotal 3055.95 = sum of line amounts, tax 262.81 = 8.6% × 3055.95, total 3318.76 = subtotal + tax. Currency (USD), remit-to bank details (Desert West Bank, routing 122100024, acct 3348812706), and payment history (no duplicates) all match vendor master V05."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: ALS-INV-101

**Step 1 — LLM call** (agent: `extractor`, 538+295 tok, 5.63s)
- assistant said:

```
{"invoice_no": "ALS-INV-101", "vendor_name": "Auriga Logistics Services", "date": "2025-07-06", "po_number": "PO-2025-4106", "currency": "USD", "lines": [{"sku": "AL-FUEL", "description": "Fuel surcharge", "qty": 8, "unit_price": 63.75, "amount": 510.00}, {"sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 26, "unit_price": 18.50, "amount": 481.00}, {"sku": "AL-LTL-STD", "description": "LTL freight, standard lane", "qty": 19, "unit_price": 425.00, "amount": 8075.00}, {"sku": "AL-LIFT", "description": "Liftgate service", "qty": 31, "unit_price": 45.00, "amount": 1395.00}], "subtotal": 10461.00, "tax": 0.00, "total": 10461.00, "bank_name": "River City Bank", "bank_routing": "084000026", "bank_account": "6650371928", "payment_terms": "Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1978+452 tok, 12.67s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4106"})`
- agent called `get_received_totals({"po_number":"PO-2025-4106"})`
- agent called `get_vendor_by_name({"name":"Auriga Logistics Services"})`
- assistant said:

```
I'll verify this invoice against the PO, GRNs, vendor master, and payment history. Starting with the independent lookups:
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4106", "vendor_id": "V06", "date": "2025-06-27", "currency": "USD", "lines": [{"line_no": 1, "sku": "AL-FUEL", "description": "Fuel surcharge", "qty": 8, "unit_price": 63.75}, {"line_no": 2, "sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 26, "unit_price": 18.5}, {"line_no": 3, "sku": "AL-LTL-STD", "description": "LTL freight, standard lane", "qty": 19, "unit_price": 425.0}, {"line_no": 4, "sku": "AL-LIFT", "description": "Liftgate service", "qty": 31, "unit_price": 45.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 8, "2": 26, "3": 19, "4": 31}, "grn_count": 1, "grn_numbers": ["GRN-88306"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V06", "name": "Auriga Logistics Services", "city": "Memphis, TN", "currency": "USD", "payment_terms": "Net 30", "bank_name": "River City Bank", "bank_routing": "084000026", "bank_account": "6650371928", "tax_rate": 0.0}
```

**Step 7 — LLM call** (agent: `matcher`, 2411+213 tok, 8.36s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `arithmetic_check({"vendor_id":"V06"})`
- agent called `search_payments({"invoice_no":"ALS-INV-101","po_number":"PO-2025-4106","total":10461.0,"vendor_id":"V06"})`
- assistant said:

```
PO confirmed for vendor V06 with matching currency, and received totals (8/26/19/31) match the billed quantities exactly. Now checking arithmetic and screening for duplicates in parallel:
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 9 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 10 — LLM call** (agent: `matcher`, 2560+604 tok, 13.55s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are clean. Here's the summary:

- **PO**: PO-2025-4106 exists, belongs to vendor V06, currency USD — matches invoice currency
- **Prices**: All 4 line unit prices (63.75 / 18.50 / 425.00 / 45.00) exactly match PO line prices (0% variance, within 0.5% tolerance)
- **Quantities**: Billed 8/26/19/31 vs. received totals 8/26/19/31 across GRN-88306 — no overbilling
- **Arithmetic**: Deterministic check passed — line amounts, subtotal ($10,461.00), tax ($0.00 = 0% × subtotal), and total all within tolerance
- **Duplicate screen**: No payments found for vendor V06 + PO-2025-4106 at $10,461.00, and invoice ALS-INV-101 does not appear in payment history (only ALS-INV-107 on a different PO)
- **Bank**: River City Bank / routing 084000026 / account 6650371928 matches vendor master exactly

```json
{
  "invoice_id": "ALS-INV-101",
  "po_number": "PO-2025-4106",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "All four lines match PO-2025-4106 unit prices exactly (63.75/18.50/425.00/45.00), and billed quantities (8/26/19/31) equal total received quantities on GRN-88306. Arithmetic check passed (subtotal 10461.00, tax 0.00 at 0% rate, total 10461.00), currency is USD per PO, remit-to bank matches vendor master, and no duplicate payment exists for this vendor/PO/amount or invoice number."
}
```
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: SOI-25-101

**Step 1 — LLM call** (agent: `extractor`, 585+741 tok, 9.48s)
- assistant said:

```
{
  "invoice_no": "SOI-25-101",
  "vendor_name": "Stellar Office Interiors",
  "date": "2025-06-06",
  "po_number": "PO-2025-4107",
  "currency": "USD",
  "lines": [
    {
      "sku": "SO-MON-ARM",
      "description": "Dual monitor arm",
      "qty": 6,
      "unit_price": 74.25,
      "amount": 445.50
    },
    {
      "sku": "SO-CHR-T2",
      "description": "Task chair, mesh back",
      "qty": 40,
      "unit_price": 189.00,
      "amount": 7560.00
    },
    {
      "sku": "SO-DSK-60",
      "description": "Sit-stand desk 60in",
      "qty": 12,
      "unit_price": 415.00,
      "amount": 4980.00
    }
  ],
  "subtotal": 12985.50,
  "tax": 1051.83,
  "total": 14037.33,
  "bank_name": "Front Range Credit Union",
  "bank_routing": "107000233",
  "bank_account": "8812204575",
  "payment_terms": "Net 30"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1870+1175 tok, 23.01s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4107"})`
- agent called `get_received_totals({"po_number":"PO-2025-4107"})`
- agent called `get_vendor_by_name({"name":"Stellar Office Interiors"})`
- assistant said:

```
I'll verify this invoice against the PO, GRNs, vendor master, payment history, and arithmetic. First, let me pull the PO, received totals, and resolve the vendor record (these are independent):
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4107", "vendor_id": "V07", "date": "2025-06-24", "currency": "USD", "lines": [{"line_no": 1, "sku": "SO-MON-ARM", "description": "Dual monitor arm", "qty": 6, "unit_price": 74.25}, {"line_no": 2, "sku": "SO-CHR-T2", "description": "Task chair, mesh back", "qty": 40, "unit_price": 189.0}, {"line_no": 3, "sku": "SO-DSK-60", "description": "Sit-stand desk 60in", "qty": 12, "unit_price": 415.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 6, "2": 40, "3": 12}, "grn_count": 1, "grn_numbers": ["GRN-88307"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V07", "name": "Stellar Office Interiors", "city": "Denver, CO", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Front Range Credit Union", "bank_routing": "107000233", "bank_account": "8812204575", "tax_rate": 0.081}
```

**Step 7 — LLM call** (agent: `matcher`, 2279+135 tok, 8.74s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"invoice_no":"SOI-25-101","po_number":"PO-2025-4107","total":14037.33,"vendor_id":"V07"})`
- agent called `arithmetic_check({"vendor_id":"V07"})`
- assistant said:

```
PO exists and matches (V07, USD), and received quantities match billed quantities. Now let me run the duplicate screen and the deterministic arithmetic check (both independent now that I have the vendor ID):
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (1051.83 ~= 1051.83).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2433+732 tok, 17.49s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All verifications are complete. Here's the summary:

**Check results:**
- **PO existence**: PO-2025-4107 exists (vendor V07, USD, open status) ✓
- **Prices**: All three line unit prices match the PO exactly — SO-MON-ARM @ $74.25, SO-CHR-T2 @ $189.00, SO-DSK-60 @ $415.00 (0% variance, within 0.5% tolerance) ✓
- **Quantities**: Billed qty (6 / 40 / 12) matches total received across GRN-88307 (6 / 40 / 12) ✓
- **GRN**: GRN-88307 dated 2025-06-24 covers all three lines ✓
- **Duplicate**: No matching invoice number, and no vendor+PO+total match in payment history (only prior payment is HIST-7102 for $4,567.68 on a different PO) ✓
- **Currency**: Invoice USD = PO USD = vendor master USD ✓
- **Arithmetic**: Tax $1,051.83 = 0.081 × $12,985.50; lines, subtotal, and total all verified within $0.02 tolerance ✓
- **Bank**: Front Range Credit Union / routing 107000233 / account 8812204575 matches vendor master exactly ✓

```json
{
  "invoice_id": "SOI-25-101",
  "po_number": "PO-2025-4107",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "All three lines match PO-2025-4107 exactly (prices $74.25/$189.00/$415.00, 0% variance) and billed quantities (6/40/12) equal total received per GRN-88307. Arithmetic verified: tax $1,051.83 equals 8.1% of the $12,985.50 subtotal, and total $14,037.33 is correct. No duplicate found in payment history, currency is USD on both invoice and PO, and remit-to bank details (Front Range CU, routing 107000233, acct 8812204575) match vendor master V07."
}
```

**Decision: APPROVE** — this invoice passes the three-way match cleanly with no discrepancies.
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: GP-101

**Step 1 — LLM call** (agent: `extractor`, 490+277 tok, 6.7s)
- assistant said:

```
{
 "invoice_no": "GP-101",
 "vendor_name": "Granite Peak Safety Gear",
 "date": "2025-07-13",
 "po_number": "PO-2025-4108",
 "currency": "USD",
 "lines": [
  {"sku": "GP-EAR-200", "description": "Ear plugs, box 200 pr", "qty": 22, "unit_price": 38.90, "amount": 855.80},
  {"sku": "GP-VIS-XL", "description": "Hi-vis vests XL, pack 10", "qty": 5, "unit_price": 84.50, "amount": 422.50},
  {"sku": "GP-HH-CL2", "description": "Hard hats class E, box 20", "qty": 16, "unit_price": 196.00, "amount": 3136.00}
 ],
 "subtotal": 4414.30,
 "tax": 264.86,
 "total": 4679.16,
 "bank_name": "Sawtooth Community Bank",
 "bank_routing": "123103729",
 "bank_account": "2290156841",
 "payment_terms": "Net 30"
}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1816+868 tok, 17.14s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4108"})`
- agent called `get_received_totals({"po_number":"PO-2025-4108"})`
- agent called `get_vendor_by_name({"name":"Granite Peak Safety Gear"})`
- agent called `search_payments({"invoice_no":"GP-101","po_number":"PO-2025-4108","total":4679.16,"vendor_id":"V08"})`
- agent called `arithmetic_check({"vendor_id":"V08"})`
- assistant said:

```
I'll verify all checks using the tools. Since the PO context shows vendor_id V08, all of these calls are independent and I can run them together.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4108", "vendor_id": "V08", "date": "2025-04-26", "currency": "USD", "lines": [{"line_no": 1, "sku": "GP-EAR-200", "description": "Ear plugs, box 200 pr", "qty": 22, "unit_price": 38.9}, {"line_no": 2, "sku": "GP-VIS-XL", "description": "Hi-vis vests XL, pack 10", "qty": 5, "unit_price": 84.5}, {"line_no": 3, "sku": "GP-HH-CL2", "description": "Hard hats class E, box 20", "qty": 16, "unit_price": 196.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 22, "2": 5, "3": 16}, "grn_count": 1, "grn_numbers": ["GRN-88308"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V08", "name": "Granite Peak Safety Gear", "city": "Boise, ID", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Sawtooth Community Bank", "bank_routing": "123103729", "bank_account": "2290156841", "tax_rate": 0.06}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (264.86 ~= 264.86).", "Remit-to bank details match vendor master."]}
```

**Step 9 — LLM call** (agent: `matcher`, 2331+898 tok, 17.55s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Verification results:

- **PO existence:** PO-2025-4108 exists (V08, USD) — no PO_NOT_FOUND.
- **Prices:** All three lines match the PO exactly ($38.90, $84.50, $196.00) — 0% variance, within 0.5% tolerance — no PRICE_MISMATCH.
- **Quantities:** Billed 22/5/16 equals total received across GRN-88308 (22/5/16) — no QTY_MISMATCH, and GRN exists so no GRN_MISSING.
- **Currency:** Invoice USD = PO USD — no CURRENCY_MISMATCH.
- **Arithmetic:** arithmetic_check passed all tests — tax $264.86 ≈ 6% × $4,414.30 ($264.858, within $0.02), line amounts = qty × price, subtotal $4,414.30 = sum of lines, total $4,679.16 = subtotal + tax — no TAX_ERROR or TOTAL_ERROR.
- **Bank details:** Sawtooth Community Bank / routing 123103729 / account 2290156841 match vendor master — no BANK_CHANGE.
- **Duplicates:** Payment history is empty; search found no potential duplicates — no DUPLICATE.

```json
{
  "invoice_id": "GP-101",
  "po_number": "PO-2025-4108",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "All three lines match PO-2025-4108 exactly on unit price ($38.90/$84.50/$196.00) and billed quantities (22/5/16) equal the full received quantities on GRN-88308. Arithmetic check passed: tax $264.86 = 6% of subtotal $4,414.30 within tolerance, and total $4,679.16 = subtotal + tax. Remit-to bank (Sawtooth Community Bank, routing 123103729) matches vendor master V08, currency is USD on both PO and invoice, and payment history shows no duplicates."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: VPL-2025-101

**Step 1 — LLM call** (agent: `extractor`, 580+840 tok, 11.07s)
- assistant said:

```
{
  "invoice_no": "VPL-2025-101",
  "vendor_name": "Vireo Print & Label GmbH",
  "date": "2025-06-09",
  "po_number": "PO-2025-4109",
  "currency": "EUR",
  "lines": [
    {
      "sku": "VP-LBL-4x6",
      "description": "Thermal labels 4x6, roll 500",
      "qty": 15,
      "unit_price": 21.40,
      "amount": 321.00
    },
    {
      "sku": "VP-RIB-110",
      "description": "TTR ribbon 110mm",
      "qty": 33,
      "unit_price": 9.60,
      "amount": 316.80
    },
    {
      "sku": "VP-TAG-ASSET",
      "description": "Asset tags, custom, 1000",
      "qty": 27,
      "unit_price": 340.00,
      "amount": 9180.00
    }
  ],
  "subtotal": 9817.80,
  "tax": 1865.38,
  "total": 11683.18,
  "bank_name": "Hansa Handelsbank",
  "bank_routing": "DE44 5001 0517",
  "bank_account": "5407 3249 31",
  "payment_terms": "Net 60"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1893+944 tok, 18.99s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4109"})`
- agent called `get_received_totals({"po_number":"PO-2025-4109"})`
- agent called `get_vendor_by_name({"name":"Vireo Print & Label GmbH"})`
- agent called `arithmetic_check({"vendor_id":"V09"})`
- agent called `search_payments({"invoice_no":"VPL-2025-101","po_number":"PO-2025-4109","total":11683.18,"vendor_id":"V09"})`
- assistant said:

```
I'll verify this invoice against the PO, GRNs, vendor master, and payment history using the tools. All checks are independent, so I'll run them in parallel:
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4109", "vendor_id": "V09", "date": "2025-06-15", "currency": "EUR", "lines": [{"line_no": 1, "sku": "VP-LBL-4x6", "description": "Thermal labels 4x6, roll 500", "qty": 15, "unit_price": 21.4}, {"line_no": 2, "sku": "VP-RIB-110", "description": "TTR ribbon 110mm", "qty": 33, "unit_price": 9.6}, {"line_no": 3, "sku": "VP-TAG-ASSET", "description": "Asset tags, custom, 1000", "qty": 27, "unit_price": 340.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 15, "2": 33, "3": 27}, "grn_count": 1, "grn_numbers": ["GRN-88309"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V09", "name": "Vireo Print & Label GmbH", "city": "Hamburg, DE", "currency": "EUR", "payment_terms": "Net 60", "bank_name": "Hansa Handelsbank", "bank_routing": "DE44 5001 0517", "bank_account": "5407 3249 31", "tax_rate": 0.19, "memory": {"known_aliases": ["Vireo Print and Label"], "notes": "Always bills in EUR. Any USD invoice from this vendor is anomalous."}}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (1865.38 ~= 1865.38).", "Remit-to bank details match vendor master."]}
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — LLM call** (agent: `matcher`, 2464+806 tok, 16.53s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks completed. Here's the verification summary:

**Verification results:**
- **PO existence**: PO-2025-4109 exists in the system (status: open, vendor V09, currency EUR). ✓
- **Line prices**: Invoice matches PO exactly on all 3 lines — VP-LBL-4x6 @ 21.40, VP-RIB-110 @ 9.60, VP-TAG-ASSET @ 340.00. No price discrepancy. ✓
- **Quantities**: Billed qty matches summed GRN receipts on all lines (15/15, 33/33, 27/27 per GRN-88309). ✓
- **GRN**: GRN-88309 exists covering all three PO lines. ✓
- **Arithmetic (deterministic check)**: Passed — tax 1865.38 equals 0.19 × 9817.80; line amounts, subtotal, and total all within tolerance. ✓
- **Currency**: Invoice EUR = PO EUR = vendor master EUR. ✓
- **Bank details**: Hansa Handelsbank, DE44 5001 0517, acct 5407 3249 31 match vendor master. ✓
- **Duplicates**: No payments found for vendor V09 / PO-2025-4109 / invoice VPL-2025-101. ✓

```json
{
  "invoice_id": "VPL-2025-101",
  "po_number": "PO-2025-4109",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "Invoice VPL-2025-101 matches PO-2025-4109 on all three lines (15 x 21.40, 33 x 9.60, 27 x 340.00) with billed quantities equal to GRN-88309 receipts (15/33/27). Deterministic arithmetic check passed (subtotal 9817.80, tax 1865.38 = 19% of subtotal, total 11683.18), currency EUR matches PO and vendor master, remit-to bank details match the master record, and no duplicates exist in payment history."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: AMT-101

**Step 1 — LLM call** (agent: `extractor`, 560+510 tok, 6.71s)
- assistant said:

```
{
  "invoice_no": "AMT-101",
  "vendor_name": "Ashford Machine Tools Ltd.",
  "date": "2025-07-19",
  "po_number": "PO-2025-4110",
  "currency": "USD",
  "lines": [
    {"sku": "AM-VIS-6", "description": "Machine vise 6in", "qty": 37, "unit_price": 289.00, "amount": 10693.00},
    {"sku": "AM-CHK-125", "description": "Lathe chuck 125mm", "qty": 36, "unit_price": 412.60, "amount": 14853.60}
  ],
  "subtotal": 25546.60,
  "tax": 0.00,
  "total": 25546.60,
  "bank_name": "Pennine & Yorkshire Bank",
  "bank_routing": "GB29 NWBK 6016",
  "bank_account": "1331 9268 19",
  "payment_terms": "Net 30"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1676+1047 tok, 21.82s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4110"})`
- agent called `get_received_totals({"po_number":"PO-2025-4110"})`
- agent called `get_vendor_by_name({"name":"Ashford Machine Tools Ltd."})`
- agent called `search_payments({"invoice_no":"AMT-101","po_number":"PO-2025-4110","total":25546.6,"vendor_id":"V10"})`
- agent called `arithmetic_check({"vendor_id":"V10"})`
- assistant said:

```
I'll verify this invoice against the PO, GRNs, vendor master, payment history, and arithmetic. All of these checks are independent given the scoped context (vendor_id V10 from the PO), so I'll run them in parallel.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4110", "vendor_id": "V10", "date": "2025-05-24", "currency": "USD", "lines": [{"line_no": 1, "sku": "AM-VIS-6", "description": "Machine vise 6in", "qty": 37, "unit_price": 289.0}, {"line_no": 2, "sku": "AM-CHK-125", "description": "Lathe chuck 125mm", "qty": 36, "unit_price": 412.6}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 37, "2": 36}, "grn_count": 1, "grn_numbers": ["GRN-88310"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V10", "name": "Ashford Machine Tools Ltd.", "city": "Sheffield, UK", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Pennine & Yorkshire Bank", "bank_routing": "GB29 NWBK 6016", "bank_account": "1331 9268 19", "tax_rate": 0.0}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 9 — LLM call** (agent: `matcher`, 2159+853 tok, 12.44s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the verification summary:

| Check | Result |
|---|---|
| PO existence | PO-2025-4110 exists (vendor V10, USD, open) ✓ |
| Line prices | Line 1: 289.00 vs PO 289.00 (0.0% diff); Line 2: 412.60 vs PO 412.60 (0.0% diff) — within 0.5% ✓ |
| Quantities | Billed 37/36 vs received 37/36 across GRN-88310 ✓ |
| GRN | GRN-88310 exists for this PO ✓ |
| Duplicates | No matches in payment history (no same vendor+PO+total payment, invoice AMT-101 not previously seen) ✓ |
| Currency | Invoice USD = PO USD = vendor master USD ✓ |
| Arithmetic | Tax 0.00 = 0.0% × 25,546.60; line amounts 37×289.00 = 10,693.00 and 36×412.60 = 14,853.60; subtotal 25,546.60; total 25,546.60 = subtotal + tax ✓ |
| Bank | Pennine & Yorkshire Bank / GB29 NWBK 6016 / 1331 9268 19 — exact match to vendor master ✓ |

```json
{
  "invoice_id": "AMT-101",
  "po_number": "PO-2025-4110",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "Invoice AMT-101 fully matches PO-2025-4110: line prices (289.00 and 412.60) equal PO unit prices exactly, billed quantities (37 and 36) equal total received on GRN-88310 (37 and 36), and totals verify (subtotal 25,546.60 = 10,693.00 + 14,853.60; tax 0.00 = 0.0% rate; total 25,546.60). Currency (USD), remit-to bank details, and payment terms match the vendor master, and no duplicate payment was found for vendor V10 on this PO or invoice number."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: NIS-2025-104

**Step 1 — LLM call** (agent: `extractor`, 546+284 tok, 13.02s)
- assistant said:

```
{
 "invoice_no": "NIS-2025-104",
 "vendor_name": "Northgate Ind. Supply (a div. of NIS Holdings)",
 "date": "2025-06-05",
 "po_number": "PO-2025-4111",
 "currency": "USD",
 "lines": [
  {"sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 34, "unit_price": 149.00, "amount": 5066.00},
  {"sku": "NG-4410", "description": "Nitrile work gloves, box of 100", "qty": 33, "unit_price": 18.40, "amount": 607.20},
  {"sku": "NG-3305", "description": "Absorbent pads, case", "qty": 7, "unit_price": 42.50, "amount": 297.50}
 ],
 "subtotal": 5970.70,
 "tax": 432.88,
 "total": 6403.58,
 "bank_name": "First Commerce Bank",
 "bank_routing": "021000021",
 "bank_account": "4402198837",
 "payment_terms": "Net 60"
}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-104"}`

**Step 3 — LLM call** (agent: `matcher`, 2103+1049 tok, 19.25s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4111"})`
- agent called `get_received_totals({"po_number":"PO-2025-4111"})`
- agent called `get_vendor_by_name({"name":"Northgate Ind. Supply (a div. of NIS Holdings)"})`
- agent called `search_payments({"invoice_no":"NIS-2025-104","po_number":"PO-2025-4111","total":6403.58,"vendor_id":"V01"})`
- agent called `arithmetic_check({"vendor_id":"V01"})`
- assistant said:

```
I'll verify all checks using the tools: PO existence, received totals, vendor resolution, duplicate screening, and arithmetic.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4111", "vendor_id": "V01", "date": "2025-04-28", "currency": "USD", "lines": [{"line_no": 1, "sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 34, "unit_price": 149.0}, {"line_no": 2, "sku": "NG-4410", "description": "Nitrile work gloves, box of 100", "qty": 33, "unit_price": 18.4}, {"line_no": 3, "sku": "NG-3305", "description": "Absorbent pads, case", "qty": 7, "unit_price": 42.5}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 34, "2": 33, "3": 7}, "grn_count": 2, "grn_numbers": ["GRN-88311", "GRN-88312"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V01", "name": "Northgate Industrial Supply LLC", "city": "Columbus, OH", "currency": "USD", "payment_terms": "Net 60", "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "tax_rate": 0.0725, "memory": {"known_aliases": ["Northgate Ind. Supply (a div. of NIS Holdings)", "NIS Holdings LLC", "Northgate Industrial"], "notes": "Invoices under NIS Holdings trade names since 2024 reorg. Split deliveries common."}}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (432.88 ~= 432.88).", "Remit-to bank details match vendor master."]}
```

**Step 9 — LLM call** (agent: `matcher`, 2688+696 tok, 11.39s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All verifications are complete and clean:

- **PO exists**: PO-2025-4111 is in the system for vendor V01, USD.
- **Prices**: All three invoice line prices ($149.00, $18.40, $42.50) exactly match the PO unit prices — within 0.5% tolerance.
- **Quantities**: Billed qty (34 / 33 / 7) equals total received across the two partial GRNs (GRN-88311 + GRN-88312 = 34 / 33 / 7) — no overbilling; split deliveries are legitimate per policy.
- **Arithmetic**: The tool confirmed tax = $432.88 matches 7.25% × $5,970.70 subtotal, and line amounts/subtotal/total all reconcile within $0.02.
- **Bank**: Remit-to First Commerce Bank, routing 021000021, account 4402198837 matches vendor master.
- **Duplicates**: No payment history match on vendor + PO + total or invoice number.
- **Vendor name**: "Northgate Ind. Supply (a div. of NIS Holdings)" is a known alias in vendor memory — not a discrepancy.

```json
{
  "invoice_id": "NIS-2025-104",
  "po_number": "PO-2025-4111",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "All three lines match PO-2025-4111 exactly on unit price ($149.00, $18.40, $42.50) and billed quantities equal total received (34/33/7 across GRN-88311 and GRN-88312, summing to 34/33/7). Arithmetic verified by tool: tax $432.88 = 7.25% of $5,970.70 subtotal, total $6,403.58 correct; no duplicates in payment history; remit-to bank (routing 021000021, account 4402198837) matches vendor master; vendor trade name is a known alias."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: HEC-2025-104

**Step 1 — LLM call** (agent: `extractor`, 531+622 tok, 63.38s)
- assistant said:

```
{
 "invoice_no": "HEC-2025-104",
 "vendor_name": "Helios Electrical Components",
 "date": "2025-06-22",
 "po_number": "PO-2025-4112",
 "currency": "USD",
 "lines": [
  {"sku": "HE-REL-24", "description": "Relay 24VDC 8-pin", "qty": 26, "unit_price": 14.20, "amount": 369.20},
  {"sku": "HE-CAB-14", "description": "Copper cable 14AWG, 500ft spool", "qty": 26, "unit_price": 118.00, "amount": 3068.00},
  {"sku": "HE-PSU-24", "description": "PSU 24V 10A DIN rail", "qty": 40, "unit_price": 96.30, "amount": 3852.00},
  {"sku": "HE-CB-20", "description": "Circuit breaker 20A DIN", "qty": 31, "unit_price": 9.85, "amount": 305.35}
 ],
 "subtotal": 7594.55,
 "tax": 653.14,
 "total": 8247.69,
 "bank_name": "Desert West Bank",
 "bank_routing": "122100024",
 "bank_account": "3348812706",
 "payment_terms": "Net 45"
}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1970+819 tok, 16.81s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4112"})`
- agent called `get_received_totals({"po_number":"PO-2025-4112"})`
- agent called `get_vendor_by_name({"name":"Helios Electrical Components"})`
- agent called `arithmetic_check({"vendor_id":"V05"})`
- agent called `search_payments({"invoice_no":"HEC-2025-104","po_number":"PO-2025-4112","total":8247.69,"vendor_id":"V05"})`
- assistant said:

```
I'll verify all checks using the tools. Since the scoped PO already identifies vendor V05, I can run all verifications in parallel:
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4112", "vendor_id": "V05", "date": "2025-06-09", "currency": "USD", "lines": [{"line_no": 1, "sku": "HE-REL-24", "description": "Relay 24VDC 8-pin", "qty": 26, "unit_price": 14.2}, {"line_no": 2, "sku": "HE-CAB-14", "description": "Copper cable 14AWG, 500ft spool", "qty": 26, "unit_price": 118.0}, {"line_no": 3, "sku": "HE-PSU-24", "description": "PSU 24V 10A DIN rail", "qty": 40, "unit_price": 96.3}, {"line_no": 4, "sku": "HE-CB-20", "description": "Circuit breaker 20A DIN", "qty": 31, "unit_price": 9.85}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 26, "2": 26, "3": 40, "4": 31}, "grn_count": 1, "grn_numbers": ["GRN-88313"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V05", "name": "Helios Electrical Components", "city": "Tucson, AZ", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Desert West Bank", "bank_routing": "122100024", "bank_account": "3348812706", "tax_rate": 0.086}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (653.14 ~= 653.13).", "Remit-to bank details match vendor master."]}
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — LLM call** (agent: `matcher`, 2542+785 tok, 16.28s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the verification summary:

**Verification results:**
1. **PO existence**: PO-2025-4112 exists, vendor V05, USD — matches invoice reference. ✓
2. **Line prices**: All four invoice unit prices (14.20, 118.00, 96.30, 9.85) match PO prices exactly — within 0.5% tolerance. ✓
3. **Billed vs received quantities**: Received totals (GRN-88313): line 1: 26/26, line 2: 26/26, line 3: 40/40, line 4: 31/31 — no over-billing. ✓
4. **GRN**: GRN-88313 exists for this PO. ✓
5. **Duplicates**: No payment history for this vendor; no matching invoice number, PO, or total. ✓
6. **Currency**: Invoice USD = PO USD = vendor master USD. ✓
7. **Arithmetic**: arithmetic_check passed all checks — line amounts = qty × price, subtotal 7594.55 sums correctly, total 8247.69 = subtotal + tax, tax 653.14 ≈ 0.086 × 7594.55 (653.13, within $0.02). ✓
8. **Bank details**: Desert West Bank / 122100024 / 3348812706 match vendor master exactly. ✓

```json
{
  "invoice_id": "HEC-2025-104",
  "po_number": "PO-2025-4112",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "All four lines match PO-2025-4112 unit prices exactly (14.20/118.00/96.30/9.85), billed quantities (26/26/40/31) equal total received quantities per GRN-88313, and currency is USD on both invoice and PO. Arithmetic_check confirms subtotal 7594.55, tax 653.14 (≈ 0.086 × 7594.55 = 653.13, within $0.02), and total 8247.69; remit-to bank (Desert West Bank, routing 122100024, account 3348812706) matches vendor master V05, and payment history shows no duplicates."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: MF/25/104

**Step 1 — LLM call** (agent: `extractor`, 566+404 tok, 32.12s)
- assistant said:

```
{
 "invoice_no": "MF/25/104",
 "vendor_name": "Meridian Fasteners Inc.",
 "date": "2025-07-17",
 "po_number": "PO-2025-4113",
 "currency": "USD",
 "lines": [
  {"sku": "MF-M8-50", "description": "Hex bolts M8x50 zinc, box 500", "qty": 9, "unit_price": 49.28, "amount": 443.52},
  {"sku": "MF-W-8", "description": "Flat washers 8mm, box 1000", "qty": 20, "unit_price": 15.30, "amount": 306.00},
  {"sku": "MF-M8-NUT", "description": "Hex nuts M8 zinc, box 1000", "qty": 29, "unit_price": 27.60, "amount": 800.40},
  {"sku": "MF-ANC-10", "description": "Concrete anchors 10mm, box 100", "qty": 12, "unit_price": 62.75, "amount": 753.00}
 ],
 "subtotal": 2302.92,
 "tax": 138.18,
 "total": 2441.10,
 "bank_name": "Keystone National",
 "bank_routing": "031000503",
 "bank_account": "5583920164",
 "payment_terms": "Net 30"
}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/104"}`

**Step 3 — LLM call** (agent: `matcher`, 1965+1125 tok, 24.93s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4113"})`
- agent called `get_received_totals({"po_number":"PO-2025-4113"})`
- agent called `get_vendor_by_name({"name":"Meridian Fasteners Inc."})`
- agent called `search_payments({"invoice_no":"MF/25/104","po_number":"PO-2025-4113","total":2441.1,"vendor_id":"V03"})`
- agent called `arithmetic_check({"vendor_id":"V03"})`
- assistant said:

```
I'll verify all checks using the tools. The invoice references PO-2025-4113 with vendor V03 (from the scoped PO), so I can run all verifications in parallel:
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4113", "vendor_id": "V03", "date": "2025-05-01", "currency": "USD", "lines": [{"line_no": 1, "sku": "MF-M8-50", "description": "Hex bolts M8x50 zinc, box 500", "qty": 9, "unit_price": 44.0}, {"line_no": 2, "sku": "MF-W-8", "description": "Flat washers 8mm, box 1000", "qty": 20, "unit_price": 15.3}, {"line_no": 3, "sku": "MF-M8-NUT", "description": "Hex nuts M8 zinc, box 1000", "qty": 29, "unit_price": 27.6}, {"line_no": 4, "sku": "MF-ANC-10", "description": "Concrete anchors 10mm, box 100", "qty": 12, "unit_price": 62.75}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 9, "2": 20, "3": 29, "4": 12}, "grn_count": 1, "grn_numbers": ["GRN-88314"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V03", "name": "Meridian Fasteners Inc.", "city": "Erie, PA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Keystone National", "bank_routing": "031000503", "bank_account": "5583920164", "tax_rate": 0.06}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (138.18 ~= 138.18).", "Remit-to bank details match vendor master."]}
```

**Step 9 — LLM call** (agent: `matcher`, 2548+1022 tok, 19.01s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the analysis:

**Verification results:**
- **PO existence**: PO-2025-4113 exists (vendor V03, USD). ✓
- **Quantities**: Billed 9/20/29/12 vs. received (GRN-88314) 9/20/29/12 — all lines fully received. ✓
- **GRN**: GRN-88314 exists. ✓
- **Duplicate screening**: No payments found for this vendor/PO/total/invoice number. ✓
- **Currency**: USD on both invoice and PO. ✓
- **Arithmetic**: Passed — line amounts (9×49.28=443.52; 20×15.30=306.00; 29×27.60=800.40; 12×62.75=753.00), subtotal 2302.92, tax 138.18 = 6% × 2302.92, total 2441.10. ✓
- **Bank details**: Keystone National / 031000503 / 5583920164 match vendor master. ✓
- **Prices**: **Line 1 mismatch** — invoice unit price **49.28** vs. PO unit price **44.00** for MF-M8-50, a **+12.0%** difference, far beyond the 0.5% tolerance (lines 2–4 match exactly: 15.30, 27.60, 62.75). ✗

```json
{
  "invoice_id": "MF/25/104",
  "po_number": "PO-2025-4113",
  "decision": "hold",
  "discrepancies": ["PRICE_MISMATCH"],
  "explanation": "Line 1 (MF-M8-50) is billed at 49.28/unit vs. the PO price of 44.00/unit — a $5.28 (12.0%) overcharge, exceeding the 0.5% tolerance (adds $47.52 to the invoice). All other checks pass: quantities billed match GRN-88314 receipts (9/20/29/12), arithmetic and 6% tax are correct, currency and bank details match vendor master V03, and no duplicate payment exists. Hold pending price correction or PO amendment."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH"], "engine_codes": ["PRICE_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: SOI-25-104

**Step 1 — LLM call** (agent: `extractor`, 543+611 tok, 11.88s)
- assistant said:

```
{
  "invoice_no": "SOI-25-104",
  "vendor_name": "Stellar Office Interiors",
  "date": "2025-06-12",
  "po_number": "PO-2025-4114",
  "currency": "USD",
  "lines": [
    {
      "sku": "SO-CHR-T2",
      "description": "Task chair, mesh back",
      "qty": 21,
      "unit_price": 204.12,
      "amount": 4286.52
    },
    {
      "sku": "SO-MON-ARM",
      "description": "Dual monitor arm",
      "qty": 34,
      "unit_price": 74.25,
      "amount": 2524.50
    }
  ],
  "subtotal": 6811.02,
  "tax": 551.69,
  "total": 7362.71,
  "bank_name": "Front Range Credit Union",
  "bank_routing": "107000233",
  "bank_account": "8812204575",
  "payment_terms": "Net 30"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1728+1246 tok, 25.3s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4114"})`
- agent called `get_received_totals({"po_number":"PO-2025-4114"})`
- agent called `get_vendor_by_name({"name":"Stellar Office Interiors"})`
- agent called `search_payments({"invoice_no":"SOI-25-104","po_number":"PO-2025-4114","total":7362.71,"vendor_id":"V07"})`
- agent called `arithmetic_check({"vendor_id":"V07"})`
- assistant said:

```
I'll verify all checks for this invoice. The PO reference, vendor resolution, received quantities, duplicate screen, and arithmetic are independent checks, so I'll run them all now.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4114", "vendor_id": "V07", "date": "2025-06-07", "currency": "USD", "lines": [{"line_no": 1, "sku": "SO-CHR-T2", "description": "Task chair, mesh back", "qty": 21, "unit_price": 189.0}, {"line_no": 2, "sku": "SO-MON-ARM", "description": "Dual monitor arm", "qty": 34, "unit_price": 74.25}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 21, "2": 34}, "grn_count": 1, "grn_numbers": ["GRN-88315"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V07", "name": "Stellar Office Interiors", "city": "Denver, CO", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Front Range Credit Union", "bank_routing": "107000233", "bank_account": "8812204575", "tax_rate": 0.081}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (551.69 ~= 551.69).", "Remit-to bank details match vendor master."]}
```

**Step 9 — LLM call** (agent: `matcher`, 2190+849 tok, 14.45s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the summary:

- **PO existence**: PO-2025-4114 exists (vendor V07, USD, open). ✓
- **Line prices**: Line 2 matches exactly ($74.25 = $74.25), but Line 1 invoices at **$204.12/unit vs PO price $189.00** — a $15.12 (8.0%) difference, far beyond the 0.5% tolerance. ✗
- **Quantities vs GRNs**: Billed 21/34 matches GRN-88315 received totals of 21 and 34 (single GRN, full delivery). ✓
- **Currency**: USD on both invoice and PO. ✓
- **Arithmetic**: Tax OK ($551.69 ≈ 8.1% × $6,811.02); line amounts, subtotal, and total all internally consistent. ✓
- **Bank details**: Front Range Credit Union / 107000233 / 8812204575 match vendor master. ✓
- **Duplicates**: No matches in payment history (only HIST-7102, different PO and amount). ✓

```json
{
  "invoice_id": "SOI-25-104",
  "po_number": "PO-2025-4114",
  "decision": "hold",
  "discrepancies": ["PRICE_MISMATCH"],
  "explanation": "Line 1 (SO-CHR-T2) is billed at $204.12/unit vs the PO price of $189.00, an 8.0% overcharge that exceeds the 0.5% tolerance. All other checks pass: billed quantities (21, 34) match GRN-88315 receipts, tax of $551.69 equals 8.1% of the $6,811.02 subtotal, bank details match vendor master V07, currency is USD, and no duplicate payment exists."
}
```

**Decision: HOLD** — the invoice should be routed back to the buyer/vendor for a corrected invoice or price-variation approval before payment.
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH"], "engine_codes": ["PRICE_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: AMT-104

**Step 1 — LLM call** (agent: `extractor`, 559+690 tok, 19.05s)
- assistant said:

```
{
  "invoice_no": "AMT-104",
  "vendor_name": "Ashford Machine Tools Ltd.",
  "date": "2025-07-27",
  "po_number": "PO-2025-4115",
  "currency": "USD",
  "lines": [
    {
      "sku": "AM-END-12",
      "description": "End mill 12mm carbide",
      "qty": 22,
      "unit_price": 78.43,
      "amount": 1725.46
    },
    {
      "sku": "AM-CHK-125",
      "description": "Lathe chuck 125mm",
      "qty": 33,
      "unit_price": 412.60,
      "amount": 13615.80
    }
  ],
  "subtotal": 15341.26,
  "tax": 0.00,
  "total": 15341.26,
  "bank_name": "Pennine & Yorkshire Bank",
  "bank_routing": "GB29 NWBK 6016",
  "bank_account": "1331 9268 19",
  "payment_terms": "Net 30"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1673+725 tok, 11.63s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4115"})`
- agent called `get_received_totals({"po_number":"PO-2025-4115"})`
- agent called `get_vendor_by_name({"name":"Ashford Machine Tools Ltd."})`
- agent called `arithmetic_check({"vendor_id":"V10"})`
- agent called `search_payments({"invoice_no":"AMT-104","po_number":"PO-2025-4115","total":15341.26,"vendor_id":"V10"})`
- assistant said:

```
I'll verify this invoice against the PO, receipts, vendor master, and payment history using the tools.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4115", "vendor_id": "V10", "date": "2025-04-04", "currency": "USD", "lines": [{"line_no": 1, "sku": "AM-END-12", "description": "End mill 12mm carbide", "qty": 22, "unit_price": 68.2}, {"line_no": 2, "sku": "AM-CHK-125", "description": "Lathe chuck 125mm", "qty": 33, "unit_price": 412.6}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 22, "2": 33}, "grn_count": 1, "grn_numbers": ["GRN-88316"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V10", "name": "Ashford Machine Tools Ltd.", "city": "Sheffield, UK", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Pennine & Yorkshire Bank", "bank_routing": "GB29 NWBK 6016", "bank_account": "1331 9268 19", "tax_rate": 0.0}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — LLM call** (agent: `matcher`, 2128+784 tok, 16.91s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's my analysis:

**Check results:**
- **PO existence:** PO-2025-4115 exists and is referenced correctly. ✓
- **Quantities:** Line 1 billed 22 vs received 22 (GRN-88316); Line 2 billed 33 vs received 33. No QTY_MISMATCH. ✓
- **GRN:** GRN-88316 exists — no GRN_MISSING. ✓
- **Currency:** Invoice USD = PO USD. ✓
- **Arithmetic:** Tool passed all line math (22 × 78.43 = 1725.46; 33 × 412.60 = 13,615.80), subtotal, tax (0.00 = 0.0% × subtotal), and total. ✓
- **Duplicate:** No payments found for vendor V10/PO-2025-4115/invoice AMT-104. ✓
- **Bank:** Remit-to bank details match vendor master exactly. ✓
- **Price:** Line 2 matches (412.60 = 412.60), but **Line 1 invoice price 78.43 vs PO price 68.20 = $10.23 over, ~15.0% deviation — far beyond the 0.5% tolerance**. ✗ PRICE_MISMATCH

```json
{
  "invoice_id": "AMT-104",
  "po_number": "PO-2025-4115",
  "decision": "hold",
  "discrepancies": ["PRICE_MISMATCH"],
  "explanation": "Line 1 (AM-END-12) is billed at $78.43/unit vs the PO price of $68.20/unit — a $10.23 (15.0%) overcharge, exceeding the 0.5% tolerance. All other checks pass: quantities match receipts (22/22 and 33/33 on GRN-88316), arithmetic is correct, currency USD matches, bank details match vendor master, and no duplicates were found, so the invoice is placed on hold pending a price correction or PO amendment."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH"], "engine_codes": ["PRICE_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: INV-2025-0104

**Step 1 — LLM call** (agent: `extractor`, 485+272 tok, 12.36s)
- assistant said:

```
{
 "invoice_no": "INV-2025-0104",
 "vendor_name": "Bluefin Packaging Co.",
 "date": "2025-06-25",
 "po_number": "PO-2025-4116",
 "currency": "USD",
 "lines": [
  {"sku": "BP-115", "description": "Stretch wrap roll 80ga", "qty": 38, "unit_price": 12.80, "amount": 486.40},
  {"sku": "BP-201", "description": "Corrugated boxes 18x12x10, bundle 25", "qty": 7, "unit_price": 31.25, "amount": 218.75},
  {"sku": "BP-330", "description": "Packing tape, case of 36", "qty": 7, "unit_price": 58.90, "amount": 412.30}
 ],
 "subtotal": 1117.45,
 "tax": 78.22,
 "total": 1195.67,
 "bank_name": "Coastal Georgia Bank",
 "bank_routing": "061000104",
 "bank_account": "7719045512",
 "payment_terms": "Net 30"
}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0104"}`

**Step 3 — LLM call** (agent: `matcher`, 1929+1333 tok, 23.93s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4116"})`
- agent called `get_received_totals({"po_number":"PO-2025-4116"})`
- agent called `get_vendor_by_name({"name":"Bluefin Packaging Co."})`
- agent called `arithmetic_check({"vendor_id":"V02"})`
- agent called `search_payments({"invoice_no":"INV-2025-0104","po_number":"PO-2025-4116","total":1195.67,"vendor_id":"V02"})`
- assistant said:

```
I'll verify all checks using the tools. First, let me confirm the PO, received totals, vendor resolution, arithmetic, and duplicate screening.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4116", "vendor_id": "V02", "date": "2025-06-16", "currency": "USD", "lines": [{"line_no": 1, "sku": "BP-115", "description": "Stretch wrap roll 80ga", "qty": 38, "unit_price": 12.8}, {"line_no": 2, "sku": "BP-201", "description": "Corrugated boxes 18x12x10, bundle 25", "qty": 7, "unit_price": 31.25}, {"line_no": 3, "sku": "BP-330", "description": "Packing tape, case of 36", "qty": 7, "unit_price": 58.9}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 22, "2": 4, "3": 4}, "grn_count": 1, "grn_numbers": ["GRN-88317"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V02", "name": "Bluefin Packaging Co.", "city": "Savannah, GA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Coastal Georgia Bank", "bank_routing": "061000104", "bank_account": "7719045512", "tax_rate": 0.07, "memory": {"known_aliases": ["Bluefin Packaging Company"], "notes": "Re-issued invoices previously arrived with reformatted numbers (INV-25-xxx vs INV-2025-0xxx)."}}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (78.22 ~= 78.22).", "Remit-to bank details match vendor master."]}
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — LLM call** (agent: `matcher`, 2484+797 tok, 13.29s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the verification summary:

**Verification results:**
- **PO existence:** PO-2025-4116 found, matches vendor V02, currency USD ✓
- **Prices:** All three line unit prices match the PO exactly (12.80 / 31.25 / 58.90) ✓
- **Quantities:** ❌ GRN-88317 (only GRN) shows received totals of 22 / 4 / 4, but the invoice bills 38 / 7 / 7 — all three lines exceed received quantities
- **Arithmetic:** Passed — tax 78.22 = 7% × 1117.45, line amounts and total consistent ✓
- **Currency:** USD = USD ✓
- **Bank details:** Coastal Georgia Bank / 061000104 / 7719045512 match vendor master ✓
- **Duplicates:** No payment history match; prior payment INV-25-107 is a different PO and amount, so the reformatted-number pattern doesn't apply here ✓

```json
{
  "invoice_id": "INV-2025-0104",
  "po_number": "PO-2025-4116",
  "decision": "hold",
  "discrepancies": ["QTY_MISMATCH"],
  "explanation": "All three lines are billed above received quantities: BP-115 billed 38 vs 22 received, BP-201 billed 7 vs 4 received, and BP-330 billed 7 vs 4 received (per GRN-88317, the only GRN for PO-2025-4116). Prices, tax (78.22 = 7% of 1117.45), total, currency, bank details, and duplicate screening all passed, so the invoice is held pending receipt of the outstanding goods."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": ["QTY_MISMATCH"], "engine_codes": ["QTY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: HEC-2025-107

**Step 1 — LLM call** (agent: `extractor`, 584+777 tok, 9.79s)
- assistant said:

```
{
  "invoice_no": "HEC-2025-107",
  "vendor_name": "Helios Electrical Components",
  "date": "2025-06-23",
  "po_number": "PO-2025-4117",
  "currency": "USD",
  "lines": [
    {
      "sku": "HE-REL-24",
      "description": "Relay 24VDC 8-pin",
      "qty": 18,
      "unit_price": 14.20,
      "amount": 255.60
    },
    {
      "sku": "HE-CB-20",
      "description": "Circuit breaker 20A DIN",
      "qty": 35,
      "unit_price": 9.85,
      "amount": 344.75
    },
    {
      "sku": "HE-PSU-24",
      "description": "PSU 24V 10A DIN rail",
      "qty": 40,
      "unit_price": 96.30,
      "amount": 3852.00
    },
    {
      "sku": "HE-CAB-14",
      "description": "Copper cable 14AWG, 500ft spool",
      "qty": 29,
      "unit_price": 118.00,
      "amount": 3422.00
    }
  ],
  "subtotal": 7874.35,
  "tax": 677.19,
  "total": 8551.54,
  "bank_name": "Desert West Bank",
  "bank_routing": "122100024",
  "bank_account": "3348812706",
  "payment_terms": "Net 45"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1971+827 tok, 18.5s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4117"})`
- agent called `get_received_totals({"po_number":"PO-2025-4117"})`
- agent called `get_vendor_by_name({"name":"Helios Electrical Components"})`
- assistant said:

```
I'll verify this invoice against the PO, receipts, vendor master, and payment history. Starting with the independent lookups:
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4117", "vendor_id": "V05", "date": "2025-04-18", "currency": "USD", "lines": [{"line_no": 1, "sku": "HE-REL-24", "description": "Relay 24VDC 8-pin", "qty": 18, "unit_price": 14.2}, {"line_no": 2, "sku": "HE-CB-20", "description": "Circuit breaker 20A DIN", "qty": 35, "unit_price": 9.85}, {"line_no": 3, "sku": "HE-PSU-24", "description": "PSU 24V 10A DIN rail", "qty": 40, "unit_price": 96.3}, {"line_no": 4, "sku": "HE-CAB-14", "description": "Copper cable 14AWG, 500ft spool", "qty": 29, "unit_price": 118.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 10, "2": 21, "3": 24, "4": 17}, "grn_count": 1, "grn_numbers": ["GRN-88318"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V05", "name": "Helios Electrical Components", "city": "Tucson, AZ", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Desert West Bank", "bank_routing": "122100024", "bank_account": "3348812706", "tax_rate": 0.086}
```

**Step 7 — LLM call** (agent: `matcher`, 2428+245 tok, 8.23s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `arithmetic_check({"vendor_id":"V05"})`
- agent called `search_payments({"invoice_no":"HEC-2025-107","po_number":"PO-2025-4117","total":8551.54,"vendor_id":"V05"})`
- assistant said:

```
PO exists and matches, bank details match the vendor master, and one GRN exists. However, billed quantities exceed received quantities on every line. Now running the arithmetic verification and duplicate screen in parallel:
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (677.19 ~= 677.19).", "Remit-to bank details match vendor master."]}
```

**Step 9 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 10 — LLM call** (agent: `matcher`, 2584+790 tok, 14.23s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All verifications are complete. Here's the summary of the three-way match:

**Checks performed:**
- **PO existence:** PO-2025-4117 found, vendor V05, currency USD — matches invoice ✓
- **Prices:** All 4 line unit prices (14.20 / 9.85 / 96.30 / 118.00) match the PO exactly — within 0.5% tolerance ✓
- **Quantities (billed vs. total received across GRNs):**
  - HE-REL-24: billed 18 vs received 10 (GRN-88318) → **over-billed by 8**
  - HE-CB-20: billed 35 vs received 21 → **over-billed by 14**
  - HE-PSU-24: billed 40 vs received 24 → **over-billed by 16**
  - HE-CAB-14: billed 29 vs received 17 → **over-billed by 12**
- **Arithmetic & tax:** Passed — tax 677.19 ≈ 7874.35 × 8.6% ✓
- **Currency:** USD = USD ✓
- **Bank details:** Desert West Bank / 122100024 / 3348812706 match vendor master ✓
- **Duplicates:** No prior payments for this vendor/PO/total or invoice number ✓

```json
{
  "invoice_id": "HEC-2025-107",
  "po_number": "PO-2025-4117",
  "decision": "hold",
  "discrepancies": ["QTY_MISMATCH"],
  "explanation": "All four lines are billed ahead of receipts: invoice bills 18/35/40/29 units against only 10/21/24/17 units received on GRN-88318 (the sole GRN for PO-2025-4117), so billed quantities exceed total received on every line. Prices, currency, tax (677.19 ≈ 7874.35 × 8.6%), totals, bank details, and duplicate screening all passed, so the invoice is held pending receipt of the remaining goods."
}
```
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["QTY_MISMATCH"], "engine_codes": ["QTY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: GP-104

**Step 1 — LLM call** (agent: `extractor`, 492+259 tok, 10.06s)
- assistant said:

```
{

```

**Step 2 — pipeline_error**: `{"error": "no JSON object found in: {"}`


## Case: CCW-104

**Step 1 — LLM call** (agent: `extractor`, 587+645 tok, 12.32s)
- assistant said:

```
{
  "invoice_no": "CCW-104",
  "vendor_name": "Cascadia Chemical Works",
  "date": "2025-06-28",
  "po_number": "PO-2025-4119",
  "currency": "USD",
  "lines": [
    {
      "sku": "CC-IPA-55",
      "description": "Isopropyl alcohol 99%, 55gal drum",
      "qty": 2,
      "unit_price": 612.00,
      "amount": 1224.00
    },
    {
      "sku": "CC-COOL-55",
      "description": "Machine coolant concentrate, 55gal",
      "qty": 6,
      "unit_price": 744.50,
      "amount": 4467.00
    },
    {
      "sku": "CC-DEG-5",
      "description": "Industrial degreaser, 5gal",
      "qty": 5,
      "unit_price": 87.40,
      "amount": 437.00
    }
  ],
  "subtotal": 6128.00,
  "tax": 582.16,
  "total": 6710.16,
  "bank_name": "Puget Sound Trust",
  "bank_routing": "125000024",
  "bank_account": "9027481133",
  "payment_terms": "Net 60"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1754+941 tok, 18.74s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4119"})`
- agent called `get_received_totals({"po_number":"PO-2025-4119"})`
- agent called `get_vendor_by_name({"name":"Cascadia Chemical Works"})`
- agent called `arithmetic_check({"vendor_id":"V04"})`
- assistant said:

```
I'll verify this invoice against the ERP. Starting with the independent checks: PO existence, received totals, vendor resolution, and arithmetic.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4119", "vendor_id": "V04", "date": "2025-04-03", "currency": "USD", "lines": [{"line_no": 1, "sku": "CC-IPA-55", "description": "Isopropyl alcohol 99%, 55gal drum", "qty": 2, "unit_price": 612.0}, {"line_no": 2, "sku": "CC-COOL-55", "description": "Machine coolant concentrate, 55gal", "qty": 6, "unit_price": 744.5}, {"line_no": 3, "sku": "CC-DEG-5", "description": "Industrial degreaser, 5gal", "qty": 5, "unit_price": 87.4}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-4119"}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V04", "name": "Cascadia Chemical Works", "city": "Tacoma, WA", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Puget Sound Trust", "bank_routing": "125000024", "bank_account": "9027481133", "tax_rate": 0.095}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (582.16 ~= 582.16).", "Remit-to bank details match vendor master."]}
```

**Step 8 — LLM call** (agent: `matcher`, 2191+447 tok, 12.73s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"invoice_no":"CCW-104","po_number":"PO-2025-4119","total":6710.16,"vendor_id":"V04"})`
- assistant said:

```
Initial results: PO exists (matches vendor V04, USD, all three SKUs and unit prices exactly), arithmetic and tax pass, bank details match. However, **no GRNs exist** for this PO. Now checking payment history for duplicates:
```

**Step 9 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 10 — LLM call** (agent: `matcher`, 2299+1435 tok, 30.75s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the full verification summary:

**Verification results:**
- **PO existence:** PO-2025-4119 exists, is USD, and matches vendor V04 — ✅ no PO_NOT_FOUND
- **Prices:** All three line prices match the PO exactly ($612.00, $744.50, $87.40) — ✅ no PRICE_MISMATCH
- **GRNs:** No goods receipt notes exist for PO-2025-4119 → total received quantity is **0** on every line, while the invoice bills qty **2 / 6 / 5** — ❌ GRN_MISSING and QTY_MISMATCH
- **Arithmetic:** Tool-verified: line amounts (2×612.00=1224.00, 6×744.50=4467.00, 5×87.40=437.00), subtotal 6128.00, tax 582.16 = 9.5% × 6128.00, total 6710.16 — ✅ no TAX_ERROR / TOTAL_ERROR
- **Currency:** Both USD — ✅
- **Bank:** Remit-to (Puget Sound Trust / 125000024 / 9027481133) matches vendor master V04 — ✅ no BANK_CHANGE
- **Duplicates:** Payment history contains only HIST-7101 (different PO, different amount); duplicate search returned none — ✅ no DUPLICATE

```json
{
  "invoice_id": "CCW-104",
  "po_number": "PO-2025-4119",
  "decision": "hold",
  "discrepancies": ["GRN_MISSING", "QTY_MISMATCH"],
  "explanation": "Invoice CCW-104 bills quantities of 2/6/5 against PO-2025-4119, but no goods receipt notes exist for that PO, so total received quantity is 0 on every line (billed qty exceeds received qty). All other checks pass: unit prices match the PO exactly ($612.00/$744.50/$87.40), tax of 582.16 equals 9.5% of the 6128.00 subtotal, total 6710.16 is arithmetically correct, USD matches, remit-to bank matches vendor master V04, and no duplicates were found — so this is a hold pending receipts, not a rejection."
}
```
```

**Step 11 — verifier**: `{"agree": false, "matcher_codes": ["GRN_MISSING", "QTY_MISMATCH"], "engine_codes": ["GRN_MISSING"], "matcher_decision": "hold", "engine_decision": "hold"}`

**Step 12 — LLM call** (agent: `matcher`, 1933+1542 tok, 27.64s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4119"})`
- agent called `get_received_totals({"po_number":"PO-2025-4119"})`
- agent called `get_vendor_by_name({"name":"Cascadia Chemical Works"})`
- agent called `search_payments({"invoice_no":"CCW-104","po_number":"PO-2025-4119","total":6710.16,"vendor_id":"V04"})`
- agent called `arithmetic_check({"vendor_id":"V04"})`
- assistant said:

```
I'll re-run all verification checks with the tools, then reconcile my coding against the engine's result.
```

**Step 13 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4119", "vendor_id": "V04", "date": "2025-04-03", "currency": "USD", "lines": [{"line_no": 1, "sku": "CC-IPA-55", "description": "Isopropyl alcohol 99%, 55gal drum", "qty": 2, "unit_price": 612.0}, {"line_no": 2, "sku": "CC-COOL-55", "description": "Machine coolant concentrate, 55gal", "qty": 6, "unit_price": 744.5}, {"line_no": 3, "sku": "CC-DEG-5", "description": "Industrial degreaser, 5gal", "qty": 5, "unit_price": 87.4}], "status": "open"}
```

**Step 14 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-4119"}
```

**Step 15 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V04", "name": "Cascadia Chemical Works", "city": "Tacoma, WA", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Puget Sound Trust", "bank_routing": "125000024", "bank_account": "9027481133", "tax_rate": 0.095}
```

**Step 16 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 17 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (582.16 ~= 582.16).", "Remit-to bank details match vendor master."]}
```

**Step 18 — LLM call** (agent: `matcher`, 2418+1057 tok, 18.62s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All tool checks are consistent with the engine. Reconciling my codes:

- **PO found**: PO-2025-4119 exists, vendor V04, USD — no PO_NOT_FOUND, no CURRENCY_MISMATCH.
- **Prices**: invoice lines match PO unit prices exactly ($612.00, $744.50, $87.40) — no PRICE_MISMATCH.
- **GRNs**: `get_received_totals` returns "no GRNs exist for PO-2025-4119" — **GRN_MISSING** applies. I incorrectly also coded QTY_MISMATCH: since *zero* GRNs exist, the billed-vs-received comparison is undefined (received totals are not established at 0), so GRN_MISSING is the governing code for the missing receipt. QTY_MISMATCH is for over-billing against *existing* GRN receipts. Removing it per the engine.
- **Arithmetic** (`arithmetic_check`): tax $582.16 = 9.5% × $6,128.00; line amounts, subtotal, and total $6,710.16 all pass — no TAX_ERROR/TOTAL_ERROR.
- **Bank**: Puget Sound Trust / 125000024 / 9027481133 match vendor master — no BANK_CHANGE.
- **Duplicates**: `search_payments` returns no potential duplicates; payment history contains only HIST-7101 for PO-2025-4051 — no DUPLICATE.

Decision rule: DUPLICATE absent, one other discrepancy present → **hold**.

```json
{
  "invoice_id": "CCW-104",
  "po_number": "PO-2025-4119",
  "decision": "hold",
  "discrepancies": ["GRN_MISSING"],
  "explanation": "Invoice CCW-104 matches PO-2025-4119 on all three line prices ($612.00, $744.50, $87.40), currency (USD), arithmetic (tax $582.16 = 9.5% x $6,128.00; total $6,710.16), and remit-to bank details, and no duplicate payment was found. However, no goods receipt notes exist for PO-2025-4119, so delivery is unverified — GRN_MISSING applies and the invoice is held. QTY_MISMATCH is not separately coded because with zero GRNs the received-quantity comparison is undefined; GRN_MISSING is the governing discrepancy."
}
```
```

**Step 19 — verifier**: `{"agree": true, "matcher_codes": ["GRN_MISSING"], "engine_codes": ["GRN_MISSING"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: ALS-INV-104

**Step 1 — LLM call** (agent: `extractor`, 580+580 tok, 7.83s)
- assistant said:

```
{
  "invoice_no": "ALS-INV-104",
  "vendor_name": "AURIGA LOGISTICS SERVICES",
  "date": "2025-07-08",
  "po_number": "PO-2025-4120",
  "currency": "USD",
  "lines": [
    {
      "sku": "AL-LTL-STD",
      "description": "LTL freight, standard lane",
      "qty": 19,
      "unit_price": 425.00,
      "amount": 8075.00
    },
    {
      "sku": "AL-LIFT",
      "description": "Liftgate service",
      "qty": 33,
      "unit_price": 45.00,
      "amount": 1485.00
    },
    {
      "sku": "AL-WHS-P",
      "description": "Warehouse handling, per pallet",
      "qty": 15,
      "unit_price": 18.50,
      "amount": 277.50
    }
  ],
  "subtotal": 9837.50,
  "tax": 0.00,
  "total": 9837.50,
  "bank_name": "River City Bank",
  "bank_routing": "084000026",
  "bank_account": "6650371928",
  "payment_terms": "Net 30"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1718+686 tok, 15.56s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4120"})`
- agent called `get_vendor_by_name({"name":"AURIGA LOGISTICS SERVICES"})`
- agent called `get_received_totals({"po_number":"PO-2025-4120"})`
- assistant said:

```
I'll verify this invoice against the PO, receipts, vendor master, and payment history. Let me start with the independent lookups.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4120", "vendor_id": "V06", "date": "2025-06-05", "currency": "USD", "lines": [{"line_no": 1, "sku": "AL-LTL-STD", "description": "LTL freight, standard lane", "qty": 19, "unit_price": 425.0}, {"line_no": 2, "sku": "AL-LIFT", "description": "Liftgate service", "qty": 33, "unit_price": 45.0}, {"line_no": 3, "sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 15, "unit_price": 18.5}], "status": "open"}
```

**Step 5 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V06", "name": "Auriga Logistics Services", "city": "Memphis, TN", "currency": "USD", "payment_terms": "Net 30", "bank_name": "River City Bank", "bank_routing": "084000026", "bank_account": "6650371928", "tax_rate": 0.0}
```

**Step 6 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-4120"}
```

**Step 7 — LLM call** (agent: `matcher`, 2083+633 tok, 10.41s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"invoice_no":"ALS-INV-104","po_number":"PO-2025-4120","total":9837.5,"vendor_id":"V06"})`
- agent called `arithmetic_check({"vendor_id":"V06"})`
- assistant said:

```
The PO exists and bank details match the vendor master exactly (River City Bank, routing 084000026, account 6650371928). Critically, **no GRNs exist** for this PO. Now let me run the duplicate screen and the deterministic arithmetic verification.
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2254+1600 tok, 31.47s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the verification summary:

**Check results:**
- **PO existence:** PO-2025-4120 exists (vendor V06, USD) ✓
- **Line prices:** $425.00 / $45.00 / $18.50 match PO exactly (0% difference, within 0.5% tolerance) ✓
- **Arithmetic:** arithmetic_check passed — line amounts, subtotal $9,837.50, tax $0.00 (0% rate), and total all clean ✓
- **Currency:** Invoice USD = PO USD ✓
- **Bank:** River City Bank / routing 084000026 / account 6650371928 match vendor master ✓
- **Duplicates:** No matches in payment history (only ALS-INV-107 on PO-2025-4122 for $13,741.75 — different PO, number, and amount) ✓
- **Vendor name:** Case-only variation of "Auriga Logistics Services" — acceptable per policy ✓
- **Receipts:** **No GRNs exist for PO-2025-4120** — total received qty is 0 across all lines, while the invoice bills 19 / 33 / 15

```json
{
  "invoice_id": "ALS-INV-104",
  "po_number": "PO-2025-4120",
  "decision": "hold",
  "discrepancies": ["GRN_MISSING", "QTY_MISMATCH"],
  "explanation": "All line prices ($425.00/$45.00/$18.50), arithmetic (subtotal $9,837.50, tax $0.00, total $9,837.50), currency (USD), bank details (routing 084000026/acct 6650371928), and duplicate screen are clean. However, no goods receipt notes exist for PO-2025-4120 (GRN_MISSING), so total received quantity is 0 across all lines while the invoice bills 19, 33, and 15 units (QTY_MISMATCH). Hold until goods receipt is posted; the receipt issue is the root cause, so the quantity mismatch should resolve once GRNs are recorded."
}
```

**Decision: HOLD** — the invoice is internally consistent and matches the PO and vendor master on every count, but it bills quantities that have never been received. Post the GRNs (or confirm the deliveries were made under a different PO) before releasing payment.
```

**Step 11 — verifier**: `{"agree": false, "matcher_codes": ["GRN_MISSING", "QTY_MISMATCH"], "engine_codes": ["GRN_MISSING"], "matcher_decision": "hold", "engine_decision": "hold"}`

**Step 12 — LLM call** (agent: `matcher`, 1889+846 tok, 14.1s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4120"})`
- agent called `get_received_totals({"po_number":"PO-2025-4120"})`
- agent called `get_vendor_by_name({"name":"AURIGA LOGISTICS SERVICES"})`
- assistant said:

```
I'll re-verify every check with the tools, paying particular attention to the quantity question given the engine's correction.
```

**Step 13 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4120", "vendor_id": "V06", "date": "2025-06-05", "currency": "USD", "lines": [{"line_no": 1, "sku": "AL-LTL-STD", "description": "LTL freight, standard lane", "qty": 19, "unit_price": 425.0}, {"line_no": 2, "sku": "AL-LIFT", "description": "Liftgate service", "qty": 33, "unit_price": 45.0}, {"line_no": 3, "sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 15, "unit_price": 18.5}], "status": "open"}
```

**Step 14 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-4120"}
```

**Step 15 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V06", "name": "Auriga Logistics Services", "city": "Memphis, TN", "currency": "USD", "payment_terms": "Net 30", "bank_name": "River City Bank", "bank_routing": "084000026", "bank_account": "6650371928", "tax_rate": 0.0}
```

**Step 16 — LLM call** (agent: `matcher`, 2251+452 tok, 13.63s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"invoice_no":"ALS-INV-104","po_number":"PO-2025-4120","total":9837.5,"vendor_id":"V06"})`
- agent called `arithmetic_check({"vendor_id":"V06"})`
- assistant said:

```
PO and vendor confirmed; `get_received_totals` confirms zero GRNs exist for this PO. Now let me run the duplicate screen and the deterministic arithmetic check:
```

**Step 17 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 18 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 19 — LLM call** (agent: `matcher`, 2395+1579 tok, 27.93s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All verification steps are complete. Here's my re-assessment, adopting the engine's corrected code set:

**Check-by-check results:**
- **PO existence:** PO-2025-4120 found, vendor V06, currency USD — matches invoice currency. ✓
- **Prices:** 425.00 / 45.00 / 18.50 match PO line prices exactly (0% variance, within 0.5% tolerance). ✓
- **GRN/receipts:** `get_received_totals` returns an error — **no GRNs exist for PO-2025-4120 at all**. The receipt record itself is absent; this is the root cause captured by GRN_MISSING. The engine evaluates QTY_MISMATCH only where received totals exist to compare against; with zero receipts on record, GRN_MISSING is the operative (and non-redundant) code. I've removed QTY_MISMATCH per the engine's correction — decision is unchanged either way.
- **Arithmetic:** `arithmetic_check` returned zero findings — line amounts, subtotal (9837.50), tax (0.00 ≈ 0.00% × 9837.50), and total all pass. ✓
- **Bank:** River City Bank / routing 084000026 / account 6650371928 match vendor master exactly. ✓
- **Duplicates:** `search_payments` found no matches; payment history contains only ALS-INV-107 (different invoice, PO-2025-4122, different amount). ✓
- **Vendor name:** "AURIGA LOGISTICS SERVICES" is a case-variant of master "Auriga Logistics Services" — not a discrepancy.

```json
{
  "invoice_id": "ALS-INV-104",
  "po_number": "PO-2025-4120",
  "decision": "hold",
  "discrepancies": ["GRN_MISSING"],
  "explanation": "No goods receipt notes exist for PO-2025-4120, so the three-way match cannot be completed: the billed quantities (19 LTL, 33 liftgate, 15 pallets) cannot be validated against any receipts, and the PO remains open. All other checks pass — line prices match the PO exactly (425.00/45.00/18.50), arithmetic_check confirms subtotal 9837.50, tax 0.00, and total 9837.50, currency (USD) matches the PO, remit-to bank details match vendor master (routing 084000026, account 6650371928), and the duplicate screen found no matches. Hold pending receipt of valid GRNs for this PO."
}
```

**Correction note for the auditor:** My prior answer listed QTY_MISMATCH in addition to GRN_MISSING. While billed quantities nominally exceed the (nonexistent) received totals, the deterministic engine correctly treats the complete absence of GRNs as the single root-cause discrepancy (GRN_MISSING) rather than double-reporting it as a quantity breach — QTY_MISMATCH applies when receipts exist but are insufficient. The decision remains **hold** under both code sets.
```

**Step 20 — verifier**: `{"agree": true, "matcher_codes": ["GRN_MISSING"], "engine_codes": ["GRN_MISSING"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: INV-2025-0107

**Step 1 — LLM call** (agent: `extractor`, 550+765 tok, 10.41s)
- assistant said:

```
{
  "invoice_no": "INV-2025-0107",
  "vendor_name": "Bluefin Packaging Co.",
  "date": "2025-07-28",
  "po_number": "PO-2025-4121",
  "currency": "USD",
  "lines": [
    {
      "sku": "BP-450",
      "description": "Foam inserts, custom cut",
      "qty": 8,
      "unit_price": 4.15,
      "amount": 33.20
    },
    {
      "sku": "BP-201",
      "description": "Corrugated boxes 18x12x10, bundle 25",
      "qty": 29,
      "unit_price": 31.25,
      "amount": 906.25
    },
    {
      "sku": "BP-330",
      "description": "Packing tape, case of 36",
      "qty": 24,
      "unit_price": 58.90,
      "amount": 1413.60
    }
  ],
  "subtotal": 2353.05,
  "tax": 164.71,
  "total": 2517.76,
  "bank_name": "Coastal Georgia Bank",
  "bank_routing": "061000104",
  "bank_account": "7719045512",
  "payment_terms": "Net 30"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0107"}`

**Step 3 — LLM call** (agent: `matcher`, 1930+783 tok, 16.15s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4121"})`
- agent called `get_received_totals({"po_number":"PO-2025-4121"})`
- agent called `get_vendor_by_name({"name":"Bluefin Packaging Co."})`
- assistant said:

```
I'll verify this invoice systematically. First, let me confirm the PO, received quantities, and resolve the vendor record.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4121", "vendor_id": "V02", "date": "2025-05-14", "currency": "USD", "lines": [{"line_no": 1, "sku": "BP-450", "description": "Foam inserts, custom cut", "qty": 8, "unit_price": 4.15}, {"line_no": 2, "sku": "BP-201", "description": "Corrugated boxes 18x12x10, bundle 25", "qty": 29, "unit_price": 31.25}, {"line_no": 3, "sku": "BP-330", "description": "Packing tape, case of 36", "qty": 24, "unit_price": 58.9}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 8, "2": 29, "3": 24}, "grn_count": 1, "grn_numbers": ["GRN-88320"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V02", "name": "Bluefin Packaging Co.", "city": "Savannah, GA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Coastal Georgia Bank", "bank_routing": "061000104", "bank_account": "7719045512", "tax_rate": 0.07, "memory": {"known_aliases": ["Bluefin Packaging Company"], "notes": "Re-issued invoices previously arrived with reformatted numbers (INV-25-xxx vs INV-2025-0xxx)."}}
```

**Step 7 — LLM call** (agent: `matcher`, 2371+418 tok, 11.81s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"invoice_no":"INV-2025-0107","po_number":"PO-2025-4121","total":2517.76,"vendor_id":"V02"})`
- agent called `arithmetic_check({"vendor_id":"V02"})`
- assistant said:

```
PO confirmed, vendor resolved to V02, and received quantities (8/29/24) match billed quantities. The payment history shows a suspicious entry — INV-25-107 for the same vendor, PO, and total. Let me run the duplicate search and arithmetic verification.
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": [{"invoice_no": "INV-25-107", "vendor_id": "V02", "po_number": "PO-2025-4121", "amount": 2517.76, "currency": "USD", "paid_date": "2025-06-14", "match_reasons": ["same vendor + PO + amount already paid"]}]}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (164.71 ~= 164.71).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2616+1038 tok, 18.7s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. The arithmetic and bank details pass, but the duplicate screen triggered: payment history contains **INV-25-107** — same vendor (V02), same PO (PO-2025-4121), same total ($2,517.76) — paid on 2025-06-14. The vendor memory note confirms this is exactly the known reformatting pattern (INV-2025-0xxx ↔ INV-25-xxx), so this is a re-issued duplicate of an already-paid invoice. Under the decision rule, a DUPLICATE requires rejection.

```json
{
  "invoice_id": "INV-2025-0107",
  "po_number": "PO-2025-4121",
  "decision": "reject",
  "discrepancies": ["DUPLICATE"],
  "explanation": "Invoice INV-2025-0107 for $2,517.76 is a duplicate of INV-25-107, already paid 2025-06-14 for the same vendor (V02), same PO (PO-2025-4121), and identical total — matching the vendor's known invoice-number reformatting pattern (INV-25-107 ≡ INV-2025-0107). All other checks passed: line prices match PO ($4.15/$31.25/$58.90), billed qty equals received qty (8/29/24 per GRN-88320), tax $164.71 = 7% of $2,535.05... subtotal verified, and bank details match master, but the prior payment mandates rejection to prevent double payment."
}
```

Wait — let me correct that subtotal figure in the explanation for accuracy: the verified subtotal is **$2,353.05** and tax $164.71 = 0.07 × $2,353.05, confirmed by the arithmetic check. Final answer:

```json
{
  "invoice_id": "INV-2025-0107",
  "po_number": "PO-2025-4121",
  "decision": "reject",
  "discrepancies": ["DUPLICATE"],
  "explanation": "Invoice INV-2025-0107 for $2,517.76 duplicates INV-25-107, already paid 2025-06-14 for the same vendor (V02), same PO (PO-2025-4121), and identical total, consistent with the vendor's known re-issuance pattern (INV-25-107 ≡ INV-2025-0107). All other checks passed: line prices match PO ($4.15/$31.25/$58.90), billed qty equals received qty (8/29/24 per GRN-88320), arithmetic verified (subtotal $2,353.05, tax $164.71 = 7%), and bank details match vendor master — but the prior payment requires rejection to prevent double payment."
}
```
```

**Step 11 — pipeline_error**: `{"error": "Extra data: line 8 column 1 (char 678)"}`


## Case: ALS-INV-107

**Step 1 — LLM call** (agent: `extractor`, 545+697 tok, 5.07s)
- assistant said:

```
{
 "invoice_no": "ALS-INV-107",
 "vendor_name": "Auriga Logistics Services",
 "date": "2025-07-05",
 "po_number": "PO-2025-4122",
 "currency": "USD",
 "lines": [
  {"sku": "AL-LTL-STD", "description": "LTL freight, standard lane", "qty": 27, "unit_price": 425.00, "amount": 11475.00},
  {"sku": "AL-LIFT", "description": "Liftgate service", "qty": 23, "unit_price": 45.00, "amount": 1035.00},
  {"sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 8, "unit_price": 18.50, "amount": 148.00},
  {"sku": "AL-FUEL", "description": "Fuel surcharge", "qty": 17, "unit_price": 63.75, "amount": 1083.75}
 ],
 "subtotal": 13741.75,
 "tax": 0.00,
 "total": 13741.75,
 "bank_name": "River City Bank",
 "bank_routing": "084000026",
 "bank_account": "6650371928",
 "payment_terms": "Net 30"
}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1976+995 tok, 16.45s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4122"})`
- agent called `get_received_totals({"po_number":"PO-2025-4122"})`
- agent called `get_vendor_by_name({"name":"Auriga Logistics Services"})`
- assistant said:

```
I'll verify this invoice against the ERP system. First, let me check the PO, received quantities, and resolve the vendor.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4122", "vendor_id": "V06", "date": "2025-04-07", "currency": "USD", "lines": [{"line_no": 1, "sku": "AL-LTL-STD", "description": "LTL freight, standard lane", "qty": 27, "unit_price": 425.0}, {"line_no": 2, "sku": "AL-LIFT", "description": "Liftgate service", "qty": 23, "unit_price": 45.0}, {"line_no": 3, "sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 8, "unit_price": 18.5}, {"line_no": 4, "sku": "AL-FUEL", "description": "Fuel surcharge", "qty": 17, "unit_price": 63.75}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 27, "2": 23, "3": 8, "4": 17}, "grn_count": 1, "grn_numbers": ["GRN-88321"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V06", "name": "Auriga Logistics Services", "city": "Memphis, TN", "currency": "USD", "payment_terms": "Net 30", "bank_name": "River City Bank", "bank_routing": "084000026", "bank_account": "6650371928", "tax_rate": 0.0}
```

**Step 7 — LLM call** (agent: `matcher`, 2409+251 tok, 4.98s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"invoice_no":"ALS-INV-107","po_number":"PO-2025-4122","total":13741.75,"vendor_id":"V06"})`
- agent called `arithmetic_check({"vendor_id":"V06"})`
- assistant said:

```
PO and vendor resolved. All 4 line prices match the PO exactly, and billed quantities (27/23/8/17) match received totals from GRN-88321. Now let me verify duplicates and arithmetic.
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": [{"invoice_no": "ALS-INV-107", "vendor_id": "V06", "po_number": "PO-2025-4122", "amount": 13741.75, "currency": "USD", "paid_date": "2025-07-02", "match_reasons": ["invoice number already paid (normalized match)", "same vendor + PO + amount already paid"]}]}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2649+403 tok, 10.63s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
**Duplicate confirmed.** All pricing, quantity, arithmetic, currency, and bank checks pass — but this invoice was already paid on 2025-07-02, three days before this submission's date of 2025-07-05.

```json
{
  "invoice_id": "ALS-INV-107",
  "po_number": "PO-2025-4122",
  "decision": "reject",
  "discrepancies": ["DUPLICATE"],
  "explanation": "Payment history shows invoice ALS-INV-107 for vendor V06 on PO-2025-4122 was already paid $13,741.75 (USD) on 2025-07-02 — both the invoice number and the vendor+PO+total combination match an existing payment. All other checks pass (4/4 line prices match PO, billed qty equals GRN-88321 received qty of 27/23/8/17, arithmetic and bank details verified), but per policy a DUPLICATE requires rejection."
}
```
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["DUPLICATE"], "engine_codes": ["DUPLICATE"], "matcher_decision": "reject", "engine_decision": "reject"}`


## Case: NIS-2025-107

**Step 1 — LLM call** (agent: `extractor`, 516+263 tok, 4.25s)
- assistant said:

```
{"invoice_no": "NIS-2025-107", "vendor_name": "Northgate Industrial Supply LLC", "date": "2025-06-21", "po_number": "PO-2025-4123", "currency": "USD", "lines": [{"sku": "NG-7720", "description": "Safety goggles, anti-fog", "qty": 17, "unit_price": 6.95, "amount": 118.15}, {"sku": "NG-3305", "description": "Absorbent pads, case", "qty": 6, "unit_price": 42.5, "amount": 255.0}, {"sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 30, "unit_price": 149.0, "amount": 4470.0}], "subtotal": 4843.15, "tax": 388.27, "total": 5231.42, "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "payment_terms": "Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1944+1543 tok, 35.13s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4123"})`
- agent called `get_received_totals({"po_number":"PO-2025-4123"})`
- agent called `get_vendor_by_name({"name":"Northgate Industrial Supply LLC"})`
- agent called `search_payments({"invoice_no":"NIS-2025-107","po_number":"PO-2025-4123","total":5231.42,"vendor_id":"V01"})`
- agent called `arithmetic_check({"vendor_id":"V01"})`
- assistant said:

```
I'll verify this invoice against the PO, GRN totals, vendor master, payment history, and run the deterministic arithmetic check. All these checks are independent, so I'll run them together:
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4123", "vendor_id": "V01", "date": "2025-06-04", "currency": "USD", "lines": [{"line_no": 1, "sku": "NG-7720", "description": "Safety goggles, anti-fog", "qty": 17, "unit_price": 6.95}, {"line_no": 2, "sku": "NG-3305", "description": "Absorbent pads, case", "qty": 6, "unit_price": 42.5}, {"line_no": 3, "sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 30, "unit_price": 149.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 17, "2": 6, "3": 30}, "grn_count": 1, "grn_numbers": ["GRN-88322"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V01", "name": "Northgate Industrial Supply LLC", "city": "Columbus, OH", "currency": "USD", "payment_terms": "Net 60", "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "tax_rate": 0.0725, "memory": {"known_aliases": ["Northgate Ind. Supply (a div. of NIS Holdings)", "NIS Holdings LLC", "Northgate Industrial"], "notes": "Invoices under NIS Holdings trade names since 2024 reorg. Split deliveries common."}}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TAX_ERROR", "evidence": "Tax 388.27 != tax_rate 0.0725 x subtotal 4843.15 = 351.13 (tolerance $0.02)."}], "checks_passed": ["Remit-to bank details match vendor master."]}
```

**Step 9 — LLM call** (agent: `matcher`, 2559+1188 tok, 22.9s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's my analysis:

**Check results:**
- **PO**: PO-2025-4123 exists (V01, USD, open) — all 3 SKUs match the PO lines
- **Prices**: $6.95 / $42.50 / $149.00 — identical to PO unit prices (0% variance, within 0.5% tolerance)
- **Quantities**: Billed 17/6/30 vs. received totals from GRN-88322 of 17/6/30 — full match, no overbilling
- **GRN**: GRN-88322 exists — no GRN_MISSING
- **Duplicate screen**: No payment history matches for vendor V01 + PO-2025-4123 + $5,231.42, and invoice NIS-2025-107 doesn't appear in history (only HIST-7100, $2,982.56, different PO)
- **Currency**: USD = USD
- **Arithmetic**: Line amounts ($118.15, $255.00, $4,470.00), subtotal ($4,843.15), and total ($5,231.42) all verified; **BUT tax check failed** — invoiced tax $388.27 vs. expected 0.0725 × $4,843.15 = $351.13, a $37.14 overcharge (tolerance $0.02)
- **Bank**: Remit-to First Commerce Bank, routing 021000021, account 4402198837 — exact match to vendor master

```json
{
  "invoice_id": "NIS-2025-107",
  "po_number": "PO-2025-4123",
  "decision": "hold",
  "discrepancies": ["TAX_ERROR"],
  "explanation": "Invoiced tax of $388.27 exceeds the expected 7.25% x $4,843.15 subtotal = $351.13 by $37.14, well beyond the $0.02 tolerance (TAX_ERROR). All other checks pass: line prices match PO-2025-4123 exactly ($6.95/$42.50/$149.00), billed quantities (17/6/30) equal total received per GRN-88322 (17/6/30), line math/subtotal/total verify, currency is USD, remit-to bank matches vendor master, and the duplicate screen found no prior payment for this vendor/PO/total or invoice number."
}
```

**Decision: HOLD** — the invoice is a clean three-way match on price and quantity, but the sales tax is overstated by $37.14 relative to the vendor master's 7.25% rate. Recommend returning to Northgate for a corrected tax calculation before payment.
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": ["TAX_ERROR"], "engine_codes": ["TAX_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: VPL-2025-104

**Step 1 — LLM call** (agent: `extractor`, 518+638 tok, 15.17s)
- assistant said:

```
{
  "invoice_no": "VPL-2025-104",
  "vendor_name": "Vireo Print & Label GmbH",
  "date": "2025-07-02",
  "po_number": "PO-2025-4124",
  "currency": "EUR",
  "lines": [
    {"sku": "VP-LBL-4x6", "description": "Thermal labels 4x6, roll 500", "qty": 12, "unit_price": 21.40, "amount": 256.80},
    {"sku": "VP-RIB-110", "description": "TTR ribbon 110mm", "qty": 28, "unit_price": 9.60, "amount": 268.80},
    {"sku": "VP-TAG-ASSET", "description": "Asset tags, custom, 1000", "qty": 33, "unit_price": 340.00, "amount": 11220.00}
  ],
  "subtotal": 11745.60,
  "tax": 2284.26,
  "total": 14029.86,
  "bank_name": "Hansa Handelsbank",
  "bank_routing": "DE44 5001 0517",
  "bank_account": "5407 3249 31",
  "payment_terms": "Net 60"
}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1890+1100 tok, 18.34s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4124"})`
- agent called `get_received_totals({"po_number":"PO-2025-4124"})`
- agent called `get_vendor_by_name({"name":"Vireo Print & Label GmbH"})`
- agent called `search_payments({"invoice_no":"VPL-2025-104","po_number":"PO-2025-4124","total":14029.86,"vendor_id":"V09"})`
- agent called `arithmetic_check({"vendor_id":"V09"})`
- assistant said:

```
I'll verify all checks using the tools. Since the PO context already provides vendor_id V09, I can run all independent checks in parallel.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4124", "vendor_id": "V09", "date": "2025-05-07", "currency": "EUR", "lines": [{"line_no": 1, "sku": "VP-LBL-4x6", "description": "Thermal labels 4x6, roll 500", "qty": 12, "unit_price": 21.4}, {"line_no": 2, "sku": "VP-RIB-110", "description": "TTR ribbon 110mm", "qty": 28, "unit_price": 9.6}, {"line_no": 3, "sku": "VP-TAG-ASSET", "description": "Asset tags, custom, 1000", "qty": 33, "unit_price": 340.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 12, "2": 28, "3": 33}, "grn_count": 1, "grn_numbers": ["GRN-88323"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V09", "name": "Vireo Print & Label GmbH", "city": "Hamburg, DE", "currency": "EUR", "payment_terms": "Net 60", "bank_name": "Hansa Handelsbank", "bank_routing": "DE44 5001 0517", "bank_account": "5407 3249 31", "tax_rate": 0.19, "memory": {"known_aliases": ["Vireo Print and Label"], "notes": "Always bills in EUR. Any USD invoice from this vendor is anomalous."}}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TAX_ERROR", "evidence": "Tax 2284.26 != tax_rate 0.1900 x subtotal 11745.60 = 2231.66 (tolerance $0.02)."}], "checks_passed": ["Remit-to bank details match vendor master."]}
```

**Step 9 — LLM call** (agent: `matcher`, 2490+1078 tok, 19.8s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the verification summary:

**Checks performed:**
1. **PO existence** ✓ — PO-2025-4124 exists (vendor V09, EUR, status open)
2. **Prices** ✓ — All three lines match PO exactly: €21.40, €9.60, €340.00 (0% variance, within 0.5% tolerance)
3. **Quantities** ✓ — Billed 12/28/33 equals total received across GRN-88323 (12/28/33); no over-billing
4. **GRN** ✓ — GRN-88323 exists for this PO
5. **Duplicates** ✓ — No matching payments found for this vendor/PO/total/invoice number
6. **Currency** ✓ — Invoice EUR matches PO and vendor master EUR
7. **Arithmetic** — Line amounts (256.80 + 268.80 + 11,220.00 = 11,745.60) and total (11,745.60 + 2,284.26 = 14,029.86) all reconcile, **but tax fails**: 2284.26 ≠ 0.19 × 11,745.60 = 2,231.66
8. **Bank details** ✓ — Remit-to (Hansa Handelsbank / DE44 5001 0517 / 5407 3249 31) matches vendor master exactly

```json
{
  "invoice_id": "VPL-2025-104",
  "po_number": "PO-2025-4124",
  "decision": "hold",
  "discrepancies": ["TAX_ERROR"],
  "explanation": "All three lines match PO-2025-4124 prices exactly (€21.40/€9.60/€340.00), billed quantities equal GRN-88323 received quantities (12/28/33), currency is EUR, bank details match vendor master V09, and no duplicate payments exist. However, tax of €2,284.26 differs from the expected 19% × subtotal €11,745.60 = €2,231.66 by €52.60, exceeding the $0.02 tolerance, so the invoice is held for tax correction."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": ["TAX_ERROR"], "engine_codes": ["TAX_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: SOI-25-107

**Step 1 — LLM call** (agent: `extractor`, 546+547 tok, 6.9s)
- assistant said:

```
{
  "invoice_no": "SOI-25-107",
  "vendor_name": "Stellar Office Interiors",
  "date": "2025-07-23",
  "po_number": "PO-2025-4125",
  "currency": "USD",
  "lines": [
    {
      "sku": "SO-FIL-3D",
      "description": "File cabinet 3-drawer",
      "qty": 26,
      "unit_price": 156.80,
      "amount": 4076.80
    },
    {
      "sku": "SO-CHR-T2",
      "description": "Task chair, mesh back",
      "qty": 18,
      "unit_price": 189.00,
      "amount": 3492.00
    }
  ],
  "subtotal": 7568.80,
  "tax": 613.07,
  "total": 8181.87,
  "bank_name": "Front Range Credit Union",
  "bank_routing": "107000233",
  "bank_account": "8812204575",
  "payment_terms": "Net 30"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1737+659 tok, 12.21s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4125"})`
- agent called `get_received_totals({"po_number":"PO-2025-4125"})`
- agent called `get_vendor_by_name({"name":"Stellar Office Interiors"})`
- agent called `search_payments({"invoice_no":"SOI-25-107","po_number":"PO-2025-4125","total":8181.87,"vendor_id":"V07"})`
- agent called `arithmetic_check({"vendor_id":"V07"})`
- assistant said:

```
I'll verify all checks for invoice SOI-25-107. The PO context gives me vendor_id V07, so I can run all independent checks in parallel: PO existence, received totals, vendor master resolution, duplicate screening, and arithmetic verification.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4125", "vendor_id": "V07", "date": "2025-05-10", "currency": "USD", "lines": [{"line_no": 1, "sku": "SO-FIL-3D", "description": "File cabinet 3-drawer", "qty": 26, "unit_price": 156.8}, {"line_no": 2, "sku": "SO-CHR-T2", "description": "Task chair, mesh back", "qty": 18, "unit_price": 189.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 26, "2": 18}, "grn_count": 1, "grn_numbers": ["GRN-88324"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V07", "name": "Stellar Office Interiors", "city": "Denver, CO", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Front Range Credit Union", "bank_routing": "107000233", "bank_account": "8812204575", "tax_rate": 0.081}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TOTAL_ERROR", "evidence": "Line SO-CHR-T2: amount 3492.00 != qty 18 x unit price 189.00 = 3402.00."}], "checks_passed": ["Tax OK (613.07 ~= 613.07).", "Remit-to bank details match vendor master."]}
```

**Step 9 — LLM call** (agent: `matcher`, 2262+1032 tok, 18.79s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the summary:

**Verification results:**
- **PO existence:** PO-2025-4125 exists for vendor V07 ✓
- **Prices:** Line 1: $156.80 = PO $156.80 ✓; Line 2: $189.00 = PO $189.00 ✓ (no PRICE_MISMATCH)
- **Quantities:** Billed 26/18 vs received 26/18 per GRN-88324 ✓ (no QTY_MISMATCH, no GRN_MISSING)
- **Currency:** Invoice USD = PO USD ✓
- **Duplicates:** No matching payments in history ✓
- **Bank details:** Remit-to matches vendor master (Front Range Credit Union / 107000233 / 8812204575) ✓
- **Arithmetic:** ❌ **TOTAL_ERROR** — Line SO-CHR-T2: invoiced amount $3,492.00 vs qty 18 × unit price $189.00 = **$3,402.00** (a $90.00 difference, far exceeding the $0.02 tolerance; appears to be a digit transposition). Subtotal ($7,568.80) is internally consistent with the stated line amounts and tax ($613.07 ≈ 0.081 × $7,568.80) passed, but the line-2 amount itself is wrong.

```json
{
  "invoice_id": "SOI-25-107",
  "po_number": "PO-2025-4125",
  "decision": "hold",
  "discrepancies": ["TOTAL_ERROR"],
  "explanation": "Line 2 (SO-CHR-T2) shows an amount of $3,492.00, but qty 18 x unit price $189.00 = $3,402.00 — a $90.00 overstatement far beyond the $0.02 tolerance, so TOTAL_ERROR applies. All other checks pass: prices and quantities match the PO and GRN-88324 received totals (26/18), currency is USD, tax of $613.07 equals 8.1% of $7,568.80, bank details match vendor master V07, and no duplicate payments were found."
}
```

**Recommendation:** Hold this invoice and request a corrected invoice from Stellar Office Interiors — the likely intended total is $7,478.80 subtotal / $8,057.88 total (or a corrected line-2 amount if the price/quantity intent differs).
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": ["TOTAL_ERROR"], "engine_codes": ["TOTAL_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: MF/25/107

**Step 1 — LLM call** (agent: `extractor`, 630+817 tok, 10.17s)
- assistant said:

```
{
  "invoice_no": "MF/25/107",
  "vendor_name": "Meridian Fasteners Inc.",
  "date": "2025-07-02",
  "po_number": "PO-2025-4126",
  "currency": "USD",
  "lines": [
    {
      "sku": "MF-ANC-10",
      "description": "Concrete anchors 10mm, box 100",
      "qty": 15,
      "unit_price": 62.75,
      "amount": 941.25
    },
    {
      "sku": "MF-M8-50",
      "description": "Hex bolts M8x50 zinc, box 500",
      "qty": 5,
      "unit_price": 44.00,
      "amount": 220.00
    },
    {
      "sku": "MF-W-8",
      "description": "Flat washers 8mm, box 1000",
      "qty": 39,
      "unit_price": 15.30,
      "amount": 596.70
    },
    {
      "sku": "MF-M8-NUT",
      "description": "Hex nuts M8 zinc, box 1000",
      "qty": 36,
      "unit_price": 27.60,
      "amount": 1021.60
    }
  ],
  "subtotal": 2779.55,
  "tax": 166.77,
  "total": 2946.32,
  "bank_name": "Keystone National",
  "bank_routing": "031000503",
  "bank_account": "5583920164",
  "payment_terms": "Net 30"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/107"}`

**Step 3 — LLM call** (agent: `matcher`, 1962+1254 tok, 38.15s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4126"})`
- agent called `get_received_totals({"po_number":"PO-2025-4126"})`
- agent called `get_vendor_by_name({"name":"Meridian Fasteners Inc."})`
- assistant said:

```
I'll run the three-way match for invoice MF/25/107 against PO-2025-4126. First, let me verify the PO, received quantities, and vendor resolution in parallel:
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4126", "vendor_id": "V03", "date": "2025-04-24", "currency": "USD", "lines": [{"line_no": 1, "sku": "MF-ANC-10", "description": "Concrete anchors 10mm, box 100", "qty": 15, "unit_price": 62.75}, {"line_no": 2, "sku": "MF-M8-50", "description": "Hex bolts M8x50 zinc, box 500", "qty": 5, "unit_price": 44.0}, {"line_no": 3, "sku": "MF-W-8", "description": "Flat washers 8mm, box 1000", "qty": 39, "unit_price": 15.3}, {"line_no": 4, "sku": "MF-M8-NUT", "description": "Hex nuts M8 zinc, box 1000", "qty": 36, "unit_price": 27.6}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 15, "2": 5, "3": 39, "4": 36}, "grn_count": 1, "grn_numbers": ["GRN-88325"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V03", "name": "Meridian Fasteners Inc.", "city": "Erie, PA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Keystone National", "bank_routing": "031000503", "bank_account": "5583920164", "tax_rate": 0.06}
```

**Step 7 — LLM call** (agent: `matcher`, 2443+366 tok, 9.68s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `arithmetic_check({"vendor_id":"V03"})`
- agent called `search_payments({"invoice_no":"MF/25/107","po_number":"PO-2025-4126","total":2946.32,"vendor_id":"V03"})`
- assistant said:

```
PO exists and matches, GRN-88325 covers all four lines, and the vendor resolves cleanly to V03. Bank details on the invoice (Keystone National, routing 031000503, account 5583920164) match the vendor master exactly — no BANK_CHANGE. Currency (USD) matches the PO. Now let me run the deterministic arithmetic verification and the duplicate screen:
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TOTAL_ERROR", "evidence": "Line MF-M8-NUT: amount 1021.60 != qty 36 x unit price 27.60 = 993.60."}], "checks_passed": ["Tax OK (166.77 ~= 166.77).", "Remit-to bank details match vendor master."]}
```

**Step 9 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 10 — LLM call** (agent: `matcher`, 2682+610 tok, 10.44s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. The arithmetic check flagged a line-extension error on the last line, while tax, bank details, and the duplicate screen all came back clean.

**Findings summary:**
- **PO exists** (PO-2025-4126, V03, USD — currency matches)
- **Prices**: all four line unit prices match the PO exactly ($62.75, $44.00, $15.30, $27.60)
- **Quantities**: billed qty (15 / 5 / 39 / 36) equals GRN-88325 received totals (15 / 5 / 39 / 36) — no overbilling
- **Arithmetic**: ❌ Line MF-M8-NUT: amount $1,021.60 ≠ 36 × $27.60 = $993.60 (a $28.00 overstatement, far beyond the $0.02 tolerance)
- **Tax**: $166.77 = 6% × $2,779.55 ✓
- **Bank**: Keystone National / 031000503 / 5583920164 matches vendor master ✓
- **Duplicates**: none found in payment history

```json
{
  "invoice_id": "MF/25/107",
  "po_number": "PO-2025-4126",
  "decision": "hold",
  "discrepancies": ["TOTAL_ERROR"],
  "explanation": "Line 4 (MF-M8-NUT) shows an amount of $1,021.60 but 36 boxes × $27.60 = $993.60, a $28.00 overstatement exceeding the $0.02 tolerance. All other checks pass: prices and quantities match PO-2025-4126 and GRN-88325 exactly, tax of $166.77 equals 6% of the subtotal, bank details match vendor master V03, and no duplicate payments were found. Hold pending a corrected invoice."
}
```
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["TOTAL_ERROR"], "engine_codes": ["TOTAL_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: HEC-2025-110

**Step 1 — LLM call** (agent: `extractor`, 469+572 tok, 3.35s)
- assistant said:

```
{
  "invoice_no": "HEC-2025-110",
  "vendor_name": "Helios Electrical Components",
  "date": "2025-06-28",
  "po_number": "PO-2025-4127",
  "currency": "USD",
  "lines": [
    {
      "sku": "HE-PSU-24",
      "description": "PSU 24V 10A DIN rail",
      "qty": 35,
      "unit_price": 96.30,
      "amount": 3370.50
    },
    {
      "sku": "HE-CAB-14",
      "description": "Copper cable 14AWG, 500ft spool",
      "qty": 12,
      "unit_price": 118.00,
      "amount": 1416.00
    }
  ],
  "subtotal": 4786.50,
  "tax": 411.64,
  "total": 5198.14,
  "bank_name": "Meridian Trust Bank",
  "bank_routing": "122100024",
  "bank_account": "7791024468",
  "payment_terms": "Net 45"
}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-110"}`

**Step 3 — LLM call** (agent: `matcher`, 1689+859 tok, 14.93s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4127"})`
- agent called `get_received_totals({"po_number":"PO-2025-4127"})`
- agent called `get_vendor_by_name({"name":"Helios Electrical Components"})`
- agent called `search_payments({"invoice_no":"HEC-2025-110","po_number":"PO-2025-4127","total":5198.14,"vendor_id":"V05"})`
- agent called `arithmetic_check({"vendor_id":"V05"})`
- assistant said:

```
I'll verify all checks using the tools. The vendor ID is V05 (from the PO), so I can run all independent checks in parallel.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4127", "vendor_id": "V05", "date": "2025-04-17", "currency": "USD", "lines": [{"line_no": 1, "sku": "HE-PSU-24", "description": "PSU 24V 10A DIN rail", "qty": 35, "unit_price": 96.3}, {"line_no": 2, "sku": "HE-CAB-14", "description": "Copper cable 14AWG, 500ft spool", "qty": 12, "unit_price": 118.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 35, "2": 12}, "grn_count": 1, "grn_numbers": ["GRN-88326"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V05", "name": "Helios Electrical Components", "city": "Tucson, AZ", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Desert West Bank", "bank_routing": "122100024", "bank_account": "3348812706", "tax_rate": 0.086}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "BANK_CHANGE", "evidence": "Remit-to account 7791024468 != vendor master 3348812706 \u2014 verify with vendor before payment."}], "checks_passed": ["Tax OK (411.64 ~= 411.64)."]}
```

**Step 9 — LLM call** (agent: `matcher`, 2194+876 tok, 18.3s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All tool checks are complete. Summary of findings:

- **PO existence:** PO-2025-4127 exists and matches (USD, vendor V05) ✓
- **Prices:** Line 1: $96.30 vs PO $96.30; Line 2: $118.00 vs PO $118.00 — exact match, no PRICE_MISMATCH ✓
- **Quantities:** Billed 35/35 (PSU) and 12/12 (cable) vs total received (GRN-88326: 35 and 12) — no QTY_MISMATCH ✓
- **GRN:** GRN-88326 exists — no GRN_MISSING ✓
- **Duplicates:** No payment history match on vendor + PO + total or invoice number ✓
- **Currency:** Invoice USD = PO USD ✓
- **Arithmetic/Tax:** arithmetic_check passed — tax $411.64 = 0.086 × $4,786.50; line amounts, subtotal $4,786.50, and total $5,198.14 all within tolerance ✓
- **Bank:** ❌ Invoice remit-to account **7791024468** (Meridian Trust Bank) differs from vendor master account **3348812706** (Desert West Bank), though the routing number 122100024 matches → **BANK_CHANGE**

```json
{
  "invoice_id": "HEC-2025-110",
  "po_number": "PO-2025-4127",
  "decision": "hold",
  "discrepancies": ["BANK_CHANGE"],
  "explanation": "All three-way match checks pass: quantities (35/35 and 12/12) match GRN-88326 receipts, prices ($96.30 and $118.00) match the PO exactly, and arithmetic/tax ($411.64 = 0.086 x $4,786.50; total $5,198.14) verify with no duplicates. However, the remit-to bank account 7791024468 (Meridian Trust Bank) differs from the vendor master account 3348812706 (Desert West Bank), triggering BANK_CHANGE; hold and verify the new bank details with the vendor before payment."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": ["BANK_CHANGE"], "engine_codes": ["BANK_CHANGE"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: GP-107

**Step 1 — LLM call** (agent: `extractor`, 457+224 tok, 5.18s)
- assistant said:

```
{
 "invoice_no": "GP-107",
 "vendor_name": "Granite Peak Safety Gear",
 "date": "2025-06-19",
 "po_number": "PO-2025-4128",
 "currency": "USD",
 "lines": [
  {"sku": "GP-HH-CL2", "description": "Hard hats class E, box 20", "qty": 6, "unit_price": 196.00, "amount": 1176.00},
  {"sku": "GP-BOOT-10", "description": "Steel toe boots size 10", "qty": 17, "unit_price": 112.00, "amount": 1904.00}
 ],
 "subtotal": 3080.00,
 "tax": 184.80,
 "total": 3264.80,
 "bank_name": "Meridian Trust Bank",
 "bank_routing": "123103729",
 "bank_account": "4456108823",
 "payment_terms": "Net 30"
}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1669+782 tok, 17.19s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4128"})`
- agent called `get_received_totals({"po_number":"PO-2025-4128"})`
- agent called `get_vendor_by_name({"name":"Granite Peak Safety Gear"})`
- agent called `arithmetic_check({"vendor_id":"V08"})`
- agent called `search_payments({"invoice_no":"GP-107","po_number":"PO-2025-4128","total":3264.8,"vendor_id":"V08"})`
- assistant said:

```
I'll verify all checks using the tools. All lookups are independent, so I'll run them together.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4128", "vendor_id": "V08", "date": "2025-05-04", "currency": "USD", "lines": [{"line_no": 1, "sku": "GP-HH-CL2", "description": "Hard hats class E, box 20", "qty": 6, "unit_price": 196.0}, {"line_no": 2, "sku": "GP-BOOT-10", "description": "Steel toe boots size 10", "qty": 17, "unit_price": 112.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 6, "2": 17}, "grn_count": 1, "grn_numbers": ["GRN-88327"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V08", "name": "Granite Peak Safety Gear", "city": "Boise, ID", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Sawtooth Community Bank", "bank_routing": "123103729", "bank_account": "2290156841", "tax_rate": 0.06}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "BANK_CHANGE", "evidence": "Remit-to account 4456108823 != vendor master 2290156841 \u2014 verify with vendor before payment."}], "checks_passed": ["Tax OK (184.80 ~= 184.80)."]}
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — LLM call** (agent: `matcher`, 2157+712 tok, 15.34s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the summary:

**Verification results:**
- **PO existence:** PO-2025-4128 exists, references vendor V08 (Granite Peak Safety Gear), currency USD ✓
- **Prices:** Line 1 at $196.00 and Line 2 at $112.00 exactly match PO unit prices (0% variance, within 0.5% tolerance) ✓
- **Quantities:** Billed 6 / received 6 (GRN-88327) and billed 17 / received 17 ✓; GRN exists ✓
- **Arithmetic:** Tax $184.80 = 6% × $3,080.00; line amounts, subtotal, and total all pass ✓
- **Currency:** USD vs USD ✓
- **Duplicates:** No matches in payment history ✓
- **Bank details:** ❌ Invoice remit-to account **4456108823** does not match vendor master account **2290156841** (routing 123103729 matches, but the account number differs) → **BANK_CHANGE**

```json
{
  "invoice_id": "GP-107",
  "po_number": "PO-2025-4128",
  "decision": "hold",
  "discrepancies": ["BANK_CHANGE"],
  "explanation": "Invoice GP-107 matches PO-2025-4128 on prices ($196.00 and $112.00), quantities (6/6 and 17/17 received per GRN-88327), currency (USD), and arithmetic (tax $184.80 = 6% of $3,080.00; total $3,264.80), and no duplicate payments were found. However, the remit-to bank account 4456108823 on the invoice differs from the vendor master account 2290156841 for V08 (routing 123103729 matches), triggering BANK_CHANGE. Hold payment until the bank account change is verified directly with the vendor."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": ["BANK_CHANGE"], "engine_codes": ["BANK_CHANGE"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: VPL-2025-107

**Step 1 — LLM call** (agent: `extractor`, 608+1113 tok, 20.34s)
- assistant said:

```
{
  "invoice_no": "VPL-2025-107",
  "vendor_name": "Vireo Print & Label GmbH",
  "date": "2025-06-22",
  "po_number": "PO-2025-4129",
  "currency": "USD",
  "lines": [
    {
      "sku": "VP-LBL-4x6",
      "description": "Thermal labels 4x6, roll 500",
      "qty": 39,
      "unit_price": 21.40,
      "amount": 834.60
    },
    {
      "sku": "VP-RIB-110",
      "description": "TTR ribbon 110mm",
      "qty": 38,
      "unit_price": 9.60,
      "amount": 364.80
    },
    {
      "sku": "VP-TAG-ASSET",
      "description": "Asset tags, custom, 1000",
      "qty": 35,
      "unit_price": 340.00,
      "amount": 11900.00
    }
  ],
  "subtotal": 13099.40,
  "tax": 2488.89,
  "total": 15588.29,
  "bank_name": "Hansa Handelsbank",
  "bank_routing": "DE44 5001 0517",
  "bank_account": "5407 3249 31",
  "payment_terms": "Net 60"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1892+694 tok, 16.37s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_vendor_by_name({"name":"Vireo Print & Label GmbH"})`
- agent called `get_po({"po_number":"PO-2025-4129"})`
- agent called `get_received_totals({"po_number":"PO-2025-4129"})`
- assistant said:

```
I'll verify this invoice against all the required checks. Let me start with the independent lookups: resolving the vendor name, confirming the PO, and checking received totals across all GRNs.
```

**Step 4 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V09", "name": "Vireo Print & Label GmbH", "city": "Hamburg, DE", "currency": "EUR", "payment_terms": "Net 60", "bank_name": "Hansa Handelsbank", "bank_routing": "DE44 5001 0517", "bank_account": "5407 3249 31", "tax_rate": 0.19, "memory": {"known_aliases": ["Vireo Print and Label"], "notes": "Always bills in EUR. Any USD invoice from this vendor is anomalous."}}
```

**Step 5 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4129", "vendor_id": "V09", "date": "2025-05-09", "currency": "EUR", "lines": [{"line_no": 1, "sku": "VP-LBL-4x6", "description": "Thermal labels 4x6, roll 500", "qty": 39, "unit_price": 21.4}, {"line_no": 2, "sku": "VP-RIB-110", "description": "TTR ribbon 110mm", "qty": 38, "unit_price": 9.6}, {"line_no": 3, "sku": "VP-TAG-ASSET", "description": "Asset tags, custom, 1000", "qty": 35, "unit_price": 340.0}], "status": "open"}
```

**Step 6 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 39, "2": 38, "3": 35}, "grn_count": 1, "grn_numbers": ["GRN-88328"]}
```

**Step 7 — LLM call** (agent: `matcher`, 2355+221 tok, 7.97s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"invoice_no":"VPL-2025-107","po_number":"PO-2025-4129","total":15588.29,"vendor_id":"V09"})`
- agent called `arithmetic_check({"vendor_id":"V09"})`
- assistant said:

```
Vendor resolves to V09, PO exists (EUR), and GRN-88328 confirms receipt of 39/38/35 units matching the billed quantities. Now let me run the duplicate screen and the deterministic arithmetic check — these are independent, so I'll run both together.
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (2488.89 ~= 2488.89).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2529+871 tok, 19.23s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the summary:

- **PO existence:** PO-2025-4129 found, all three SKUs match. ✅
- **Prices:** Invoice unit prices (21.40 / 9.60 / 340.00) exactly match PO unit prices — 0% variance, well within 0.5% tolerance. ✅
- **Quantities:** Billed 39/38/35 vs. GRN-88328 received 39/38/35 — no excess billing. ✅
- **Arithmetic:** Deterministic check passed — tax 2488.89 = 19% × 13099.40 (within $0.02), line amounts, subtotal, and total all tie out. ✅
- **Bank details:** Hansa Handelsbank / DE44 5001 0517 / 5407 3249 31 matches vendor master V09 exactly. ✅
- **Duplicates:** No payment history, no potential duplicates found. ✅
- **Currency:** Invoice is billed in **USD**, but PO-2025-4129 is in **EUR** (and vendor master confirms EUR; vendor notes flag any USD invoice as anomalous). ❌

```json
{
  "invoice_id": "VPL-2025-107",
  "po_number": "PO-2025-4129",
  "decision": "hold",
  "discrepancies": ["CURRENCY_MISMATCH"],
  "explanation": "Invoice is billed in USD (total 15,588.29) while PO-2025-4129, the vendor master record, and vendor history are all in EUR, triggering CURRENCY_MISMATCH. All other checks pass: line prices match PO exactly (21.40/9.60/340.00), billed qty 39/38/35 equals GRN-88328 received qty 39/38/35, arithmetic (tax 2,488.89 = 19% of 13,099.40 subtotal) verifies within tolerance, bank details match vendor master, and no duplicates were found. Hold for currency reconciliation before payment."
}
```
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["CURRENCY_MISMATCH"], "engine_codes": ["CURRENCY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: AMT-107

**Step 1 — LLM call** (agent: `extractor`, 565+316 tok, 2.38s)
- assistant said:

```
{"invoice_no": "AMT-107", "vendor_name": "Ashford Machine Tools Ltd.", "date": "2025-07-20", "po_number": "PO-2025-9911", "currency": "USD", "lines": [{"sku": "AM-CHK-125", "description": "Lathe chuck 125mm", "qty": 10, "unit_price": 412.60, "amount": 4126.00}, {"sku": "AM-END-12", "description": "End mill 12mm carbide", "qty": 21, "unit_price": 68.20, "amount": 1432.20}, {"sku": "AM-VIS-6", "description": "Machine vise 6in", "qty": 31, "unit_price": 289.00, "amount": 8959.00}, {"sku": "AM-INS-CNMG", "description": "Turning inserts CNMG, box 10", "qty": 22, "unit_price": 94.80, "amount": 2085.60}], "subtotal": 16602.80, "tax": 0.00, "total": 16602.80, "bank_name": "Pennine & Yorkshire Bank", "bank_routing": "GB29 NWBK 6016", "bank_account": "1331 9268 19", "payment_terms": "Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1521+834 tok, 17.59s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-9911"})`
- agent called `get_received_totals({"po_number":"PO-2025-9911"})`
- agent called `search_payments({"invoice_no":"AMT-107","po_number":"PO-2025-9911","total":16602.8,"vendor_id":"V10"})`
- agent called `arithmetic_check({"vendor_id":"V10"})`
- assistant said:

```
I'll verify all checks now: PO existence, received quantities, duplicate screening, and arithmetic. These are independent, so I'll call them together.
```

**Step 4 — tool `get_po` responded:**

```
{"error": "PO PO-2025-9911 not found"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-9911"}
```

**Step 6 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 8 — LLM call** (agent: `matcher`, 1731+675 tok, 27.55s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here are the results:

**Verification summary:**
- **PO existence:** `PO-2025-9911` does not exist in the PO system → **PO_NOT_FOUND**
- **GRNs:** No goods receipt notes exist for this PO → **GRN_MISSING** (consequently, billed vs. received quantities cannot be validated against any receipt)
- **Arithmetic:** Line math, subtotal ($16,602.80), tax ($0.00 at vendor master rate 0%), and total ($16,602.80) all pass within tolerance
- **Bank details:** Remit-to bank (Pennine & Yorkshire Bank, GB29 NWBK 6016 / 1331 9268 19) matches vendor master exactly → no BANK_CHANGE
- **Duplicates:** No payments found for this vendor + PO + total or invoice number AMT-107
- **Currency:** USD matches vendor master currency

```json
{
  "invoice_id": "AMT-107",
  "po_number": "PO-2025-9911",
  "decision": "hold",
  "discrepancies": ["PO_NOT_FOUND", "GRN_MISSING"],
  "explanation": "Referenced PO-2025-9911 does not exist in the PO system and no GRNs exist for it, so line prices and billed quantities (e.g., 10x chuck at $412.60, 31x vise at $289.00) cannot be matched to any PO or receipts. Invoice arithmetic is internally consistent (subtotal $16,602.80 + tax $0.00 = total $16,602.80), bank details match vendor master V10, and no duplicate payments were found; the invoice is held pending confirmation of the correct PO number."
}
```
```

**Step 9 — verifier**: `{"agree": false, "matcher_codes": ["GRN_MISSING", "PO_NOT_FOUND"], "engine_codes": ["PO_NOT_FOUND"], "matcher_decision": "hold", "engine_decision": "hold"}`

**Step 10 — LLM call** (agent: `matcher`, 1636+932 tok, 16.67s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-9911"})`
- agent called `get_vendor_by_name({"name":"Ashford Machine Tools Ltd."})`
- agent called `get_received_totals({"po_number":"PO-2025-9911"})`
- agent called `search_payments({"invoice_no":"AMT-107","po_number":"PO-2025-9911","total":16602.8,"vendor_id":"V10"})`
- agent called `arithmetic_check({"vendor_id":"V10"})`
- assistant said:

```
I'll re-verify all checks with the tools, paying attention to the engine's treatment of GRN_MISSING when the PO itself doesn't exist.
```

**Step 11 — tool `get_po` responded:**

```
{"error": "PO PO-2025-9911 not found"}
```

**Step 12 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V10", "name": "Ashford Machine Tools Ltd.", "city": "Sheffield, UK", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Pennine & Yorkshire Bank", "bank_routing": "GB29 NWBK 6016", "bank_account": "1331 9268 19", "tax_rate": 0.0}
```

**Step 13 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-9911"}
```

**Step 14 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 15 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 16 — LLM call** (agent: `matcher`, 1960+781 tok, 21.7s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks re-verified with the tools. Here's what I found:

- **PO lookup**: `PO PO-2025-9911 not found` → **PO_NOT_FOUND confirmed**. Because the PO doesn't exist, there are no PO lines to compare prices or billed quantities against, and the absence of GRNs is a direct consequence of the missing PO — so GRN_MISSING (like PRICE/QTY/CURRENCY mismatches) is subsumed by the root cause and should not be separately reported. I'm removing my earlier GRN_MISSING code per the engine's ruling.
- **Arithmetic**: `arithmetic_check` returned no findings — line amounts, subtotal ($16,602.80), tax ($0.00 vs 0.0% × $16,602.80), and total all pass.
- **Bank**: Remit-to details (Pennine & Yorkshire Bank, routing GB29 NWBK 6016, account 1331 9268 19) match vendor master V10 exactly — no BANK_CHANGE.
- **Duplicates**: `search_payments` for V10 / PO-2025-9911 / $16,602.80 / AMT-107 returned no potential duplicates — no DUPLICATE.
- **Vendor/currency**: Vendor V10 (USD, Net 30) matches the invoice's terms and USD currency.

Corrected final decision:

```json
{
  "invoice_id": "AMT-107",
  "po_number": "PO-2025-9911",
  "decision": "hold",
  "discrepancies": ["PO_NOT_FOUND"],
  "explanation": "Referenced PO PO-2025-9911 does not exist in the PO system, so PO_NOT_FOUND is the sole discrepancy; the missing GRN is a consequence of the nonexistent PO, not an independent code. All arithmetic passes (tax $0.00 = 0.0% × $16,602.80 subtotal, total $16,602.80), remit-to bank matches vendor master V10, and no duplicate payments exist — so the invoice is held pending a valid PO reference rather than rejected."
}
```
```

**Step 17 — verifier**: `{"agree": true, "matcher_codes": ["PO_NOT_FOUND"], "engine_codes": ["PO_NOT_FOUND"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: NIS-2025-110

**Step 1 — LLM call** (agent: `extractor`, 608+852 tok, 11.44s)
- assistant said:

```
{
  "invoice_no": "NIS-2025-110",
  "vendor_name": "Northgate Industrial Supply LLC",
  "date": "2025-06-15",
  "po_number": "PO-2025-4131",
  "currency": "USD",
  "lines": [
    {
      "sku": "NG-4410",
      "description": "Nitrile work gloves, box of 100",
      "qty": 10,
      "unit_price": 20.24,
      "amount": 202.40
    },
    {
      "sku": "NG-3305",
      "description": "Absorbent pads, case",
      "qty": 24,
      "unit_price": 42.50,
      "amount": 1020.00
    },
    {
      "sku": "NG-1180",
      "description": "Steel shelving unit 72in",
      "qty": 6,
      "unit_price": 149.00,
      "amount": 894.00
    },
    {
      "sku": "NG-7720",
      "description": "Safety goggles, anti-fog",
      "qty": 17,
      "unit_price": 6.95,
      "amount": 118.15
    }
  ],
  "subtotal": 2234.55,
  "tax": 162.00,
  "total": 2396.55,
  "bank_name": "First Commerce Bank",
  "bank_routing": "021000021",
  "bank_account": "4402198837",
  "payment_terms": "Net 60"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-110"}`

**Step 3 — LLM call** (agent: `matcher`, 2087+1177 tok, 25.23s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4131"})`
- agent called `get_received_totals({"po_number":"PO-2025-4131"})`
- agent called `arithmetic_check({"vendor_id":"V01"})`
- agent called `search_payments({"invoice_no":"NIS-2025-110","po_number":"PO-2025-4131","total":2396.55,"vendor_id":"V01"})`
- assistant said:

```
I'll verify this invoice against the PO, GRN totals, vendor master, and payment history using the tools.
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4131", "vendor_id": "V01", "date": "2025-05-10", "currency": "USD", "lines": [{"line_no": 1, "sku": "NG-4410", "description": "Nitrile work gloves, box of 100", "qty": 10, "unit_price": 18.4}, {"line_no": 2, "sku": "NG-3305", "description": "Absorbent pads, case", "qty": 24, "unit_price": 42.5}, {"line_no": 3, "sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 6, "unit_price": 149.0}, {"line_no": 4, "sku": "NG-7720", "description": "Safety goggles, anti-fog", "qty": 17, "unit_price": 6.95}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 5, "2": 12, "3": 3, "4": 8}, "grn_count": 1, "grn_numbers": ["GRN-88330"]}
```

**Step 6 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (162.00 ~= 162.00).", "Remit-to bank details match vendor master."]}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — LLM call** (agent: `matcher`, 2539+1043 tok, 22.97s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the summary of findings:

- **PO existence:** PO-2025-4131 found, USD, matches invoice currency ✓
- **Prices:** Line 1 (NG-4410) invoiced at $20.24 vs PO price $18.40 — a +$1.84 (10%) deviation, far beyond the 0.5% tolerance → PRICE_MISMATCH. Lines 2–4 match PO prices exactly.
- **Quantities:** Received totals across all GRNs (GRN-88330 only): line 1: 5, line 2: 12, line 3: 3, line 4: 8. Invoice bills 10/24/6/17 — every line's billed qty exceeds received qty → QTY_MISMATCH (partial delivery noted as common for this vendor, but billed exceeds the sum received regardless).
- **Arithmetic:** Tool confirms tax ($162.00 ≈ 7.25% × subtotal), line amounts, subtotal, and total all pass — no TOTAL_ERROR.
- **Duplicates:** No prior payment matches vendor + PO + total or invoice number.
- **Bank:** Remit-to details match vendor master exactly.

```json
{
  "invoice_id": "NIS-2025-110",
  "po_number": "PO-2025-4131",
  "decision": "hold",
  "discrepancies": ["PRICE_MISMATCH", "QTY_MISMATCH"],
  "explanation": "Line 1 (NG-4410) is billed at $20.24/unit vs the PO price of $18.40, a +10% price deviation exceeding the 0.5% tolerance. Additionally, all four lines are billed above total received quantities per GRN-88330 (billed/received: 10/5, 24/12, 6/3, 17/8), so no line can be fully receipted. Arithmetic, tax ($162.00 at 7.25%), currency (USD), remit-to bank details, and duplicate screening all passed."
}
```
```

**Step 9 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH", "QTY_MISMATCH"], "engine_codes": ["PRICE_MISMATCH", "QTY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: CCW-107

**Step 1 — LLM call** (agent: `extractor`, 592+580 tok, 7.23s)
- assistant said:

```
{
  "invoice_no": "CCW-107",
  "vendor_name": "Cascadia Chemical Works",
  "date": "2025-06-04",
  "po_number": "PO-2025-4132",
  "currency": "USD",
  "lines": [
    {
      "sku": "CC-COOL-55",
      "description": "Machine coolant concentrate, 55gal",
      "qty": 37,
      "unit_price": 744.50,
      "amount": 27546.50
    },
    {
      "sku": "CC-DEG-5",
      "description": "Industrial degreaser, 5gal",
      "qty": 21,
      "unit_price": 87.40,
      "amount": 1835.40
    },
    {
      "sku": "CC-IPA-55",
      "description": "Isopropyl alcohol 99%, 55gal drum",
      "qty": 8,
      "unit_price": 612.00,
      "amount": 4896.00
    }
  ],
  "subtotal": 34277.90,
  "tax": 3300.50,
  "total": 37578.40,
  "bank_name": "Meridian Trust Bank",
  "bank_routing": "125000024",
  "bank_account": "6120087745",
  "payment_terms": "Net 60"
}

```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1900+755 tok, 12.8s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number":"PO-2025-4132"})`
- agent called `get_received_totals({"po_number":"PO-2025-4132"})`
- agent called `get_vendor_by_name({"name":"Cascadia Chemical Works"})`
- agent called `arithmetic_check({"vendor_id":"V04"})`
- agent called `search_payments({"invoice_no":"CCW-107","po_number":"PO-2025-4132","total":37578.4,"vendor_id":"V04"})`
- assistant said:

```
I'll verify all checks using the tools. The vendor ID (V04) and invoice total are known from the scoped context, so all calls are independent:
```

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4132", "vendor_id": "V04", "date": "2025-04-09", "currency": "USD", "lines": [{"line_no": 1, "sku": "CC-COOL-55", "description": "Machine coolant concentrate, 55gal", "qty": 37, "unit_price": 744.5}, {"line_no": 2, "sku": "CC-DEG-5", "description": "Industrial degreaser, 5gal", "qty": 21, "unit_price": 87.4}, {"line_no": 3, "sku": "CC-IPA-55", "description": "Isopropyl alcohol 99%, 55gal drum", "qty": 8, "unit_price": 612.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 37, "2": 21, "3": 8}, "grn_count": 1, "grn_numbers": ["GRN-88331"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V04", "name": "Cascadia Chemical Works", "city": "Tacoma, WA", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Puget Sound Trust", "bank_routing": "125000024", "bank_account": "9027481133", "tax_rate": 0.095}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TAX_ERROR", "evidence": "Tax 3300.50 != tax_rate 0.0950 x subtotal 34277.90 = 3256.40 (tolerance $0.02)."}, {"code": "BANK_CHANGE", "evidence": "Remit-to account 6120087745 != vendor master 9027481133 \u2014 verify with vendor before payment."}], "checks_passed": []}
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — LLM call** (agent: `matcher`, 2496+788 tok, 13.64s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
All checks are complete. Here's the summary:

**Check results:**
- **PO existence:** PO-2025-4132 exists for V04, status open ✓
- **Prices:** All three line unit prices (744.50 / 87.40 / 612.00) match PO exactly ✓
- **Quantities:** Billed 37/21/8 vs received 37/21/8 across GRN-88331 ✓ (GRN exists, no QTY mismatch)
- **Currency:** USD = USD ✓
- **Duplicates:** No matches in payment history ✓
- **Arithmetic:** Lines and subtotal/total are internally consistent, but **tax is wrong**: 3,300.50 vs expected 0.095 × 34,277.90 = 3,256.40 → off by $44.10 (TAX_ERROR)
- **Bank details:** Routing matches (125000024) but **account number differs**: invoice 6120087745 vs vendor master 9027481133 (BANK_CHANGE)

```json
{
  "invoice_id": "CCW-107",
  "po_number": "PO-2025-4132",
  "decision": "hold",
  "discrepancies": ["TAX_ERROR", "BANK_CHANGE"],
  "explanation": "Prices (744.50/87.40/612.00), quantities (37/21/8 billed vs 37/21/8 received on GRN-88331), and currency all match, and no duplicate payment exists, but tax of 3,300.50 exceeds the master-rate expectation of 3,256.40 (0.095 × 34,277.90) by $44.10 (TAX_ERROR), and the remit-to account 6120087745 differs from the vendor master 9027481133 (BANK_CHANGE). Hold pending corrected tax and vendor-verified bank details."
}
```
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": ["BANK_CHANGE", "TAX_ERROR"], "engine_codes": ["BANK_CHANGE", "TAX_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`
