"""
Polished HTML report · multi-language · tree-heavy · Nour Matine · Madani Lab branded.

Self-contained · inline CSS · no external runtime deps.
Renders:
  - Nour Matine · Madani Lab branded header (inline SVG logo)
  - Composite hero + grade
  - Cluster grid
  - Pillar maturity table
  - PILLAR TREES (one per cluster, expandable)
  - PATTERN ADAPTER CATALOG (50+ resources organized as tree)
  - INFORMATION THEORY layer (α · SNR · entropy · density)
  - Improvement priority cards
  - L0-L4 legend
  - Print-friendly · responsive · multi-language
"""

from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any

from .data import PILLARS, CLUSTERS, LEVEL_NAMES, LEVEL_SHORT, LEVEL_DESCRIPTIONS, pillars_by_cluster
from .i18n import t, language_name
from .patterns import PATTERNS, CATEGORIES, patterns_by_category, patterns_by_pillar, pattern_coverage_per_pillar, total_patterns


GRADE_COLOR = {"A": "#10b981", "B": "#3b82f6", "C": "#f59e0b", "D": "#ef4444", "F": "#7c2d12"}
CLUSTER_COLOR = {"A": "#a855f7", "B": "#3b82f6", "C": "#f59e0b", "D": "#10b981"}
LEVEL_COLOR = {0: "#6b7280", 1: "#ef4444", 2: "#f59e0b", 3: "#3b82f6", 4: "#10b981"}


# Madani Lab research articles (live · https://www.madani.agency/[locale]/research/articles/<slug>)
MADANI_LAB_BASE = "https://www.madani.agency"
MADANI_LAB_ARTICLES = {
    "architettura-12-pillar":       "Architettura · 12 Pilastri",
    "catalogo-pattern-50":          "Catalogo · 50 Pattern",
    "forward-deploy-portabilita":   "Forward Deploy · Portabilità",
    "manifesto-vision":             "Manifesto · Vision",
    "maturita-l0-l4":               "Maturità · L0–L4",
    "metacognizione-prospettica":   "Metacognizione Prospettica",
    "multi-agent-dpi-stanford":     "Multi-Agent DPI · Stanford 2604.02460",
    "reliability-pass-at-k-mast":   "Reliability · pass@k MAST",
    "signal-to-noise-workspace":    "Signal-to-Noise · Workspace",
    "teoria-informazione-alpha":    "Teoria Informazione · α formula",
}

# Anomaly → list of relevant Madani Lab article slugs
EXTENSION_ARTICLES = {
    "01-architecture-capability-decoupling": ["teoria-informazione-alpha", "manifesto-vision"],
    "02-information-theory":                 ["signal-to-noise-workspace", "teoria-informazione-alpha"],
    "03-causal-reasoning":                   ["catalogo-pattern-50"],
    "04-adversarial-robustness":             ["reliability-pass-at-k-mast"],
    "05-compositionality":                   ["catalogo-pattern-50", "forward-deploy-portabilita"],
    "06-temporal-coherence":                 ["catalogo-pattern-50"],
    "07-embodied-awareness":                 ["metacognizione-prospettica"],
    "08-knowledge-representation":           ["signal-to-noise-workspace"],
    "09-resilience-partial-failure":         ["reliability-pass-at-k-mast", "forward-deploy-portabilita"],
    "10-index-density":                      ["signal-to-noise-workspace"],
    "11-meta-measurement":                   ["reliability-pass-at-k-mast", "maturita-l0-l4"],
}

# Per-pillar fallback when pillar is L0-L1
PILLAR_ARTICLES = {
    "P01": ["architettura-12-pillar", "manifesto-vision"],
    "P02": ["catalogo-pattern-50", "signal-to-noise-workspace"],
    "P03": ["catalogo-pattern-50"],
    "P04": ["metacognizione-prospettica", "catalogo-pattern-50"],
    "P05": ["catalogo-pattern-50"],
    "P06": ["multi-agent-dpi-stanford"],
    "P07": ["signal-to-noise-workspace"],
    "P08": ["reliability-pass-at-k-mast"],
    "P09": ["maturita-l0-l4", "architettura-12-pillar"],
    "P10": ["forward-deploy-portabilita"],
    "P11": ["reliability-pass-at-k-mast"],
    "P12": ["manifesto-vision", "teoria-informazione-alpha"],
}

# Folders excluded from workspace tree walk (noise · build artifacts · VCS)
TREE_EXCLUDE = {
    ".git", "node_modules", "__pycache__", ".pytest_cache", ".next", ".nuxt",
    "build", "dist", ".cache", ".turbo", ".vercel", ".vscode", ".idea",
    "venv", ".venv", "env", ".env", "target", "out", ".DS_Store",
}
CATEGORY_COLOR = {
    "foundational": "#a855f7",
    "production": "#3b82f6",
    "governance": "#f59e0b",
    "doctrine": "#10b981",
    "industry": "#06b6d4",
}


# Inline SVG · minimal Madani Lab mark · accent blue (HR#10 canonical palette)
MADANI_LOGO_SVG = '''<svg width="42" height="42" viewBox="0 0 42 42" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Nour Matine">
  <rect x="3" y="3" width="36" height="36" rx="6" stroke="#1a1a1a" stroke-width="1.5" fill="none"/>
  <path d="M11 30 L11 12 L21 22 L31 12 L31 30" stroke="#1a1a1a" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="21" cy="26" r="1.8" fill="#4D6BFF"/>
</svg>'''


