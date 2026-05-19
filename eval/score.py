#!/usr/bin/env python3
"""
Backwards-compatible shim · forwards to `python -m workspace_bench score`.

For the full sophisticated CLI experience:
    pip install -e .
    workspace-bench score audit.json
"""

from __future__ import annotations
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from workspace_bench.cli import cmd_score


if __name__ == "__main__":
    # Default to --quiet for backwards-compat (legacy emits raw JSON to stdout)
    if "--quiet" not in sys.argv and "-q" not in sys.argv:
        sys.argv.append("--quiet")
    cmd_score(prog_name="score.py")
