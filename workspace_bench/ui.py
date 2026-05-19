"""
Rich-based terminal rendering · `slash context` style ultra-detailed UI.

Inspired by Claude Code /context display: visual block indicators · tree-indented
breakdown · per-section detail · hyper-granular maturity visualization.
"""

from __future__ import annotations
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, MofNCompleteColumn
from rich.live import Live
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from rich.padding import Padding
from rich.rule import Rule
from rich.box import HEAVY, ROUNDED, SIMPLE_HEAD, MINIMAL, SQUARE, DOUBLE

from .data import PILLARS, CLUSTERS, LEVEL_SHORT, LEVEL_NAMES, LEVEL_DESCRIPTIONS, pillars_by_cluster


# ─── Color palette · sophisticated · semantic ───────────────────────────────
GRADE_COLOR = {"A": "#10b981", "B": "#3b82f6", "C": "#f59e0b", "D": "#ef4444", "F": "#7c2d12"}
LEVEL_COLOR = {0: "#6b7280", 1: "#ef4444", 2: "#f59e0b", 3: "#3b82f6", 4: "#10b981"}
LEVEL_RICH = {0: "grey50", 1: "bright_red", 2: "yellow", 3: "bright_blue", 4: "bright_green"}
CLUSTER_COLOR = {"A": "#a855f7", "B": "#3b82f6", "C": "#f59e0b", "D": "#10b981"}
CLUSTER_RICH = {"A": "magenta", "B": "blue", "C": "yellow", "D": "green"}

# Block characters for visual indicators (slash context style)
BLOCK_FULL = "⛁"          # filled block (used)
BLOCK_EMPTY = "⛶"         # empty block (free)
BLOCK_PARTIAL = "⛀"       # partial block

# Maturity progression chars
MATURITY_FULL = "█"
MATURITY_EMPTY = "░"


def make_console(no_color: bool = False) -> Console:
    return Console(
        no_color=no_color,
        soft_wrap=False,
        force_terminal=True if not no_color else None,
        highlight=False,
        width=None,  # auto-detect width
    )


# ═══════════════════════════════════════════════════════════════════════════
# Banner
# ═══════════════════════════════════════════════════════════════════════════

def banner(version: str) -> Panel:
    body = Text()
    body.append("\n  ")
    body.append("WORKSPACE AGENTIC BENCHMARK", style="bold white")
    body.append(f"   v{version}\n", style="dim cyan")
    body.append("  First-principles framework", style="italic dim")
    body.append("  ·  ", style="grey30")
    body.append("12 pillars  ·  4 clusters  ·  L0-L4 maturity model", style="cyan")
    body.append("\n  ")
    body.append("github.com/ceomadani/workspace-agentic-benchmark", style="dim blue underline")
    return Panel(body, border_style="cyan", box=HEAVY, padding=(0, 1))


# ═══════════════════════════════════════════════════════════════════════════
# Workspace info card
# ═══════════════════════════════════════════════════════════════════════════

def workspace_card(workspace: Path, stats: dict, fmt_size_fn) -> Panel:
    body = Text()
    body.append("  ")
    body.append("PATH       ", style="dim")
    body.append(f"{workspace}\n", style="bold white")
    body.append("  ")
    body.append("FILES      ", style="dim")
    body.append(f"{stats['files']:,}", style="cyan")
    body.append("           ")
    body.append("SIZE   ", style="dim")
    body.append(f"{fmt_size_fn(stats['bytes'])}\n", style="cyan")
    body.append("  ")
    body.append("DIRS       ", style="dim")
    body.append(f"{stats['dirs']:,}", style="cyan")
    body.append("           ")
    body.append("START  ", style="dim")
    body.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), style="cyan")
    return Panel(body, title="[bold cyan]┃ WORKSPACE", title_align="left", border_style="dim", box=ROUNDED, padding=(0, 1))


# ═══════════════════════════════════════════════════════════════════════════
# Progress
# ═══════════════════════════════════════════════════════════════════════════