# HR#10 canonical · derived from ~/madani/02_LEAD-GENERATION/02a_ORGANICA/CONTENT-PRODUCTION/06_TOOLS/madani-pdf-style.css
# Palette: white + #1a1a1a text + #4D6BFF accent · Satoshi + Instrument Serif italic + SF Mono · glass cards
CSS = """<style>
@import url('https://api.fontshare.com/v2/css?f[]=satoshi@300,400,500,600,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap');

:root {
    --bg: #FFFFFF;
    --bg-elev: rgba(248, 248, 250, 1);
    --bg-card: rgba(248, 248, 250, 0.8);
    --border: rgba(0, 0, 0, 0.06);
    --border-strong: rgba(0, 0, 0, 0.1);
    --fg: #1a1a1a;
    --fg-dim: rgba(26, 26, 26, 0.6);
    --fg-faint: rgba(26, 26, 26, 0.4);
    --accent: #4D6BFF;
    --accent-bright: #4D6BFF;
    --accent-glow: rgba(77, 107, 255, 0.08);
    --accent-line: rgba(77, 107, 255, 0.2);
    --emerald: #10b981;
    --rose: #f43f5e;
    --amber: #f59e0b;
    --glass-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
    --font-sans: 'Satoshi', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-serif: 'Instrument Serif', Georgia, serif;
    --font-mono: 'SF Mono', 'Fira Code', 'Fira Mono', 'Roboto Mono', monospace;
}
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background: var(--bg);
    color: var(--fg);
    font-family: var(--font-sans);
    font-size: 15px;
    font-weight: 400;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
.container { max-width: 920px; margin: 0 auto; padding: 3rem clamp(20px, 5vw, 40px) 6rem; }

/* Branded header */
.brand-header { display: flex; align-items: center; gap: 1rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border); margin-bottom: 2rem; }
.brand-logo { display: flex; align-items: center; }
.brand-text { font-family: var(--font-mono); font-size: 10px; font-weight: 600; letter-spacing: 0.08em; color: var(--fg-faint); text-transform: uppercase; line-height: 1.4; }
.brand-text b { color: var(--fg); font-weight: 700; }
.brand-meta { margin-left: auto; font-family: var(--font-mono); font-size: 10px; color: var(--fg-faint); letter-spacing: 0.04em; }

h1 {
    font-family: var(--font-sans);
    font-size: clamp(28px, 5vw, 44px);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: var(--fg);
    margin: 1.5rem 0 0.5rem;
}
h1 em { font-family: var(--font-serif); font-style: italic; font-weight: 400; color: var(--accent); letter-spacing: -0.01em; }
.subtitle { font-family: var(--font-serif); font-style: italic; font-size: 1.15rem; color: var(--fg-dim); margin: 0 0 2rem; line-height: 1.6; }
h2 {
    font-family: var(--font-sans);
    font-size: clamp(18px, 2.5vw, 22px);
    font-weight: 600;
    line-height: 1.2;
    letter-spacing: -0.02em;
    color: var(--fg);
    margin: 3rem 0 0.75rem;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
h3 { font-family: var(--font-sans); font-size: 17px; font-weight: 600; letter-spacing: -0.01em; color: var(--fg); margin: 1.75rem 0 0.5rem; }
.eyebrow { font-family: var(--font-mono); font-size: 10px; font-weight: 600; letter-spacing: 0.08em; color: var(--fg-faint); text-transform: uppercase; margin-bottom: 0.5rem; }
.meta { font-family: var(--font-mono); font-size: 12px; color: var(--fg-faint); margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border); }
.meta span { margin-right: 1.5rem; display: inline-block; }
.meta b { color: var(--fg-dim); font-weight: 600; }

/* Composite hero · glass card */
.composite-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: var(--glass-shadow);
    padding: 2.5rem;
    margin: 2rem 0 3rem;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    align-items: center;
}
.composite-score { text-align: center; }
.composite-value { font-family: var(--font-sans); font-size: 4.5rem; line-height: 1; font-weight: 700; letter-spacing: -0.04em; margin: 0; }
.composite-max { font-family: var(--font-mono); font-size: 0.8rem; color: var(--fg-faint); letter-spacing: 0.08em; text-transform: uppercase; margin-top: 0.5rem; }
.grade-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.6rem 1.5rem;
    border-radius: 999px;
    font-family: var(--font-mono);
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.75rem;
    letter-spacing: 0.05em;
}
.grade-description { font-family: var(--font-serif); font-style: italic; color: var(--fg-dim); margin: 0; font-size: 1rem; line-height: 1.6; }

/* Cluster cards · stat-box pattern */
.cluster-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin: 1.25rem 0 2rem; }
.cluster-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--fg);
    border-radius: 12px;
    box-shadow: var(--glass-shadow);
    padding: 16px 18px;
}
.cluster-card .label { font-family: var(--font-mono); font-size: 10px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--fg-faint); }
.cluster-card .value { font-family: var(--font-sans); font-size: 24px; font-weight: 700; line-height: 1.1; letter-spacing: -0.02em; margin: 0.75rem 0 0.5rem; color: var(--fg); }
.cluster-card .progress { height: 4px; background: rgba(0, 0, 0, 0.04); border-radius: 2px; overflow: hidden; margin: 0.5rem 0 0.6rem; }
.cluster-card .progress-fill { height: 100%; border-radius: 2px; }
.cluster-card .desc { font-family: var(--font-serif); font-style: italic; font-size: 0.85rem; color: var(--fg-dim); margin: 0; line-height: 1.5; }

/* Pillar table */
table { width: 100%; border-collapse: collapse; margin: 1rem 0 1.5rem; font-family: var(--font-sans); font-size: 13px; line-height: 1.5; }
th { background: var(--bg-elev); text-align: left; padding: 10px 10px; border-bottom: 2px solid rgba(0,0,0,0.08); color: var(--fg); font-family: var(--font-mono); font-weight: 600; font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; }
td { padding: 8px 10px; border-bottom: 1px solid rgba(0,0,0,0.05); vertical-align: middle; color: var(--fg-dim); }
tr:nth-child(even) td { background: rgba(248, 248, 250, 0.5); }
td.pillar-name { font-family: var(--font-sans); font-weight: 500; font-size: 14px; color: var(--fg); }
.new-badge { display: inline-block; margin-left: 0.5rem; padding: 1px 6px; border: 1px solid var(--accent); border-radius: 4px; font-family: var(--font-mono); font-size: 9px; font-weight: 600; letter-spacing: 0.08em; color: var(--accent); text-transform: uppercase; }
.level-badge { display: inline-block; padding: 3px 10px; border-radius: 999px; font-weight: 600; color: #fff; font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.04em; }
.maturity-bar { display: inline-flex; gap: 2px; align-items: center; }
.maturity-cell { width: 18px; height: 12px; border-radius: 2px; }
.cluster-tag { display: inline-block; padding: 2px 8px; border-radius: 999px; font-family: var(--font-mono); font-size: 10px; font-weight: 600; letter-spacing: 0.04em; color: #fff; }

/* TREES */
.tree {
    font-family: var(--font-mono);
    font-size: 12px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    box-shadow: var(--glass-shadow);
    padding: 1.5rem;
    margin: 1rem 0 2rem;
    overflow-x: auto;
    line-height: 1.7;
}
.tree-root { color: var(--fg); font-family: var(--font-serif); font-style: italic; font-size: 1.1rem; margin-bottom: 0.75rem; padding-bottom: 0.75rem; border-bottom: 1px dashed var(--border); }
.tree-node { display: flex; align-items: baseline; gap: 0.5rem; padding: 3px 0; }
.tree-prefix { color: var(--fg-faint); white-space: pre; font-family: var(--font-mono); }
.tree-label { color: var(--fg-dim); }
.tree-meta { color: var(--fg-faint); font-size: 0.9em; margin-left: 0.5rem; }
.tree-tag { display: inline-block; padding: 2px 7px; border-radius: 999px; font-family: var(--font-mono); font-size: 9px; font-weight: 600; letter-spacing: 0.06em; color: #fff; margin-right: 0.4rem; text-transform: uppercase; }
.tree-section { margin-bottom: 1.5rem; }
.tree-pillar-link { color: var(--accent); text-decoration: none; }
.tree-pillar-link:hover { color: var(--accent); text-decoration: underline; }

/* Pattern catalog */
.pattern-section { margin: 2rem 0; }
.pattern-row { display: grid; grid-template-columns: auto 1fr auto; gap: 1rem; align-items: baseline; padding: 0.6rem 0; border-bottom: 1px dashed rgba(0,0,0,0.06); }
.pattern-name { font-family: var(--font-sans); font-weight: 500; font-size: 1rem; color: var(--fg); }
.pattern-source { font-family: var(--font-mono); font-size: 11px; color: var(--fg-faint); }
.pattern-abstract { font-family: var(--font-serif); font-style: italic; font-size: 0.95rem; color: var(--fg-dim); margin-top: 4px; line-height: 1.5; }
.pattern-pillars { font-family: var(--font-mono); font-size: 10px; color: var(--accent); white-space: nowrap; }

/* Information theory · stat-box pattern */
.info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin: 1rem 0 2rem; }
.info-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--fg);
    border-radius: 12px;
    box-shadow: var(--glass-shadow);
    padding: 16px 18px;
}
.info-card .label { font-family: var(--font-mono); font-size: 10px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--fg-faint); }
.info-card .value { font-family: var(--font-sans); font-size: 24px; font-weight: 700; line-height: 1.1; letter-spacing: -0.02em; color: var(--fg); margin: 0.5rem 0 0.5rem; }
.info-card .interpretation { font-family: var(--font-serif); font-style: italic; font-size: 0.85rem; color: var(--fg-dim); margin: 0; line-height: 1.5; }

/* Priorities */
.priority-list { counter-reset: priority; list-style: none; padding: 0; }
.priority-item {
    counter-increment: priority;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 12px;
    box-shadow: var(--glass-shadow);
    padding: 1.25rem 1.5rem;
    margin: 0 0 1rem;
    position: relative;
}
.priority-item::before { content: counter(priority); position: absolute; top: 1rem; right: 1.5rem; font-family: var(--font-serif); font-size: 2.5rem; color: var(--fg-faint); line-height: 1; font-style: italic; }
.priority-pillar { font-family: var(--font-sans); font-weight: 600; font-size: 1.05rem; color: var(--fg); margin: 0 0 0.4rem; padding-right: 3rem; letter-spacing: -0.01em; }
.priority-transition { font-family: var(--font-mono); font-size: 0.85rem; color: var(--fg-dim); margin: 0 0 0.5rem; }
.priority-principle { font-family: var(--font-serif); font-style: italic; color: var(--fg-dim); font-size: 1rem; margin: 0; line-height: 1.55; }

/* Legend */
.legend { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; box-shadow: var(--glass-shadow); padding: 1.5rem; margin: 1rem 0; }
.legend-row { display: flex; align-items: center; gap: 1rem; padding: 0.5rem 0; }
.legend-code { font-family: var(--font-mono); font-weight: 700; font-size: 13px; min-width: 32px; }
.legend-name { font-family: var(--font-mono); color: var(--fg-dim); font-size: 12px; min-width: 110px; }
.legend-desc { font-family: var(--font-serif); color: var(--fg-dim); font-size: 1rem; line-height: 1.5; }

/* Anomaly card · canonical signal pattern */
.anomaly-item { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; box-shadow: var(--glass-shadow); padding: 1rem 1.25rem; margin-bottom: 0.75rem; }
.article-link { color: var(--accent); text-decoration: none; border-bottom: 1px solid var(--accent-line); font-family: var(--font-sans); font-weight: 500; transition: border-color 0.15s; }
.article-link:hover { border-bottom-color: var(--accent); }

/* Workspace tree · compact ASCII · canonical pattern madani.agency/research */
.workspace-tree {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    box-shadow: var(--glass-shadow);
    padding: 1.25rem 1.5rem;
    margin: 1rem 0 2rem;
    font-family: var(--font-mono);
    font-size: 12.5px;
    line-height: 1.7;
    overflow-x: auto;
}
.ws-tree-row { display: flex; align-items: baseline; gap: 1rem; white-space: nowrap; }
.ws-tree-label { color: var(--fg-dim); white-space: pre; }
.ws-tree-meta { color: var(--fg-faint); font-size: 0.85em; margin-left: auto; white-space: nowrap; }
.ws-tree-rootrow { padding-bottom: 0.5rem; margin-bottom: 0.4rem; border-bottom: 1px dashed var(--border); }
.ws-tree-rootrow .ws-tree-label { color: var(--fg); font-weight: 600; }
.ws-tree-rootrow .ws-tree-meta { font-size: 10px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--fg-faint); }

footer { margin-top: 5rem; padding-top: 2rem; border-top: 1px solid var(--border); font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.04em; color: var(--fg-faint); text-align: center; line-height: 1.8; }
footer em { font-family: var(--font-serif); }

@media print {
    body { background: white; color: var(--fg); }
    .container { max-width: none; padding: 1rem; }
    .composite-card, .cluster-card, .priority-item, .legend, .tree, .info-card, .anomaly-item {
        background: rgba(248, 248, 250, 0.6);
        border-color: rgba(0,0,0,0.08);
        box-shadow: none;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
        break-inside: avoid;
    }
    h1, h2, h3 { color: var(--fg); }
    a { color: var(--accent); text-decoration: underline; }
}
@media (max-width: 720px) {
    .composite-card { grid-template-columns: 1fr; text-align: center; }
    .container { padding: 1.5rem 1rem 4rem; }
    table { font-size: 11px; }
    th, td { padding: 0.5rem 0.4rem; }
    .pattern-row { grid-template-columns: 1fr; }
}
</style>"""


