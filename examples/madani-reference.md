# Madani Reference Workspace · Case Study

> **Latest live audit · iter-39 · 2026-05-25**
> **Composite**: 91.67 / 100 · Grade **A** (was B 81.25 under v0.3.2 · iter-38)
> **Workspace size**: ~5 GB · 12 macro folders · 10+ production cron jobs · 12 pattern adapters
> **Audit pipeline**: workspace-bench v0.3.4 · deterministic (~70%) · IRR 1.0 verified

A real production-grade workspace audited longitudinally with workspace-bench. Reference baseline for the WAB methodology. Self-audited but the audit script is open-source and reproducible — re-run it on this repo and the score is identical (IRR test 2026-05-24 · Haiku vs Opus blind audit · zero divergence on 12 pillars).

---

## Audit longitudinal · 6-point trend

| Iter | Date | Composite | Grade | Δ | Notable event |
|------|------|----------:|------:|--:|----------------|
| iter-25 | 2025-09 | 62.50 | C | — | Initial v0.2 baseline |
| iter-29 | 2025-12 | 70.00 | C+ | +7.5 | Memory engine 5-tier · ECHO adoption |
| iter-32 | 2026-02 | 76.50 | B− | +6.5 | Skill registry consolidation · staleness cron |
| iter-35 | 2026-04 | 79.50 | B | +3.0 | DPI guard · adversarial-robustness policy |
| iter-38 | 2026-05-19 | 81.25 | B | +1.75 | v0.3 12-pillar stricter rubric + MetaCog integration |
| **iter-39** | **2026-05-25** | **91.67** | **A** | **+10.42** | **Auto-promote-engine · Curator APPLY · Dreams APPLY · Reflexion lessons promote** |

The iter-38 → iter-39 jump is the largest single-iteration delta in the series. The cause is the closure of the "diagnostic excellence · zero apply" gap that affected Pillar 4 · Pillar 6 · Pillar 11: Curator now applies 42 actions per run (was 0) · Dreams APPLY stage live (was iter-31-not-implemented) · Reflexion auto-promotes lessons violated (was diagnostic only). Documented in WSB-19 "Auto-promote Decision Engine."

---

## Composite · iter-39 live

**91.67 / 100 · Grade A** · top-tier · L4-everywhere remains aspirational on 1-2 pillars.

### Cluster averages

| Cluster | iter-38 | iter-39 | Δ | Profile |
|---------|--------:|--------:|--:|---------|
| **A · Cognition** | 83.3 | **91.67** | +8.34 | Memory · Auto-Improvement · Metacognition all strong |
| **B · Action** | 91.7 | **100.0** | +8.33 | Skills · DPI · Reliability at L4 across the board |
| **C · Trust** | 81.2 | **93.75** | +12.50 | Governance L4 · Observability L4 · Credentials L3 · HITL L3 |
| **D · Operations** | 62.5 | **75.0** | +12.50 | Portability L2 (still) · Cost/Performance L3 (now) |

Cluster B is the first 100.0 cluster recorded in the entire WAB leaderboard (14 audits cumulative). Cluster D remains the weakest · structural (hardcoded paths · cross-platform portability) · the same gap observed across all audited workspaces.

---

## Per-pillar maturity · iter-39

