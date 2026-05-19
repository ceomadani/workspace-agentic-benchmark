#!/usr/bin/env python3
"""
================================================================================
score.py · Workspace Agentic Benchmark · pillar scorer
================================================================================

LEGGENDA 4W:
  COSA  · Apply 8-pillar scoring rubric to audit.json signals.
  COME  · Map raw audit signals to 0-10 score per pillar via rule-based rubric.
  DOVE  · Input: audit.json (from audit.py). Output: score.json to stdout.
  QUANDO · CLI usage: python3 score.py audit.json > score.json

Each pillar applies a checklist of 10 binary criteria:
  · pass (1.0) · partial (0.5) · fail (0.0) · capped at 10.

Grade thresholds (total 0-80):
  · A · 68-80 · production-grade · forward-deployable
  · B · 51-67 · solid · needs hardening in 1-2 pillars
  · C · 34-50 · early-stage · multiple gaps
  · D · 0-33 · prototype · not production-ready

================================================================================
"""

from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def _b(condition: bool) -> float:
    """Binary pass/fail."""
    return 1.0 if condition else 0.0


def _p(condition: bool, partial: bool = False) -> float:
    """Pass/partial/fail."""
    if condition:
        return 1.0
    if partial:
        return 0.5
    return 0.0


# ==============================================================================
# Pillar 1 · Context Hierarchy & Memory
# ==============================================================================

def score_pillar_1(s: dict) -> dict:
    tiers = len(s.get("tier_dirs_found", []))
    index_count = len(s.get("memory_index_files", []))
    structured = s.get("structured_entries_count", 0)
    crosslinks = s.get("cross_link_pattern_count", 0)

    criteria = [
        ("multi_tier_3plus", _p(tiers >= 3, partial=(tiers >= 2))),
        ("retrieval_policy_explicit", _b(s.get("retrieval_policy_doc", False))),
        ("decay_policy_explicit", _b(s.get("decay_policy_doc", False))),
        ("index_file_loads_auto", _p(index_count > 0, partial=False)),
        ("structured_frontmatter", _p(structured >= 5, partial=(structured >= 1))),
        ("cross_links_graph", _p(crosslinks >= 10, partial=(crosslinks >= 1))),
        ("episodic_from_reflection", _b(any("episodic" in t.get("tier", "") for t in s.get("tier_dirs_found", [])))),
        ("queryable_storage", _b(s.get("mcp_query_layer", False))),
        ("kv_cache_awareness", _b(s.get("kv_cache_awareness", False))),
        ("documented_retrieval_failure_mode", _p(s.get("retrieval_policy_doc", False) and s.get("decay_policy_doc", False), partial=False)),
    ]
    return _bundle(criteria)


# ==============================================================================
# Pillar 2 · Skill / Tool Architecture
# ==============================================================================

def score_pillar_2(s: dict) -> dict:
    n_skills = len(s.get("skill_folders", []))
    fm = s.get("skills_with_frontmatter", 0)
    det = s.get("deterministic_tools_count", 0)
    llm = s.get("llm_tools_count", 0)
    total_tools = det + llm

    criteria = [
        ("skills_dedicated_location", _p(n_skills >= 3, partial=(n_skills >= 1))),
        ("self_contained_units", _p(n_skills >= 5, partial=(n_skills >= 1))),
        ("frontmatter_present", _p(fm >= 5, partial=(fm >= 1))),
        ("auto_trigger_mechanism", _b(s.get("auto_trigger_mechanism", False))),
        ("staleness_detection", _b(s.get("staleness_detector_found", False))),
        ("determinism_preferred", _p(det > 0 and (total_tools == 0 or det / max(total_tools, 1) >= 0.3), partial=(det > 0))),
        ("roster_curation", _b(s.get("skill_roster_doc", False))),
        ("changelog_versioning", _p(s.get("skill_changelog", 0) >= 1, partial=False)),
        ("no_grab_bag_megaskills", _p(n_skills >= 5, partial=(n_skills >= 1))),
        ("cross_referenced", _p(n_skills >= 10, partial=(n_skills >= 1))),
    ]
    return _bundle(criteria)


# ==============================================================================
# Pillar 3 · Governance & Compliance
# ==============================================================================

