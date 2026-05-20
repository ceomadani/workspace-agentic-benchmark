# Extension 05 · Compositionality

> Skills, tools, sub-agents, and rules must compose without combinatorial degradation. Adding a new module shouldn't break existing ones.

---

## Principle

A workspace is **compositional** when:
- Modules have clear contracts (inputs · outputs · side effects · failure modes)
- Combining two modules has predictable behavior — not "depends on phase of moon"
- Adding a new module doesn't require touching unrelated modules

Lack of compositionality is why agentic systems explode in complexity past 20-30 components. Each new tool adds N quadratic interactions with existing ones if contracts are implicit.

---

## Requirements

| Requirement | Artifact |
|-------------|---------|
| Explicit module contracts | Skill frontmatter declares `tools: [...]` · `disallowedTools: [...]` · `inputs: [...]` · `outputs: [...]` |
| Idempotency where stateful | Tools that write state must declare idempotency (safe to retry?) · benchmarked |
| No hidden globals | Modules read config from explicit input or env, not from shared mutable state |
| Versioned interfaces | Breaking changes bumped via semver in module changelog |
| Compatibility matrix | Some pairs (e.g., DPI multi-agent + Reflexion) need explicit compatibility notes |

---

## Measurement

- `% of skills with complete frontmatter contract (inputs/outputs/tools)` (target ≥ 0.9 at L4)
- `% of tools with declared idempotency` (target ≥ 0.8 at L4)
- `composition test pass rate`: 10 random pairs of modules · do they work together? (target ≥ 9/10 at L4)

---

## Anti-patterns

- ❌ Tools that secretly depend on environment state set by another tool.
- ❌ Skills that mutate shared files used by other skills (without lock + contract).
- ❌ Sub-agents that recurse (sub-agent spawns sub-agent · MAST failure mode #11).

---

_Extension 05 · iter-2 · 2026-05-20_
