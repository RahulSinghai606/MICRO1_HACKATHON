# Agent trajectories — run `agent_v2`


## Case: NIS-2025-101

**Step 1 — LLM call** (agent: `extractor`, 538+243 tok, 3.91s)
- assistant said:

```
{"invoice_no":"NIS-2025-101","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-18","po_number":"PO-2025-4101","currency":"USD","lines":[{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":3,"unit_price":18.40,"amount":55.20},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":7,"unit_price":149.00,"amount":1043.00},{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":15,"unit_price":6.95,"amount":104.25},{"sku":"NG-3305","description":"Absorbent pads, case","qty":16,"unit_price":42.50,"amount":680.00}],"subtotal":1882.45,"tax":136.48,"total":2018.93,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1828+84 tok, 2.78s)
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

**Step 7 — LLM call** (agent: `matcher`, 2276+83 tok, 2.9s)
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

**Step 10 — LLM call** (agent: `matcher`, 2418+180 tok, 3.8s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "NIS-2025-101",
  "po_number": "PO-2025-4101",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4101 exists for vendor V01 and the invoice matches the PO on currency (USD), unit prices, and quantities: billed quantities 3, 7, 15, and 16 do not exceed GRN totals on GRN-88301 for lines 1-4. Arithmetic checks passed, including subtotal 1882.45, tax 136.48 at the vendor tax rate, and total 2018.93; remit-to bank routing 021000021 and account 4402198837 match the vendor master, and no duplicate payment or prior invoice number was found."
}
```


## Case: INV-2025-0101

**Step 1 — LLM call** (agent: `extractor`, 446+178 tok, 4.38s)
- assistant said:

```
{"invoice_no":"INV-2025-0101","vendor_name":"Bluefin Packaging Co.","date":"2025-06-25","po_number":"PO-2025-4102","currency":"USD","lines":[{"sku":"BP-450","description":"Foam inserts, custom cut","qty":30,"unit_price":4.15,"amount":124.50},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":39,"unit_price":31.25,"amount":1218.75}],"subtotal":1343.25,"tax":94.03,"total":1437.28,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0101"}`

**Step 3 — LLM call** (agent: `matcher`, 1561+84 tok, 3.06s)
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

**Step 7 — LLM call** (agent: `matcher`, 1913+83 tok, 3.55s)
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

