"""Click-based CLI · subcommands: init · audit · score · report · run."""

from __future__ import annotations
import json
import os
import sys
import time
from pathlib import Path

import click
from rich.console import Console

from . import __version__
from .audit import run_audit, workspace_stats, fmt_size, SCANNERS
from .score import load_weights, score_audit
from .ui import (
    banner,
    workspace_card,
    make_progress,
    composite_hero,
    maturity_breakdown,
    clusters_tree,
    scoring_legend,
    improvement_priorities,
    output_files_card,
    print_completion,
    make_console,
)
from .html_report import render_html
from .i18n import detect_language, language_name
from .info_theory import compute_info_theory
from .info_theory_advanced import compute_advanced_metrics
from .compare import compare_scores, save_to_history, load_history, composite_trend, sparkline
from .onboarding import run_init as run_init_wizard, read_config, CONFIG_FILENAME


@click.group(help="Workspace Agentic Benchmark · evaluate agentic workspace infrastructures · 12 pillars · 4 clusters · L0-L4 maturity.")
@click.version_option(__version__, prog_name="workspace-bench")
def cli():
    pass


@cli.command("init", help="Interactive onboarding wizard · saves config to .workspace-bench.yaml")
@click.option("--force", is_flag=True, help="Overwrite existing config")
@click.option("--no-color", is_flag=True, help="Disable color output")
def cmd_init(force: bool, no_color: bool):
    console = make_console(no_color=no_color)
    run_init_wizard(console, __version__, force=force)


