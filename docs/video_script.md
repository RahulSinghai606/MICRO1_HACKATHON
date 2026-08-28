# Solution video script (target 4:30, hard cap 5:00)

> Record at 1080p+. Screen-record the terminal (large font) + browser.
> Numbers marked ⟨⟩ — read them from `eval/results/comparison.md` before recording.

## 0:00–0:35 — The problem (talking head or slide over invoice PNG)

> "This is Maria. She's an accounts-payable specialist at a mid-size manufacturer.
> Before any supplier invoice is paid, she has to three-way match it: invoice against
> purchase order against goods receipt — plus check for duplicates, tax errors, and
> changed bank accounts, which is how invoice fraud actually happens.
> It's 10–15 minutes per invoice, hundreds per month, and one missed check is real
> money out the door. AP automation tools exist, but the long tail of messy invoices
> still lands on Maria's desk."

*Show one invoice PNG on screen, point at PO number, totals, remit-to bank.*

## 0:35–1:05 — The baseline

> "The obvious 2026 fix: dump the OCR text and the ERP data into one big LLM prompt
> with the policy and ask for a decision. That's our baseline — same model, same
> policy, same 32 invoices as the final system, 12 clean and 20 with seeded defects
> we know the ground truth for."

*Terminal: `make baseline` (pre-recorded/sped up), then show the score:*

> "It looks fine — until you score it. ⟨81%⟩ decision accuracy, and it approved
> ⟨30%⟩ of the defective invoices. Look at WHICH ones it missed: every single
> arithmetic error, and both invoices where the goods receipt simply didn't exist.
> LLMs are bad at multiplying, and worse at noticing what's absent."

## 1:05–2:50 — One realistic execution, start to finish (the core demo)

*Terminal: `make agent-final` running on one defective invoice (e.g. the tax-error
case NIS-2025-107 or the duplicate INV-2025-0104). Show the trajectory markdown
side-by-side (`trajectories/agent_final.md`).*

> "Here's the final system on one invoice, end to end.
> Step one: an extraction agent turns Mistral-OCR output into strict JSON — it is
> forbidden from 'fixing' numbers, because the printed numbers are the evidence.
> Step two: a matching agent investigates with deterministic tools — it pulls the PO,
> sums the goods receipts across partial deliveries, searches payment history for
> duplicates, and calls an arithmetic checker. The LLM never does math.
> Step three: an independent verifier — a deterministic match engine — recomputes
> everything from scratch. If it disagrees with the agent, the agent gets one round
> of feedback; if they still disagree, the deterministic evidence wins.
> Step four: nothing is paid by a machine. Every decision lands in a human approval
> queue, and payments only post to a sandbox ledger after sign-off."

*Show: the tool calls in the trajectory, the verifier verdict, then
`python -m matchpoint.hitl review` approving one invoice, then the audit packet HTML.*

> "And this is what Maria actually receives: a signed-off audit packet — every
> decision with the exact numbers that justify it."

## 2:50–3:40 — Final comparison + changelog

*Show `eval/results/comparison.md` table full screen.*

> "Same 32 invoices, same policy, same model. Decision accuracy ⟨81% → 100%⟩.
> Missed defects ⟨30% → 0%⟩. False holds on clean invoices stayed at zero — the
> system doesn't buy recall by spamming holds. And cost per invoice went DOWN ⟨3×⟩,
> because scoped context beats a full-ERP prompt dump.
> The changelog connects each jump to one change: scoping context fixed needle-in-
> haystack misses; deterministic tools fixed arithmetic; the verifier fixed the last
> code-confusion errors."

## 3:40–4:15 — The change that mattered most + the experiment we removed

> "The biggest single contribution: taking arithmetic away from the model and giving
> it to tools — that alone eliminated every missed tax and total error.
> And here's the experiment we removed: before building tools, we tried just PROMPTING
> the model to recompute every number step by step, chain-of-thought style. Result:
> ⟨read v1cot numbers⟩ — it still missed arithmetic errors, while burning more tokens.
> Asking an LLM to try harder at math is not an engineering strategy. We deleted it
> and kept the config in the repo so you can reproduce the negative result."

## 4:15–4:50 — Hot take + close

> "Our hot take: in agent design, the LLM should be the *translator and investigator*,
> never the *calculator or the memory*. Every reliability gain we measured came from
> moving a responsibility OUT of the model into something deterministic — and the
> agent got cheaper each time we did it.
> Everything you saw — data, gold labels, all five pipeline stages, trajectories —
> is in the repo and reruns from a clean environment with one make command per stage.
> Thanks."

---

### Recording checklist
- [ ] Fill every ⟨⟩ from `eval/results/comparison.md`
- [ ] Pre-run all commands so nothing stalls on camera; speed up waits 4–8×
- [ ] Show gold `data/gold/cases.md` briefly when introducing seeded defects
- [ ] Keep the trajectory markdown visible during the tool-call narration
- [ ] End on the audit packet + comparison table, not on code
