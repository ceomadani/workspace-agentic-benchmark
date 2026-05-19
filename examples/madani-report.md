# Workspace Agentic Benchmark · Report

**Workspace**: `/Users/nourmatine/madani`
**Scored at**: 2026-05-19T22:36:10.298973

---

## Executive Summary

**Total**: **70.5 / 80** · Grade **A**

**Production-grade** · forward-deployable · ready for FDE engagements.

### Pillar overview

| Pillar | Score | Bar |
|--------|-------|-----|
| Context Hierarchy & Memory | 8.5 / 10 | `█████████████████░░░` |
| Skill / Tool Architecture | 10.0 / 10 | `████████████████████` |
| Governance & Compliance | 9.0 / 10 | `██████████████████░░` |
| Auto-Improvement Loop | 9.0 / 10 | `██████████████████░░` |
| Multi-Agent Discipline (DPI) | 10.0 / 10 | `████████████████████` |
| Observability & Recovery | 9.0 / 10 | `██████████████████░░` |
| Credentials & Security | 6.0 / 10 | `████████████░░░░░░░░` |
| Portability & Re-deployability | 9.0 / 10 | `██████████████████░░` |

---

## Per-pillar deep-dive

### Context Hierarchy & Memory

**Score**: 8.5 / 10 · `█████████████████░░░`

| Criterion | Pass |
|-----------|------|
| `multi_tier_3plus` | ✅ (1.0) |
| `retrieval_policy_explicit` | ✅ (1.0) |
| `decay_policy_explicit` | ✅ (1.0) |
| `index_file_loads_auto` | ❌ (0.0) |
| `structured_frontmatter` | 🟡 (0.5) |
| `cross_links_graph` | ✅ (1.0) |
| `episodic_from_reflection` | ✅ (1.0) |
| `queryable_storage` | ✅ (1.0) |
| `kv_cache_awareness` | ✅ (1.0) |
| `documented_retrieval_failure_mode` | ✅ (1.0) |

**To improve**:
- Address `index_file_loads_auto` · see `pillars/01-*.md` for the rubric.

### Skill / Tool Architecture

**Score**: 10.0 / 10 · `████████████████████`

| Criterion | Pass |
|-----------|------|
| `skills_dedicated_location` | ✅ (1.0) |
| `self_contained_units` | ✅ (1.0) |
| `frontmatter_present` | ✅ (1.0) |
| `auto_trigger_mechanism` | ✅ (1.0) |
| `staleness_detection` | ✅ (1.0) |
| `determinism_preferred` | ✅ (1.0) |
| `roster_curation` | ✅ (1.0) |
| `changelog_versioning` | ✅ (1.0) |
| `no_grab_bag_megaskills` | ✅ (1.0) |
| `cross_referenced` | ✅ (1.0) |

### Governance & Compliance

**Score**: 9.0 / 10 · `██████████████████░░`

| Criterion | Pass |
|-----------|------|
| `constitution_exists` | ✅ (1.0) |
| `hard_rules_enumerated` | ✅ (1.0) |
| `pre_output_check` | ✅ (1.0) |
| `external_action_gate` | ✅ (1.0) |
| `destructive_action_gate` | ✅ (1.0) |
| `constitution_versioned` | ✅ (1.0) |
| `compliance_judge_exists` | ✅ (1.0) |
| `evidence_linked_rules` | ❌ (0.0) |
| `escalation_path_documented` | ✅ (1.0) |
| `layered_rules` | ✅ (1.0) |

**To improve**:
- Address `evidence_linked_rules` · see `pillars/03-*.md` for the rubric.

### Auto-Improvement Loop

**Score**: 9.0 / 10 · `██████████████████░░`

| Criterion | Pass |
|-----------|------|
| `session_capture` | ✅ (1.0) |
| `reflection_cron` | ✅ (1.0) |
| `reflection_writes_episodic` | ✅ (1.0) |
| `improvement_proposal_system` | ✅ (1.0) |
| `scoring_rubric_for_proposals` | ✅ (1.0) |
| `two_stage_review` | ❌ (0.0) |
| `apply_log_exists` | ✅ (1.0) |
| `feedback_loop_measured` | ✅ (1.0) |
| `cron_driven` | ✅ (1.0) |
| `cost_aware_cheaper_model` | ✅ (1.0) |