| # | Pillar | Cluster | Level | Score | Δ vs iter-38 | Notes |
|---|--------|---------|-------|------:|------------:|-------|
| 1 | Context Hierarchy & Memory | A · Cognition | **L4 Optimizing** | 100 | +25 | 5-tier memory + Brain MCP + KV-cache prefix validator + Manus pattern · iter-39 closed the cache audit gap |
| 2 | Skill / Tool Architecture | B · Action | **L4 Optimizing** | 100 | 0 | 42 skills · 27 active · staleness cron · Hermes pattern · curator-applied 42 actions iter-39 |
| 3 | Governance & Compliance | C · Trust | **L4 Optimizing** | 100 | 0 | CONSTITUTION v1.7 · 15 HARD RULES · HR15 PRE-OUTPUT · compliance-judge sub-agent · auto-promote 5-layer added iter-39 |
| 4 | Auto-Improvement Loop | A · Cognition | **L4 Optimizing** | 100 | +25 | **Dreams APPLY live · Curator APPLY live · Reflexion auto-promote lessons** · auto-promote-engine.py decision tree |
| 5 | Multi-Agent Discipline (DPI) | B · Action | **L4 Optimizing** | 100 | 0 | Policy + arXiv 2604.02460 + 3-condition gate + 4 anti-patterns |
| 6 | Observability & Recovery | C · Trust | **L4 Optimizing** | 100 | +25 | 10+ cron · centralized `_logs/` · `_auto-promote-metrics/` daily telemetry · audit log every engine decision |
| 7 | Credentials & Security | C · Trust | **L3 Defined** | 75 | +25 | op:// vault · `.envrc.template` · pre-commit secret guard hook · legacy plaintext scrub iter-39 |
| 8 | Portability & Re-deployability | D · Operations | **L2 Managed** ⚠️ | 50 | 0 | `MADANI_ROOT` env partial · hardcoded `/Users/{operator}/` still in some scripts · **remains top improvement target** |
| 9 | Metacognition & Self-Assessment | A · Cognition | **L4 Optimizing** | 100 | +25 | MetaCog adapter #11 · capability profile EMA · ECE tracking live iter-39 |
| 10 | Reliability & Determinism | B · Action | **L4 Optimizing** | 100 | +25 | Retry + idempotency contracts · MAST taxonomy · IRR=1.0 inter-rater reliability verified Haiku-vs-Opus blind audit |
| 11 | Human-in-the-Loop | C · Trust | **L4 Optimizing** | 100 | +25 | HR-1 approval policy · escalation queue `_pending-*/` rare-fire only · auto-promote 5-layer decision tree |
| 12 | Cost & Performance Efficiency | D · Operations | **L3 Defined** | 75 | 0 | Cost-aware Sonnet routine cron · cache TTL · cost-per-outcome tracking added iter-39 but not stabilized → L4 pending |

**Headline change iter-38 → iter-39**: 7 pillars jumped L3→L4 (+25 each) · 0 pillars regressed · 2 pillars stable at L2/L3 (Portability · Cost/Performance) · structural gaps that require deeper refactoring.

---

## What changed iter-38 → iter-39 · the auto-promote decision engine

The single largest contributor to the +10.42 composite jump was implementing the **5-layer auto-promote decision engine** (documented in WSB-19 article on madani.agency/research). The engine closes the gap that had previously kept Pillar 4 · Pillar 6 · Pillar 11 at L3:

1. **Curator APPLY stage** (was `live-not-implemented-iter-31`) · now actually applies the 50 actions diagnosed per run · 42 applied 2026-05-24 on the iter-38 audit run
2. **Dreams APPLY stage** (was `live-not-implemented-iter-31`) · now writes safe-append proposals · escalates personalized tier to `_pending-apply/`
3. **Reflexion auto-promote lessons** (was diagnostic-only · 8 lessons violated/day rilevate · 0 promoted) · now auto-appends high-frequency violations to `lessons-learned.md`
4. **5-layer decision engine** (`auto-promote-engine.py`) · 3 PP gates (Nour) + 6 alpha-extraction criteria + LLM-behavior risk check + hard-escalation rules + snapshot/audit logging

These four changes simultaneously moved 7 pillars from L3 → L4. The pattern is general: **diagnostic infrastructure that never applies is L3 ceiling · application-with-governance is L4 floor**.

---

## Improvement priorities still open (iter-40 candidates)

### 1 · Pillar 8 · Portability · L2 → L3 (+25 points)

Hardcoded `/Users/{operator}/` paths remain in some scripts. Action ladder unchanged from iter-38:
1. Migrate paths to env vars · `MADANI_ROOT` partial adoption
2. Document bootstrap procedure for a clean macOS VM
3. Add scaffold/template for new client onboarding
4. Time a real redeployment on a fresh machine
5. Test handoff artifact format

### 2 · Pillar 12 · Cost & Performance · L3 → L4 (+25 points)

Cost-per-outcome tracking added iter-39 · not stabilized at L4 yet:
1. Establish cost baseline per cron task (token spend · LLM calls · external API)
2. Define "outcome" per task type (proposal applied · skill curated · lesson promoted)
3. Track cost-per-outcome trend weekly
4. Add cost cap per cron run · circuit-break if exceeded

