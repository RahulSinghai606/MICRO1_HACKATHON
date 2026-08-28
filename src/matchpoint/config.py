"""Project paths and .env loading (no python-dotenv dependency)."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
ERP = DATA / "erp"
INVOICE_PNG = DATA / "invoices" / "png"
OCR_CACHE = DATA / "invoices" / "ocr_cache"
GOLD = DATA / "gold"
OUT = ROOT / "out"
TRAJ = ROOT / "trajectories"
RESULTS = ROOT / "eval" / "results"


def load_env() -> None:
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
    missing = [k for k in ("LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL") if not os.environ.get(k)]
    if missing:
        raise SystemExit(
            f"Missing env vars: {', '.join(missing)}. Copy .env.example to .env and fill them in."
        )