def _maturity_cells(level: int) -> str:
    cells = []
    for i in range(4):
        if i < level:
            color = LEVEL_COLOR.get(level, "#666")
            cells.append(f'<span class="maturity-cell" style="background:{color}"></span>')
        else:
            cells.append('<span class="maturity-cell" style="background:rgba(0,0,0,0.06)"></span>')
    return f'<span class="maturity-bar">{"".join(cells)}</span>'


def _bar(value: float, max_value: float = 100) -> str:
    pct = max(0, min(100, (value / max_value) * 100))
    return f'<div style="height:4px;background:rgba(0,0,0,0.04);border-radius:2px;overflow:hidden;"><div style="height:100%;width:{pct}%;background:var(--accent);border-radius:2px;"></div></div>'


def _tree_pillar(score: dict, lang: str) -> str:
    """Render one tree per cluster containing its pillars."""
    pillars = score.get("pillars", {})
    parts = []
    for letter, name, desc in CLUSTERS:
        cluster_pillars = pillars_by_cluster(letter)
        if not cluster_pillars:
            continue
        cluster_color = CLUSTER_COLOR.get(letter, "#888")
        parts.append(f'<div class="tree-section"><div class="tree">')
        parts.append(f'<div class="tree-root">▸ Cluster {letter} · {name} <span style="color:{cluster_color};font-size:0.85em;">— {desc}</span></div>')
        for i, p in enumerate(cluster_pillars):
            data = pillars.get(p.key, {})
            level = data.get("level", 0)
            score_val = data.get("score", 0)
            passed = data.get("criteria_passed", 0)
            total = data.get("criteria_total", 10)
            level_color = LEVEL_COLOR.get(level, "#888")
            is_last = i == len(cluster_pillars) - 1
            prefix = "└─ " if is_last else "├─ "
            new = ' <span class="new-badge">⭐</span>' if p.is_new_v03 else ""
            parts.append(f'''<div class="tree-node">
                <span class="tree-prefix">{prefix}</span>
                <span class="tree-label">P{p.n:02d} · {p.title}{new}</span>
                <span class="tree-meta">
                    <span class="level-badge" style="background:{level_color}">{LEVEL_SHORT[level]}</span>
                    {score_val}/100 · {passed}/{total} {t("criteria", lang).lower()}
                </span>
            </div>''')
            # Sub-tree: principle
            sub_prefix = "    " if is_last else "│   "
            parts.append(f'''<div class="tree-node" style="margin-left:0;font-size:0.85em;font-style:italic;color:var(--fg-faint);">
                <span class="tree-prefix">{sub_prefix}└─</span>
                <span>{p.principle}</span>
            </div>''')
        parts.append('</div></div>')
    return "".join(parts)


