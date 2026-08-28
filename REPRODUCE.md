# Reproduction guide — Matchpoint

Written for a clean machine. Follow top to bottom; every command is copy-pasteable.

## 1. What you need

| Requirement | Notes |
|---|---|
| Python 3.11+ | tested on 3.14.0, macOS 15 (works on Linux the same way) |
| An OpenAI-compatible chat endpoint | any of: Azure AI Foundry, OpenAI, OpenRouter. We used Azure `gpt-5.4` |
| ~25–40 min runtime | for all 5 runs (baseline + 4 iterations, 32 invoices each) |
| ~$1.50 in tokens | measured: ≈$0.89 for the baseline run, ≈$0.30–0.60 per agent run at gpt-5.4 pricing assumptions in `eval/run_eval.py` |
| (optional) Mistral API key | **not needed** — raw OCR output is committed at `data/invoices/ocr_cache/`; only needed if you want to re-run OCR live |

No private data is required. The entire evaluation world (invoice images, ERP records,
gold labels) is synthetic, committed to the repo, and regenerable with a fixed seed.

## 2. Setup (2 minutes)

```bash
cd matchpoint
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt        # pillow + requests, nothing else
cp .env.example .env                             # then edit .env:
# LLM_BASE_URL=https://api.openai.com/v1         (or your Azure ...services.ai.azure.com/openai/v1)
# LLM_API_KEY=<your key>
# LLM_MODEL=<model or deployment name>
export PYTHONPATH=src
```

Sanity check the dataset is intact (or regenerate it — same seed, same bytes):

```bash
.venv/bin/python data/generate.py     # deterministic; overwrites data/ with identical content
```

Expected output: `Generated 32 invoices, 36 POs, 35 GRNs, 5 payment records, 32 gold labels.`

## 3. Run the baseline

```bash
make baseline          # or: .venv/bin/python -m matchpoint.baseline
```

Expected: 32 lines like `[7/32] MF/25/104: hold ['PRICE_MISMATCH']`, then
`out/runs/baseline/results.json` + `trajectories/baseline.jsonl`.
Runtime ≈ 3–5 min.

## 4. Run the agent (every changelog stage is runnable)

```bash
make agent-v1          # extraction agent + scoped ERP context
make agent-v2          # + deterministic function-calling tools
make agent-v3          # + independent verifier engine
make agent-final       # + vendor memory + HITL queue
```

Runtime ≈ 5–12 min each. Each writes `out/runs/agent_<cfg>/results.json` and a full
trajectory log `trajectories/agent_<cfg>.jsonl`.

## 5. Score everything against gold labels

```bash
make eval-all          # or: .venv/bin/python eval/run_eval.py --all
```

Expected output: one JSON summary per run plus a markdown comparison table, written to
`eval/results/comparison.md`. The main result to reproduce: the final agent beats the
baseline on decision accuracy, discrepancy F1 and missed-defect rate (see README
Improvement Changelog for our measured numbers; LLM nondeterminism may shift individual
cases by a point or two — the ordering and the arithmetic/absence failure pattern of the
baseline are stable across reruns).

## 6. The user-facing output (audit packet + human approval)

```bash
make report            # out/audit_packet_agent_final.html  (open in a browser)
make queue             # builds out/approval_queue.json from the final run
.venv/bin/python -m matchpoint.hitl review    # interactive human review CLI
.venv/bin/python -m matchpoint.hitl execute   # posts APPROVED items to the SANDBOX ledger csv
```

No real payment system is touched: `execute` appends rows to `out/sandbox_ledger.csv`,
and only for invoices a human approved in `review`.

## 7. Render trajectories to markdown

```bash
make trajectories      # trajectories/<run>.md for every run
```

## 8. Optional extras

```bash
.venv/bin/python -m matchpoint.ocr --live     # re-OCR the PNGs (needs MISTRAL_API_KEY)
```

## Versions used

- Python 3.14.0, pillow 12.3.0, requests 2.x
- Model: Azure AI Foundry deployment `gpt-5.4` (api `2026-03`), endpoint form
  `https://<resource>.services.ai.azure.com/openai/v1`
- OCR: `mistral-ocr-latest` (output cached in repo on 2026-08-28)
- OS: macOS 15.6 (Darwin 24.6.0); no OS-specific code paths

## Troubleshooting

- `Missing env vars` → your `.env` isn't filled in or you're not in `matchpoint/`.
- Azure 401 → check the key; Azure needs the `/openai/v1` suffix on the base URL.
- Rate limits (429) → the client retries with backoff automatically; runs just slow down.
- Regenerating invoices on Linux may render with a fallback font (PNG bytes differ),
  but the committed PNGs + OCR cache are the evaluation inputs, so results are unaffected.
