# Reference Workspace · Case Study

> **Score**: 81.25 / 100 · Grade **B** (was A under v0.2 · L0-L4 stricter)
> **Audited**: 2026-05-19 (iter-38 · post-MetaCog integration)
> **Workspace size**: ~5 GB · 12 macro folders · 7 production cron jobs · 11 pattern adapters

A real production-grade workspace audited with v0.3 (12 pillars · L0-L4 maturity · weighted composite). Use as a comparison baseline for your own workspace.

---

## Composite

**81.25 / 100 · Grade B** · Solid · 1-2 pillars need hardening before scale.

### Cluster averages

| Cluster | Avg | Profile |
|---------|----:|---------|
| **A · Cognition** | 83.3 / 100 | Memory · Auto-Improvement · Metacognition all strong |
| **B · Action** | 91.7 / 100 | Skills + DPI + Reliability · strongest cluster |
| **C · Trust** | 81.2 / 100 | Governance + Observability at L4 · dragged by credentials gap |
| **D · Operations** | 62.5 / 100 | Weakest cluster · Portability + Cost/Performance both need work |

---

## Per-pillar maturity

| # | Pillar | Cluster | Level | Score | Notes |
|---|--------|---------|-------|------:|-------|
| 1 | Context Hierarchy & Memory | A · Cognition | **L3 Defined** | 75 | 5-tier memory · Brain MCP query · Reflexion daily. Cache prefix audit not yet formalized → L4. |
| 2 | Skill / Tool Architecture | B · Action | **L4 Optimizing** | 100 | 42 skills · 27 active · staleness cron · ROSTER curated · 30%+ deterministic. |
| 3 | Governance & Compliance | C · Trust | **L4 Optimizing** | 100 | CONSTITUTION v1.7 · 15 HARD RULES · HR15 PRE-OUTPUT · compliance-judge sub-agent. |
| 4 | Auto-Improvement Loop | A · Cognition | **L4 Optimizing** | 100 | Dreams + Reflexion + A-MAC · Sonnet cost-aware · 2-stage review. |
| 5 | Multi-Agent Discipline (DPI) | B · Action | **L4 Optimizing** | 100 | Policy + arXiv 2604.02460 + 3-condition gate + 4 anti-patterns. |
| 6 | Observability & Recovery | C · Trust | **L4 Optimizing** | 100 | 7 cron · centralized `_logs/` · M08 6-state · stderr split. |
| 7 | Credentials & Security | C · Trust | **L2 Managed** ⚠️ | 50 | Vault integrated but legacy plaintext stragglers + rotation undocumented. **Top improvement priority.** |
| 8 | Portability & Re-deployability | D · Operations | **L2 Managed** ⚠️ | 50 | 8 clients isolated but hardcoded `/Users/...` paths still in scripts. **Second improvement priority.** |
| 9 | Metacognition & Self-Assessment | A · Cognition | **L3 Defined** | 75 | MetaCog adapter #11 · capability profile · EMA. ECE tracking pending → L4. |
| 10 | Reliability & Determinism | B · Action | **L3 Defined** | 75 | Retry + idempotency documented · MAST taxonomy referenced. Pass@k not yet measured → L4. |
| 11 | Human-in-the-Loop | C · Trust | **L3 Defined** | 75 | HR-1 approval policy + escalation criteria documented. Approval friction not measured → L4. |
| 12 | Cost & Performance Efficiency | D · Operations | **L3 Defined** | 75 | Cost-aware Sonnet routine cron · cache TTL doc'd. Cost-per-outcome tracking pending → L4. |

---

## Top 3 improvement priorities (largest impact)

### 1. Pillar 7 · Credentials & Security · L2 → L3 (+25 points)

The audit flagged legacy plaintext secret patterns in archive folders. Action ladder:
1. Rotate any keys flagged as real (LLM API · image generation · webhook secrets)
2. Replace hardcoded with `op://{vault}/{service}/api_key` runtime resolution
3. Add pre-commit hook to block plaintext patterns (TruffleHog / gitleaks)
4. Document quarterly rotation cadence
5. Run git-history scrub (BFG / `filter-branch`) for already-committed keys

### 2. Pillar 8 · Portability · L2 → L3 (+25 points)

Hardcoded `/Users/{operator}/` paths remain in scripts. Action ladder:
1. Move paths to env vars (`MADANI_ROOT`, etc. — already partially adopted)
2. Document bootstrap procedure for a clean macOS VM
3. Add scaffold/template for new client onboarding
4. Time a real redeployment on a fresh machine
5. Test handoff artifact format

