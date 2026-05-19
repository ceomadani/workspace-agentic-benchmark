# Madani Workspace · Reference Case Study

> **Score**: 79.5 / 90 · Grade **A** · production-grade · forward-deployable
> **Audited**: 2026-05-19 (iter-38 · post-MetaCog integration)
> **Workspace size**: ~5 GB · 12 macro folders · 7 production cron jobs · 11 pattern adapters

This is the first reference workspace audited with this framework. Madani is a portfolio operation (~50M EUR aggregate revenue) running an iterated agentic system since iter-1 (Apr 2026). Use it as a high-score case study to compare against your own.

---

## Score breakdown

| Pillar | Score | Grade | Why |
|--------|-------|-------|-----|
| 1 · Context Hierarchy & Memory | 8.5 / 10 | A | 5-tier memory engine · Brain MCP query layer · Reflexion daily reflection cron. Loses 0.5 for cache prefix audit not formalized. |
| 2 · Skill / Tool Architecture | 10 / 10 | A | 42 skills (27 active) · ROSTER curated · Hermes staleness cron daily 02:30 · 30%+ deterministic tools · cross-linked. |
| 3 · Governance & Compliance | 9 / 10 | A | CONSTITUTION v1.7 with 15 HARD RULES · HR15 PRE-OUTPUT 5-criteria · compliance-judge sub-agent · evidence-linked. |
| 4 · Auto-Improvement Loop | 9 / 10 | A | Dreams 6-stage pipeline · Reflexion cron 23:30 · A-MAC 6-factor scoring · Sonnet (cost-aware) · two-stage review. |
| 5 · Multi-Agent Discipline (DPI) | 10 / 10 | A | multi-agent-policy.md · single-thread default · arXiv 2604.02460 cited · 3-condition gate · 4 anti-patterns documented. |
| 6 · Observability & Recovery | 9 / 10 | A | Centralized `_logs/` · liveness-watchdog hourly · aggregate-report daily 09:00 · M08 6-state lifecycle · stderr separated. |
| 7 · Credentials & Security | 6 / 10 | C ⚠️ | Vault integrated (1Password op://) but legacy plaintext keys found in archive paths. Rotation undocumented. |
| 8 · Portability & Re-deployability | 9 / 10 | A | 8 clients isolated · per-engagement vault · handoff format documented · low hardcoded paths (mostly in scripts). |
| 9 · Metacognition & Self-Assessment | 9 / 10 | A | MCU runner `metacog-self-assess.py` · capability profile 6 dims · composite formula · conflict detection · EMA update · DPI integrated. Loses 1.0 for ECE not yet tracked over time. |

**Total**: 79.5 / 90 (88%)

---

## What works · architectural choices to replicate

### 1. Multi-tier memory engine (Pillar 1 · 8.5/10)

Madani separates memory into 5 explicit tiers:

```
12_HARNESS/memory-engine/
├── semantic/        ← facts about world
├── episodic/        ← past sessions · grown by Reflexion cron
├── procedural/      ← skills · runbooks
├── personalized/    ← Nour preferences · feedback patterns
└── env-dynamics/    ← live state of mutable env (added post-ECHO iter-35)
```

Plus a **Brain MCP query layer** (workspace-local `.mcp.json`) exposing 6 tools to agents:
- `search_cronologia`
- `get_session_by_date` ⭐ (Nour-critical)
- `search_madani`
- `get_madani_index`
- `search_skills`
- `search_memory`

**Replicate by**:
1. Create separate folders per tier
2. Write `MEMORY.md` index that auto-loads
3. Standard frontmatter (`name`, `description`, `type`, `last_updated`)
4. Add a query layer (MCP server or simple grep wrapper)

### 2. Auto-improvement triad: Dreams + Reflexion + Hermes (Pillar 4 · 9/10)

Three independent loops with different cadences:

| Loop | Frequency | What it does | Pattern source |
|------|-----------|--------------|----------------|
| **Hermes auto-stale** | Daily 02:30 CEST | Flag stale/unused skills | NousResearch hermes-agent |
| **Dreams pipeline** | Daily 03:00 CEST | 6-stage: capture → extract → propose → review → apply → feedback | Anthropic Managed Agents |
| **Reflexion** | Daily 23:30 CEST | Extract Nour-corrections from session JSONL · write to episodic memory | arXiv 2303.11366 |

All use `claude CLI` locally (Sonnet · NO API key · subscription-based) for cost control.

**Critical design choice**: `claude -p --model sonnet --dangerously-skip-permissions` instead of Anthropic API. This costs $0 marginal (already paying for subscription) and avoids credential sprawl.

### 3. DPI guard with evidence (Pillar 5 · 10/10)

`.claude/rules/multi-agent-policy.md` documents:
- Default: 1 thread
- Multi-agent requires 3 conditions:
  1. Primary context already >50KB consumed
  2. Budget estimate ≥2× single-thread
  3. Nour explicit approval (production)
- Explore-only sub-agent pre-authorized for read-only audits
- 4 anti-patterns enumerated
- arXiv 2604.02460 (Stanford DPI) cited as evidence

This translates Stanford's theoretical claim into operational policy.

### 4. PRE-OUTPUT compliance judge (Pillar 3 · 9/10)

HR15 (HARD RULE 15) requires a 5-criteria PRE-OUTPUT check before significant emission:
1. Mission alignment (does this serve the documented intent?)
2. Input verbatim Nour (do we have the exact request?)
3. Architectural coherence (does this fit the documented system?)
4. Verdict possible: PASS / REFINE / BLOCK
5. Compliance judge sub-agent invoked every 3 turns or pre-major-emission

Most other workspaces have implicit alignment · this makes it explicit.

### 5. Cron production grid (Pillar 6 · 9/10)

7 launchd cron jobs (production):

| Cron | Schedule | Tool |
|------|----------|------|
| `com.madani.hermes-stale` | Daily 02:30 | `skill-staleness-detector.py` |
| `com.madani.dreams` | Daily 03:00 | `dreams-runner.py --model sonnet` |
| `com.madani.aggregate-report` | Daily 09:00 | `aggregate-report.py` |
| `com.madani.liveness-watchdog` | Hourly | `liveness-watchdog.py --scan` |
| `com.madani.reflexion` | Daily 23:30 | `reflexion-runner.py --model sonnet` |
| `com.madani.transcript-summary` | Daily | M3 daily standup PDF |
| `com.madani.voice-caller.idle-watcher` | Service | GPU cost saving |

All logs in `12_HARNESS/operativo/_logs/{name}.{out,err}.log`. Templates committed in `_launchd-templates/` for reproducibility.

---

## What needs improvement · gaps documented

### Pillar 7 · Credentials & Security · 6/10 (only gap below B)

The audit flagged plaintext secret patterns in legacy scripts and false-positive matches on documentation strings. Lesson for any workspace at scale: even strong vault adoption (1Password `op://`) doesn't retroactively clean up legacy paths.

**Action items** (post-audit):
1. Rotate any keys flagged as real (LLM API · image generation · webhook secrets)
2. Replace hardcoded with `op://{Vault}/{Service}/api_key` runtime resolution
3. Add pre-commit hook to block plaintext patterns (TruffleHog / gitleaks)
4. Document secret rotation cadence (recommended quarterly)
5. Run git-history scrub (BFG / `filter-branch`) for already-committed keys
6. Triage false positives — the `sk-*` prefix is too broad and matches legitimate documentation strings; the audit script should be improved with stricter regex (e.g., require key entropy threshold)

### Pillar 1 · Context Hierarchy & Memory · 8.5/10 (small gap)

KV-cache awareness is documented but not formally audited. Action: add a KV-cache prefix stability test (compare prompts across sessions for variable prefix).

### Pillar 8 · Portability · 9/10 (small gap)

Bootstrap procedure exists (`ONBOARDING.md`) but **time-to-bootstrap not measured**. Action: time the next FDE engagement onboarding as a benchmark · or run a synthetic test on a clean macOS VM.

---

## What's unique about this workspace · novel architectural patterns

1. **5-tier memory with environment-dynamics**: most workspaces have 3 tiers (semantic + episodic + procedural). The env-dynamics tier (added iter-35 post-ECHO) tracks the *current mutable state* of the environment separately from facts about it. Catches "the migration ran" → distinct from "this is what migrations are."

2. **Compliance judge as sub-agent**: instead of a check function, a dedicated `.claude/agents/compliance-judge.md` sub-agent verifies PRE-OUTPUT against canonical Madani files. Verdict: PASS / REFINE / BLOCK. Triggered every 3 turns or pre-major-emission.

3. **Brain MCP query layer**: instead of cramming all memory into context, a workspace-local MCP server (`.mcp.json` workspace-scoped) exposes 6 query tools. `get_session_by_date` ⭐ is the most-used (Nour-flagged critical).

4. **Pattern transfer REGISTRY**: 10 named adapters (Hermes / PaperClip / OpenCode / Voyager / Reflexion / Manus / DGM / Cynefin / ECHO / Crafft) — each is a "named pattern" from external research adapted to Madani. The REGISTRY tracks which patterns are active and what they're inspired by.

5. **Mission V2 §0.1 four-level intent** (L1 letterale · L2 funzionale · L3 architettonico · L4 filosofico): when the agent receives a directive, it parses the four levels to avoid surface-reading. This is unique terminology not documented elsewhere.

6. **MetaCogAgent adapter (#11 REGISTRY)** — adopted within 4 days of the paper's release (arXiv 2605.17292v1 · May 17, 2026). Provides operational evidence for the DPI 3rd condition: `c < θ` becomes the measurable trigger for sub-agent delegation, replacing subjective judgment with calibrated composite confidence. Capability profile in procedural memory tier updated via EMA from outcome signal. ECE tracking pending (target ≤ 0.10).

---

## Try it yourself

```bash
cd workspace-agentic-benchmark
python3 eval/audit.py /Users/nourmatine/madani > my-audit.json
python3 eval/score.py my-audit.json > my-score.json
python3 eval/report.py my-score.json --output my-report.md
```

Compare your workspace against this reference. Pillars 5 (DPI) and 2 (Skills) are well-codified · use Madani's patterns directly. Pillar 7 (Credentials) is a cautionary tale — even high-scoring workspaces leak when they grow fast.

---

_Case study v0.1 · 2026-05-19 · audit and score files in `examples/madani-audit.json` and `examples/madani-score.json`._