def _tree_patterns(lang: str) -> str:
    """Render pattern adapter catalog as trees grouped by category."""
    parts = [f'<p class="subtitle" style="margin-bottom:1.5rem;">{t("patterns_subtitle", lang)}</p>']
    coverage = pattern_coverage_per_pillar()
    parts.append(f'<p style="font-family:var(--font-mono);font-size:12px;color:var(--accent);margin-bottom:1rem;letter-spacing:0.08em;text-transform:uppercase;">{total_patterns()} {t("patterns_total", lang)}</p>')

    for cat_code, cat_label in CATEGORIES:
        cat_color = CATEGORY_COLOR.get(cat_code, "#888")
        items = patterns_by_category(cat_code)
        if not items:
            continue
        parts.append(f'<div class="tree-section"><div class="tree">')
        parts.append(f'<div class="tree-root">▸ {cat_label} <span style="color:{cat_color};font-size:0.85em;">— {len(items)} patterns</span></div>')
        for i, p in enumerate(items):
            is_last = i == len(items) - 1
            prefix = "└─ " if is_last else "├─ "
            pillar_tags = " ".join(f'P{n:02d}' for n in p.pillars)
            parts.append(f'''<div class="tree-node">
                <span class="tree-prefix">{prefix}</span>
                <span class="tree-label" style="color:var(--accent-bright);">{p.name}</span>
                <span class="tree-meta" style="margin-left:auto;">
                    <span class="tree-tag" style="background:{cat_color}">{cat_code}</span>
                    <span class="pattern-pillars">{pillar_tags}</span>
                </span>
            </div>''')
            sub_prefix = "    " if is_last else "│   "
            parts.append(f'''<div class="tree-node" style="font-size:0.85em;">
                <span class="tree-prefix">{sub_prefix}├─</span>
                <span style="color:var(--fg-faint);font-family:var(--font-mono);">{p.source} · {p.year}</span>
            </div>''')
            parts.append(f'''<div class="tree-node" style="font-size:0.88em;font-style:italic;color:var(--fg-dim);">
                <span class="tree-prefix">{sub_prefix}└─</span>
                <span>{p.abstract}</span>
            </div>''')
        parts.append('</div></div>')

    # Coverage tree · per pillar
    parts.append('<h3>Pattern coverage per pillar</h3>')
    parts.append('<div class="tree-section"><div class="tree">')
    parts.append('<div class="tree-root">▸ How many catalog patterns inform each pillar</div>')
    for p in PILLARS:
        count = coverage.get(p.n, 0)
        cluster_color = CLUSTER_COLOR.get(p.cluster_letter, "#888")
        is_last = p.n == 12
        prefix = "└─ " if is_last else "├─ "
        bar_filled = min(20, count)
        bar = "█" * bar_filled + "░" * (20 - bar_filled)
        parts.append(f'''<div class="tree-node">
            <span class="tree-prefix">{prefix}</span>
            <span class="tree-label">P{p.n:02d} · {p.title}</span>
            <span class="tree-meta" style="margin-left:auto;color:{cluster_color};">{count} patterns <span style="color:{cluster_color};font-family:var(--font-mono);font-size:11px;">{bar}</span></span>
        </div>''')
    parts.append('</div></div>')

    return "".join(parts)