def make_progress() -> Progress:
    return Progress(
        SpinnerColumn(style="cyan", spinner_name="dots"),
        TextColumn("[progress.description]{task.description}", style="white"),
        BarColumn(bar_width=32, complete_style="cyan", finished_style="bright_green", pulse_style="cyan"),
        TextColumn("[cyan]{task.completed}[/cyan][dim]/[/dim][cyan]{task.total}[/cyan]"),
        TextColumn("[dim]·[/dim]"),
        TimeElapsedColumn(),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Composite score · big hero panel · slash-context style
# ═══════════════════════════════════════════════════════════════════════════

def composite_hero(score: dict, total_pillars: int = 12) -> Panel:
    composite = score.get("composite", 0)
    grade = score.get("grade", "F")
    grade_desc = score.get("grade_description", "")
    color = GRADE_COLOR.get(grade, "#888")
    pillars = score.get("pillars", {})

    # Visual block representation · slash-context inspired
    # 12 blocks · one per pillar · colored by maturity level
    blocks_line1 = Text()
    blocks_line2 = Text()
    for i, p_meta in enumerate(PILLARS):
        data = pillars.get(p_meta.key, {})
        level = data.get("level", 0)
        block_color = LEVEL_COLOR.get(level, "#444")
        if i < 6:
            blocks_line1.append(BLOCK_FULL + " ", style=block_color)
        else:
            blocks_line2.append(BLOCK_FULL + " ", style=block_color)

    body = Text()
    body.append("\n  ")
    body.append("Composite: ", style="dim")
    body.append(f"{composite:.2f}", style=f"bold {color}")
    body.append(" / 100  ", style="dim")
    body.append("·  Grade: ", style="dim")
    body.append(f"  {grade}  ", style=f"bold reverse {color}")
    body.append("\n\n  ")
    body.append_text(blocks_line1)
    body.append(f"  ", style="dim")
    body.append(f"{total_pillars} pillars · ", style="dim cyan")
    body.append("4 clusters · ", style="dim cyan")
    body.append("L0-L4 maturity\n", style="dim cyan")
    body.append("  ")
    body.append_text(blocks_line2)
    body.append("\n\n  ")
    body.append(grade_desc, style="italic dim")
    body.append("\n")

    return Panel(body, border_style=color, box=HEAVY, padding=(0, 1))


# ═══════════════════════════════════════════════════════════════════════════
# Slash-context-style breakdown · estimated usage by category
# ═══════════════════════════════════════════════════════════════════════════

def maturity_breakdown(score: dict) -> Panel:
    """Slash-context style breakdown: per-pillar tokens-like distribution."""
    pillars = score.get("pillars", {})
    composite = score.get("composite", 0)
    cluster_avgs = score.get("cluster_averages", {})

    body = Text()
    body.append("\n  ")
    body.append("Estimated maturity by pillar", style="italic dim")
    body.append("\n\n")

    for p_meta in PILLARS:
        data = pillars.get(p_meta.key, {})
        level = data.get("level", 0)
        score_val = data.get("score", 0)
        passed = data.get("criteria_passed", 0)
        total = data.get("criteria_total", 10)
        level_color = LEVEL_COLOR.get(level, "#444")
        level_rich = LEVEL_RICH.get(level, "grey50")
        cluster_color = CLUSTER_COLOR.get(p_meta.cluster_letter, "#888")
        cluster_rich = CLUSTER_RICH.get(p_meta.cluster_letter, "white")

        # Visual block
        body.append("  ")
        body.append(BLOCK_FULL, style=level_color)
        body.append(" ", style="dim")

        # Pillar label
        new_tag = " [bright_green]⭐[/bright_green]" if p_meta.is_new_v03 else ""
        body.append(f"P{p_meta.n:02d}", style="dim")
        body.append(" ")
        body.append(f"{p_meta.title:<38}", style="white")
        if p_meta.is_new_v03:
            body.append("⭐", style="bright_green")
            body.append("  ", style="dim")
        else:
            body.append("   ", style="dim")

        # Cluster
        body.append("[", style="dim")
        body.append(p_meta.cluster_letter, style=cluster_rich)
        body.append("]  ", style="dim")

        # Level
        body.append(LEVEL_SHORT[level], style=f"bold {level_rich}")
        body.append(" ", style="dim")

        # Maturity dots
        for i in range(4):
            char = "⬤" if i < level else "○"
            body.append(char + " ", style=level_rich if i < level else "grey30")

        # Score + criteria
        body.append(f"  {score_val:>3}", style=f"bold {level_rich}")
        body.append("/100  ", style="dim")
        body.append(f"{passed}/{total}", style="dim cyan")
        body.append(" criteria\n", style="dim")

    body.append("\n")
    return Panel(body, title="[bold cyan]┃ PILLAR MATURITY", title_align="left", border_style="dim", box=ROUNDED, padding=(0, 1))


# ═══════════════════════════════════════════════════════════════════════════
# Tree-indented cluster sections · /context style
# ═══════════════════════════════════════════════════════════════════════════

def clusters_tree(score: dict) -> Panel:
    pillars = score.get("pillars", {})
    cluster_avgs = score.get("cluster_averages", {})

    body = Text()
    body.append("\n  ")
    body.append("Cluster aggregates · per-pillar trees", style="italic dim")
    body.append("\n\n")

    for letter, name, desc in CLUSTERS:
        if letter not in cluster_avgs:
            continue
        avg = cluster_avgs[letter]["average"]
        cluster_color = CLUSTER_COLOR.get(letter, "#888")
        cluster_rich = CLUSTER_RICH.get(letter, "white")

        # Cluster header line
        body.append("  ")
        body.append("▸ ", style=cluster_rich)
        body.append(f"Cluster {letter} · {name}", style=f"bold {cluster_rich}")
        body.append("  ", style="dim")
        body.append("[dim]·[/dim] ".replace("[dim]", "").replace("[/dim]", ""), style="dim")
        body.append(f"{avg:.1f}", style=f"bold {cluster_rich}")
        body.append(" / 100\n", style="dim")

        # Bar
        body.append("    ", style="dim")
        bar_filled = int(avg / 100 * 30)
        body.append(MATURITY_FULL * bar_filled, style=cluster_rich)
        body.append(MATURITY_EMPTY * (30 - bar_filled), style="grey30")
        body.append(f"    {desc}\n", style="italic dim")
        body.append("\n")

        # Per-pillar in this cluster (tree style)
        cluster_pillars = pillars_by_cluster(letter)
        for i, p_meta in enumerate(cluster_pillars):
            data = pillars.get(p_meta.key, {})
            level = data.get("level", 0)
            score_val = data.get("score", 0)
            level_rich = LEVEL_RICH.get(level, "grey50")
            is_last = i == len(cluster_pillars) - 1

            body.append("    ")
            body.append("└─ " if is_last else "├─ ", style="grey30")
            body.append(f"P{p_meta.n:02d}", style="dim")
            body.append("  ", style="dim")
            body.append(f"{p_meta.title:<40}", style="white")
            body.append("  ", style="dim")
            body.append(LEVEL_SHORT[level], style=f"bold {level_rich}")
            body.append("  ", style="dim")
            # mini-bar
            for j in range(4):
                body.append("⬤" if j < level else "○", style=level_rich if j < level else "grey30")
            body.append(f"  {score_val:>3}", style=f"bold {level_rich}")
            body.append("/100\n", style="dim")
        body.append("\n")

    return Panel(body, title="[bold cyan]┃ CLUSTER BREAKDOWN", title_align="left", border_style="dim", box=ROUNDED, padding=(0, 1))


# ═══════════════════════════════════════════════════════════════════════════
# Scoring legend · L0-L4 explanation
# ═══════════════════════════════════════════════════════════════════════════

def scoring_legend() -> Panel:
    body = Text()
    body.append("\n")
    for i in range(5):
        rich_color = LEVEL_RICH[i]
        body.append("  ")
        # Visual dots
        for j in range(4):
            body.append("⬤" if j < i else "○", style=rich_color if j < i else "grey30")
        body.append("  ", style="dim")
        body.append(f"{LEVEL_SHORT[i]}", style=f"bold {rich_color}")
        body.append("  ", style="dim")
        # Score
        scores = {0: "  0", 1: " 20", 2: " 50", 3: " 75", 4: "100"}
        body.append(f"{scores[i]}", style=f"bold {rich_color}")
        body.append("  ", style="dim")
        # Name
        name_only = LEVEL_NAMES[i].split(" ", 1)[1] if " " in LEVEL_NAMES[i] else LEVEL_NAMES[i]
        body.append(f"{name_only:<13}", style=f"bold {rich_color}")
        body.append(" — ", style="grey30")
        body.append(LEVEL_DESCRIPTIONS[i], style="dim")
        body.append("\n")
    body.append("\n  ")
    body.append("Composite = Σ (level_score × weight)", style="italic dim")
    body.append(" · default equal weight 1/12", style="dim grey50")
    body.append("\n  ")
    body.append("Grades: ", style="dim")
    body.append("A", style="bold bright_green")
    body.append(" ≥85  ", style="dim")
    body.append("B", style="bold bright_blue")
    body.append(" ≥70  ", style="dim")
    body.append("C", style="bold yellow")
    body.append(" ≥50  ", style="dim")
    body.append("D", style="bold bright_red")
    body.append(" ≥30  ", style="dim")
    body.append("F", style="bold red")
    body.append(" <30", style="dim")
    body.append("\n")
    return Panel(body, title="[bold cyan]┃ L0-L4 LEGEND", title_align="left", border_style="dim", box=ROUNDED, padding=(0, 1))


# ═══════════════════════════════════════════════════════════════════════════
# Improvement priorities · ranked
# ═══════════════════════════════════════════════════════════════════════════

def improvement_priorities(score: dict, top_n: int = 5) -> Panel:
    pillars = score.get("pillars", {})
    ranked = sorted(
        ((k, v) for k, v in pillars.items() if v.get("level", 0) < 4),
        key=lambda kv: kv[1].get("level", 0),
    )

    if not ranked:
        body = Text()
        body.append("\n  ")
        body.append("✨ ", style="bright_green")
        body.append("All 12 pillars at L4 Optimizing.", style="bold bright_green")
        body.append("\n  ")
        body.append("Maintain cybernetic feedback loops · monitor for regression.", style="italic dim")
        body.append("\n")
        return Panel(body, title="[bold cyan]┃ PRIORITIES", title_align="left", border_style="bright_green", box=ROUNDED, padding=(0, 1))

    body = Text()
    body.append("\n  ")
    body.append("Ordered by gap to next maturity level · top wins for the next iteration", style="italic dim")
    body.append("\n\n")

    for i, (key, data) in enumerate(ranked[:top_n], 1):
        p_meta = next(p for p in PILLARS if p.key == key)
        level = data.get("level", 0)
        next_level = level + 1
        cluster_rich = CLUSTER_RICH.get(p_meta.cluster_letter, "white")
        level_rich = LEVEL_RICH.get(level, "grey50")
        next_level_rich = LEVEL_RICH.get(next_level, "bright_green")
        score_val = data.get("score", 0)
        next_score = {0: 20, 1: 50, 2: 75, 3: 100, 4: 100}.get(next_level, 100)
        gap = next_score - score_val

        body.append(f"  {i}.  ", style="bold cyan")
        body.append(f"P{p_meta.n:02d}  ", style="dim")
        body.append(p_meta.title, style="bold white")
        body.append("  [", style="dim")
        body.append(f"{p_meta.cluster_letter}", style=cluster_rich)
        body.append(" · ", style="dim")
        body.append(p_meta.cluster, style=cluster_rich)
        body.append("]\n", style="dim")

        body.append("       ", style="dim")
        body.append(LEVEL_SHORT[level], style=f"bold {level_rich}")
        body.append("  ", style="dim")
        # bars
        for j in range(4):
            body.append("⬤" if j < level else "○", style=level_rich if j < level else "grey30")
        body.append("  →  ", style="dim cyan")
        body.append(LEVEL_SHORT[next_level], style=f"bold {next_level_rich}")
        body.append("  ", style="dim")
        for j in range(4):
            body.append("⬤" if j < next_level else "○", style=next_level_rich if j < next_level else "grey30")
        body.append(f"   +{gap} pts on this pillar", style="dim cyan")
        body.append("\n       ")
        body.append(p_meta.principle, style="italic dim")
        body.append("\n\n")

    return Panel(body, title="[bold cyan]┃ TOP IMPROVEMENT PRIORITIES", title_align="left", border_style="cyan", box=ROUNDED, padding=(0, 1))


# ═══════════════════════════════════════════════════════════════════════════
# Output files panel
# ═══════════════════════════════════════════════════════════════════════════

def output_files_card(audit_path: Path, score_path: Path, report_path: Path) -> Panel:
    body = Text()
    body.append("\n  ")
    body.append("audit.json    ", style="dim")
    body.append(str(audit_path), style="cyan")
    body.append("\n  ")
    body.append("score.json    ", style="dim")
    body.append(str(score_path), style="cyan")
    body.append("\n  ")
    body.append("report.html   ", style="dim")
    body.append(str(report_path), style="cyan")
    body.append("\n\n  ")
    body.append("Open the report: ", style="dim")
    body.append(f"open {report_path}", style="bold yellow")
    body.append("\n")
    return Panel(body, title="[bold cyan]┃ OUTPUT FILES", title_align="left", border_style="dim", box=ROUNDED, padding=(0, 1))


# ═══════════════════════════════════════════════════════════════════════════
# Footer · completion
# ═══════════════════════════════════════════════════════════════════════════

def print_completion(console: Console, elapsed: float) -> None:
    msg = Text()
    msg.append("  ", style="dim")
    msg.append("✓", style="bold bright_green")
    msg.append("  Audit completed in ", style="dim")
    msg.append(f"{elapsed:.2f}s", style="bold green")
    console.print(msg)


def hard_rule(console: Console, char: str = "─") -> None:
    console.print(Rule(style="grey30"))


# ═══════════════════════════════════════════════════════════════════════════
# LEGACY · simpler views (for compactness if needed)
# ═══════════════════════════════════════════════════════════════════════════

def composite_card(score: dict) -> Panel:
    """Legacy compact composite. Use composite_hero() for full slash-context experience."""
    return composite_hero(score)


def cluster_table(score: dict) -> Table:
    cluster_avgs = score.get("cluster_averages", {})
    t = Table(title="[bold cyan]Cluster averages[/bold cyan]", box=SIMPLE_HEAD, show_header=True, header_style="bold cyan", border_style="dim")
    t.add_column("Cluster", style="white", min_width=22)
    t.add_column("Score", justify="right", style="bold")
    t.add_column("Distribution", min_width=24)
    for letter, name, desc in CLUSTERS:
        if letter in cluster_avgs:
            avg = cluster_avgs[letter]["average"]
            color = CLUSTER_RICH.get(letter, "white")
            filled = int(avg / 100 * 20)
            bar = MATURITY_FULL * filled + MATURITY_EMPTY * (20 - filled)
            t.add_row(
                f"[{color}]{letter}[/{color}] · {name}",
                f"[{color}]{avg:5.1f}[/{color}] [dim]/ 100[/dim]",
                f"[{color}]{bar}[/{color}]",
            )
    return t


def pillars_table(score: dict) -> Table:
    """Legacy compact pillar table. Use maturity_breakdown() for slash-context style."""
    pillars = score.get("pillars", {})
    t = Table(title="[bold cyan]Pillar maturity[/bold cyan]", box=SIMPLE_HEAD, show_header=True, header_style="bold cyan", border_style="dim")
    t.add_column("#", style="dim", width=4)
    t.add_column("Pillar", style="white", min_width=36)
    t.add_column("Cluster", justify="center", width=10)
    t.add_column("Level", min_width=24)
    t.add_column("Score", justify="right", min_width=10)
    t.add_column("Maturity", min_width=22)
    for p_meta in PILLARS:
        data = pillars.get(p_meta.key, {})
        level = data.get("level", 0)
        score_val = data.get("score", 0)
        cluster_color = CLUSTER_RICH.get(p_meta.cluster_letter, "white")
        level_color = LEVEL_RICH.get(level, "grey50")
        new_tag = " [bright_green]⭐[/bright_green]" if p_meta.is_new_v03 else ""
        warn = " ⚠" if level <= 2 else ""
        dots = "".join("⬤" if j < level else "○" for j in range(4))
        t.add_row(
            f"P{p_meta.n:02d}",
            p_meta.title + new_tag,
            f"[{cluster_color}]{p_meta.cluster_letter}[/{cluster_color}]",
            f"[{level_color}]{LEVEL_SHORT[level]}[/{level_color}] [dim]· {LEVEL_NAMES[level].split(' ', 1)[1]}[/dim]{warn}",
            f"[{level_color}]{score_val:>3}[/{level_color}] [dim]/100[/dim]",
            f"[{level_color}]{dots}[/{level_color}]",
        )
    return t
