"""The AP decision policy. Shared verbatim by the baseline and the agent so
the comparison is fair — both see the exact same rules and tolerances.
"""

DISCREPANCY_CODES = [
    "PRICE_MISMATCH", "QTY_MISMATCH", "GRN_MISSING", "DUPLICATE",
    "CURRENCY_MISMATCH", "TAX_ERROR", "TOTAL_ERROR", "BANK_CHANGE", "PO_NOT_FOUND",
]

POLICY = """\
AP THREE-WAY MATCH POLICY (Harborview Manufacturing Inc.)

For each supplier invoice, match it against the referenced Purchase Order (PO)
and Goods Receipt Notes (GRNs), and screen it against vendor master data and
payment history. Then decide: approve, hold, or reject.

Discrepancy codes (report every one that applies):
- PO_NOT_FOUND      referenced PO does not exist in the PO system
- PRICE_MISMATCH    any line unit price differs from the PO unit price by more than 0.5%
- QTY_MISMATCH      any line billed quantity exceeds the total received quantity across all GRNs for that PO line
- GRN_MISSING       no goods receipt note exists for the referenced PO
- DUPLICATE         same vendor + same PO + same total amount already paid, or the
                    invoice number (in any formatting) already appears in payment history
- CURRENCY_MISMATCH invoice currency differs from the PO currency
- TAX_ERROR         tax amount differs from tax_rate x subtotal by more than $0.02
- TOTAL_ERROR       any line amount differs from qty x unit_price by more than $0.02,
                    or subtotal is not the sum of line amounts (tolerance $0.02),
                    or total is not subtotal + tax (tolerance $0.02)
- BANK_CHANGE       remit-to bank account or routing number differs from the vendor master record

Tolerances (differences within tolerance are NOT discrepancies):
- Unit price: 0.5% relative tolerance
- All currency amounts (tax, line amounts, subtotal, total): $0.02 absolute tolerance
- Vendor trade names / aliases are acceptable if the invoice clearly belongs to the
  vendor on the PO (same PO reference, catalog SKUs, bank details). A name variation
  alone is NOT a discrepancy.
- Multiple partial GRNs are legitimate; compare billed qty against the SUM received.

Decision rule:
- reject  if DUPLICATE
- hold    if any other discrepancy applies
- approve only if there are no discrepancies

Return your answer as JSON:
{
  "invoice_id": "...",
  "po_number": "...",
  "decision": "approve" | "hold" | "reject",
  "discrepancies": ["CODE", ...],
  "explanation": "1-3 sentences citing the specific numbers that justify the decision"
}
"""
