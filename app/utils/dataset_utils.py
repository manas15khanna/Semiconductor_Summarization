import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.config import DATASET_DIR


def _read_json(path: Path) -> Any:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def get_dataset_metadata() -> dict[str, Any]:
    metadata_dir = DATASET_DIR / "metadata"
    return {
        "project_summary": _read_json(metadata_dir / "project_summary.json") or {},
        "timeline": _read_json(metadata_dir / "timeline.json") or [],
        "decisions": _read_json(metadata_dir / "decisions.json") or [],
        "action_items": _read_json(metadata_dir / "action_items.json") or [],
        "risks": _read_json(metadata_dir / "risks.json") or [],
        "participants": _read_json(metadata_dir / "participants.json") or [],
    }


def severity_emoji(severity: str) -> str:
    mapping = {
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢",
        "mitigated": "🟢",
        "monitoring": "🟡",
        "open": "🔴",
    }
    return mapping.get((severity or "").strip().lower(), "⚪")


def infer_risk_severity(description: str, impact: str = "") -> str:
    combined = f"{description} {impact}".lower()
    high_markers = ["critical", "high", "yield loss", "delamination", "radiation", "burn-in", "slip"]
    medium_markers = ["medium", "monitoring", "exposure", "delay", "alignment"]
    if any(marker in combined for marker in high_markers):
        return "high"
    if any(marker in combined for marker in medium_markers):
        return "medium"
    return "low"
