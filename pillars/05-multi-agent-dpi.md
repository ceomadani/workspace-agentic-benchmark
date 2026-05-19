# Pillar 5 · Multi-Agent Discipline (DPI)

> **Cluster B · Action**
> **First principle**: *Default to single-thread. Multi-agent is an exception with explicit justification.*
> **Weight**: 1/12 (equal-weighted baseline · v0.3 default)

---

## Why this pillar exists

Multi-agent is fashionable but evidence-light. Stanford 2604.02460 shows single-agent dominates under equal token budget. Multi-agent only wins under 3 specific conditions:
1. Context already degraded in primary
2. 2× token budget available
3. Evidence of need (not "feels more modern")

Without DPI discipline, workspaces over-spawn sub-agents and pay context handoff loss + cost explosion + recursion bugs.

---

## Scoring criteria · 10 binary checks

1. **[1.0]** Default mode documented as single-thread.
2. **[1.0]** Multi-agent policy file exists · enumerates when sub-agents allowed.
3. **[1.0]** Pre-spawn gate · documented criteria checked before invoking sub-agent.
4. **[1.0]** Explore-only sub-agent pre-authorized for read-only protection.
5. **[1.0]** No recursive sub-agents (sub-agent spawning sub-agent · MAST failure mode).
6. **[1.0]** Sub-agent prompts self-contained (zero parent context · explicit bootstrap).
7. **[1.0]** Pattern source cited · evidence-based rationale (paper / case study).
8. **[1.0]** Budget guard · token estimate enforced before spawn.
9. **[1.0]** Anti-pattern list documented (4+ known failure modes).
10. **[1.0]** Multi-agent invocations logged · auditable post-hoc.

---

## L0-L4 Maturity Rubric

| Level | Score | Profile |
|-------|------:|---------|
| **L0 Absent** | 0 | Multi-agent by default · sub-agent recursion allowed · no constraints. |
| **L1 Initial** | 20 | Multi-agent used often without measurement · no documented policy. |
| **L2 Managed** | 50 | Multi-agent used selectively · informal awareness of context cost · no formal policy file. |
| **L3 Defined** | 75 | Single-thread documented as default · `multi-agent-policy.md` enforces pre-spawn gate · Explore-only pre-authorized · evidence cited (arXiv 2604.02460 + Cognition steel-man) · 4+ anti-patterns documented. |
| **L4 Optimizing** | 100 | Sub-agent invocations logged + audited · DPI condition evidence operationalized via metacognitive confidence trigger (P9 integration) · context handoff cost measured + budgeted · multi-agent ROI ratio tracked vs single-thread baseline. |

---

## Evidence sources

- **arXiv 2604.02460 (Tran/Kiela Stanford)** · "Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets".
- **Cognition "Don't Build Multi-Agents"** · steel-man · context sharing is the bottleneck.
- **MAST framework** · 14 documented multi-agent failure modes.
- **Anthropic sub-agent guidance** · self-contained prompts · no context leakage.

---

## Anti-patterns (4 documented)

- ❌ **Parallel division for non-parallel work**: spawning 4 sub-agents to "divide" a task that requires shared state · loses to single-agent.
- ❌ **"Multi-agent because it's modern"**: no evidence · no measurement · cargo cult.
- ❌ **Orchestrator-worker without KV-cache sharing**: context handoff loss guaranteed.
- ❌ **Recursive sub-agents**: sub-agent spawns sub-agent · debugging nightmare · MAST documented failure.

---

## Profiles

**Production-grade (9-10)**:
- `multi-agent-policy.md` (or equivalent) in rules directory · explicit policy
- Single-thread baseline: 1 thread default · multi-agent requires 3 explicit conditions met
- Read-only / explore-only sub-agent pre-authorized for context-protected exploration
- Pre-spawn checklist (4+ binary checks documented)
- Anti-pattern list enumerated (4+ entries)
- Evidence cited (e.g., arXiv 2604.02460 Stanford DPI + Cognition "Don't Build Multi-Agents")

**Prototype-stage (0-2)**:
- Every task auto-spawns 3-5 sub-agents
- No documented policy
- Sub-agents themselves spawn sub-agents (recursion)
- No budget tracking · cost runaway · no spawn audit log

---

## How to improve from low score

| From | To | Action |
|------|-----|--------|
| 0-3 | 5 | Write multi-agent policy file · document single-thread default · stop sub-agent recursion |
| 4-6 | 7 | Add pre-spawn gate (3-condition check) · pre-authorize Explore-only for read-only |
| 7-8 | 9 | Cite evidence (arXiv 2604.02460) · enumerate anti-patterns · enforce budget guard |
| 9 | 10 | Log all multi-agent invocations · post-hoc audit · measure context handoff cost |

---

## Self-audit questions

- When did you last spawn a sub-agent · was it justified by context degradation or convenience?
- Could the task have been done single-thread with better context management?
- What's the cost overhead of your multi-agent invocations in the last 30 days?
- If a sub-agent recurses (spawns its own sub-agent), what happens?
