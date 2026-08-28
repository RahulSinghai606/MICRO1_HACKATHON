# Agent trajectories — run `agent_v3`


## Case: NIS-2025-101

**Step 1 — LLM call** (agent: `extractor`, 538+243 tok, 3.58s)
- assistant said:

```
{"invoice_no":"NIS-2025-101","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-18","po_number":"PO-2025-4101","currency":"USD","lines":[{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":3,"unit_price":18.40,"amount":55.20},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":7,"unit_price":149.00,"amount":1043.00},{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":15,"unit_price":6.95,"amount":104.25},{"sku":"NG-3305","description":"Absorbent pads, case","qty":16,"unit_price":42.50,"amount":680.00}],"subtotal":1882.45,"tax":136.48,"total":2018.93,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1828+84 tok, 4.21s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4101"})`
- agent called `get_received_totals({"po_number": "PO-2025-4101"})`
- agent called `get_vendor_by_name({"name": "Northgate Industrial Supply LLC"})`

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
{"vendor_id": "V01", "name": "Northgate Industrial Supply LLC", "city": "Columbus, OH", "currency": "USD", "payment_terms": "Net 60", "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "tax_rate": 0.0725}
```

**Step 7 — LLM call** (agent: `matcher`, 2276+83 tok, 2.55s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V01", "po_number": "PO-2025-4101", "total": 2018.93, "invoice_no": "NIS-2025-101"})`
- agent called `arithmetic_check({"vendor_id": "V01"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (136.48 ~= 136.48).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2418+184 tok, 4.5s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"NIS-2025-101","po_number":"PO-2025-4101","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4101 exists for vendor V01 in USD, and all invoiced unit prices match the PO exactly: NG-4410 at 18.40, NG-1180 at 149.00, NG-7720 at 6.95, and NG-3305 at 42.50. GRN totals show full receipt against GRN-88301 with quantities 3, 7, 15, and 16 respectively, matching the billed quantities; arithmetic check passed including tax 136.48, bank details matched vendor master, and no duplicate payment was found for invoice NIS-2025-101 or total 2018.93 on this PO."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: INV-2025-0101

**Step 1 — LLM call** (agent: `extractor`, 446+178 tok, 3.35s)
- assistant said:

```
{"invoice_no":"INV-2025-0101","vendor_name":"Bluefin Packaging Co.","date":"2025-06-25","po_number":"PO-2025-4102","currency":"USD","lines":[{"sku":"BP-450","description":"Foam inserts, custom cut","qty":30,"unit_price":4.15,"amount":124.50},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":39,"unit_price":31.25,"amount":1218.75}],"subtotal":1343.25,"tax":94.03,"total":1437.28,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0101"}`

**Step 3 — LLM call** (agent: `matcher`, 1561+84 tok, 2.6s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4102"})`
- agent called `get_vendor_by_name({"name": "Bluefin Packaging Co."})`
- agent called `get_received_totals({"po_number": "PO-2025-4102"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4102", "vendor_id": "V02", "date": "2025-05-26", "currency": "USD", "lines": [{"line_no": 1, "sku": "BP-450", "description": "Foam inserts, custom cut", "qty": 30, "unit_price": 4.15}, {"line_no": 2, "sku": "BP-201", "description": "Corrugated boxes 18x12x10, bundle 25", "qty": 39, "unit_price": 31.25}], "status": "open"}
```

**Step 5 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V02", "name": "Bluefin Packaging Co.", "city": "Savannah, GA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Coastal Georgia Bank", "bank_routing": "061000104", "bank_account": "7719045512", "tax_rate": 0.07}
```

**Step 6 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 30, "2": 39}, "grn_count": 1, "grn_numbers": ["GRN-88302"]}
```

**Step 7 — LLM call** (agent: `matcher`, 1913+83 tok, 3.08s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V02", "po_number": "PO-2025-4102", "total": 1437.28, "invoice_no": "INV-2025-0101"})`
- agent called `arithmetic_check({"vendor_id": "V02"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (94.03 ~= 94.03).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2055+175 tok, 3.75s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "INV-2025-0101",
  "po_number": "PO-2025-4102",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4102 exists for vendor V02 in USD, and the invoice line prices match the PO exactly: BP-450 at 4.15 and BP-201 at 31.25. GRN-88302 shows full receipt of 30 units on line 1 and 39 units on line 2, matching billed quantities; arithmetic_check found no total or tax errors (tax 94.03 at 7% on subtotal 1343.25, total 1437.28), bank details match the vendor master, and no duplicate payment was found."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: MF/25/101

**Step 1 — LLM call** (agent: `extractor`, 487+182 tok, 2.91s)
- assistant said:

```
{"invoice_no":"MF/25/101","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-07-04","po_number":"PO-2025-4103","currency":"USD","lines":[{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":19,"unit_price":62.75,"amount":1192.25},{"sku":"MF-M8-NUT","description":"Hex nuts M8 zinc, box 1000","qty":11,"unit_price":27.60,"amount":303.60}],"subtotal":1495.85,"tax":89.75,"total":1585.60,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/101"}`

**Step 3 — LLM call** (agent: `matcher`, 1505+87 tok, 2.57s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4103"})`
- agent called `get_received_totals({"po_number": "PO-2025-4103"})`
- agent called `get_vendor_by_name({"name": "MERIDIAN FASTENERS INC."})`

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

**Step 7 — LLM call** (agent: `matcher`, 1864+81 tok, 2.52s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V03", "po_number": "PO-2025-4103", "total": 1585.6, "invoice_no": "MF/25/101"})`
- agent called `arithmetic_check({"vendor_id": "V03"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (89.75 ~= 89.75).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2004+171 tok, 3.71s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "MF/25/101",
  "po_number": "PO-2025-4103",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4103 exists for vendor V03 in USD, and the invoice lines match the PO unit prices exactly: MF-ANC-10 at 62.75 for qty 19 and MF-M8-NUT at 27.60 for qty 11. GRN totals show 19 received on line 1 and 11 on line 2 (GRN-88303), so billed quantities do not exceed receipts; arithmetic_check also passed tax at 89.75 and confirmed the remit-to bank details match vendor master, and payment history returned no duplicates."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: CCW-101

**Step 1 — LLM call** (agent: `extractor`, 489+183 tok, 4.6s)
- assistant said:

```
{"invoice_no":"CCW-101","vendor_name":"Cascadia Chemical Works","date":"2025-06-24","po_number":"PO-2025-4104","currency":"USD","lines":[{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":24,"unit_price":87.40,"amount":2097.60},{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":24,"unit_price":612.00,"amount":14688.00}],"subtotal":16785.60,"tax":1594.63,"total":18380.23,"bank_name":"Puget Sound Trust","bank_routing":"125000024","bank_account":"9027481133","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1575+84 tok, 2.65s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4104"})`
- agent called `get_received_totals({"po_number": "PO-2025-4104"})`
- agent called `get_vendor_by_name({"name": "Cascadia Chemical Works"})`

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

**Step 7 — LLM call** (agent: `matcher`, 1933+80 tok, 2.46s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V04", "po_number": "PO-2025-4104", "total": 18380.23, "invoice_no": "CCW-101"})`
- agent called `arithmetic_check({"vendor_id": "V04"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (1594.63 ~= 1594.63).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2074+176 tok, 3.44s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "CCW-101",
  "po_number": "PO-2025-4104",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4104 exists for vendor V04 in USD, and the invoice matches the PO line prices exactly ($87.40 for CC-DEG-5 and $612.00 for CC-IPA-55). GRN totals show 24 units received on line 1 and 24 on line 2 (GRN-88304), matching the billed quantities; arithmetic_check found no total or tax errors (tax $1,594.63 on subtotal $16,785.60 at 9.5%), bank details match vendor master, and no duplicate payment or invoice number was found."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: HEC-2025-101

**Step 1 — LLM call** (agent: `extractor`, 481+216 tok, 3.64s)
- assistant said:

```
{"invoice_no":"HEC-2025-101","vendor_name":"Helios Electrical Components","date":"2025-06-02","po_number":"PO-2025-4105","currency":"USD","lines":[{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":37,"unit_price":9.85,"amount":364.45},{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":20,"unit_price":14.2,"amount":284.00},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":25,"unit_price":96.3,"amount":2407.50}],"subtotal":3055.95,"tax":262.81,"total":3318.76,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1643+83 tok, 2.59s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4105"})`
- agent called `get_received_totals({"po_number": "PO-2025-4105"})`
- agent called `get_vendor_by_name({"name": "Helios Electrical Components"})`

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

**Step 7 — LLM call** (agent: `matcher`, 2048+83 tok, 2.93s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V05", "po_number": "PO-2025-4105", "total": 3318.76, "invoice_no": "HEC-2025-101"})`
- agent called `arithmetic_check({"vendor_id": "V05"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (262.81 ~= 262.81).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2190+175 tok, 3.53s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"HEC-2025-101","po_number":"PO-2025-4105","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4105 exists for vendor V05 in USD, and all invoice line prices match the PO exactly: HE-CB-20 at 9.85, HE-REL-24 at 14.2, and HE-PSU-24 at 96.3. GRN totals on GRN-88305 fully support the billed quantities (37, 20, and 25 respectively), arithmetic_check found no tax/total errors and confirmed tax 262.81, bank details match the vendor master, and no duplicate was found in payment history for invoice HEC-2025-101 or total 3318.76."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: ALS-INV-101

**Step 1 — LLM call** (agent: `extractor`, 525+230 tok, 3.49s)
- assistant said:

```
{"invoice_no":"ALS-INV-101","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-06","po_number":"PO-2025-4106","currency":"USD","lines":[{"sku":"AL-FUEL","description":"Fuel surcharge","qty":8,"unit_price":63.75,"amount":510.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":26,"unit_price":18.50,"amount":481.00},{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":19,"unit_price":425.00,"amount":8075.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":31,"unit_price":45.00,"amount":1395.00}],"subtotal":10461.00,"tax":0.00,"total":10461.00,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1799+85 tok, 4.5s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4106"})`
- agent called `get_received_totals({"po_number": "PO-2025-4106"})`
- agent called `get_vendor_by_name({"name": "AURIGA LOGISTICS SERVICES"})`

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

**Step 7 — LLM call** (agent: `matcher`, 2233+79 tok, 2.88s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V06", "po_number": "PO-2025-4106", "total": 10461, "invoice_no": "ALS-INV-101"})`
- agent called `arithmetic_check({"vendor_id": "V06"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2371+189 tok, 3.36s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"ALS-INV-101","po_number":"PO-2025-4106","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4106 exists for vendor V06 in USD, and all invoice line prices match the PO exactly: AL-FUEL 8 @ 63.75, AL-WHS-P 26 @ 18.50, AL-LTL-STD 19 @ 425.00, and AL-LIFT 31 @ 45.00. GRN totals from GRN-88306 fully support the billed quantities (8, 26, 19, and 31 respectively), arithmetic checks passed including subtotal 10461.00, tax 0.00 at tax rate 0.0, and total 10461.00, the remit-to bank matches the vendor master, and no duplicate payment was found."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: SOI-25-101

**Step 1 — LLM call** (agent: `extractor`, 508+208 tok, 3.35s)
- assistant said:

```
{"invoice_no":"SOI-25-101","vendor_name":"Stellar Office Interiors","date":"2025-06-06","po_number":"PO-2025-4107","currency":"USD","lines":[{"sku":"SO-MON-ARM","description":"Dual monitor arm","qty":6,"unit_price":74.25,"amount":445.50},{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":40,"unit_price":189.00,"amount":7560.00},{"sku":"SO-DSK-60","description":"Sit-stand desk 60in","qty":12,"unit_price":415.00,"amount":4980.00}],"subtotal":12985.50,"tax":1051.83,"total":14037.33,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1692+83 tok, 2.86s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4107"})`
- agent called `get_received_totals({"po_number": "PO-2025-4107"})`
- agent called `get_vendor_by_name({"name": "Stellar Office Interiors"})`

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

**Step 7 — LLM call** (agent: `matcher`, 2086+82 tok, 2.47s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V07", "po_number": "PO-2025-4107", "total": 14037.33, "invoice_no": "SOI-25-101"})`
- agent called `arithmetic_check({"vendor_id": "V07"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (1051.83 ~= 1051.83).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2229+167 tok, 4.51s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"SOI-25-101","po_number":"PO-2025-4107","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4107 exists for vendor V07 in USD, and all invoice line prices match the PO exactly: SO-MON-ARM 6 @ 74.25, SO-CHR-T2 40 @ 189.00, and SO-DSK-60 12 @ 415.00. GRN totals show full receipt against GRN-88307 (6, 40, and 12 respectively), arithmetic check passed including tax 1,051.83 and total 14,037.33, bank details match the vendor master, and no duplicate payment or invoice number was found."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: GP-101

**Step 1 — LLM call** (agent: `extractor`, 479+214 tok, 3.8s)
- assistant said:

```
{"invoice_no":"GP-101","vendor_name":"Granite Peak Safety Gear","date":"2025-07-13","po_number":"PO-2025-4108","currency":"USD","lines":[{"sku":"GP-EAR-200","description":"Ear plugs, box 200 pr","qty":22,"unit_price":38.90,"amount":855.80},{"sku":"GP-VIS-XL","description":"Hi-vis vests XL, pack 10","qty":5,"unit_price":84.50,"amount":422.50},{"sku":"GP-HH-CL2","description":"Hard hats class E, box 20","qty":16,"unit_price":196.00,"amount":3136.00}],"subtotal":4414.30,"tax":264.86,"total":4679.16,"bank_name":"Sawtooth Community Bank","bank_routing":"123103729","bank_account":"2290156841","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1642+84 tok, 2.61s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4108"})`
- agent called `get_received_totals({"po_number": "PO-2025-4108"})`
- agent called `get_vendor_by_name({"name": "Granite Peak Safety Gear"})`

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

**Step 7 — LLM call** (agent: `matcher`, 2049+79 tok, 2.49s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V08", "po_number": "PO-2025-4108", "total": 4679.16, "invoice_no": "GP-101"})`
- agent called `arithmetic_check({"vendor_id": "V08"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (264.86 ~= 264.86).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2187+143 tok, 4.67s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"GP-101","po_number":"PO-2025-4108","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4108 exists for vendor V08 in USD, and all billed line prices match the PO exactly: 38.90, 84.50, and 196.00. GRN-88308 shows received quantities of 22, 5, and 16 respectively, matching the billed quantities; arithmetic_check also confirmed tax 264.86 at 6% and matching remit-to bank details, and payment history found no duplicate for invoice GP-101 or total 4679.16."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: VPL-2025-101

**Step 1 — LLM call** (agent: `extractor`, 506+232 tok, 3.85s)
- assistant said:

```
{"invoice_no":"VPL-2025-101","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-06-09","po_number":"PO-2025-4109","currency":"EUR","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":15,"unit_price":21.40,"amount":321.00},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":33,"unit_price":9.60,"amount":316.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":27,"unit_price":340.00,"amount":9180.00}],"subtotal":9817.80,"tax":1865.38,"total":11683.18,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1672+88 tok, 2.52s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4109"})`
- agent called `get_received_totals({"po_number": "PO-2025-4109"})`
- agent called `get_vendor_by_name({"name": "VIREO PRINT & LABEL GMBH"})`

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
{"vendor_id": "V09", "name": "Vireo Print & Label GmbH", "city": "Hamburg, DE", "currency": "EUR", "payment_terms": "Net 60", "bank_name": "Hansa Handelsbank", "bank_routing": "DE44 5001 0517", "bank_account": "5407 3249 31", "tax_rate": 0.19}
```

**Step 7 — LLM call** (agent: `matcher`, 2094+83 tok, 2.52s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V09", "po_number": "PO-2025-4109", "total": 11683.18, "invoice_no": "VPL-2025-101"})`
- agent called `arithmetic_check({"vendor_id": "V09"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (1865.38 ~= 1865.38).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2238+176 tok, 3.62s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "VPL-2025-101",
  "po_number": "PO-2025-4109",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4109 exists for vendor V09 in EUR, and the invoice line prices match the PO exactly: 21.4, 9.6, and 340.0. GRN totals on GRN-88309 fully cover the billed quantities (15, 33, and 27), arithmetic_check found no arithmetic or tax errors (tax 1865.38 at 19% is valid), the remit-to bank details match the vendor master, and payment history shows no duplicate for invoice VPL-2025-101 or total 11683.18."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: AMT-101

**Step 1 — LLM call** (agent: `extractor`, 485+181 tok, 3.18s)
- assistant said:

```
{"invoice_no":"AMT-101","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-19","po_number":"PO-2025-4110","currency":"USD","lines":[{"sku":"AM-VIS-6","description":"Machine vise 6in","qty":37,"unit_price":289.00,"amount":10693.00},{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":36,"unit_price":412.60,"amount":14853.60}],"subtotal":25546.60,"tax":0.00,"total":25546.60,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1505+85 tok, 2.95s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4110"})`
- agent called `get_received_totals({"po_number": "PO-2025-4110"})`
- agent called `get_vendor_by_name({"name": "Ashford Machine Tools Ltd."})`

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

**Step 7 — LLM call** (agent: `matcher`, 1863+80 tok, 2.53s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V10", "po_number": "PO-2025-4110", "total": 25546.6, "invoice_no": "AMT-101"})`
- agent called `arithmetic_check({"vendor_id": "V10"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2002+188 tok, 4.72s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "AMT-101",
  "po_number": "PO-2025-4110",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4110 exists for vendor V10 in USD, and the invoice lines match the PO exactly: AM-VIS-6 billed 37 @ 289.00 vs PO 289.00, and AM-CHK-125 billed 36 @ 412.60 vs PO 412.60. GRN totals show receipt of 37 and 36 respectively under GRN-88310, arithmetic checks passed including subtotal 25,546.60, tax 0.00 at 0.0% tax rate, total 25,546.60, the remit-to bank details match vendor master, and no duplicate payment record was found."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: NIS-2025-104

**Step 1 — LLM call** (agent: `extractor`, 527+219 tok, 3.85s)
- assistant said:

```
{"invoice_no":"NIS-2025-104","vendor_name":"Northgate Ind. Supply (a div. of NIS Holdings)","date":"2025-06-05","po_number":"PO-2025-4111","currency":"USD","lines":[{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":34,"unit_price":149.00,"amount":5066.00},{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":33,"unit_price":18.40,"amount":607.20},{"sku":"NG-3305","description":"Absorbent pads, case","qty":7,"unit_price":42.50,"amount":297.50}],"subtotal":5970.70,"tax":432.88,"total":6403.58,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1841+93 tok, 2.84s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4111"})`
- agent called `get_received_totals({"po_number": "PO-2025-4111"})`
- agent called `get_vendor_by_name({"name": "Northgate Ind. Supply (a div. of NIS Holdings)"})`

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
{"error": "no vendor matches 'Northgate Ind. Supply (a div. of NIS Holdings)'"}
```

**Step 7 — LLM call** (agent: `matcher`, 2200+83 tok, 2.6s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V01", "po_number": "PO-2025-4111", "total": 6403.58, "invoice_no": "NIS-2025-104"})`
- agent called `arithmetic_check({"vendor_id": "V01"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (432.88 ~= 432.88).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2342+183 tok, 3.83s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"NIS-2025-104","po_number":"PO-2025-4111","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4111 exists for vendor V01 in USD, and the invoice line prices match the PO exactly: NG-1180 at 149.00, NG-4410 at 18.40, and NG-3305 at 42.50. Received quantities across GRNs GRN-88311 and GRN-88312 total 34, 33, and 7 respectively, matching the billed quantities exactly; arithmetic_check also confirmed tax 432.88 and matching bank details, and no duplicate payment was found for vendor V01, PO-2025-4111, total 6403.58, or invoice number NIS-2025-104."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: HEC-2025-104

**Step 1 — LLM call** (agent: `extractor`, 517+256 tok, 3.88s)
- assistant said:

```
{"invoice_no":"HEC-2025-104","vendor_name":"Helios Electrical Components","date":"2025-06-22","po_number":"PO-2025-4112","currency":"USD","lines":[{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":26,"unit_price":14.20,"amount":369.20},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":26,"unit_price":118.00,"amount":3068.00},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":40,"unit_price":96.30,"amount":3852.00},{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":31,"unit_price":9.85,"amount":305.35}],"subtotal":7594.55,"tax":653.14,"total":8247.69,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1790+83 tok, 2.88s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4112"})`
- agent called `get_received_totals({"po_number": "PO-2025-4112"})`
- agent called `get_vendor_by_name({"name": "Helios Electrical Components"})`

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

**Step 7 — LLM call** (agent: `matcher`, 2249+83 tok, 2.52s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V05", "po_number": "PO-2025-4112", "total": 8247.69, "invoice_no": "HEC-2025-104"})`
- agent called `arithmetic_check({"vendor_id": "V05"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (653.14 ~= 653.13).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2391+152 tok, 3.49s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"HEC-2025-104","po_number":"PO-2025-4112","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4112 exists for vendor V05 in USD, and all invoice line unit prices match the PO (14.20, 118.00, 96.30, 9.85). GRN totals show full receipt against all four PO lines (26, 26, 40, 31), arithmetic check passed including tax 653.14 within tolerance of 8.6% on subtotal 7,594.55, bank details match the vendor master, and no duplicate payment or invoice number was found."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": [], "engine_codes": [], "matcher_decision": "approve", "engine_decision": "approve"}`


## Case: MF/25/104

**Step 1 — LLM call** (agent: `extractor`, 551+257 tok, 3.81s)
- assistant said:

```
{"invoice_no":"MF/25/104","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-07-17","po_number":"PO-2025-4113","currency":"USD","lines":[{"sku":"MF-M8-50","description":"Hex bolts M8x50 zinc, box 500","qty":9,"unit_price":49.28,"amount":443.52},{"sku":"MF-W-8","description":"Flat washers 8mm, box 1000","qty":20,"unit_price":15.30,"amount":306.00},{"sku":"MF-M8-NUT","description":"Hex nuts M8 zinc, box 1000","qty":29,"unit_price":27.60,"amount":800.40},{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":12,"unit_price":62.75,"amount":753.00}],"subtotal":2302.92,"tax":138.18,"total":2441.10,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/104"}`

**Step 3 — LLM call** (agent: `matcher`, 1791+87 tok, 2.68s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4113"})`
- agent called `get_received_totals({"po_number": "PO-2025-4113"})`
- agent called `get_vendor_by_name({"name": "MERIDIAN FASTENERS INC."})`

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

**Step 7 — LLM call** (agent: `matcher`, 2256+81 tok, 2.66s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V03", "po_number": "PO-2025-4113", "total": 2441.1, "invoice_no": "MF/25/104"})`
- agent called `arithmetic_check({"vendor_id": "V03"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (138.18 ~= 138.18).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2396+158 tok, 3.58s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"MF/25/104","po_number":"PO-2025-4113","decision":"hold","discrepancies":["PRICE_MISMATCH"],"explanation":"PO PO-2025-4113 exists in USD and has GRN GRN-88314 with received quantities matching the billed quantities on all four lines (9, 20, 29, and 12 respectively). However, line 1 SKU MF-M8-50 is billed at $49.28 versus the PO unit price of $44.00, which exceeds the 0.5% tolerance; arithmetic, tax ($138.18 at 6% of $2,302.92), bank details, currency, and duplicate checks all passed."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH"], "engine_codes": ["PRICE_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: SOI-25-104

**Step 1 — LLM call** (agent: `extractor`, 475+171 tok, 3.44s)
- assistant said:

```
{"invoice_no":"SOI-25-104","vendor_name":"Stellar Office Interiors","date":"2025-06-12","po_number":"PO-2025-4114","currency":"USD","lines":[{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":21,"unit_price":204.12,"amount":4286.52},{"sku":"SO-MON-ARM","description":"Dual monitor arm","qty":34,"unit_price":74.25,"amount":2524.5}],"subtotal":6811.02,"tax":551.69,"total":7362.71,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1550+83 tok, 2.65s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4114"})`
- agent called `get_received_totals({"po_number": "PO-2025-4114"})`
- agent called `get_vendor_by_name({"name": "Stellar Office Interiors"})`

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

**Step 7 — LLM call** (agent: `matcher`, 1893+82 tok, 2.82s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V07", "po_number": "PO-2025-4114", "total": 7362.71, "invoice_no": "SOI-25-104"})`
- agent called `arithmetic_check({"vendor_id": "V07"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (551.69 ~= 551.69).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2034+160 tok, 3.2s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"SOI-25-104","po_number":"PO-2025-4114","decision":"hold","discrepancies":["PRICE_MISMATCH"],"explanation":"PO PO-2025-4114 exists, GRN GRN-88315 shows full receipt of 21 units on line 1 and 34 units on line 2, invoice currency is USD like the PO, bank details match vendor V07, arithmetic checks passed, and no duplicate payment was found. However, line SKU SO-CHR-T2 is billed at 204.12 versus the PO unit price of 189.00, which exceeds the 0.5% price tolerance; line SKU SO-MON-ARM matches at 74.25."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH"], "engine_codes": ["PRICE_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: AMT-104

**Step 1 — LLM call** (agent: `extractor`, 485+181 tok, 3.57s)
- assistant said:

```
{"invoice_no":"AMT-104","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-27","po_number":"PO-2025-4115","currency":"USD","lines":[{"sku":"AM-END-12","description":"End mill 12mm carbide","qty":22,"unit_price":78.43,"amount":1725.46},{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":33,"unit_price":412.60,"amount":13615.80}],"subtotal":15341.26,"tax":0.00,"total":15341.26,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1504+85 tok, 3.02s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4115"})`
- agent called `get_received_totals({"po_number": "PO-2025-4115"})`
- agent called `get_vendor_by_name({"name": "Ashford Machine Tools Ltd."})`

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

**Step 7 — LLM call** (agent: `matcher`, 1862+80 tok, 3.14s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V10", "po_number": "PO-2025-4115", "total": 15341.26, "invoice_no": "AMT-104"})`
- agent called `arithmetic_check({"vendor_id": "V10"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2001+185 tok, 4.02s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "AMT-104",
  "po_number": "PO-2025-4115",
  "decision": "hold",
  "discrepancies": [
    "PRICE_MISMATCH"
  ],
  "explanation": "PO PO-2025-4115 exists for vendor V10 in USD, and GRN-88316 shows full receipt of 22 units for line 1 and 33 units for line 2, so there is no quantity or receipt issue. However, invoice line SKU AM-END-12 bills 22 units at 78.43 while the PO unit price is 68.20, which exceeds the 0.5% tolerance; line 2 matches at 412.60. Arithmetic, tax (0.00 at 0.0%), bank details, currency, and duplicate checks all passed."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH"], "engine_codes": ["PRICE_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: INV-2025-0104

**Step 1 — LLM call** (agent: `extractor`, 473+210 tok, 3.27s)
- assistant said:

```
{"invoice_no":"INV-2025-0104","vendor_name":"Bluefin Packaging Co.","date":"2025-06-25","po_number":"PO-2025-4116","currency":"USD","lines":[{"sku":"BP-115","description":"Stretch wrap roll 80ga","qty":38,"unit_price":12.80,"amount":486.40},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":7,"unit_price":31.25,"amount":218.75},{"sku":"BP-330","description":"Packing tape, case of 36","qty":7,"unit_price":58.90,"amount":412.30}],"subtotal":1117.45,"tax":78.22,"total":1195.67,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0104"}`

**Step 3 — LLM call** (agent: `matcher`, 1692+84 tok, 2.64s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4116"})`
- agent called `get_vendor_by_name({"name": "Bluefin Packaging Co."})`
- agent called `get_received_totals({"po_number": "PO-2025-4116"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4116", "vendor_id": "V02", "date": "2025-06-16", "currency": "USD", "lines": [{"line_no": 1, "sku": "BP-115", "description": "Stretch wrap roll 80ga", "qty": 38, "unit_price": 12.8}, {"line_no": 2, "sku": "BP-201", "description": "Corrugated boxes 18x12x10, bundle 25", "qty": 7, "unit_price": 31.25}, {"line_no": 3, "sku": "BP-330", "description": "Packing tape, case of 36", "qty": 7, "unit_price": 58.9}], "status": "open"}
```

**Step 5 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V02", "name": "Bluefin Packaging Co.", "city": "Savannah, GA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Coastal Georgia Bank", "bank_routing": "061000104", "bank_account": "7719045512", "tax_rate": 0.07}
```

**Step 6 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 22, "2": 4, "3": 4}, "grn_count": 1, "grn_numbers": ["GRN-88317"]}
```

**Step 7 — LLM call** (agent: `matcher`, 2092+83 tok, 2.54s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V02", "po_number": "PO-2025-4116", "total": 1195.67, "invoice_no": "INV-2025-0104"})`
- agent called `arithmetic_check({"vendor_id": "V02"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (78.22 ~= 78.22).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2234+174 tok, 4.08s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "INV-2025-0104",
  "po_number": "PO-2025-4116",
  "decision": "hold",
  "discrepancies": [
    "QTY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4116 exists for vendor V02 in USD, invoice prices match the PO on all three lines, arithmetic passed, bank details match vendor master, and no duplicate payment was found. However, billed quantities exceed received quantities on every line: BP-115 billed 38 vs received 22, BP-201 billed 7 vs received 4, and BP-330 billed 7 vs received 4 based on GRN GRN-88317, so the invoice must be held for QTY_MISMATCH."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["QTY_MISMATCH"], "engine_codes": ["QTY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: HEC-2025-107

**Step 1 — LLM call** (agent: `extractor`, 517+256 tok, 3.65s)
- assistant said:

```
{"invoice_no":"HEC-2025-107","vendor_name":"Helios Electrical Components","date":"2025-06-23","po_number":"PO-2025-4117","currency":"USD","lines":[{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":18,"unit_price":14.20,"amount":255.60},{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":35,"unit_price":9.85,"amount":344.75},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":40,"unit_price":96.30,"amount":3852.00},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":29,"unit_price":118.00,"amount":3422.00}],"subtotal":7874.35,"tax":677.19,"total":8551.54,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1790+83 tok, 2.54s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4117"})`
- agent called `get_received_totals({"po_number": "PO-2025-4117"})`
- agent called `get_vendor_by_name({"name": "Helios Electrical Components"})`

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

**Step 7 — LLM call** (agent: `matcher`, 2249+83 tok, 2.75s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V05", "po_number": "PO-2025-4117", "total": 8551.54, "invoice_no": "HEC-2025-107"})`
- agent called `arithmetic_check({"vendor_id": "V05"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (677.19 ~= 677.19).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2391+188 tok, 3.81s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"HEC-2025-107","po_number":"PO-2025-4117","decision":"hold","discrepancies":["QTY_MISMATCH"],"explanation":"PO PO-2025-4117 exists for vendor V05 in USD, and the invoice unit prices match the PO (14.20, 9.85, 96.30, 118.00). Arithmetic check passed, tax 677.19 matches the expected amount, bank details match the vendor master, and no duplicate payment was found. However, billed quantities exceed received quantities on every line: line 1 billed 18 vs received 10, line 2 billed 35 vs 21, line 3 billed 40 vs 24, and line 4 billed 29 vs 17 based on GRN GRN-88318, so the invoice must be held."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["QTY_MISMATCH"], "engine_codes": ["QTY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: GP-104

**Step 1 — LLM call** (agent: `extractor`, 480+213 tok, 3.48s)
- assistant said:

```
{"invoice_no":"GP-104","vendor_name":"Granite Peak Safety Gear","date":"2025-06-03","po_number":"PO-2025-4118","currency":"USD","lines":[{"sku":"GP-EAR-200","description":"Ear plugs, box 200 pr","qty":30,"unit_price":38.90,"amount":1167.00},{"sku":"GP-BOOT-10","description":"Steel toe boots size 10","qty":35,"unit_price":112.00,"amount":3920.00},{"sku":"GP-VIS-XL","description":"Hi-vis vests XL, pack 10","qty":30,"unit_price":84.50,"amount":2535.00}],"subtotal":7622.00,"tax":457.32,"total":8079.32,"bank_name":"Sawtooth Community Bank","bank_routing":"123103729","bank_account":"2290156841","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1637+84 tok, 2.66s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4118"})`
- agent called `get_received_totals({"po_number": "PO-2025-4118"})`
- agent called `get_vendor_by_name({"name": "Granite Peak Safety Gear"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4118", "vendor_id": "V08", "date": "2025-04-08", "currency": "USD", "lines": [{"line_no": 1, "sku": "GP-EAR-200", "description": "Ear plugs, box 200 pr", "qty": 30, "unit_price": 38.9}, {"line_no": 2, "sku": "GP-BOOT-10", "description": "Steel toe boots size 10", "qty": 35, "unit_price": 112.0}, {"line_no": 3, "sku": "GP-VIS-XL", "description": "Hi-vis vests XL, pack 10", "qty": 30, "unit_price": 84.5}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 18, "2": 21, "3": 18}, "grn_count": 1, "grn_numbers": ["GRN-88319"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V08", "name": "Granite Peak Safety Gear", "city": "Boise, ID", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Sawtooth Community Bank", "bank_routing": "123103729", "bank_account": "2290156841", "tax_rate": 0.06}
```

**Step 7 — LLM call** (agent: `matcher`, 2041+79 tok, 3.03s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V08", "po_number": "PO-2025-4118", "total": 8079.32, "invoice_no": "GP-104"})`
- agent called `arithmetic_check({"vendor_id": "V08"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (457.32 ~= 457.32).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2179+184 tok, 3.48s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "GP-104",
  "po_number": "PO-2025-4118",
  "decision": "hold",
  "discrepancies": [
    "QTY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4118 exists for vendor V08 in USD, and the invoice unit prices match the PO (38.90, 112.00, 84.50). However, billed quantities exceed received quantities on all lines: line 1 billed 30 vs received 18, line 2 billed 35 vs received 21, and line 3 billed 30 vs received 18 from GRN-88319. Arithmetic, tax (457.32 at 6%), bank details, currency, and duplicate screening all passed, so the invoice must be held for the quantity mismatch."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["QTY_MISMATCH"], "engine_codes": ["QTY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: CCW-104

**Step 1 — LLM call** (agent: `extractor`, 518+218 tok, 3.31s)
- assistant said:

```
{"invoice_no":"CCW-104","vendor_name":"Cascadia Chemical Works","date":"2025-06-28","po_number":"PO-2025-4119","currency":"USD","lines":[{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":2,"unit_price":612.00,"amount":1224.00},{"sku":"CC-COOL-55","description":"Machine coolant concentrate, 55gal","qty":6,"unit_price":744.50,"amount":4467.00},{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":5,"unit_price":87.40,"amount":437.00}],"subtotal":6128.00,"tax":582.16,"total":6710.16,"bank_name":"Puget Sound Trust","bank_routing":"125000024","bank_account":"9027481133","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1574+84 tok, 2.69s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4119"})`
- agent called `get_received_totals({"po_number": "PO-2025-4119"})`
- agent called `get_vendor_by_name({"name": "Cascadia Chemical Works"})`

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

**Step 7 — LLM call** (agent: `matcher`, 1955+80 tok, 2.54s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V04", "po_number": "PO-2025-4119", "total": 6710.16, "invoice_no": "CCW-104"})`
- agent called `arithmetic_check({"vendor_id": "V04"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (582.16 ~= 582.16).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2094+206 tok, 3.69s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "CCW-104",
  "po_number": "PO-2025-4119",
  "decision": "hold",
  "discrepancies": [
    "GRN_MISSING",
    "QTY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4119 exists for vendor V04 and the invoice matches the PO on currency (USD), line unit prices (612.00, 744.50, 87.40), bank details, and arithmetic; no duplicate payment was found for invoice CCW-104 or total 6710.16. However, no GRNs exist for this PO, so received quantity is effectively 0 for all lines, while the invoice bills 2 units of CC-IPA-55, 6 units of CC-COOL-55, and 5 units of CC-DEG-5, creating both GRN_MISSING and QTY_MISMATCH."
}
```

**Step 11 — verifier**: `{"agree": false, "matcher_codes": ["GRN_MISSING", "QTY_MISMATCH"], "engine_codes": ["GRN_MISSING"], "matcher_decision": "hold", "engine_decision": "hold"}`

**Step 12 — LLM call** (agent: `matcher`, 1750+84 tok, 2.82s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4119"})`
- agent called `get_received_totals({"po_number": "PO-2025-4119"})`
- agent called `get_vendor_by_name({"name": "Cascadia Chemical Works"})`

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

**Step 16 — LLM call** (agent: `matcher`, 2131+80 tok, 2.37s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V04", "po_number": "PO-2025-4119", "total": 6710.16, "invoice_no": "CCW-104"})`
- agent called `arithmetic_check({"vendor_id": "V04"})`

**Step 17 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 18 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (582.16 ~= 582.16).", "Remit-to bank details match vendor master."]}
```

**Step 19 — LLM call** (agent: `matcher`, 2270+146 tok, 3.82s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "CCW-104",
  "po_number": "PO-2025-4119",
  "decision": "hold",
  "discrepancies": ["GRN_MISSING"],
  "explanation": "PO PO-2025-4119 exists for vendor V04 in USD, and the invoice line prices match the PO exactly (612.00, 744.50, and 87.40). No goods receipt notes exist for this PO, so GRN_MISSING applies; arithmetic checks passed including tax 582.16 at the 9.5% rate, bank details match the vendor master, and no duplicate payment was found."
}
```

**Step 20 — verifier**: `{"agree": true, "matcher_codes": ["GRN_MISSING"], "engine_codes": ["GRN_MISSING"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: ALS-INV-104

**Step 1 — LLM call** (agent: `extractor`, 502+202 tok, 3.54s)
- assistant said:

```
{"invoice_no":"ALS-INV-104","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-08","po_number":"PO-2025-4120","currency":"USD","lines":[{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":19,"unit_price":425.00,"amount":8075.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":33,"unit_price":45.00,"amount":1485.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":15,"unit_price":18.50,"amount":277.50}],"subtotal":9837.50,"tax":0.00,"total":9837.50,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1540+146 tok, 3.02s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4120"})`
- agent called `get_received_totals({"po_number": "PO-2025-4120"})`
- agent called `get_vendor_by_name({"name": "AURIGA LOGISTICS SERVICES"})`
- agent called `arithmetic_check({"vendor_id": "V06"})`
- agent called `search_payments({"vendor_id": "V06", "po_number": "PO-2025-4120", "total": 9837.5, "invoice_no": "ALS-INV-104"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4120", "vendor_id": "V06", "date": "2025-06-05", "currency": "USD", "lines": [{"line_no": 1, "sku": "AL-LTL-STD", "description": "LTL freight, standard lane", "qty": 19, "unit_price": 425.0}, {"line_no": 2, "sku": "AL-LIFT", "description": "Liftgate service", "qty": 33, "unit_price": 45.0}, {"line_no": 3, "sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 15, "unit_price": 18.5}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-4120"}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V06", "name": "Auriga Logistics Services", "city": "Memphis, TN", "currency": "USD", "payment_terms": "Net 30", "bank_name": "River City Bank", "bank_routing": "084000026", "bank_account": "6650371928", "tax_rate": 0.0}
```

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — LLM call** (agent: `matcher`, 2010+195 tok, 3.79s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "ALS-INV-104",
  "po_number": "PO-2025-4120",
  "decision": "hold",
  "discrepancies": [
    "GRN_MISSING",
    "QTY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4120 exists for vendor V06 and the invoice matches the PO on currency (USD), line unit prices (425.00, 45.00, 18.50), arithmetic, and bank details. However, no GRNs exist for this PO, so billed quantities of 19 AL-LTL-STD, 33 AL-LIFT, and 15 AL-WHS-P each exceed total received quantity of 0, creating GRN_MISSING and QTY_MISMATCH. No duplicate payment was found for invoice ALS-INV-104 or total 9,837.50."
}
```

**Step 10 — verifier**: `{"agree": false, "matcher_codes": ["GRN_MISSING", "QTY_MISMATCH"], "engine_codes": ["GRN_MISSING"], "matcher_decision": "hold", "engine_decision": "hold"}`

**Step 11 — LLM call** (agent: `matcher`, 1712+85 tok, 2.58s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4120"})`
- agent called `get_received_totals({"po_number": "PO-2025-4120"})`
- agent called `get_vendor_by_name({"name": "AURIGA LOGISTICS SERVICES"})`

**Step 12 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4120", "vendor_id": "V06", "date": "2025-06-05", "currency": "USD", "lines": [{"line_no": 1, "sku": "AL-LTL-STD", "description": "LTL freight, standard lane", "qty": 19, "unit_price": 425.0}, {"line_no": 2, "sku": "AL-LIFT", "description": "Liftgate service", "qty": 33, "unit_price": 45.0}, {"line_no": 3, "sku": "AL-WHS-P", "description": "Warehouse handling, per pallet", "qty": 15, "unit_price": 18.5}], "status": "open"}
```

**Step 13 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-4120"}
```

**Step 14 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V06", "name": "Auriga Logistics Services", "city": "Memphis, TN", "currency": "USD", "payment_terms": "Net 30", "bank_name": "River City Bank", "bank_routing": "084000026", "bank_account": "6650371928", "tax_rate": 0.0}
```

**Step 15 — LLM call** (agent: `matcher`, 2075+81 tok, 2.62s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V06", "po_number": "PO-2025-4120", "total": 9837.5, "invoice_no": "ALS-INV-104"})`
- agent called `arithmetic_check({"vendor_id": "V06"})`

**Step 16 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 17 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 18 — LLM call** (agent: `matcher`, 2215+181 tok, 3.61s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "ALS-INV-104",
  "po_number": "PO-2025-4120",
  "decision": "hold",
  "discrepancies": [
    "GRN_MISSING"
  ],
  "explanation": "PO PO-2025-4120 exists for vendor V06 and matches the invoice in USD, with line prices matching the PO (AL-LTL-STD 425.00, AL-LIFT 45.00, AL-WHS-P 18.50). However, no goods receipt notes exist for PO-2025-4120, so GRN_MISSING applies. Duplicate search found no prior paid invoice matching invoice ALS-INV-104 or the same vendor/PO/total 9,837.50, and the tax and remit-to bank details were verified as correct."
}
```

**Step 19 — verifier**: `{"agree": true, "matcher_codes": ["GRN_MISSING"], "engine_codes": ["GRN_MISSING"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: INV-2025-0107

**Step 1 — LLM call** (agent: `extractor`, 475+211 tok, 3.47s)
- assistant said:

```
{"invoice_no":"INV-2025-0107","vendor_name":"Bluefin Packaging Co.","date":"2025-07-28","po_number":"PO-2025-4121","currency":"USD","lines":[{"sku":"BP-450","description":"Foam inserts, custom cut","qty":8,"unit_price":4.15,"amount":33.20},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":29,"unit_price":31.25,"amount":906.25},{"sku":"BP-330","description":"Packing tape, case of 36","qty":24,"unit_price":58.90,"amount":1413.60}],"subtotal":2353.05,"tax":164.71,"total":2517.76,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0107"}`

**Step 3 — LLM call** (agent: `matcher`, 1693+84 tok, 2.82s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4121"})`
- agent called `get_vendor_by_name({"name": "Bluefin Packaging Co."})`
- agent called `get_received_totals({"po_number": "PO-2025-4121"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4121", "vendor_id": "V02", "date": "2025-05-14", "currency": "USD", "lines": [{"line_no": 1, "sku": "BP-450", "description": "Foam inserts, custom cut", "qty": 8, "unit_price": 4.15}, {"line_no": 2, "sku": "BP-201", "description": "Corrugated boxes 18x12x10, bundle 25", "qty": 29, "unit_price": 31.25}, {"line_no": 3, "sku": "BP-330", "description": "Packing tape, case of 36", "qty": 24, "unit_price": 58.9}], "status": "open"}
```

**Step 5 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V02", "name": "Bluefin Packaging Co.", "city": "Savannah, GA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Coastal Georgia Bank", "bank_routing": "061000104", "bank_account": "7719045512", "tax_rate": 0.07}
```

**Step 6 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 8, "2": 29, "3": 24}, "grn_count": 1, "grn_numbers": ["GRN-88320"]}
```

**Step 7 — LLM call** (agent: `matcher`, 2093+83 tok, 2.74s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V02", "po_number": "PO-2025-4121", "total": 2517.76, "invoice_no": "INV-2025-0107"})`
- agent called `arithmetic_check({"vendor_id": "V02"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": [{"invoice_no": "INV-25-107", "vendor_id": "V02", "po_number": "PO-2025-4121", "amount": 2517.76, "currency": "USD", "paid_date": "2025-06-14", "match_reasons": ["same vendor + PO + amount already paid"]}]}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (164.71 ~= 164.71).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2309+170 tok, 3.62s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "INV-2025-0107",
  "po_number": "PO-2025-4121",
  "decision": "reject",
  "discrepancies": [
    "DUPLICATE"
  ],
  "explanation": "PO PO-2025-4121 exists for vendor V02 in USD, all three billed quantities match received quantities on GRN-88320 (8, 29, and 24), arithmetic passed, and the remit-to bank details match the vendor master. However, payment history already shows a paid invoice for vendor V02 on the same PO and same total amount of 2517.76 (invoice INV-25-107, paid 2025-06-14), which triggers DUPLICATE and requires rejection."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["DUPLICATE"], "engine_codes": ["DUPLICATE"], "matcher_decision": "reject", "engine_decision": "reject"}`


## Case: ALS-INV-107

**Step 1 — LLM call** (agent: `extractor`, 527+231 tok, 3.65s)
- assistant said:

```
{"invoice_no":"ALS-INV-107","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-05","po_number":"PO-2025-4122","currency":"USD","lines":[{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":27,"unit_price":425.00,"amount":11475.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":23,"unit_price":45.00,"amount":1035.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":8,"unit_price":18.50,"amount":148.00},{"sku":"AL-FUEL","description":"Fuel surcharge","qty":17,"unit_price":63.75,"amount":1083.75}],"subtotal":13741.75,"tax":0.00,"total":13741.75,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1800+146 tok, 3.7s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4122"})`
- agent called `get_received_totals({"po_number": "PO-2025-4122"})`
- agent called `get_vendor_by_name({"name": "AURIGA LOGISTICS SERVICES"})`
- agent called `arithmetic_check({"vendor_id": "V06"})`
- agent called `search_payments({"vendor_id": "V06", "po_number": "PO-2025-4122", "total": 13741.75, "invoice_no": "ALS-INV-107"})`

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

**Step 7 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": [{"invoice_no": "ALS-INV-107", "vendor_id": "V06", "po_number": "PO-2025-4122", "amount": 13741.75, "currency": "USD", "paid_date": "2025-07-02", "match_reasons": ["invoice number already paid (normalized match)", "same vendor + PO + amount already paid"]}]}
```

**Step 9 — LLM call** (agent: `matcher`, 2425+165 tok, 3.8s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "ALS-INV-107",
  "po_number": "PO-2025-4122",
  "decision": "reject",
  "discrepancies": [
    "DUPLICATE"
  ],
  "explanation": "Invoice ALS-INV-107 matches PO-2025-4122 for vendor V06 in USD, with billed quantities matching received quantities on GRN-88321 (27, 23, 8, and 17) and no arithmetic or bank-detail exceptions. However, payment history already shows invoice ALS-INV-107 for vendor V06 on the same PO and amount USD 13,741.75, paid on 2025-07-02, which makes this a duplicate and requires rejection."
}
```

**Step 10 — verifier**: `{"agree": true, "matcher_codes": ["DUPLICATE"], "engine_codes": ["DUPLICATE"], "matcher_decision": "reject", "engine_decision": "reject"}`


## Case: NIS-2025-107

**Step 1 — LLM call** (agent: `extractor`, 506+206 tok, 3.52s)
- assistant said:

```
{"invoice_no":"NIS-2025-107","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-21","po_number":"PO-2025-4123","currency":"USD","lines":[{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":17,"unit_price":6.95,"amount":118.15},{"sku":"NG-3305","description":"Absorbent pads, case","qty":6,"unit_price":42.5,"amount":255.0},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":30,"unit_price":149.0,"amount":4470.0}],"subtotal":4843.15,"tax":388.27,"total":5231.42,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1687+84 tok, 2.85s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4123"})`
- agent called `get_received_totals({"po_number": "PO-2025-4123"})`
- agent called `get_vendor_by_name({"name": "Northgate Industrial Supply LLC"})`

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
{"vendor_id": "V01", "name": "Northgate Industrial Supply LLC", "city": "Columbus, OH", "currency": "USD", "payment_terms": "Net 60", "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "tax_rate": 0.0725}
```

**Step 7 — LLM call** (agent: `matcher`, 2083+83 tok, 2.4s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V01", "po_number": "PO-2025-4123", "total": 5231.42, "invoice_no": "NIS-2025-107"})`
- agent called `arithmetic_check({"vendor_id": "V01"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TAX_ERROR", "evidence": "Tax 388.27 != tax_rate 0.0725 x subtotal 4843.15 = 351.13 (tolerance $0.02)."}], "checks_passed": ["Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2258+174 tok, 3.4s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"NIS-2025-107","po_number":"PO-2025-4123","decision":"hold","discrepancies":["TAX_ERROR"],"explanation":"PO PO-2025-4123 exists for vendor V01 in USD, all three invoice line unit prices match the PO (6.95, 42.50, 149.00), billed quantities do not exceed received quantities from GRN-88322 (17, 6, 30), bank details match the vendor master, and no duplicate was found in payment history. The invoice must be held because the arithmetic check found a TAX_ERROR: tax of 388.27 does not match 7.25% of subtotal 4843.15, which is 351.13, exceeding the $0.02 tolerance."}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["TAX_ERROR"], "engine_codes": ["TAX_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: VPL-2025-104

**Step 1 — LLM call** (agent: `extractor`, 506+232 tok, 4.25s)
- assistant said:

```
{"invoice_no":"VPL-2025-104","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-07-02","po_number":"PO-2025-4124","currency":"EUR","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":12,"unit_price":21.40,"amount":256.80},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":28,"unit_price":9.60,"amount":268.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":33,"unit_price":340.00,"amount":11220.00}],"subtotal":11745.60,"tax":2284.26,"total":14029.86,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1672+88 tok, 2.72s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4124"})`
- agent called `get_received_totals({"po_number": "PO-2025-4124"})`
- agent called `get_vendor_by_name({"name": "VIREO PRINT & LABEL GMBH"})`

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
{"vendor_id": "V09", "name": "Vireo Print & Label GmbH", "city": "Hamburg, DE", "currency": "EUR", "payment_terms": "Net 60", "bank_name": "Hansa Handelsbank", "bank_routing": "DE44 5001 0517", "bank_account": "5407 3249 31", "tax_rate": 0.19}
```

**Step 7 — LLM call** (agent: `matcher`, 2094+83 tok, 2.66s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V09", "po_number": "PO-2025-4124", "total": 14029.86, "invoice_no": "VPL-2025-104"})`
- agent called `arithmetic_check({"vendor_id": "V09"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TAX_ERROR", "evidence": "Tax 2284.26 != tax_rate 0.1900 x subtotal 11745.60 = 2231.66 (tolerance $0.02)."}], "checks_passed": ["Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2271+186 tok, 3.58s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "VPL-2025-104",
  "po_number": "PO-2025-4124",
  "decision": "hold",
  "discrepancies": [
    "TAX_ERROR"
  ],
  "explanation": "PO PO-2025-4124 exists for vendor V09, the invoice currency EUR matches the PO, line prices match the PO exactly, billed quantities (12, 28, 33) do not exceed received quantities on GRN-88323, bank details match vendor master, and no duplicate payment was found. The invoice must be held because the tax is incorrect: invoice tax is 2284.26, but at the vendor master tax rate of 0.19 applied to subtotal 11745.60 the expected tax is 2231.66, exceeding the $0.02 tolerance."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["TAX_ERROR"], "engine_codes": ["TAX_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: SOI-25-107

**Step 1 — LLM call** (agent: `extractor`, 479+175 tok, 4.23s)
- assistant said:

```
{"invoice_no":"SOI-25-107","vendor_name":"Stellar Office Interiors","date":"2025-07-23","po_number":"PO-2025-4125","currency":"USD","lines":[{"sku":"SO-FIL-3D","description":"File cabinet 3-drawer","qty":26,"unit_price":156.80,"amount":4076.80},{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":18,"unit_price":189.00,"amount":3492.00}],"subtotal":7568.80,"tax":613.07,"total":8181.87,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1559+83 tok, 5.52s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4125"})`
- agent called `get_received_totals({"po_number": "PO-2025-4125"})`
- agent called `get_vendor_by_name({"name": "Stellar Office Interiors"})`

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

**Step 7 — LLM call** (agent: `matcher`, 1906+82 tok, 2.37s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V07", "po_number": "PO-2025-4125", "total": 8181.87, "invoice_no": "SOI-25-107"})`
- agent called `arithmetic_check({"vendor_id": "V07"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TOTAL_ERROR", "evidence": "Line SO-CHR-T2: amount 3492.00 != qty 18 x unit price 189.00 = 3402.00."}], "checks_passed": ["Tax OK (613.07 ~= 613.07).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2090+176 tok, 4.29s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "SOI-25-107",
  "po_number": "PO-2025-4125",
  "decision": "hold",
  "discrepancies": ["TOTAL_ERROR"],
  "explanation": "PO PO-2025-4125 exists for vendor V07 in USD, and GRN-88324 shows full receipt of 26 units of SO-FIL-3D and 18 units of SO-CHR-T2, matching the billed quantities; unit prices also match the PO and no duplicate payment was found. However, the arithmetic check found a line total error: line SO-CHR-T2 is billed as 18 x 189.00 but the invoice amount shows 3,492.00 instead of 3,402.00, so the invoice must be held."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["TOTAL_ERROR"], "engine_codes": ["TOTAL_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: MF/25/107

**Step 1 — LLM call** (agent: `extractor`, 553+258 tok, 4.11s)
- assistant said:

```
{"invoice_no":"MF/25/107","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-07-02","po_number":"PO-2025-4126","currency":"USD","lines":[{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":15,"unit_price":62.75,"amount":941.25},{"sku":"MF-M8-50","description":"Hex bolts M8x50 zinc, box 500","qty":5,"unit_price":44.00,"amount":220.00},{"sku":"MF-W-8","description":"Flat washers 8mm, box 1000","qty":39,"unit_price":15.30,"amount":596.70},{"sku":"MF-M8-NUT","description":"Hex nuts M8 zinc, box 1000","qty":36,"unit_price":27.60,"amount":1021.60}],"subtotal":2779.55,"tax":166.77,"total":2946.32,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/107"}`

**Step 3 — LLM call** (agent: `matcher`, 1792+87 tok, 2.66s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4126"})`
- agent called `get_received_totals({"po_number": "PO-2025-4126"})`
- agent called `get_vendor_by_name({"name": "MERIDIAN FASTENERS INC."})`

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

**Step 7 — LLM call** (agent: `matcher`, 2257+81 tok, 2.47s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V03", "po_number": "PO-2025-4126", "total": 2946.32, "invoice_no": "MF/25/107"})`
- agent called `arithmetic_check({"vendor_id": "V03"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TOTAL_ERROR", "evidence": "Line MF-M8-NUT: amount 1021.60 != qty 36 x unit price 27.60 = 993.60."}], "checks_passed": ["Tax OK (166.77 ~= 166.77).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2439+190 tok, 4.0s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "MF/25/107",
  "po_number": "PO-2025-4126",
  "decision": "hold",
  "discrepancies": [
    "TOTAL_ERROR"
  ],
  "explanation": "PO PO-2025-4126 exists for vendor V03, currency matches USD, all invoiced quantities match received quantities on GRN-88325 (15, 5, 39, and 36), unit prices match the PO, the tax 166.77 matches the 6% vendor tax rate, bank details match the vendor master, and no duplicate payment was found. The invoice must be held because line MF-M8-NUT shows amount 1021.60, but arithmetic_check verified that 36 × 27.60 = 993.60, which exceeds the $0.02 tolerance and triggers TOTAL_ERROR."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["TOTAL_ERROR"], "engine_codes": ["TOTAL_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: HEC-2025-110

**Step 1 — LLM call** (agent: `extractor`, 457+186 tok, 3.5s)
- assistant said:

```
{"invoice_no":"HEC-2025-110","vendor_name":"Helios Electrical Components","date":"2025-06-28","po_number":"PO-2025-4127","currency":"USD","lines":[{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":35,"unit_price":96.30,"amount":3370.50},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":12,"unit_price":118.00,"amount":1416.00}],"subtotal":4786.50,"tax":411.64,"total":5198.14,"bank_name":"Meridian Trust Bank","bank_routing":"122100024","bank_account":"7791024468","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-110"}`

**Step 3 — LLM call** (agent: `matcher`, 1514+83 tok, 3.71s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4127"})`
- agent called `get_received_totals({"po_number": "PO-2025-4127"})`
- agent called `get_vendor_by_name({"name": "Helios Electrical Components"})`

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

**Step 7 — LLM call** (agent: `matcher`, 1873+83 tok, 3.13s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V05", "po_number": "PO-2025-4127", "total": 5198.14, "invoice_no": "HEC-2025-110"})`
- agent called `arithmetic_check({"vendor_id": "V05"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "BANK_CHANGE", "evidence": "Remit-to account 7791024468 != vendor master 3348812706 \u2014 verify with vendor before payment."}], "checks_passed": ["Tax OK (411.64 ~= 411.64)."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2040+214 tok, 5.6s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "HEC-2025-110",
  "po_number": "PO-2025-4127",
  "decision": "hold",
  "discrepancies": [
    "BANK_CHANGE"
  ],
  "explanation": "PO PO-2025-4127 exists for vendor V05 in USD, and the invoice matches the PO line prices and quantities: HE-PSU-24 billed 35 at 96.30 vs received 35, and HE-CAB-14 billed 12 at 118.00 vs received 12; GRN GRN-88326 is on file. Arithmetic and tax passed (subtotal 4786.50, tax 411.64 at 8.6%, total 5198.14), and no duplicate payment was found for invoice HEC-2025-110, but the remit-to bank account 7791024468 differs from the vendor master account 3348812706, so the invoice must be held."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["BANK_CHANGE"], "engine_codes": ["BANK_CHANGE"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: GP-107

**Step 1 — LLM call** (agent: `extractor`, 446+176 tok, 3.35s)
- assistant said:

```
{"invoice_no":"GP-107","vendor_name":"Granite Peak Safety Gear","date":"2025-06-19","po_number":"PO-2025-4128","currency":"USD","lines":[{"sku":"GP-HH-CL2","description":"Hard hats class E, box 20","qty":6,"unit_price":196.00,"amount":1176.00},{"sku":"GP-BOOT-10","description":"Steel toe boots size 10","qty":17,"unit_price":112.00,"amount":1904.00}],"subtotal":3080.00,"tax":184.80,"total":3264.80,"bank_name":"Meridian Trust Bank","bank_routing":"123103729","bank_account":"4456108823","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1498+84 tok, 2.59s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4128"})`
- agent called `get_received_totals({"po_number": "PO-2025-4128"})`
- agent called `get_vendor_by_name({"name": "Granite Peak Safety Gear"})`

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

**Step 7 — LLM call** (agent: `matcher`, 1852+79 tok, 2.65s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V08", "po_number": "PO-2025-4128", "total": 3264.8, "invoice_no": "GP-107"})`
- agent called `arithmetic_check({"vendor_id": "V08"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "BANK_CHANGE", "evidence": "Remit-to account 4456108823 != vendor master 2290156841 \u2014 verify with vendor before payment."}], "checks_passed": ["Tax OK (184.80 ~= 184.80)."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2015+207 tok, 4.34s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "GP-107",
  "po_number": "PO-2025-4128",
  "decision": "hold",
  "discrepancies": [
    "BANK_CHANGE"
  ],
  "explanation": "PO PO-2025-4128 exists for vendor V08 in USD, invoice line prices match the PO (GP-HH-CL2 at 196.00 and GP-BOOT-10 at 112.00), and billed quantities 6 and 17 do not exceed received quantities on GRN-88327. Arithmetic passed including subtotal 3080.00, tax 184.80 at 6%, and total 3264.80, and no duplicate payment was found; however, the remit-to bank details differ from vendor master because the invoice shows account 4456108823 at Meridian Trust Bank while vendor master has account 2290156841 at Sawtooth Community Bank, so the invoice must be held."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["BANK_CHANGE"], "engine_codes": ["BANK_CHANGE"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: VPL-2025-107

**Step 1 — LLM call** (agent: `extractor`, 533+232 tok, 3.64s)
- assistant said:

```
{"invoice_no":"VPL-2025-107","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-06-22","po_number":"PO-2025-4129","currency":"USD","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":39,"unit_price":21.40,"amount":834.60},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":38,"unit_price":9.60,"amount":364.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":35,"unit_price":340.00,"amount":11900.00}],"subtotal":13099.40,"tax":2488.89,"total":15588.29,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1672+88 tok, 2.7s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4129"})`
- agent called `get_received_totals({"po_number": "PO-2025-4129"})`
- agent called `get_vendor_by_name({"name": "VIREO PRINT & LABEL GMBH"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4129", "vendor_id": "V09", "date": "2025-05-09", "currency": "EUR", "lines": [{"line_no": 1, "sku": "VP-LBL-4x6", "description": "Thermal labels 4x6, roll 500", "qty": 39, "unit_price": 21.4}, {"line_no": 2, "sku": "VP-RIB-110", "description": "TTR ribbon 110mm", "qty": 38, "unit_price": 9.6}, {"line_no": 3, "sku": "VP-TAG-ASSET", "description": "Asset tags, custom, 1000", "qty": 35, "unit_price": 340.0}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 39, "2": 38, "3": 35}, "grn_count": 1, "grn_numbers": ["GRN-88328"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V09", "name": "Vireo Print & Label GmbH", "city": "Hamburg, DE", "currency": "EUR", "payment_terms": "Net 60", "bank_name": "Hansa Handelsbank", "bank_routing": "DE44 5001 0517", "bank_account": "5407 3249 31", "tax_rate": 0.19}
```

**Step 7 — LLM call** (agent: `matcher`, 2094+83 tok, 4.58s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V09", "po_number": "PO-2025-4129", "total": 15588.29, "invoice_no": "VPL-2025-107"})`
- agent called `arithmetic_check({"vendor_id": "V09"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (2488.89 ~= 2488.89).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2238+165 tok, 3.8s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "VPL-2025-107",
  "po_number": "PO-2025-4129",
  "decision": "hold",
  "discrepancies": ["CURRENCY_MISMATCH"],
  "explanation": "PO PO-2025-4129 exists for vendor V09, all three invoiced unit prices match the PO (21.4, 9.6, 340.0), billed quantities match total receipts on GRN-88328 (39, 38, 35), arithmetic passed, bank details match vendor master, and no duplicate payment was found. However, the invoice is in USD while both the PO and vendor master are in EUR, so this must be held for CURRENCY_MISMATCH."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["CURRENCY_MISMATCH"], "engine_codes": ["CURRENCY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: AMT-107

**Step 1 — LLM call** (agent: `extractor`, 550+253 tok, 3.69s)
- assistant said:

```
{"invoice_no":"AMT-107","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-20","po_number":"PO-2025-9911","currency":"USD","lines":[{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":10,"unit_price":412.60,"amount":4126.00},{"sku":"AM-END-12","description":"End mill 12mm carbide","qty":21,"unit_price":68.20,"amount":1432.20},{"sku":"AM-VIS-6","description":"Machine vise 6in","qty":31,"unit_price":289.00,"amount":8959.00},{"sku":"AM-INS-CNMG","description":"Turning inserts CNMG, box 10","qty":22,"unit_price":94.80,"amount":2085.60}],"subtotal":16602.80,"tax":0.00,"total":16602.80,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1353+122 tok, 2.82s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-9911"})`
- agent called `get_vendor_by_name({"name": "Ashford Machine Tools Ltd."})`
- agent called `arithmetic_check({"vendor_id": "V10"})`
- agent called `search_payments({"vendor_id": "V10", "po_number": "PO-2025-9911", "total": 16602.8, "invoice_no": "AMT-107"})`

**Step 4 — tool `get_po` responded:**

```
{"error": "PO PO-2025-9911 not found"}
```

**Step 5 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V10", "name": "Ashford Machine Tools Ltd.", "city": "Sheffield, UK", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Pennine & Yorkshire Bank", "bank_routing": "GB29 NWBK 6016", "bank_account": "1331 9268 19", "tax_rate": 0.0}
```

**Step 6 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 7 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 8 — LLM call** (agent: `matcher`, 1638+123 tok, 3.01s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "AMT-107",
  "po_number": "PO-2025-9911",
  "decision": "hold",
  "discrepancies": ["PO_NOT_FOUND"],
  "explanation": "PO PO-2025-9911 does not exist in the PO system, so the invoice cannot be matched to an authorized order. Duplicate screening found no prior payment match for vendor V10/invoice AMT-107/total 16602.80, and the arithmetic check found no tax, total, or bank-detail issues."
}
```

**Step 9 — verifier**: `{"agree": true, "matcher_codes": ["PO_NOT_FOUND"], "engine_codes": ["PO_NOT_FOUND"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: NIS-2025-110

**Step 1 — LLM call** (agent: `extractor`, 538+243 tok, 3.5s)
- assistant said:

```
{"invoice_no":"NIS-2025-110","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-15","po_number":"PO-2025-4131","currency":"USD","lines":[{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":10,"unit_price":20.24,"amount":202.40},{"sku":"NG-3305","description":"Absorbent pads, case","qty":24,"unit_price":42.50,"amount":1020.00},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":6,"unit_price":149.00,"amount":894.00},{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":17,"unit_price":6.95,"amount":118.15}],"subtotal":2234.55,"tax":162.00,"total":2396.55,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-110"}`

**Step 3 — LLM call** (agent: `matcher`, 1828+84 tok, 2.85s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4131"})`
- agent called `get_received_totals({"po_number": "PO-2025-4131"})`
- agent called `get_vendor_by_name({"name": "Northgate Industrial Supply LLC"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4131", "vendor_id": "V01", "date": "2025-05-10", "currency": "USD", "lines": [{"line_no": 1, "sku": "NG-4410", "description": "Nitrile work gloves, box of 100", "qty": 10, "unit_price": 18.4}, {"line_no": 2, "sku": "NG-3305", "description": "Absorbent pads, case", "qty": 24, "unit_price": 42.5}, {"line_no": 3, "sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 6, "unit_price": 149.0}, {"line_no": 4, "sku": "NG-7720", "description": "Safety goggles, anti-fog", "qty": 17, "unit_price": 6.95}], "status": "open"}
```

**Step 5 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 5, "2": 12, "3": 3, "4": 8}, "grn_count": 1, "grn_numbers": ["GRN-88330"]}
```

**Step 6 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V01", "name": "Northgate Industrial Supply LLC", "city": "Columbus, OH", "currency": "USD", "payment_terms": "Net 60", "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "tax_rate": 0.0725}
```

**Step 7 — LLM call** (agent: `matcher`, 2276+83 tok, 3.3s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V01", "po_number": "PO-2025-4131", "total": 2396.55, "invoice_no": "NIS-2025-110"})`
- agent called `arithmetic_check({"vendor_id": "V01"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (162.00 ~= 162.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2418+193 tok, 3.88s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "NIS-2025-110",
  "po_number": "PO-2025-4131",
  "decision": "hold",
  "discrepancies": [
    "PRICE_MISMATCH",
    "QTY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4131 exists and is in USD, the invoice bank details match the vendor master, no duplicate payment was found, and arithmetic checks passed. However, line SKU NG-4410 is billed at 20.24 versus PO unit price 18.40, which exceeds the 0.5% price tolerance, and billed quantities exceed received quantities on all lines: line 1 billed 10 vs received 5, line 2 billed 24 vs 12, line 3 billed 6 vs 3, and line 4 billed 17 vs 8."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["PRICE_MISMATCH", "QTY_MISMATCH"], "engine_codes": ["PRICE_MISMATCH", "QTY_MISMATCH"], "matcher_decision": "hold", "engine_decision": "hold"}`


## Case: CCW-107

**Step 1 — LLM call** (agent: `extractor`, 521+220 tok, 3.42s)
- assistant said:

```
{"invoice_no":"CCW-107","vendor_name":"Cascadia Chemical Works","date":"2025-06-04","po_number":"PO-2025-4132","currency":"USD","lines":[{"sku":"CC-COOL-55","description":"Machine coolant concentrate, 55gal","qty":37,"unit_price":744.50,"amount":27546.50},{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":21,"unit_price":87.40,"amount":1835.40},{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":8,"unit_price":612.00,"amount":4896.00}],"subtotal":34277.90,"tax":3300.50,"total":37578.40,"bank_name":"Meridian Trust Bank","bank_routing":"125000024","bank_account":"6120087745","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1717+84 tok, 2.74s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4132"})`
- agent called `get_received_totals({"po_number": "PO-2025-4132"})`
- agent called `get_vendor_by_name({"name": "Cascadia Chemical Works"})`

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

**Step 7 — LLM call** (agent: `matcher`, 2126+80 tok, 2.55s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V04", "po_number": "PO-2025-4132", "total": 37578.4, "invoice_no": "CCW-107"})`
- agent called `arithmetic_check({"vendor_id": "V04"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [{"code": "TAX_ERROR", "evidence": "Tax 3300.50 != tax_rate 0.0950 x subtotal 34277.90 = 3256.40 (tolerance $0.02)."}, {"code": "BANK_CHANGE", "evidence": "Remit-to account 6120087745 != vendor master 9027481133 \u2014 verify with vendor before payment."}], "checks_passed": []}
```

**Step 10 — LLM call** (agent: `matcher`, 2326+192 tok, 3.77s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "CCW-107",
  "po_number": "PO-2025-4132",
  "decision": "hold",
  "discrepancies": [
    "TAX_ERROR",
    "BANK_CHANGE"
  ],
  "explanation": "PO PO-2025-4132 exists for vendor V04, all three invoice line prices match the PO, billed quantities 37/21/8 match GRN totals from GRN-88331, currency is USD on both invoice and PO, and no duplicate payment was found. However, the tax is incorrect: invoice tax 3300.50 does not match 9.5% of subtotal 34277.90, which is 3256.40, and the remit-to bank account 6120087745 differs from the vendor master account 9027481133 (routing 125000024 matches)."
}
```

**Step 11 — verifier**: `{"agree": true, "matcher_codes": ["BANK_CHANGE", "TAX_ERROR"], "engine_codes": ["BANK_CHANGE", "TAX_ERROR"], "matcher_decision": "hold", "engine_decision": "hold"}`
