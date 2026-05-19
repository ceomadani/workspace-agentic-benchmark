"""Polished HTML report · white-paper aesthetic · self-contained inline CSS."""

from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any

from .data import PILLARS, CLUSTERS, LEVEL_NAMES, LEVEL_SHORT, LEVEL_DESCRIPTIONS, GRADE_THRESHOLDS


GRADE_COLOR = {"A": "#10b981", "B": "#3b82f6", "C": "#f59e0b", "D": "#ef4444", "F": "#7c2d12"}
CLUSTER_COLOR = {"A": "#a855f7", "B": "#3b82f6", "C": "#f59e0b", "D": "#10b981"}
LEVEL_COLOR = {0: "#7c2d12", 1: "#ef4444", 2: "#f59e0b", 3: "#3b82f6", 4: "#10b981"}


CSS = """
<style>
:root {
    --bg: #0a0d0a;
    --bg-elev: #0f1410;
    --bg-card: #131815;
    --border: rgba(168, 192, 168, 0.18);
    --border-strong: rgba(168, 192, 168, 0.35);
    --fg: #E8EBE8;
    --fg-dim: rgba(232, 235, 232, 0.70);
    --fg-faint: rgba(232, 235, 232, 0.45);
    --accent: #A8C0A8;
    --accent-bright: #C8DDC8;
    --font-serif: 'Iowan Old Style', 'Palatino Linotype', Georgia, serif;
    --font-mono: 'JetBrains Mono', 'SF Mono', Monaco, 'Cascadia Code', monospace;
    --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

* { box-sizing: border-box; }

body {
    background: var(--bg);
    color: var(--fg);
    font-family: var(--font-sans);
    margin: 0;
    padding: 0;
    line-height: 1.6;
    font-size: 15px;
}

.container {
    max-width: 1080px;
    margin: 0 auto;
    padding: 3rem 1.5rem 6rem;
}

.brand {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.18em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

h1 {
    font-family: var(--font-serif);
    font-size: clamp(2.5rem, 5vw, 3.5rem);
    line-height: 1.05;
    margin: 0 0 0.5rem;
    color: #F5F7F5;
}

h1 em {
    font-style: italic;
    color: var(--accent-bright);
}

.subtitle {
    font-family: var(--font-serif);
    font-style: italic;
    font-size: 1.1rem;
    color: var(--fg-dim);
    margin: 0 0 2rem;
}

h2 {
    font-family: var(--font-serif);
    font-size: 1.5rem;
    color: #F5F7F5;
    margin: 3rem 0 1rem;
}

h3 {
    font-family: var(--font-serif);
    font-size: 1.15rem;
    color: var(--accent-bright);
    margin: 2rem 0 0.75rem;
}

.eyebrow {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.18em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.meta {
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--fg-faint);
    margin-bottom: 3rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}

.meta span { margin-right: 1.5rem; }
.meta b { color: var(--fg-dim); font-weight: normal; }

/* Composite hero */
.composite-card {
    background: var(--bg-elev);
    border: 1px solid var(--border-strong);
    border-radius: 8px;
    padding: 2.5rem;
    margin: 2rem 0 3rem;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    align-items: center;
}

.composite-score {
    text-align: center;
}

.composite-value {
    font-family: var(--font-serif);
    font-size: 4.5rem;
    line-height: 1;
    font-weight: 400;
    margin: 0;
}

.composite-max {
    font-family: var(--font-mono);
    font-size: 0.9rem;
    color: var(--fg-faint);
    letter-spacing: 0.1em;
}

.grade-badge {
    display: inline-block;
    padding: 0.6rem 1.5rem;
    border-radius: 8px;
    font-family: var(--font-mono);
    font-size: 2rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.75rem;
    letter-spacing: 0.05em;
}

.grade-description {
    font-family: var(--font-serif);
    font-style: italic;
    color: var(--fg-dim);
    margin: 0;
    font-size: 0.95rem;
}

/* Cluster cards */
.cluster-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0 2rem;
}

.cluster-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.25rem;
}

.cluster-card .label {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.cluster-card .value {
    font-family: var(--font-serif);
    font-size: 2rem;
    line-height: 1;
    margin: 0.75rem 0;
    color: #F5F7F5;
}

.cluster-card .progress {
    height: 6px;
    background: rgba(168, 192, 168, 0.08);
    border-radius: 3px;
    overflow: hidden;
}

.cluster-card .progress-fill {
    height: 100%;
    border-radius: 3px;
}

.cluster-card .desc {
    font-family: var(--font-serif);
    font-style: italic;
    font-size: 0.85rem;
    color: var(--fg-faint);
    margin: 0.5rem 0 0;
    line-height: 1.4;
}

/* Pillar table */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    font-family: var(--font-mono);
    font-size: 13px;
}

th {
    text-align: left;
    padding: 0.75rem 0.75rem;
    border-bottom: 2px solid var(--accent);
    color: var(--accent);
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-size: 11px;
}

td {
    padding: 0.85rem 0.75rem;
    border-bottom: 1px solid var(--border);
    vertical-align: middle;
}

tr:hover td { background: rgba(168, 192, 168, 0.04); }

td.pillar-name {
    font-family: var(--font-serif);
    font-size: 1rem;
    color: var(--accent-bright);
}

.new-badge {
    display: inline-block;
    margin-left: 0.5rem;
    padding: 1px 6px;
    border: 1px solid var(--accent);
    border-radius: 3px;
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.1em;
    color: var(--accent-bright);
    text-transform: uppercase;
}

.level-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: 600;
    color: #fff;
    font-family: var(--font-mono);
    font-size: 12px;
}

.maturity-bar {
    display: inline-flex;
    gap: 2px;
    align-items: center;
}

.maturity-cell {
    width: 18px;
    height: 14px;
    border-radius: 2px;
}

.cluster-tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 3px;
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: #fff;
}

/* Priorities */
.priority-list {
    counter-reset: priority;
    list-style: none;
    padding: 0;
}

.priority-item {
    counter-increment: priority;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 6px;
    padding: 1.25rem 1.5rem;
    margin: 0 0 1rem;
    position: relative;
}

.priority-item::before {
    content: counter(priority);
    position: absolute;
    top: 1.25rem;
    right: 1.5rem;
    font-family: var(--font-serif);
    font-size: 2rem;
    color: var(--accent);
    line-height: 1;
}

.priority-pillar {
    font-family: var(--font-serif);
    font-size: 1.1rem;
    color: var(--accent-bright);
    margin: 0 0 0.5rem;
    padding-right: 3rem;
}

.priority-transition {
    font-family: var(--font-mono);
    font-size: 0.9rem;
    color: var(--fg-dim);
    margin: 0 0 0.5rem;
}

.priority-principle {
    font-family: var(--font-serif);
    font-style: italic;
    color: var(--fg-dim);
    font-size: 0.95rem;
    margin: 0;
    line-height: 1.55;
}

/* Legend */
.legend {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.legend-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem 0;
}

.legend-code {
    font-family: var(--font-mono);
    font-weight: 700;
    min-width: 32px;
}

.legend-name {
    font-family: var(--font-mono);
    color: var(--fg-dim);
    min-width: 110px;
}

.legend-desc {
    font-family: var(--font-serif);
    color: var(--fg-dim);
    font-size: 0.95rem;
}

/* Footer */
footer {
    margin-top: 5rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--fg-faint);
}

/* Print */
@media print {
    body { background: white; color: #1a1a1a; }
    .container { max-width: none; padding: 1rem; }
    .composite-card, .cluster-card, .priority-item, .legend { background: #f8f8f5; border-color: #ddd; }
    h1, h2, h3 { color: #1a1a1a; }
    a { color: #1a1a1a; text-decoration: underline; }
}

/* Responsive */
@media (max-width: 720px) {
    .composite-card { grid-template-columns: 1fr; text-align: center; }
    .container { padding: 2rem 1rem 4rem; }
    table { font-size: 11px; }
    th, td { padding: 0.5rem 0.4rem; }
}
</style>
"""


