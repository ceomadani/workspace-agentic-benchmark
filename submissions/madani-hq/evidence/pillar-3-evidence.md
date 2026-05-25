# Pillar 3 · Governance & Compliance · L4 Optimizing

## What the audit detected
A written constitution, enumerated non-negotiable hard rules, and an automated pre-output
compliance gate.

## Substantiating artifacts
- `CONSTITUTION.md` · system constitution; 15 hard rules (HR#1 external-comms gate … HR#15 skill auto-create).
- `.claude/rules/*.md` · project-level rules (multi-agent-policy, metacognition-policy, credentials-policy, adversarial-robustness-policy) with changelog.
- `11_TOOLS/compliance-check.py` · HR#15 PRE-OUTPUT compliance check (5 criteria vs canonical files) run before significant output.
- `.claude/agents/compliance-judge.md` · persistent judge sub-agent spec (PASS / REFINE / BLOCK verdicts).

## Operator commentary
Governance is re-asserted every turn via a UserPromptSubmit hook that re-injects the active hard
rules, defeating long-session drift. The compliance-check tool + compliance-judge sub-agent make
the pre-output gate executable rather than a checklist someone has to remember — the L4 marker.
