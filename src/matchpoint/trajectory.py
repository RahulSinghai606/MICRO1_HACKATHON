"""Trajectory logging. Every LLM call, tool call, verification verdict and
human checkpoint is appended to a JSONL file per run, and can be rendered to
readable markdown (trajectories/ deliverable).
"""
from __future__ import annotations

import json
import time
from pathlib import Path


class Trajectory:
    def __init__(self, path: Path, run: str, case: str):
        self.path = path
        self.run = run
        self.case = case
        path.parent.mkdir(parents=True, exist_ok=True)

    def _write(self, kind: str, payload: dict) -> None:
        rec = {"ts": round(time.time(), 3), "run": self.run, "case": self.case,
               "kind": kind, **payload}
        with self.path.open("a") as f:
            f.write(json.dumps(rec) + "\n")

    def log_llm(self, agent, messages, tools, response, usage, latency_s, attempt):
        self._write("llm_call", {
            "agent": agent,
            "n_messages": len(messages),
            "last_message": _clip(messages[-1].get("content") or "", 2000),
            "tools_offered": tools,
            "assistant_content": _clip(response.get("content") or "", 3000),
            "tool_calls": [
                {"name": tc["function"]["name"], "arguments": _clip(tc["function"]["arguments"], 1000)}
                for tc in (response.get("tool_calls") or [])
            ],
            "usage": {"prompt_tokens": usage.get("prompt_tokens"),
                      "completion_tokens": usage.get("completion_tokens")},
            "latency_s": latency_s,
            "attempt": attempt,
        })

    def log_tool(self, name: str, arguments: dict, result) -> None:
        self._write("tool_result", {"tool": name, "arguments": arguments,
                                    "result": _clip(json.dumps(result, default=str), 3000)})

    def log_event(self, event: str, detail: dict) -> None:
        self._write(event, detail)


def _clip(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n] + f"... [{len(s) - n} chars clipped]"


def render_markdown(jsonl_path: Path, out_path: Path) -> None:
    """Render a run's JSONL trajectories into a readable markdown document."""
    by_case: dict[str, list[dict]] = {}
    for line in jsonl_path.read_text().splitlines():
        rec = json.loads(line)
        by_case.setdefault(rec["case"], []).append(rec)

    lines = [f"# Agent trajectories — run `{jsonl_path.stem}`", ""]
    for case, recs in by_case.items():
        lines.append(f"\n## Case: {case}\n")
        step = 0
        for r in recs:
            step += 1
            if r["kind"] == "llm_call":
                lines.append(f"**Step {step} — LLM call** (agent: `{r['agent']}`, "
                             f"{r['usage']['prompt_tokens']}+{r['usage']['completion_tokens']} tok, "
                             f"{r['latency_s']}s)")
                if r["tools_offered"]:
                    lines.append(f"- tools offered: {', '.join(r['tools_offered'])}")
                if r["tool_calls"]:
                    for tc in r["tool_calls"]:
                        lines.append(f"- agent called `{tc['name']}({tc['arguments']})`")
                if r["assistant_content"]:
                    lines.append(f"- assistant said:\n\n```\n{r['assistant_content']}\n```")
            elif r["kind"] == "tool_result":
                lines.append(f"**Step {step} — tool `{r['tool']}` responded:**\n\n```\n{r['result']}\n```")
            else:
                lines.append(f"**Step {step} — {r['kind']}**: "
                             f"`{json.dumps({k: v for k, v in r.items() if k not in ('ts', 'run', 'case', 'kind')}, default=str)[:1500]}`")
            lines.append("")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines))