def score_pillar_3(s: dict) -> dict:
    cf = len(s.get("constitution_found", []))
    hr = s.get("hard_rules_count", 0)

    criteria = [
        ("constitution_exists", _p(cf >= 1, partial=False)),
        ("hard_rules_enumerated", _p(hr >= 5, partial=(hr >= 1))),
        ("pre_output_check", _b(s.get("pre_output_check", False))),
        ("external_action_gate", _b(s.get("external_action_gate", False))),
        ("destructive_action_gate", _b(s.get("destructive_action_gate", False))),
        ("constitution_versioned", _b(s.get("rules_versioning", False))),
        ("compliance_judge_exists", _b(s.get("compliance_judge", False))),
        ("evidence_linked_rules", _p(s.get("evidence_linked_rules", 0) >= 5, partial=(s.get("evidence_linked_rules", 0) >= 1))),
        ("escalation_path_documented", _p(s.get("external_action_gate", False) and s.get("destructive_action_gate", False), partial=False)),
        ("layered_rules", _b(s.get("rules_dir_found", False))),
    ]
    return _bundle(criteria)


# ==============================================================================
# Pillar 4 · Auto-Improvement Loop
# ==============================================================================

def score_pillar_4(s: dict) -> dict:
    criteria = [
        ("session_capture", _b(s.get("session_capture_evidence", False))),
        ("reflection_cron", _b(s.get("reflexion_runner", False) and s.get("cron_for_improvement", False))),
        ("reflection_writes_episodic", _b(s.get("reflexion_runner", False))),
        ("improvement_proposal_system", _b(s.get("dreams_pipeline", False))),
        ("scoring_rubric_for_proposals", _b(s.get("scoring_rubric_for_proposals", False))),
        ("two_stage_review", _b(s.get("two_stage_review", False))),
        ("apply_log_exists", _b(s.get("apply_log_exists", False))),
        ("feedback_loop_measured", _p(s.get("dreams_pipeline", False) and s.get("apply_log_exists", False), partial=False)),
        ("cron_driven", _b(s.get("cron_for_improvement", False))),
        ("cost_aware_cheaper_model", _b(s.get("cheaper_model_used", False))),
    ]
    return _bundle(criteria)


# ==============================================================================
# Pillar 5 · Multi-Agent Discipline (DPI)
# ==============================================================================

def score_pillar_5(s: dict) -> dict:
    criteria = [
        ("single_thread_default_documented", _b(s.get("single_thread_default", False))),
        ("multi_agent_policy_file", _b(s.get("multi_agent_policy_doc", False))),
        ("pre_spawn_gate", _b(s.get("pre_spawn_checklist", False))),
        ("explore_only_preauthorized", _b(s.get("explore_only_preauthorized", False))),
        ("no_recursive_subagents", _b(s.get("no_recursive_subagents_rule", False))),
        ("self_contained_subagent_prompts", _p(s.get("multi_agent_policy_doc", False), partial=False)),
        ("evidence_cited", _b(s.get("evidence_cited_dpi", False))),
        ("budget_guard", _p(s.get("pre_spawn_checklist", False), partial=False)),
        ("anti_pattern_list", _p(s.get("anti_pattern_doc_count", 0) >= 4, partial=(s.get("anti_pattern_doc_count", 0) >= 1))),
        ("logged_invocations", _p(s.get("multi_agent_policy_doc", False), partial=False)),
    ]
    return _bundle(criteria)


# ==============================================================================
# Pillar 6 · Observability & Recovery
# ==============================================================================

def score_pillar_6(s: dict) -> dict:
    criteria = [
        ("centralized_logs", _b(s.get("centralized_log_dir", False))),
        ("liveness_watchdog", _b(s.get("liveness_watchdog", False))),
        ("aggregate_health_report", _b(s.get("aggregate_report", False))),
        ("drift_detector", _b(s.get("drift_detector", False))),
        ("explicit_state_machine", _b(s.get("task_lifecycle_state_machine", False))),
        ("stuck_task_detection", _b(s.get("stuck_task_detection", False))),
        ("cron_success_tracked", _p(s.get("aggregate_report", False), partial=False)),
        ("stderr_separated", _b(s.get("stderr_separated_from_stdout", False))),
        ("log_rotation_policy", _b(s.get("log_rotation_policy", False))),
        ("recovery_procedure_doc", _b(s.get("recovery_procedure_doc", False))),
    ]
    return _bundle(criteria)


# ==============================================================================
# Pillar 7 · Credentials & Security
# ==============================================================================

