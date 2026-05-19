# Pillar 1 · Context Hierarchy & Memory

> **First principle**: *Information flows into context only when needed, only the parts needed.*
> **Max score**: 10 points.

---

## Why this pillar exists

The context window is the agent's most precious resource. Naive workspaces dump everything into context → context degradation → DPI violation (Stanford 2604.02460). Production workspaces tier memory by access pattern and apply explicit retrieval policies.

**Multi-tier memory architecture** (5 tiers, after Anthropic + ECHO + Reflexion fusion):

| Tier | What it stores | Retrieval pattern | Decay |
|------|----------------|-------------------|-------|
| **Semantic** | Facts about world (companies · APIs · technical concepts) | On-demand search | Slow |
| **Episodic** | Past sessions · what happened when | Time-windowed | Append-only · summarized |
| **Procedural** | How-to · skills · runbooks | Trigger-based | Manual + staleness flag |
| **Personalized** | User preferences · feedback patterns · style | Always-on subset | Updated on signal |
| **Environment-dynamics** | Current state of mutable env (file tree · running processes · API status) | Live-query | Refresh per call |

---

## Scoring criteria · 10 binary checks

Each criterion: pass (1.0) · partial (0.5) · fail (0.0). Total capped at 10.

1. **[1.0]** Multi-tier memory exists · at least 3 of 5 tiers explicitly separated in workspace.
2. **[1.0]** Retrieval policy explicit · file or doc describes *when* and *how* memory is retrieved.
3. **[1.0]** Forgetting / decay policy explicit · old or stale entries removed automatically or flagged.
4. **[1.0]** Index file exists (`MEMORY.md` or equivalent) · loads automatically into agent context.
5. **[1.0]** Memory entries have structured frontmatter (id · type · last_updated · source).
6. **[1.0]** Cross-links between memory entries (graph structure, not flat list).
7. **[1.0]** Episodic memory grows from session reflection (not manual entry only).
8. **[1.0]** Long-term storage is queryable (MCP · DB · vector store · grep-friendly).
9. **[1.0]** KV-cache awareness · prompt structure preserves cacheable prefix.
10. **[1.0]** Documented retrieval failure mode · what happens when memory query misses.

---

## Scoring rubric (band thresholds)

| Score | Profile |
|-------|---------|
| **9-10** | All tiers present · explicit retrieval policy · auto-decay · query layer (MCP/DB) · structured frontmatter · cache-aware |
| **7-8** | 4+ tiers · retrieval policy documented · index file loads · some auto-decay |
| **5-6** | 2-3 tiers · ad-hoc retrieval · manual decay · flat index |
| **3-4** | Single memory file · no policy · no decay |
| **0-2** | No memory layer · context dump every session |

---

## Evidence sources

- **arXiv 2604.02460** (Tran/Kiela Stanford) · DPI · context utilization is the choke point.
- **Cognition "Don't Build Multi-Agents"** · context handoff loss.
- **Anthropic Managed Agents Dreams API** · nightly compaction pattern.
- **Reflexion (arXiv 2303.11366)** · episodic memory from session reflection.
- **ECHO (iter-35 Madani)** · environment-dynamics tier addition.
- **MemGPT (arXiv 2310.08560)** · virtual context management.

---

## Anti-patterns

- ❌ Single mega-file loaded every turn ("context dump")
- ❌ Vector store with no retrieval policy ("search and pray")
- ❌ Memory written but never read
- ❌ No staleness flag · 6-month-old entries treated as current
- ❌ Memory entries reference deleted files / dead links

---

## Profiles

**Production-grade (9-10)**:
- 5 tiers explicitly separated as `memory/{semantic,episodic,procedural,personalized,env-dynamics}/` or equivalent
- Index file (e.g., `MEMORY.md`) auto-loaded on session start
- Scheduled reflection job (cron/hook) writes to episodic tier nightly
- Query layer exposing retrieval as a tool (MCP server · vector DB · or grep wrapper)
- Standard frontmatter on every entry (`name` · `type` · `last_updated` · `source`)
- Cross-links between entries (`[[wiki-style]]` or graph references)

**Prototype-stage (1-2)**:
- One `notes.md` updated occasionally
- Loaded fully in context every session
- No retrieval policy, no decay, no structure
- New entries appended without dedup or curation

---

## How to improve from low score

| From | To | Action |
|------|-----|--------|
| 0-3 | 5 | Create separate folders for semantic / episodic / procedural memory · write MEMORY.md index |
| 4-6 | 7 | Add frontmatter standard · enable auto-decay flag · document retrieval policy |
| 7-8 | 9 | Add query layer (MCP or DB) · implement session-reflection cron for episodic tier |
| 9 | 10 | KV-cache audit · ensure prompt prefix stable for cache hits |

---

## Self-audit questions

- When the agent needs to recall a fact from 3 months ago, what path does it take?
- What happens when memory grows beyond context window?
- Who removes stale memory entries · and on what trigger?
- If you delete `MEMORY.md`, does the agent notice?