def _maturity_cells(level: int) -> str:
    cells = []
    for i in range(4):
        if i < level:
            color = LEVEL_COLOR.get(level, "#666")
            cells.append(f'<span class="maturity-cell" style="background:{color}"></span>')
        else:
            cells.append('<span class="maturity-cell" style="background:rgba(168,192,168,0.12)"></span>')
    return f'<span class="maturity-bar">{"".join(cells)}</span>'


def render_html(score: dict, audit: dict | None = None) -> str:
    composite = score.get("composite", 0)
    grade = score.get("grade", "F")
    grade_desc = score.get("grade_description", "")
    workspace = score.get("workspace", "?")
    pillars = score.get("pillars", {})
    cluster_avgs = score.get("cluster_averages", {})
    scored_at = score.get("scored_at", "?")
    version = score.get("version", "?")

    grade_color = GRADE_COLOR.get(grade, "#888")

    # ─── Cluster cards ──────────────────────────────────────────────
    cluster_cards_html = ""
    for letter, name, desc in CLUSTERS:
        if letter not in cluster_avgs:
            continue
        avg = cluster_avgs[letter]["average"]
        color = CLUSTER_COLOR.get(letter, "#888")
        cluster_cards_html += f'''
        <div class="cluster-card">
            <div class="label" style="color:{color}">{letter} · {name}</div>
            <div class="value">{avg:.1f}<span style="font-size:0.5em;color:rgba(232,235,232,0.4);"> / 100</span></div>
            <div class="progress"><div class="progress-fill" style="width:{avg}%;background:{color}"></div></div>
            <p class="desc">{desc}</p>
        </div>'''

    # ─── Pillar table ───────────────────────────────────────────────
    pillar_rows = ""
    for pillar_meta in PILLARS:
        data = pillars.get(pillar_meta.key, {})
        level = data.get("level", 0)
        score_val = data.get("score", 0)
        passed = data.get("criteria_passed", 0)
        total = data.get("criteria_total", 10)
        cluster_color = CLUSTER_COLOR.get(pillar_meta.cluster_letter, "#888")
        level_color = LEVEL_COLOR.get(level, "#888")
        level_label = LEVEL_NAMES.get(level, "?")
        cells = _maturity_cells(level)
        new_badge = '<span class="new-badge">⭐ v0.3</span>' if pillar_meta.is_new_v03 else ''
        warn = ' <span title="needs improvement">⚠</span>' if level <= 2 else ''
        pillar_rows += f'''
        <tr>
            <td style="color:rgba(232,235,232,0.4);">P{pillar_meta.n:02d}</td>
            <td class="pillar-name">{pillar_meta.title}{new_badge}</td>
            <td><span class="cluster-tag" style="background:{cluster_color}">{pillar_meta.cluster_letter}</span></td>
            <td><span class="level-badge" style="background:{level_color}">{LEVEL_SHORT[level]}</span>&nbsp;<span style="color:rgba(232,235,232,0.55);">{level_label.split(" ", 1)[1] if " " in level_label else ""}</span>{warn}</td>
            <td style="text-align:right;"><b style="color:{level_color};font-size:1.05rem">{score_val}</b><span style="color:rgba(232,235,232,0.3);"> / 100</span></td>
            <td style="text-align:right;color:rgba(232,235,232,0.5);">{passed}/{total}</td>
            <td>{cells}</td>
        </tr>'''

    # ─── Priorities ─────────────────────────────────────────────────
    ranked = sorted(
        ((k, v) for k, v in pillars.items() if v.get("level", 0) < 4),
        key=lambda kv: kv[1].get("level", 0),
    )
    priorities_html = ""
    if ranked:
        priorities_html = '<ol class="priority-list">'
        for key, data in ranked[:5]:
            pillar_meta = next(p for p in PILLARS if p.key == key)
            level = data.get("level", 0)
            next_level = level + 1
            score_val = data.get("score", 0)
            gap = LEVEL_NAMES[next_level] if next_level <= 4 else "—"
            color = CLUSTER_COLOR.get(pillar_meta.cluster_letter, "#888")
            priorities_html += f'''
            <li class="priority-item" style="border-left-color:{color}">
                <h3 class="priority-pillar">P{pillar_meta.n:02d} · {pillar_meta.title}</h3>
                <p class="priority-transition">
                    <span style="color:{LEVEL_COLOR[level]}">{LEVEL_SHORT[level]}</span> →
                    <span style="color:{LEVEL_COLOR[next_level]}">{LEVEL_SHORT[next_level]}</span>
                    &nbsp;·&nbsp; <span style="color:rgba(232,235,232,0.4)">Cluster {pillar_meta.cluster_letter} · {pillar_meta.cluster}</span>
                </p>
                <p class="priority-principle">{pillar_meta.principle}</p>
            </li>'''
        priorities_html += '</ol>'
    else:
        priorities_html = '<p style="color:#10b981;font-style:italic;font-family:var(--font-serif);font-size:1.1rem;">✨ All 12 pillars at L4 Optimizing. Maintain feedback loops · monitor for regression.</p>'

    # ─── Legend ─────────────────────────────────────────────────────
    legend_html = '<div class="legend">'
    for lvl in range(5):
        color = LEVEL_COLOR[lvl]
        cells = _maturity_cells(lvl)
        legend_html += f'''
        <div class="legend-row">
            <span class="legend-code" style="color:{color}">{LEVEL_SHORT[lvl]}</span>
            {cells}
            <span class="legend-name">{LEVEL_NAMES[lvl].split(" ", 1)[1]}</span>
            <span class="legend-desc">{LEVEL_DESCRIPTIONS[lvl]}</span>
        </div>'''
    legend_html += '</div>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Workspace Agentic Benchmark · Report · Grade {grade}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
{CSS}
</head>
<body>
<div class="container">
    <div class="brand">Workspace Agentic Benchmark · v{version}</div>
    <h1>Workspace<br><em>Benchmark Report</em></h1>
    <p class="subtitle">A first-principles audit across 12 pillars in 4 clusters · L0-L4 maturity model</p>

    <div class="meta">
        <span><b>Workspace</b> {workspace}</span>
        <span><b>Scored</b> {scored_at}</span>
        <span><b>Tool</b> workspace-bench v{version}</span>
    </div>

    <div class="eyebrow">Executive summary</div>
    <div class="composite-card">
        <div class="composite-score">
            <div class="composite-value" style="color:{grade_color};">{composite:.2f}</div>
            <div class="composite-max">/ 100 composite</div>
        </div>
        <div>
            <span class="grade-badge" style="background:{grade_color};">{grade}</span>
            <p class="grade-description">{grade_desc}</p>
        </div>
    </div>

    <div class="eyebrow">Cluster averages</div>
    <h2 style="margin-top:0.5rem;">Four dimensions of workspace maturity</h2>
    <div class="cluster-grid">
        {cluster_cards_html}
    </div>

    <div class="eyebrow" style="margin-top:3rem;">12 pillars</div>
    <h2 style="margin-top:0.5rem;">Per-pillar maturity breakdown</h2>
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Pillar</th>
                <th>Cluster</th>
                <th>Maturity level</th>
                <th style="text-align:right">Score</th>
                <th style="text-align:right">Criteria</th>
                <th>L0&nbsp;→&nbsp;L4</th>
            </tr>
        </thead>
        <tbody>
            {pillar_rows}
        </tbody>
    </table>

    <div class="eyebrow" style="margin-top:3rem;">Top improvement priorities</div>
    <h2 style="margin-top:0.5rem;">Ordered by gap to next maturity level</h2>
    {priorities_html}

    <div class="eyebrow" style="margin-top:3rem;">L0-L4 maturity model</div>
    <h2 style="margin-top:0.5rem;">CMMI-inspired · used by AWS Well-Architected · NIST AI RMF · OWASP</h2>
    {legend_html}

    <footer>
        Generated by workspace-bench v{version} · {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
        github.com/ceomadani/workspace-agentic-benchmark · MIT license
    </footer>
</div>
</body>
</html>
'''