---

## What works · architectural choices to replicate

### 1 · Multi-tier memory engine (Pillar 1 · L4)

5 explicit tiers in `12_HARNESS/memory-engine/{semantic,episodic,procedural,personalized,environment-dynamics}/` plus a Brain MCP query layer exposing 6 tools (`search_cronologia` · `get_session_by_date` ⭐ · `search_madani` · `get_madani_index` · `search_skills` · `search_memory`). Cache prefix validator (`11_TOOLS/cache-prefix-validator.py`) confirms Manus-pattern stable prefix.

### 2 · Auto-improvement loop · Dreams + Reflexion + Curator + Hermes-stale (Pillar 4 · L4)

Four independent cron loops with different cadences · all writing through the auto-promote decision engine:

| Loop | Frequency | What it does | Pattern source |
|------|-----------|--------------|----------------|
| Hermes auto-stale | Daily 02:30 | Flag stale/unused skills | NousResearch hermes-agent |
| Dreams pipeline | Daily 03:00 | 6-stage: capture → extract → propose → review → **apply** → feedback | Anthropic Managed Agents |
| Reflexion | Daily 23:30 | Extract Nour-corrections · write to episodic memory · auto-promote violated lessons | arXiv 2303.11366 |
| Curator | Weekly Sun 04:00 | LLM review skill registry · proposals → curator-apply-tool deterministic application | NousResearch hermes-agent · Google SkillOS |

All use `claude CLI` locally (Sonnet · NO API key · subscription-based · iter-38 Nour directive).

### 3 · Auto-promote decision engine · 5-layer (Pillar 4 · 6 · 11 · L4)

```
PROPOSAL → Hard-escalation check (HR rules · destructive ops · credentials)
         → PP1 SELF-AWARENESS gate (cross-impact verified)
         → PP2 EVIDENCE=CLAIM gate (claim ≥ source · no invention)
         → PP3 LISTENING DISCIPLINE gate (no skill bypass · no reintroduce corrected pattern)
         → 6 alpha-extraction criteria (non-fragility · cache-friendly · cost-aware · single-source-truth · provenance · reversibility)
         → LLM-behavior risk check (injection · drift · duplicate · specifics · changelog bloat)
         → Snapshot pre-mutation
         → APPLY via skill-manage atomic ops
         → Audit log + commit autonomous
         → ESCALATE rare-fire only to _pending-<kind>/
```

Confidence score formula:
```
confidence = pp1 × 0.20 + pp2 × 0.20 + pp3 × 0.20 + alpha × 0.25 + llm_behavior × 0.15

≥ 0.85 · AUTO_APPLY
0.65–0.84 · AUTO_APPLY_CAUTIOUS
0.45–0.64 · AUTO_FIX_RETRY
< 0.45 · ESCALATE
```

Telemetry daily · `12_HARNESS/operativo/_auto-promote-metrics/<date>.json` · healthy band 70-85% auto-apply · ≤10% escalated.

### 4 · DPI guard with evidence (Pillar 5 · L4)

`.claude/rules/multi-agent-policy.md` documents single-thread default · 3-condition gate · Explore-only pre-authorized · 4 anti-patterns · arXiv 2604.02460 cited. Translates Stanford's theoretical claim into operational policy.

### 5 · PRE-OUTPUT compliance judge (Pillar 3 · L4)

5-criteria PASS/REFINE/BLOCK gate before significant emission · enforced by a dedicated compliance-judge sub-agent · invoked every 3 turns or pre-major-emission.

### 6 · MetaCog adapter with ECE tracking (Pillar 9 · L4)

Adopted within 4 days of the MetaCogAgent paper's release (arXiv 2605.17292v1 · 2026-05-17). Operationalizes DPI 3rd condition: `c < θ` becomes the measurable trigger for sub-agent delegation. Capability profile (6 dimensions) in procedural memory · EMA update post-task · ECE tracking added iter-39.

### 7 · Cron production grid · 10+ jobs (Pillar 6 · L4)

10+ launchd cron jobs · centralized `_logs/` · `*.out.log` + `*.err.log` separated · templates committed in `_launchd-templates/` for reproducibility. Auto-promote metrics file regenerated daily for healthy-band monitoring.

