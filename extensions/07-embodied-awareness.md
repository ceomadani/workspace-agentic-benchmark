# Extension 07 · Embodied / Situational Awareness

> The agent must know where it is · when it is · what state the environment is in · before acting.

---

## Principle

An agent without situational awareness behaves like a person teleported into an unknown room blindfolded. Useful for nothing until it has: current working directory · current time · current git branch · last action taken · what tools are available · what credentials are loaded · what mode (auto/manual) is on.

Most of this is **passive injection at session start** — the agent doesn't have to ask, it's given.

---

## Requirements

| Awareness | Mechanism | Example injection (any workspace) |
|-----------|-----------|------------------------------------|
| Time · absolute · timezone | SessionStart injection | "Today's date is YYYY-MM-DD · Europe/Paris" |
| Location · cwd · git state | SessionStart injection | "pwd: /Users/operator/workspace · branch: feature/x" |
| User identity · scope | Auto from system | "user: operator · email: operator@org.com" |
| Recent actions · last 24h | SessionStart reads tool-log file last 50 events | "Last 50 tool calls: ..." |
| Active rules · live | SessionStart injects procedural memory top 5 | "Active hard rules: HR#1, HR#10, HR#13, HR#15" |
| Available tools | Automatic via Claude Code tool list | (built-in) |
| Active hooks | SessionStart injects hook list | "Active enforcement: PreToolUse · PostToolUse · Stop · ..." |
| External system status | Optional health checks | "n8n: up · CRM: up · Slack: up" |

---

## Measurement

- `situational_query_test`: ask the agent 10 questions about current state without grep/search (target ≥ 9/10 at L4)
- `SessionStart injection size` (target 6-12 KB · enough signal · not bloat)
- `% of sessions where agent re-asks for state already injected` (target ≤ 0.05 at L4 · agent should reference, not re-query)

---

## Anti-patterns

- ❌ SessionStart hook missing or thin · agent grep for time/branch/cwd every session.
- ❌ Session injection of stale data (e.g., yesterday's git status) · misleading worse than absent.
- ❌ Inject too much (>15 KB) · context cost > recall benefit · pillar density suffers.

---

_Extension 07 · iter-2 · 2026-05-20_
