#!/usr/bin/env python3
"""
Backwards-compatible shim · forwards to `python -m workspace_bench report`.

For the full sophisticated CLI experience:
    pip install -e .
    workspace-bench report score.json --output report.html
"""

from __future__ import annotations
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from workspace_bench.cli import cmd_report


if __name__ == "__main__":
    cmd_report(prog_name="report.py")
