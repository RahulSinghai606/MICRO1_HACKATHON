# Agent trajectories — run `agent_v1`


## Case: NIS-2025-101

**Step 1 — LLM call** (agent: `extractor`, 538+243 tok, 4.09s)
- assistant said:

```
{"invoice_no":"NIS-2025-101","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-18","po_number":"PO-2025-4101","currency":"USD","lines":[{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":3,"unit_price":18.40,"amount":55.20},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":7,"unit_price":149.00,"amount":1043.00},{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":15,"unit_price":6.95,"amount":104.25},{"sku":"NG-3305","description":"Absorbent pads, case","qty":16,"unit_price":42.50,"amount":680.00}],"subtotal":1882.45,"tax":136.48,"total":2018.93,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-101"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1554+220 tok, 4.07s)
- assistant said:

```
{
  "invoice_id": "NIS-2025-101",
  "po_number": "PO-2025-4101",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4101 exists and matches the invoice in currency (USD), vendor bank details (routing 021000021, account 4402198837), and all line unit prices and billed quantities: 3/3 for NG-4410, 7/7 for NG-1180, 15/15 for NG-7720, and 16/16 for NG-3305 against GRN-88301. Invoice arithmetic is consistent within tolerance: line amounts sum to subtotal 1882.45, tax 136.48 matches the vendor tax rate of 7.25% on 1882.45, and total 2018.93 equals subtotal plus tax. No duplicate invoice number or same vendor+PO+amount payment was found in payment history."
}
```


## Case: INV-2025-0101

**Step 1 — LLM call** (agent: `extractor`, 446+178 tok, 3.11s)
- assistant said:

```
{"invoice_no":"INV-2025-0101","vendor_name":"Bluefin Packaging Co.","date":"2025-06-25","po_number":"PO-2025-4102","currency":"USD","lines":[{"sku":"BP-450","description":"Foam inserts, custom cut","qty":30,"unit_price":4.15,"amount":124.50},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":39,"unit_price":31.25,"amount":1218.75}],"subtotal":1343.25,"tax":94.03,"total":1437.28,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0101"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1287+198 tok, 3.96s)
- assistant said:

```
{
  "invoice_id": "INV-2025-0101",
  "po_number": "PO-2025-4102",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4102 exists and matches the invoice in currency (USD), vendor bank details, and unit prices: BP-450 at 4.15 and BP-201 at 31.25. GRN-88302 shows 30 received for BP-450 and 39 received for BP-201, matching billed quantities exactly, and the invoice arithmetic is consistent: line amounts 124.50 and 1218.75 sum to subtotal 1343.25, tax 94.03 matches 7% within tolerance, and total 1437.28 equals subtotal plus tax. No duplicate invoice number or same vendor+PO+amount match appears in payment history."
}
```


## Case: MF/25/101

**Step 1 — LLM call** (agent: `extractor`, 487+182 tok, 3.27s)
- assistant said:

```
{"invoice_no":"MF/25/101","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-07-04","po_number":"PO-2025-4103","currency":"USD","lines":[{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":19,"unit_price":62.75,"amount":1192.25},{"sku":"MF-M8-NUT","description":"Hex nuts M8 zinc, box 1000","qty":11,"unit_price":27.6,"amount":303.6}],"subtotal":1495.85,"tax":89.75,"total":1585.6,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/101"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1231+212 tok, 3.78s)
- assistant said:

```
{
  "invoice_id": "MF/25/101",
  "po_number": "PO-2025-4103",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4103 exists, matches vendor V03, and the invoice currency USD matches the PO and vendor master. Line prices match the PO exactly (MF-ANC-10 at 62.75 and MF-M8-NUT at 27.60), billed quantities 19 and 11 do not exceed GRN-88303 received quantities 19 and 11, remit-to bank details match the vendor master exactly, and there is no payment history indicating a duplicate. Arithmetic is consistent: line amounts 1192.25 and 303.60 sum to subtotal 1495.85, tax 89.75 matches 6% of subtotal within tolerance, and total 1585.60 equals subtotal plus tax."
}
```


## Case: CCW-101

**Step 1 — LLM call** (agent: `extractor`, 489+183 tok, 3.71s)
- assistant said:

```
{"invoice_no":"CCW-101","vendor_name":"Cascadia Chemical Works","date":"2025-06-24","po_number":"PO-2025-4104","currency":"USD","lines":[{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":24,"unit_price":87.40,"amount":2097.60},{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":24,"unit_price":612.00,"amount":14688.00}],"subtotal":16785.60,"tax":1594.63,"total":18380.23,"bank_name":"Puget Sound Trust","bank_routing":"125000024","bank_account":"9027481133","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-101"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1301+198 tok, 4.39s)
- assistant said:

```
{
  "invoice_id": "CCW-101",
  "po_number": "PO-2025-4104",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4104 exists and matches the invoice in USD for vendor V04; billed quantities match the GRN totals (24 received and billed for both CC-DEG-5 and CC-IPA-55), and unit prices match the PO exactly at 87.40 and 612.00. Invoice arithmetic is consistent: line amounts 2,097.60 and 14,688.00 sum to subtotal 16,785.60, tax 1,594.63 matches the 9.5% vendor tax rate within tolerance, total 18,380.23 equals subtotal plus tax, bank details match the vendor master, and no duplicate invoice/payment history match was found."
}
```


## Case: HEC-2025-101

**Step 1 — LLM call** (agent: `extractor`, 481+216 tok, 4.27s)
- assistant said:

```
{"invoice_no":"HEC-2025-101","vendor_name":"Helios Electrical Components","date":"2025-06-02","po_number":"PO-2025-4105","currency":"USD","lines":[{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":37,"unit_price":9.85,"amount":364.45},{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":20,"unit_price":14.20,"amount":284.00},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":25,"unit_price":96.30,"amount":2407.50}],"subtotal":3055.95,"tax":262.81,"total":3318.76,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-101"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1369+212 tok, 4.05s)
- assistant said:

```
{
  "invoice_id": "HEC-2025-101",
  "po_number": "PO-2025-4105",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4105 exists, invoice currency USD matches the PO and vendor master, all billed unit prices match the PO (9.85, 14.20, 96.30), and billed quantities 37/20/25 do not exceed the GRN receipt quantities 37/20/25. Invoice arithmetic is consistent (line amounts 364.45, 284.00, and 2407.50 sum to subtotal 3055.95; tax 262.81 matches 8.6% of subtotal within $0.02; total 3318.76 equals subtotal plus tax), bank routing/account 122100024 / 3348812706 matches vendor master, and there is no duplicate in payment history."
}
```


## Case: ALS-INV-101

**Step 1 — LLM call** (agent: `extractor`, 525+230 tok, 3.67s)
- assistant said:

```
{"invoice_no":"ALS-INV-101","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-06","po_number":"PO-2025-4106","currency":"USD","lines":[{"sku":"AL-FUEL","description":"Fuel surcharge","qty":8,"unit_price":63.75,"amount":510.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":26,"unit_price":18.50,"amount":481.00},{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":19,"unit_price":425.00,"amount":8075.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":31,"unit_price":45.00,"amount":1395.00}],"subtotal":10461.00,"tax":0.00,"total":10461.00,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-101"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1525+180 tok, 4.29s)
- assistant said:

```
{
  "invoice_id": "ALS-INV-101",
  "po_number": "PO-2025-4106",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4106 exists and matches the invoice in USD; all invoice unit prices match the PO exactly, and billed quantities match the received quantities on GRN-88306 (8, 26, 19, and 31 respectively). Invoice arithmetic is consistent: line amounts sum to subtotal 10461.00, tax 0.00 matches the vendor tax rate of 0.0, total equals 10461.00, the remit-to bank details match the vendor master exactly, and no duplicate invoice or paid invoice with the same vendor, PO, and amount appears in payment history."
}
```


## Case: SOI-25-101

**Step 1 — LLM call** (agent: `extractor`, 508+208 tok, 3.14s)
- assistant said:

```
{"invoice_no":"SOI-25-101","vendor_name":"Stellar Office Interiors","date":"2025-06-06","po_number":"PO-2025-4107","currency":"USD","lines":[{"sku":"SO-MON-ARM","description":"Dual monitor arm","qty":6,"unit_price":74.25,"amount":445.50},{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":40,"unit_price":189.00,"amount":7560.00},{"sku":"SO-DSK-60","description":"Sit-stand desk 60in","qty":12,"unit_price":415.00,"amount":4980.00}],"subtotal":12985.50,"tax":1051.83,"total":14037.33,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-101"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1418+189 tok, 3.95s)
- assistant said:

```
{
  "invoice_id": "SOI-25-101",
  "po_number": "PO-2025-4107",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4107 exists, invoice currency USD matches the PO and vendor master, and billed quantities match GRN-88307 receipts exactly: 6 SO-MON-ARM, 40 SO-CHR-T2, and 12 SO-DSK-60. Line prices match the PO at 74.25, 189.00, and 415.00, arithmetic is consistent (subtotal 12,985.50, tax 1,051.83 at 8.1%, total 14,037.33), remit-to bank details match the vendor master, and no duplicate invoice/payment history match was found."
}
```


## Case: GP-101

**Step 1 — LLM call** (agent: `extractor`, 479+214 tok, 4.76s)
- assistant said:

```
{"invoice_no":"GP-101","vendor_name":"Granite Peak Safety Gear","date":"2025-07-13","po_number":"PO-2025-4108","currency":"USD","lines":[{"sku":"GP-EAR-200","description":"Ear plugs, box 200 pr","qty":22,"unit_price":38.90,"amount":855.80},{"sku":"GP-VIS-XL","description":"Hi-vis vests XL, pack 10","qty":5,"unit_price":84.50,"amount":422.50},{"sku":"GP-HH-CL2","description":"Hard hats class E, box 20","qty":16,"unit_price":196.00,"amount":3136.00}],"subtotal":4414.30,"tax":264.86,"total":4679.16,"bank_name":"Sawtooth Community Bank","bank_routing":"123103729","bank_account":"2290156841","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-101"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1368+180 tok, 4.77s)
- assistant said:

```
{
  "invoice_id": "GP-101",
  "po_number": "PO-2025-4108",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4108 exists, invoice currency USD matches the PO and vendor master, and all billed quantities match received quantities on GRN-88308 (22, 5, and 16 respectively). Unit prices match the PO exactly (38.9, 84.5, 196.0), remit-to bank details match the vendor master exactly, there is no payment history indicating a duplicate, and the invoice arithmetic is consistent: line amounts sum to subtotal 4414.30, tax 264.86 matches 6% of subtotal, and total 4679.16 equals subtotal plus tax."
}
```


## Case: VPL-2025-101

**Step 1 — LLM call** (agent: `extractor`, 506+232 tok, 3.52s)
- assistant said:

```
{"invoice_no":"VPL-2025-101","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-06-09","po_number":"PO-2025-4109","currency":"EUR","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":15,"unit_price":21.40,"amount":321.00},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":33,"unit_price":9.60,"amount":316.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":27,"unit_price":340.00,"amount":9180.00}],"subtotal":9817.80,"tax":1865.38,"total":11683.18,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-101"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1398+189 tok, 4.16s)
- assistant said:

```
{
  "invoice_id": "VPL-2025-101",
  "po_number": "PO-2025-4109",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4109 exists, invoice currency EUR matches the PO, all billed unit prices match the PO exactly (21.4, 9.6, 340.0), and billed quantities 15, 33, and 27 do not exceed the received quantities on GRN-88309. The remit-to bank details match the vendor master exactly, there is no payment history indicating a duplicate, and the invoice arithmetic is consistent: line amounts sum to subtotal 9817.80, tax 1865.38 matches 19% within $0.02, and total 11683.18 equals subtotal plus tax."
}
```


## Case: AMT-101

**Step 1 — LLM call** (agent: `extractor`, 485+181 tok, 3.17s)
- assistant said:

```
{"invoice_no":"AMT-101","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-19","po_number":"PO-2025-4110","currency":"USD","lines":[{"sku":"AM-VIS-6","description":"Machine vise 6in","qty":37,"unit_price":289.00,"amount":10693.00},{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":36,"unit_price":412.60,"amount":14853.60}],"subtotal":25546.60,"tax":0.00,"total":25546.60,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-101"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1231+182 tok, 4.62s)
- assistant said:

```
{
  "invoice_id": "AMT-101",
  "po_number": "PO-2025-4110",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4110 exists, invoice currency USD matches the PO, and billed quantities match receipts exactly: AM-VIS-6 billed 37 vs GRN received 37, and AM-CHK-125 billed 36 vs GRN received 36. Unit prices match the PO exactly (289.00 and 412.60), remit-to bank details match the vendor master, there is no payment history indicating a duplicate, and the invoice arithmetic is consistent with subtotal 25,546.60, tax 0.00 at a 0.0 tax rate, and total 25,546.60."
}
```


## Case: NIS-2025-104

**Step 1 — LLM call** (agent: `extractor`, 527+219 tok, 3.94s)
- assistant said:

```
{"invoice_no":"NIS-2025-104","vendor_name":"Northgate Ind. Supply (a div. of NIS Holdings)","date":"2025-06-05","po_number":"PO-2025-4111","currency":"USD","lines":[{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":34,"unit_price":149.00,"amount":5066.00},{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":33,"unit_price":18.40,"amount":607.20},{"sku":"NG-3305","description":"Absorbent pads, case","qty":7,"unit_price":42.50,"amount":297.50}],"subtotal":5970.70,"tax":432.88,"total":6403.58,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-104"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1567+220 tok, 5.52s)
- assistant said:

```
{
  "invoice_id": "NIS-2025-104",
  "po_number": "PO-2025-4111",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4111 exists, invoice currency USD matches the PO and vendor master, and remit-to bank details match exactly: routing 021000021 and account 4402198837. Billed quantities match total received across GRNs (NG-1180: 34 vs 17+17, NG-4410: 33 vs 16+17, NG-3305: 7 vs 3+4), unit prices match the PO exactly, and invoice arithmetic is consistent: line amounts total 5970.70, tax 432.88 matches 7.25% of 5970.70 within tolerance, and total 6403.58 equals subtotal plus tax. No duplicate invoice number or same vendor+PO+amount paid record appears in payment history."
}
```


## Case: HEC-2025-104

**Step 1 — LLM call** (agent: `extractor`, 517+256 tok, 4.41s)
- assistant said:

```
{"invoice_no":"HEC-2025-104","vendor_name":"Helios Electrical Components","date":"2025-06-22","po_number":"PO-2025-4112","currency":"USD","lines":[{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":26,"unit_price":14.20,"amount":369.20},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":26,"unit_price":118.00,"amount":3068.00},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":40,"unit_price":96.30,"amount":3852.00},{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":31,"unit_price":9.85,"amount":305.35}],"subtotal":7594.55,"tax":653.14,"total":8247.69,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-104"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1516+212 tok, 5.84s)
- assistant said:

```
{
  "invoice_id": "HEC-2025-104",
  "po_number": "PO-2025-4112",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4112 exists, the invoice currency USD matches the PO and vendor master, and all four billed unit prices match the PO exactly (14.20, 118.00, 96.30, 9.85). GRN GRN-88313 shows received quantities exactly matching billed quantities for all lines (26, 26, 40, 31), the remit-to bank details match the vendor master exactly, there is no payment history indicating a duplicate, and the invoice arithmetic is consistent: line amounts roll up to subtotal 7594.55, tax 653.14 matches the 8.6% tax rate within tolerance, and total 8247.69 equals subtotal plus tax."
}
```


## Case: MF/25/104

**Step 1 — LLM call** (agent: `extractor`, 551+257 tok, 4.74s)
- assistant said:

```
{"invoice_no":"MF/25/104","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-07-17","po_number":"PO-2025-4113","currency":"USD","lines":[{"sku":"MF-M8-50","description":"Hex bolts M8x50 zinc, box 500","qty":9,"unit_price":49.28,"amount":443.52},{"sku":"MF-W-8","description":"Flat washers 8mm, box 1000","qty":20,"unit_price":15.30,"amount":306.00},{"sku":"MF-M8-NUT","description":"Hex nuts M8 zinc, box 1000","qty":29,"unit_price":27.60,"amount":800.40},{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":12,"unit_price":62.75,"amount":753.00}],"subtotal":2302.92,"tax":138.18,"total":2441.10,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/104"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1517+201 tok, 4.28s)
- assistant said:

```
{
  "invoice_id": "MF/25/104",
  "po_number": "PO-2025-4113",
  "decision": "hold",
  "discrepancies": [
    "PRICE_MISMATCH"
  ],
  "explanation": "PO PO-2025-4113 exists in USD and has matching GRN quantities received for all billed lines (9, 20, 29, and 12 respectively), with matching bank details and no payment-history duplicate. The invoice line for SKU MF-M8-50 bills unit price 49.28 versus PO unit price 44.00, which exceeds the 0.5% tolerance, so PRICE_MISMATCH applies. All other arithmetic checks align: line amounts sum to subtotal 2302.92, tax 138.18 matches 6% of subtotal, and total 2441.10 equals subtotal plus tax."
}
```


## Case: SOI-25-104

**Step 1 — LLM call** (agent: `extractor`, 475+171 tok, 3.34s)
- assistant said:

```
{"invoice_no":"SOI-25-104","vendor_name":"Stellar Office Interiors","date":"2025-06-12","po_number":"PO-2025-4114","currency":"USD","lines":[{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":21,"unit_price":204.12,"amount":4286.52},{"sku":"SO-MON-ARM","description":"Dual monitor arm","qty":34,"unit_price":74.25,"amount":2524.5}],"subtotal":6811.02,"tax":551.69,"total":7362.71,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-104"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1276+223 tok, 3.94s)
- assistant said:

```
{
  "invoice_id": "SOI-25-104",
  "po_number": "PO-2025-4114",
  "decision": "hold",
  "discrepancies": [
    "PRICE_MISMATCH"
  ],
  "explanation": "PO PO-2025-4114 exists, has a GRN covering the full received quantities (21 of SO-CHR-T2 and 34 of SO-MON-ARM), and the invoice currency, bank details, and duplicate screening all match/clear. The invoice line for SKU SO-CHR-T2 bills unit price 204.12 versus PO unit price 189.00, which exceeds the 0.5% tolerance; SKU SO-MON-ARM matches at 74.25. Invoice arithmetic is consistent: line amounts 4286.52 and 2524.50 sum to subtotal 6811.02, tax 551.69 matches 8.1% of subtotal within tolerance, and total 7362.71 equals subtotal plus tax."
}
```


## Case: AMT-104

**Step 1 — LLM call** (agent: `extractor`, 485+181 tok, 2.99s)
- assistant said:

```
{"invoice_no":"AMT-104","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-27","po_number":"PO-2025-4115","currency":"USD","lines":[{"sku":"AM-END-12","description":"End mill 12mm carbide","qty":22,"unit_price":78.43,"amount":1725.46},{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":33,"unit_price":412.60,"amount":13615.80}],"subtotal":15341.26,"tax":0.00,"total":15341.26,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-104"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1230+209 tok, 4.09s)
- assistant said:

```
{
  "invoice_id": "AMT-104",
  "po_number": "PO-2025-4115",
  "decision": "hold",
  "discrepancies": [
    "PRICE_MISMATCH",
    "TOTAL_ERROR"
  ],
  "explanation": "PO PO-2025-4115 exists, has matching currency USD, a GRN is present, billed quantities match received quantities (22 and 33), bank details match the vendor master, and there is no duplicate in payment history. However, line AM-END-12 is billed at 78.43 versus the PO unit price of 68.20, which exceeds the 0.5% tolerance, and the invoice line amount for that line is incorrect because 22 × 78.43 = 1725.46 does not reconcile within the $0.02 tolerance. Because non-duplicate discrepancies are present, the invoice must be placed on hold."
}
```


## Case: INV-2025-0104

**Step 1 — LLM call** (agent: `extractor`, 473+210 tok, 3.34s)
- assistant said:

```
{"invoice_no":"INV-2025-0104","vendor_name":"Bluefin Packaging Co.","date":"2025-06-25","po_number":"PO-2025-4116","currency":"USD","lines":[{"sku":"BP-115","description":"Stretch wrap roll 80ga","qty":38,"unit_price":12.80,"amount":486.40},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":7,"unit_price":31.25,"amount":218.75},{"sku":"BP-330","description":"Packing tape, case of 36","qty":7,"unit_price":58.90,"amount":412.30}],"subtotal":1117.45,"tax":78.22,"total":1195.67,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0104"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1418+169 tok, 4.53s)
- assistant said:

```
{
  "invoice_id": "INV-2025-0104",
  "po_number": "PO-2025-4116",
  "decision": "hold",
  "discrepancies": [
    "QTY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4116 exists and matches the invoice currency (USD), unit prices, vendor bank details, and invoice arithmetic; no duplicate was found in payment history. However, billed quantities exceed received quantities on all three lines: BP-115 billed 38 vs received 22, BP-201 billed 7 vs received 4, and BP-330 billed 7 vs received 4 on GRN-88317, so the invoice must be held for QTY_MISMATCH."
}
```


## Case: HEC-2025-107

**Step 1 — LLM call** (agent: `extractor`, 517+256 tok, 3.89s)
- assistant said:

```
{"invoice_no":"HEC-2025-107","vendor_name":"Helios Electrical Components","date":"2025-06-23","po_number":"PO-2025-4117","currency":"USD","lines":[{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":18,"unit_price":14.20,"amount":255.60},{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":35,"unit_price":9.85,"amount":344.75},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":40,"unit_price":96.30,"amount":3852.00},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":29,"unit_price":118.00,"amount":3422.00}],"subtotal":7874.35,"tax":677.19,"total":8551.54,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-107"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1516+185 tok, 4.6s)
- assistant said:

```
{
  "invoice_id": "HEC-2025-107",
  "po_number": "PO-2025-4117",
  "decision": "hold",
  "discrepancies": [
    "QTY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4117 exists, the invoice currency matches USD, line unit prices match the PO, arithmetic is consistent, and the remit-to bank details match vendor V05. However, the invoice bills quantities above total received on the only GRN: HE-REL-24 billed 18 vs received 10, HE-CB-20 billed 35 vs 21, HE-PSU-24 billed 40 vs 24, and HE-CAB-14 billed 29 vs 17, so the invoice must be held for QTY_MISMATCH."
}
```


## Case: GP-104

**Step 1 — LLM call** (agent: `extractor`, 480+213 tok, 4.52s)
- assistant said:

```
{"invoice_no":"GP-104","vendor_name":"Granite Peak Safety Gear","date":"2025-06-03","po_number":"PO-2025-4118","currency":"USD","lines":[{"sku":"GP-EAR-200","description":"Ear plugs, box 200 pr","qty":30,"unit_price":38.90,"amount":1167.00},{"sku":"GP-BOOT-10","description":"Steel toe boots size 10","qty":35,"unit_price":112.00,"amount":3920.00},{"sku":"GP-VIS-XL","description":"Hi-vis vests XL, pack 10","qty":30,"unit_price":84.50,"amount":2535.00}],"subtotal":7622.00,"tax":457.32,"total":8079.32,"bank_name":"Sawtooth Community Bank","bank_routing":"123103729","bank_account":"2290156841","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-104"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1363+212 tok, 4.09s)
- assistant said:

```
{
  "invoice_id": "GP-104",
  "po_number": "PO-2025-4118",
  "decision": "hold",
  "discrepancies": [
    "QTY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4118 exists and matches the invoice in USD, with unit prices matching the PO on all lines (GP-EAR-200 at 38.90, GP-BOOT-10 at 112.00, GP-VIS-XL at 84.50). However, the invoice bills quantities of 30, 35, and 30, while the only GRN on file (GRN-88319) shows received quantities of 18, 21, and 18 respectively, so billed quantities exceed received quantities on every line. Bank details match the vendor master, no duplicate is present in payment history, and the invoice arithmetic and 6% tax are consistent with the stated subtotal and total."
}
```


## Case: CCW-104

**Step 1 — LLM call** (agent: `extractor`, 518+218 tok, 3.49s)
- assistant said:

```
{"invoice_no":"CCW-104","vendor_name":"Cascadia Chemical Works","date":"2025-06-28","po_number":"PO-2025-4119","currency":"USD","lines":[{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":2,"unit_price":612.00,"amount":1224.00},{"sku":"CC-COOL-55","description":"Machine coolant concentrate, 55gal","qty":6,"unit_price":744.50,"amount":4467.00},{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":5,"unit_price":87.40,"amount":437.00}],"subtotal":6128.00,"tax":582.16,"total":6710.16,"bank_name":"Puget Sound Trust","bank_routing":"125000024","bank_account":"9027481133","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-104"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1300+196 tok, 4.19s)
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
  "explanation": "PO PO-2025-4119 exists and matches the invoice currency (USD), line unit prices (612.00, 744.50, 87.40), and vendor bank details. However, no GRNs exist for this PO, so received quantity is 0 for all lines while the invoice bills quantities of 2, 6, and 5; therefore GRN_MISSING applies and each billed quantity exceeds received quantity, causing QTY_MISMATCH. No duplicate was found in payment history for invoice CCW-104 or for the same vendor + PO + total 6710.16."
}
```


## Case: ALS-INV-104

**Step 1 — LLM call** (agent: `extractor`, 502+202 tok, 3.18s)
- assistant said:

```
{"invoice_no":"ALS-INV-104","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-08","po_number":"PO-2025-4120","currency":"USD","lines":[{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":19,"unit_price":425.00,"amount":8075.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":33,"unit_price":45.00,"amount":1485.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":15,"unit_price":18.50,"amount":277.50}],"subtotal":9837.50,"tax":0.00,"total":9837.50,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-104"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1266+232 tok, 4.27s)
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
  "explanation": "PO PO-2025-4120 exists and matches the invoice on currency (USD), line prices (425.00, 45.00, 18.50), bank details, and arithmetic: line amounts 8,075.00, 1,485.00, and 277.50 sum to subtotal 9,837.50, tax 0.00 matches the 0.0 tax rate, and total 9,837.50 is correct. However, no GRNs were found for this PO, so received quantity is 0 for all lines; the invoice bills quantities of 19, 33, and 15, which exceed received quantities, so GRN_MISSING and QTY_MISMATCH apply. No duplicate was found in payment history."
}
```


## Case: INV-2025-0107

**Step 1 — LLM call** (agent: `extractor`, 475+211 tok, 5.03s)
- assistant said:

```
{"invoice_no":"INV-2025-0107","vendor_name":"Bluefin Packaging Co.","date":"2025-07-28","po_number":"PO-2025-4121","currency":"USD","lines":[{"sku":"BP-450","description":"Foam inserts, custom cut","qty":8,"unit_price":4.15,"amount":33.20},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":29,"unit_price":31.25,"amount":906.25},{"sku":"BP-330","description":"Packing tape, case of 36","qty":24,"unit_price":58.90,"amount":1413.60}],"subtotal":2353.05,"tax":164.71,"total":2517.76,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0107"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1419+226 tok, 4.19s)
- assistant said:

```
{
  "invoice_id": "INV-2025-0107",
  "po_number": "PO-2025-4121",
  "decision": "reject",
  "discrepancies": [
    "DUPLICATE"
  ],
  "explanation": "PO PO-2025-4121 exists in USD, invoice line prices match the PO (4.15, 31.25, 58.9), billed quantities (8, 29, 24) do not exceed received quantities on GRN-88320, tax 164.71 equals 7% of subtotal 2353.05 within tolerance, total 2517.76 equals subtotal plus tax, and the remit-to bank matches vendor V02. However, payment history already shows invoice number INV-25-107 for vendor V02, which is the same invoice number in different formatting as INV-2025-0107, and it was already paid for the same PO and amount 2517.76, so this invoice must be rejected as a duplicate."
}
```


## Case: ALS-INV-107

**Step 1 — LLM call** (agent: `extractor`, 527+231 tok, 3.79s)
- assistant said:

```
{"invoice_no":"ALS-INV-107","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-05","po_number":"PO-2025-4122","currency":"USD","lines":[{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":27,"unit_price":425.00,"amount":11475.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":23,"unit_price":45.00,"amount":1035.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":8,"unit_price":18.50,"amount":148.00},{"sku":"AL-FUEL","description":"Fuel surcharge","qty":17,"unit_price":63.75,"amount":1083.75}],"subtotal":13741.75,"tax":0.00,"total":13741.75,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-107"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1526+217 tok, 3.71s)
- assistant said:

```
{
  "invoice_id": "ALS-INV-107",
  "po_number": "PO-2025-4122",
  "decision": "reject",
  "discrepancies": [
    "DUPLICATE"
  ],
  "explanation": "PO PO-2025-4122 exists, invoice currency USD matches the PO, billed quantities match the GRN totals exactly (27, 23, 8, and 17), unit prices match the PO exactly ($425.00, $45.00, $18.50, and $63.75), arithmetic is consistent (subtotal $13,741.75, tax $0.00, total $13,741.75), and the remit bank details match the vendor master. However, this invoice is a duplicate because payment history already shows invoice number ALS-INV-107 for vendor V06 on PO PO-2025-4122, amount $13,741.75, paid on 2025-07-02."
}
```


## Case: NIS-2025-107

**Step 1 — LLM call** (agent: `extractor`, 506+206 tok, 3.62s)
- assistant said:

```
{"invoice_no":"NIS-2025-107","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-21","po_number":"PO-2025-4123","currency":"USD","lines":[{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":17,"unit_price":6.95,"amount":118.15},{"sku":"NG-3305","description":"Absorbent pads, case","qty":6,"unit_price":42.50,"amount":255.00},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":30,"unit_price":149.00,"amount":4470.00}],"subtotal":4843.15,"tax":388.27,"total":5231.42,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-107"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1413+205 tok, 4.37s)
- assistant said:

```
{
  "invoice_id": "NIS-2025-107",
  "po_number": "PO-2025-4123",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4123 exists and matches the invoice in USD; all three invoice line unit prices match the PO exactly (6.95, 42.50, 149.00), and billed quantities 17, 6, and 30 do not exceed the GRN received quantities 17, 6, and 30. Invoice arithmetic is consistent: line amounts sum to subtotal 4843.15, tax 388.27 matches the vendor tax rate of 7.25% on the subtotal within tolerance, and total 5231.42 equals subtotal plus tax; bank routing 021000021 and account 4402198837 match vendor master, and no duplicate invoice/payment record is present."
}
```


## Case: VPL-2025-104

**Step 1 — LLM call** (agent: `extractor`, 506+232 tok, 3.39s)
- assistant said:

```
{"invoice_no":"VPL-2025-104","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-07-02","po_number":"PO-2025-4124","currency":"EUR","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":12,"unit_price":21.40,"amount":256.80},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":28,"unit_price":9.60,"amount":268.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":33,"unit_price":340.00,"amount":11220.00}],"subtotal":11745.60,"tax":2284.26,"total":14029.86,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-104"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1398+185 tok, 3.74s)
- assistant said:

```
{
  "invoice_id": "VPL-2025-104",
  "po_number": "PO-2025-4124",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4124 exists and matches the invoice currency (EUR). All invoice line prices match the PO exactly (21.4, 9.6, 340.0), billed quantities match total received quantities on GRN-88323 (12, 28, 33), bank details match the vendor master exactly, and there is no payment history indicating a duplicate. Arithmetic is consistent: line amounts sum to subtotal 11745.60, tax 2284.26 matches 19% of subtotal within tolerance, and total 14029.86 equals subtotal plus tax."
}
```


## Case: SOI-25-107

**Step 1 — LLM call** (agent: `extractor`, 479+175 tok, 3.06s)
- assistant said:

```
{"invoice_no":"SOI-25-107","vendor_name":"Stellar Office Interiors","date":"2025-07-23","po_number":"PO-2025-4125","currency":"USD","lines":[{"sku":"SO-FIL-3D","description":"File cabinet 3-drawer","qty":26,"unit_price":156.80,"amount":4076.80},{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":18,"unit_price":189.00,"amount":3492.00}],"subtotal":7568.80,"tax":613.07,"total":8181.87,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-107"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1285+229 tok, 4.54s)
- assistant said:

```
{
  "invoice_id": "SOI-25-107",
  "po_number": "PO-2025-4125",
  "decision": "approve",
  "discrepancies": [],
  "explanation": "PO PO-2025-4125 exists in USD, the invoice currency is USD, and the billed unit prices match the PO exactly: SO-FIL-3D at 156.80 for qty 26 and SO-CHR-T2 at 189.00 for qty 18. GRN-88324 shows receipts of 26 and 18 respectively, matching billed quantities, the remit-to bank details match the vendor master exactly, and payment history shows no duplicate invoice number or same vendor+PO+amount combination. Invoice arithmetic is consistent within tolerance: line amounts 4,076.80 and 3,402.00 sum to the stated subtotal 7,568.80; tax 613.07 matches 8.1% of subtotal within $0.02; and total 8,181.87 equals subtotal plus tax."
}
```


## Case: MF/25/107

**Step 1 — LLM call** (agent: `extractor`, 553+258 tok, 3.78s)
- assistant said:

```
{"invoice_no":"MF/25/107","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-07-02","po_number":"PO-2025-4126","currency":"USD","lines":[{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":15,"unit_price":62.75,"amount":941.25},{"sku":"MF-M8-50","description":"Hex bolts M8x50 zinc, box 500","qty":5,"unit_price":44.00,"amount":220.00},{"sku":"MF-W-8","description":"Flat washers 8mm, box 1000","qty":39,"unit_price":15.30,"amount":596.70},{"sku":"MF-M8-NUT","description":"Hex nuts M8 zinc, box 1000","qty":36,"unit_price":27.60,"amount":1021.60}],"subtotal":2779.55,"tax":166.77,"total":2946.32,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/107"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1518+189 tok, 4.41s)
- assistant said:

```
{
  "invoice_id": "MF/25/107",
  "po_number": "PO-2025-4126",
  "decision": "hold",
  "discrepancies": [
    "TOTAL_ERROR"
  ],
  "explanation": "PO PO-2025-4126 exists, currency matches USD, GRN-88325 shows full receipt for all billed quantities (15, 5, 39, and 36), vendor bank details match the master record, and there is no payment-history duplicate. However, line 4 is incorrect: qty 36 × unit price 27.60 should be 993.60, but the invoice shows 1021.60, a difference of 28.00, which also causes the subtotal 2779.55 and total 2946.32 to be overstated."
}
```


## Case: HEC-2025-110

**Step 1 — LLM call** (agent: `extractor`, 457+186 tok, 3.86s)
- assistant said:

```
{"invoice_no":"HEC-2025-110","vendor_name":"Helios Electrical Components","date":"2025-06-28","po_number":"PO-2025-4127","currency":"USD","lines":[{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":35,"unit_price":96.30,"amount":3370.50},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":12,"unit_price":118.00,"amount":1416.00}],"subtotal":4786.50,"tax":411.64,"total":5198.14,"bank_name":"Meridian Trust Bank","bank_routing":"122100024","bank_account":"7791024468","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-110"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1240+236 tok, 4.25s)
- assistant said:

```
{
  "invoice_id": "HEC-2025-110",
  "po_number": "PO-2025-4127",
  "decision": "hold",
  "discrepancies": ["BANK_CHANGE"],
  "explanation": "PO PO-2025-4127 exists in USD, GRN-88326 shows full receipt of 35 units for HE-PSU-24 and 12 units for HE-CAB-14, and the invoice line prices and quantities match the PO. Arithmetic checks are consistent: line amounts 3370.50 and 1416.00 sum to subtotal 4786.50, tax 411.64 matches 8.6% of subtotal within tolerance, and total 5198.14 equals subtotal plus tax. The invoice remit-to banking differs from vendor master: invoice shows Meridian Trust Bank / routing 122100024 / account 7791024468, while vendor master has Desert West Bank / routing 122100024 / account 3348812706, so the invoice must be held for BANK_CHANGE review."
}
```


## Case: GP-107

**Step 1 — LLM call** (agent: `extractor`, 446+176 tok, 4.43s)
- assistant said:

```
{"invoice_no":"GP-107","vendor_name":"Granite Peak Safety Gear","date":"2025-06-19","po_number":"PO-2025-4128","currency":"USD","lines":[{"sku":"GP-HH-CL2","description":"Hard hats class E, box 20","qty":6,"unit_price":196.00,"amount":1176.00},{"sku":"GP-BOOT-10","description":"Steel toe boots size 10","qty":17,"unit_price":112.00,"amount":1904.00}],"subtotal":3080.00,"tax":184.80,"total":3264.80,"bank_name":"Meridian Trust Bank","bank_routing":"123103729","bank_account":"4456108823","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-107"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1224+241 tok, 4.24s)
- assistant said:

```
{
  "invoice_id": "GP-107",
  "po_number": "PO-2025-4128",
  "decision": "hold",
  "discrepancies": [
    "BANK_CHANGE"
  ],
  "explanation": "PO PO-2025-4128 exists, is in USD, and the invoice line prices and quantities match the PO and received quantities exactly: GP-HH-CL2 billed 6 @ 196.00 with 6 received, and GP-BOOT-10 billed 17 @ 112.00 with 17 received. Arithmetic is consistent (line amounts 1176.00 and 1904.00, subtotal 3080.00, tax 184.80 at 6%, total 3264.80) and there is no duplicate in payment history. The invoice must be held because the remit bank details differ from vendor master: invoice shows Meridian Trust Bank / routing 123103729 / account 4456108823, while vendor master shows Sawtooth Community Bank / routing 123103729 / account 2290156841."
}
```


## Case: VPL-2025-107

**Step 1 — LLM call** (agent: `extractor`, 533+232 tok, 3.87s)
- assistant said:

```
{"invoice_no":"VPL-2025-107","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-06-22","po_number":"PO-2025-4129","currency":"USD","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":39,"unit_price":21.40,"amount":834.60},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":38,"unit_price":9.60,"amount":364.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":35,"unit_price":340.00,"amount":11900.00}],"subtotal":13099.40,"tax":2488.89,"total":15588.29,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-107"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1398+189 tok, 3.45s)
- assistant said:

```
{
  "invoice_id": "VPL-2025-107",
  "po_number": "PO-2025-4129",
  "decision": "hold",
  "discrepancies": [
    "CURRENCY_MISMATCH"
  ],
  "explanation": "PO PO-2025-4129 exists, GRN-88328 shows full receipt of all billed quantities (39, 38, and 35), and the invoice line prices match the PO prices (21.4, 9.6, and 340.0). The invoice is in USD while the PO and vendor master are in EUR, so CURRENCY_MISMATCH applies; no duplicate or bank change was found, and the invoice arithmetic is internally consistent with subtotal 13099.40, tax 2488.89 at 19%, and total 15588.29."
}
```


## Case: AMT-107

**Step 1 — LLM call** (agent: `extractor`, 550+253 tok, 3.62s)
- assistant said:

```
{"invoice_no":"AMT-107","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-20","po_number":"PO-2025-9911","currency":"USD","lines":[{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":10,"unit_price":412.60,"amount":4126.00},{"sku":"AM-END-12","description":"End mill 12mm carbide","qty":21,"unit_price":68.20,"amount":1432.20},{"sku":"AM-VIS-6","description":"Machine vise 6in","qty":31,"unit_price":289.00,"amount":8959.00},{"sku":"AM-INS-CNMG","description":"Turning inserts CNMG, box 10","qty":22,"unit_price":94.80,"amount":2085.60}],"subtotal":16602.80,"tax":0.00,"total":16602.80,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-107"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1079+143 tok, 4.46s)
- assistant said:

```
{
  "invoice_id": "AMT-107",
  "po_number": "PO-2025-9911",
  "decision": "hold",
  "discrepancies": ["PO_NOT_FOUND", "GRN_MISSING"],
  "explanation": "The referenced purchase order PO-2025-9911 does not exist in the PO system, so the invoice cannot be matched to any authorized PO. Because no valid PO exists, there are also no GRNs available for that PO reference; vendor master checks shown are consistent (USD currency, tax rate 0.0, and bank routing/account match), and payment history shows no duplicate."
}
```


## Case: NIS-2025-110

**Step 1 — LLM call** (agent: `extractor`, 538+243 tok, 4.17s)
- assistant said:

```
{"invoice_no":"NIS-2025-110","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-15","po_number":"PO-2025-4131","currency":"USD","lines":[{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":10,"unit_price":20.24,"amount":202.40},{"sku":"NG-3305","description":"Absorbent pads, case","qty":24,"unit_price":42.50,"amount":1020.00},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":6,"unit_price":149.00,"amount":894.00},{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":17,"unit_price":6.95,"amount":118.15}],"subtotal":2234.55,"tax":162.00,"total":2396.55,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-110"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1554+211 tok, 4.3s)
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
  "explanation": "PO PO-2025-4131 exists and matches the invoice currency (USD), and the remit-to bank details match the vendor master exactly. However, line SKU NG-4410 is billed at 20.24 versus the PO price of 18.40, which exceeds the 0.5% unit-price tolerance, and billed quantities exceed received quantities on all lines: NG-4410 10 vs 5 received, NG-3305 24 vs 12 received, NG-1180 6 vs 3 received, and NG-7720 17 vs 8 received based on GRN-88330. No duplicate was found in payment history."
}
```


## Case: CCW-107

**Step 1 — LLM call** (agent: `extractor`, 521+220 tok, 4.53s)
- assistant said:

```
{"invoice_no":"CCW-107","vendor_name":"Cascadia Chemical Works","date":"2025-06-04","po_number":"PO-2025-4132","currency":"USD","lines":[{"sku":"CC-COOL-55","description":"Machine coolant concentrate, 55gal","qty":37,"unit_price":744.50,"amount":27546.50},{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":21,"unit_price":87.40,"amount":1835.40},{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":8,"unit_price":612.00,"amount":4896.00}],"subtotal":34277.90,"tax":3300.50,"total":37578.40,"bank_name":"Meridian Trust Bank","bank_routing":"125000024","bank_account":"6120087745","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-107"}`

**Step 3 — LLM call** (agent: `matcher_v1`, 1443+251 tok, 4.58s)
- assistant said:

```
{
  "invoice_id": "CCW-107",
  "po_number": "PO-2025-4132",
  "decision": "hold",
  "discrepancies": [
    "BANK_CHANGE",
    "TAX_ERROR"
  ],
  "explanation": "PO PO-2025-4132 exists in USD, invoice line unit prices match the PO (744.50, 87.40, 612.00), and billed quantities 37/21/8 do not exceed the received quantities on GRN-88331 (37/21/8). The invoice bank details differ from vendor master: routing matches at 125000024, but bank name is 'Meridian Trust Bank' vs 'Puget Sound Trust' and account is 6120087745 vs 9027481133, triggering BANK_CHANGE. Tax is also incorrect: with subtotal 34277.90 and vendor tax rate 9.5%, expected tax is 3256.40, but invoice shows 3300.50, a difference of 44.10, so TAX_ERROR applies; no duplicate, currency, quantity, price, or total arithmetic discrepancies were found."
}
```