def _info_theory_section(info: dict, lang: str) -> str:
    """Render information theory metrics section."""
    interpretations = info.get("interpretation", {})
    comp = info.get("components", {})

    cards_html = ""
    cards = [
        ("alpha_label", info.get("alpha", 0), interpretations.get("alpha", ""), "#a855f7"),
        ("snr_label", f'{info.get("snr_db", 0)} dB', interpretations.get("snr", ""), "#3b82f6"),
        ("entropy_label", f'{info.get("entropy_bits", 0)} bits', interpretations.get("entropy", ""), "#f59e0b"),
        ("density_label", f'{info.get("density", 0)}%', "", "#10b981"),
        ("quality_label", info.get("quality_index", 0), interpretations.get("balance", ""), "#06b6d4"),
        ("quantity_label", info.get("quantity_index", 0), "", "#ec4899"),
    ]
    for label_key, value, interp, color in cards:
        cards_html += f'''<div class="info-card" style="border-left:3px solid {color};">
            <div class="label" style="color:{color}">{t(label_key, lang)}</div>
            <div class="value">{value}</div>
            <p class="interpretation">{interp}</p>
        </div>'''

    # Components tree
    components_tree = '<div class="tree-section"><div class="tree">'
    components_tree += '<div class="tree-root">▸ Information theory components · raw counts</div>'
    component_rows = [
        ("Files total", comp.get("files_total", 0)),
        ("Docs (md/rst/txt)", comp.get("files_docs", 0)),
        ("Code files", comp.get("files_code", 0)),
        ("Config files", comp.get("files_config", 0)),
        ("Assets", comp.get("files_assets", 0)),
        ("Files with frontmatter", comp.get("files_with_frontmatter", 0)),
        ("Frontmatter rate", f'{comp.get("frontmatter_rate_pct", 0)}%'),
        ("Wiki-style cross-links", comp.get("cross_links_total", 0)),
        ("arXiv citations", comp.get("arxiv_citations", 0)),
        ("Markdown links", comp.get("md_links", 0)),
        ("Stale files (>6 months)", f'{comp.get("files_stale_pct", 0)}%'),
        ("Empty / near-empty", f'{comp.get("files_empty_or_near_empty_pct", 0)}%'),
        ("Citation density", f'{comp.get("citation_density_pct", 0)}%'),
        ("Structure ratio", f'{comp.get("structure_ratio_pct", 0)}%'),
    ]
    for i, (label, value) in enumerate(component_rows):
        is_last = i == len(component_rows) - 1
        prefix = "└─ " if is_last else "├─ "
        components_tree += f'''<div class="tree-node">
            <span class="tree-prefix">{prefix}</span>
            <span class="tree-label">{label}</span>
            <span class="tree-meta" style="margin-left:auto;color:var(--accent-bright);">{value}</span>
        </div>'''
    components_tree += '</div></div>'

    return f'''
    <p class="subtitle" style="margin-bottom:1rem;">{t("info_theory_subtitle", lang)}</p>
    <div class="info-grid">{cards_html}</div>
    {components_tree}
    '''


def _article_link(slug: str, lang: str) -> str:
    """Render <a> link to Madani Lab research article."""
    title = MADANI_LAB_ARTICLES.get(slug, slug)
    locale = lang if lang in ("it", "en", "fr") else "it"
    url = f"{MADANI_LAB_BASE}/{locale}/research/articles/{slug}"
    return f'<a href="{url}" target="_blank" rel="noopener" class="article-link" style="color:var(--accent-bright);text-decoration:none;border-bottom:1px dashed var(--accent);">{title}</a>'