**To improve**:
- Address `two_stage_review` · see `pillars/04-*.md` for the rubric.

### Multi-Agent Discipline (DPI)

**Score**: 10.0 / 10 · `████████████████████`

| Criterion | Pass |
|-----------|------|
| `single_thread_default_documented` | ✅ (1.0) |
| `multi_agent_policy_file` | ✅ (1.0) |
| `pre_spawn_gate` | ✅ (1.0) |
| `explore_only_preauthorized` | ✅ (1.0) |
| `no_recursive_subagents` | ✅ (1.0) |
| `self_contained_subagent_prompts` | ✅ (1.0) |
| `evidence_cited` | ✅ (1.0) |
| `budget_guard` | ✅ (1.0) |
| `anti_pattern_list` | ✅ (1.0) |
| `logged_invocations` | ✅ (1.0) |

### Observability & Recovery

**Score**: 9.0 / 10 · `██████████████████░░`

| Criterion | Pass |
|-----------|------|
| `centralized_logs` | ✅ (1.0) |
| `liveness_watchdog` | ✅ (1.0) |
| `aggregate_health_report` | ✅ (1.0) |
| `drift_detector` | ❌ (0.0) |
| `explicit_state_machine` | ✅ (1.0) |
| `stuck_task_detection` | ✅ (1.0) |
| `cron_success_tracked` | ✅ (1.0) |
| `stderr_separated` | ✅ (1.0) |
| `log_rotation_policy` | ✅ (1.0) |
| `recovery_procedure_doc` | ✅ (1.0) |

**To improve**:
- Address `drift_detector` · see `pillars/06-*.md` for the rubric.

### Credentials & Security

**Score**: 6.0 / 10 · `████████████░░░░░░░░`

| Criterion | Pass |
|-----------|------|
| `zero_plaintext_secrets` | ❌ (0.0) |
| `vault_integrated` | ✅ (1.0) |
| `runtime_resolution` | ✅ (1.0) |
| `env_in_gitignore` | ✅ (1.0) |
| `external_action_approval` | ✅ (1.0) |
| `audit_log` | ✅ (1.0) |
| `rotation_documented` | ❌ (0.0) |
| `no_credentials_in_history` | ❌ (0.0) |
| `no_credentials_in_urls` | ❌ (0.0) |
| `per_environment_separation` | ✅ (1.0) |

**To improve**:
- Address `zero_plaintext_secrets` · see `pillars/07-*.md` for the rubric.
- Address `rotation_documented` · see `pillars/07-*.md` for the rubric.
- Address `no_credentials_in_history` · see `pillars/07-*.md` for the rubric.

### Portability & Re-deployability

**Score**: 9.0 / 10 · `██████████████████░░`

| Criterion | Pass |
|-----------|------|
| `bootstrap_doc_exists` | ✅ (1.0) |
| `skills_client_agnostic_or_tagged` | ✅ (1.0) |
| `credentials_per_engagement_isolated` | ✅ (1.0) |
| `per_environment_separation` | ✅ (1.0) |
| `state_externalized` | ✅ (1.0) |
| `template_scaffold_exists` | ✅ (1.0) |
| `memory_isolation_per_engagement` | ✅ (1.0) |
| `handoff_artifact_format` | ✅ (1.0) |
| `low_hardcoded_paths` | ❌ (0.0) |
| `multiple_deployments_evidence` | ✅ (1.0) |

**To improve**:
- Address `low_hardcoded_paths` · see `pillars/08-*.md` for the rubric.

---

## Next steps · ordered by impact

- **Credentials & Security** · gap 4.0 pts · see `pillars/07-*.md` for the improvement ladder.
- **Context Hierarchy & Memory** · gap 1.5 pts · see `pillars/01-*.md` for the improvement ladder.
- **Governance & Compliance** · gap 1.0 pts · see `pillars/03-*.md` for the improvement ladder.

---

_Generated by workspace-agentic-benchmark/report.py v0.1.0 · 2026-05-19T22:36:10.343311_