@cli.command("audit", help="Run audit on a workspace · emit audit.json")
@click.argument("workspace", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output JSON path (default: stdout)")
@click.option("--no-color", is_flag=True, help="Disable color output")
@click.option("--quiet", "-q", is_flag=True, help="Suppress progress output")
def cmd_audit(workspace: Path, output: Path | None, no_color: bool, quiet: bool):
    console = make_console(no_color=no_color)
    if not quiet:
        console.print()
        console.print(banner(__version__))
        console.print()
        stats = workspace_stats(workspace)
        console.print(workspace_card(workspace, stats, fmt_size))
        console.print()

    progress = None
    task_id = None
    if not quiet:
        progress = make_progress()
        progress.start()
        task_id = progress.add_task("[white]Scanning pillars", total=len(SCANNERS))

    def on_progress(key: str, idx: int, total: int):
        if progress and task_id is not None:
            if key != "done":
                progress.update(task_id, description=f"[white]Scanning [cyan]{key.split('_', 1)[1]}", completed=idx)
            else:
                progress.update(task_id, completed=total, description="[bright_green]Audit complete")

    start = time.time()
    audit = run_audit(workspace, on_progress=on_progress)
    elapsed = time.time() - start

    if progress:
        progress.stop()
        print_completion(console, elapsed)

    output_json = json.dumps(audit, indent=2, ensure_ascii=False)
    if output:
        output.write_text(output_json, encoding="utf-8")
        if not quiet:
            console.print(f"[dim]Wrote audit to[/dim] [cyan]{output}[/cyan]")
    else:
        print(output_json)


@cli.command("score", help="Score an audit.json against the 12-pillar L0-L4 rubric")
@click.argument("audit_json", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output JSON path (default: stdout)")
@click.option("--weights", type=click.Path(exists=True, dir_okay=False, path_type=Path), help="Path to weights.json")
@click.option("--no-color", is_flag=True, help="Disable color output")
@click.option("--quiet", "-q", is_flag=True, help="Suppress display output")
def cmd_score(audit_json: Path, output: Path | None, weights: Path | None, no_color: bool, quiet: bool):
    console = make_console(no_color=no_color)
    audit = json.loads(audit_json.read_text(encoding="utf-8"))
    weight_dict = load_weights(weights)
    score = score_audit(audit, weight_dict)

    if not quiet:
        console.print()
        console.print(composite_hero(score))
        console.print()
        console.print(maturity_breakdown(score))
        console.print()
        console.print(clusters_tree(score))
        console.print()
        console.print(improvement_priorities(score))
        console.print()
        console.print(scoring_legend())
        console.print()

    output_json = json.dumps(score, indent=2, ensure_ascii=False)
    if output:
        output.write_text(output_json, encoding="utf-8")
        if not quiet:
            console.print(f"[dim]Wrote score to[/dim] [cyan]{output}[/cyan]")
    else:
        if quiet:
            print(output_json)


@cli.command("report", help="Generate HTML report from a score.json")
@click.argument("score_json", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--output", "-o", type=click.Path(path_type=Path), required=True, help="Output HTML path")
@click.option("--language", type=click.Choice(["en", "it", "fr", "es", "de", "pt"]), default=None, help="Report language (default: auto-detect from workspace)")
@click.option("--workspace-name", default="", help="Display name for the workspace in report")
@click.option("--include-info-theory", is_flag=True, default=True, help="Include information theory metrics (default: on)")
@click.option("--no-color", is_flag=True, help="Disable color output")
def cmd_report(score_json: Path, output: Path, language: str | None, workspace_name: str, include_info_theory: bool, no_color: bool):
    console = make_console(no_color=no_color)
    score = json.loads(score_json.read_text(encoding="utf-8"))

    # Auto-detect language from workspace if not specified
    workspace_path_str = score.get("workspace")
    detected_lang = "en"
    info = None
    if workspace_path_str:
        wp = Path(workspace_path_str)
        if wp.exists():
            if language is None:
                detected_lang, _ = detect_language(wp)
            if include_info_theory:
                console.print("[dim]  Computing information theory metrics...[/dim]")
                info = compute_info_theory(wp)

    lang = language or detected_lang
    html = render_html(score, info_theory=info, language=lang, workspace_name=workspace_name)
    output.write_text(html, encoding="utf-8")
    console.print(f"[bright_green]✓[/bright_green] Wrote HTML report to [cyan]{output}[/cyan]")
    console.print(f"[dim]  Language: [/dim][cyan]{language_name(lang)}[/cyan] ({lang})")
    console.print(f"[dim]  Open the report:[/dim]  [yellow]open {output}[/yellow]")


@cli.command("run", help="Run full pipeline (audit + score + report) with live progress · uses .workspace-bench.yaml if present")
@click.argument("workspace", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path), required=False)
@click.option("--output-dir", "-d", type=click.Path(path_type=Path), default=None, help="Output directory (default: from config or ./bench-output)")
@click.option("--language", type=click.Choice(["en", "it", "fr", "es", "de", "pt"]), default=None, help="Report language (default: auto-detect)")
@click.option("--workspace-name", default="", help="Display name in HTML report")
@click.option("--weights", type=click.Path(exists=True, dir_okay=False, path_type=Path), help="Path to weights.json")
@click.option("--no-color", is_flag=True, help="Disable color output")
def cmd_run(workspace: Path | None, output_dir: Path | None, language: str | None, workspace_name: str, weights: Path | None, no_color: bool):
    console = make_console(no_color=no_color)

    # Load config if present (cwd/.workspace-bench.yaml)
    config_path = Path.cwd() / CONFIG_FILENAME
    config = read_config(config_path) if config_path.exists() else {}

    # Resolve workspace: CLI arg > config > error
    if workspace is None:
        wp_from_config = config.get("workspace")
        if isinstance(wp_from_config, list):
            wp_from_config = wp_from_config[0]
        if wp_from_config:
            workspace = Path(str(wp_from_config))
            console.print(f"[dim]  Using workspace from config:[/dim] [cyan]{workspace}[/cyan]")
        else:
            console.print("[red]✗ No workspace specified.[/red] Provide a path or run [yellow]workspace-bench init[/yellow] first.")
            sys.exit(1)

    if not workspace.exists() or not workspace.is_dir():
        console.print(f"[red]✗ Workspace not found:[/red] {workspace}")
        sys.exit(1)

    # Resolve output_dir
    if output_dir is None:
        output_dir = Path(str(config.get("output_dir", "./bench-output")))
    output_dir.mkdir(parents=True, exist_ok=True)

    # Resolve language
    if language is None:
        language = config.get("language")

    # Resolve workspace_name
    if not workspace_name:
        workspace_name = str(config.get("workspace_name", ""))

    audit_path = output_dir / "audit.json"
    score_path = output_dir / "score.json"
    report_path = output_dir / "report.html"

    # 1. Banner
    console.print()
    console.print(banner(__version__))
    console.print()
    stats = workspace_stats(workspace)
    console.print(workspace_card(workspace, stats, fmt_size))
    console.print()

    # 2. Audit
    progress = make_progress()
    progress.start()
    task_id = progress.add_task("[white]Scanning pillars", total=len(SCANNERS))

    def on_progress(key: str, idx: int, total: int):
        if key != "done":
            label = key.split("_", 1)[1].replace("_", " ").title()
            progress.update(task_id, description=f"[white]Scanning [cyan]{label}", completed=idx)
        else:
            progress.update(task_id, completed=total, description="[bright_green]Audit complete")

    start = time.time()
    audit = run_audit(workspace, on_progress=on_progress)
    elapsed = time.time() - start
    progress.stop()
    print_completion(console, elapsed)

    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")

    # 3. Score
    weight_dict = load_weights(weights)
    score = score_audit(audit, weight_dict)
    score_path.write_text(json.dumps(score, indent=2, ensure_ascii=False), encoding="utf-8")

    # 4. Info theory (base + advanced) + language detection
    console.print()
    console.print("[dim]  Computing information theory metrics...[/dim]")
    info = compute_info_theory(workspace)
    console.print("[dim]  Computing knowledge graph + advanced metrics...[/dim]")
    advanced = compute_advanced_metrics(workspace)
    info["advanced"] = advanced
    if language is None:
        language, _ = detect_language(workspace)
    console.print(f"[dim]  Language detected:[/dim] [cyan]{language_name(language)}[/cyan] ({language})")
    console.print(f"[dim]  α (quantity × quality):[/dim] [magenta]{info['alpha']}[/magenta]  ·  SNR: [blue]{info['snr_db']} dB[/blue]")
    console.print()

    # 5. Display
    console.print(composite_hero(score))
    console.print()
    console.print(maturity_breakdown(score))
    console.print()
    console.print(clusters_tree(score))
    console.print()
    console.print(improvement_priorities(score))
    console.print()
    console.print(scoring_legend())
    console.print()

    # 6. HTML report
    html = render_html(score, info_theory=info, language=language, workspace_name=workspace_name)
    report_path.write_text(html, encoding="utf-8")

    # 7. Save to history (.workspace-bench/history/)
    history_dir = workspace / ".workspace-bench" / "history"
    try:
        save_to_history(audit, score, history_dir)
        console.print(f"[dim]  Snapshot saved to history:[/dim] [cyan]{history_dir}[/cyan]")
    except Exception as e:
        console.print(f"[yellow]  ! Could not save history snapshot: {e}[/yellow]")
    console.print()

    # 8. Output files panel
    console.print(output_files_card(audit_path, score_path, report_path))
    console.print()


@cli.command("compare", help="Compare two audits · trend diff · what improved/regressed between two scores")
@click.argument("before_score_json", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("after_score_json", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output JSON path (default: stdout)")
@click.option("--no-color", is_flag=True, help="Disable color output")
def cmd_compare(before_score_json: Path, after_score_json: Path, output: Path | None, no_color: bool):
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.box import HEAVY, ROUNDED, SIMPLE_HEAD
    console = make_console(no_color=no_color)
    before = json.loads(before_score_json.read_text(encoding="utf-8"))
    after = json.loads(after_score_json.read_text(encoding="utf-8"))
    diff = compare_scores(before, after)

    composite_delta = diff.get("composite_delta", 0)
    arrow = "↑" if composite_delta > 0 else ("↓" if composite_delta < 0 else "→")
    color = "bright_green" if composite_delta > 0 else ("bright_red" if composite_delta < 0 else "yellow")

    hero = Text()
    hero.append("\n  Composite trend  ", style="dim")
    hero.append(f"{diff['before']['composite']:.2f}", style="cyan")
    hero.append(" → ", style="dim")
    hero.append(f"{diff['after']['composite']:.2f}", style=f"bold {color}")
    hero.append(f"  {arrow}{abs(composite_delta):+.2f}", style=f"bold {color}")
    hero.append("\n  Grade            ", style="dim")
    hero.append(diff["grade_change"], style="bold")
    hero.append("\n\n  Pillar movements  ", style="dim")
    hero.append(f"+{diff['improvements_count']}", style="bright_green")
    hero.append("  /  ", style="dim")
    hero.append(f"-{diff['regressions_count']}", style="bright_red")
    hero.append("  /  ", style="dim")
    hero.append(f"={diff['flat_count']}", style="dim")
    hero.append("\n")
    console.print()
    console.print(Panel(hero, title="[bold cyan]┃ COMPARE", title_align="left", border_style=color, box=HEAVY, padding=(0, 1)))
    console.print()

    # Per-pillar table
    t = Table(title="[bold]Pillar diffs[/bold]", box=SIMPLE_HEAD, show_header=True, header_style="bold cyan", border_style="dim")
    t.add_column("#", style="dim", width=4)
    t.add_column("Pillar", style="white", min_width=36)
    t.add_column("Before", justify="right")
    t.add_column("After", justify="right")
    t.add_column("Δ", justify="right")
    for d in diff["pillar_diffs"]:
        delta = d["score_delta"]
        if delta > 0:
            sym = f"[bright_green]+{delta}[/bright_green]"
        elif delta < 0:
            sym = f"[bright_red]{delta}[/bright_red]"
        else:
            sym = "[dim]·[/dim]"
        t.add_row(
            f"P{d['n']:02d}",
            d["title"],
            f"[dim]{d['before_score']}[/dim]",
            f"[bold]{d['after_score']}[/bold]",
            sym,
        )
    console.print(t)
    console.print()

    if output:
        output.write_text(json.dumps(diff, indent=2, ensure_ascii=False), encoding="utf-8")
        console.print(f"[dim]Wrote diff to[/dim] [cyan]{output}[/cyan]")


@cli.command("history", help="Show audit history trend · composite over time · sparkline")
@click.argument("workspace", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path), required=False)
@click.option("--no-color", is_flag=True, help="Disable color output")
def cmd_history(workspace: Path | None, no_color: bool):
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.box import HEAVY, ROUNDED, SIMPLE_HEAD
    console = make_console(no_color=no_color)

    if workspace is None:
        # Try to read from config
        config_path = Path.cwd() / CONFIG_FILENAME
        config = read_config(config_path) if config_path.exists() else {}
        wp = config.get("workspace")
        if isinstance(wp, list):
            wp = wp[0]
        if wp:
            workspace = Path(str(wp))
        else:
            console.print("[red]✗ No workspace specified. Provide path or run init.[/red]")
            sys.exit(1)

    history_dir = workspace / ".workspace-bench" / "history"
    history = load_history(history_dir)

    if not history:
        console.print(f"[yellow]  No history found at {history_dir}.  Run `workspace-bench run` first.[/yellow]")
        return

    trend = composite_trend(history)
    composites = [p[1] for p in trend["points"]]
    spark = sparkline(composites, width=40)

    body = Text()
    body.append("\n  Workspace  ", style="dim")
    body.append(str(workspace), style="cyan")
    body.append(f"\n  Samples    ", style="dim")
    body.append(f"{trend['samples']}", style="cyan")
    body.append("\n  First      ", style="dim")
    body.append(f"{trend['first']}", style="cyan")
    body.append("\n  Current    ", style="dim")
    body.append(f"{trend['current']}", style="bright_cyan")
    body.append("\n  Min / Max  ", style="dim")
    body.append(f"{trend['min']} / {trend['max']}", style="cyan")
    body.append("\n  Delta      ", style="dim")
    delta = trend["delta_from_first"]
    color = "bright_green" if delta > 0 else ("bright_red" if delta < 0 else "dim")
    sign = "+" if delta > 0 else ""
    body.append(f"{sign}{delta}", style=f"bold {color}")
    body.append("\n\n  Trend      ", style="dim")
    body.append(spark, style="cyan")
    body.append("\n")
    console.print()
    console.print(Panel(body, title="[bold cyan]┃ HISTORY", title_align="left", border_style="cyan", box=HEAVY, padding=(0, 1)))
    console.print()

    # Table of snapshots
    t = Table(title="[bold]Snapshots[/bold]", box=SIMPLE_HEAD, show_header=True, header_style="bold cyan", border_style="dim")
    t.add_column("Timestamp", style="white")
    t.add_column("Composite", justify="right")
    t.add_column("Grade", justify="center")
    t.add_column("Cluster A", justify="right")
    t.add_column("Cluster B", justify="right")
    t.add_column("Cluster C", justify="right")
    t.add_column("Cluster D", justify="right")
    for entry in history[-10:]:
        ts = entry.get("timestamp", "?")[:19].replace("T", " ")
        ca = entry.get("cluster_averages", {})
        t.add_row(
            ts,
            f"[bold]{entry.get('composite', 0):.1f}[/bold]",
            entry.get("grade", "?"),
            f"{ca.get('A', 0):.0f}",
            f"{ca.get('B', 0):.0f}",
            f"{ca.get('C', 0):.0f}",
            f"{ca.get('D', 0):.0f}",
        )
    console.print(t)
    console.print()


def main():
    cli(prog_name="workspace-bench")


if __name__ == "__main__":
    main()