### 3. Pillar 1 · Context Memory · L3 → L4 (+25 points)

Smaller gap but high-leverage: KV-cache awareness documented but not formally audited.
1. Add a KV-cache prefix stability test (compare prompts across sessions)
2. Measure cache hit rate on hot paths · target ≥ 80%
3. Document cross-tier interaction (promotion / demotion / conflict resolution)
4. Track memory retrieval precision/recall over a representative query set

---

## What works · architectural choices to replicate

### 1. Multi-tier memory engine (Pillar 1 · L3)

5 explicit tiers in `memory/{semantic,episodic,procedural,personalized,env-dynamics}/` plus a Brain MCP query layer exposing 6 tools (`search_cronologia` · `get_session_by_date` ⭐ · `search_madani` · `get_madani_index` · `search_skills` · `search_memory`).

### 2. Auto-improvement triad: Dreams + Reflexion + Hermes (Pillar 4 · L4)

Three independent cron loops with different cadences:

| Loop | Frequency | What it does | Pattern source |
|------|-----------|--------------|----------------|
| Hermes auto-stale | Daily 02:30 | Flag stale/unused skills | NousResearch hermes-agent |
| Dreams pipeline | Daily 03:00 | 6-stage: capture → extract → propose → review → apply → feedback | Anthropic Managed Agents |
| Reflexion | Daily 23:30 | Extract Nour-corrections · write to episodic memory | arXiv 2303.11366 |

All use `claude CLI` locally (Sonnet · NO API key · subscription-based).

### 3. DPI guard with evidence (Pillar 5 · L4)

`.claude/rules/multi-agent-policy.md` documents single-thread default · 3-condition gate · Explore-only pre-authorized · 4 anti-patterns · arXiv 2604.02460 cited. Translates Stanford's theoretical claim into operational policy.

### 4. PRE-OUTPUT compliance judge (Pillar 3 · L4)

5-criteria PASS/REFINE/BLOCK gate before significant emission · enforced by a dedicated compliance-judge sub-agent · invoked every 3 turns or pre-major-emission.

### 5. MetaCog adapter (Pillar 9 · L3)

Adopted within 4 days of the MetaCogAgent paper's release (arXiv 2605.17292v1 · May 17, 2026). Operationalizes DPI 3rd condition: `c < θ` becomes the measurable trigger for sub-agent delegation. Capability profile (6 dimensions) in procedural memory · EMA update post-task.

### 6. Cron production grid (Pillar 6 · L4)

7 launchd cron jobs · centralized `_logs/` · `*.out.log` + `*.err.log` separated · templates committed in `_launchd-templates/` for reproducibility.

---

## What's unique · novel architectural patterns

1. **5-tier memory with environment-dynamics** · most workspaces have 3 tiers · env-dynamics tier (added post-ECHO) tracks current mutable state separately from facts.

2. **Compliance judge as sub-agent** · dedicated `.claude/agents/compliance-judge.md` verifies PRE-OUTPUT against canonical files · PASS/REFINE/BLOCK verdict.

3. **Brain MCP query layer** · workspace-local MCP server exposes 6 query tools rather than cramming memory into context.

4. **Pattern transfer REGISTRY** · 11 named adapters (Hermes / PaperClip / OpenCode / Voyager / Reflexion / Manus / DGM / Cynefin / ECHO / Crafft / MetaCog) — each a named pattern from external research adapted to the workspace.

5. **Mission §0.1 four-level intent parsing** · directives parsed across L1 letterale · L2 funzionale · L3 architettonico · L4 filosofico to avoid surface-reading.

6. **MetaCog adapter (#11)** · first known production integration of MetaCogAgent paper (arXiv 2605.17292) · 4-day turnaround from publication to deployment.

---

## Try it yourself

```bash
cd workspace-agentic-benchmark
python3 eval/audit.py /path/to/your/workspace > my-audit.json
python3 eval/score.py my-audit.json > my-score.json
python3 eval/report.py my-score.json --output my-report.md
```

Compare your workspace against this reference. Cluster B (Action) is well-codified · use these patterns directly. Cluster D (Operations) is the consistent gap across most workspaces — credentials hygiene and portability are infrastructure work, not agent work.

---

_Case study v0.3 · 2026-05-19 · audit and score files in `examples/madani-audit.json` and `examples/madani-score.json`. Re-audit recommended monthly to track maturity progression._