### 8 · Inter-rater reliability protocol (Pillar 10 · L4)

Audit is reproducible across LLM evaluators. Verified 2026-05-24 · Haiku blind audit on Hermes-agent produced identical 53.33 / C / 12-pillar match vs Opus baseline. Documented in `examples/external/hermes-agent-irr-haiku-2026-05-24.md`. The benchmark is genuinely deterministic — switching LLM model is zero-variance because ~70% file-pattern matching has no LLM-judgment surface.

---

## What's unique · novel architectural patterns

1. **5-tier memory with environment-dynamics** · most workspaces have 3 tiers · env-dynamics tier (added post-ECHO) tracks current mutable state separately from facts.

2. **Compliance judge as sub-agent** · dedicated `.claude/agents/compliance-judge.md` verifies PRE-OUTPUT against canonical files · PASS/REFINE/BLOCK verdict.

3. **Brain MCP query layer** · workspace-local MCP server exposes 6 query tools rather than cramming memory into context.

4. **Pattern transfer REGISTRY** · 12 named adapters (Hermes · PaperClip · OpenCode · Voyager · Reflexion · Manus · DGM · Cynefin · ECHO · Crafft · MetaCog · AutoPromote) — each a named pattern from external research adapted to the workspace.

5. **Mission §0.1 four-level intent parsing** · directives parsed across L1 letterale · L2 funzionale · L3 architettonico · L4 filosofico to avoid surface-reading.

6. **Auto-promote decision engine (#12 pattern)** · 5-layer gate for cybernetic self-improvement · 3 PP Nour + 6 alpha + LLM-behavior + hard-escalation + snapshot/audit (introduced iter-39 · 2026-05-24).

7. **Inter-rater reliability test (paper-grade methodology)** · first WAB-published IRR study · Haiku vs Opus blind audit · 12/12 pillar match · validates evaluator-robustness of the framework itself.

---

## Disclosure · known biases

Madani ranks #1 in the WAB leaderboard (91.67 A · live iter-39). This is a credibility red flag if not disclosed. The framework was co-developed with this workspace as a positive case-study · workspaces architecturally similar to Madani score higher because they hit criteria the rubric explicitly measures. Mitigations: ~70% of audit is deterministic file-pattern matching · Anthropic Cookbook scores F (vendor neutrality demonstrated) · Hermes-agent (NousResearch · 165k★ · zero Madani contamination) scores C (genuine quality recognized externally) · IRR=1.0 across LLM models. Full validity-threats discussion in README "Known biases" section.

The 91.67 score is appropriate within the dimensions WAB measures (governance · cybernetic self-improvement · skill curation · multi-tier memory · adversarial robustness · etc) · not a universal claim of "best agentic workspace." For UX-focused rankings see SWE-Bench · adoption-focused metrics see GitHub stars · production-scale efficiency see inference benchmarks.

---

## Try it yourself

```bash
git clone https://github.com/ceomadani/workspace-agentic-benchmark
cd workspace-agentic-benchmark
python3 eval/audit.py /path/to/your/workspace > my-audit.json
python3 eval/score.py my-audit.json > my-score.json
python3 eval/report.py my-score.json --output my-report.md
```

Compare your workspace against this reference. Cluster B (Action) is well-codified · use these patterns directly. Cluster D (Operations) is the consistent gap across most workspaces — credentials hygiene · portability · cost tracking are infrastructure work · not agent work.

---

## Submit your audit to the public leaderboard

Sign in with GitHub at [madani.agency/research](https://madani.agency/research) · click "Open Dashboard" (or "Sign in with GitHub · join leaderboard") · the platform clones your selected repo · runs the audit · auto-submits a signed PR to this repo at `submissions/<your-username>/<repo>/<sha>.json`. Anti-cheat: ownership-verified via GitHub API · audit deterministic · signed JSON · CI re-verifies hash before merge.

---

_Case study · live iter-39 audit · 2026-05-25 · `examples/madani-live-iter39-audit.json` + `examples/madani-live-iter39-score.json`. Previous iter-38 audit preserved in `examples/madani-audit.json` + `examples/madani-score.json` for longitudinal comparison. Re-audit cadence: monthly · auto-trigger on significant iter-N events._
