# Extension 03 · Causal Reasoning Support

> The workspace must enable interventional reasoning, not just observational pattern-matching.

---

## Principle

Pearl's hierarchy:
1. **Observation**: "X and Y are correlated."
2. **Intervention**: "If I do X, Y changes."
3. **Counterfactual**: "Y happened. If X had been different, would Y have happened?"

LLMs default to observation. A workspace that wants intervention/counterfactual reasoning must **encode causal structure explicitly** — not leave the agent to infer it from prose.

---

## Operational requirements

| Requirement | Workspace artifact |
|-------------|---------------------|
| Cause → effect maps for failures | `lessons.md` with structure: `trigger → consequence → fix → systemic cause` |
| Decision rationale (the reason a rule exists) | Every rule has `## Why` and `## How to apply` sections |
| Counterfactual logs | `12_HARNESS/memory-engine/episodic/` events tagged with `would_have_avoided_with: <rule>` |
| Intervention catalog | Skills + tools tagged with `intervenes_on: <what>` |
| Failure causality graphs | Post-mortem files reference upstream causes + downstream blast radius |

---

## Why this matters for agents

A weak model with explicit causal structure performs counterfactual reasoning **better than** a strong model with implicit structure. The workspace bridges the model's pattern-matching default into actual cause-effect manipulation.

Example pattern: a mature workspace maintains a `lessons-learned.md` (or equivalent) with explicit "trigger → cause → fix → systemic-pattern" chains for every notable failure. An agent asked "what could have prevented X" can do counterfactual retrieval against these structured entries; without them, the agent has to hallucinate from prose.

---

## Measurement

- `% of rules with stated Why` (target ≥ 0.9 at L4)
- `% of skills/tools with stated intervenes_on` (target ≥ 0.8 at L4)
- `% of post-mortems with full trigger-cause-fix-systemic chain` (target ≥ 0.85 at L4)

---

## Anti-patterns

- ❌ Rules without Why · agent can't reason about edge cases or apply to new contexts.
- ❌ Post-mortems that only describe the symptom · no cause encoded · learning lost.
- ❌ Skills without "what does this intervene on" · agent picks tools by name-matching, not by causal fit.

---

_Extension 03 · iter-2 · 2026-05-20_