def score_pillar_7(s: dict) -> dict:
    plaintext_count = len(s.get("plaintext_secrets_found", []))
    criteria = [
        ("zero_plaintext_secrets", _p(plaintext_count == 0, partial=(plaintext_count <= 2))),
        ("vault_integrated", _b(s.get("vault_integration", False))),
        ("runtime_resolution", _b(s.get("runtime_resolution_pattern", False))),
        ("env_in_gitignore", _b(s.get("env_in_gitignore", False))),
        ("external_action_approval", _p(s.get("credentials_doc", False), partial=False)),
        ("audit_log", _p(s.get("vault_integration", False), partial=False)),
        ("rotation_documented", _b(s.get("secret_rotation_doc", False))),
        ("no_credentials_in_history", _p(plaintext_count == 0, partial=False)),
        ("no_credentials_in_urls", _p(plaintext_count == 0, partial=False)),
        ("per_environment_separation", _p(s.get("vault_integration", False), partial=False)),
    ]
    return _bundle(criteria)


# ==============================================================================
# Pillar 8 · Portability & Re-deployability
# ==============================================================================

def score_pillar_8(s: dict) -> dict:
    n_bootstrap = len(s.get("bootstrap_doc", []))
    hardcoded = s.get("hardcoded_paths_count", 0)
    criteria = [
        ("bootstrap_doc_exists", _p(n_bootstrap >= 1, partial=False)),
        ("skills_client_agnostic_or_tagged", _p(s.get("client_isolation_evidence", False), partial=False)),
        ("credentials_per_engagement_isolated", _b(s.get("vault_per_engagement", False))),
        ("per_environment_separation", _p(s.get("vault_per_engagement", False), partial=False)),
        ("state_externalized", _p(s.get("client_isolation_evidence", False), partial=False)),
        ("template_scaffold_exists", _p(s.get("templates_dir", False) or s.get("scaffold_dir", False), partial=False)),
        ("memory_isolation_per_engagement", _p(s.get("vault_per_engagement", False), partial=False)),
        ("handoff_artifact_format", _b(s.get("handoff_artifact_format", False))),
        ("low_hardcoded_paths", _p(hardcoded <= 20, partial=(hardcoded <= 100))),
        ("multiple_deployments_evidence", _b(s.get("multiple_deployments_evidence", False))),
    ]
    return _bundle(criteria)


# ==============================================================================
# Helpers
# ==============================================================================

def _bundle(criteria: list[tuple[str, float]]) -> dict:
    total = sum(score for _, score in criteria)
    total = min(total, 10.0)
    return {
        "criteria": [{"name": name, "score": score} for name, score in criteria],
        "score": round(total, 2),
        "max": 10,
    }


PILLARS = [
    ("1_context_memory", "Context Hierarchy & Memory", score_pillar_1),
    ("2_skill_tool", "Skill / Tool Architecture", score_pillar_2),
    ("3_governance", "Governance & Compliance", score_pillar_3),
    ("4_auto_improvement", "Auto-Improvement Loop", score_pillar_4),
    ("5_multi_agent_dpi", "Multi-Agent Discipline (DPI)", score_pillar_5),
    ("6_observability", "Observability & Recovery", score_pillar_6),
    ("7_credentials_security", "Credentials & Security", score_pillar_7),
    ("8_portability", "Portability & Re-deployability", score_pillar_8),
]


def grade(total: float) -> str:
    if total >= 68:
        return "A"
    if total >= 51:
        return "B"
    if total >= 34:
        return "C"
    return "D"


def score_audit(audit: dict) -> dict:
    pillars_in = audit.get("pillars", {})
    pillars_out: dict[str, Any] = {}
    total = 0.0

    for key, title, scorer in PILLARS:
        signals = pillars_in.get(key, {})
        if "error" in signals:
            pillars_out[key] = {"title": title, "error": signals["error"], "score": 0, "max": 10}
            continue
        result = scorer(signals)
        result["title"] = title
        pillars_out[key] = result
        total += result["score"]

    return {
        "tool": "workspace-agentic-benchmark/score.py",
        "version": "0.1.0",
        "scored_at": datetime.now().isoformat(),
        "workspace": audit.get("workspace"),
        "audit_at": audit.get("audited_at"),
        "total": round(total, 2),
        "max": 80,
        "grade": grade(total),
        "pillars": pillars_out,
    }


def main():
    p = argparse.ArgumentParser(description="Score an audit.json against the 8-pillar rubric.")
    p.add_argument("audit_json", help="Path to audit.json (output of audit.py).")
    p.add_argument("--output", "-o", help="Output JSON path (default: stdout).")
    args = p.parse_args()

    audit = json.loads(Path(args.audit_json).read_text(encoding="utf-8"))
    score = score_audit(audit)

    out_json = json.dumps(score, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(out_json, encoding="utf-8")
        sys.stderr.write(f"Wrote score to {args.output}\n")
    else:
        print(out_json)


if __name__ == "__main__":
    main()