**Step 10 — LLM call** (agent: `matcher`, 2055+181 tok, 3.54s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "INV-2025-0101",
  "po_number": "PO-2025-4102",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4102 exists for vendor V02 in USD, and the invoice matches the PO line prices exactly: BP-450 at 4.15 for qty 30 and BP-201 at 31.25 for qty 39. GRN totals show 30 received on line 1 and 39 on line 2 via GRN-88302, so billed quantities do not exceed receipts; arithmetic check passed including subtotal 1343.25, tax 94.03 at 7%, total 1437.28, bank details matched the vendor master, and no duplicate payment was found."
}
```


## Case: MF/25/101

**Step 1 — LLM call** (agent: `extractor`, 487+182 tok, 3.76s)
- assistant said:

```
{"invoice_no":"MF/25/101","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-07-04","po_number":"PO-2025-4103","currency":"USD","lines":[{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":19,"unit_price":62.75,"amount":1192.25},{"sku":"MF-M8-NUT","description":"Hex nuts M8 zinc, box 1000","qty":11,"unit_price":27.60,"amount":303.60}],"subtotal":1495.85,"tax":89.75,"total":1585.60,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/101"}`

**Step 3 — LLM call** (agent: `matcher`, 1505+87 tok, 3.58s)
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

**Step 7 — LLM call** (agent: `matcher`, 1864+81 tok, 3.67s)
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

**Step 10 — LLM call** (agent: `matcher`, 2004+168 tok, 4.18s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "MF/25/101",
  "po_number": "PO-2025-4103",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4103 exists for vendor V03 in USD, and the invoice matches the PO line prices exactly: MF-ANC-10 at 62.75 for qty 19 and MF-M8-NUT at 27.60 for qty 11. GRN totals show full receipt against the PO (line 1 received 19, line 2 received 11), arithmetic checks passed including tax 89.75 at the 6% vendor tax rate, bank details match the vendor master, and no duplicate payment or invoice number was found."
}
```


## Case: CCW-101

**Step 1 — LLM call** (agent: `extractor`, 489+183 tok, 3.01s)
- assistant said:

```
{"invoice_no":"CCW-101","vendor_name":"Cascadia Chemical Works","date":"2025-06-24","po_number":"PO-2025-4104","currency":"USD","lines":[{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":24,"unit_price":87.40,"amount":2097.60},{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":24,"unit_price":612.00,"amount":14688.00}],"subtotal":16785.60,"tax":1594.63,"total":18380.23,"bank_name":"Puget Sound Trust","bank_routing":"125000024","bank_account":"9027481133","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1575+84 tok, 3.21s)
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

**Step 7 — LLM call** (agent: `matcher`, 1933+80 tok, 2.7s)
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

**Step 10 — LLM call** (agent: `matcher`, 2074+154 tok, 3.61s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"CCW-101","po_number":"PO-2025-4104","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4104 exists for vendor V04 in USD, and the invoice line prices match the PO exactly (CC-DEG-5 at 87.4 and CC-IPA-55 at 612.0). GRN coverage is complete via GRN-88304 with 24 received on line 1 and 24 on line 2, matching billed quantities; arithmetic_check found tax 1594.63 valid, bank details matching vendor master, and payment search found no duplicate for invoice CCW-101 or total 18380.23."}
```


## Case: HEC-2025-101

**Step 1 — LLM call** (agent: `extractor`, 481+216 tok, 3.44s)
- assistant said:

```
{"invoice_no":"HEC-2025-101","vendor_name":"Helios Electrical Components","date":"2025-06-02","po_number":"PO-2025-4105","currency":"USD","lines":[{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":37,"unit_price":9.85,"amount":364.45},{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":20,"unit_price":14.20,"amount":284.00},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":25,"unit_price":96.30,"amount":2407.50}],"subtotal":3055.95,"tax":262.81,"total":3318.76,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1643+83 tok, 2.73s)
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

**Step 7 — LLM call** (agent: `matcher`, 2048+83 tok, 2.5s)
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

**Step 10 — LLM call** (agent: `matcher`, 2190+182 tok, 3.87s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"HEC-2025-101","po_number":"PO-2025-4105","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4105 exists for vendor V05 in USD, and the invoice line prices match the PO exactly (HE-CB-20 at 9.85, HE-REL-24 at 14.20, HE-PSU-24 at 96.30). GRN totals show full receipt against the PO (line 1: 37, line 2: 20, line 3: 25), arithmetic checks passed including tax 262.81 at the 8.6% vendor tax rate, bank details match the vendor master, and no duplicate payment was found for invoice HEC-2025-101 or total 3318.76."}
```


## Case: ALS-INV-101

**Step 1 — LLM call** (agent: `extractor`, 525+230 tok, 3.34s)
- assistant said:

```
{"invoice_no":"ALS-INV-101","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-06","po_number":"PO-2025-4106","currency":"USD","lines":[{"sku":"AL-FUEL","description":"Fuel surcharge","qty":8,"unit_price":63.75,"amount":510.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":26,"unit_price":18.50,"amount":481.00},{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":19,"unit_price":425.00,"amount":8075.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":31,"unit_price":45.00,"amount":1395.00}],"subtotal":10461.00,"tax":0.00,"total":10461.00,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1799+85 tok, 2.42s)
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

**Step 7 — LLM call** (agent: `matcher`, 2233+79 tok, 3.94s)
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

**Step 10 — LLM call** (agent: `matcher`, 2371+183 tok, 3.99s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"ALS-INV-101","po_number":"PO-2025-4106","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4106 exists for vendor V06 in USD, and all invoice line prices match the PO exactly: AL-FUEL 63.75, AL-WHS-P 18.50, AL-LTL-STD 425.00, and AL-LIFT 45.00. GRN totals from GRN-88306 fully cover the billed quantities (8, 26, 19, and 31 respectively), arithmetic checks passed including subtotal 10,461.00, tax 0.00 at the 0.0 tax rate, and total 10,461.00, the remit-to bank details match vendor master, and no duplicate payment or invoice number was found."}
```


## Case: SOI-25-101

**Step 1 — LLM call** (agent: `extractor`, 508+208 tok, 3.91s)
- assistant said:

```
{"invoice_no":"SOI-25-101","vendor_name":"Stellar Office Interiors","date":"2025-06-06","po_number":"PO-2025-4107","currency":"USD","lines":[{"sku":"SO-MON-ARM","description":"Dual monitor arm","qty":6,"unit_price":74.25,"amount":445.5},{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":40,"unit_price":189.0,"amount":7560.0},{"sku":"SO-DSK-60","description":"Sit-stand desk 60in","qty":12,"unit_price":415.0,"amount":4980.0}],"subtotal":12985.5,"tax":1051.83,"total":14037.33,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1692+83 tok, 2.99s)
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

**Step 7 — LLM call** (agent: `matcher`, 2086+82 tok, 2.39s)
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

**Step 10 — LLM call** (agent: `matcher`, 2229+177 tok, 4.98s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "SOI-25-101",
  "po_number": "PO-2025-4107",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4107 exists for vendor V07 in USD, and the invoice line prices match the PO exactly: SO-MON-ARM 74.25, SO-CHR-T2 189.00, and SO-DSK-60 415.00. GRN GRN-88307 shows full receipt of 6, 40, and 12 units respectively, arithmetic checks passed including tax 1,051.83 at the 8.1% vendor tax rate, the remit-to bank details match the vendor master, and no duplicate payment or invoice number was found."
}
```


## Case: GP-101

**Step 1 — LLM call** (agent: `extractor`, 479+214 tok, 3.68s)
- assistant said:

```
{"invoice_no":"GP-101","vendor_name":"Granite Peak Safety Gear","date":"2025-07-13","po_number":"PO-2025-4108","currency":"USD","lines":[{"sku":"GP-EAR-200","description":"Ear plugs, box 200 pr","qty":22,"unit_price":38.90,"amount":855.80},{"sku":"GP-VIS-XL","description":"Hi-vis vests XL, pack 10","qty":5,"unit_price":84.50,"amount":422.50},{"sku":"GP-HH-CL2","description":"Hard hats class E, box 20","qty":16,"unit_price":196.00,"amount":3136.00}],"subtotal":4414.30,"tax":264.86,"total":4679.16,"bank_name":"Sawtooth Community Bank","bank_routing":"123103729","bank_account":"2290156841","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1642+84 tok, 3.13s)
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

**Step 7 — LLM call** (agent: `matcher`, 2049+79 tok, 2.75s)
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

**Step 10 — LLM call** (agent: `matcher`, 2187+154 tok, 3.55s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"GP-101","po_number":"PO-2025-4108","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4108 exists for vendor V08 in USD, and all invoiced line prices match the PO exactly (38.90, 84.50, and 196.00). GRN totals show full receipt against all PO lines (22, 5, and 16 units on GRN-88308), arithmetic passed including subtotal 4414.30, tax 264.86 at 6%, and total 4679.16, the remit-to bank matches vendor master, and no duplicate payment or prior invoice GP-101 was found."}
```


## Case: VPL-2025-101

**Step 1 — LLM call** (agent: `extractor`, 506+232 tok, 3.85s)
- assistant said:

```
{"invoice_no":"VPL-2025-101","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-06-09","po_number":"PO-2025-4109","currency":"EUR","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":15,"unit_price":21.40,"amount":321.00},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":33,"unit_price":9.60,"amount":316.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":27,"unit_price":340.00,"amount":9180.00}],"subtotal":9817.80,"tax":1865.38,"total":11683.18,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1672+88 tok, 2.61s)
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

**Step 7 — LLM call** (agent: `matcher`, 2094+83 tok, 2.62s)
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

**Step 10 — LLM call** (agent: `matcher`, 2238+177 tok, 4.01s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "VPL-2025-101",
  "po_number": "PO-2025-4109",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4109 exists for vendor V09, the invoice currency EUR matches the PO, all billed unit prices match the PO (21.4, 9.6, 340.0), and billed quantities 15/33/27 do not exceed total received quantities 15/33/27 on GRN-88309. Arithmetic check passed including subtotal 9817.80, tax 1865.38 at 19%, and total 11683.18, the remit-to bank details match the vendor master, and payment history returned no duplicate invoice or paid match."
}
```


## Case: AMT-101

**Step 1 — LLM call** (agent: `extractor`, 485+181 tok, 3.3s)
- assistant said:

```
{"invoice_no":"AMT-101","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-19","po_number":"PO-2025-4110","currency":"USD","lines":[{"sku":"AM-VIS-6","description":"Machine vise 6in","qty":37,"unit_price":289.00,"amount":10693.00},{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":36,"unit_price":412.60,"amount":14853.60}],"subtotal":25546.60,"tax":0.00,"total":25546.60,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-101"}`

**Step 3 — LLM call** (agent: `matcher`, 1505+85 tok, 3.17s)
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

**Step 7 — LLM call** (agent: `matcher`, 1863+80 tok, 3.54s)
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

**Step 10 — LLM call** (agent: `matcher`, 2002+173 tok, 3.74s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "AMT-101",
  "po_number": "PO-2025-4110",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4110 exists for vendor V10 in USD, and the invoice line prices match the PO exactly: AM-VIS-6 at 289.00 for qty 37 and AM-CHK-125 at 412.60 for qty 36. GRN-88310 shows full receipt of 37 and 36 units respectively, arithmetic checks passed including subtotal 25546.60, tax 0.00 at a 0.0 tax rate, total 25546.60, the remit-to bank matches the vendor master, and no duplicate payment was found."
}
```


## Case: NIS-2025-104

**Step 1 — LLM call** (agent: `extractor`, 527+219 tok, 3.69s)
- assistant said:

```
{"invoice_no":"NIS-2025-104","vendor_name":"Northgate Ind. Supply (a div. of NIS Holdings)","date":"2025-06-05","po_number":"PO-2025-4111","currency":"USD","lines":[{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":34,"unit_price":149.00,"amount":5066.00},{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":33,"unit_price":18.40,"amount":607.20},{"sku":"NG-3305","description":"Absorbent pads, case","qty":7,"unit_price":42.50,"amount":297.50}],"subtotal":5970.70,"tax":432.88,"total":6403.58,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1841+93 tok, 2.74s)
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

**Step 7 — LLM call** (agent: `matcher`, 2200+83 tok, 2.53s)
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

**Step 10 — LLM call** (agent: `matcher`, 2342+173 tok, 4.01s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"NIS-2025-104","po_number":"PO-2025-4111","decision":"approve","discrepancies":[],"explanation":"PO PO-2025-4111 exists for vendor V01 in USD, and the invoice line prices match the PO exactly: NG-1180 at 149.00, NG-4410 at 18.40, and NG-3305 at 42.50. Total received quantities across GRNs GRN-88311 and GRN-88312 equal the billed quantities for each line (34, 33, and 7 respectively), arithmetic checks passed including tax 432.88 and total 6403.58, bank details match the vendor master, and no duplicate payment was found for invoice NIS-2025-104."}
```


## Case: HEC-2025-104

**Step 1 — LLM call** (agent: `extractor`, 517+256 tok, 3.67s)
- assistant said:

```
{"invoice_no":"HEC-2025-104","vendor_name":"Helios Electrical Components","date":"2025-06-22","po_number":"PO-2025-4112","currency":"USD","lines":[{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":26,"unit_price":14.20,"amount":369.20},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":26,"unit_price":118.00,"amount":3068.00},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":40,"unit_price":96.30,"amount":3852.00},{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":31,"unit_price":9.85,"amount":305.35}],"subtotal":7594.55,"tax":653.14,"total":8247.69,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1790+83 tok, 3.41s)
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

**Step 7 — LLM call** (agent: `matcher`, 2249+83 tok, 2.43s)
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

**Step 10 — LLM call** (agent: `matcher`, 2391+181 tok, 4.26s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "HEC-2025-104",
  "po_number": "PO-2025-4112",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4112 exists for vendor V05 in USD, and all invoice line prices match the PO exactly: 14.20, 118.00, 96.30, and 9.85. Received quantities from GRN-88313 fully cover billed quantities for lines 1-4 (26, 26, 40, and 31 respectively), arithmetic passed including tax 653.14 within tolerance of expected 653.13, bank details match the vendor master, and no duplicate payment was found for invoice HEC-2025-104 or total 8247.69."
}
```


## Case: MF/25/104

**Step 1 — LLM call** (agent: `extractor`, 551+257 tok, 3.76s)
- assistant said:

```
{"invoice_no":"MF/25/104","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-07-17","po_number":"PO-2025-4113","currency":"USD","lines":[{"sku":"MF-M8-50","description":"Hex bolts M8x50 zinc, box 500","qty":9,"unit_price":49.28,"amount":443.52},{"sku":"MF-W-8","description":"Flat washers 8mm, box 1000","qty":20,"unit_price":15.30,"amount":306.00},{"sku":"MF-M8-NUT","description":"Hex nuts M8 zinc, box 1000","qty":29,"unit_price":27.60,"amount":800.40},{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":12,"unit_price":62.75,"amount":753.00}],"subtotal":2302.92,"tax":138.18,"total":2441.10,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/104"}`

**Step 3 — LLM call** (agent: `matcher`, 1791+87 tok, 2.9s)
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

**Step 7 — LLM call** (agent: `matcher`, 2256+81 tok, 2.44s)
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

**Step 10 — LLM call** (agent: `matcher`, 2396+172 tok, 4.42s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"MF/25/104","po_number":"PO-2025-4113","decision":"hold","discrepancies":["PRICE_MISMATCH"],"explanation":"PO PO-2025-4113 exists, GRN GRN-88314 covers the full billed quantities (9, 20, 29, and 12 units), currency is USD on both invoice and PO, the bank details match vendor master, and no duplicate payment was found. However, line SKU MF-M8-50 is billed at 49.28 while the PO unit price is 44.00, which exceeds the 0.5% unit-price tolerance; arithmetic checks otherwise passed, including subtotal 2302.92, tax 138.18 at 6%, and total 2441.10."}
```


## Case: SOI-25-104

**Step 1 — LLM call** (agent: `extractor`, 475+171 tok, 3.3s)
- assistant said:

```
{"invoice_no":"SOI-25-104","vendor_name":"Stellar Office Interiors","date":"2025-06-12","po_number":"PO-2025-4114","currency":"USD","lines":[{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":21,"unit_price":204.12,"amount":4286.52},{"sku":"SO-MON-ARM","description":"Dual monitor arm","qty":34,"unit_price":74.25,"amount":2524.5}],"subtotal":6811.02,"tax":551.69,"total":7362.71,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1550+83 tok, 2.39s)
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

**Step 7 — LLM call** (agent: `matcher`, 1893+82 tok, 3.73s)
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

**Step 10 — LLM call** (agent: `matcher`, 2034+155 tok, 3.41s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"SOI-25-104","po_number":"PO-2025-4114","decision":"hold","discrepancies":["PRICE_MISMATCH"],"explanation":"PO PO-2025-4114 exists in USD and has GRN GRN-88315 with received quantities matching the invoice (line 1: 21 received vs 21 billed; line 2: 34 received vs 34 billed). However, invoice line SO-CHR-T2 is billed at 204.12 while the PO unit price is 189.00, which exceeds the 0.5% tolerance; the other line price matches, arithmetic passed, bank details match vendor master, and no duplicate payment was found."}
```


## Case: AMT-104

**Step 1 — LLM call** (agent: `extractor`, 485+181 tok, 3.15s)
- assistant said:

```
{"invoice_no":"AMT-104","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-27","po_number":"PO-2025-4115","currency":"USD","lines":[{"sku":"AM-END-12","description":"End mill 12mm carbide","qty":22,"unit_price":78.43,"amount":1725.46},{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":33,"unit_price":412.60,"amount":13615.80}],"subtotal":15341.26,"tax":0.00,"total":15341.26,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1504+85 tok, 2.78s)
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

**Step 7 — LLM call** (agent: `matcher`, 1862+80 tok, 2.5s)
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

**Step 10 — LLM call** (agent: `matcher`, 2001+189 tok, 4.15s)
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
  "explanation": "PO PO-2025-4115 exists in USD for vendor V10, and GRN-88316 shows received quantities of 22 for line 1 and 33 for line 2, matching the billed quantities. However, invoice line SKU AM-END-12 is billed at 78.43 versus the PO unit price of 68.20, which exceeds the 0.5% tolerance; line 2 matches at 412.60. No duplicate payment was found for vendor V10 / PO-2025-4115 / total 15341.26, and the remit-to bank details and tax check passed."
}
```


## Case: INV-2025-0104

**Step 1 — LLM call** (agent: `extractor`, 473+210 tok, 5.05s)
- assistant said:

```
{"invoice_no":"INV-2025-0104","vendor_name":"Bluefin Packaging Co.","date":"2025-06-25","po_number":"PO-2025-4116","currency":"USD","lines":[{"sku":"BP-115","description":"Stretch wrap roll 80ga","qty":38,"unit_price":12.80,"amount":486.40},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":7,"unit_price":31.25,"amount":218.75},{"sku":"BP-330","description":"Packing tape, case of 36","qty":7,"unit_price":58.90,"amount":412.30}],"subtotal":1117.45,"tax":78.22,"total":1195.67,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0104"}`

**Step 3 — LLM call** (agent: `matcher`, 1692+84 tok, 2.61s)
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

**Step 7 — LLM call** (agent: `matcher`, 2092+83 tok, 2.9s)
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

**Step 10 — LLM call** (agent: `matcher`, 2234+176 tok, 3.46s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"INV-2025-0104","po_number":"PO-2025-4116","decision":"hold","discrepancies":["QTY_MISMATCH"],"explanation":"PO PO-2025-4116 exists for vendor V02 in USD, invoice unit prices match the PO (BP-115 $12.80, BP-201 $31.25, BP-330 $58.90), arithmetic passed, bank details match vendor master, and no duplicate was found. However, billed quantities exceed received quantities on all lines: line 1 billed 38 vs received 22, line 2 billed 7 vs received 4, and line 3 billed 7 vs received 4 based on GRN GRN-88317, so the invoice must be held for QTY_MISMATCH."}
```


## Case: HEC-2025-107

**Step 1 — LLM call** (agent: `extractor`, 517+256 tok, 3.53s)
- assistant said:

```
{"invoice_no":"HEC-2025-107","vendor_name":"Helios Electrical Components","date":"2025-06-23","po_number":"PO-2025-4117","currency":"USD","lines":[{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":18,"unit_price":14.20,"amount":255.60},{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":35,"unit_price":9.85,"amount":344.75},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":40,"unit_price":96.30,"amount":3852.00},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":29,"unit_price":118.00,"amount":3422.00}],"subtotal":7874.35,"tax":677.19,"total":8551.54,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1790+83 tok, 2.52s)
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

**Step 7 — LLM call** (agent: `matcher`, 2249+83 tok, 4.15s)
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

**Step 10 — LLM call** (agent: `matcher`, 2391+178 tok, 3.77s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "HEC-2025-107",
  "po_number": "PO-2025-4117",
  "decision": "hold",
  "discrepancies": [
    "QTY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4117 exists and matches the invoice in USD, line unit prices, arithmetic, tax ($677.19 at 8.6%), and bank details; no duplicate payment was found for vendor V05. However, billed quantities exceed received quantities on every line: line 1 billed 18 vs received 10, line 2 billed 35 vs 21, line 3 billed 40 vs 24, and line 4 billed 29 vs 17 (GRN-88318), so the invoice must be held."
}
```


## Case: GP-104

**Step 1 — LLM call** (agent: `extractor`, 480+213 tok, 4.11s)
- assistant said:

```
{"invoice_no":"GP-104","vendor_name":"Granite Peak Safety Gear","date":"2025-06-03","po_number":"PO-2025-4118","currency":"USD","lines":[{"sku":"GP-EAR-200","description":"Ear plugs, box 200 pr","qty":30,"unit_price":38.90,"amount":1167.00},{"sku":"GP-BOOT-10","description":"Steel toe boots size 10","qty":35,"unit_price":112.00,"amount":3920.00},{"sku":"GP-VIS-XL","description":"Hi-vis vests XL, pack 10","qty":30,"unit_price":84.50,"amount":2535.00}],"subtotal":7622.00,"tax":457.32,"total":8079.32,"bank_name":"Sawtooth Community Bank","bank_routing":"123103729","bank_account":"2290156841","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1637+84 tok, 2.4s)
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

**Step 7 — LLM call** (agent: `matcher`, 2041+79 tok, 2.42s)
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

**Step 10 — LLM call** (agent: `matcher`, 2179+160 tok, 3.71s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "GP-104",
  "po_number": "PO-2025-4118",
  "decision": "hold",
  "discrepancies": ["QTY_MISMATCH"],
  "explanation": "The PO exists and matches the invoice in USD, prices, and bank details, and arithmetic checks passed including tax of 457.32 on subtotal 7622.00 with no duplicate found. However, billed quantities exceed received quantities on every line: line 1 billed 30 vs received 18, line 2 billed 35 vs received 21, and line 3 billed 30 vs received 18 (GRN-88319), so the invoice must be held for QTY_MISMATCH."
}
```


## Case: CCW-104

**Step 1 — LLM call** (agent: `extractor`, 518+218 tok, 3.77s)
- assistant said:

```
{"invoice_no":"CCW-104","vendor_name":"Cascadia Chemical Works","date":"2025-06-28","po_number":"PO-2025-4119","currency":"USD","lines":[{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":2,"unit_price":612.00,"amount":1224.00},{"sku":"CC-COOL-55","description":"Machine coolant concentrate, 55gal","qty":6,"unit_price":744.50,"amount":4467.00},{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":5,"unit_price":87.40,"amount":437.00}],"subtotal":6128.00,"tax":582.16,"total":6710.16,"bank_name":"Puget Sound Trust","bank_routing":"125000024","bank_account":"9027481133","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1574+84 tok, 2.74s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4119"})`
- agent called `get_vendor_by_name({"name": "Cascadia Chemical Works"})`
- agent called `get_received_totals({"po_number": "PO-2025-4119"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4119", "vendor_id": "V04", "date": "2025-04-03", "currency": "USD", "lines": [{"line_no": 1, "sku": "CC-IPA-55", "description": "Isopropyl alcohol 99%, 55gal drum", "qty": 2, "unit_price": 612.0}, {"line_no": 2, "sku": "CC-COOL-55", "description": "Machine coolant concentrate, 55gal", "qty": 6, "unit_price": 744.5}, {"line_no": 3, "sku": "CC-DEG-5", "description": "Industrial degreaser, 5gal", "qty": 5, "unit_price": 87.4}], "status": "open"}
```

**Step 5 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V04", "name": "Cascadia Chemical Works", "city": "Tacoma, WA", "currency": "USD", "payment_terms": "Net 60", "bank_name": "Puget Sound Trust", "bank_routing": "125000024", "bank_account": "9027481133", "tax_rate": 0.095}
```

**Step 6 — tool `get_received_totals` responded:**

```
{"error": "no GRNs exist for PO-2025-4119"}
```

**Step 7 — LLM call** (agent: `matcher`, 1956+80 tok, 4.47s)
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

**Step 10 — LLM call** (agent: `matcher`, 2095+185 tok, 3.74s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"CCW-104","po_number":"PO-2025-4119","decision":"hold","discrepancies":["GRN_MISSING","QTY_MISMATCH"],"explanation":"PO PO-2025-4119 exists for vendor V04 and the invoice matches the PO on currency (USD), line prices (612.00, 744.50, 87.40), bank details, and arithmetic; no duplicate payment was found for invoice CCW-104 or total 6710.16. However, no GRNs exist for this PO, so received quantity is 0 for all lines; the invoice bills 2 of CC-IPA-55, 6 of CC-COOL-55, and 5 of CC-DEG-5, which exceeds received quantities and triggers both GRN_MISSING and QTY_MISMATCH."}
```


## Case: ALS-INV-104

**Step 1 — LLM call** (agent: `extractor`, 502+202 tok, 3.27s)
- assistant said:

```
{"invoice_no":"ALS-INV-104","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-08","po_number":"PO-2025-4120","currency":"USD","lines":[{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":19,"unit_price":425.00,"amount":8075.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":33,"unit_price":45.00,"amount":1485.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":15,"unit_price":18.50,"amount":277.50}],"subtotal":9837.50,"tax":0.00,"total":9837.50,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1540+85 tok, 2.58s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4120"})`
- agent called `get_received_totals({"po_number": "PO-2025-4120"})`
- agent called `get_vendor_by_name({"name": "AURIGA LOGISTICS SERVICES"})`

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

**Step 7 — LLM call** (agent: `matcher`, 1903+81 tok, 2.52s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V06", "po_number": "PO-2025-4120", "total": 9837.5, "invoice_no": "ALS-INV-104"})`
- agent called `arithmetic_check({"vendor_id": "V06"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2043+179 tok, 3.67s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"ALS-INV-104","po_number":"PO-2025-4120","decision":"hold","discrepancies":["GRN_MISSING","QTY_MISMATCH"],"explanation":"PO PO-2025-4120 exists for vendor V06 and matches the invoice in USD, line unit prices (425.00, 45.00, 18.50), and bank details, and no duplicate payment was found for invoice ALS-INV-104 or total 9837.50. However, no GRNs exist for this PO, so received quantity is 0 for all lines while the invoice bills 19 AL-LTL-STD, 33 AL-LIFT, and 15 AL-WHS-P; therefore both GRN_MISSING and QTY_MISMATCH apply, so the invoice must be held."}
```


## Case: INV-2025-0107

**Step 1 — LLM call** (agent: `extractor`, 475+211 tok, 3.58s)
- assistant said:

```
{"invoice_no":"INV-2025-0107","vendor_name":"Bluefin Packaging Co.","date":"2025-07-28","po_number":"PO-2025-4121","currency":"USD","lines":[{"sku":"BP-450","description":"Foam inserts, custom cut","qty":8,"unit_price":4.15,"amount":33.20},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":29,"unit_price":31.25,"amount":906.25},{"sku":"BP-330","description":"Packing tape, case of 36","qty":24,"unit_price":58.90,"amount":1413.60}],"subtotal":2353.05,"tax":164.71,"total":2517.76,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0107"}`

**Step 3 — LLM call** (agent: `matcher`, 1693+84 tok, 2.86s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4121"})`
- agent called `get_received_totals({"po_number": "PO-2025-4121"})`
- agent called `get_vendor_by_name({"name": "Bluefin Packaging Co."})`

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
{"vendor_id": "V02", "name": "Bluefin Packaging Co.", "city": "Savannah, GA", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Coastal Georgia Bank", "bank_routing": "061000104", "bank_account": "7719045512", "tax_rate": 0.07}
```

**Step 7 — LLM call** (agent: `matcher`, 2093+83 tok, 2.68s)
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

**Step 10 — LLM call** (agent: `matcher`, 2309+183 tok, 4.25s)
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
  "explanation": "PO PO-2025-4121 exists for vendor V02 in USD, GRN GRN-88320 shows full receipt of 8, 29, and 24 units for lines 1-3, and arithmetic/bank checks passed including tax 164.71 at the 7% master tax rate. However, payment history already contains a paid invoice for the same vendor, same PO, and same total amount 2517.76 (invoice INV-25-107 paid on 2025-06-14), so this invoice must be rejected as DUPLICATE."
}
```


## Case: ALS-INV-107

**Step 1 — LLM call** (agent: `extractor`, 527+231 tok, 3.32s)
- assistant said:

```
{"invoice_no":"ALS-INV-107","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-05","po_number":"PO-2025-4122","currency":"USD","lines":[{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":27,"unit_price":425.00,"amount":11475.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":23,"unit_price":45.00,"amount":1035.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":8,"unit_price":18.50,"amount":148.00},{"sku":"AL-FUEL","description":"Fuel surcharge","qty":17,"unit_price":63.75,"amount":1083.75}],"subtotal":13741.75,"tax":0.00,"total":13741.75,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1800+85 tok, 14.75s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4122"})`
- agent called `get_received_totals({"po_number": "PO-2025-4122"})`
- agent called `get_vendor_by_name({"name": "AURIGA LOGISTICS SERVICES"})`

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

**Step 7 — LLM call** (agent: `matcher`, 2234+81 tok, 2.56s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id": "V06", "po_number": "PO-2025-4122", "total": 13741.75, "invoice_no": "ALS-INV-107"})`
- agent called `arithmetic_check({"vendor_id": "V06"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": [{"invoice_no": "ALS-INV-107", "vendor_id": "V06", "po_number": "PO-2025-4122", "amount": 13741.75, "currency": "USD", "paid_date": "2025-07-02", "match_reasons": ["invoice number already paid (normalized match)", "same vendor + PO + amount already paid"]}]}
```

**Step 9 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 10 — LLM call** (agent: `matcher`, 2457+172 tok, 3.52s)
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
  "explanation": "PO PO-2025-4122 exists for vendor V06 in USD, all billed quantities match received quantities on GRN-88321 (27, 23, 8, and 17), and the arithmetic/bank checks passed. However, payment history already shows invoice ALS-INV-107 for vendor V06 and PO PO-2025-4122 paid on 2025-07-02 for the same total amount of 13,741.75 USD, so this invoice is a DUPLICATE and must be rejected."
}
```


## Case: NIS-2025-107

**Step 1 — LLM call** (agent: `extractor`, 506+206 tok, 3.43s)
- assistant said:

```
{"invoice_no":"NIS-2025-107","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-21","po_number":"PO-2025-4123","currency":"USD","lines":[{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":17,"unit_price":6.95,"amount":118.15},{"sku":"NG-3305","description":"Absorbent pads, case","qty":6,"unit_price":42.5,"amount":255.0},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":30,"unit_price":149.0,"amount":4470.0}],"subtotal":4843.15,"tax":388.27,"total":5231.42,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1687+84 tok, 2.27s)
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

**Step 7 — LLM call** (agent: `matcher`, 2083+83 tok, 2.64s)
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

**Step 10 — LLM call** (agent: `matcher`, 2258+166 tok, 3.59s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"NIS-2025-107","po_number":"PO-2025-4123","decision":"hold","discrepancies":["TAX_ERROR"],"explanation":"PO PO-2025-4123 exists for vendor V01 in USD, all three invoice line unit prices match the PO (6.95, 42.50, 149.00), and billed quantities 17/6/30 do not exceed received quantities on GRN-88322 (17/6/30). No duplicate payment was found and the remit-to bank matches vendor master, but the arithmetic check flagged TAX_ERROR: invoice tax 388.27 does not match 7.25% of subtotal 4843.15, which is 351.13 within policy tolerance."}
```


## Case: VPL-2025-104

**Step 1 — LLM call** (agent: `extractor`, 506+232 tok, 4.36s)
- assistant said:

```
{"invoice_no":"VPL-2025-104","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-07-02","po_number":"PO-2025-4124","currency":"EUR","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":12,"unit_price":21.40,"amount":256.80},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":28,"unit_price":9.60,"amount":268.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":33,"unit_price":340.00,"amount":11220.00}],"subtotal":11745.60,"tax":2284.26,"total":14029.86,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-104"}`

**Step 3 — LLM call** (agent: `matcher`, 1672+88 tok, 3.13s)
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

**Step 7 — LLM call** (agent: `matcher`, 2094+83 tok, 2.7s)
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

**Step 10 — LLM call** (agent: `matcher`, 2271+188 tok, 4.28s)
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
  "explanation": "PO PO-2025-4124 exists for vendor V09, the invoice currency EUR matches the PO, all billed quantities match received quantities on GRN-88323 (12, 28, and 33), line prices match the PO, the remit-to bank matches vendor master, and no duplicate payment was found. The invoice must be held because tax is incorrect: the invoice shows tax of 2284.26, but at the vendor master tax rate of 0.19 on subtotal 11745.60, the expected tax is 2231.66, which exceeds the $0.02 tolerance."
}
```


## Case: SOI-25-107

**Step 1 — LLM call** (agent: `extractor`, 479+175 tok, 3.09s)
- assistant said:

```
{"invoice_no":"SOI-25-107","vendor_name":"Stellar Office Interiors","date":"2025-07-23","po_number":"PO-2025-4125","currency":"USD","lines":[{"sku":"SO-FIL-3D","description":"File cabinet 3-drawer","qty":26,"unit_price":156.80,"amount":4076.80},{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":18,"unit_price":189.00,"amount":3492.00}],"subtotal":7568.80,"tax":613.07,"total":8181.87,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1559+83 tok, 2.76s)
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

**Step 7 — LLM call** (agent: `matcher`, 1906+82 tok, 2.44s)
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

**Step 10 — LLM call** (agent: `matcher`, 2090+178 tok, 3.54s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"SOI-25-107","po_number":"PO-2025-4125","decision":"hold","discrepancies":["TOTAL_ERROR"],"explanation":"PO PO-2025-4125 exists for vendor V07 in USD, and GRN GRN-88324 shows full receipt of 26 units on line 1 and 18 units on line 2, matching the billed quantities; unit prices also match the PO at 156.80 and 189.00. Payment history returned no duplicate, tax 613.07 matches the vendor tax rate, and bank details match vendor master, but the invoice line for SKU SO-CHR-T2 shows amount 3492.00 while arithmetic_check verified 18 x 189.00 = 3402.00, creating a TOTAL_ERROR and requiring a hold."}
```


## Case: MF/25/107

**Step 1 — LLM call** (agent: `extractor`, 553+258 tok, 3.95s)
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

**Step 7 — LLM call** (agent: `matcher`, 2257+81 tok, 2.68s)
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

**Step 10 — LLM call** (agent: `matcher`, 2439+172 tok, 3.5s)
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
  "explanation": "PO PO-2025-4126 exists for vendor V03, currency matches USD, GRN-88325 covers all billed quantities (15, 5, 39, and 36), prices match the PO, bank details match vendor master, and no duplicate payment was found. However, the invoice fails arithmetic: line SKU MF-M8-NUT shows amount 1021.60, but arithmetic_check verified that 36 x 27.60 = 993.60, creating a TOTAL_ERROR; tax 166.77 was otherwise correct."
}
```


## Case: HEC-2025-110

**Step 1 — LLM call** (agent: `extractor`, 457+186 tok, 3.95s)
- assistant said:

```
{"invoice_no":"HEC-2025-110","vendor_name":"Helios Electrical Components","date":"2025-06-28","po_number":"PO-2025-4127","currency":"USD","lines":[{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":35,"unit_price":96.30,"amount":3370.50},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":12,"unit_price":118.00,"amount":1416.00}],"subtotal":4786.50,"tax":411.64,"total":5198.14,"bank_name":"Meridian Trust Bank","bank_routing":"122100024","bank_account":"7791024468","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-110"}`

**Step 3 — LLM call** (agent: `matcher`, 1514+83 tok, 2.93s)
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

**Step 7 — LLM call** (agent: `matcher`, 1873+83 tok, 2.48s)
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

**Step 10 — LLM call** (agent: `matcher`, 2040+195 tok, 4.8s)
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
  "explanation": "PO PO-2025-4127 exists for vendor V05 in USD, invoice line prices match the PO (HE-PSU-24 at 96.3 and HE-CAB-14 at 118.0), and billed quantities 35 and 12 do not exceed received quantities on GRN-88326. Arithmetic passed including tax 411.64, and no duplicate payment was found; however, the remit-to bank account on the invoice (7791024468, routing 122100024) differs from the vendor master account (3348812706, routing 122100024), so the invoice must be held for bank-change verification."
}
```


## Case: GP-107

**Step 1 — LLM call** (agent: `extractor`, 446+176 tok, 3.34s)
- assistant said:

```
{"invoice_no":"GP-107","vendor_name":"Granite Peak Safety Gear","date":"2025-06-19","po_number":"PO-2025-4128","currency":"USD","lines":[{"sku":"GP-HH-CL2","description":"Hard hats class E, box 20","qty":6,"unit_price":196.00,"amount":1176.00},{"sku":"GP-BOOT-10","description":"Steel toe boots size 10","qty":17,"unit_price":112.00,"amount":1904.00}],"subtotal":3080.00,"tax":184.80,"total":3264.80,"bank_name":"Meridian Trust Bank","bank_routing":"123103729","bank_account":"4456108823","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1498+84 tok, 2.95s)
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

**Step 7 — LLM call** (agent: `matcher`, 1852+79 tok, 2.58s)
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

**Step 10 — LLM call** (agent: `matcher`, 2015+190 tok, 3.95s)
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
  "explanation": "PO PO-2025-4128 exists for vendor V08 in USD, and the invoice matches the PO line prices (6 × 196.00 and 17 × 112.00), received quantities (GRN-88327 shows 6 and 17 received), and arithmetic/tax (subtotal 3080.00, tax 184.80 at 6%, total 3264.80). However, the remit-to bank details do not match vendor master: routing 123103729 matches, but bank account 4456108823 on the invoice differs from master account 2290156841, so the invoice must be held."
}
```


## Case: VPL-2025-107

**Step 1 — LLM call** (agent: `extractor`, 533+230 tok, 3.73s)
- assistant said:

```
{"invoice_no":"VPL-2025-107","vendor_name":"Vireo Print & Label GmbH","date":"2025-06-22","po_number":"PO-2025-4129","currency":"USD","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":39,"unit_price":21.40,"amount":834.60},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":38,"unit_price":9.60,"amount":364.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":35,"unit_price":340.00,"amount":11900.00}],"subtotal":13099.40,"tax":2488.89,"total":15588.29,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1670+86 tok, 2.58s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4129"})`
- agent called `get_received_totals({"po_number": "PO-2025-4129"})`
- agent called `get_vendor_by_name({"name": "Vireo Print & Label GmbH"})`

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

**Step 7 — LLM call** (agent: `matcher`, 2090+83 tok, 2.57s)
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

**Step 10 — LLM call** (agent: `matcher`, 2234+167 tok, 3.63s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "VPL-2025-107",
  "po_number": "PO-2025-4129",
  "decision": "hold",
  "discrepancies": [
    "CURRENCY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4129 exists for vendor V09, all billed quantities match receipts exactly (39, 38, and 35 received on GRN-88328), unit prices match the PO (21.4, 9.6, 340.0), arithmetic passed, bank details match the vendor master, and no duplicate was found. However, the invoice is in USD while the PO and vendor master are in EUR, so this requires a hold for CURRENCY_MISMATCH."
}
```


## Case: AMT-107

**Step 1 — LLM call** (agent: `extractor`, 550+253 tok, 3.75s)
- assistant said:

```
{"invoice_no":"AMT-107","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-20","po_number":"PO-2025-9911","currency":"USD","lines":[{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":10,"unit_price":412.60,"amount":4126.00},{"sku":"AM-END-12","description":"End mill 12mm carbide","qty":21,"unit_price":68.20,"amount":1432.20},{"sku":"AM-VIS-6","description":"Machine vise 6in","qty":31,"unit_price":289.00,"amount":8959.00},{"sku":"AM-INS-CNMG","description":"Turning inserts CNMG, box 10","qty":22,"unit_price":94.80,"amount":2085.60}],"subtotal":16602.80,"tax":0.00,"total":16602.80,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1353+79 tok, 3.41s)
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
{"vendor_id": "V10", "name": "Ashford Machine Tools Ltd.", "city": "Sheffield, UK", "currency": "USD", "payment_terms": "Net 30", "bank_name": "Pennine & Yorkshire Bank", "bank_routing": "GB29 NWBK 6016", "bank_account": "1331 9268 19", "tax_rate": 0.0}
```

**Step 6 — tool `arithmetic_check` responded:**

```
{"arithmetic_and_bank_findings": [], "checks_passed": ["Tax OK (0.00 ~= 0.00).", "Remit-to bank details match vendor master."]}
```

**Step 7 — LLM call** (agent: `matcher`, 1589+47 tok, 2.07s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `search_payments({"vendor_id":"V10","po_number":"PO-2025-9911","total":16602.8,"invoice_no":"AMT-107"})`

**Step 8 — tool `search_payments` responded:**

```
{"potential_duplicates": []}
```

**Step 9 — LLM call** (agent: `matcher`, 1653+142 tok, 3.68s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "AMT-107",
  "po_number": "PO-2025-9911",
  "decision": "hold",
  "discrepancies": ["PO_NOT_FOUND"],
  "explanation": "The referenced purchase order PO-2025-9911 does not exist in the PO system, so the invoice cannot be matched to an authorized PO. Other checked controls passed: no duplicate payment was found for vendor V10 and total 16602.80 / invoice AMT-107, the invoice currency matches the vendor/PO context currency USD, arithmetic checks passed, and the remit-to bank details match the vendor master record."
}
```


## Case: NIS-2025-110

**Step 1 — LLM call** (agent: `extractor`, 538+243 tok, 3.69s)
- assistant said:

```
{"invoice_no":"NIS-2025-110","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-15","po_number":"PO-2025-4131","currency":"USD","lines":[{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":10,"unit_price":20.24,"amount":202.40},{"sku":"NG-3305","description":"Absorbent pads, case","qty":24,"unit_price":42.50,"amount":1020.00},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":6,"unit_price":149.00,"amount":894.00},{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":17,"unit_price":6.95,"amount":118.15}],"subtotal":2234.55,"tax":162.00,"total":2396.55,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-110"}`

**Step 3 — LLM call** (agent: `matcher`, 1828+84 tok, 3.1s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- agent called `get_po({"po_number": "PO-2025-4131"})`
- agent called `get_vendor_by_name({"name": "Northgate Industrial Supply LLC"})`
- agent called `get_received_totals({"po_number": "PO-2025-4131"})`

**Step 4 — tool `get_po` responded:**

```
{"po_number": "PO-2025-4131", "vendor_id": "V01", "date": "2025-05-10", "currency": "USD", "lines": [{"line_no": 1, "sku": "NG-4410", "description": "Nitrile work gloves, box of 100", "qty": 10, "unit_price": 18.4}, {"line_no": 2, "sku": "NG-3305", "description": "Absorbent pads, case", "qty": 24, "unit_price": 42.5}, {"line_no": 3, "sku": "NG-1180", "description": "Steel shelving unit 72in", "qty": 6, "unit_price": 149.0}, {"line_no": 4, "sku": "NG-7720", "description": "Safety goggles, anti-fog", "qty": 17, "unit_price": 6.95}], "status": "open"}
```

**Step 5 — tool `get_vendor_by_name` responded:**

```
{"vendor_id": "V01", "name": "Northgate Industrial Supply LLC", "city": "Columbus, OH", "currency": "USD", "payment_terms": "Net 60", "bank_name": "First Commerce Bank", "bank_routing": "021000021", "bank_account": "4402198837", "tax_rate": 0.0725}
```

**Step 6 — tool `get_received_totals` responded:**

```
{"received_by_line_no": {"1": 5, "2": 12, "3": 3, "4": 8}, "grn_count": 1, "grn_numbers": ["GRN-88330"]}
```

**Step 7 — LLM call** (agent: `matcher`, 2276+83 tok, 2.75s)
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

**Step 10 — LLM call** (agent: `matcher`, 2418+189 tok, 4.57s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{"invoice_id":"NIS-2025-110","po_number":"PO-2025-4131","decision":"hold","discrepancies":["PRICE_MISMATCH","QTY_MISMATCH"],"explanation":"PO PO-2025-4131 exists in USD for vendor V01, and no duplicate payment was found for invoice NIS-2025-110; arithmetic, tax, total, and bank details all passed. However, invoice line SKU NG-4410 bills unit price 20.24 versus PO price 18.40, which exceeds the 0.5% tolerance, and billed quantities exceed received quantities on all lines: line 1 billed 10 vs received 5, line 2 billed 24 vs 12, line 3 billed 6 vs 3, and line 4 billed 17 vs 8 based on GRN-88330."}
```


## Case: CCW-107

**Step 1 — LLM call** (agent: `extractor`, 521+220 tok, 3.55s)
- assistant said:

```
{"invoice_no":"CCW-107","vendor_name":"Cascadia Chemical Works","date":"2025-06-04","po_number":"PO-2025-4132","currency":"USD","lines":[{"sku":"CC-COOL-55","description":"Machine coolant concentrate, 55gal","qty":37,"unit_price":744.50,"amount":27546.50},{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":21,"unit_price":87.40,"amount":1835.40},{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":8,"unit_price":612.00,"amount":4896.00}],"subtotal":34277.90,"tax":3300.50,"total":37578.40,"bank_name":"Meridian Trust Bank","bank_routing":"125000024","bank_account":"6120087745","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-107"}`

**Step 3 — LLM call** (agent: `matcher`, 1717+84 tok, 2.4s)
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

**Step 7 — LLM call** (agent: `matcher`, 2126+80 tok, 2.86s)
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

**Step 10 — LLM call** (agent: `matcher`, 2326+212 tok, 4.02s)
- tools offered: get_po, get_received_totals, get_vendor_by_name, search_payments, arithmetic_check
- assistant said:

```
{
  "invoice_id": "CCW-107",
  "po_number": "PO-2025-4132",
  "decision": "hold",
  "discrepancies": ["TAX_ERROR", "BANK_CHANGE"],
  "explanation": "PO PO-2025-4132 exists for vendor V04 in USD, and the invoice line prices match the PO exactly (744.50, 87.40, and 612.00); received quantities also fully support the billed quantities via GRN-88331 (37, 21, and 8 received). However, the arithmetic check found tax of 3300.50 versus expected tax of 3256.40 at the vendor master tax rate of 9.5% on subtotal 34277.90, exceeding the $0.02 tolerance, and the remit-to bank account 6120087745 differs from the vendor master account 9027481133 (routing 125000024 matches). No duplicate payment was found."
}
```
