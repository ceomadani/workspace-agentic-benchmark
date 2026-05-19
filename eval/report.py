#!/usr/bin/env python3
"""
================================================================================
report.py · Workspace Agentic Benchmark v0.3 · report generator
================================================================================

LEGEND 4W:
  WHAT  · Generate human-readable markdown + HTML report from score.json (v0.3).
  HOW   · Render executive summary · cluster breakdown · per-pillar L0-L4 detail ·
          improvement ladder (next-level actions).
  WHERE · Input: score.json (from score.py). Output: markdown to stdout
          (or specified path), HTML if --html flag.
  WHEN  · CLI usage: python3 report.py score.json --output report.md
          python3 report.py score.json --html --output report.html

================================================================================
"""

from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


GRADE_DESCRIPTIONS = {
    "A": "**Production-grade** · forward-deployable · FDE-engagement ready.",
    "B": "**Solid** · 1-2 pillars need hardening before scale.",
    "C": "**Early-stage** · multiple gaps · workspace work needed alongside agent work.",
    "D": "**Prototype** · not production-ready · infrastructure-first work required.",
    "F": "**Failing** · workspace not fit for purpose.",
}

GRADE_COLORS = {"A": "#10b981", "B": "#3b82f6", "C": "#f59e0b", "D": "#ef4444", "F": "#7c2d12"}

LEVEL_BAR = {0: "░░░░░░░░░░░░░░░░░░░░", 1: "████░░░░░░░░░░░░░░░░", 2: "██████████░░░░░░░░░░", 3: "███████████████░░░░░", 4: "████████████████████"}


def render_markdown(score: dict) -> str:
    composite = score.get("composite", 0)
    grade = score.get("grade", "F")
    pillars = score.get("pillars", {})
    workspace = score.get("workspace", "?")
    cluster_avgs = score.get("cluster_averages", {})

    lines = [
        "# Workspace Agentic Benchmark · Report (v0.3)",
        "",
        f"**Workspace**: `{workspace}`",
        f"**Scored at**: {score.get('scored_at', '?')}",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        f"**Composite score**: **{composite:.1f} / 100** · Grade **{grade}**",
        "",
        GRADE_DESCRIPTIONS.get(grade, ""),
        "",
    ]

    if cluster_avgs:
        lines.extend([
            "### Cluster averages",
            "",
            "| Cluster | Average score |",
            "|---------|--------------:|",
        ])
        for cluster_name in ["A · Cognition", "B · Action", "C · Trust", "D · Operations"]:
            if cluster_name in cluster_avgs:
                lines.append(f"| {cluster_name} | {cluster_avgs[cluster_name]:.1f} / 100 |")
        lines.append("")

    lines.extend([
        "### Pillar overview",
        "",
        "| # | Pillar | Cluster | Level | Score | Maturity |",
        "|---|--------|---------|-------|------:|----------|",
    ])

    for key, data in pillars.items():
        title = data.get("title", key)
        cluster = data.get("cluster", "?")
        level = data.get("level", 0)
        level_name = data.get("level_name", "?")
        s = data.get("score", 0)
        bar = LEVEL_BAR.get(level, LEVEL_BAR[0])
        pillar_num = key.split("_")[0]
        lines.append(f"| P{pillar_num.zfill(2)} | {title} | {cluster} | **{level_name}** | {s} | `{bar}` |")

    lines.extend([
        "",
        "---",
        "",
        "## Per-pillar deep-dive",
        "",
    ])

    for key, data in pillars.items():
        title = data.get("title", key)
        cluster = data.get("cluster", "?")
        level = data.get("level", 0)
        level_name = data.get("level_name", "?")
        s = data.get("score", 0)
        passed = data.get("criteria_passed", 0)
        total = data.get("criteria_total", 10)

        lines.extend([
            f"### {title}",
            "",
            f"**Cluster**: {cluster}",
            f"**Maturity**: {level_name} · `{LEVEL_BAR.get(level, LEVEL_BAR[0])}` · {s}/100",
            f"**Criteria passed**: {passed}/{total}",
            "",
        ])

        # Next-level guidance
        if level < 4:
            next_level = level + 1
            next_name = {1: "L1 Initial", 2: "L2 Managed", 3: "L3 Defined", 4: "L4 Optimizing"}.get(next_level, "?")
            lines.extend([
                f"**To advance to {next_name}**: see `pillars/{key.split('_')[0].zfill(2)}-*.md` for the criteria checklist and improvement ladder.",
                "",
            ])
        else:
            lines.extend([
                "**Status**: At L4 Optimizing · maintain cybernetic feedback loop · monitor for regression.",
                "",
            ])

    lines.extend([
        "---",
        "",
        "## Improvement priorities · ordered by gap to next level",
        "",
    ])

    # Rank pillars by lowest level (most improvement potential)
    ranked = sorted(pillars.items(), key=lambda kv: kv[1].get("level", 0))
    for key, data in ranked[:5]:
        title = data.get("title", key)
        cluster = data.get("cluster", "?")
        level = data.get("level", 0)
        if level < 4:
            next_level_name = {1: "L1", 2: "L2", 3: "L3", 4: "L4"}.get(level + 1, "?")
            lines.append(f"- **{title}** ({cluster}) · currently {LEVEL_BAR.get(level, '')} · advance to **{next_level_name}** for the largest impact.")

    lines.extend([
        "",
        "---",
        "",
        f"_Generated by workspace-agentic-benchmark/report.py v0.3.0 · {datetime.now().isoformat()}_",
        "",
    ])

    return "\n".join(lines)


def render_html(score: dict) -> str:
    md = render_markdown(score)
    grade = score.get("grade", "F")
    composite = score.get("composite", 0)
    grade_color = GRADE_COLORS.get(grade, "#6b7280")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Workspace Agentic Benchmark · Report</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         max-width: 1040px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6;
         color: #1a1a1a; background: #fafafa; }}
  h1 {{ color: {grade_color}; border-bottom: 3px solid {grade_color}; padding-bottom: .5rem; }}
  h2 {{ color: #333; margin-top: 2.5rem; }}
  h3 {{ color: #555; margin-top: 2rem; }}
  code, pre {{ font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
              background: #f0f0f0; padding: 0.1rem 0.4rem; border-radius: 3px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
  th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; }}
  th {{ background: #f5f5f5; }}
  .grade-badge {{ display: inline-block; padding: 0.5rem 1rem; border-radius: 4px;
                 background: {grade_color}; color: white; font-weight: bold; font-size: 1.5rem; }}
</style>
</head>
<body>
<div class="grade-badge">{grade} · {composite:.1f}/100</div>
<pre style="white-space: pre-wrap; font-family: -apple-system, sans-serif;">{md}</pre>
</body>
</html>
"""


def main():
    p = argparse.ArgumentParser(description="Generate a v0.3 report from score.json (L0-L4 + composite).")
    p.add_argument("score_json", help="Path to score.json (output of score.py).")
    p.add_argument("--html", action="store_true", help="Render as HTML instead of markdown.")
    p.add_argument("--output", "-o", help="Output path (default: stdout).")
    args = p.parse_args()

    score = json.loads(Path(args.score_json).read_text(encoding="utf-8"))

    if args.html:
        out = render_html(score)
    else:
        out = render_markdown(score)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        sys.stderr.write(f"Wrote report to {args.output}\n")
    else:
        print(out)


if __name__ == "__main__":
    main()
