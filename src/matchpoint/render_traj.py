"""Render run trajectories (JSONL) to readable markdown.

Run:  python -m matchpoint.render_traj --run agent_final [--cases INV-1,INV-2]
"""
from __future__ import annotations

import argparse

from .config import TRAJ
from .trajectory import render_markdown


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    args = ap.parse_args()
    src = TRAJ / f"{args.run}.jsonl"
    out = TRAJ / f"{args.run}.md"
    render_markdown(src, out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
