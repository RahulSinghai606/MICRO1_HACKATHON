# Agent trajectories — run `agent_final_stress`


## Case: NIS-2025-401

**Step 1 — LLM call** (agent: `extractor`, 540+244 tok, 4.4s)
- assistant said:

```
{"invoice_no":"NIS-2025-401","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-28","po_number":"PO-2025-4101","currency":"USD","lines":[{"sku":"NG-3305","description":"Absorbent pads, case","qty":38,"unit_price":42.50,"amount":1615.00},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":25,"unit_price":149.00,"amount":3725.00},{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":37,"unit_price":18.40,"amount":680.80},{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":29,"unit_price":6.95,"amount":201.55}],"subtotal":6222.35,"tax":451.12,"total":6673.47,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-401"}`

**Step 3 — LLM call** (agent: `matcher`, 1901+84 tok, 2.57s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4101"})`
- agent called `get_received_totals({"po_number": "PO-2025-4101"})`
- agent called `get_vendor_by_name({"name": "Northgate Industrial Supply LLC"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4101", "vendor_id": "V01", "date": "2025-05-06", "currency": "USD", "lines": [{"line_no": 1, "sku": "NG-3305", "description": "Absorbent pads, case", "qty": 38, "unit_price": 42.5}, {"line_no": 2, "sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 25, "unit_price": 149.0}, {"line_no": 3, "sku": "NG-4410", "description": "Nitrile work gloves, box of 100", "qty": 37, "unit_price": 18.4}, {"line_no": 4, "sku": "NG-7720", "description": "Safety goggles, anti-fog", "qty": 29, "unit_price": 6.95}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 38, "2": 25, "3": 37, "4": 29}, "grn_count": 1, "grn_numbers": ["GRN-88301"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V01", "name": "Northgate Industrial Supply LLC", "city": "Columbus, OH", "currency": "USD", "payment_terms": "Net 30", "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "tax_rate": 0.0725, "memory": {"known_aliases": ["Northgate Ind. Supply (a div. of NIS Holdings)", "NIS Holdings LLC", "Northgate Industrial"], "notes": "Invoices under NIS Holdings trade names since 2024 reorg. Split deliveries common."}}
```

**Step 7 — LLM call** (agent: `matcher`, 2407+83 tok, 2.33s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V01", "po_number": "PO-2025-4101", "total": 6673.47, "invoice_no": "NIS-2025-401"})`
- agent called `arithmetic_check({"vendor_id": "V01"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (451.12 ~= 451.12).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2549+178 tok, 3.75s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"NIS-2025-401","po_number":"PO-2025-4101","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4101 exists for vendor V01 in USD, and all invoice line unit prices match the PO exactly: NG-3305 at 42.50, NG-1180 at 149.00, NG-4410 at 18.40, and NG-7720 at 6.95. GRN totals on GRN-88301 fully cover the billed quantities (38, 25, 37, and 29 respectively), arithmetic checks passed including tax 451.12 on subtotal 6222.35 and total 6673.47, bank details match the vendor master, and no duplicate payment or invoice number was found."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: INV-2025-0401

**Step 1 — LLM call** (agent: `extractor`, 441+175 tok, 3.48s)
- assistant said:

```
{"invoice_no":"INV-2025-0401","vendor_name":"Bluefin Packaging Co.","date":"2025-07-05","po_number":"PO-2025-4102","currency":"USD","lines":[{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":11,"unit_price":31.25,"amount":343.75},{"sku":"BP-115","description":"Stretch wrap roll 80ga","qty":8,"unit_price":12.80,"amount":102.40}],"subtotal":446.15,"tax":31.23,"total":477.38,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0401"}`

**Step 3 — LLM call** (agent: `matcher`, 1615+84 tok, 3.24s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4102"})`
- agent called `get_received_totals({"po_number": "PO-2025-4102"})`
- agent called `get_vendor_by_name({"name": "Bluefin Packaging Co."})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4102", "vendor_id": "V02", "date": "2025-04-17", "currency": "USD", "lines": [{"line_no": 1, "sku": "BP-201", "description": "Corrugated boxes 18x12x10, bundle 25", "qty": 11, "unit_price": 31.25}, {"line_no": 2, "sku": "BP-115", "description": "Stretch wrap roll 80ga", "qty": 8, "unit_price": 12.8}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 11, "2": 8}, "grn_count": 1, "grn_numbers": ["GRN-88302"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V02", "name": "Bluefin Packaging Co.", "city": "Savannah, GA", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Coastal Georgia Bank", "bank_routing": "061000104", "bank_account": "7719045512", "tax_rate": 0.07, "memory": {"known_aliases": ["Bluefin Packaging Company"], "notes": "Re-issued invoices previously arrived with reformatted numbers (INV-25-xxx vs INV-2025-0xxx)."}}
```

**Step 7 — LLM call** (agent: `matcher`, 2011+82 tok, 2.77s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V02", "po_number": "PO-2025-4102", "total": 477.38, "invoice_no": "INV-2025-0401"})`
- agent called `arithmetic_check({"vendor_id": "V02"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (31.23 ~= 31.23).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2152+160 tok, 3.71s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "INV-2025-0401",
  "po_number": "PO-2025-4102",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4102 exists for vendor V02 in USD, and the invoice matches the PO line prices exactly: BP-201 at 31.25 for qty 11 and BP-115 at 12.80 for qty 8. GRN GRN-88302 shows receipts of 11 and 8 respectively, arithmetic checks passed including subtotal/tax/total (tax 31.23 at 7%), bank details match the vendor master, and no duplicate payment or invoice number was found."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: MF/25/401

**Step 1 — LLM call** (agent: `extractor`, 516+218 tok, 4.01s)
- assistant said:

```
{"invoice_no":"MF/25/401","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-06-02","po_number":"PO-2025-4103","currency":"USD","lines":[{"sku":"MF-W-8","description":"Flat washers 8mm, box 1000","qty":26,"unit_price":15.30,"amount":397.80},{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":6,"unit_price":62.75,"amount":376.50},{"sku":"MF-M8-50","description":"Hex bolts M8x50 zinc, box 500","qty":5,"unit_price":44.00,"amount":220.00}],"subtotal":994.30,"tax":59.66,"total":1053.96,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/401"}`

**Step 3 — LLM call** (agent: `matcher`, 1646+87 tok, 2.52s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4103"})`
- agent called `get_vendor_by_name({"name": "MERIDIAN FASTENERS INC."})`
- agent called `get_received_totals({"po_number": "PO-2025-4103"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4103", "vendor_id": "V03", "date": "2025-06-02", "currency": "USD", "lines": [{"line_no": 1, "sku": "MF-W-8", "description": "Flat washers 8mm, box 1000", "qty": 26, "unit_price": 15.3}, {"line_no": 2, "sku": "MF-ANC-10", "description": "Concrete anchors 10mm, box 100", "qty": 6, "unit_price": 62.75}, {"line_no": 3, "sku": "MF-M8-50", "description": "Hex bolts M8x50 zinc, box 500", "qty": 5, "unit_price": 44.0}], "status": "open"}
```

**Step 5 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V03", "name": "Meridian Fasteners Inc.", "city": "Erie, PA", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Keystone National", "bank_routing": "031000503", "bank_account": "5583920164", "tax_rate": 0.06}
```

**Step 6 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 26, "2": 6, "3": 5}, "grn_count": 1, "grn_numbers": ["GRN-88303"]}
```

**Step 7 — LLM call** (agent: `matcher`, 2058+81 tok, 3.12s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V03", "po_number": "PO-2025-4103", "total": 1053.96, "invoice_no": "MF/25/401"})`
- agent called `arithmetic_check({"vendor_id": "V03"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (59.66 ~= 59.66).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2198+160 tok, 3.74s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"MF/25/401","po_number":"PO-2025-4103","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4103 exists for vendor V03, invoice currency USD matches the PO, unit prices match the PO exactly (15.30, 62.75, and 44.00), and billed quantities 26/6/5 do not exceed received quantities on GRN-88303 totaling 26/6/5. Arithmetic check passed: subtotal 994.30, tax 59.66 at 6%, and total 1,053.96 are within tolerance; remit-to bank details match the vendor master, and no duplicate payment or invoice number was found."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: CCW-401

**Step 1 — LLM call** (agent: `extractor`, 483+178 tok, 3.33s)
- assistant said:

```
{"invoice_no":"CCW-401","vendor_name":"Cascadia Chemical Works","date":"2025-06-04","po_number":"PO-2025-4104","currency":"USD","lines":[{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":6,"unit_price":87.40,"amount":524.40},{"sku":"CC-COOL-55","description":"Machine coolant concentrate, 55gal","qty":35,"unit_price":744.50,"amount":26057.50}],"subtotal":26581.90,"tax":2525.28,"total":29107.18,"bank_name":"Puget Sound Trust","bank_routing":"125000024","bank_account":"9027481133","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-401"}`

**Step 3 — LLM call** (agent: `matcher`, 1568+84 tok, 2.48s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4104"})`
- agent called `get_received_totals({"po_number": "PO-2025-4104"})`
- agent called `get_vendor_by_name({"name": "Cascadia Chemical Works"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4104", "vendor_id": "V04", "date": "2025-06-04", "currency": "USD", "lines": [{"line_no": 1, "sku": "CC-DEG-5", "description": "Industrial degreaser, 5gal", "qty": 6, "unit_price": 87.4}, {"line_no": 2, "sku": "CC-COOL-55", "description": "Machine coolant concentrate, 55gal", "qty": 35, "unit_price": 744.5}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 6, "2": 35}, "grn_count": 1, "grn_numbers": ["GRN-88304"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V04", "name": "Cascadia Chemical Works", "city": "Tacoma, WA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Puget Sound Trust", "bank_routing": "125000024", "bank_account": "9027481133", "tax_rate": 0.095}
```

**Step 7 — LLM call** (agent: `matcher`, 1922+80 tok, 2.68s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V04", "po_number": "PO-2025-4104", "total": 29107.18, "invoice_no": "CCW-401"})`
- agent called `arithmetic_check({"vendor_id": "V04"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (2525.28 ~= 2525.28).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2063+170 tok, 4.01s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"CCW-401","po_number":"PO-2025-4104","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4104 exists for vendor V04 in USD, and the invoice matches the PO line prices exactly: CC-DEG-5 at 87.40 for qty 6 and CC-COOL-55 at 744.50 for qty 35. GRN totals show 6 units received on line 1 and 35 on line 2 (GRN-88304), arithmetic passed including subtotal 26581.90, tax 2525.28 at 9.5%, and total 29107.18, bank details match the vendor master, and no duplicate payment or prior invoice number match was found."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: HEC-2025-401

**Step 1 — LLM call** (agent: `extractor`, 517+256 tok, 3.6s)
- assistant said:

```
{"invoice_no":"HEC-2025-401","vendor_name":"Helios Electrical Components","date":"2025-07-02","po_number":"PO-2025-4105","currency":"USD","lines":[{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":35,"unit_price":96.30,"amount":3370.50},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":30,"unit_price":118.00,"amount":3540.00},{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":12,"unit_price":14.20,"amount":170.40},{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":10,"unit_price":9.85,"amount":98.50}],"subtotal":7179.40,"tax":617.43,"total":7796.83,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-401"}`

**Step 3 — LLM call** (agent: `matcher`, 1790+83 tok, 2.74s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4105"})`
- agent called `get_received_totals({"po_number": "PO-2025-4105"})`
- agent called `get_vendor_by_name({"name": "Helios Electrical Components"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4105", "vendor_id": "V05", "date": "2025-04-25", "currency": "USD", "lines": [{"line_no": 1, "sku": "HE-PSU-24", "description": "PSU 24V 10A DIN rail", "qty": 35, "unit_price": 96.3}, {"line_no": 2, "sku": "HE-CAB-14", "description": "Copper cable 14AWG, 500ft spool", "qty": 30, "unit_price": 118.0}, {"line_no": 3, "sku": "HE-REL-24", "description": "Relay 24VDC 8-pin", "qty": 12, "unit_price": 14.2}, {"line_no": 4, "sku": "HE-CB-20", "description": "Circuit breaker 20A DIN", "qty": 10, "unit_price": 9.85}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 35, "2": 30, "3": 12, "4": 10}, "grn_count": 1, "grn_numbers": ["GRN-88305"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V05", "name": "Helios Electrical Components", "city": "Tucson, AZ", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Desert West Bank", "bank_routing": "122100024", "bank_account": "3348812706", "tax_rate": 0.086}
```

**Step 7 — LLM call** (agent: `matcher`, 2249+83 tok, 2.74s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V05", "po_number": "PO-2025-4105", "total": 7796.83, "invoice_no": "HEC-2025-401"})`
- agent called `arithmetic_check({"vendor_id": "V05"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (617.43 ~= 617.43).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2391+198 tok, 4.87s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "HEC-2025-401",
  "po_number": "PO-2025-4105",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4105 exists for vendor V05 in USD, and all invoice line prices match the PO exactly: HE-PSU-24 at 96.30, HE-CAB-14 at 118.00, HE-REL-24 at 14.20, and HE-CB-20 at 9.85. GRN GRN-88305 shows full receipt of all billed quantities (35, 30, 12, and 10 respectively), arithmetic_check found no tax/total errors and confirmed tax 617.43 at the 8.6% vendor tax rate, the remit-to bank details match the vendor master, and no duplicate payment was found."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: ALS-INV-401

**Step 1 — LLM call** (agent: `extractor`, 525+230 tok, 4.84s)
- assistant said:

```
{"invoice_no":"ALS-INV-401","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-02","po_number":"PO-2025-4106","currency":"USD","lines":[{"sku":"AL-LIFT","description":"Liftgate service","qty":37,"unit_price":45.00,"amount":1665.00},{"sku":"AL-FUEL","description":"Fuel surcharge","qty":9,"unit_price":63.75,"amount":573.75},{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":21,"unit_price":425.00,"amount":8925.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":33,"unit_price":18.50,"amount":610.50}],"subtotal":11774.25,"tax":0.00,"total":11774.25,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-401"}`

**Step 3 — LLM call** (agent: `matcher`, 1799+85 tok, 3.05s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4106"})`
- agent called `get_received_totals({"po_number": "PO-2025-4106"})`
- agent called `get_vendor_by_name({"name": "AURIGA LOGISTICS SERVICES"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4106", "vendor_id": "V06", "date": "2025-06-12", "currency": "USD", "lines": [{"line_no": 1, "sku": "AL-LIFT", "description": "Liftgate service", "qty": 37, "unit_price": 45.0}, {"line_no": 2, "sku": "AL-FUEL", "description": "Fuel surcharge", "qty": 9, "unit_price": 63.75}, {"line_no": 3, "sku": "AL-LTL-STD", "description": "LTL freight, standard lane", "qty": 21, "unit_price": 425.0}, {"line_no": 4, "sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 33, "unit_price": 18.5}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 37, "2": 9, "3": 21, "4": 33}, "grn_count": 1, "grn_numbers": ["GRN-88306"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V06", "name": "Auriga Logistics Services", "city": "Memphis, TN", "currency": "USD", "payment_terms": "Net 45", "bank_name": "River City Bank", "bank_routing": "084000026", "bank_account": "6650371928", "tax_rate": 0.0}
```

**Step 7 — LLM call** (agent: `matcher`, 2233+81 tok, 2.82s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V06", "po_number": "PO-2025-4106", "total": 11774.25, "invoice_no": "ALS-INV-401"})`
- agent called `arithmetic_check({"vendor_id": "V06"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2373+200 tok, 4.6s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"ALS-INV-401","po_number":"PO-2025-4106","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4106 exists for vendor V06 in USD, and all invoice line prices match the PO exactly: AL-LIFT 37 @ 45.00, AL-FUEL 9 @ 63.75, AL-LTL-STD 21 @ 425.00, and AL-WHS-P 33 @ 18.50. GRN totals from GRN-88306 fully support the billed quantities (37, 9, 21, and 33 respectively), arithmetic checks passed including subtotal 11,774.25, tax 0.00 at 0.0% tax rate, and total 11,774.25, the remit-to bank details match the vendor master, and no duplicate payment was found for invoice ALS-INV-401."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: SOI-25-401

**Step 1 — LLM call** (agent: `extractor`, 505+206 tok, 4.6s)
- assistant said:

```
{"invoice_no":"SOI-25-401","vendor_name":"Stellar Office Interiors","date":"2025-06-19","po_number":"PO-2025-4107","currency":"USD","lines":[{"sku":"SO-FIL-3D","description":"File cabinet 3-drawer","qty":24,"unit_price":156.80,"amount":3763.20},{"sku":"SO-MON-ARM","description":"Dual monitor arm","qty":10,"unit_price":74.25,"amount":742.50},{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":7,"unit_price":189.00,"amount":1323.00}],"subtotal":5828.70,"tax":472.12,"total":6300.82,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-401"}`

**Step 3 — LLM call** (agent: `matcher`, 1688+83 tok, 2.6s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4107"})`
- agent called `get_received_totals({"po_number": "PO-2025-4107"})`
- agent called `get_vendor_by_name({"name": "Stellar Office Interiors"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4107", "vendor_id": "V07", "date": "2025-06-24", "currency": "USD", "lines": [{"line_no": 1, "sku": "SO-FIL-3D", "description": "File cabinet 3-drawer", "qty": 24, "unit_price": 156.8}, {"line_no": 2, "sku": "SO-MON-ARM", "description": "Dual monitor arm", "qty": 10, "unit_price": 74.25}, {"line_no": 3, "sku": "SO-CHR-T2", "description": "Task chair, mesh back", "qty": 7, "unit_price": 189.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 24, "2": 10, "3": 7}, "grn_count": 1, "grn_numbers": ["GRN-88307"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V07", "name": "Stellar Office Interiors", "city": "Denver, CO", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Front Range Credit Union", "bank_routing": "107000233", "bank_account": "8812204575", "tax_rate": 0.081}
```

**Step 7 — LLM call** (agent: `matcher`, 2081+82 tok, 2.64s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V07", "po_number": "PO-2025-4107", "total": 6300.82, "invoice_no": "SOI-25-401"})`
- agent called `arithmetic_check({"vendor_id": "V07"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (472.12 ~= 472.12).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2222+168 tok, 4.09s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"SOI-25-401","po_number":"PO-2025-4107","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4107 exists for vendor V07 in USD, and the invoice line prices match the PO exactly: SO-FIL-3D 156.80, SO-MON-ARM 74.25, and SO-CHR-T2 189.00. GRN totals show full receipt against all PO lines (24, 10, and 7 respectively via GRN-88307), arithmetic check passed including tax 472.12 at the 8.1% vendor tax rate and total 6300.82, bank details match vendor master, and no duplicate payment or invoice number was found."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: GP-401

**Step 1 — LLM call** (agent: `extractor`, 480+214 tok, 3.52s)
- assistant said:

```
{"invoice_no":"GP-401","vendor_name":"Granite Peak Safety Gear","date":"2025-06-26","po_number":"PO-2025-4108","currency":"USD","lines":[{"sku":"GP-HH-CL2","description":"Hard hats class E, box 20","qty":30,"unit_price":196.00,"amount":5880.00},{"sku":"GP-BOOT-10","description":"Steel toe boots size 10","qty":39,"unit_price":112.00,"amount":4368.00},{"sku":"GP-VIS-XL","description":"Hi-vis vests XL, pack 10","qty":4,"unit_price":84.50,"amount":338.00}],"subtotal":10586.00,"tax":635.16,"total":11221.16,"bank_name":"Sawtooth Community Bank","bank_routing":"123103729","bank_account":"2290156841","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-401"}`

**Step 3 — LLM call** (agent: `matcher`, 1641+84 tok, 3.15s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4108"})`
- agent called `get_received_totals({"po_number": "PO-2025-4108"})`
- agent called `get_vendor_by_name({"name": "Granite Peak Safety Gear"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4108", "vendor_id": "V08", "date": "2025-04-01", "currency": "USD", "lines": [{"line_no": 1, "sku": "GP-HH-CL2", "description": "Hard hats class E, box 20", "qty": 30, "unit_price": 196.0}, {"line_no": 2, "sku": "GP-BOOT-10", "description": "Steel toe boots size 10", "qty": 39, "unit_price": 112.0}, {"line_no": 3, "sku": "GP-VIS-XL", "description": "Hi-vis vests XL, pack 10", "qty": 4, "unit_price": 84.5}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 30, "2": 39, "3": 4}, "grn_count": 1, "grn_numbers": ["GRN-88308"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V08", "name": "Granite Peak Safety Gear", "city": "Boise, ID", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Sawtooth Community Bank", "bank_routing": "123103729", "bank_account": "2290156841", "tax_rate": 0.06}
```

**Step 7 — LLM call** (agent: `matcher`, 2047+79 tok, 2.88s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V08", "po_number": "PO-2025-4108", "total": 11221.16, "invoice_no": "GP-401"})`
- agent called `arithmetic_check({"vendor_id": "V08"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (635.16 ~= 635.16).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2185+171 tok, 3.82s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "GP-401",
  "po_number": "PO-2025-4108",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4108 exists for vendor V08 in USD, and all invoice line prices match the PO exactly: GP-HH-CL2 at 196.00, GP-BOOT-10 at 112.00, and GP-VIS-XL at 84.50. GRN totals show full receipt of the billed quantities (30, 39, and 4 respectively via GRN-88308), arithmetic checks passed including tax 635.16 at the 6% vendor tax rate, bank details match the vendor master, and no duplicate payment was found."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: VPL-2025-401

**Step 1 — LLM call** (agent: `extractor`, 501+192 tok, 3.83s)
- assistant said:

```
{"invoice_no":"VPL-2025-401","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-07-09","po_number":"PO-2025-4109","currency":"EUR","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":23,"unit_price":21.40,"amount":492.20},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":9,"unit_price":9.60,"amount":86.40}],"subtotal":578.60,"tax":109.93,"total":688.53,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-401"}`

**Step 3 — LLM call** (agent: `matcher`, 1577+88 tok, 2.63s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4109"})`
- agent called `get_received_totals({"po_number": "PO-2025-4109"})`
- agent called `get_vendor_by_name({"name": "VIREO PRINT & LABEL GMBH"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4109", "vendor_id": "V09", "date": "2025-06-18", "currency": "EUR", "lines": [{"line_no": 1, "sku": "VP-LBL-4x6", "description": "Thermal labels 4x6, roll 500", "qty": 23, "unit_price": 21.4}, {"line_no": 2, "sku": "VP-RIB-110", "description": "TTR ribbon 110mm", "qty": 9, "unit_price": 9.6}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 23, "2": 9}, "grn_count": 1, "grn_numbers": ["GRN-88309"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V09", "name": "Vireo Print & Label GmbH", "city": "Hamburg, DE", "currency": "EUR", "payment_terms": "Net 30", "bank_name": "Hansa Handelsbank", "bank_routing": "DE44 5001 0517", "bank_account": "5407 3249 31", "tax_rate": 0.19, "memory": {"known_aliases": ["Vireo Print and Label"], "notes": "Always bills in EUR. Any USD invoice from this vendor is anomalous."}}
```

**Step 7 — LLM call** (agent: `matcher`, 1984+82 tok, 2.68s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V09", "po_number": "PO-2025-4109", "total": 688.53, "invoice_no": "VPL-2025-401"})`
- agent called `arithmetic_check({"vendor_id": "V09"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (109.93 ~= 109.93).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2125+178 tok, 3.85s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "VPL-2025-401",
  "po_number": "PO-2025-4109",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4109 exists for vendor V09 in EUR, and the invoice line prices match the PO exactly: VP-LBL-4x6 at 21.4 and VP-RIB-110 at 9.6. GRN GRN-88309 shows receipts of 23 and 9 respectively, matching the billed quantities, arithmetic_check found no tax/total errors and confirmed tax 109.93 at the 19% rate, bank details match the vendor master, and payment history shows no duplicate for invoice VPL-2025-401 or total 688.53."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: AMT-401

**Step 1 — LLM call** (agent: `extractor`, 548+252 tok, 3.49s)
- assistant said:

```
{"invoice_no":"AMT-401","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-09","po_number":"PO-2025-4110","currency":"USD","lines":[{"sku":"AM-INS-CNMG","description":"Turning inserts CNMG, box 10","qty":4,"unit_price":94.80,"amount":379.20},{"sku":"AM-VIS-6","description":"Machine vise 6in","qty":7,"unit_price":289.00,"amount":2023.00},{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":15,"unit_price":412.60,"amount":6189.00},{"sku":"AM-END-12","description":"End mill 12mm carbide","qty":27,"unit_price":68.20,"amount":1841.40}],"subtotal":10432.60,"tax":0.00,"total":10432.60,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-401"}`

**Step 3 — LLM call** (agent: `matcher`, 1782+85 tok, 2.81s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4110"})`
- agent called `get_received_totals({"po_number": "PO-2025-4110"})`
- agent called `get_vendor_by_name({"name": "Ashford Machine Tools Ltd."})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4110", "vendor_id": "V10", "date": "2025-04-22", "currency": "USD", "lines": [{"line_no": 1, "sku": "AM-INS-CNMG", "description": "Turning inserts CNMG, box 10", "qty": 4, "unit_price": 94.8}, {"line_no": 2, "sku": "AM-VIS-6", "description": "Machine vise 6in", "qty": 7, "unit_price": 289.0}, {"line_no": 3, "sku": "AM-CHK-125", "description": "Lathe chuck 125mm", "qty": 15, "unit_price": 412.6}, {"line_no": 4, "sku": "AM-END-12", "description": "End mill 12mm carbide", "qty": 27, "unit_price": 68.2}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 4, "2": 7, "3": 15, "4": 27}, "grn_count": 1, "grn_numbers": ["GRN-88310"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V10", "name": "Ashford Machine Tools Ltd.", "city": "Sheffield, UK", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Pennine & Yorkshire Bank", "bank_routing": "GB29 NWBK 6016", "bank_account": "1331 9268 19", "tax_rate": 0.0}
```

**Step 7 — LLM call** (agent: `matcher`, 2240+80 tok, 2.46s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V10", "po_number": "PO-2025-4110", "total": 10432.6, "invoice_no": "AMT-401"})`
- agent called `arithmetic_check({"vendor_id": "V10"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2379+171 tok, 3.52s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"AMT-401","po_number":"PO-2025-4110","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4110 exists for vendor V10 in USD, and all invoice line unit prices match the PO exactly: 94.80, 289.00, 412.60, and 68.20. GRN totals from GRN-88310 fully cover the billed quantities (4, 7, 15, and 27 respectively), arithmetic checks passed including tax 0.00 at a 0.0 tax rate and total 10,432.60, the remit-to bank details match vendor master, and no duplicate payment was found for invoice AMT-401 or the same vendor/PO/amount combination."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: NIS-2025-404

**Step 1 — LLM call** (agent: `extractor`, 555+252 tok, 3.69s)
- assistant said:

```
{"invoice_no":"NIS-2025-404","vendor_name":"Northgate Ind. Supply (a div. of NIS Holdings)","date":"2025-06-22","po_number":"PO-2025-4111","currency":"USD","lines":[{"sku":"NG-3305","description":"Absorbent pads, case","qty":5,"unit_price":42.50,"amount":212.50},{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":13,"unit_price":6.95,"amount":90.35},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":36,"unit_price":149.00,"amount":5364.00},{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":13,"unit_price":18.40,"amount":239.20}],"subtotal":5906.05,"tax":428.19,"total":6334.24,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-404"}`

**Step 3 — LLM call** (agent: `matcher`, 2076+110 tok, 3.07s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4111"})`
- agent called `get_received_totals({"po_number": "PO-2025-4111"})`
- agent called `get_vendor_by_name({"name": "Northgate Ind. Supply (a div. of NIS Holdings)"})`
- agent called `arithmetic_check({"vendor_id": "V01"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4111", "vendor_id": "V01", "date": "2025-04-23", "currency": "USD", "lines": [{"line_no": 1, "sku": "NG-3305", "description": "Absorbent pads, case", "qty": 5, "unit_price": 42.5}, {"line_no": 2, "sku": "NG-7720", "description": "Safety goggles, anti-fog", "qty": 13, "unit_price": 6.95}, {"line_no": 3, "sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 36, "unit_price": 149.0}, {"line_no": 4, "sku": "NG-4410", "description": "Nitrile work gloves, box of 100", "qty": 13, "unit_price": 18.4}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 5, "2": 13, "3": 36, "4": 13}, "grn_count": 2, "grn_numbers": ["GRN-88311", "GRN-88312"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V01", "name": "Northgate Industrial Supply LLC", "city": "Columbus, OH", "currency": "USD", "payment_terms": "Net 30", "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "tax_rate": 0.0725, "memory": {"known_aliases": ["Northgate Ind. Supply (a div. of NIS Holdings)", "NIS Holdings LLC", "Northgate Industrial"], "notes": "Invoices under NIS Holdings trade names since 2024 reorg. Split deliveries common."}}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (428.19 ~= 428.19).", "Remit-to bank details match vendor master."]}
```

**Step 8 — LLM call** (agent: `matcher`, 2654+50 tok, 2.43s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id":"V01","po_number":"PO-2025-4111","total":6334.24,"invoice_no":"NIS-2025-404"})`

**Step 9 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 10 — LLM call** (agent: `matcher`, 2721+183 tok, 3.86s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "NIS-2025-404",
  "po_number": "PO-2025-4111",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4111 exists for vendor V01, the invoice currency matches the PO (USD), all billed unit prices match the PO exactly, and received totals across GRNs GRN-88311 and GRN-88312 fully support the billed quantities (line totals received: 5, 13, 36, and 13). Arithmetic check found no tax or total errors, the remit-to bank details match vendor master exactly, and payment-history screening found no duplicate for invoice NIS-2025-404 or for vendor V01 + PO-2025-4111 + total 6334.24."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: HEC-2025-404

**Step 1 — LLM call** (agent: `extractor`, 451+180 tok, 2.88s)
- assistant said:

```
{"invoice_no":"HEC-2025-404","vendor_name":"Helios Electrical Components","date":"2025-07-08","po_number":"PO-2025-4112","currency":"USD","lines":[{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":24,"unit_price":118.00,"amount":2832.00},{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":14,"unit_price":9.85,"amount":137.90}],"subtotal":2969.90,"tax":255.42,"total":3225.32,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-404"}`

**Step 3 — LLM call** (agent: `matcher`, 1502+83 tok, 3.24s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4112"})`
- agent called `get_received_totals({"po_number": "PO-2025-4112"})`
- agent called `get_vendor_by_name({"name": "Helios Electrical Components"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4112", "vendor_id": "V05", "date": "2025-04-13", "currency": "USD", "lines": [{"line_no": 1, "sku": "HE-CAB-14", "description": "Copper cable 14AWG, 500ft spool", "qty": 24, "unit_price": 118.0}, {"line_no": 2, "sku": "HE-CB-20", "description": "Circuit breaker 20A DIN", "qty": 14, "unit_price": 9.85}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 24, "2": 14}, "grn_count": 1, "grn_numbers": ["GRN-88313"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V05", "name": "Helios Electrical Components", "city": "Tucson, AZ", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Desert West Bank", "bank_routing": "122100024", "bank_account": "3348812706", "tax_rate": 0.086}
```

**Step 7 — LLM call** (agent: `matcher`, 1856+83 tok, 2.81s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V05", "po_number": "PO-2025-4112", "total": 3225.32, "invoice_no": "HEC-2025-404"})`
- agent called `arithmetic_check({"vendor_id": "V05"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (255.42 ~= 255.41).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 1998+154 tok, 3.52s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"HEC-2025-404","po_number":"PO-2025-4112","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4112 exists for vendor V05 in USD, and the invoice lines match the PO prices exactly: HE-CAB-14 at 24 x 118.00 and HE-CB-20 at 14 x 9.85. GRN GRN-88313 shows full receipt of 24 and 14 units respectively, arithmetic_check passed the totals and tax (tax 255.42 accepted vs expected 255.41 within tolerance), bank details match the vendor master, and no duplicate payment or invoice number was found."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: MF/25/404

**Step 1 — LLM call** (agent: `extractor`, 480+178 tok, 3.24s)
- assistant said:

```
{"invoice_no":"MF/25/404","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-06-19","po_number":"PO-2025-4113","currency":"USD","lines":[{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":5,"unit_price":70.28,"amount":351.40},{"sku":"MF-W-8","description":"Flat washers 8mm, box 1000","qty":8,"unit_price":15.30,"amount":122.40}],"subtotal":473.80,"tax":28.43,"total":502.23,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/404"}`

**Step 3 — LLM call** (agent: `matcher`, 1499+87 tok, 2.38s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4113"})`
- agent called `get_received_totals({"po_number": "PO-2025-4113"})`
- agent called `get_vendor_by_name({"name": "MERIDIAN FASTENERS INC."})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4113", "vendor_id": "V03", "date": "2025-04-01", "currency": "USD", "lines": [{"line_no": 1, "sku": "MF-ANC-10", "description": "Concrete anchors 10mm, box 100", "qty": 5, "unit_price": 62.75}, {"line_no": 2, "sku": "MF-W-8", "description": "Flat washers 8mm, box 1000", "qty": 8, "unit_price": 15.3}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 5, "2": 8}, "grn_count": 1, "grn_numbers": ["GRN-88314"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V03", "name": "Meridian Fasteners Inc.", "city": "Erie, PA", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Keystone National", "bank_routing": "031000503", "bank_account": "5583920164", "tax_rate": 0.06}
```

**Step 7 — LLM call** (agent: `matcher`, 1857+80 tok, 2.65s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V03", "po_number": "PO-2025-4113", "total": 502.23, "invoice_no": "MF/25/404"})`
- agent called `arithmetic_check({"vendor_id": "V03"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (28.43 ~= 28.43).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 1996+192 tok, 3.95s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "MF/25/404",
  "po_number": "PO-2025-4113",
  "decision": "hold",
  "discrepancies": [
    "PRICE_MISMATCH"
  ],
  "explanation": "PO PO-2025-4113 exists in USD for vendor V03, GRN-88314 confirms receipts of 5 units for MF-ANC-10 and 8 units for MF-W-8, and no duplicate payment was found for invoice MF/25/404 or total 502.23. The invoice line for MF-ANC-10 bills unit price 70.28 versus the PO unit price 62.75, which exceeds the 0.5% tolerance, while the second line matches at 15.30; arithmetic checks, tax (28.43 at 6%), currency, and bank details all pass."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH"], "engine_codes": ["PRICE_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: SOI-25-404

**Step 1 — LLM call** (agent: `extractor`, 507+207 tok, 3.39s)
- assistant said:

```
{"invoice_no":"SOI-25-404","vendor_name":"Stellar Office Interiors","date":"2025-06-23","po_number":"PO-2025-4114","currency":"USD","lines":[{"sku":"SO-MON-ARM","description":"Dual monitor arm","qty":30,"unit_price":80.19,"amount":2405.70},{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":27,"unit_price":189.00,"amount":5103.00},{"sku":"SO-FIL-3D","description":"File cabinet 3-drawer","qty":11,"unit_price":156.80,"amount":1724.80}],"subtotal":9233.50,"tax":747.91,"total":9981.41,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-404"}`

**Step 3 — LLM call** (agent: `matcher`, 1689+83 tok, 2.45s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4114"})`
- agent called `get_received_totals({"po_number": "PO-2025-4114"})`
- agent called `get_vendor_by_name({"name": "Stellar Office Interiors"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4114", "vendor_id": "V07", "date": "2025-04-01", "currency": "USD", "lines": [{"line_no": 1, "sku": "SO-MON-ARM", "description": "Dual monitor arm", "qty": 30, "unit_price": 74.25}, {"line_no": 2, "sku": "SO-CHR-T2", "description": "Task chair, mesh back", "qty": 27, "unit_price": 189.0}, {"line_no": 3, "sku": "SO-FIL-3D", "description": "File cabinet 3-drawer", "qty": 11, "unit_price": 156.8}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 30, "2": 27, "3": 11}, "grn_count": 1, "grn_numbers": ["GRN-88315"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V07", "name": "Stellar Office Interiors", "city": "Denver, CO", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Front Range Credit Union", "bank_routing": "107000233", "bank_account": "8812204575", "tax_rate": 0.081}
```

**Step 7 — LLM call** (agent: `matcher`, 2082+82 tok, 3.99s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V07", "po_number": "PO-2025-4114", "total": 9981.41, "invoice_no": "SOI-25-404"})`
- agent called `arithmetic_check({"vendor_id": "V07"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (747.91 ~= 747.91).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2223+199 tok, 4.03s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "SOI-25-404",
  "po_number": "PO-2025-4114",
  "decision": "hold",
  "discrepancies": [
    "PRICE_MISMATCH"
  ],
  "explanation": "PO PO-2025-4114 exists, GRN GRN-88315 confirms full receipt of 30, 27, and 11 units for lines 1-3, and no duplicate payment was found for vendor V07 / invoice SOI-25-404 / total 9981.41. The invoice is on hold because line SKU SO-MON-ARM is billed at 80.19 versus the PO unit price of 74.25, which exceeds the 0.5% price tolerance; the other line prices match, the currency is USD on both invoice and PO, arithmetic passed, and the remit-to bank details match the vendor master."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH"], "engine_codes": ["PRICE_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: AMT-404

**Step 1 — LLM call** (agent: `extractor`, 485+181 tok, 3.15s)
- assistant said:

```
{"invoice_no":"AMT-404","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-06-01","po_number":"PO-2025-4115","currency":"USD","lines":[{"sku":"AM-END-12","description":"End mill 12mm carbide","qty":28,"unit_price":78.43,"amount":2196.04},{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":14,"unit_price":412.60,"amount":5776.40}],"subtotal":7972.44,"tax":0.00,"total":7972.44,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-404"}`

**Step 3 — LLM call** (agent: `matcher`, 1504+85 tok, 2.65s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4115"})`
- agent called `get_received_totals({"po_number": "PO-2025-4115"})`
- agent called `get_vendor_by_name({"name": "Ashford Machine Tools Ltd."})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4115", "vendor_id": "V10", "date": "2025-05-14", "currency": "USD", "lines": [{"line_no": 1, "sku": "AM-END-12", "description": "End mill 12mm carbide", "qty": 28, "unit_price": 68.2}, {"line_no": 2, "sku": "AM-CHK-125", "description": "Lathe chuck 125mm", "qty": 14, "unit_price": 412.6}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 28, "2": 14}, "grn_count": 1, "grn_numbers": ["GRN-88316"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V10", "name": "Ashford Machine Tools Ltd.", "city": "Sheffield, UK", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Pennine & Yorkshire Bank", "bank_routing": "GB29 NWBK 6016", "bank_account": "1331 9268 19", "tax_rate": 0.0}
```

**Step 7 — LLM call** (agent: `matcher`, 1862+80 tok, 2.54s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V10", "po_number": "PO-2025-4115", "total": 7972.44, "invoice_no": "AMT-404"})`
- agent called `arithmetic_check({"vendor_id": "V10"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2001+195 tok, 3.88s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "AMT-404",
  "po_number": "PO-2025-4115",
  "decision": "hold",
  "discrepancies": [
    "PRICE_MISMATCH"
  ],
  "explanation": "PO PO-2025-4115 exists for vendor V10 and has GRN GRN-88316 with received quantities matching the invoice (line 1: 28 received vs 28 billed; line 2: 14 received vs 14 billed). However, invoice line 1 for SKU AM-END-12 bills USD 78.43 each while the PO unit price is USD 68.20, which exceeds the 0.5% tolerance; line 2 matches at USD 412.60. Currency is USD on both invoice and PO, bank details match the vendor master, no duplicate payment was found, and arithmetic/tax checks passed."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH"], "engine_codes": ["PRICE_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: INV-2025-0404

**Step 1 — LLM call** (agent: `extractor`, 440+175 tok, 3.19s)
- assistant said:

```
{"invoice_no":"INV-2025-0404","vendor_name":"Bluefin Packaging Co.","date":"2025-06-18","po_number":"PO-2025-4116","currency":"USD","lines":[{"sku":"BP-450","description":"Foam inserts, custom cut","qty":23,"unit_price":4.15,"amount":95.45},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":22,"unit_price":31.25,"amount":687.50}],"subtotal":782.95,"tax":54.81,"total":837.76,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0404"}`

**Step 3 — LLM call** (agent: `matcher`, 1615+84 tok, 2.54s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4116"})`
- agent called `get_received_totals({"po_number": "PO-2025-4116"})`
- agent called `get_vendor_by_name({"name": "Bluefin Packaging Co."})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4116", "vendor_id": "V02", "date": "2025-05-18", "currency": "USD", "lines": [{"line_no": 1, "sku": "BP-450", "description": "Foam inserts, custom cut", "qty": 23, "unit_price": 4.15}, {"line_no": 2, "sku": "BP-201", "description": "Corrugated boxes 18x12x10, bundle 25", "qty": 22, "unit_price": 31.25}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 13, "2": 13}, "grn_count": 1, "grn_numbers": ["GRN-88317"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V02", "name": "Bluefin Packaging Co.", "city": "Savannah, GA", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Coastal Georgia Bank", "bank_routing": "061000104", "bank_account": "7719045512", "tax_rate": 0.07, "memory": {"known_aliases": ["Bluefin Packaging Company"], "notes": "Re-issued invoices previously arrived with reformatted numbers (INV-25-xxx vs INV-2025-0xxx)."}}
```

**Step 7 — LLM call** (agent: `matcher`, 2011+82 tok, 2.58s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V02", "po_number": "PO-2025-4116", "total": 837.76, "invoice_no": "INV-2025-0404"})`
- agent called `arithmetic_check({"vendor_id": "V02"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (54.81 ~= 54.81).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2152+170 tok, 5.1s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"INV-2025-0404","po_number":"PO-2025-4116","decision":"hold","discrepancies":["QTY_MISMATCH"],"explanation":"PO PO-2025-4116 exists and matches the invoice currency (USD) and unit prices (BP-450 at 4.15; BP-201 at 31.25). Arithmetic passed, tax 54.81 matches the 7% rate on subtotal 782.95, bank details match vendor master, and no duplicate was found; however, the invoice bills 23 units on line 1 and 22 units on line 2 while total received per GRN is only 13 units for each line (GRN-88317), so billed quantity exceeds received quantity on both lines."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["QTY_MISMATCH"], "engine_codes": ["QTY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: HEC-2025-407

**Step 1 — LLM call** (agent: `extractor`, 515+255 tok, 3.54s)
- assistant said:

```
{"invoice_no":"HEC-2025-407","vendor_name":"Helios Electrical Components","date":"2025-07-27","po_number":"PO-2025-4117","currency":"USD","lines":[{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":17,"unit_price":14.20,"amount":241.40},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":4,"unit_price":118.00,"amount":472.00},{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":7,"unit_price":9.85,"amount":68.95},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":19,"unit_price":96.30,"amount":1829.70}],"subtotal":2612.05,"tax":224.64,"total":2836.69,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-407"}`

**Step 3 — LLM call** (agent: `matcher`, 1789+83 tok, 2.6s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4117"})`
- agent called `get_received_totals({"po_number": "PO-2025-4117"})`
- agent called `get_vendor_by_name({"name": "Helios Electrical Components"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4117", "vendor_id": "V05", "date": "2025-05-23", "currency": "USD", "lines": [{"line_no": 1, "sku": "HE-REL-24", "description": "Relay 24VDC 8-pin", "qty": 17, "unit_price": 14.2}, {"line_no": 2, "sku": "HE-CAB-14", "description": "Copper cable 14AWG, 500ft spool", "qty": 4, "unit_price": 118.0}, {"line_no": 3, "sku": "HE-CB-20", "description": "Circuit breaker 20A DIN", "qty": 7, "unit_price": 9.85}, {"line_no": 4, "sku": "HE-PSU-24", "description": "PSU 24V 10A DIN rail", "qty": 19, "unit_price": 96.3}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 10, "2": 2, "3": 4, "4": 11}, "grn_count": 1, "grn_numbers": ["GRN-88318"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V05", "name": "Helios Electrical Components", "city": "Tucson, AZ", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Desert West Bank", "bank_routing": "122100024", "bank_account": "3348812706", "tax_rate": 0.086}
```

**Step 7 — LLM call** (agent: `matcher`, 2248+83 tok, 2.5s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V05", "po_number": "PO-2025-4117", "total": 2836.69, "invoice_no": "HEC-2025-407"})`
- agent called `arithmetic_check({"vendor_id": "V05"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (224.64 ~= 224.64).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2390+181 tok, 3.77s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "HEC-2025-407",
  "po_number": "PO-2025-4117",
  "decision": "hold",
  "discrepancies": [
    "QTY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4117 exists and matches the invoice in USD, vendor V05, unit prices, and bank details; duplicate search found no prior paid invoice. However, billed quantities exceed received quantities on every line: line 1 billed 17 vs received 10, line 2 billed 4 vs received 2, line 3 billed 7 vs received 4, and line 4 billed 19 vs received 11 (GRN count 1, GRN-88318), so the invoice must be held for QTY_MISMATCH."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["QTY_MISMATCH"], "engine_codes": ["QTY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: GP-404

**Step 1 — LLM call** (agent: `extractor`, 510+249 tok, 3.88s)
- assistant said:

```
{"invoice_no":"GP-404","vendor_name":"Granite Peak Safety Gear","date":"2025-06-10","po_number":"PO-2025-4118","currency":"USD","lines":[{"sku":"GP-HH-CL2","description":"Hard hats class E, box 20","qty":22,"unit_price":196.00,"amount":4312.00},{"sku":"GP-VIS-XL","description":"Hi-vis vests XL, pack 10","qty":16,"unit_price":84.50,"amount":1352.00},{"sku":"GP-BOOT-10","description":"Steel toe boots size 10","qty":2,"unit_price":112.00,"amount":224.00},{"sku":"GP-EAR-200","description":"Ear plugs, box 200 pr","qty":15,"unit_price":38.90,"amount":583.50}],"subtotal":6471.50,"tax":388.29,"total":6859.79,"bank_name":"Sawtooth Community Bank","bank_routing":"123103729","bank_account":"2290156841","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-404"}`

**Step 3 — LLM call** (agent: `matcher`, 1779+84 tok, 2.65s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4118"})`
- agent called `get_received_totals({"po_number": "PO-2025-4118"})`
- agent called `get_vendor_by_name({"name": "Granite Peak Safety Gear"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4118", "vendor_id": "V08", "date": "2025-05-21", "currency": "USD", "lines": [{"line_no": 1, "sku": "GP-HH-CL2", "description": "Hard hats class E, box 20", "qty": 22, "unit_price": 196.0}, {"line_no": 2, "sku": "GP-VIS-XL", "description": "Hi-vis vests XL, pack 10", "qty": 16, "unit_price": 84.5}, {"line_no": 3, "sku": "GP-BOOT-10", "description": "Steel toe boots size 10", "qty": 2, "unit_price": 112.0}, {"line_no": 4, "sku": "GP-EAR-200", "description": "Ear plugs, box 200 pr", "qty": 15, "unit_price": 38.9}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 13, "2": 9, "3": 1, "4": 9}, "grn_count": 1, "grn_numbers": ["GRN-88319"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V08", "name": "Granite Peak Safety Gear", "city": "Boise, ID", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Sawtooth Community Bank", "bank_routing": "123103729", "bank_account": "2290156841", "tax_rate": 0.06}
```

**Step 7 — LLM call** (agent: `matcher`, 2235+79 tok, 2.7s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V08", "po_number": "PO-2025-4118", "total": 6859.79, "invoice_no": "GP-404"})`
- agent called `arithmetic_check({"vendor_id": "V08"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (388.29 ~= 388.29).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2373+179 tok, 4.09s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "GP-404",
  "po_number": "PO-2025-4118",
  "decision": "hold",
  "discrepancies": ["QTY_MISMATCH"],
  "explanation": "PO PO-2025-4118 exists, is in USD, and the invoice unit prices match the PO exactly for all four lines; arithmetic check passed, bank details match vendor V08, and no duplicate payment was found. However, billed quantities exceed received quantities on every line: line 1 billed 22 vs received 13, line 2 billed 16 vs received 9, line 3 billed 2 vs received 1, and line 4 billed 15 vs received 9 (GRN-88319 only), so the invoice must be held for QTY_MISMATCH."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["QTY_MISMATCH"], "engine_codes": ["QTY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: CCW-404

**Step 1 — LLM call** (agent: `extractor`, 522+220 tok, 3.34s)
- assistant said:

```
{"invoice_no":"CCW-404","vendor_name":"Cascadia Chemical Works","date":"2025-07-28","po_number":"PO-2025-4119","currency":"USD","lines":[{"sku":"CC-COOL-55","description":"Machine coolant concentrate, 55gal","qty":32,"unit_price":744.50,"amount":23824.00},{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":30,"unit_price":87.40,"amount":2622.00},{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":21,"unit_price":612.00,"amount":12852.00}],"subtotal":39298.00,"tax":3733.31,"total":43031.31,"bank_name":"Puget Sound Trust","bank_routing":"125000024","bank_account":"9027481133","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-404"}`

**Step 3 — LLM call** (agent: `matcher`, 1577+84 tok, 2.61s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4119"})`
- agent called `get_received_totals({"po_number": "PO-2025-4119"})`
- agent called `get_vendor_by_name({"name": "Cascadia Chemical Works"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4119", "vendor_id": "V04", "date": "2025-06-18", "currency": "USD", "lines": [{"line_no": 1, "sku": "CC-COOL-55", "description": "Machine coolant concentrate, 55gal", "qty": 32, "unit_price": 744.5}, {"line_no": 2, "sku": "CC-DEG-5", "description": "Industrial degreaser, 5gal", "qty": 30, "unit_price": 87.4}, {"line_no": 3, "sku": "CC-IPA-55", "description": "Isopropyl alcohol 99%, 55gal drum", "qty": 21, "unit_price": 612.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-4119"}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V04", "name": "Cascadia Chemical Works", "city": "Tacoma, WA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Puget Sound Trust", "bank_routing": "125000024", "bank_account": "9027481133", "tax_rate": 0.095}
```

**Step 7 — LLM call** (agent: `matcher`, 1958+80 tok, 2.66s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V04", "po_number": "PO-2025-4119", "total": 43031.31, "invoice_no": "CCW-404"})`
- agent called `arithmetic_check({"vendor_id": "V04"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (3733.31 ~= 3733.31).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2099+160 tok, 3.67s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"CCW-404","po_number":"PO-2025-4119","decision":"hold","discrepancies":["GRN_MISSING"],"explanation":"PO PO-2025-4119 exists for vendor V04, the invoice currency matches the PO (USD), line unit prices match the PO exactly (744.50, 87.40, and 612.00), arithmetic passed, bank details match the vendor master, and no duplicate was found in payment history. However, no goods receipt notes exist for PO-2025-4119, so there is no received quantity on record to support the billed quantities of 32, 30, and 21; therefore the invoice must be held for GRN_MISSING."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["GRN_MISSING"], "engine_codes": ["GRN_MISSING"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: ALS-INV-404

**Step 1 — LLM call** (agent: `extractor`, 525+230 tok, 4.22s)
- assistant said:

```
{"invoice_no":"ALS-INV-404","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-06-25","po_number":"PO-2025-4120","currency":"USD","lines":[{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":15,"unit_price":18.50,"amount":277.50},{"sku":"AL-LIFT","description":"Liftgate service","qty":11,"unit_price":45.00,"amount":495.00},{"sku":"AL-FUEL","description":"Fuel surcharge","qty":40,"unit_price":63.75,"amount":2550.00},{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":3,"unit_price":425.00,"amount":1275.00}],"subtotal":4597.50,"tax":0.00,"total":4597.50,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-404"}`

**Step 3 — LLM call** (agent: `matcher`, 1633+85 tok, 2.95s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4120"})`
- agent called `get_vendor_by_name({"name": "AURIGA LOGISTICS SERVICES"})`
- agent called `get_received_totals({"po_number": "PO-2025-4120"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4120", "vendor_id": "V06", "date": "2025-06-04", "currency": "USD", "lines": [{"line_no": 1, "sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 15, "unit_price": 18.5}, {"line_no": 2, "sku": "AL-LIFT", "description": "Liftgate service", "qty": 11, "unit_price": 45.0}, {"line_no": 3, "sku": "AL-FUEL", "description": "Fuel surcharge", "qty": 40, "unit_price": 63.75}, {"line_no": 4, "sku": "AL-LTL-STD", "description": "LTL freight, standard lane", "qty": 3, "unit_price": 425.0}], "status": "open"}
```

**Step 5 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V06", "name": "Auriga Logistics Services", "city": "Memphis, TN", "currency": "USD", "payment_terms": "Net 45", "bank_name": "River City Bank", "bank_routing": "084000026", "bank_account": "6650371928", "tax_rate": 0.0}
```

**Step 6 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-4120"}
```

**Step 7 — LLM call** (agent: `matcher`, 2034+81 tok, 2.43s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V06", "po_number": "PO-2025-4120", "total": 4597.5, "invoice_no": "ALS-INV-404"})`
- agent called `arithmetic_check({"vendor_id": "V06"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2174+196 tok, 4.15s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"ALS-INV-404","po_number":"PO-2025-4120","decision":"hold","discrepancies":["GRN_MISSING","QTY_MISMATCH"],"explanation":"PO PO-2025-4120 exists for vendor V06 in USD and the invoice unit prices match the PO exactly (18.50, 45.00, 63.75, 425.00); arithmetic check passed, tax is 0.00 at a 0.0 tax rate, bank details match vendor master, and no duplicate payment was found for invoice ALS-INV-404. However, no GRNs exist for PO-2025-4120, so GRN_MISSING applies, and with received quantities effectively at 0, the billed quantities of 15, 11, 40, and 3 exceed received quantities on every line, so QTY_MISMATCH also applies."}
```

**Step 11 — verifier**: `{"agree": false, "matcher_codes": ["GRN_MISSING", "QTY_MISMATCH"], "engine_codes": ["GRN_MISSING"], "matcher_decision": "hold", "engine_decision": "hold"}`

**Step 12 — LLM call** (agent: `matcher`, 1818+85 tok, 3.1s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4120"})`
- agent called `get_vendor_by_name({"name": "AURIGA LOGISTICS SERVICES"})`
- agent called `get_received_totals({"po_number": "PO-2025-4120"})`

**Step 13 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4120", "vendor_id": "V06", "date": "2025-06-04", "currency": "USD", "lines": [{"line_no": 1, "sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 15, "unit_price": 18.5}, {"line_no": 2, "sku": "AL-LIFT", "description": "Liftgate service", "qty": 11, "unit_price": 45.0}, {"line_no": 3, "sku": "AL-FUEL", "description": "Fuel surcharge", "qty": 40, "unit_price": 63.75}, {"line_no": 4, "sku": "AL-LTL-STD", "description": "LTL freight, standard lane", "qty": 3, "unit_price": 425.0}], "status": "open"}
```

**Step 14 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V06", "name": "Auriga Logistics Services", "city": "Memphis, TN", "currency": "USD", "payment_terms": "Net 45", "bank_name": "River City Bank", "bank_routing": "084000026", "bank_account": "6650371928", "tax_rate": 0.0}
```

**Step 15 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-4120"}
```

**Step 16 — LLM call** (agent: `matcher`, 2219+81 tok, 2.81s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V06", "po_number": "PO-2025-4120", "total": 4597.5, "invoice_no": "ALS-INV-404"})`
- agent called `arithmetic_check({"vendor_id": "V06"})`

**Step 17 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 18 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 19 — LLM call** (agent: `matcher`, 2359+181 tok, 4.2s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "ALS-INV-404",
  "po_number": "PO-2025-4120",
  "decision": "hold",
  "discrepancies": ["GRN_MISSING"],
  "explanation": "PO PO-2025-4120 exists for vendor V06 in USD, and all invoiced unit prices match the PO exactly: AL-WHS-P 18.50, AL-LIFT 45.00, AL-FUEL 63.75, and AL-LTL-STD 425.00. No goods receipt notes exist for PO-2025-4120, so the invoice must be held for GRN_MISSING. Arithmetic/tax checks passed (tax 0.00 at vendor tax rate 0.0), bank details match the vendor master, and no duplicate payment was found."
}
```

**Step 20 — verifier**: `{"agree": true, "matcher_codes": ["GRN_MISSING"], "engine_codes": ["GRN_MISSING"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: INV-2025-0407

**Step 1 — LLM call** (agent: `extractor`, 501+243 tok, 4.06s)
- assistant said:

```
{"invoice_no":"INV-2025-0407","vendor_name":"Bluefin Packaging Co.","date":"2025-06-11","po_number":"PO-2025-4121","currency":"USD","lines":[{"sku":"BP-115","description":"Stretch wrap roll 80ga","qty":18,"unit_price":12.80,"amount":230.40},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":12,"unit_price":31.25,"amount":375.00},{"sku":"BP-330","description":"Packing tape, case of 36","qty":33,"unit_price":58.90,"amount":1943.70},{"sku":"BP-450","description":"Foam inserts, custom cut","qty":31,"unit_price":4.15,"amount":128.65}],"subtotal":2677.75,"tax":187.44,"total":2865.19,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0407"}`

**Step 3 — LLM call** (agent: `matcher`, 1880+84 tok, 2.74s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4121"})`
- agent called `get_received_totals({"po_number": "PO-2025-4121"})`
- agent called `get_vendor_by_name({"name": "Bluefin Packaging Co."})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4121", "vendor_id": "V02", "date": "2025-05-10", "currency": "USD", "lines": [{"line_no": 1, "sku": "BP-115", "description": "Stretch wrap roll 80ga", "qty": 18, "unit_price": 12.8}, {"line_no": 2, "sku": "BP-201", "description": "Corrugated boxes 18x12x10, bundle 25", "qty": 12, "unit_price": 31.25}, {"line_no": 3, "sku": "BP-330", "description": "Packing tape, case of 36", "qty": 33, "unit_price": 58.9}, {"line_no": 4, "sku": "BP-450", "description": "Foam inserts, custom cut", "qty": 31, "unit_price": 4.15}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 18, "2": 12, "3": 33, "4": 31}, "grn_count": 1, "grn_numbers": ["GRN-88320"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V02", "name": "Bluefin Packaging Co.", "city": "Savannah, GA", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Coastal Georgia Bank", "bank_routing": "061000104", "bank_account": "7719045512", "tax_rate": 0.07, "memory": {"known_aliases": ["Bluefin Packaging Company"], "notes": "Re-issued invoices previously arrived with reformatted numbers (INV-25-xxx vs INV-2025-0xxx)."}}
```

**Step 7 — LLM call** (agent: `matcher`, 2371+83 tok, 2.55s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V02", "po_number": "PO-2025-4121", "total": 2865.19, "invoice_no": "INV-2025-0407"})`
- agent called `arithmetic_check({"vendor_id": "V02"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": [{"invoice_no": "INV-25-407", "vendor_id": "V02", "po_number": "PO-2025-4121", "amount": 2865.19, "currency": "USD", "paid_date": "2025-06-14", "match_reasons": ["same vendor + PO + amount already paid"]}]}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (187.44 ~= 187.44).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2587+172 tok, 3.97s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "INV-2025-0407",
  "po_number": "PO-2025-4121",
  "decision": "reject",
  "discrepancies": [
    "DUPLICATE"
  ],
  "explanation": "PO PO-2025-4121 exists for vendor V02 in USD, all billed quantities match received quantities from GRN-88320 (18, 12, 33, and 31), unit prices match the PO, and arithmetic/bank checks passed. However, payment history already shows a paid invoice for the same vendor, PO, and total amount: invoice INV-25-407 for USD 2865.19 paid on 2025-06-14, so this invoice must be rejected as DUPLICATE."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["DUPLICATE"], "engine_codes": ["DUPLICATE"], "matcher_decision": "reject", "engine_decision": "reject"}`


## Case: ALS-INV-407

**Step 1 — LLM call** (agent: `extractor`, 492+194 tok, 4.91s)
- assistant said:

```
{"invoice_no":"ALS-INV-407","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-12","po_number":"PO-2025-4122","currency":"USD","lines":[{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":33,"unit_price":18.50,"amount":610.50},{"sku":"AL-LIFT","description":"Liftgate service","qty":10,"unit_price":45.00,"amount":450.00},{"sku":"AL-FUEL","description":"Fuel surcharge","qty":9,"unit_price":63.75,"amount":573.75}],"subtotal":1634.25,"tax":0.00,"total":1634.25,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-407"}`

**Step 3 — LLM call** (agent: `matcher`, 1661+85 tok, 2.89s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4122"})`
- agent called `get_received_totals({"po_number": "PO-2025-4122"})`
- agent called `get_vendor_by_name({"name": "AURIGA LOGISTICS SERVICES"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4122", "vendor_id": "V06", "date": "2025-05-12", "currency": "USD", "lines": [{"line_no": 1, "sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 33, "unit_price": 18.5}, {"line_no": 2, "sku": "AL-LIFT", "description": "Liftgate service", "qty": 10, "unit_price": 45.0}, {"line_no": 3, "sku": "AL-FUEL", "description": "Fuel surcharge", "qty": 9, "unit_price": 63.75}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 33, "2": 10, "3": 9}, "grn_count": 1, "grn_numbers": ["GRN-88321"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V06", "name": "Auriga Logistics Services", "city": "Memphis, TN", "currency": "USD", "payment_terms": "Net 45", "bank_name": "River City Bank", "bank_routing": "084000026", "bank_account": "6650371928", "tax_rate": 0.0}
```

**Step 7 — LLM call** (agent: `matcher`, 2046+81 tok, 2.98s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V06", "po_number": "PO-2025-4122", "total": 1634.25, "invoice_no": "ALS-INV-407"})`
- agent called `arithmetic_check({"vendor_id": "V06"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": [{"invoice_no": "ALS-INV-407", "vendor_id": "V06", "po_number": "PO-2025-4122", "amount": 1634.25, "currency": "USD", "paid_date": "2025-07-02", "match_reasons": ["invoice number already paid (normalized match)", "same vendor + PO + amount already paid"]}]}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2269+196 tok, 3.82s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "ALS-INV-407",
  "po_number": "PO-2025-4122",
  "decision": "reject",
  "discrepancies": [
    "DUPLICATE"
  ],
  "explanation": "PO PO-2025-4122 exists for vendor V06 in USD, all three invoice line prices match the PO exactly (18.50, 45.00, and 63.75), and billed quantities 33/10/9 do not exceed GRN-88321 received quantities 33/10/9; arithmetic, tax 0.00, and bank details also passed. However, payment history shows invoice ALS-INV-407 was already paid on 2025-07-02 for vendor V06 against the same PO and amount USD 1,634.25, so this invoice is a DUPLICATE and must be rejected."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["DUPLICATE"], "engine_codes": ["DUPLICATE"], "matcher_decision": "reject", "engine_decision": "reject"}`


## Case: NIS-2025-407

**Step 1 — LLM call** (agent: `extractor`, 480+174 tok, 3.09s)
- assistant said:

```
{"invoice_no":"NIS-2025-407","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-08","po_number":"PO-2025-4123","currency":"USD","lines":[{"sku":"NG-3305","description":"Absorbent pads, case","qty":30,"unit_price":42.50,"amount":1275.00},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":22,"unit_price":149.00,"amount":3278.00}],"subtotal":4553.00,"tax":367.23,"total":4920.23,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-407"}`

**Step 3 — LLM call** (agent: `matcher`, 1627+84 tok, 2.62s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4123"})`
- agent called `get_received_totals({"po_number": "PO-2025-4123"})`
- agent called `get_vendor_by_name({"name": "Northgate Industrial Supply LLC"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4123", "vendor_id": "V01", "date": "2025-05-27", "currency": "USD", "lines": [{"line_no": 1, "sku": "NG-3305", "description": "Absorbent pads, case", "qty": 30, "unit_price": 42.5}, {"line_no": 2, "sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 22, "unit_price": 149.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 30, "2": 22}, "grn_count": 1, "grn_numbers": ["GRN-88322"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V01", "name": "Northgate Industrial Supply LLC", "city": "Columbus, OH", "currency": "USD", "payment_terms": "Net 30", "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "tax_rate": 0.0725, "memory": {"known_aliases": ["Northgate Ind. Supply (a div. of NIS Holdings)", "NIS Holdings LLC", "Northgate Industrial"], "notes": "Invoices under NIS Holdings trade names since 2024 reorg. Split deliveries common."}}
```

**Step 7 — LLM call** (agent: `matcher`, 2033+83 tok, 2.92s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V01", "po_number": "PO-2025-4123", "total": 4920.23, "invoice_no": "NIS-2025-407"})`
- agent called `arithmetic_check({"vendor_id": "V01"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TAX_ERROR", "evidence": "Tax 367.23 != tax_rate 0.0725 x subtotal 4553.00 = 330.09 (tolerance $0.02)."}], "checks_passed": ["Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2208+176 tok, 3.9s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"NIS-2025-407","po_number":"PO-2025-4123","decision":"hold","discrepancies":["TAX_ERROR"],"explanation":"PO PO-2025-4123 exists for vendor V01 in USD, and the invoice line prices match the PO (NG-3305 at 42.50; NG-1180 at 149.00); billed quantities 30 and 22 do not exceed received quantities on GRN-88322 (30 and 22). Arithmetic check found a tax discrepancy: invoice tax is 367.23, but at the vendor master tax rate of 0.0725 on subtotal 4553.00, expected tax is 330.09, exceeding the $0.02 tolerance; no duplicate payment or bank detail change was found."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["TAX_ERROR"], "engine_codes": ["TAX_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: VPL-2025-404

**Step 1 — LLM call** (agent: `extractor`, 506+232 tok, 4.45s)
- assistant said:

```
{"invoice_no":"VPL-2025-404","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-06-06","po_number":"PO-2025-4124","currency":"EUR","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":29,"unit_price":21.40,"amount":620.60},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":17,"unit_price":340.00,"amount":5780.00},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":39,"unit_price":9.60,"amount":374.40}],"subtotal":6775.00,"tax":1339.85,"total":8114.85,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-404"}`

**Step 3 — LLM call** (agent: `matcher`, 1721+88 tok, 2.68s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4124"})`
- agent called `get_received_totals({"po_number": "PO-2025-4124"})`
- agent called `get_vendor_by_name({"name": "VIREO PRINT & LABEL GMBH"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4124", "vendor_id": "V09", "date": "2025-05-17", "currency": "EUR", "lines": [{"line_no": 1, "sku": "VP-LBL-4x6", "description": "Thermal labels 4x6, roll 500", "qty": 29, "unit_price": 21.4}, {"line_no": 2, "sku": "VP-TAG-ASSET", "description": "Asset tags, custom, 1000", "qty": 17, "unit_price": 340.0}, {"line_no": 3, "sku": "VP-RIB-110", "description": "TTR ribbon 110mm", "qty": 39, "unit_price": 9.6}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 29, "2": 17, "3": 39}, "grn_count": 1, "grn_numbers": ["GRN-88323"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V09", "name": "Vireo Print & Label GmbH", "city": "Hamburg, DE", "currency": "EUR", "payment_terms": "Net 30", "bank_name": "Hansa Handelsbank", "bank_routing": "DE44 5001 0517", "bank_account": "5407 3249 31", "tax_rate": 0.19, "memory": {"known_aliases": ["Vireo Print and Label"], "notes": "Always bills in EUR. Any USD invoice from this vendor is anomalous."}}
```

**Step 7 — LLM call** (agent: `matcher`, 2179+83 tok, 2.43s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V09", "po_number": "PO-2025-4124", "total": 8114.85, "invoice_no": "VPL-2025-404"})`
- agent called `arithmetic_check({"vendor_id": "V09"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TAX_ERROR", "evidence": "Tax 1339.85 != tax_rate 0.1900 x subtotal 6775.00 = 1287.25 (tolerance $0.02)."}], "checks_passed": ["Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2356+179 tok, 4.15s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"VPL-2025-404","po_number":"PO-2025-4124","decision":"hold","discrepancies":["TAX_ERROR"],"explanation":"PO PO-2025-4124 exists for vendor V09, invoice currency EUR matches the PO, unit prices match the PO lines (21.40, 340.00, 9.60), and billed quantities 29/17/39 do not exceed received quantities from GRN-88323 of 29/17/39. Arithmetic check found a tax discrepancy: invoiced tax is 1339.85, but at the vendor master tax rate of 19% on subtotal 6775.00, expected tax is 1287.25, which exceeds the $0.02 tolerance; no duplicate payment or bank-detail mismatch was found."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["TAX_ERROR"], "engine_codes": ["TAX_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: SOI-25-407

**Step 1 — LLM call** (agent: `extractor`, 508+208 tok, 3.51s)
- assistant said:

```
{"invoice_no":"SOI-25-407","vendor_name":"Stellar Office Interiors","date":"2025-06-09","po_number":"PO-2025-4125","currency":"USD","lines":[{"sku":"SO-DSK-60","description":"Sit-stand desk 60in","qty":10,"unit_price":415.00,"amount":4150.00},{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":13,"unit_price":189.00,"amount":2457.00},{"sku":"SO-MON-ARM","description":"Dual monitor arm","qty":39,"unit_price":74.25,"amount":2985.75}],"subtotal":9592.75,"tax":777.01,"total":10369.76,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-407"}`

**Step 3 — LLM call** (agent: `matcher`, 1691+83 tok, 2.54s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4125"})`
- agent called `get_received_totals({"po_number": "PO-2025-4125"})`
- agent called `get_vendor_by_name({"name": "Stellar Office Interiors"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4125", "vendor_id": "V07", "date": "2025-06-23", "currency": "USD", "lines": [{"line_no": 1, "sku": "SO-DSK-60", "description": "Sit-stand desk 60in", "qty": 10, "unit_price": 415.0}, {"line_no": 2, "sku": "SO-CHR-T2", "description": "Task chair, mesh back", "qty": 13, "unit_price": 189.0}, {"line_no": 3, "sku": "SO-MON-ARM", "description": "Dual monitor arm", "qty": 39, "unit_price": 74.25}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 10, "2": 13, "3": 39}, "grn_count": 1, "grn_numbers": ["GRN-88324"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V07", "name": "Stellar Office Interiors", "city": "Denver, CO", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Front Range Credit Union", "bank_routing": "107000233", "bank_account": "8812204575", "tax_rate": 0.081}
```

**Step 7 — LLM call** (agent: `matcher`, 2085+82 tok, 2.5s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V07", "po_number": "PO-2025-4125", "total": 10369.76, "invoice_no": "SOI-25-407"})`
- agent called `arithmetic_check({"vendor_id": "V07"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TOTAL_ERROR", "evidence": "Line SO-MON-ARM: amount 2985.75 != qty 39 x unit price 74.25 = 2895.75."}], "checks_passed": ["Tax OK (777.01 ~= 777.01).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2269+203 tok, 3.88s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "SOI-25-407",
  "po_number": "PO-2025-4125",
  "decision": "hold",
  "discrepancies": [
    "TOTAL_ERROR"
  ],
  "explanation": "PO PO-2025-4125 exists for vendor V07 in USD, GRN GRN-88324 shows full receipt of 10 desks, 13 chairs, and 39 monitor arms, and the billed unit prices match the PO (415.00, 189.00, and 74.25). The invoice is not a duplicate and the remit-to bank matches vendor master, but line SO-MON-ARM has a line amount error: billed amount 2985.75 does not equal 39 × 74.25 = 2895.75; tax 777.01 is consistent with the vendor tax rate, so the invoice should be held for the line total discrepancy."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["TOTAL_ERROR"], "engine_codes": ["TOTAL_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: MF/25/407

**Step 1 — LLM call** (agent: `extractor`, 522+221 tok, 3.59s)
- assistant said:

```
{"invoice_no":"MF/25/407","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-06-27","po_number":"PO-2025-4126","currency":"USD","lines":[{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":18,"unit_price":62.75,"amount":1129.50},{"sku":"MF-W-8","description":"Flat washers 8mm, box 1000","qty":8,"unit_price":15.30,"amount":122.40},{"sku":"MF-M8-50","description":"Hex bolts M8x50 zinc, box 500","qty":34,"unit_price":44.00,"amount":1524.00}],"subtotal":2775.90,"tax":166.55,"total":2942.45,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/407"}`

**Step 3 — LLM call** (agent: `matcher`, 1649+87 tok, 2.77s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4126"})`
- agent called `get_received_totals({"po_number": "PO-2025-4126"})`
- agent called `get_vendor_by_name({"name": "MERIDIAN FASTENERS INC."})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4126", "vendor_id": "V03", "date": "2025-05-05", "currency": "USD", "lines": [{"line_no": 1, "sku": "MF-ANC-10", "description": "Concrete anchors 10mm, box 100", "qty": 18, "unit_price": 62.75}, {"line_no": 2, "sku": "MF-W-8", "description": "Flat washers 8mm, box 1000", "qty": 8, "unit_price": 15.3}, {"line_no": 3, "sku": "MF-M8-50", "description": "Hex bolts M8x50 zinc, box 500", "qty": 34, "unit_price": 44.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 18, "2": 8, "3": 34}, "grn_count": 1, "grn_numbers": ["GRN-88325"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V03", "name": "Meridian Fasteners Inc.", "city": "Erie, PA", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Keystone National", "bank_routing": "031000503", "bank_account": "5583920164", "tax_rate": 0.06}
```

**Step 7 — LLM call** (agent: `matcher`, 2061+81 tok, 3.55s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V03", "po_number": "PO-2025-4126", "total": 2942.45, "invoice_no": "MF/25/407"})`
- agent called `arithmetic_check({"vendor_id": "V03"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TOTAL_ERROR", "evidence": "Line MF-M8-50: amount 1524.00 != qty 34 x unit price 44.00 = 1496.00."}], "checks_passed": ["Tax OK (166.55 ~= 166.55).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2244+170 tok, 3.7s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "MF/25/407",
  "po_number": "PO-2025-4126",
  "decision": "hold",
  "discrepancies": [
    "TOTAL_ERROR"
  ],
  "explanation": "PO PO-2025-4126 exists for vendor V03, currency matches USD, all billed quantities match received quantities on GRN-88325 (18, 8, and 34), prices match the PO, bank details match the vendor master, and no duplicate payment was found. However, the invoice fails arithmetic validation: line MF-M8-50 shows amount 1524.00, but the arithmetic check found 34 x 44.00 = 1496.00, so the invoice must be held for TOTAL_ERROR."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["TOTAL_ERROR"], "engine_codes": ["TOTAL_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: HEC-2025-410

**Step 1 — LLM call** (agent: `extractor`, 486+221 tok, 3.61s)
- assistant said:

```
{"invoice_no":"HEC-2025-410","vendor_name":"Helios Electrical Components","date":"2025-07-02","po_number":"PO-2025-4127","currency":"USD","lines":[{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":8,"unit_price":118.00,"amount":944.00},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":11,"unit_price":96.30,"amount":1059.30},{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":38,"unit_price":14.20,"amount":539.60}],"subtotal":2542.90,"tax":218.69,"total":2761.59,"bank_name":"Meridian Trust Bank","bank_routing":"122100024","bank_account":"7791024468","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-410"}`

**Step 3 — LLM call** (agent: `matcher`, 1653+83 tok, 2.71s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4127"})`
- agent called `get_received_totals({"po_number": "PO-2025-4127"})`
- agent called `get_vendor_by_name({"name": "Helios Electrical Components"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4127", "vendor_id": "V05", "date": "2025-06-17", "currency": "USD", "lines": [{"line_no": 1, "sku": "HE-CAB-14", "description": "Copper cable 14AWG, 500ft spool", "qty": 8, "unit_price": 118.0}, {"line_no": 2, "sku": "HE-PSU-24", "description": "PSU 24V 10A DIN rail", "qty": 11, "unit_price": 96.3}, {"line_no": 3, "sku": "HE-REL-24", "description": "Relay 24VDC 8-pin", "qty": 38, "unit_price": 14.2}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 8, "2": 11, "3": 38}, "grn_count": 1, "grn_numbers": ["GRN-88326"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V05", "name": "Helios Electrical Components", "city": "Tucson, AZ", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Desert West Bank", "bank_routing": "122100024", "bank_account": "3348812706", "tax_rate": 0.086}
```

**Step 7 — LLM call** (agent: `matcher`, 2063+83 tok, 2.63s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V05", "po_number": "PO-2025-4127", "total": 2761.59, "invoice_no": "HEC-2025-410"})`
- agent called `arithmetic_check({"vendor_id": "V05"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "BANK_CHANGE", "evidence": "Remit-to account 7791024468 != vendor master 3348812706 \u2014 verify with vendor before payment."}], "checks_passed": ["Tax OK (218.69 ~= 218.69)."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2230+219 tok, 4.16s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "HEC-2025-410",
  "po_number": "PO-2025-4127",
  "decision": "hold",
  "discrepancies": ["BANK_CHANGE"],
  "explanation": "PO PO-2025-4127 exists for vendor V05 in USD, and the invoice line prices and quantities match the PO and received totals exactly: HE-CAB-14 8 received/billed at 118.00, HE-PSU-24 11 at 96.30, and HE-REL-24 38 at 14.20; GRN GRN-88326 covers all lines. Arithmetic and tax passed, and no duplicate payment was found for invoice HEC-2025-410 or total 2761.59. However, the remit-to bank differs from vendor master: routing 122100024 matches, but account 7791024468 on the invoice does not match vendor master account 3348812706, so the invoice must be held."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["BANK_CHANGE"], "engine_codes": ["BANK_CHANGE"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: GP-407

**Step 1 — LLM call** (agent: `extractor`, 478+212 tok, 3.31s)
- assistant said:

```
{"invoice_no":"GP-407","vendor_name":"Granite Peak Safety Gear","date":"2025-06-22","po_number":"PO-2025-4128","currency":"USD","lines":[{"sku":"GP-EAR-200","description":"Ear plugs, box 200 pr","qty":37,"unit_price":38.90,"amount":1439.30},{"sku":"GP-BOOT-10","description":"Steel toe boots size 10","qty":32,"unit_price":112.00,"amount":3584.00},{"sku":"GP-VIS-XL","description":"Hi-vis vests XL, pack 10","qty":36,"unit_price":84.50,"amount":3042.00}],"subtotal":8065.30,"tax":483.92,"total":8549.22,"bank_name":"Meridian Trust Bank","bank_routing":"123103729","bank_account":"4456108823","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-407"}`

**Step 3 — LLM call** (agent: `matcher`, 1636+84 tok, 2.93s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4128"})`
- agent called `get_received_totals({"po_number": "PO-2025-4128"})`
- agent called `get_vendor_by_name({"name": "Granite Peak Safety Gear"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4128", "vendor_id": "V08", "date": "2025-06-04", "currency": "USD", "lines": [{"line_no": 1, "sku": "GP-EAR-200", "description": "Ear plugs, box 200 pr", "qty": 37, "unit_price": 38.9}, {"line_no": 2, "sku": "GP-BOOT-10", "description": "Steel toe boots size 10", "qty": 32, "unit_price": 112.0}, {"line_no": 3, "sku": "GP-VIS-XL", "description": "Hi-vis vests XL, pack 10", "qty": 36, "unit_price": 84.5}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 37, "2": 32, "3": 36}, "grn_count": 1, "grn_numbers": ["GRN-88327"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V08", "name": "Granite Peak Safety Gear", "city": "Boise, ID", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Sawtooth Community Bank", "bank_routing": "123103729", "bank_account": "2290156841", "tax_rate": 0.06}
```

**Step 7 — LLM call** (agent: `matcher`, 2040+79 tok, 3.0s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V08", "po_number": "PO-2025-4128", "total": 8549.22, "invoice_no": "GP-407"})`
- agent called `arithmetic_check({"vendor_id": "V08"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "BANK_CHANGE", "evidence": "Remit-to account 4456108823 != vendor master 2290156841 \u2014 verify with vendor before payment."}], "checks_passed": ["Tax OK (483.92 ~= 483.92)."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2203+190 tok, 4.56s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "GP-407",
  "po_number": "PO-2025-4128",
  "decision": "hold",
  "discrepancies": [
    "BANK_CHANGE"
  ],
  "explanation": "PO PO-2025-4128 exists for vendor V08 in USD, all three invoice line prices match the PO (38.90, 112.00, 84.50), billed quantities match received quantities on GRN-88327 (37, 32, 36), and arithmetic passed including tax of 483.92 at the 6% vendor tax rate with no duplicate found. However, the invoice remit-to bank details differ from vendor master: routing 123103729 matches, but bank account 4456108823 differs from the master account 2290156841, so the invoice must be held for bank-change verification."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["BANK_CHANGE"], "engine_codes": ["BANK_CHANGE"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: VPL-2025-407

**Step 1 — LLM call** (agent: `extractor`, 533+230 tok, 3.39s)
- assistant said:

```
{"invoice_no":"VPL-2025-407","vendor_name":"Vireo Print & Label GmbH","date":"2025-06-22","po_number":"PO-2025-4129","currency":"USD","lines":[{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":20,"unit_price":340.00,"amount":6800.00},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":8,"unit_price":9.60,"amount":76.80},{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":15,"unit_price":21.40,"amount":321.00}],"subtotal":7197.80,"tax":1367.58,"total":8565.38,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-407"}`

**Step 3 — LLM call** (agent: `matcher`, 1719+86 tok, 2.49s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4129"})`
- agent called `get_received_totals({"po_number": "PO-2025-4129"})`
- agent called `get_vendor_by_name({"name": "Vireo Print & Label GmbH"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4129", "vendor_id": "V09", "date": "2025-05-23", "currency": "EUR", "lines": [{"line_no": 1, "sku": "VP-TAG-ASSET", "description": "Asset tags, custom, 1000", "qty": 20, "unit_price": 340.0}, {"line_no": 2, "sku": "VP-RIB-110", "description": "TTR ribbon 110mm", "qty": 8, "unit_price": 9.6}, {"line_no": 3, "sku": "VP-LBL-4x6", "description": "Thermal labels 4x6, roll 500", "qty": 15, "unit_price": 21.4}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 20, "2": 8, "3": 15}, "grn_count": 1, "grn_numbers": ["GRN-88328"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V09", "name": "Vireo Print & Label GmbH", "city": "Hamburg, DE", "currency": "EUR", "payment_terms": "Net 30", "bank_name": "Hansa Handelsbank", "bank_routing": "DE44 5001 0517", "bank_account": "5407 3249 31", "tax_rate": 0.19, "memory": {"known_aliases": ["Vireo Print and Label"], "notes": "Always bills in EUR. Any USD invoice from this vendor is anomalous."}}
```

**Step 7 — LLM call** (agent: `matcher`, 2175+83 tok, 2.55s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V09", "po_number": "PO-2025-4129", "total": 8565.38, "invoice_no": "VPL-2025-407"})`
- agent called `arithmetic_check({"vendor_id": "V09"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (1367.58 ~= 1367.58).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2319+198 tok, 3.53s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "VPL-2025-407",
  "po_number": "PO-2025-4129",
  "decision": "hold",
  "discrepancies": ["CURRENCY_MISMATCH"],
  "explanation": "PO PO-2025-4129 exists for vendor V09, and GRN GRN-88328 shows full receipt of all billed quantities: line 1 received 20, line 2 received 8, and line 3 received 15, matching the invoice quantities exactly. Unit prices also match the PO (340.00, 9.60, and 21.40), arithmetic passed including tax 1367.58, bank details match the vendor master, and no duplicate was found in payment history. However, the invoice is in USD while both the PO and vendor master currency are EUR, so the invoice must be held for CURRENCY_MISMATCH."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["CURRENCY_MISMATCH"], "engine_codes": ["CURRENCY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: AMT-407

**Step 1 — LLM call** (agent: `extractor`, 536+251 tok, 4.38s)
- assistant said:

```
{"invoice_no":"AMT-407","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-06-18","po_number":"PO-2025-9911","currency":"USD","lines":[{"sku":"AM-INS-CNMG","description":"Turning inserts CNMG, box 10","qty":24,"unit_price":94.80,"amount":2275.20},{"sku":"AM-VIS-6","description":"Machine vise 6in","qty":2,"unit_price":289.00,"amount":578.00},{"sku":"AM-END-12","description":"End mill 12mm carbide","qty":7,"unit_price":68.20,"amount":477.40},{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":18,"unit_price":412.60,"amount":7426.80}],"subtotal":10757.40,"tax":0.00,"total":10757.40,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-407"}`

**Step 3 — LLM call** (agent: `matcher`, 1351+79 tok, 5.28s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-9911"})`
- agent called `get_vendor_by_name({"name": "Ashford Machine Tools Ltd."})`
- agent called `arithmetic_check({"vendor_id": "V10"})`

**Step 4 — tool `get_po` responded:**

```
{"error": "PO PO-2025-9911 not found"}
```

**Step 5 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V10", "name": "Ashford Machine Tools Ltd.", "city": "Sheffield, UK", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Pennine & Yorkshire Bank", "bank_routing": "GB29 NWBK 6016", "bank_account": "1331 9268 19", "tax_rate": 0.0}
```

**Step 6 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 7 — LLM call** (agent: `matcher`, 1587+47 tok, 2.83s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id":"V10","po_number":"PO-2025-9911","total":10757.4,"invoice_no":"AMT-407"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — LLM call** (agent: `matcher`, 1651+149 tok, 4.51s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "AMT-407",
  "po_number": "PO-2025-9911",
  "decision": "hold",
  "discrepancies": ["PO_NOT_FOUND", "GRN_MISSING"],
  "explanation": "PO PO-2025-9911 was not found in the PO system, so the invoice cannot be matched to any authorized order. Because no valid PO exists, there are also no GRNs available for that PO reference. Duplicate screening found no prior payment match for vendor V10, and arithmetic/bank checks passed: total 10757.40, tax 0.00, and remit-to bank details match the vendor master."
}
```

**Step 10 — verifier**: `{"agree": false, "matcher_codes": ["GRN_MISSING", "PO_NOT_FOUND"], "engine_codes": ["PO_NOT_FOUND"], "matcher_decision": "hold", "engine_decision": "hold"}`

**Step 11 — LLM call** (agent: `matcher`, 1466+62 tok, 2.27s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-9911"})`
- agent called `get_vendor_by_name({"name": "Ashford Machine Tools Ltd."})`

**Step 12 — tool `get_po` responded:**

```
{"error": "PO PO-2025-9911 not found"}
```

**Step 13 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V10", "name": "Ashford Machine Tools Ltd.", "city": "Sheffield, UK", "currency": "USD", "payment_terms": "Net 45", "bank_name": "Pennine & Yorkshire Bank", "bank_routing": "GB29 NWBK 6016", "bank_account": "1331 9268 19", "tax_rate": 0.0}
```

**Step 14 — LLM call** (agent: `matcher`, 1645+80 tok, 2.77s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `arithmetic_check({"vendor_id": "V10"})`
- agent called `search_payments({"vendor_id": "V10", "po_number": "PO-2025-9911", "total": 10757.4, "invoice_no": "AMT-407"})`

**Step 15 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 16 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 17 — LLM call** (agent: `matcher`, 1784+128 tok, 3.44s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "AMT-407",
  "po_number": "PO-2025-9911",
  "decision": "hold",
  "discrepancies": ["PO_NOT_FOUND"],
  "explanation": "PO PO-2025-9911 does not exist in the PO system, so the invoice cannot be matched and must be held. Duplicate screening found no prior payment for vendor V10 with invoice AMT-407 or total 10757.40, and the verifier confirms tax is 0.00 and the remit-to bank details match the vendor master."
}
```

**Step 18 — verifier**: `{"agree": true, "matcher_codes": ["PO_NOT_FOUND"], "engine_codes": ["PO_NOT_FOUND"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: NIS-2025-410

**Step 1 — LLM call** (agent: `extractor`, 504+207 tok, 3.34s)
- assistant said:

```
{"invoice_no":"NIS-2025-410","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-01","po_number":"PO-2025-4131","currency":"USD","lines":[{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":15,"unit_price":7.65,"amount":114.75},{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":22,"unit_price":18.40,"amount":404.80},{"sku":"NG-3305","description":"Absorbent pads, case","qty":9,"unit_price":42.50,"amount":382.50}],"subtotal":902.05,"tax":65.40,"total":967.45,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-410"}`

**Step 3 — LLM call** (agent: `matcher`, 1764+84 tok, 2.54s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4131"})`
- agent called `get_received_totals({"po_number": "PO-2025-4131"})`
- agent called `get_vendor_by_name({"name": "Northgate Industrial Supply LLC"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4131", "vendor_id": "V01", "date": "2025-05-15", "currency": "USD", "lines": [{"line_no": 1, "sku": "NG-7720", "description": "Safety goggles, anti-fog", "qty": 15, "unit_price": 6.95}, {"line_no": 2, "sku": "NG-4410", "description": "Nitrile work gloves, box of 100", "qty": 22, "unit_price": 18.4}, {"line_no": 3, "sku": "NG-3305", "description": "Absorbent pads, case", "qty": 9, "unit_price": 42.5}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 7, "2": 11, "3": 4}, "grn_count": 1, "grn_numbers": ["GRN-88330"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V01", "name": "Northgate Industrial Supply LLC", "city": "Columbus, OH", "currency": "USD", "payment_terms": "Net 30", "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "tax_rate": 0.0725, "memory": {"known_aliases": ["Northgate Ind. Supply (a div. of NIS Holdings)", "NIS Holdings LLC", "Northgate Industrial"], "notes": "Invoices under NIS Holdings trade names since 2024 reorg. Split deliveries common."}}
```

**Step 7 — LLM call** (agent: `matcher`, 2222+82 tok, 2.52s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V01", "po_number": "PO-2025-4131", "total": 967.45, "invoice_no": "NIS-2025-410"})`
- agent called `arithmetic_check({"vendor_id": "V01"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (65.40 ~= 65.40).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2363+204 tok, 3.71s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "NIS-2025-410",
  "po_number": "PO-2025-4131",
  "decision": "hold",
  "discrepancies": [
    "PRICE_MISMATCH",
    "QTY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4131 exists in USD for vendor V01, and no duplicate, arithmetic, currency, tax, total, GRN-missing, or bank-change issues were found. However, invoice line SKU NG-7720 bills unit price 7.65 while the PO price is 6.95, which exceeds the 0.5% tolerance, and the billed quantities exceed received quantities on all three lines: 15 vs 7 received for NG-7720, 22 vs 11 for NG-4410, and 9 vs 4 for NG-3305 based on GRN GRN-88330."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH", "QTY_MISMATCH"], "engine_codes": ["PRICE_MISMATCH", "QTY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: CCW-407

**Step 1 — LLM call** (agent: `extractor`, 521+220 tok, 4.78s)
- assistant said:

```
{"invoice_no":"CCW-407","vendor_name":"Cascadia Chemical Works","date":"2025-07-02","po_number":"PO-2025-4132","currency":"USD","lines":[{"sku":"CC-COOL-55","description":"Machine coolant concentrate, 55gal","qty":8,"unit_price":744.50,"amount":5956.00},{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":14,"unit_price":612.00,"amount":8568.00},{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":15,"unit_price":87.40,"amount":1311.00}],"subtotal":15835.00,"tax":1548.43,"total":17383.43,"bank_name":"Meridian Trust Bank","bank_routing":"125000024","bank_account":"6120087745","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-407"}`

**Step 3 — LLM call** (agent: `matcher`, 1718+84 tok, 2.61s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4132"})`
- agent called `get_received_totals({"po_number": "PO-2025-4132"})`
- agent called `get_vendor_by_name({"name": "Cascadia Chemical Works"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4132", "vendor_id": "V04", "date": "2025-04-02", "currency": "USD", "lines": [{"line_no": 1, "sku": "CC-COOL-55", "description": "Machine coolant concentrate, 55gal", "qty": 8, "unit_price": 744.5}, {"line_no": 2, "sku": "CC-IPA-55", "description": "Isopropyl alcohol 99%, 55gal drum", "qty": 14, "unit_price": 612.0}, {"line_no": 3, "sku": "CC-DEG-5", "description": "Industrial degreaser, 5gal", "qty": 15, "unit_price": 87.4}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 8, "2": 14, "3": 15}, "grn_count": 1, "grn_numbers": ["GRN-88331"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V04", "name": "Cascadia Chemical Works", "city": "Tacoma, WA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Puget Sound Trust", "bank_routing": "125000024", "bank_account": "9027481133", "tax_rate": 0.095}
```

**Step 7 — LLM call** (agent: `matcher`, 2127+80 tok, 2.66s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V04", "po_number": "PO-2025-4132", "total": 17383.43, "invoice_no": "CCW-407"})`
- agent called `arithmetic_check({"vendor_id": "V04"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TAX_ERROR", "evidence": "Tax 1548.43 != tax_rate 0.0950 x subtotal 15835.00 = 1504.33 (tolerance $0.02)."}, {"code": "BANK_CHANGE", "evidence": "Remit-to account 6120087745 != vendor master 9027481133 \u2014 verify with vendor before payment."}], "checks_passed": []}
```

**Step 10 — LLM call** (agent: `matcher`, 2327+218 tok, 3.9s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "CCW-407",
  "po_number": "PO-2025-4132",
  "decision": "hold",
  "discrepancies": [
    "TAX_ERROR",
    "BANK_CHANGE"
  ],
  "explanation": "PO PO-2025-4132 exists for vendor V04 in USD, invoice line prices match the PO (744.50, 612.00, 87.40), billed quantities 8/14/15 do not exceed received quantities from GRN-88331, and no duplicate payment was found for invoice CCW-407 or total 17383.43. However, the tax is incorrect: invoice tax 1548.43 does not match the vendor tax rate 0.095 × subtotal 15835.00 = 1504.33, and the remit-to bank account 6120087745 differs from the vendor master account 9027481133 (routing 125000024 matches), so the invoice must be held."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["BANK_CHANGE", "TAX_ERROR"], "engine_codes": ["BANK_CHANGE", "TAX_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`
