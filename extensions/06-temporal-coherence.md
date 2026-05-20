# Extension 06 · Temporal Coherence

> The workspace must maintain consistent state across long time horizons · decisions made in session N must remain accessible and applicable in session N+100.

---

## Principle

Sessions die. Context windows compact. Memory drifts. Without explicit temporal mechanisms, the workspace forgets its own history and the agent re-litigates past decisions.

```
coherence(t) = (decisions_made_before_t still findable AND still correctly applicable) / total_decisions_made_before_t
```

Target ≥ 0.95 for L4.

---

## Operational requirements

| Requirement | Workspace artifact |
|-------------|---------------------|
| **Session archive** | PreCompact hook saves session snapshots to a dedicated folder (e.g. `sessions/`, `history/`, `cronologia/`) — provenance + recoverable |
| **Decision log** | `lessons.md` · `_CHANGELOG.md` per cluster · who/when/why for every architectural decision |
| **Memory tier separation** | Episodic (events) ≠ Procedural (rules) ≠ Semantic (facts) — different aging/decay rules |
| **Drift detection** | Periodic audits compare current state vs decisions log · flag inconsistencies |
| **Time-stamp discipline** | Absolute dates (`2026-05-20`) not relative (`yesterday` · `last week`) in memory entries |
| **Memory promotion** | Episodic events that recur get promoted to procedural rules (Voyager pattern · `memory-promote.py`) |
| **Reflexion cycles** | Daily/weekly reflection that extracts patterns from session history (Reflexion arXiv 2303.11366) |

---

## Why a separate extension and not just "memory"

Memory (P01) is about **structure**. Temporal coherence is about **time-dimension integrity**. A workspace can have great tier structure (L4 P01) but no drift detection · its memory grows inconsistent over months · agent acts on stale assumptions.

This is the layer that catches "we decided X in March, but by November we're doing not-X without ever marking the change."

---

## Measurement

- `decision_recall_test`: random sample 10 past decisions · agent retrieves and applies correctly (target ≥ 9/10)
- `drift_audit_lag`: time between drift events and detection (target ≤ 7 days at L4)
- `% of memory entries with absolute timestamps` (target = 1.0 at L4)
- `Reflexion cycle frequency` (target daily at L4)

---

## Anti-patterns

- ❌ "Yesterday we decided X" — relative time stamps decay into uninterpretable.
- ❌ Memory entries that don't note WHO made the decision · accountability lost.
- ❌ No reflexion cycle · session history is write-only · no learning extracted.
- ❌ Decisions logged but no drift check · workspace evolves silently against the log.

---

_Extension 06 · iter-2 · 2026-05-20_
