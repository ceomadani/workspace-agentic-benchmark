"""Pytest fixtures for workspace-bench tests."""

import json
import shutil
from pathlib import Path

import pytest


@pytest.fixture
def empty_workspace(tmp_path: Path) -> Path:
    """A bare-minimum workspace · should score L0/L1 on most pillars."""
    ws = tmp_path / "empty-ws"
    ws.mkdir()
    (ws / "README.md").write_text("# Empty workspace\n\nNothing structured here.")
    return ws


@pytest.fixture
def structured_workspace(tmp_path: Path) -> Path:
    """A more structured workspace · should score L2-L3 on multiple pillars."""
    ws = tmp_path / "structured-ws"
    ws.mkdir()

    # Memory tiers
    (ws / "memory").mkdir()
    (ws / "memory" / "semantic").mkdir()
    (ws / "memory" / "episodic").mkdir()
    (ws / "memory" / "procedural").mkdir()
    (ws / "memory" / "MEMORY.md").write_text("# Memory index\n\nSee tiers.")

    # Skills
    (ws / "skills").mkdir()
    skill_dir = ws / "skills" / "example-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\nname: example-skill\ndescription: example\ntriggers: example\n---\n# Example"
    )

    # Constitution
    (ws / "CONSTITUTION.md").write_text(
        "# Constitution\n\n## HARD RULE 1\nNo plaintext credentials.\n\n## HARD RULE 2\nApproval required for external actions.\n"
    )

    # Rules dir
    (ws / "rules").mkdir()
    (ws / "rules" / "multi-agent-policy.md").write_text(
        "# Multi-agent policy\n\nSingle-thread default. Multi-agent requires evidence. "
        "Reference: arxiv 2604.02460 (DPI). Anti-pattern: ❌ recursive sub-agents."
    )

    # Vault integration
    (ws / ".gitignore").write_text(".env\n.env.*\n")
    (ws / ".envrc.template").write_text(
        'export API_KEY="$(op read \'op://Vault/Service/api_key\')"\n'
    )

    # Logs
    (ws / "_logs").mkdir()

    return ws


@pytest.fixture
def example_audit(tmp_path: Path, structured_workspace: Path) -> dict:
    """Run audit on structured_workspace · return parsed dict."""
    from workspace_bench.audit import run_audit
    return run_audit(structured_workspace)
