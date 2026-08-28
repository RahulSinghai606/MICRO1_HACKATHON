# Matchpoint — an agentic 3-way match that an AP specialist can actually sign

**micro1 Agentic Workflows Hackathon submission.**
Everything in this repository was built during the competition. Pre-existing components:
Python, Pillow, Requests, the LLM APIs (Azure AI Foundry / OpenRouter) and Mistral OCR.
Everything else — dataset, generator, agents, tools, verifier, evaluation harness, UI — is ours.

---

## 1. Who has the problem

An **accounts-payable specialist** at a mid-size company. Before any supplier invoice is
paid, she must **three-way match** it: the invoice against the **purchase order** (did we
order this, at this price?) and against the **goods receipt** (did it actually arrive?) —
then screen for duplicates, tax errors, and changed bank details.

## 2. The bottleneck, and why solving it matters

- Manual invoice processing costs **$12.88–$19.83 per invoice**; even the industry
  average all-in cost is **$9.40** vs **$2.78** for best-in-class automated teams
  ([Ardent Partners, *AP Metrics That Matter 2025*](https://www.apexanalytix.com/resources/blog/ardent-partners-key-ap-metrics-2025/)).
- The average invoice takes **9.2 days** to clear, and **over 60% of invoices still
  require human touch** (same report). Manual three-way matching specifically runs
  [$20–24 per invoice](https://virtualworkforce.ai/3-way-match-automation/).
- The stakes are not just efficiency: **76% of US organizations were hit by attempted or
  actual payments fraud in 2025**
  ([AFP Payments Fraud Survey 2026](https://www.financialprofessionals.org/about/learn-more/press-releases/Details/over-75-percent-of-us-firms-experienced-payments-fraud-in-2025-while-ai-adoption-for-fraud-mitigation-lags)),
  and [more than a third of attacks involve phony bank-account-change requests](https://finance.yahoo.com/news/under-attack-ap-leaders-stop-125404624.html) —
  exactly the "remit-to changed" pattern a tired human misses at 4:55 pm on invoice #178.

A missed price bump, a duplicate, or a swapped bank account is money that does not come
back (only 22% of defrauded organizations recovered ≥75% of funds in 2024, per AFP).

## 3. What Matchpoint does

One realistic batch, end to end:

```
32 invoice images (PNG)
   │  Mistral OCR
   ▼
Extraction agent      LLM turns OCR markdown into strict JSON. Forbidden from "fixing"
   │                  numbers — the printed numbers are the evidence.
   ▼
Matching agent        LLM investigates with deterministic tools: get_po,
   │                  get_received_totals (partial deliveries summed), search_payments
   │                  (duplicate detection), arithmetic_check, vendor resolution with
   │                  learned aliases. The LLM never does arithmetic.
   ▼
Verifier              An independent deterministic match engine recomputes every check
   │                  from the extracted JSON. Disagreement → one feedback round to the
   │                  matcher → if still unresolved, deterministic evidence wins (flagged).
   ▼
Human approval queue  Nothing is ever paid by a machine. Web UI or CLI review; payments
   │                  post only to a sandbox CSV ledger after human sign-off.
   ▼
Audit packet          A single self-contained HTML report: every decision, the exact
                      numbers that justify it, checks passed, and the human review trail.
```

Decisions follow a written AP policy (`src/matchpoint/policy.py`) shared **verbatim** by
the baseline and the agent: `approve` / `hold` (with one of 9 discrepancy codes) /
`reject` (duplicates).

## 4. Evaluation design (defined before running)

- **32 invoices** per batch: 12 clean, 20 defective across 9 seeded discrepancy types
  (price, quantity, missing goods receipt, duplicate, currency, tax arithmetic, line-math,
  changed bank account, phantom PO), including two multi-defect invoices and two
  **challenging legitimate** cases (vendor invoicing under an alias trade name with split
  partial deliveries; a 1-cent tax rounding) that punish over-flagging.
- Ground truth is **seeded**, so every metric is exact — no LLM judging.
- **Primary metric: decision accuracy** (approve/hold/reject correct). Secondary:
  exact match (decision + full discrepancy set), discrepancy precision/recall/F1,
  **false-hold rate** (clean invoices wrongly flagged — supplier friction),
  **missed-defect rate** (bad invoices approved — money out the door), tokens, cost, latency.
- Baseline = **one direct prompt** with the same model, same policy, same ERP data, same
  32 cases. Same everything except the workflow.
- A **held-out stress batch** (seed 43, disjoint invoice numbers, never seen during
  development) verifies we didn't tune to our own test set.

## 5. Results

Main batch (same 32 cases, same model — Azure `gpt-5.4`):

| Metric | Baseline (1 prompt) | Matchpoint final | Change |
|---|---|---|---|
| Decision accuracy | 81.3% | **100%** | +18.7 pts |
| Exact match (decision + all codes) | 75.0% | **100%** | +25 pts |
| Discrepancy F1 | 0.79 | **1.00** | +0.21 |
| Missed-defect rate (bad invoices approved) | 30% | **0%** | −30 pts |
| False-hold rate (clean invoices flagged) | 0% | **0%** | recall not bought with spam |
| Est. cost per invoice | $0.028 | $0.020 | −29% |
| Latency per invoice | 4.4 s | 15.1 s | slower, still ≫ faster than a human |

**Held-out stress batch (seed 43, zero tuning):** baseline 81.3% → Matchpoint **100%**
decision accuracy (exact match 71.9% → **100%**). The improvement generalizes.

Human time (industry-benchmarked estimate, not measured): manual 3-way match ≈ 10–15 min
per invoice; with Matchpoint the 12 clean invoices need only a sign-off glance and the
20 flagged ones arrive with the discrepancy already isolated and evidenced — minutes, not
document hunts. At Ardent's $12.88 manual cost, the model spend is **0.16%** of the manual cost.

## 6. Improvement Changelog

Every stage is still runnable (`make agent-v1` … `make agent-final`), every number comes
from a committed results file in `eval/results/`, and full trajectories for every run are
in `trajectories/`.

| Stage | What we tried and why | Evidence (same 32 cases) | Decision / learning |
|---|---|---|---|
| **Baseline** | One prompt: OCR text + full ERP dump + policy → decision. | 81.3% acc, 75% exact, **missed 30% of defects** — including *every* tax/total arithmetic error and both missing-GRN cases. Cost $0.028/inv. | Established the failure signature: LLMs miss arithmetic and *absence*. `eval/results/baseline.json` |
| **Iteration 1 — extraction agent + scoped context** | Split extract→decide; retrieve only the referenced PO/GRNs/vendor/payments instead of the whole ERP. | 90.6% acc, missed defects 30%→15%, cost **−67%** ($0.009/inv). Precision fell 0.94→0.83 (over-flagging). | Kept. Needle-in-haystack misses were context failures, not reasoning failures. `eval/results/agent_v1.json` |
| **Iteration 1b — chain-of-thought arithmetic (REMOVED)** | Before building tools: just *ask* the model to recompute every number step by step. | 87.5% acc, exact match **dropped** to 68.8%, still missed 20% of defects, cost 2.2× v1. | **Removed.** Prompting an LLM to try harder at math is not an engineering control. Config kept as `--config v1cot` so the negative result is reproducible. `eval/results/agent_v1cot.json` |
| **Iteration 2 — deterministic tools** | Function-calling matcher: PO lookup, GRN totals (partial deliveries summed), payment search, `arithmetic_check`. LLM banned from computing. | **100% decision accuracy, 100% recall, 0 missed defects.** Exact match 93.8% — two cases double-flagged (`GRN_MISSING`+spurious `QTY_MISMATCH`). | Kept. The single biggest jump. Remaining errors were code-taxonomy confusion, not detection misses. `eval/results/agent_v2.json` |
| **Iteration 3 — independent verifier** | Deterministic engine recomputes everything; disagreement → one feedback round; unresolved → engine wins. | **100% / 100% / 1.00 across every metric.** Verifier fired on exactly the 2 double-flagged cases; matcher accepted feedback both times; 0 overrides needed. | Kept. Verification converted "usually right" into "auditable". `eval/results/agent_v3.json` |
| **Iteration 4 — vendor memory + HITL (final)** | Aliases/history notes from prior quarters; human approval queue; sandbox ledger; audit packet. | Same 100% scores; memory made the alias case's explanation cite the 2024 reorg note; every decision now carries a human checkpoint. | Kept. No metric delta on this batch — memory pays in explanation quality and operator trust, and HITL is a ground-rule requirement, not garnish. `eval/results/agent_final.json` |
| **Ablation — engine only** | Extraction agent + deterministic engine, no matcher LLM. | **100% / 100%** at **$0.004/inv and 3.5 s** — 5× cheaper, 4× faster than final. | Eye-opening. For fully codified checks the matcher LLM adds explanation quality and open-world flexibility, not accuracy. See Hot Take. `eval/results/agent_engine_only.json` |
| **Robustness — cheap model** | Swap gpt-5.4 → GLM-5.3-flash (reasoning model) on the identical pipeline. | Baseline-GLM: 96.9% acc by brute-forcing arithmetic through ~38K reasoning tokens/case — yet still approved a defective invoice and ran 4.3× the latency. | The scaffolding, not the model, is what guarantees the floor. `eval/results/baseline_glm.json` |
| **Generalization — held-out batch** | Fresh world, seed 43, disjoint invoice numbers, zero prompt/tool changes. | Baseline 81.3% vs final **100%** decision accuracy. | The gain is the workflow's, not the test set's. `eval/results/agent_final_stress.json` |

## 7. Main failure mode

**The baseline's catastrophic failure is silent approval.** It never spammed false holds —
it *confidently approved* invoices with overstated tax, inflated line amounts, and goods
that were never received (30% of all defective invoices, 100% of arithmetic defects).
The dangerous LLM failure in back-office automation isn't hallucinated flags; it's the
quiet "looks fine" on a document whose numbers don't add up. Our residual failure mode in
the final system is extraction: if OCR+extraction misreads a printed number, the engine
verifies a fiction. That's why extraction is forbidden from "correcting" values, why the
verifier works only from printed evidence, and why a human signs every payment.

## 8. Hot take

**The most reliable agent is the one with the smallest possible LLM surface area.**
Every measured gain came from *taking a responsibility away from the model*: retrieval
took away context hunting (+9 pts), tools took away arithmetic (+9 pts, −30 pts missed
defects), the deterministic verifier took away final say (+6 pts exact match). Our
ablation is the punchline: extraction + a for-loop scored the same 100% as the full agent
at a fifth of the cost. And a reasoning model burning 38K tokens per invoice to brute-force
multiplication still approved a bad invoice. If a check can be written as code, write it
as code — spend the LLM only where the world is unstructured (reading messy documents,
resolving "NIS Holdings" to "Northgate Industrial Supply", explaining decisions to
humans). We came in building an agent and left having measured exactly which parts of it
deserve to be an agent.

## 9. Repository map

```
data/generate.py            deterministic world generator (--seed, --world)
data/erp/                   vendor master, POs, GRNs, payment history, vendor memory
data/invoices/png/          32 rendered invoice images   ocr_cache/  committed OCR output
data/gold/                  labels.json (ground truth) + cases.md (every seeded case)
data/worlds/stress/         held-out batch (seed 43)
src/matchpoint/
  baseline.py               single-prompt baseline
  agent.py                  extractor + matcher + verifier pipeline (configs v1..final + ablations)
  tools.py                  deterministic ERP tools + 3-way match engine
  policy.py                 the AP policy (shared verbatim by baseline and agent)
  ocr.py                    Mistral OCR + cache      llm.py  provider-agnostic client
  hitl.py                   approval queue + sandbox ledger    review_ui.py  web review UI
  report.py                 audit packet renderer    trajectory.py  JSONL logger + renderer
eval/run_eval.py            gold-label scorer        eval/results/  every run's scores
trajectories/               full trajectories (JSONL + markdown) for every run
out/                        runs, audit packet, approval queue, sandbox ledger
```

- **Reproduction guide:** [REPRODUCE.md](REPRODUCE.md)
- **Video script:** [docs/video_script.md](docs/video_script.md)
- **Seeded cases:** [data/gold/cases.md](data/gold/cases.md)

## 10. Responsible use

Entirely synthetic data — no real companies, people, invoices or bank accounts. No real
payment is ever executed: consequential actions are sandboxed (CSV ledger) behind a human
approval step. Credentials live in `.env` (gitignored); `.env.example` documents the
required variables.
