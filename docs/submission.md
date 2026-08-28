# Submission form content

## Title

**Matchpoint — an agentic 3-way invoice match that goes 81% → 100% over a fair baseline, with a human signing every payment**

## Description (paste into the form)

**Who has the problem.** An accounts-payable specialist. Before any supplier invoice is
paid she must three-way match it — invoice vs purchase order vs goods receipt — then screen
for duplicates, tax errors and changed bank details. Manual processing costs $12.88–$19.83
per invoice and takes 9.2 days on average (Ardent Partners 2025); 76% of US organizations
were hit by payments fraud in 2025, and over a third of attacks are fake bank-account-change
requests (AFP 2026). One miss is money that doesn't come back.

**What we built.** Matchpoint runs a batch of 32 invoice images end to end:
Mistral OCR → an **extraction agent** (strict JSON, forbidden from "fixing" numbers) → a
**matching agent** that investigates with deterministic tools (PO lookup, goods-receipt
totals summed across partial deliveries, duplicate search, arithmetic checker — the LLM
never does math) → an **independent deterministic verifier** that recomputes every check
and feeds disagreements back → a **human approval queue** (web UI) with a sandbox payment
ledger → a signed, evidence-cited **audit packet**.

**Measured improvement (gold labels, not vibes).** The baseline — the same model, same
written AP policy, one direct prompt over the same data — scored 81.3% decision accuracy
and silently approved 30% of defective invoices, including every arithmetic error and both
invoices whose goods were never received. The final agent: **100% decision accuracy, 100%
discrepancy F1, 0 missed defects, 0 false holds — at 29% lower cost per invoice.** On a
held-out stress batch (new seed, disjoint invoice numbers, zero tuning): baseline 81.3%,
Matchpoint again **100%**.

**The changelog is the story** — every stage is still runnable and every number is a
committed results file: scoped context (+9 pts, −67% cost) → deterministic tools (+9 pts,
missed defects 30%→0) → independent verifier (last mile to 100% exact match) → memory +
human-in-the-loop. We also publish our **removed experiment** (asking the model to do
chain-of-thought arithmetic made results *worse* at 2.2× the cost) and an **ablation**
(extraction + the deterministic engine alone also hits 100% at a fifth of the cost —
which is the point of our hot take: *the most reliable agent has the smallest possible
LLM surface area*).

**Reproducibility.** Fully synthetic world (no real people, companies or accounts),
generator with fixed seeds, committed OCR cache so no Mistral key is needed, one make
command per stage, full agent trajectories (JSONL + rendered markdown) for every run,
and a reproduction guide written for a clean machine. Consequential actions are sandboxed
behind human sign-off (ground rules 04/05).

- **Live site:** https://matchpoint-teal.vercel.app
- **Repo:** https://github.com/RahulSinghai606/MICRO1_HACKATHON
- **Reproduction guide:** REPRODUCE.md · **Changelog + evidence:** README.md · **Trajectories:** trajectories/

## Video URL

<paste your recorded video link — script at docs/video_script.md>

## Source code

Upload `matchpoint_submission.zip` (repo export, ~13 MB — includes data, evidence, trajectories; excludes venv/node_modules; `.env.example` documents required keys, no credentials inside).
