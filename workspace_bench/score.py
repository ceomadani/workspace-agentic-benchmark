"""L0-L4 maturity scoring · weighted composite · cluster aggregation."""

from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import Callable

from .data import (
    LEVEL_SCORES,
    LEVEL_NAMES,
    PILLARS,
    grade,
    grade_description,
    equal_weights,
)


def determine_level(criteria_passed: int, criteria_total: int, premium_passed: int = 0) -> int:
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


def _score_p1(s: dict) -> dict:
    tiers = len(s.get("tier_dirs_found", []))
    structured = s.get("structured_entries_count", 0)
    crosslinks = s.get("cross_link_pattern_count", 0)
    passed = 0
    if tiers >= 1: passed += 1
    if tiers >= 3: passed += 1
    if tiers >= 5: passed += 1
    if len(s.get("memory_index_files", [])) > 0: passed += 1
    if s.get("retrieval_policy_doc"): passed += 1
    if s.get("decay_policy_doc"): passed += 1
    if structured >= 5: passed += 1
    if crosslinks >= 10: passed += 1
    if s.get("mcp_query_layer"): passed += 1
    if s.get("kv_cache_awareness"): passed += 1
    premium = (1 if s.get("mcp_query_layer") else 0) + (1 if s.get("kv_cache_awareness") else 0)
    return _bundle(passed, 10, premium)


def _score_p2(s: dict) -> dict:
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
    return _bundle(passed, 10, premium)


def _score_p3(s: dict) -> dict:
    hr = s.get("hard_rules_count", 0)
    passed = 0
    if len(s.get("constitution_found", [])) >= 1: passed += 1
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
    return _bundle(passed, 10, premium)


def _score_p4(s: dict) -> dict:
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
    return _bundle(passed, 10, premium)


def _score_p5(s: dict) -> dict:
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
    return _bundle(passed, 10, premium)


def _score_p6(s: dict) -> dict:
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
    return _bundle(passed, 10, premium)


def _score_p7(s: dict) -> dict:
    plaintext_count = len(s.get("plaintext_secrets_found", []))
    passed = 0
    if s.get("env_in_gitignore"): passed += 1
    if s.get("vault_integration"): passed += 1
    if s.get("runtime_resolution_pattern"): passed += 1
    if s.get("credentials_doc"): passed += 1
    if s.get("secret_rotation_doc"): passed += 1
    if plaintext_count == 0:
        passed += 3
    elif plaintext_count <= 2:
        passed += 1
    if s.get("owasp_llm_referenced"): passed += 2
    premium = (1 if plaintext_count == 0 else 0) + (1 if s.get("owasp_llm_referenced") else 0)
    return _bundle(min(passed, 10), 10, premium)


def _score_p8(s: dict) -> dict:
    n_bootstrap = len(s.get("bootstrap_doc", []))
    hardcoded = s.get("hardcoded_paths_count", 0)
    passed = 0
    if n_bootstrap >= 1: passed += 1
    if s.get("client_isolation_evidence"): passed += 1
    if s.get("vault_per_engagement"): passed += 1
    if s.get("templates_dir") or s.get("scaffold_dir"): passed += 1
    if s.get("handoff_artifact_format"): passed += 1
    if hardcoded <= 20: passed += 1
    if s.get("multiple_deployments_evidence"): passed += 1
    if s.get("client_isolation_evidence") and s.get("vault_per_engagement"): passed += 1
    if n_bootstrap >= 1 and (s.get("templates_dir") or s.get("scaffold_dir")): passed += 1
    if s.get("vault_per_engagement") and s.get("client_isolation_evidence"): passed += 1
    premium = (1 if s.get("vault_per_engagement") else 0) + (1 if s.get("multiple_deployments_evidence") else 0)
    return _bundle(passed, 10, premium)


def _score_p9(s: dict) -> dict:
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
    return _bundle(passed, 10, premium)


def _score_p10(s: dict) -> dict:
    passed = 0
    if s.get("determinism_doc"): passed += 1
    if s.get("retry_logic_documented"): passed += 1
    if s.get("idempotency_doc"): passed += 1
    if s.get("pass_at_k_measurement"): passed += 2
    if s.get("mast_taxonomy_coverage"): passed += 2
    if s.get("replay_harness"): passed += 1
    if s.get("circuit_breaker_pattern"): passed += 1
    if s.get("retry_logic_documented") and s.get("idempotency_doc"): passed += 1
    if s.get("pass_at_k_measurement") and s.get("mast_taxonomy_coverage"): passed += 1
    premium = (1 if s.get("pass_at_k_measurement") else 0) + (1 if s.get("mast_taxonomy_coverage") else 0)
    return _bundle(min(passed, 10), 10, premium)


def _score_p11(s: dict) -> dict:
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
    return _bundle(min(passed, 10), 10, premium)


def _score_p12(s: dict) -> dict:
    passed = 0
    if s.get("cost_tracking_doc"): passed += 1
    if s.get("latency_measurement_doc"): passed += 1
    if s.get("cache_hit_rate_measured"): passed += 1
    if s.get("cheaper_model_in_cron"): passed += 1
    if s.get("model_routing_policy"): passed += 1
    if s.get("subscription_vs_api_doc"): passed += 1
    if s.get("cost_per_outcome_doc"): passed += 2
    if s.get("clear_paper_cited"): passed += 1
    if s.get("cost_tracking_doc") and s.get("cache_hit_rate_measured"): passed += 1
    if s.get("model_routing_policy") and s.get("cheaper_model_in_cron"): passed += 1
    premium = (1 if s.get("cost_per_outcome_doc") else 0) + (1 if s.get("clear_paper_cited") else 0)
    return _bundle(min(passed, 10), 10, premium)


