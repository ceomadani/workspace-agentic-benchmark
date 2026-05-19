"""Click-based CLI · subcommands: audit · score · report · run."""

from __future__ import annotations
import json
import sys
import time
from pathlib import Path

import click
from rich.console import Console
from rich.live import Live

from . import __version__
from .audit import run_audit, workspace_stats, fmt_size, SCANNERS
from .score import load_weights, score_audit
from .ui import (
    banner,
    workspace_card,
    make_progress,
    composite_card,
    cluster_table,
    pillars_table,
    improvement_priorities,
    scoring_legend,
    output_files_card,
    print_completion,
    make_console,
)
from .html_report import render_html


@click.group(help="Workspace Agentic Benchmark · evaluate agentic workspace infrastructures · 12 pillars · 4 clusters · L0-L4 maturity.")
@click.version_option(__version__, prog_name="workspace-bench")
def cli():
    pass


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
        console.print(composite_card(score))
        console.print()
        console.print(cluster_table(score))
        console.print()
        console.print(pillars_table(score))
        console.print()
        console.print(improvement_priorities(score))
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
@click.option("--no-color", is_flag=True, help="Disable color output")
def cmd_report(score_json: Path, output: Path, no_color: bool):
    console = make_console(no_color=no_color)
    score = json.loads(score_json.read_text(encoding="utf-8"))
    html = render_html(score)
    output.write_text(html, encoding="utf-8")
    console.print(f"[bright_green]✓[/bright_green] Wrote HTML report to [cyan]{output}[/cyan]")
    console.print(f"[dim]Open the report:[/dim]  [yellow]open {output}[/yellow]")


@cli.command("run", help="Run full pipeline (audit + score + report) with live progress")
@click.argument("workspace", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.option("--output-dir", "-d", type=click.Path(path_type=Path), default=Path("."), help="Output directory (default: cwd)")
@click.option("--weights", type=click.Path(exists=True, dir_okay=False, path_type=Path), help="Path to weights.json")
@click.option("--no-color", is_flag=True, help="Disable color output")
def cmd_run(workspace: Path, output_dir: Path, weights: Path | None, no_color: bool):
    console = make_console(no_color=no_color)
    output_dir.mkdir(parents=True, exist_ok=True)

    audit_path = output_dir / "audit.json"
    score_path = output_dir / "score.json"
    report_path = output_dir / "report.html"

    # 1. Banner + workspace card
    console.print()
    console.print(banner(__version__))
    console.print()
    stats = workspace_stats(workspace)
    console.print(workspace_card(workspace, stats, fmt_size))
    console.print()

    # 2. Audit with progress
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
    console.print()

    # Persist audit
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")

    # 3. Score
    weight_dict = load_weights(weights)
    score = score_audit(audit, weight_dict)
    score_path.write_text(json.dumps(score, indent=2, ensure_ascii=False), encoding="utf-8")

    # 4. Display
    console.print(composite_card(score))
    console.print()
    console.print(cluster_table(score))
    console.print()
    console.print(pillars_table(score))
    console.print()
    console.print(improvement_priorities(score))
    console.print()
    console.print(scoring_legend())
    console.print()

    # 5. HTML report
    html = render_html(score)
    report_path.write_text(html, encoding="utf-8")

    # 6. Output files panel
    console.print(output_files_card(audit_path, score_path, report_path))
    console.print()


def main():
    cli(prog_name="workspace-bench")


if __name__ == "__main__":
    main()
