#!/usr/bin/env python3
"""
================================================================================
audit.py · Workspace Agentic Benchmark · deterministic scanner
================================================================================

LEGGENDA 4W:
  COSA  · Scan a workspace directory for signals across 8 pillars.
          Pure deterministic file-tree + grep scanner · NO LLM calls.
  COME  · Walk file tree · pattern match · count occurrences · output structured JSON.
  DOVE  · Input: workspace path (positional arg). Output: JSON to stdout.
  QUANDO · CLI usage: python3 audit.py /path/to/workspace > audit.json

USAGE:
  python3 audit.py /Users/me/my-workspace > audit.json
  python3 audit.py . --verbose > audit.json

ARCHITECTURE:
  Each pillar has a `scan_pillar_N()` function returning a dict of raw signals.
  The combined output is then consumed by score.py to produce 0-10 per pillar.

This script is intentionally heuristic · production usage should validate
qualitatively · scoring rubric is in METHODOLOGY.md.

================================================================================
"""

from __future__ import annotations
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SECRET_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9_-]{20,}"),
    re.compile(r"sk-ant-[a-zA-Z0-9_-]{50,}"),
    re.compile(r"ghp_[a-zA-Z0-9]{36}"),
    re.compile(r"gho_[a-zA-Z0-9]{36}"),
    re.compile(r"github_pat_[a-zA-Z0-9_]{82}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"Bearer\s+[a-zA-Z0-9_\-\.=]{30,}"),
    re.compile(r"['\"]?api[_-]?key['\"]?\s*[:=]\s*['\"][a-zA-Z0-9_-]{20,}['\"]", re.IGNORECASE),
    re.compile(r"xoxb-[a-zA-Z0-9-]{50,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{35}"),
]

SCAN_EXTENSIONS = {".md", ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".json", ".yml", ".yaml", ".toml", ".env", ".txt", ".plist"}

IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".next", "dist", "build", ".pytest_cache", ".mypy_cache"}


def safe_read(path: Path, max_bytes: int = 200_000) -> str:
    """Read a file, returning empty string on error or if too large."""
    try:
        if path.stat().st_size > max_bytes:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except (OSError, UnicodeDecodeError):
        return ""


