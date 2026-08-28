# Matchpoint — one command per reproduction step.
# Prereq: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
#         cp .env.example .env  (fill in your LLM endpoint)

PY := .venv/bin/python
export PYTHONPATH := src

.PHONY: data ocr baseline agent-v1 agent-v2 agent-v3 agent-final eval-all report queue trajectories all

data:            ## regenerate the synthetic world (deterministic, seed 42)
	$(PY) data/generate.py

ocr:             ## re-run live OCR (needs MISTRAL_API_KEY; cached output is committed)
	$(PY) -m matchpoint.ocr --live

baseline:        ## run the single-prompt baseline on all 32 invoices
	$(PY) -m matchpoint.baseline

agent-v1:        ## iteration 1: extraction agent + scoped context
	$(PY) -m matchpoint.agent --config v1

agent-v2:        ## iteration 2: + deterministic function-calling tools
	$(PY) -m matchpoint.agent --config v2

agent-v3:        ## iteration 3: + independent verifier engine
	$(PY) -m matchpoint.agent --config v3

agent-final:     ## final: + vendor memory + HITL queue
	$(PY) -m matchpoint.agent --config final

eval-all:        ## score every run against gold labels, write comparison table
	$(PY) eval/run_eval.py --all

report:          ## render the batch Audit Packet for the final run
	$(PY) -m matchpoint.report --run agent_final

queue:           ## build the human approval queue from the final run
	$(PY) -m matchpoint.hitl build --run agent_final

trajectories:    ## render all trajectories to markdown
	for r in baseline agent_v1 agent_v2 agent_v3 agent_final; do \
		$(PY) -m matchpoint.render_traj --run $$r; done

all: baseline agent-v1 agent-v2 agent-v3 agent-final eval-all report queue trajectories