def _bundle(passed: int, total: int, premium: int) -> dict:
    level = determine_level(passed, total, premium)
    return {
        "level": level,
        "level_name": LEVEL_NAMES[level],
        "score": LEVEL_SCORES[level],
        "criteria_passed": passed,
        "criteria_total": total,
    }


SCORERS: dict[str, Callable[[dict], dict]] = {
    "1_context_memory": _score_p1,
    "2_skill_tool": _score_p2,
    "3_governance": _score_p3,
    "4_auto_improvement": _score_p4,
    "5_multi_agent_dpi": _score_p5,
    "6_observability": _score_p6,
    "7_credentials_security": _score_p7,
    "8_portability": _score_p8,
    "9_metacognition": _score_p9,
    "10_reliability": _score_p10,
    "11_human_in_the_loop": _score_p11,
    "12_cost_performance": _score_p12,
}


def load_weights(weights_path: Path | None) -> dict[str, float]:
    if weights_path and weights_path.exists():
        try:
            data = json.loads(weights_path.read_text(encoding="utf-8"))
            return {k: float(v) for k, v in data.get("weights", {}).items()}
        except Exception:
            pass
    return equal_weights()


def score_audit(
    audit: dict,
    weights: dict[str, float] | None = None,
    profile: dict | None = None,
    extensions_result: dict | None = None,
) -> dict:
    """Score a workspace audit · backward-compatible iter-1.

    iter-2 args (optional):
      - profile: parsed YAML dict from profiles/<id>.yml · applies per-pillar weights + extension enforcement
      - extensions_result: dict from extensions.detect_extensions(workspace) · 11 extension presence checks

    When profile is provided · its weights override the `weights` arg.
    When extensions_result is provided · added to output + used for profile compliance check.
    """
    from . import __version__

    # Profile · resolve weights if profile passed
    profile_id = None
    profile_summary = None
    if profile is not None:
        from .profiles import profile_to_pillar_weights, evaluate_extensions_against_profile
        weights = profile_to_pillar_weights(profile)
        profile_id = profile.get("profile_id", "custom")
        if extensions_result:
            profile_summary = evaluate_extensions_against_profile(profile, extensions_result)

    if weights is None:
        weights = equal_weights()

    pillars_in = audit.get("pillars", {})
    pillars_out: dict = {}
    composite = 0.0
    total_weight_used = 0.0
    cluster_scores: dict = {}

    for pillar_meta in PILLARS:
        key = pillar_meta.key
        signals = pillars_in.get(key, {})
        weight = weights.get(key, 1.0 / len(PILLARS))
        if "error" in signals:
            pillars_out[key] = {
                "title": pillar_meta.title,
                "cluster": f"{pillar_meta.cluster_letter} · {pillar_meta.cluster}",
                "cluster_letter": pillar_meta.cluster_letter,
                "n": pillar_meta.n,
                "error": signals["error"],
                "level": 0,
                "level_name": LEVEL_NAMES[0],
                "score": 0,
                "weight": weight,
            }
            continue
        result = SCORERS[key](signals)
        result["title"] = pillar_meta.title
        result["cluster"] = f"{pillar_meta.cluster_letter} · {pillar_meta.cluster}"
        result["cluster_letter"] = pillar_meta.cluster_letter
        result["n"] = pillar_meta.n
        result["weight"] = round(weight, 4)
        pillars_out[key] = result
        composite += result["score"] * weight
        total_weight_used += weight

        cluster = pillar_meta.cluster_letter
        if cluster not in cluster_scores:
            cluster_scores[cluster] = {"sum": 0.0, "count": 0, "name": pillar_meta.cluster}
        cluster_scores[cluster]["sum"] += result["score"]
        cluster_scores[cluster]["count"] += 1

    composite_norm = composite / total_weight_used if total_weight_used > 0 else 0
    composite_norm = round(composite_norm, 2)

    cluster_summary = {
        cluster: {
            "name": data["name"],
            "average": round(data["sum"] / data["count"], 2) if data["count"] > 0 else 0,
        }
        for cluster, data in cluster_scores.items()
    }

    result = {
        "tool": "workspace-bench",
        "version": __version__,
        "scored_at": datetime.now().isoformat(),
        "workspace": audit.get("workspace"),
        "audit_at": audit.get("audited_at"),
        "composite": composite_norm,
        "max": 100,
        "grade": grade(composite_norm),
        "grade_description": grade_description(grade(composite_norm)),
        "cluster_averages": cluster_summary,
        "pillars": pillars_out,
        "scoring_model": {
            "level_mapping": LEVEL_SCORES,
            "level_names": LEVEL_NAMES,
            "thresholds": {"A": 85, "B": 70, "C": 50, "D": 30, "F": 0},
        },
    }

    # iter-2 additions · only present when used
    if profile_id is not None:
        result["profile_id"] = profile_id
        result["profile_weights_applied"] = {k: round(v, 3) for k, v in weights.items()}
    if extensions_result is not None:
        result["extensions"] = extensions_result
    if profile_summary is not None:
        result["profile_extension_compliance"] = profile_summary
        # Penalty: if required extensions ratio < 1.0, apply soft penalty visible to user
        compliance = profile_summary.get("required_compliance_ratio", 1.0)
        if compliance < 1.0:
            result["composite_pre_extension_penalty"] = composite_norm
            # Penalty proportional to missing required extensions · max -10 pts
            penalty = round((1.0 - compliance) * 10, 2)
            result["extension_penalty"] = penalty
            result["composite"] = round(max(0.0, composite_norm - penalty), 2)
            result["grade"] = grade(result["composite"])
            result["grade_description"] = grade_description(result["grade"])

    return result