def walk_files(root: Path, extensions: set[str] | None = None):
    """Walk filesystem, yielding files. Skip IGNORE_DIRS and binary files."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".") or d in {".claude", ".github"}]
        for fname in filenames:
            p = Path(dirpath) / fname
            if extensions and p.suffix not in extensions:
                continue
            yield p


def find_files_by_pattern(root: Path, pattern: str) -> list[Path]:
    """Find files matching a name pattern (glob-like)."""
    return list(root.rglob(pattern))


# ==============================================================================
# Pillar 1 · Context Hierarchy & Memory
# ==============================================================================

def scan_pillar_1_memory(root: Path) -> dict:
    signals: dict[str, Any] = {
        "tier_dirs_found": [],
        "memory_index_files": [],
        "structured_entries_count": 0,
        "cross_link_pattern_count": 0,
        "retrieval_policy_doc": False,
        "decay_policy_doc": False,
        "mcp_query_layer": False,
        "kv_cache_awareness": False,
    }

    tier_candidates = ["semantic", "episodic", "procedural", "personalized", "personalised", "env-dynamics", "environment-dynamics", "memory"]

    for dirpath, dirnames, _ in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for d in dirnames:
            low = d.lower()
            for tier in tier_candidates:
                if tier in low and tier not in [t["tier"] for t in signals["tier_dirs_found"]]:
                    signals["tier_dirs_found"].append({"tier": tier, "path": str(Path(dirpath) / d)})
                    break

    for fname in ["MEMORY.md", "memory.md", "MEMORY-INDEX.md", "memory_index.md"]:
        files = find_files_by_pattern(root, fname)
        for f in files:
            signals["memory_index_files"].append(str(f))

    # Look at common memory file patterns
    for memfile in find_files_by_pattern(root, "*.md"):
        content = safe_read(memfile)
        if not content:
            continue
        if "[[" in content and "]]" in content:
            signals["cross_link_pattern_count"] += content.count("[[")
        if "name:" in content[:500] and "description:" in content[:500] and "metadata:" in content[:500]:
            signals["structured_entries_count"] += 1
        low = content.lower()
        if "retrieval policy" in low or "memory retrieval" in low:
            signals["retrieval_policy_doc"] = True
        if "decay policy" in low or "staleness" in low or "forgetting policy" in low:
            signals["decay_policy_doc"] = True
        if "brain mcp" in low or "memory mcp" in low or "memory server" in low:
            signals["mcp_query_layer"] = True
        if "kv-cache" in low or "kv cache" in low or "cache prefix" in low:
            signals["kv_cache_awareness"] = True

    return signals


# ==============================================================================
# Pillar 2 · Skill / Tool Architecture
# ==============================================================================

def scan_pillar_2_skills(root: Path) -> dict:
    signals: dict[str, Any] = {
        "skill_folders": [],
        "skills_with_frontmatter": 0,
        "skill_index_files": [],
        "auto_trigger_mechanism": False,
        "staleness_detector_found": False,
        "deterministic_tools_count": 0,
        "llm_tools_count": 0,
        "skill_roster_doc": False,
        "skill_changelog": 0,
    }

    skill_dirs = []
    for dirpath, dirnames, _ in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for d in dirnames:
            low = d.lower()
            if low in ("skills", "10_skills", "skill", ".claude/skills"):
                skill_dirs.append(Path(dirpath) / d)

    for sd in skill_dirs:
        for skill_md in sd.rglob("SKILL.md"):
            signals["skill_folders"].append(str(skill_md.parent))
            content = safe_read(skill_md)
            if content.startswith("---") and "name:" in content[:200] and "description:" in content[:500]:
                signals["skills_with_frontmatter"] += 1
            if "trigger" in content.lower()[:1000]:
                signals["auto_trigger_mechanism"] = True

    # Look for staleness detection tools
    for f in find_files_by_pattern(root, "*staleness*.py") + find_files_by_pattern(root, "*hermes*.py"):
        signals["staleness_detector_found"] = True
        break

    # Tools folder · try common naming conventions
    for tools_dir_name in ("tools", "scripts", "lib", "src/tools", "src/scripts"):
        for tools_dir in [d for d in root.rglob(tools_dir_name) if d.is_dir() and not any(part in IGNORE_DIRS for part in d.parts)]:
            for tool_file in tools_dir.rglob("*.py"):
                content = safe_read(tool_file)
                if "anthropic" in content.lower() or "openai" in content.lower() or "claude_cli_invoke" in content or "claude -p" in content:
                    signals["llm_tools_count"] += 1
                else:
                    signals["deterministic_tools_count"] += 1
            for tool_file in tools_dir.rglob("*.sh"):
                signals["deterministic_tools_count"] += 1

    for fname in ("ROSTER.md", "INDEX.md"):
        for f in find_files_by_pattern(root, fname):
            content = safe_read(f).lower()
            if "skill" in content[:500] or "active" in content[:1000] or "deprecated" in content[:1000]:
                signals["skill_roster_doc"] = True
                break

    for f in find_files_by_pattern(root, "CHANGELOG*.md"):
        signals["skill_changelog"] += 1

    return signals


# ==============================================================================
# Pillar 3 · Governance & Compliance
# ==============================================================================

def scan_pillar_3_governance(root: Path) -> dict:
    signals: dict[str, Any] = {
        "constitution_found": [],
        "hard_rules_count": 0,
        "pre_output_check": False,
        "compliance_judge": False,
        "rules_dir_found": False,
        "external_action_gate": False,
        "destructive_action_gate": False,
        "rules_versioning": False,
        "evidence_linked_rules": 0,
    }

    constitution_candidates = ["CONSTITUTION.md", "CLAUDE.md", "AGENT.md", "PRINCIPLES.md", "RULES.md", "constitution.md"]
    for fname in constitution_candidates:
        for f in find_files_by_pattern(root, fname):
            signals["constitution_found"].append(str(f))
            content = safe_read(f)
            if not content:
                continue
            # Count HARD RULES (numbered patterns, "HARD RULE", "HR" prefixes)
            hr_matches = re.findall(r"(?:HARD RULE|HR\s*#?\s*\d+|HR\d+|^\d+\.\s+[A-Z])", content, re.MULTILINE)
            signals["hard_rules_count"] = max(signals["hard_rules_count"], len(hr_matches))
            low = content.lower()
            if "pre-output" in low or "pre_output" in low or "compliance check" in low:
                signals["pre_output_check"] = True
            if "compliance judge" in low or "compliance-judge" in low:
                signals["compliance_judge"] = True
            if any(kw in low for kw in ["approval", "non mandare", "no external", "without approval", "approvazione esplicita"]):
                signals["external_action_gate"] = True
            if any(kw in low for kw in ["destructive", "rm -rf", "force-push", "drop table", "irreversible"]):
                signals["destructive_action_gate"] = True
            if re.search(r"v\d+\.\d+|version:\s*\d|iter-\d+", content):
                signals["rules_versioning"] = True
            # Evidence-linked rules: count rules with explicit incident/paper reference
            signals["evidence_linked_rules"] += len(re.findall(r"(?:incident|arxiv|origine:|backing:|reason:|why:)", low))

    # Rules directory · try common naming conventions
    for d in [".claude/rules", "rules", "policies", ".agent/rules", "agent/rules"]:
        if (root / d).exists() and (root / d).is_dir():
            signals["rules_dir_found"] = True
            break
    # Also check nested .claude/rules
    for p in root.rglob(".claude/rules"):
        if p.is_dir():
            signals["rules_dir_found"] = True
            break

    return signals


# ==============================================================================
# Pillar 4 · Auto-Improvement Loop
# ==============================================================================

def scan_pillar_4_auto_improvement(root: Path) -> dict:
    signals: dict[str, Any] = {
        "dreams_pipeline": False,
        "reflexion_runner": False,
        "session_capture_evidence": False,
        "scoring_rubric_for_proposals": False,
        "two_stage_review": False,
        "apply_log_exists": False,
        "cron_for_improvement": False,
        "cheaper_model_used": False,
    }

    for f in find_files_by_pattern(root, "*dreams*.py") + find_files_by_pattern(root, "*dreams*.md"):
        signals["dreams_pipeline"] = True
        break

    for f in find_files_by_pattern(root, "*reflexion*.py") + find_files_by_pattern(root, "*reflexion*.md"):
        signals["reflexion_runner"] = True
        break

    for f in find_files_by_pattern(root, "*.plist"):
        content = safe_read(f).lower()
        if "dreams" in content or "reflexion" in content or "self-improve" in content or "hermes" in content:
            signals["cron_for_improvement"] = True
        if "sonnet" in content or "haiku" in content:
            signals["cheaper_model_used"] = True

    # Cronologia or session preservation evidence
    for d_name in ("cronologia", "session-log", "sessions", "history"):
        if any(root.rglob(d_name)):
            signals["session_capture_evidence"] = True
            break

    for f in find_files_by_pattern(root, "*A-MAC*") + find_files_by_pattern(root, "*a_mac*") + find_files_by_pattern(root, "*scoring*"):
        if f.is_file():
            content = safe_read(f).lower()
            if "factor" in content or "rubric" in content or "criteria" in content:
                signals["scoring_rubric_for_proposals"] = True
                break

    for f in find_files_by_pattern(root, "*review*.md") + find_files_by_pattern(root, "*propose*.md"):
        content = safe_read(f).lower()
        if "two-stage" in content or "two stage" in content or "approve" in content and "apply" in content:
            signals["two_stage_review"] = True
            break

    # Apply log
    for f in find_files_by_pattern(root, "APPLY*.md") + find_files_by_pattern(root, "applied*.md") + find_files_by_pattern(root, "CHANGELOG*.md"):
        signals["apply_log_exists"] = True
        break

    return signals


# ==============================================================================
# Pillar 5 · Multi-Agent Discipline (DPI)
# ==============================================================================

def scan_pillar_5_multi_agent(root: Path) -> dict:
    signals: dict[str, Any] = {
        "multi_agent_policy_doc": False,
        "single_thread_default": False,
        "explore_only_preauthorized": False,
        "pre_spawn_checklist": False,
        "anti_pattern_doc_count": 0,
        "evidence_cited_dpi": False,
        "no_recursive_subagents_rule": False,
    }

    for fname in ["multi-agent-policy.md", "MULTI-AGENT.md", "agents-policy.md"]:
        for f in find_files_by_pattern(root, fname):
            signals["multi_agent_policy_doc"] = True
            content = safe_read(f).lower()
            if "single-thread" in content or "single thread" in content or "default 1 agent" in content:
                signals["single_thread_default"] = True
            if "explore-only" in content or "explore only" in content or "explore preauth" in content:
                signals["explore_only_preauthorized"] = True
            if "pre-spawn" in content or "checklist" in content:
                signals["pre_spawn_checklist"] = True
            if "anti-pattern" in content or "antipattern" in content:
                signals["anti_pattern_doc_count"] = content.count("❌") + content.count("anti-pattern")
            if "2604.02460" in content or "tran" in content or "kiela" in content or "dpi" in content:
                signals["evidence_cited_dpi"] = True
            if "ricorsivi" in content or "recursive" in content:
                signals["no_recursive_subagents_rule"] = True

    return signals


# ==============================================================================
# Pillar 6 · Observability & Recovery
# ==============================================================================

def scan_pillar_6_observability(root: Path) -> dict:
    signals: dict[str, Any] = {
        "centralized_log_dir": False,
        "liveness_watchdog": False,
        "aggregate_report": False,
        "drift_detector": False,
        "task_lifecycle_state_machine": False,
        "stuck_task_detection": False,
        "stderr_separated_from_stdout": False,
        "log_rotation_policy": False,
        "recovery_procedure_doc": False,
    }

    log_dirs = list(root.rglob("_logs")) + list(root.rglob("logs"))
    if log_dirs and any(d.is_dir() for d in log_dirs):
        signals["centralized_log_dir"] = True

    for f in find_files_by_pattern(root, "*liveness*.py") + find_files_by_pattern(root, "*watchdog*.py"):
        signals["liveness_watchdog"] = True
        break

    for f in find_files_by_pattern(root, "*aggregate*.py") + find_files_by_pattern(root, "*health*.py"):
        signals["aggregate_report"] = True
        break

    for f in find_files_by_pattern(root, "*drift*.py") + find_files_by_pattern(root, "*drift*.md"):
        signals["drift_detector"] = True
        break

    # State machine evidence
    for f in find_files_by_pattern(root, "*.md"):
        content = safe_read(f).lower()
        if any(seq in content for seq in ["inbox", "planning", "active", "review", "closing"]) and "kanban" in content.lower():
            signals["task_lifecycle_state_machine"] = True
        if "stuck" in content and "task" in content:
            signals["stuck_task_detection"] = True
        if "rotation" in content and "log" in content:
            signals["log_rotation_policy"] = True
        if "recovery" in content and "procedure" in content:
            signals["recovery_procedure_doc"] = True

    # Check .out.log / .err.log convention in plist files
    for f in find_files_by_pattern(root, "*.plist"):
        content = safe_read(f)
        if ".out.log" in content and ".err.log" in content:
            signals["stderr_separated_from_stdout"] = True
            break

    return signals


# ==============================================================================
# Pillar 7 · Credentials & Security
# ==============================================================================

def scan_pillar_7_credentials(root: Path) -> dict:
    signals: dict[str, Any] = {
        "plaintext_secrets_found": [],
        "vault_integration": False,
        "runtime_resolution_pattern": False,
        "env_in_gitignore": False,
        "credentials_doc": False,
        "secret_rotation_doc": False,
    }

    # Check .gitignore
    gitignore = root / ".gitignore"
    if gitignore.exists():
        content = safe_read(gitignore)
        if re.search(r"^\s*\.env\b", content, re.MULTILINE) or "*.env" in content:
            signals["env_in_gitignore"] = True

    # Look for vault integration evidence
    for f in find_files_by_pattern(root, ".envrc*") + find_files_by_pattern(root, "*.envrc"):
        content = safe_read(f)
        if "op://" in content or "vault read" in content or "doppler" in content.lower():
            signals["vault_integration"] = True
            signals["runtime_resolution_pattern"] = True
            break

    # Scan for plaintext secrets in committed files
    secret_count = 0
    for fp in walk_files(root, extensions={".md", ".py", ".js", ".ts", ".sh", ".json", ".yml", ".yaml", ".env", ".txt"}):
        # Skip files that are gitignored env templates that contain only op:// refs
        if fp.name == ".envrc.template":
            continue
        content = safe_read(fp, max_bytes=100_000)
        for pattern in SECRET_PATTERNS:
            matches = pattern.findall(content)
            if matches:
                # Reduce noise: only flag if it looks like an actual key (not pattern docs)
                for match in matches[:3]:  # cap per-file
                    secret_count += 1
                    signals["plaintext_secrets_found"].append({"file": str(fp.relative_to(root)) if fp.is_relative_to(root) else str(fp), "snippet_prefix": match[:20] + "..."})
                    if secret_count >= 20:
                        break
            if secret_count >= 20:
                break
        if secret_count >= 20:
            break

    # Credentials documentation
    for f in find_files_by_pattern(root, "API-MASTER*") + find_files_by_pattern(root, "credentials*.md") + find_files_by_pattern(root, "*api-master*"):
        signals["credentials_doc"] = True
        content = safe_read(f).lower()
        if "rotation" in content or "rotate" in content:
            signals["secret_rotation_doc"] = True
        break

    return signals


# ==============================================================================
# Pillar 8 · Portability & Re-deployability
# ==============================================================================

def scan_pillar_8_portability(root: Path) -> dict:
    signals: dict[str, Any] = {
        "bootstrap_doc": [],
        "templates_dir": False,
        "scaffold_dir": False,
        "client_isolation_evidence": False,
        "vault_per_engagement": False,
        "handoff_artifact_format": False,
        "hardcoded_paths_count": 0,
        "time_to_bootstrap_measured": False,
        "multiple_deployments_evidence": False,
    }

    for fname in ("ONBOARDING.md", "GETTING_STARTED.md", "QUICKSTART.md", "BOOTSTRAP.md", "SETUP.md"):
        for f in find_files_by_pattern(root, fname):
            signals["bootstrap_doc"].append(str(f))

    for d_name in ("templates", "scaffold", "boilerplate"):
        for d in root.rglob(d_name):
            if d.is_dir() and not any(part in IGNORE_DIRS for part in d.parts):
                if "scaffold" in d_name:
                    signals["scaffold_dir"] = True
                else:
                    signals["templates_dir"] = True
                break

    # Client isolation evidence: multiple subfolders under clients/ or per-client dirs · try common naming conventions
    for d_name in ("clients", "customers", "engagements", "tenants", "accounts"):
        for d in root.rglob(d_name):
            if d.is_dir() and not any(part in IGNORE_DIRS for part in d.parts):
                subdirs = [s for s in d.iterdir() if s.is_dir() and not s.name.startswith(".")]
                if len(subdirs) >= 2:
                    signals["client_isolation_evidence"] = True
                if len(subdirs) >= 2:
                    signals["multiple_deployments_evidence"] = True
                break

    # Vault per-engagement signal (look for namespace patterns in .envrc.template)
    for f in find_files_by_pattern(root, "*.envrc*"):
        content = safe_read(f)
        if re.search(r"op://[^/]+/[^/]+/", content):
            namespaces = set(re.findall(r"op://([^/]+)/", content))
            if len(namespaces) >= 2:
                signals["vault_per_engagement"] = True
            break

    # Handoff artifact format
    for f in find_files_by_pattern(root, "HANDOFF*.md") + find_files_by_pattern(root, "handoff*.md") + find_files_by_pattern(root, "SESSION-HANDOFF*"):
        signals["handoff_artifact_format"] = True
        break

    # Hardcoded paths heuristic (search /Users/ pattern in scripts)
    hardcoded_count = 0
    for fp in walk_files(root, extensions={".py", ".sh", ".js", ".ts"}):
        content = safe_read(fp, max_bytes=50_000)
        hardcoded_count += len(re.findall(r"/Users/[a-zA-Z0-9_-]+/", content))
        if hardcoded_count > 200:
            break
    signals["hardcoded_paths_count"] = hardcoded_count

    return signals


# ==============================================================================
# Pillar 9 · Metacognition & Self-Assessment
# ==============================================================================

def scan_pillar_9_metacognition(root: Path) -> dict:
    signals: dict[str, Any] = {
        "metacog_tool_found": False,
        "capability_profile_found": False,
        "verbalized_confidence_mechanism": False,
        "composite_formula_documented": False,
        "conflict_detection": False,
        "decision_gate_documented": False,
        "ema_update_mechanism": False,
        "ece_or_calibration_tracking": False,
        "anti_pattern_doc_count": 0,
        "dpi_integration_documented": False,
        "policy_doc_found": False,
        "metacog_paper_cited": False,
    }

    for f in find_files_by_pattern(root, "*metacog*.py") + find_files_by_pattern(root, "*self-assess*.py"):
        signals["metacog_tool_found"] = True
        content = safe_read(f).lower()
        if "verbalized" in content and "claude" in content or "llm" in content:
            signals["verbalized_confidence_mechanism"] = True
        if "lambda" in content and ("c_v" in content or "verbalized" in content) and ("c_p" in content or "profile" in content):
            signals["composite_formula_documented"] = True
        if "conflict" in content or "delta" in content and "abs" in content:
            signals["conflict_detection"] = True
        if "delegation_threshold" in content or "theta" in content or "decision" in content:
            signals["decision_gate_documented"] = True
        if "ema" in content or "p_new" in content and "p_old" in content or "learning_rate" in content:
            signals["ema_update_mechanism"] = True
        break

    for f in find_files_by_pattern(root, "*capability*profile*") + find_files_by_pattern(root, "*capability_profile*"):
        signals["capability_profile_found"] = True
        content = safe_read(f).lower()
        if "reasoning" in content and "retrieval" in content and "coding" in content:
            # Vector of dimensions present
            pass
        if "ema" in content or "alpha" in content:
            signals["ema_update_mechanism"] = signals["ema_update_mechanism"] or True
        if "ece" in content or "calibration" in content:
            signals["ece_or_calibration_tracking"] = True
        if "2605.17292" in content or "metacog" in content:
            signals["metacog_paper_cited"] = True
        break

    for f in find_files_by_pattern(root, "*metacognition*policy*") + find_files_by_pattern(root, "*metacognition*.md"):
        if f.is_file():
            signals["policy_doc_found"] = True
            content = safe_read(f).lower()
            if "anti-pattern" in content or "antipattern" in content:
                signals["anti_pattern_doc_count"] = content.count("❌") + content.count("anti-pattern")
            if "dpi" in content or "multi-agent" in content:
                signals["dpi_integration_documented"] = True
            if "2605.17292" in content or "metacogagent" in content:
                signals["metacog_paper_cited"] = True
            break

    return signals


# ==============================================================================
# Main
# ==============================================================================

def run_audit(workspace_path: Path, verbose: bool = False) -> dict:
    workspace = workspace_path.resolve()
    if not workspace.exists():
        sys.exit(f"Error: workspace path does not exist: {workspace}")
    if not workspace.is_dir():
        sys.exit(f"Error: workspace path is not a directory: {workspace}")

    if verbose:
        sys.stderr.write(f"Auditing workspace: {workspace}\n")

    audit = {
        "tool": "workspace-agentic-benchmark/audit.py",
        "version": "0.2.0",
        "audited_at": datetime.now().isoformat(),
        "workspace": str(workspace),
        "pillars": {},
    }

    pillar_scanners = [
        ("1_context_memory", scan_pillar_1_memory),
        ("2_skill_tool", scan_pillar_2_skills),
        ("3_governance", scan_pillar_3_governance),
        ("4_auto_improvement", scan_pillar_4_auto_improvement),
        ("5_multi_agent_dpi", scan_pillar_5_multi_agent),
        ("6_observability", scan_pillar_6_observability),
        ("7_credentials_security", scan_pillar_7_credentials),
        ("8_portability", scan_pillar_8_portability),
        ("9_metacognition", scan_pillar_9_metacognition),
    ]

    for name, scanner in pillar_scanners:
        if verbose:
            sys.stderr.write(f"  Scanning pillar: {name}\n")
        try:
            audit["pillars"][name] = scanner(workspace)
        except Exception as e:
            audit["pillars"][name] = {"error": str(e)}

    return audit


def main():
    p = argparse.ArgumentParser(description="Audit a workspace against the 8-pillar agentic benchmark.")
    p.add_argument("workspace", help="Path to workspace root directory.")
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose progress to stderr.")
    p.add_argument("--output", "-o", help="Output JSON path (default: stdout).")
    args = p.parse_args()

    audit = run_audit(Path(args.workspace), verbose=args.verbose)

    out_json = json.dumps(audit, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(out_json, encoding="utf-8")
        sys.stderr.write(f"Wrote audit to {args.output}\n")
    else:
        print(out_json)


if __name__ == "__main__":
    main()
