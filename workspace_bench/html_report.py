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


# Inline SVG · minimal Madani Lab mark · sage accent
MADANI_LOGO_SVG = '''<svg width="42" height="42" viewBox="0 0 42 42" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Nour Matine">
  <rect x="3" y="3" width="36" height="36" rx="6" stroke="#A8C0A8" stroke-width="1.5" fill="none"/>
  <path d="M11 30 L11 12 L21 22 L31 12 L31 30" stroke="#C8DDC8" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="21" cy="26" r="1.8" fill="#A8C0A8"/>
</svg>'''


CSS = """<style>
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
body { background: var(--bg); color: var(--fg); font-family: var(--font-sans); margin: 0; padding: 0; line-height: 1.6; font-size: 15px; }
.container { max-width: 1120px; margin: 0 auto; padding: 2.5rem 1.5rem 6rem; }

/* Branded header */
.brand-header { display: flex; align-items: center; gap: 1rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border); margin-bottom: 2rem; }
.brand-logo { display: flex; align-items: center; }
.brand-text { font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.18em; color: var(--accent); text-transform: uppercase; }
.brand-text b { color: var(--accent-bright); font-weight: 600; }
.brand-meta { margin-left: auto; font-family: var(--font-mono); font-size: 10px; color: var(--fg-faint); letter-spacing: 0.08em; }

h1 { font-family: var(--font-serif); font-size: clamp(2.4rem, 5vw, 3.4rem); line-height: 1.05; margin: 1.5rem 0 0.5rem; color: #F5F7F5; }
h1 em { font-style: italic; color: var(--accent-bright); }
.subtitle { font-family: var(--font-serif); font-style: italic; font-size: 1.05rem; color: var(--fg-dim); margin: 0 0 2rem; }
h2 { font-family: var(--font-serif); font-size: 1.5rem; color: #F5F7F5; margin: 3rem 0 0.5rem; }
h3 { font-family: var(--font-serif); font-size: 1.15rem; color: var(--accent-bright); margin: 1.75rem 0 0.5rem; }
.eyebrow { font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.18em; color: var(--accent); text-transform: uppercase; margin-bottom: 0.5rem; }
.meta { font-family: var(--font-mono); font-size: 12px; color: var(--fg-faint); margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border); }
.meta span { margin-right: 1.5rem; display: inline-block; }
.meta b { color: var(--fg-dim); font-weight: normal; }

/* Composite hero */
.composite-card { background: var(--bg-elev); border: 1px solid var(--border-strong); border-radius: 8px; padding: 2.5rem; margin: 2rem 0 3rem; display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: center; }
.composite-score { text-align: center; }
.composite-value { font-family: var(--font-serif); font-size: 4.5rem; line-height: 1; font-weight: 400; margin: 0; }
.composite-max { font-family: var(--font-mono); font-size: 0.85rem; color: var(--fg-faint); letter-spacing: 0.1em; margin-top: 0.5rem; }
.grade-badge { display: inline-block; padding: 0.6rem 1.5rem; border-radius: 8px; font-family: var(--font-mono); font-size: 2rem; font-weight: 700; color: #fff; margin-bottom: 0.75rem; letter-spacing: 0.05em; }
.grade-description { font-family: var(--font-serif); font-style: italic; color: var(--fg-dim); margin: 0; font-size: 0.95rem; }

/* Cluster cards */
.cluster-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin: 1.5rem 0 2rem; }
.cluster-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; padding: 1.25rem; }
.cluster-card .label { font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; }
.cluster-card .value { font-family: var(--font-serif); font-size: 2rem; line-height: 1; margin: 0.75rem 0; color: #F5F7F5; }
.cluster-card .progress { height: 6px; background: rgba(168, 192, 168, 0.08); border-radius: 3px; overflow: hidden; }
.cluster-card .progress-fill { height: 100%; border-radius: 3px; }
.cluster-card .desc { font-family: var(--font-serif); font-style: italic; font-size: 0.85rem; color: var(--fg-faint); margin: 0.5rem 0 0; line-height: 1.4; }

/* Pillar table */
table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-family: var(--font-mono); font-size: 13px; }
th { text-align: left; padding: 0.75rem 0.75rem; border-bottom: 2px solid var(--accent); color: var(--accent); font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; font-size: 11px; }
td { padding: 0.85rem 0.75rem; border-bottom: 1px solid var(--border); vertical-align: middle; }
tr:hover td { background: rgba(168, 192, 168, 0.04); }
td.pillar-name { font-family: var(--font-serif); font-size: 1rem; color: var(--accent-bright); }
.new-badge { display: inline-block; margin-left: 0.5rem; padding: 1px 6px; border: 1px solid var(--accent); border-radius: 3px; font-family: var(--font-mono); font-size: 9px; letter-spacing: 0.1em; color: var(--accent-bright); text-transform: uppercase; }
.level-badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-weight: 600; color: #fff; font-family: var(--font-mono); font-size: 12px; }
.maturity-bar { display: inline-flex; gap: 2px; align-items: center; }
.maturity-cell { width: 18px; height: 14px; border-radius: 2px; }
.cluster-tag { display: inline-block; padding: 2px 8px; border-radius: 3px; font-family: var(--font-mono); font-size: 10px; font-weight: 600; letter-spacing: 0.04em; color: #fff; }

/* TREES (the heart of v0.3.2) */
.tree { font-family: var(--font-mono); font-size: 13px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; padding: 1.5rem; margin: 1rem 0 2rem; overflow-x: auto; }
.tree-root { color: var(--accent-bright); font-family: var(--font-serif); font-size: 1.05rem; font-style: italic; margin-bottom: 0.75rem; padding-bottom: 0.75rem; border-bottom: 1px dashed var(--border); }
.tree-node { display: flex; align-items: baseline; gap: 0.5rem; padding: 4px 0; }
.tree-prefix { color: rgba(168, 192, 168, 0.35); white-space: pre; font-family: var(--font-mono); }
.tree-label { color: var(--fg-dim); }
.tree-meta { color: var(--fg-faint); font-size: 0.85em; margin-left: 0.5rem; }
.tree-tag { display: inline-block; padding: 1px 6px; border-radius: 3px; font-size: 9px; font-weight: 600; letter-spacing: 0.06em; color: #fff; margin-right: 0.4rem; }
.tree-section { margin-bottom: 2rem; }
.tree-pillar-link { color: var(--accent-bright); text-decoration: none; }
.tree-pillar-link:hover { text-decoration: underline; }

/* Pattern catalog */
.pattern-section { margin: 2rem 0; }
.pattern-row { display: grid; grid-template-columns: auto 1fr auto; gap: 1rem; align-items: baseline; padding: 0.6rem 0; border-bottom: 1px dashed rgba(168,192,168,0.10); }
.pattern-name { font-family: var(--font-serif); font-size: 1rem; color: var(--accent-bright); }
.pattern-source { font-family: var(--font-mono); font-size: 11px; color: var(--fg-faint); }
.pattern-abstract { font-family: var(--font-serif); font-style: italic; font-size: 0.9rem; color: var(--fg-dim); margin-top: 4px; }
.pattern-pillars { font-family: var(--font-mono); font-size: 10px; color: var(--accent); white-space: nowrap; }

/* Information theory */
.info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; margin: 1rem 0 2rem; }
.info-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; padding: 1rem; }
.info-card .label { font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); }
.info-card .value { font-family: var(--font-serif); font-size: 2rem; line-height: 1; margin: 0.5rem 0; color: #F5F7F5; }
.info-card .interpretation { font-family: var(--font-serif); font-style: italic; font-size: 0.8rem; color: var(--fg-faint); margin: 0; line-height: 1.4; }

/* Priorities */
.priority-list { counter-reset: priority; list-style: none; padding: 0; }
.priority-item { counter-increment: priority; background: var(--bg-card); border: 1px solid var(--border); border-left: 3px solid var(--accent); border-radius: 6px; padding: 1.25rem 1.5rem; margin: 0 0 1rem; position: relative; }
.priority-item::before { content: counter(priority); position: absolute; top: 1.25rem; right: 1.5rem; font-family: var(--font-serif); font-size: 2rem; color: var(--accent); line-height: 1; }
.priority-pillar { font-family: var(--font-serif); font-size: 1.1rem; color: var(--accent-bright); margin: 0 0 0.5rem; padding-right: 3rem; }
.priority-transition { font-family: var(--font-mono); font-size: 0.9rem; color: var(--fg-dim); margin: 0 0 0.5rem; }
.priority-principle { font-family: var(--font-serif); font-style: italic; color: var(--fg-dim); font-size: 0.95rem; margin: 0; line-height: 1.55; }

/* Legend */
.legend { background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; padding: 1.5rem; margin: 1rem 0; }
.legend-row { display: flex; align-items: center; gap: 1rem; padding: 0.5rem 0; }
.legend-code { font-family: var(--font-mono); font-weight: 700; min-width: 32px; }
.legend-name { font-family: var(--font-mono); color: var(--fg-dim); min-width: 110px; }
.legend-desc { font-family: var(--font-serif); color: var(--fg-dim); font-size: 0.95rem; }

footer { margin-top: 5rem; padding-top: 2rem; border-top: 1px solid var(--border); font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--fg-faint); }

@media print {
    body { background: white; color: #1a1a1a; }
    .container { max-width: none; padding: 1rem; }
    .composite-card, .cluster-card, .priority-item, .legend, .tree, .info-card { background: #f8f8f5; border-color: #ddd; }
    h1, h2, h3 { color: #1a1a1a; }
    a { color: #1a1a1a; text-decoration: underline; }
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
            cells.append('<span class="maturity-cell" style="background:rgba(168,192,168,0.12)"></span>')
    return f'<span class="maturity-bar">{"".join(cells)}</span>'


def _bar(value: float, max_value: float = 100) -> str:
    pct = max(0, min(100, (value / max_value) * 100))
    return f'<div style="height:6px;background:rgba(168,192,168,0.08);border-radius:3px;overflow:hidden;"><div style="height:100%;width:{pct}%;background:var(--accent);border-radius:3px;"></div></div>'


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


def _workspace_tree(workspace_path: Path | None, max_depth: int = 2, max_entries_per_dir: int = 25) -> str:
    """Walk workspace dir · render ASCII-tree of top-level structure for confirmation."""
    if workspace_path is None or not workspace_path.exists() or not workspace_path.is_dir():
        return ""

    lines = [f'<div class="tree-root">▸ {workspace_path.name}/ <span style="color:var(--fg-faint);font-size:0.85em;">— workspace identified · confirm before reading the report</span></div>']

    def _walk(d: Path, depth: int, prefix: str):
        if depth > max_depth:
            return
        try:
            entries = sorted(
                [e for e in d.iterdir() if e.name not in TREE_EXCLUDE and not e.name.startswith(".")],
                key=lambda e: (not e.is_dir(), e.name.lower()),
            )
        except (PermissionError, OSError):
            return
        if len(entries) > max_entries_per_dir:
            entries = entries[:max_entries_per_dir]
            truncated = True
        else:
            truncated = False
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└─ " if is_last else "├─ "
            icon = "📁" if entry.is_dir() else "📄"
            color = "var(--accent-bright)" if entry.is_dir() else "var(--fg-dim)"
            suffix = "/" if entry.is_dir() else ""
            lines.append(f'''<div class="tree-node">
                <span class="tree-prefix">{prefix}{connector}</span>
                <span class="tree-label" style="color:{color};">{icon} {entry.name}{suffix}</span>
            </div>''')
            if entry.is_dir() and depth < max_depth:
                next_prefix = prefix + ("    " if is_last else "│   ")
                _walk(entry, depth + 1, next_prefix)
        if truncated:
            lines.append(f'<div class="tree-node"><span class="tree-prefix">{prefix}</span><span class="tree-label" style="color:var(--fg-faint);font-style:italic;">… more entries truncated</span></div>')

    _walk(workspace_path, 1, "")
    return f'<div class="tree-section"><div class="tree">{"".join(lines)}</div></div>'


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
                <span class="tree-tag" style="background:rgba(168,192,168,0.18);color:var(--accent-bright);">{type_tag}</span>
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
            <div class="value">{avg:.1f}<span style="font-size:0.5em;color:rgba(232,235,232,0.4);"> / 100</span></div>
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
            <td style="color:rgba(232,235,232,0.4);">P{p_meta.n:02d}</td>
            <td class="pillar-name">{p_meta.title}{new_badge}</td>
            <td><span class="cluster-tag" style="background:{cluster_color}">{p_meta.cluster_letter}</span></td>
            <td><span class="level-badge" style="background:{level_color}">{LEVEL_SHORT[level]}</span>&nbsp;<span style="color:rgba(232,235,232,0.55);">{level_label.split(" ", 1)[1] if " " in level_label else ""}</span>{warn}</td>
            <td style="text-align:right;"><b style="color:{level_color};font-size:1.05rem">{score_val}</b><span style="color:rgba(232,235,232,0.3);"> / 100</span></td>
            <td style="text-align:right;color:rgba(232,235,232,0.5);">{passed}/{total}</td>
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
                    &nbsp;·&nbsp; <span style="color:rgba(232,235,232,0.4)">Cluster {p_meta.cluster_letter} · {p_meta.cluster}</span>
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

    {("<div class='eyebrow'>workspace identified · confirm before reading</div><h2 style='margin-top:0.5rem;'>Tree</h2>" + workspace_tree_html) if workspace_tree_html else ""}

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
