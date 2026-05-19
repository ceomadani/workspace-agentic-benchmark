#!/usr/bin/env python3
"""
Backwards-compatible shim · forwards to `python -m workspace_bench audit`.

For the full sophisticated CLI experience (progress bars, rich output, beautiful tables):
    pip install -e .
    workspace-bench audit /path/to/workspace
"""

from __future__ import annotations
import sys
from pathlib import Path

# Add repo root to path so `import workspace_bench` works without install
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from workspace_bench.cli import cmd_audit


if __name__ == "__main__":
    cmd_audit(prog_name="audit.py")