def _fmt_size(b: int) -> str:
    """Compact size string: 12 KB, 1.2 MB, 5 GB."""
    if b < 1024:
        return f"{b} B"
    if b < 1024 ** 2:
        return f"{b // 1024} KB"
    if b < 1024 ** 3:
        v = b / 1024 ** 2
        return f"{v:.1f} MB" if v < 10 else f"{int(v)} MB"
    v = b / 1024 ** 3
    return f"{v:.1f} GB" if v < 10 else f"{int(v)} GB"


def _dir_aggregate(d: Path) -> tuple[int, int]:
    """Quick (non-recursive) count + size for a folder. Bounded · skips noise."""
    count = 0
    size = 0
    try:
        for entry in d.iterdir():
            if entry.name in TREE_EXCLUDE or entry.name.startswith("."):
                continue
            count += 1
            if entry.is_file():
                try:
                    size += entry.stat().st_size
                except OSError:
                    pass
    except (PermissionError, OSError):
        pass
    return count, size


def _workspace_tree(workspace_path: Path | None, max_lines: int = 28) -> str:
    """Compact ASCII workspace tree · canonical pattern from madani.agency/research.

    ~25 lines max · 2 levels · folders with many subdirs aggregated as `─── N entries ───`.
    Static (no collapse) · monospaced · right-aligned size column.
    """
    if workspace_path is None or not workspace_path.exists() or not workspace_path.is_dir():
        return ""

    try:
        top_entries = sorted(
            [e for e in workspace_path.iterdir() if e.name not in TREE_EXCLUDE and not e.name.startswith(".")],
            key=lambda e: (not e.is_dir(), e.name.lower()),
        )
    except (PermissionError, OSError):
        return ""

    lines: list[tuple[str, str]] = []  # (label, right_meta)

    for i, entry in enumerate(top_entries):
        if len(lines) >= max_lines:
            lines.append((f"└── ... {len(top_entries) - i} more entries truncated", ""))
            break

        is_last_top = (i == len(top_entries) - 1)
        connector = "└──" if is_last_top else "├──"

        if entry.is_file():
            try:
                size = entry.stat().st_size
            except OSError:
                size = 0
            lines.append((f"{connector} {entry.name}", _fmt_size(size)))
        else:
            sub_count, sub_size = _dir_aggregate(entry)
            lines.append((f"{connector} {entry.name}/", f"{sub_count} entries · {_fmt_size(sub_size)}" if sub_count else ""))

            # Decide: inline subdirs (if ≤4) or aggregation line (if more)
            if sub_count == 0:
                continue
            try:
                subs = sorted(
                    [e for e in entry.iterdir() if e.name not in TREE_EXCLUDE and not e.name.startswith(".")],
                    key=lambda e: (not e.is_dir(), e.name.lower()),
                )
            except (PermissionError, OSError):
                continue

            indent = "    " if is_last_top else "│   "

            if len(subs) > 4:
                # Aggregation line for crowded folders
                if len(lines) < max_lines:
                    lines.append((f"{indent}└── ─── {len(subs)} entries ───", ""))
            else:
                for j, sub in enumerate(subs):
                    if len(lines) >= max_lines:
                        break
                    is_last_sub = (j == len(subs) - 1)
                    sub_conn = "└──" if is_last_sub else "├──"
                    if sub.is_file():
                        try:
                            sz = sub.stat().st_size
                        except OSError:
                            sz = 0
                        lines.append((f"{indent}{sub_conn} {sub.name}", _fmt_size(sz)))
                    else:
                        sc, sz = _dir_aggregate(sub)
                        lines.append((f"{indent}{sub_conn} {sub.name}/", f"{sc} entries" if sc else ""))

    # Compute total root size summary
    root_count = len(top_entries)

    # Render rows · 80-col layout with right-aligned meta
    rows_html = []
    for label, meta in lines:
        # Escape label for HTML safety
        safe_label = label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        rows_html.append(
            f'<div class="ws-tree-row"><span class="ws-tree-label">{safe_label}</span><span class="ws-tree-meta">{meta}</span></div>'
        )

    body = "".join(rows_html)

    return f'''<div class="workspace-tree">
    <div class="ws-tree-row ws-tree-rootrow">
        <span class="ws-tree-label">{workspace_path.name}/</span>
        <span class="ws-tree-meta">{root_count} top-level · workspace identified</span>
    </div>
    {body}
</div>'''


