# Extension 10 · Index Density & Semantic Coverage

> The vehicle through which α is delivered to the agent. Without high-density indices, all other workspace investments compound near zero.

---

## The principle

An agent's effective context is **not** the size of the model's window — it's the size of the **fraction of the workspace the agent can locate in <1 KB of injected hints**. Indices are how a workspace bridges arbitrarily large knowledge bases into bounded context.

```
effective_context_size = window_size + Σ (index_pointer_recall × downstream_byte_fetch)
```

An index is not "a list of files." An index is a **compressed semantic map**: given a query intent, the index produces a small set of high-precision pointers to the rest of the workspace.

---

## What counts as an index

| Index type | Common naming convention | What it answers |
|-----------|--------------------------|------------------|
| **Structural** | `INDEX.md` per folder · root-level `00_*.md` | "What is in this folder · what role · what to read first" |
| **Entity registry** | `ENTITY-REGISTRY.md` · `AGENTS.md` · `llms.txt` | "Which daemons · cron jobs · sub-agents · tools exist live and where" |
| **Skill / capability catalog** | `skills/INDEX.md` · `capabilities.json` · `llms.txt` | "Which capabilities are available and how to invoke them" |
| **Memory manifest** | `memory/_MANIFEST.md` · `MEMORY.md` · `KNOWLEDGE_BASE.md` | "Which facts/rules/events/prefs are stored and where" |
| **Pattern catalog** | `patterns/INDEX.md` · `pattern-adapters/REGISTRY.md` | "Which research patterns have adapters and what they cover" |
| **API/Credentials registry** | `API-MASTER.md` · `integrations/INDEX.md` · `.env.template` | "Which integrations are wired and where the credentials live" |
| **Configuration/Hooks registry** | `hooks/INDEX.md` · `.claude/settings.json` · `SETTINGS.md` | "Which hooks are active and where they're configured" |
| **Cross-link spine** | links inside any file that connect to other indices | "How to navigate from here to anything else" |

A workspace is **well-indexed** when every entity it depends on appears in at least one of these indices, and the indices cross-reference each other to form a navigable graph.

---

## Measurement

The benchmark introduces four explicit metrics:

### 1 · `index_coverage_ratio` (0-1)

```
indexed_entities / total_governance_entities
```

Where governance entities include: daemons (launchd · systemd) · cron jobs · sub-agents · custom skills · custom tools · hard rules · pattern adapters · external API integrations · MCP servers.

**Target**: ≥ 0.95 for L4 maturity.

### 2 · `index_info_density` (bytes useful / bytes total)

For each index file, measure:

```
density = byte_of_actionable_pointers / byte_total
```

Where "actionable pointers" = file paths, schedule strings, role descriptions, status flags. Filler (prose explanations, history) is not actionable.

**Target**: ≥ 0.6 for L4 (most of an index is signal, not framing).

### 3 · `index_recency_lag` (days)

Median age of an index file vs the entities it references. Stale indices give the agent confidently-wrong directions.

**Target**: ≤ 7 days for L4 (auto-updated weekly or on relevant change).

### 4 · `index_semantic_queryability` (binary per entity)

For a sample of 10 entity-recall tasks ("where is Hermes? · what does paperclip pattern do? · which cron runs at 15:55?"), can the agent answer in one indexed lookup (no grep)?

**Target**: 10/10 for L4.

---

## Maturity levels for Index Density

| Level | Profile |
|-------|---------|
| **L0 · Absent** | No indices. Agent must full-text search the workspace for every entity recall. |
| **L1 · Initial** | A README at the root · no per-folder indices · no entity registry. |
| **L2 · Managed** | INDEX.md per folder · manually maintained · drift to entities frequent. |
| **L3 · Defined** | Indices auto-updated by tooling on change events · entity registry exists · cross-linked. |
| **L4 · Optimizing** | Indices auto-updated · entity registry semantically queryable · staleness alerts · density metrics tracked over time · gaps trigger auto-issue. |

---

## Why this is a first principle (and not "just a P01 sub-criterion")

It's separable from Context Hierarchy & Memory (P01) for three reasons:

1. **Different update cadence.** Indices change daily/weekly · memory tiers compact monthly/quarterly · different operational disciplines.

2. **Different failure mode.** P01 fails by "wrong content surfaced into context"; Index Density fails by "agent can't find what already exists." A workspace can have a great memory engine and bad indices · the agent then has knowledge it can't reach.

3. **Different optimization lever.** P01 is fixed by content engineering; Index Density is fixed by structural engineering. Distinct skill sets.

This is why iter-2 elevates it to a top-level extension instead of folding it into P01.

---

## Operational consequences

### Every refactor must update the indices

A refactor that moves files without updating the indices is **architectural debt**, not progress. A generic failure mode (observed in live audits):

- Refactor renames or moves a folder `~/old-name/` → `~/new-location/`
- The repo's own indices (`INDEX.md` · `AGENTS.md`) get updated as part of the diff
- **But the OS-level scheduler config (launchd plist · systemd unit · crontab entry) still references the old path** — outside the repo's awareness
- Result: the job fails silently for hours/days until manual discovery
- Root cause: the OS scheduler registry is an index that needed sync · the refactor didn't treat it as one

The pattern emerges: indices live in many places, including outside the repo. A refactor checklist must enumerate all of them.

### Auto-index tooling

A workspace at L4 has tools that **regenerate indices from source-of-truth**. Example: a script that scans `launchctl list` (or `systemctl --user list-units` · or `crontab -l`) · reads each scheduler config · emits a fresh `CRON-REGISTRY.md`. Run on cron. Diff detects drift.

### Indices are not docs

Documentation explains. Indices locate. They have different audiences (humans for docs, agents for indices) and different optimization functions (clarity vs density). Mixing them produces files that are bad at both.

---

## Anti-patterns blocked

- ❌ "We document everything in one big README" — density tanks · agent has to read 50 KB to find one pointer.
- ❌ "The code is self-documenting · no index needed" — agent can't read all the code per query.
- ❌ "We update indices manually when we remember" — staleness mode by default · failure mode at next refactor.
- ❌ "We have indices but they don't cross-link" — agent finds one index, doesn't know the others exist.
- ❌ Indices that describe historical context instead of current state — density of actionable pointers near zero.

---

## How to maximize index density

1. **Enumerate entity types** in your workspace (daemons · cron · skills · tools · rules · ...). Make sure each has an index.
2. **Pick one index per type** as authoritative. No duplicates.
3. **Cross-link** all indices · each one points to the others (spine).
4. **Auto-generate** indices from source-of-truth where possible (scripts that scan launchctl/cron/files and emit the index).
5. **Add staleness detection** · cron job that checks index_recency_lag and alerts on drift.
6. **Test queryability** · run 10 entity-recall tasks against your indices monthly · score 10/10 or fix.

---

## Evidence

- Manus context engineering · KV-cache hit rate · achieved through stable index prefixes injected at session start.
- llms.txt convention (Anthropic + community) · standardizing machine-readable workspace indices for LLM consumption.
- Linux Foundation AAIF · AGENTS.md as vendor-neutral index contract.
- Observability literature · structured logs > unstructured (same principle applied to indices: structure beats prose).

---

_Extension 10 · iter-2 · 2026-05-20 · veicolo operativo della formula α dell'Extension 01_
