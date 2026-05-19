"""
Compare two audits · trend analysis · diff visualization.

Tracks workspace evolution over time. Reads two score.json files (typically
saved at different points in time) and produces a structured diff: per-pillar
level deltas, composite trend, what improved/regressed.

History tracking writes audit snapshots to .workspace-bench/history/ with
timestamps so workspace-bench can compute trends across N+ audits.
"""

from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .data import PILLARS, LEVEL_NAMES, LEVEL_SHORT, grade, grade_description


def compare_scores(before: dict, after: dict) -> dict:
    """Diff two score.json structures · return structured comparison."""
    before_pillars = before.get("pillars", {})
    after_pillars = after.get("pillars", {})

    pillar_diffs = []
    for p_meta in PILLARS:
        b = before_pillars.get(p_meta.key, {})
        a = after_pillars.get(p_meta.key, {})
        b_level = b.get("level", 0)
        a_level = a.get("level", 0)
        b_score = b.get("score", 0)
        a_score = a.get("score", 0)
        diff = {
            "n": p_meta.n,
            "key": p_meta.key,
            "title": p_meta.title,
            "cluster": f"{p_meta.cluster_letter} · {p_meta.cluster}",
            "cluster_letter": p_meta.cluster_letter,
            "before_level": b_level,
            "after_level": a_level,
            "level_delta": a_level - b_level,
            "before_score": b_score,
            "after_score": a_score,
            "score_delta": a_score - b_score,
            "direction": "up" if a_level > b_level else ("down" if a_level < b_level else "flat"),
        }
        pillar_diffs.append(diff)

    composite_before = before.get("composite", 0)
    composite_after = after.get("composite", 0)
    composite_delta = round(composite_after - composite_before, 2)
    grade_before = before.get("grade", "F")
    grade_after = after.get("grade", "F")

    improvements = [d for d in pillar_diffs if d["level_delta"] > 0]
    regressions = [d for d in pillar_diffs if d["level_delta"] < 0]
    flat = [d for d in pillar_diffs if d["level_delta"] == 0]

    return {
        "tool": "workspace-bench/compare",
        "compared_at": datetime.now().isoformat(),
        "before": {
            "audit_at": before.get("audit_at"),
            "scored_at": before.get("scored_at"),
            "composite": composite_before,
            "grade": grade_before,
        },
        "after": {
            "audit_at": after.get("audit_at"),
            "scored_at": after.get("scored_at"),
            "composite": composite_after,
            "grade": grade_after,
        },
        "composite_delta": composite_delta,
        "grade_change": f"{grade_before} → {grade_after}" if grade_before != grade_after else f"{grade_after} (stable)",
        "improvements_count": len(improvements),
        "regressions_count": len(regressions),
        "flat_count": len(flat),
        "pillar_diffs": pillar_diffs,
        "improvements": improvements,
        "regressions": regressions,
    }


def save_to_history(audit: dict, score: dict, history_dir: Path) -> Path:
    """Save an audit+score snapshot to history with timestamp."""
    history_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    snapshot_path = history_dir / f"{timestamp}.json"
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "audit": audit,
        "score": score,
    }
    snapshot_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")

    # Update history index
    index_path = history_dir / "index.json"
    index: list = []
    if index_path.exists():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            index = []
    index.append({
        "timestamp": datetime.now().isoformat(),
        "file": snapshot_path.name,
        "composite": score.get("composite", 0),
        "grade": score.get("grade", "F"),
        "cluster_averages": {k: v["average"] for k, v in score.get("cluster_averages", {}).items()},
    })
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    return snapshot_path


def load_history(history_dir: Path) -> list[dict]:
    """Load history index sorted by timestamp."""
    index_path = history_dir / "index.json"
    if not index_path.exists():
        return []
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
        return sorted(index, key=lambda e: e.get("timestamp", ""))
    except json.JSONDecodeError:
        return []


def composite_trend(history: list[dict]) -> dict:
    """Compute trend over time across composite scores."""
    if not history:
        return {"points": [], "min": 0, "max": 0, "current": 0, "delta_from_first": 0}
    composites = [(h.get("timestamp"), h.get("composite", 0)) for h in history]
    scores = [c[1] for c in composites]
    return {
        "points": composites,
        "min": round(min(scores), 2),
        "max": round(max(scores), 2),
        "current": round(scores[-1], 2),
        "first": round(scores[0], 2),
        "delta_from_first": round(scores[-1] - scores[0], 2),
        "samples": len(scores),
    }


def sparkline(values: list[float], width: int = 30) -> str:
    """Render a tiny ASCII sparkline."""
    if not values:
        return ""
    chars = "▁▂▃▄▅▆▇█"
    lo, hi = min(values), max(values)
    rng = max(hi - lo, 1)
    out = []
    for v in values:
        idx = int(((v - lo) / rng) * (len(chars) - 1))
        out.append(chars[idx])
    if len(out) > width:
        out = out[-width:]
    return "".join(out)
