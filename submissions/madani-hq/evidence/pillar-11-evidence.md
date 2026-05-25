# Pillar 11 · Human-in-the-Loop · L4 Optimizing

## What the audit detected
Hard approval gates on outward-facing actions, explicit escalation criteria, and structured
human-decision points.

## Substantiating artifacts
- `CONSTITUTION.md` HR#1 + `~/.claude/rules/communication.md` · no message to any external recipient (client / team / Slack / email / SMS) without explicit human approval — compose locally, show, human decides.
- `CLAUDE.md` §9.2 Gate System · CLOSING gate = human approval before any external action.
- `.claude/rules/metacognition-policy.md` · ESCALATE_NOUR path when c_composite < 0.4 on cross-domain / high-stakes tasks.
- Origin trace: HR#1 born from a documented 2026-02-04 incident (3 Slack messages sent without authorization) — a real feedback→rule loop.

## Operator commentary
The gate is observed, not theoretical: **this very benchmark submission was held at the CLOSING
gate** — the agent ran + scored locally, then required explicit human confirmation (and a redaction
decision) before any public push. L4 because escalation is criteria-driven and the gate has
demonstrably blocked a real outward action.
