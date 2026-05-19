#!/usr/bin/env python3
"""
================================================================================
score.py · Workspace Agentic Benchmark v0.3 · L0-L4 maturity + weighted composite
================================================================================

LEGEND 4W:
  WHAT  · Apply 12-pillar L0-L4 maturity rubric to audit.json signals.
          Compute weighted composite score 0-100 + letter grade A/B/C/D/F.
  HOW   · Each pillar emits an L0-L4 level based on signal evidence.
          Level → score mapping: L0=0 · L1=20 · L2=50 · L3=75 · L4=100.
          Composite = Σ (level_score × weight) where weights sum to 1.0.
  WHERE · Input: audit.json (from audit.py). Output: score.json to stdout.
  WHEN  · CLI usage: python3 score.py audit.json > score.json

Grade thresholds (composite 0-100):
  · A · ≥85 · production-grade · forward-deployable
  · B · ≥70 · solid · 1-2 pillars need hardening
  · C · ≥50 · early-stage · multiple gaps
  · D · ≥30 · prototype · not production-ready
  · F · <30 · failing · infrastructure-first work required

Weights: default equal weight 1/12 per pillar (configurable via weights.json).

================================================================================
"""

from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


LEVEL_SCORES = {0: 0, 1: 20, 2: 50, 3: 75, 4: 100}
LEVEL_NAMES = {0: "L0 Absent", 1: "L1 Initial", 2: "L2 Managed", 3: "L3 Defined", 4: "L4 Optimizing"}


def determine_level(criteria_passed: int, criteria_total: int, premium_passed: int = 0) -> int:
    """
    Determine L0-L4 level from criteria passed.

    Rules:
    - L0: 0% passed
    - L1: <30% passed
    - L2: 30-59% passed
    - L3: 60-89% passed OR (60%+ and at least 1 premium criterion)
    - L4: 90%+ passed AND premium_passed >= 2 (optimization signals)
    """
    if criteria_total == 0:
        return 0
    pct = criteria_passed / criteria_total
    if pct == 0:
        return 0
    if pct < 0.3:
        return 1
    if pct < 0.6:
        return 2
    if pct < 0.9:
        return 3
    if premium_passed >= 2:
        return 4
    return 3


# ==============================================================================
# Pillar 1 · Context Hierarchy & Memory (Cluster A · Cognition)
# ==============================================================================

