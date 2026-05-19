# Pillar 4 · Auto-Improvement Loop

> **First principle**: *The workspace must learn from its own session history · automatically · on a schedule.*
> **Max score**: 10 points.

---

## Why this pillar exists

Workspaces decay. Without an auto-improvement loop, agent quality drifts down over time as patterns get stale, skills get stale, and Nour-corrections are forgotten. Manual review doesn't scale. The Reflexion + Voyager + ECHO triad demonstrates that nightly verbal RL + skill growth + env-dynamics tracking produces measurable improvement over weeks.

---

## Scoring criteria · 10 binary checks

1. **[1.0]** Session capture · all session JSONL preserved (not just final summary).
2. **[1.0]** Session reflection runs automatically (cron · hook · scheduled job).
3. **[1.0]** Reflection writes to episodic memory tier (append-only).
4. **[1.0]** Improvement proposal system · agent suggests workspace changes from patterns observed.
5. **[1.0]** Scoring rubric for proposals (A-MAC · custom · or LLM-as-judge with documented criteria).
6. **[1.0]** Two-stage review · proposals approved before applied (no auto-mutate workspace).
7. **[1.0]** Apply log · changes applied are tracked (what · when · why · score).
8. **[1.0]** Feedback loop · improvement outcomes measured (did the change help or hurt?).
9. **[1.0]** Cron-driven · not on-demand only.
10. **[1.0]** Cost-aware · uses cheaper model (Sonnet/Haiku) for routine reflection · not Opus.

---

## Scoring rubric

| Score | Profile |
|-------|---------|
| **9-10** | Full Dreams pipeline · Reflexion nightly · A-MAC scoring · 2-stage review · apply log · feedback loop · cost-aware |
| **7-8** | Session reflection cron · proposal system · partial scoring · ad-hoc apply |
| **5-6** | Manual reflection occasionally · no proposal system |
| **3-4** | Sessions saved but never reflected on |
| **0-2** | No session capture · no improvement loop |

---

## Evidence sources

- **Reflexion (arXiv 2303.11366)** · verbal reinforcement learning via session reflection.
- **Voyager (arXiv 2305.16291)** · skill library auto-grown from agent experience.
- **Anthropic Managed Agents Dreams API** · nightly compaction + improvement proposal.
- **A-MAC 6-factor scoring** (Madani iter-37) · automated assessment of proposed improvements.
- **DGM** · discovery-guided mining of skill traces.

---

## Anti-patterns

- ❌ Improvements happen only when user notices something is broken
- ❌ No cron-driven reflection · everything on-demand
- ❌ Proposals applied without scoring · workspace drift accumulates
- ❌ Apply log missing · can't roll back bad changes
- ❌ Using Opus for routine nightly reflection (cost explosion)
- ❌ Session JSONL discarded after compaction · history lost

---

## Profiles

**Production-grade (9-10)**:
- Multi-stage pipeline (CAPTURE → EXTRACT → PROPOSE → REVIEW → APPLY → FEEDBACK) implemented as cron
- Reflexion-style nightly job (e.g., daily 23:30 · cheaper model like Sonnet/Haiku · subscription-based when possible)
- Multi-factor scoring of proposed improvements (e.g., A-MAC 5-6 factor rubric)
- Skill staleness curator (parallel cron · pre-improvement-loop)
- Full session capture preserved (JSONL + readable summary + backup copy · multi-layer redundancy)
- Episodic memory tier grows from reflection cron · append-only

**Prototype-stage (1-2)**:
- Sessions auto-compacted and discarded
- No reflection mechanism
- User manually edits config when something annoys them
- No tracking of what changes were made or why · no rollback path

---

## How to improve from low score

| From | To | Action |
|------|-----|--------|
| 0-3 | 5 | Preserve session JSONL · write manual reflection occasionally |
| 4-6 | 7 | Add cron for nightly reflection · write to episodic memory tier · use cheap model |
| 7-8 | 9 | Add proposal system · A-MAC-style scoring · 2-stage review (propose / approve / apply) |
| 9 | 10 | Add feedback loop (did the change help?) · multi-pattern adapter (Reflexion + Voyager + Dreams) |

---

## Self-audit questions

- When was the last time the workspace learned from a session without manual intervention?
- What's the cost per night of the auto-improvement loop · using which model?
- If a proposed improvement turns out to be wrong, can it be rolled back?
- How many improvements have been applied in the last 30 days · with what outcome?