def _anomalies_section(score: dict, lang: str) -> str:
    """Detect anomalies (L0-L1 pillars + absent/partial extensions) · render with article cross-references."""
    pillars = score.get("pillars", {})
    extensions = score.get("extensions", {})

    anomalies = []

    # Pillar anomalies (L0-L1 = missing/initial)
    for p in PILLARS:
        data = pillars.get(p.key, {})
        level = data.get("level", 0)
        if level <= 1:
            articles = PILLAR_ARTICLES.get(f"P{p.n:02d}", [])
            anomalies.append({
                "type": "pillar",
                "code": f"P{p.n:02d}",
                "title": p.title,
                "detail": f"{LEVEL_NAMES.get(level, '?')} · score {data.get('score', 0)}/100",
                "severity": "high" if level == 0 else "medium",
                "articles": articles,
            })

    # Extension anomalies (absent/partial)
    if isinstance(extensions, dict) and extensions:
        for ext_id, ext_data in extensions.items():
            if not isinstance(ext_data, dict):
                continue
            status = ext_data.get("status", "absent")
            if status in ("absent", "partial"):
                articles = EXTENSION_ARTICLES.get(ext_id, [])
                title = ext_data.get("title", ext_id)
                anomalies.append({
                    "type": "extension",
                    "code": ext_id,
                    "title": title,
                    "detail": f"status: {status}",
                    "severity": "high" if status == "absent" else "medium",
                    "articles": articles,
                })

    if not anomalies:
        return f'<p style="color:#10b981;font-style:italic;font-family:var(--font-serif);font-size:1.05rem;margin:1rem 0 2rem;">✓ No anomalies detected · all pillars L2+ · all extensions present</p>'

    rows_html = []
    for a in anomalies:
        sev_color = "#ef4444" if a["severity"] == "high" else "#f59e0b"
        sev_label = "HIGH" if a["severity"] == "high" else "MED"
        articles_html = " · ".join(_article_link(s, lang) for s in a["articles"]) if a["articles"] else '<span style="color:var(--fg-faint);font-style:italic;">no article reference yet</span>'
        type_tag = "PILLAR" if a["type"] == "pillar" else "EXT"
        rows_html.append(f'''
        <div class="anomaly-item" style="background:var(--bg-card);border:1px solid var(--border);border-left:3px solid {sev_color};border-radius:6px;padding:1rem 1.25rem;margin-bottom:0.75rem;">
            <div style="display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap;margin-bottom:0.4rem;">
                <span class="tree-tag" style="background:{sev_color};color:#fff;">{sev_label}</span>
                <span class="tree-tag" style="background:var(--accent-glow);color:var(--accent);">{type_tag}</span>
                <span style="font-family:var(--font-mono);font-size:11px;color:var(--fg-faint);letter-spacing:0.04em;">{a["code"]}</span>
                <span style="font-family:var(--font-serif);font-size:1.05rem;color:var(--accent-bright);">{a["title"]}</span>
                <span style="font-family:var(--font-mono);font-size:11px;color:var(--fg-faint);margin-left:auto;">{a["detail"]}</span>
            </div>
            <div style="font-family:var(--font-mono);font-size:11px;color:var(--fg-faint);letter-spacing:0.06em;text-transform:uppercase;margin-top:0.5rem;">→ relevant reading · Madani Lab</div>
            <div style="font-family:var(--font-serif);font-size:0.95rem;color:var(--fg-dim);margin-top:0.3rem;line-height:1.6;">{articles_html}</div>
        </div>''')

    return f'<div style="margin:1rem 0 2.5rem;">{"".join(rows_html)}</div>'