def score_pillar_1(s: dict) -> dict:
    tiers = len(s.get("tier_dirs_found", []))
    index_count = len(s.get("memory_index_files", []))
    structured = s.get("structured_entries_count", 0)
    crosslinks = s.get("cross_link_pattern_count", 0)

    passed = 0
    if tiers >= 1: passed += 1
    if tiers >= 3: passed += 1
    if tiers >= 5: passed += 1
    if index_count > 0: passed += 1
    if s.get("retrieval_policy_doc"): passed += 1
    if s.get("decay_policy_doc"): passed += 1
    if structured >= 5: passed += 1
    if crosslinks >= 10: passed += 1
    if s.get("mcp_query_layer"): passed += 1
    if s.get("kv_cache_awareness"): passed += 1

    premium = (1 if s.get("mcp_query_layer") else 0) + (1 if s.get("kv_cache_awareness") else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": passed, "criteria_total": 10}


# ==============================================================================
# Pillar 2 · Skill / Tool Architecture (Cluster B · Action)
# ==============================================================================

def score_pillar_2(s: dict) -> dict:
    n_skills = len(s.get("skill_folders", []))
    fm = s.get("skills_with_frontmatter", 0)
    det = s.get("deterministic_tools_count", 0)
    llm = s.get("llm_tools_count", 0)

    passed = 0
    if n_skills >= 1: passed += 1
    if n_skills >= 5: passed += 1
    if fm >= 1: passed += 1
    if fm >= 5: passed += 1
    if s.get("auto_trigger_mechanism"): passed += 1
    if s.get("staleness_detector_found"): passed += 1
    if det >= 1: passed += 1
    if det > 0 and (det + llm) > 0 and det / (det + llm) >= 0.3: passed += 1
    if s.get("skill_roster_doc"): passed += 1
    if s.get("skill_changelog", 0) >= 1: passed += 1

    premium = (1 if s.get("staleness_detector_found") else 0) + (1 if s.get("skill_roster_doc") else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": passed, "criteria_total": 10}


# ==============================================================================
# Pillar 3 · Governance & Compliance (Cluster C · Trust)
# ==============================================================================

def score_pillar_3(s: dict) -> dict:
    cf = len(s.get("constitution_found", []))
    hr = s.get("hard_rules_count", 0)

    passed = 0
    if cf >= 1: passed += 1
    if hr >= 1: passed += 1
    if hr >= 5: passed += 1
    if s.get("pre_output_check"): passed += 1
    if s.get("external_action_gate"): passed += 1
    if s.get("destructive_action_gate"): passed += 1
    if s.get("rules_versioning"): passed += 1
    if s.get("compliance_judge"): passed += 1
    if s.get("evidence_linked_rules", 0) >= 5: passed += 1
    if s.get("rules_dir_found"): passed += 1

    premium = (1 if s.get("compliance_judge") else 0) + (1 if s.get("pre_output_check") else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": passed, "criteria_total": 10}


# ==============================================================================
# Pillar 4 · Auto-Improvement Loop (Cluster A · Cognition)
# ==============================================================================

def score_pillar_4(s: dict) -> dict:
    passed = 0
    if s.get("session_capture_evidence"): passed += 1
    if s.get("reflexion_runner"): passed += 1
    if s.get("dreams_pipeline"): passed += 1
    if s.get("cron_for_improvement"): passed += 1
    if s.get("cheaper_model_used"): passed += 1
    if s.get("scoring_rubric_for_proposals"): passed += 1
    if s.get("two_stage_review"): passed += 1
    if s.get("apply_log_exists"): passed += 1
    if s.get("dreams_pipeline") and s.get("apply_log_exists"): passed += 1
    if s.get("reflexion_runner") and s.get("cron_for_improvement"): passed += 1

    premium = (1 if s.get("dreams_pipeline") else 0) + (1 if s.get("scoring_rubric_for_proposals") else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": passed, "criteria_total": 10}


# ==============================================================================
# Pillar 5 · Multi-Agent Discipline (DPI) (Cluster B · Action)
# ==============================================================================

def score_pillar_5(s: dict) -> dict:
    passed = 0
    if s.get("multi_agent_policy_doc"): passed += 1
    if s.get("single_thread_default"): passed += 1
    if s.get("pre_spawn_checklist"): passed += 1
    if s.get("explore_only_preauthorized"): passed += 1
    if s.get("no_recursive_subagents_rule"): passed += 1
    if s.get("evidence_cited_dpi"): passed += 1
    if s.get("anti_pattern_doc_count", 0) >= 4: passed += 1
    if s.get("multi_agent_policy_doc") and s.get("pre_spawn_checklist"): passed += 1
    if s.get("multi_agent_policy_doc") and s.get("evidence_cited_dpi"): passed += 1
    if s.get("multi_agent_policy_doc") and s.get("anti_pattern_doc_count", 0) >= 1: passed += 1

    premium = (1 if s.get("evidence_cited_dpi") else 0) + (1 if s.get("anti_pattern_doc_count", 0) >= 4 else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": passed, "criteria_total": 10}


# ==============================================================================
# Pillar 6 · Observability & Recovery (Cluster C · Trust)
# ==============================================================================

def score_pillar_6(s: dict) -> dict:
    passed = 0
    if s.get("centralized_log_dir"): passed += 1
    if s.get("liveness_watchdog"): passed += 1
    if s.get("aggregate_report"): passed += 1
    if s.get("drift_detector"): passed += 1
    if s.get("task_lifecycle_state_machine"): passed += 1
    if s.get("stuck_task_detection"): passed += 1
    if s.get("stderr_separated_from_stdout"): passed += 1
    if s.get("log_rotation_policy"): passed += 1
    if s.get("recovery_procedure_doc"): passed += 1
    if s.get("mast_taxonomy_referenced") or s.get("otel_genai_referenced"): passed += 1

    premium = (1 if s.get("mast_taxonomy_referenced") else 0) + (1 if s.get("otel_genai_referenced") else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": passed, "criteria_total": 10}


# ==============================================================================
# Pillar 7 · Credentials & Security (Cluster C · Trust)
# ==============================================================================

def score_pillar_7(s: dict) -> dict:
    plaintext_count = len(s.get("plaintext_secrets_found", []))

    passed = 0
    if s.get("env_in_gitignore"): passed += 1
    if s.get("vault_integration"): passed += 1
    if s.get("runtime_resolution_pattern"): passed += 1
    if s.get("credentials_doc"): passed += 1
    if s.get("secret_rotation_doc"): passed += 1
    if plaintext_count == 0: passed += 3  # heavy weight: zero plaintext is core
    elif plaintext_count <= 2: passed += 1
    if s.get("owasp_llm_referenced"): passed += 2

    premium = (1 if plaintext_count == 0 else 0) + (1 if s.get("owasp_llm_referenced") else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": min(passed, 10), "criteria_total": 10}


# ==============================================================================
# Pillar 8 · Portability & Re-deployability (Cluster D · Operations)
# ==============================================================================

def score_pillar_8(s: dict) -> dict:
    n_bootstrap = len(s.get("bootstrap_doc", []))
    hardcoded = s.get("hardcoded_paths_count", 0)

    passed = 0
    if n_bootstrap >= 1: passed += 1
    if s.get("client_isolation_evidence"): passed += 1
    if s.get("vault_per_engagement"): passed += 1
    if s.get("templates_dir") or s.get("scaffold_dir"): passed += 1
    if s.get("handoff_artifact_format"): passed += 1
    if hardcoded <= 20: passed += 1
    elif hardcoded <= 100: passed += 0  # partial inappropriate at L4 · only 0/1 per criterion
    if s.get("multiple_deployments_evidence"): passed += 1
    if s.get("client_isolation_evidence") and s.get("vault_per_engagement"): passed += 1
    if n_bootstrap >= 1 and (s.get("templates_dir") or s.get("scaffold_dir")): passed += 1
    if s.get("vault_per_engagement") and s.get("client_isolation_evidence"): passed += 1

    premium = (1 if s.get("vault_per_engagement") else 0) + (1 if s.get("multiple_deployments_evidence") else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": passed, "criteria_total": 10}


# ==============================================================================
# Pillar 9 · Metacognition & Self-Assessment (Cluster A · Cognition)
# ==============================================================================

def score_pillar_9(s: dict) -> dict:
    passed = 0
    if s.get("metacog_tool_found"): passed += 1
    if s.get("verbalized_confidence_mechanism"): passed += 1
    if s.get("capability_profile_found"): passed += 1
    if s.get("composite_formula_documented"): passed += 1
    if s.get("conflict_detection"): passed += 1
    if s.get("decision_gate_documented"): passed += 1
    if s.get("ema_update_mechanism"): passed += 1
    if s.get("ece_or_calibration_tracking"): passed += 1
    if s.get("anti_pattern_doc_count", 0) >= 4: passed += 1
    if s.get("dpi_integration_documented"): passed += 1

    premium = (1 if s.get("ece_or_calibration_tracking") else 0) + (1 if s.get("metacog_paper_cited") else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": passed, "criteria_total": 10}


# ==============================================================================
# Pillar 10 · Reliability & Determinism (Cluster B · Action) · NEW v0.3
# ==============================================================================

def score_pillar_10(s: dict) -> dict:
    passed = 0
    if s.get("determinism_doc"): passed += 1
    if s.get("retry_logic_documented"): passed += 1
    if s.get("idempotency_doc"): passed += 1
    if s.get("pass_at_k_measurement"): passed += 2  # heavier weight
    if s.get("mast_taxonomy_coverage"): passed += 2
    if s.get("replay_harness"): passed += 1
    if s.get("circuit_breaker_pattern"): passed += 1
    if s.get("retry_logic_documented") and s.get("idempotency_doc"): passed += 1
    if s.get("pass_at_k_measurement") and s.get("mast_taxonomy_coverage"): passed += 1

    premium = (1 if s.get("pass_at_k_measurement") else 0) + (1 if s.get("mast_taxonomy_coverage") else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": min(passed, 10), "criteria_total": 10}


# ==============================================================================
# Pillar 11 · Human-in-the-Loop (Cluster C · Trust) · NEW v0.3
# ==============================================================================

def score_pillar_11(s: dict) -> dict:
    passed = 0
    if s.get("approval_gate_documented"): passed += 2
    if s.get("escalation_criteria_doc"): passed += 2
    if s.get("feedback_collection_structured"): passed += 1
    if s.get("approval_friction_measured"): passed += 1
    if s.get("bypass_detection"): passed += 1
    if s.get("hitl_policy_doc"): passed += 1
    if s.get("nist_ai_rmf_referenced"): passed += 1
    if s.get("approval_gate_documented") and s.get("escalation_criteria_doc"): passed += 1

    premium = (1 if s.get("nist_ai_rmf_referenced") else 0) + (1 if s.get("approval_friction_measured") else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": min(passed, 10), "criteria_total": 10}


# ==============================================================================
# Pillar 12 · Cost & Performance Efficiency (Cluster D · Operations) · NEW v0.3
# ==============================================================================

def score_pillar_12(s: dict) -> dict:
    passed = 0
    if s.get("cost_tracking_doc"): passed += 1
    if s.get("latency_measurement_doc"): passed += 1
    if s.get("cache_hit_rate_measured"): passed += 1
    if s.get("cheaper_model_in_cron"): passed += 1
    if s.get("model_routing_policy"): passed += 1
    if s.get("subscription_vs_api_doc"): passed += 1
    if s.get("cost_per_outcome_doc"): passed += 2  # heavier · the only metric that matters
    if s.get("clear_paper_cited"): passed += 1
    if s.get("cost_tracking_doc") and s.get("cache_hit_rate_measured"): passed += 1
    if s.get("model_routing_policy") and s.get("cheaper_model_in_cron"): passed += 1

    premium = (1 if s.get("cost_per_outcome_doc") else 0) + (1 if s.get("clear_paper_cited") else 0)
    level = determine_level(passed, 10, premium)
    return {"level": level, "level_name": LEVEL_NAMES[level], "score": LEVEL_SCORES[level], "criteria_passed": min(passed, 10), "criteria_total": 10}


# ==============================================================================
# Helpers
# ==============================================================================

CLUSTER_MAP = {
    "1_context_memory": "A · Cognition",
    "4_auto_improvement": "A · Cognition",
    "9_metacognition": "A · Cognition",
    "2_skill_tool": "B · Action",
    "5_multi_agent_dpi": "B · Action",
    "10_reliability": "B · Action",
    "3_governance": "C · Trust",
    "6_observability": "C · Trust",
    "7_credentials_security": "C · Trust",
    "11_human_in_the_loop": "C · Trust",
    "8_portability": "D · Operations",
    "12_cost_performance": "D · Operations",
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
    ("9_metacognition", "Metacognition & Self-Assessment", score_pillar_9),
    ("10_reliability", "Reliability & Determinism", score_pillar_10),
    ("11_human_in_the_loop", "Human-in-the-Loop", score_pillar_11),
    ("12_cost_performance", "Cost & Performance Efficiency", score_pillar_12),
]


def load_weights(weights_path: Path | None) -> dict[str, float]:
    if weights_path and weights_path.exists():
        try:
            data = json.loads(weights_path.read_text(encoding="utf-8"))
            return {k: float(v) for k, v in data.get("weights", {}).items()}
        except Exception:
            pass
    # Default: equal weight 1/12 per pillar
    return {key: 1.0 / 12.0 for key, _, _ in PILLARS}


def grade(total: float) -> str:
    if total >= 85: return "A"
    if total >= 70: return "B"
    if total >= 50: return "C"
    if total >= 30: return "D"
    return "F"


def grade_description(g: str) -> str:
    descriptions = {
        "A": "Production-grade · forward-deployable · FDE-engagement ready",
        "B": "Solid · 1-2 pillars need hardening before scale",
        "C": "Early-stage · multiple gaps · workspace work needed alongside agent work",
        "D": "Prototype · not production-ready · infrastructure-first work required",
        "F": "Failing · workspace not fit for purpose",
    }
    return descriptions.get(g, "")


def score_audit(audit: dict, weights: dict[str, float]) -> dict:
    pillars_in = audit.get("pillars", {})
    pillars_out: dict = {}
    composite = 0.0
    total_weight_used = 0.0
    cluster_scores: dict = {}

    for key, title, scorer in PILLARS:
        signals = pillars_in.get(key, {})
        weight = weights.get(key, 1.0 / 12.0)
        if "error" in signals:
            pillars_out[key] = {"title": title, "cluster": CLUSTER_MAP.get(key, "?"), "error": signals["error"], "level": 0, "level_name": LEVEL_NAMES[0], "score": 0, "weight": weight}
            continue
        result = scorer(signals)
        result["title"] = title
        result["cluster"] = CLUSTER_MAP.get(key, "?")
        result["weight"] = round(weight, 4)
        pillars_out[key] = result
        composite += result["score"] * weight
        total_weight_used += weight

        # Cluster aggregation
        cluster = CLUSTER_MAP.get(key, "?")
        if cluster not in cluster_scores:
            cluster_scores[cluster] = {"sum": 0.0, "count": 0}
        cluster_scores[cluster]["sum"] += result["score"]
        cluster_scores[cluster]["count"] += 1

    composite_normalized = composite / total_weight_used if total_weight_used > 0 else 0
    composite_normalized = round(composite_normalized, 2)

    cluster_summary = {
        cluster: round(data["sum"] / data["count"], 2) if data["count"] > 0 else 0
        for cluster, data in cluster_scores.items()
    }

    return {
        "tool": "workspace-agentic-benchmark/score.py",
        "version": "0.3.0",
        "scored_at": datetime.now().isoformat(),
        "workspace": audit.get("workspace"),
        "audit_at": audit.get("audited_at"),
        "composite": composite_normalized,
        "max": 100,
        "grade": grade(composite_normalized),
        "grade_description": grade_description(grade(composite_normalized)),
        "cluster_averages": cluster_summary,
        "pillars": pillars_out,
        "scoring_model": {
            "level_mapping": LEVEL_SCORES,
            "level_names": LEVEL_NAMES,
            "thresholds": {"A": 85, "B": 70, "C": 50, "D": 30, "F": 0},
        },
    }


def main():
    p = argparse.ArgumentParser(description="Score an audit.json against the 12-pillar L0-L4 rubric (v0.3).")
    p.add_argument("audit_json", help="Path to audit.json (output of audit.py).")
    p.add_argument("--weights", help="Path to weights.json (overrides equal default).")
    p.add_argument("--output", "-o", help="Output JSON path (default: stdout).")
    args = p.parse_args()

    audit = json.loads(Path(args.audit_json).read_text(encoding="utf-8"))
    weights = load_weights(Path(args.weights) if args.weights else None)
    score = score_audit(audit, weights)

    out_json = json.dumps(score, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(out_json, encoding="utf-8")
        sys.stderr.write(f"Wrote score to {args.output}\n")
    else:
        print(out_json)


if __name__ == "__main__":
    main()
