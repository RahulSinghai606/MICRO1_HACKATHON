# Agent trajectories — run `agent_engine_only`


## Case: NIS-2025-101

**Step 1 — LLM call** (agent: `extractor`, 538+243 tok, 3.62s)
- assistant said:

```
{"invoice_no":"NIS-2025-101","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-18","po_number":"PO-2025-4101","currency":"USD","lines":[{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":3,"unit_price":18.40,"amount":55.20},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":7,"unit_price":149.00,"amount":1043.00},{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":15,"unit_price":6.95,"amount":104.25},{"sku":"NG-3305","description":"Absorbent pads, case","qty":16,"unit_price":42.50,"amount":680.00}],"subtotal":1882.45,"tax":136.48,"total":2018.93,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-101"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: INV-2025-0101

**Step 1 — LLM call** (agent: `extractor`, 446+178 tok, 2.95s)
- assistant said:

```
{"invoice_no":"INV-2025-0101","vendor_name":"Bluefin Packaging Co.","date":"2025-06-25","po_number":"PO-2025-4102","currency":"USD","lines":[{"sku":"BP-450","description":"Foam inserts, custom cut","qty":30,"unit_price":4.15,"amount":124.50},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":39,"unit_price":31.25,"amount":1218.75}],"subtotal":1343.25,"tax":94.03,"total":1437.28,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0101"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: MF/25/101

**Step 1 — LLM call** (agent: `extractor`, 487+182 tok, 3.65s)
- assistant said:

```
{"invoice_no":"MF/25/101","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-07-04","po_number":"PO-2025-4103","currency":"USD","lines":[{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":19,"unit_price":62.75,"amount":1192.25},{"sku":"MF-M8-NUT","description":"Hex nuts M8 zinc, box 1000","qty":11,"unit_price":27.6,"amount":303.6}],"subtotal":1495.85,"tax":89.75,"total":1585.6,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/101"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: CCW-101

**Step 1 — LLM call** (agent: `extractor`, 489+183 tok, 3.13s)
- assistant said:

```
{"invoice_no":"CCW-101","vendor_name":"Cascadia Chemical Works","date":"2025-06-24","po_number":"PO-2025-4104","currency":"USD","lines":[{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":24,"unit_price":87.40,"amount":2097.60},{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":24,"unit_price":612.00,"amount":14688.00}],"subtotal":16785.60,"tax":1594.63,"total":18380.23,"bank_name":"Puget Sound Trust","bank_routing":"125000024","bank_account":"9027481133","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-101"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: HEC-2025-101

**Step 1 — LLM call** (agent: `extractor`, 481+216 tok, 3.44s)
- assistant said:

```
{"invoice_no":"HEC-2025-101","vendor_name":"Helios Electrical Components","date":"2025-06-02","po_number":"PO-2025-4105","currency":"USD","lines":[{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":37,"unit_price":9.85,"amount":364.45},{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":20,"unit_price":14.20,"amount":284.00},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":25,"unit_price":96.30,"amount":2407.50}],"subtotal":3055.95,"tax":262.81,"total":3318.76,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-101"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: ALS-INV-101

**Step 1 — LLM call** (agent: `extractor`, 525+230 tok, 3.34s)
- assistant said:

```
{"invoice_no":"ALS-INV-101","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-06","po_number":"PO-2025-4106","currency":"USD","lines":[{"sku":"AL-FUEL","description":"Fuel surcharge","qty":8,"unit_price":63.75,"amount":510.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":26,"unit_price":18.50,"amount":481.00},{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":19,"unit_price":425.00,"amount":8075.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":31,"unit_price":45.00,"amount":1395.00}],"subtotal":10461.00,"tax":0.00,"total":10461.00,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-101"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: SOI-25-101

**Step 1 — LLM call** (agent: `extractor`, 508+208 tok, 3.58s)
- assistant said:

```
{"invoice_no":"SOI-25-101","vendor_name":"Stellar Office Interiors","date":"2025-06-06","po_number":"PO-2025-4107","currency":"USD","lines":[{"sku":"SO-MON-ARM","description":"Dual monitor arm","qty":6,"unit_price":74.25,"amount":445.50},{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":40,"unit_price":189.00,"amount":7560.00},{"sku":"SO-DSK-60","description":"Sit-stand desk 60in","qty":12,"unit_price":415.00,"amount":4980.00}],"subtotal":12985.50,"tax":1051.83,"total":14037.33,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-101"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: GP-101

**Step 1 — LLM call** (agent: `extractor`, 479+214 tok, 3.15s)
- assistant said:

```
{"invoice_no":"GP-101","vendor_name":"Granite Peak Safety Gear","date":"2025-07-13","po_number":"PO-2025-4108","currency":"USD","lines":[{"sku":"GP-EAR-200","description":"Ear plugs, box 200 pr","qty":22,"unit_price":38.90,"amount":855.80},{"sku":"GP-VIS-XL","description":"Hi-vis vests XL, pack 10","qty":5,"unit_price":84.50,"amount":422.50},{"sku":"GP-HH-CL2","description":"Hard hats class E, box 20","qty":16,"unit_price":196.00,"amount":3136.00}],"subtotal":4414.30,"tax":264.86,"total":4679.16,"bank_name":"Sawtooth Community Bank","bank_routing":"123103729","bank_account":"2290156841","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-101"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: VPL-2025-101

**Step 1 — LLM call** (agent: `extractor`, 506+232 tok, 4.55s)
- assistant said:

```
{"invoice_no":"VPL-2025-101","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-06-09","po_number":"PO-2025-4109","currency":"EUR","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":15,"unit_price":21.40,"amount":321.00},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":33,"unit_price":9.60,"amount":316.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":27,"unit_price":340.00,"amount":9180.00}],"subtotal":9817.80,"tax":1865.38,"total":11683.18,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-101"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: AMT-101

**Step 1 — LLM call** (agent: `extractor`, 485+181 tok, 2.98s)
- assistant said:

```
{"invoice_no":"AMT-101","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-19","po_number":"PO-2025-4110","currency":"USD","lines":[{"sku":"AM-VIS-6","description":"Machine vise 6in","qty":37,"unit_price":289.00,"amount":10693.00},{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":36,"unit_price":412.60,"amount":14853.60}],"subtotal":25546.60,"tax":0.00,"total":25546.60,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-101"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: NIS-2025-104

**Step 1 — LLM call** (agent: `extractor`, 527+219 tok, 3.4s)
- assistant said:

```
{"invoice_no":"NIS-2025-104","vendor_name":"Northgate Ind. Supply (a div. of NIS Holdings)","date":"2025-06-05","po_number":"PO-2025-4111","currency":"USD","lines":[{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":34,"unit_price":149.00,"amount":5066.00},{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":33,"unit_price":18.40,"amount":607.20},{"sku":"NG-3305","description":"Absorbent pads, case","qty":7,"unit_price":42.50,"amount":297.50}],"subtotal":5970.70,"tax":432.88,"total":6403.58,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-104"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: HEC-2025-104

**Step 1 — LLM call** (agent: `extractor`, 517+256 tok, 3.78s)
- assistant said:

```
{"invoice_no":"HEC-2025-104","vendor_name":"Helios Electrical Components","date":"2025-06-22","po_number":"PO-2025-4112","currency":"USD","lines":[{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":26,"unit_price":14.20,"amount":369.20},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":26,"unit_price":118.00,"amount":3068.00},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":40,"unit_price":96.30,"amount":3852.00},{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":31,"unit_price":9.85,"amount":305.35}],"subtotal":7594.55,"tax":653.14,"total":8247.69,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-104"}`

**Step 3 — engine_only_result**: `{"decision": "approve", "codes": []}`


## Case: MF/25/104

**Step 1 — LLM call** (agent: `extractor`, 551+257 tok, 4.11s)
- assistant said:

```
{"invoice_no":"MF/25/104","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-07-17","po_number":"PO-2025-4113","currency":"USD","lines":[{"sku":"MF-M8-50","description":"Hex bolts M8x50 zinc, box 500","qty":9,"unit_price":49.28,"amount":443.52},{"sku":"MF-W-8","description":"Flat washers 8mm, box 1000","qty":20,"unit_price":15.30,"amount":306.00},{"sku":"MF-M8-NUT","description":"Hex nuts M8 zinc, box 1000","qty":29,"unit_price":27.60,"amount":800.40},{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":12,"unit_price":62.75,"amount":753.00}],"subtotal":2302.92,"tax":138.18,"total":2441.10,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/104"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["PRICE_MISMATCH"]}`


## Case: SOI-25-104

**Step 1 — LLM call** (agent: `extractor`, 475+171 tok, 2.97s)
- assistant said:

```
{"invoice_no":"SOI-25-104","vendor_name":"Stellar Office Interiors","date":"2025-06-12","po_number":"PO-2025-4114","currency":"USD","lines":[{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":21,"unit_price":204.12,"amount":4286.52},{"sku":"SO-MON-ARM","description":"Dual monitor arm","qty":34,"unit_price":74.25,"amount":2524.50}],"subtotal":6811.02,"tax":551.69,"total":7362.71,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-104"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["PRICE_MISMATCH"]}`


## Case: AMT-104

**Step 1 — LLM call** (agent: `extractor`, 485+181 tok, 2.97s)
- assistant said:

```
{"invoice_no":"AMT-104","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-27","po_number":"PO-2025-4115","currency":"USD","lines":[{"sku":"AM-END-12","description":"End mill 12mm carbide","qty":22,"unit_price":78.43,"amount":1725.46},{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":33,"unit_price":412.60,"amount":13615.80}],"subtotal":15341.26,"tax":0.00,"total":15341.26,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-104"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["PRICE_MISMATCH"]}`


## Case: INV-2025-0104

**Step 1 — LLM call** (agent: `extractor`, 473+210 tok, 3.69s)
- assistant said:

```
{"invoice_no":"INV-2025-0104","vendor_name":"Bluefin Packaging Co.","date":"2025-06-25","po_number":"PO-2025-4116","currency":"USD","lines":[{"sku":"BP-115","description":"Stretch wrap roll 80ga","qty":38,"unit_price":12.80,"amount":486.40},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":7,"unit_price":31.25,"amount":218.75},{"sku":"BP-330","description":"Packing tape, case of 36","qty":7,"unit_price":58.90,"amount":412.30}],"subtotal":1117.45,"tax":78.22,"total":1195.67,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0104"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["QTY_MISMATCH"]}`


## Case: HEC-2025-107

**Step 1 — LLM call** (agent: `extractor`, 517+256 tok, 3.68s)
- assistant said:

```
{"invoice_no":"HEC-2025-107","vendor_name":"Helios Electrical Components","date":"2025-06-23","po_number":"PO-2025-4117","currency":"USD","lines":[{"sku":"HE-REL-24","description":"Relay 24VDC 8-pin","qty":18,"unit_price":14.20,"amount":255.60},{"sku":"HE-CB-20","description":"Circuit breaker 20A DIN","qty":35,"unit_price":9.85,"amount":344.75},{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":40,"unit_price":96.30,"amount":3852.00},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":29,"unit_price":118.00,"amount":3422.00}],"subtotal":7874.35,"tax":677.19,"total":8551.54,"bank_name":"Desert West Bank","bank_routing":"122100024","bank_account":"3348812706","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-107"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["QTY_MISMATCH"]}`


## Case: GP-104

**Step 1 — LLM call** (agent: `extractor`, 480+213 tok, 3.52s)
- assistant said:

```
{"invoice_no":"GP-104","vendor_name":"Granite Peak Safety Gear","date":"2025-06-03","po_number":"PO-2025-4118","currency":"USD","lines":[{"sku":"GP-EAR-200","description":"Ear plugs, box 200 pr","qty":30,"unit_price":38.90,"amount":1167.00},{"sku":"GP-BOOT-10","description":"Steel toe boots size 10","qty":35,"unit_price":112.00,"amount":3920.00},{"sku":"GP-VIS-XL","description":"Hi-vis vests XL, pack 10","qty":30,"unit_price":84.50,"amount":2535.00}],"subtotal":7622.00,"tax":457.32,"total":8079.32,"bank_name":"Sawtooth Community Bank","bank_routing":"123103729","bank_account":"2290156841","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-104"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["QTY_MISMATCH"]}`


## Case: CCW-104

**Step 1 — LLM call** (agent: `extractor`, 518+218 tok, 3.58s)
- assistant said:

```
{"invoice_no":"CCW-104","vendor_name":"Cascadia Chemical Works","date":"2025-06-28","po_number":"PO-2025-4119","currency":"USD","lines":[{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":2,"unit_price":612.00,"amount":1224.00},{"sku":"CC-COOL-55","description":"Machine coolant concentrate, 55gal","qty":6,"unit_price":744.50,"amount":4467.00},{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":5,"unit_price":87.40,"amount":437.00}],"subtotal":6128.00,"tax":582.16,"total":6710.16,"bank_name":"Puget Sound Trust","bank_routing":"125000024","bank_account":"9027481133","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-104"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["GRN_MISSING"]}`


## Case: ALS-INV-104

**Step 1 — LLM call** (agent: `extractor`, 502+202 tok, 3.35s)
- assistant said:

```
{"invoice_no":"ALS-INV-104","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-08","po_number":"PO-2025-4120","currency":"USD","lines":[{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":19,"unit_price":425.00,"amount":8075.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":33,"unit_price":45.00,"amount":1485.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":15,"unit_price":18.50,"amount":277.50}],"subtotal":9837.50,"tax":0.00,"total":9837.50,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-104"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["GRN_MISSING"]}`


## Case: INV-2025-0107

**Step 1 — LLM call** (agent: `extractor`, 475+211 tok, 3.42s)
- assistant said:

```
{"invoice_no":"INV-2025-0107","vendor_name":"Bluefin Packaging Co.","date":"2025-07-28","po_number":"PO-2025-4121","currency":"USD","lines":[{"sku":"BP-450","description":"Foam inserts, custom cut","qty":8,"unit_price":4.15,"amount":33.20},{"sku":"BP-201","description":"Corrugated boxes 18x12x10, bundle 25","qty":29,"unit_price":31.25,"amount":906.25},{"sku":"BP-330","description":"Packing tape, case of 36","qty":24,"unit_price":58.90,"amount":1413.60}],"subtotal":2353.05,"tax":164.71,"total":2517.76,"bank_name":"Coastal Georgia Bank","bank_routing":"061000104","bank_account":"7719045512","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "INV-2025-0107"}`

**Step 3 — engine_only_result**: `{"decision": "reject", "codes": ["DUPLICATE"]}`


## Case: ALS-INV-107

**Step 1 — LLM call** (agent: `extractor`, 527+231 tok, 3.4s)
- assistant said:

```
{"invoice_no":"ALS-INV-107","vendor_name":"AURIGA LOGISTICS SERVICES","date":"2025-07-05","po_number":"PO-2025-4122","currency":"USD","lines":[{"sku":"AL-LTL-STD","description":"LTL freight, standard lane","qty":27,"unit_price":425.00,"amount":11475.00},{"sku":"AL-LIFT","description":"Liftgate service","qty":23,"unit_price":45.00,"amount":1035.00},{"sku":"AL-WHS-P","description":"Warehouse handling, per pallet","qty":8,"unit_price":18.50,"amount":148.00},{"sku":"AL-FUEL","description":"Fuel surcharge","qty":17,"unit_price":63.75,"amount":1083.75}],"subtotal":13741.75,"tax":0.00,"total":13741.75,"bank_name":"River City Bank","bank_routing":"084000026","bank_account":"6650371928","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "ALS-INV-107"}`

**Step 3 — engine_only_result**: `{"decision": "reject", "codes": ["DUPLICATE"]}`


## Case: NIS-2025-107

**Step 1 — LLM call** (agent: `extractor`, 506+206 tok, 3.17s)
- assistant said:

```
{"invoice_no":"NIS-2025-107","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-21","po_number":"PO-2025-4123","currency":"USD","lines":[{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":17,"unit_price":6.95,"amount":118.15},{"sku":"NG-3305","description":"Absorbent pads, case","qty":6,"unit_price":42.50,"amount":255.00},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":30,"unit_price":149.00,"amount":4470.00}],"subtotal":4843.15,"tax":388.27,"total":5231.42,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-107"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["TAX_ERROR"]}`


## Case: VPL-2025-104

**Step 1 — LLM call** (agent: `extractor`, 506+232 tok, 3.46s)
- assistant said:

```
{"invoice_no":"VPL-2025-104","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-07-02","po_number":"PO-2025-4124","currency":"EUR","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":12,"unit_price":21.40,"amount":256.80},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":28,"unit_price":9.60,"amount":268.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":33,"unit_price":340.00,"amount":11220.00}],"subtotal":11745.60,"tax":2284.26,"total":14029.86,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-104"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["TAX_ERROR"]}`


## Case: SOI-25-107

**Step 1 — LLM call** (agent: `extractor`, 479+175 tok, 3.36s)
- assistant said:

```
{"invoice_no":"SOI-25-107","vendor_name":"Stellar Office Interiors","date":"2025-07-23","po_number":"PO-2025-4125","currency":"USD","lines":[{"sku":"SO-FIL-3D","description":"File cabinet 3-drawer","qty":26,"unit_price":156.80,"amount":4076.80},{"sku":"SO-CHR-T2","description":"Task chair, mesh back","qty":18,"unit_price":189.00,"amount":3492.00}],"subtotal":7568.80,"tax":613.07,"total":8181.87,"bank_name":"Front Range Credit Union","bank_routing":"107000233","bank_account":"8812204575","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "SOI-25-107"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["TOTAL_ERROR"]}`


## Case: MF/25/107

**Step 1 — LLM call** (agent: `extractor`, 553+258 tok, 4.0s)
- assistant said:

```
{"invoice_no":"MF/25/107","vendor_name":"MERIDIAN FASTENERS INC.","date":"2025-07-02","po_number":"PO-2025-4126","currency":"USD","lines":[{"sku":"MF-ANC-10","description":"Concrete anchors 10mm, box 100","qty":15,"unit_price":62.75,"amount":941.25},{"sku":"MF-M8-50","description":"Hex bolts M8x50 zinc, box 500","qty":5,"unit_price":44.00,"amount":220.00},{"sku":"MF-W-8","description":"Flat washers 8mm, box 1000","qty":39,"unit_price":15.30,"amount":596.70},{"sku":"MF-M8-NUT","description":"Hex nuts M8 zinc, box 1000","qty":36,"unit_price":27.60,"amount":1021.60}],"subtotal":2779.55,"tax":166.77,"total":2946.32,"bank_name":"Keystone National","bank_routing":"031000503","bank_account":"5583920164","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "MF/25/107"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["TOTAL_ERROR"]}`


## Case: HEC-2025-110

**Step 1 — LLM call** (agent: `extractor`, 457+186 tok, 3.34s)
- assistant said:

```
{"invoice_no":"HEC-2025-110","vendor_name":"Helios Electrical Components","date":"2025-06-28","po_number":"PO-2025-4127","currency":"USD","lines":[{"sku":"HE-PSU-24","description":"PSU 24V 10A DIN rail","qty":35,"unit_price":96.30,"amount":3370.50},{"sku":"HE-CAB-14","description":"Copper cable 14AWG, 500ft spool","qty":12,"unit_price":118.00,"amount":1416.00}],"subtotal":4786.50,"tax":411.64,"total":5198.14,"bank_name":"Meridian Trust Bank","bank_routing":"122100024","bank_account":"7791024468","payment_terms":"Net 45"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "HEC-2025-110"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["BANK_CHANGE"]}`


## Case: GP-107

**Step 1 — LLM call** (agent: `extractor`, 446+176 tok, 2.99s)
- assistant said:

```
{"invoice_no":"GP-107","vendor_name":"Granite Peak Safety Gear","date":"2025-06-19","po_number":"PO-2025-4128","currency":"USD","lines":[{"sku":"GP-HH-CL2","description":"Hard hats class E, box 20","qty":6,"unit_price":196.00,"amount":1176.00},{"sku":"GP-BOOT-10","description":"Steel toe boots size 10","qty":17,"unit_price":112.00,"amount":1904.00}],"subtotal":3080.00,"tax":184.80,"total":3264.80,"bank_name":"Meridian Trust Bank","bank_routing":"123103729","bank_account":"4456108823","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "GP-107"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["BANK_CHANGE"]}`


## Case: VPL-2025-107

**Step 1 — LLM call** (agent: `extractor`, 533+232 tok, 3.37s)
- assistant said:

```
{"invoice_no":"VPL-2025-107","vendor_name":"VIREO PRINT & LABEL GMBH","date":"2025-06-22","po_number":"PO-2025-4129","currency":"USD","lines":[{"sku":"VP-LBL-4x6","description":"Thermal labels 4x6, roll 500","qty":39,"unit_price":21.40,"amount":834.60},{"sku":"VP-RIB-110","description":"TTR ribbon 110mm","qty":38,"unit_price":9.60,"amount":364.80},{"sku":"VP-TAG-ASSET","description":"Asset tags, custom, 1000","qty":35,"unit_price":340.00,"amount":11900.00}],"subtotal":13099.40,"tax":2488.89,"total":15588.29,"bank_name":"Hansa Handelsbank","bank_routing":"DE44 5001 0517","bank_account":"5407 3249 31","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "VPL-2025-107"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["CURRENCY_MISMATCH"]}`


## Case: AMT-107

**Step 1 — LLM call** (agent: `extractor`, 550+253 tok, 3.58s)
- assistant said:

```
{"invoice_no":"AMT-107","vendor_name":"Ashford Machine Tools Ltd.","date":"2025-07-20","po_number":"PO-2025-9911","currency":"USD","lines":[{"sku":"AM-CHK-125","description":"Lathe chuck 125mm","qty":10,"unit_price":412.60,"amount":4126.00},{"sku":"AM-END-12","description":"End mill 12mm carbide","qty":21,"unit_price":68.20,"amount":1432.20},{"sku":"AM-VIS-6","description":"Machine vise 6in","qty":31,"unit_price":289.00,"amount":8959.00},{"sku":"AM-INS-CNMG","description":"Turning inserts CNMG, box 10","qty":22,"unit_price":94.80,"amount":2085.60}],"subtotal":16602.80,"tax":0.00,"total":16602.80,"bank_name":"Pennine & Yorkshire Bank","bank_routing":"GB29 NWBK 6016","bank_account":"1331 9268 19","payment_terms":"Net 30"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "AMT-107"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["PO_NOT_FOUND"]}`


## Case: NIS-2025-110

**Step 1 — LLM call** (agent: `extractor`, 538+243 tok, 3.96s)
- assistant said:

```
{"invoice_no":"NIS-2025-110","vendor_name":"Northgate Industrial Supply LLC","date":"2025-06-15","po_number":"PO-2025-4131","currency":"USD","lines":[{"sku":"NG-4410","description":"Nitrile work gloves, box of 100","qty":10,"unit_price":20.24,"amount":202.40},{"sku":"NG-3305","description":"Absorbent pads, case","qty":24,"unit_price":42.50,"amount":1020.00},{"sku":"NG-1180","description":"Steel shelving unit 72in","qty":6,"unit_price":149.00,"amount":894.00},{"sku":"NG-7720","description":"Safety goggles, anti-fog","qty":17,"unit_price":6.95,"amount":118.15}],"subtotal":2234.55,"tax":162.00,"total":2396.55,"bank_name":"First Commerce Bank","bank_routing":"021000021","bank_account":"4402198837","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "NIS-2025-110"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["PRICE_MISMATCH", "QTY_MISMATCH"]}`


## Case: CCW-107

**Step 1 — LLM call** (agent: `extractor`, 521+220 tok, 3.68s)
- assistant said:

```
{"invoice_no":"CCW-107","vendor_name":"Cascadia Chemical Works","date":"2025-06-04","po_number":"PO-2025-4132","currency":"USD","lines":[{"sku":"CC-COOL-55","description":"Machine coolant concentrate, 55gal","qty":37,"unit_price":744.50,"amount":27546.50},{"sku":"CC-DEG-5","description":"Industrial degreaser, 5gal","qty":21,"unit_price":87.40,"amount":1835.40},{"sku":"CC-IPA-55","description":"Isopropyl alcohol 99%, 55gal drum","qty":8,"unit_price":612.00,"amount":4896.00}],"subtotal":34277.90,"tax":3300.50,"total":37578.40,"bank_name":"Meridian Trust Bank","bank_routing":"125000024","bank_account":"6120087745","payment_terms":"Net 60"}
```

**Step 2 — extraction_ok**: `{"invoice_no": "CCW-107"}`

**Step 3 — engine_only_result**: `{"decision": "hold", "codes": ["BANK_CHANGE", "TAX_ERROR"]}`