def render_html(score: dict, audit: dict | None = None, info_theory: dict | None = None, language: str = "en", workspace_name: str = "", workspace_path: Path | None = None) -> str:
    composite = score.get("composite", 0)
    grade = score.get("grade", "F")
    grade_desc = score.get("grade_description", "")
    workspace = score.get("workspace", "?")
    pillars = score.get("pillars", {})
    cluster_avgs = score.get("cluster_averages", {})
    scored_at = score.get("scored_at", "?")
    version = score.get("version", "?")
    lang = language if language in ("en", "it", "fr", "es", "de", "pt") else "en"

    grade_color = GRADE_COLOR.get(grade, "#888")

    cluster_cards_html = ""
    for letter, name, desc in CLUSTERS:
        if letter not in cluster_avgs:
            continue
        avg = cluster_avgs[letter]["average"]
        color = CLUSTER_COLOR.get(letter, "#888")
        cluster_cards_html += f'''
        <div class="cluster-card">
            <div class="label" style="color:{color}">{letter} · {name}</div>
            <div class="value">{avg:.1f}<span style="font-size:0.5em;color:var(--fg-faint);"> / 100</span></div>
            <div class="progress"><div class="progress-fill" style="width:{avg}%;background:{color}"></div></div>
            <p class="desc">{desc}</p>
        </div>'''

    pillar_rows = ""
    for p_meta in PILLARS:
        data = pillars.get(p_meta.key, {})
        level = data.get("level", 0)
        score_val = data.get("score", 0)
        passed = data.get("criteria_passed", 0)
        total = data.get("criteria_total", 10)
        cluster_color = CLUSTER_COLOR.get(p_meta.cluster_letter, "#888")
        level_color = LEVEL_COLOR.get(level, "#888")
        level_label = LEVEL_NAMES.get(level, "?")
        cells = _maturity_cells(level)
        new_badge = '<span class="new-badge">⭐</span>' if p_meta.is_new_v03 else ''
        warn = ' <span title="needs improvement">⚠</span>' if level <= 2 else ''
        pillar_rows += f'''
        <tr>
            <td style="color:var(--fg-faint);">P{p_meta.n:02d}</td>
            <td class="pillar-name">{p_meta.title}{new_badge}</td>
            <td><span class="cluster-tag" style="background:{cluster_color}">{p_meta.cluster_letter}</span></td>
            <td><span class="level-badge" style="background:{level_color}">{LEVEL_SHORT[level]}</span>&nbsp;<span style="color:var(--fg-dim);">{level_label.split(" ", 1)[1] if " " in level_label else ""}</span>{warn}</td>
            <td style="text-align:right;"><b style="color:{level_color};font-size:1.05rem">{score_val}</b><span style="color:var(--fg-faint);"> / 100</span></td>
            <td style="text-align:right;color:var(--fg-dim);">{passed}/{total}</td>
            <td>{cells}</td>
        </tr>'''

    ranked = sorted(
        ((k, v) for k, v in pillars.items() if v.get("level", 0) < 4),
        key=lambda kv: kv[1].get("level", 0),
    )
    priorities_html = ""
    if ranked:
        priorities_html = '<ol class="priority-list">'
        for key, data in ranked[:5]:
            p_meta = next(p for p in PILLARS if p.key == key)
            level = data.get("level", 0)
            next_level = level + 1
            score_val = data.get("score", 0)
            color = CLUSTER_COLOR.get(p_meta.cluster_letter, "#888")
            next_score = {0: 20, 1: 50, 2: 75, 3: 100, 4: 100}.get(next_level, 100)
            gap = next_score - score_val
            priorities_html += f'''
            <li class="priority-item" style="border-left-color:{color}">
                <h3 class="priority-pillar">P{p_meta.n:02d} · {p_meta.title}</h3>
                <p class="priority-transition">
                    <span style="color:{LEVEL_COLOR[level]}">{LEVEL_SHORT[level]}</span> →
                    <span style="color:{LEVEL_COLOR[next_level]}">{LEVEL_SHORT[next_level]}</span>
                    &nbsp;·&nbsp; +{gap} {t("pts_on_pillar", lang)}
                    &nbsp;·&nbsp; <span style="color:var(--fg-faint)">Cluster {p_meta.cluster_letter} · {p_meta.cluster}</span>
                </p>
                <p class="priority-principle">{p_meta.principle}</p>
            </li>'''
        priorities_html += '</ol>'
    else:
        priorities_html = f'<p style="color:#10b981;font-style:italic;font-family:var(--font-serif);font-size:1.1rem;">✨ {t("no_priorities", lang)}</p>'

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

    info_section = ""
    if info_theory:
        info_section = f'''
        <div class="eyebrow" style="margin-top:3.5rem;">{t("info_theory", lang)}</div>
        <h2 style="margin-top:0.5rem;">{t("info_theory_subtitle", lang)}</h2>
        {_info_theory_section(info_theory, lang)}
        '''

    workspace_display = workspace_name if workspace_name else workspace
    workspace_tree_html = _workspace_tree(workspace_path) if workspace_path else ""
    anomalies_html = _anomalies_section(score, lang)

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t("title", lang)} · {grade}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
{CSS}
</head>
<body>
<div class="container">

    <header class="brand-header">
        <div class="brand-logo">{MADANI_LOGO_SVG}</div>
        <div class="brand-text">Nour Matine<br><b>Madani Lab</b><br><span style="color:var(--fg-faint);font-size:9px;letter-spacing:0.14em;">{t("report_language", lang).upper()}: {language_name(lang)} ({lang})</span></div>
        <div class="brand-meta">workspace-bench · v{version}</div>
    </header>

    <h1>{t("title", lang).split(" · ")[0]}<br><em>{t("title", lang).split(" · ")[1] if " · " in t("title", lang) else ""}</em></h1>
    <p class="subtitle">{t("subtitle", lang)}</p>

    <div class="meta">
        <span><b>{t("workspace", lang)}</b> {workspace_display}</span>
        <span><b>{t("scored", lang)}</b> {scored_at}</span>
        <span><b>{t("tool", lang)}</b> workspace-bench v{version}</span>
        <span><b>{t("language_detected", lang)}</b> {language_name(lang)} ({lang})</span>
    </div>

    {("<div class='eyebrow'>workspace identified · confirm before reading</div><h2 style='margin-top:0.5rem;'>Structure</h2>" + workspace_tree_html) if workspace_tree_html else ""}

    <div class="eyebrow">{t("executive_summary", lang)}</div>
    <div class="composite-card">
        <div class="composite-score">
            <div class="composite-value" style="color:{grade_color};">{composite:.2f}</div>
            <div class="composite-max">/ 100 {t("composite", lang).lower()}</div>
        </div>
        <div>
            <span class="grade-badge" style="background:{grade_color};">{grade}</span>
            <p class="grade-description">{grade_desc}</p>
        </div>
    </div>

    <div class="eyebrow">{t("cluster_averages", lang)}</div>
    <h2 style="margin-top:0.5rem;">{t("four_dimensions", lang)}</h2>
    <div class="cluster-grid">
        {cluster_cards_html}
    </div>

    <div class="eyebrow" style="margin-top:3rem;">{t("12_pillars", lang)}</div>
    <h2 style="margin-top:0.5rem;">{t("per_pillar_breakdown", lang)}</h2>
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>{t("pillar", lang)}</th>
                <th>{t("cluster", lang)}</th>
                <th>{t("maturity_level", lang)}</th>
                <th style="text-align:right">{t("score", lang)}</th>
                <th style="text-align:right">{t("criteria", lang)}</th>
                <th>L0&nbsp;→&nbsp;L4</th>
            </tr>
        </thead>
        <tbody>
            {pillar_rows}
        </tbody>
    </table>

    <div class="eyebrow" style="margin-top:3rem;">{t("evidence_tree", lang)}</div>
    <h2 style="margin-top:0.5rem;">{t("per_pillar_breakdown", lang)} · trees</h2>
    {_tree_pillar(score, lang)}

    {info_section}

    <div class="eyebrow" style="margin-top:3.5rem;">anomalies detected</div>
    <h2 style="margin-top:0.5rem;">Anomalies · cross-referenced with Madani Lab research</h2>
    <p class="subtitle" style="margin-bottom:1rem;">Each anomaly (L0-L1 pillar · absent/partial extension) is linked to research articles that explain the gap and the path forward.</p>
    {anomalies_html}

    <div class="eyebrow" style="margin-top:3.5rem;">{t("improvement_priorities", lang)}</div>
    <h2 style="margin-top:0.5rem;">{t("ordered_by_gap", lang)}</h2>
    {priorities_html}

    <div class="eyebrow" style="margin-top:3.5rem;">{t("patterns_catalog", lang)}</div>
    <h2 style="margin-top:0.5rem;">{t("patterns_catalog", lang)}</h2>
    {_tree_patterns(lang)}

    <div class="eyebrow" style="margin-top:3.5rem;">{t("maturity_legend", lang)}</div>
    <h2 style="margin-top:0.5rem;">{t("cmmi_inspired", lang)}</h2>
    {legend_html}

    <footer>
        {t("generated_by", lang)} workspace-bench v{version} · {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
        github.com/ceomadani/workspace-agentic-benchmark · MIT license · Nour Matine · Madani Lab
    </footer>
</div>
</body>
</html>
'''
