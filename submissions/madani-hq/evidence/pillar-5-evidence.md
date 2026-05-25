# Pillar 5 · Multi-Agent Discipline (DPI) · L4 Optimizing

## What the audit detected
An explicit, evidence-backed single-thread-default policy with a hard gate on spawning concurrent
sub-agents.

## Substantiating artifacts
- `.claude/rules/multi-agent-policy.md` · DPI Guard. Single-thread default; multi-agent requires ALL 3 conditions (context degradation >50KB · reasoning budget ≥2× · explicit human approval).
- Same file · pre-authorized exception for read-only `Explore` sub-agents (context protection) and a documented pre-spawn checklist.
- Same file · 4 named blocked anti-patterns (parallel division, "more modern", orchestrator-worker without shared KV-cache, recursive sub-agents).
- Backing: arXiv 2604.02460 (Tran/Kiela, Stanford — single-agent outperforms multi-agent under equal token budget) + Cognition steel-man, both cited.

## Operator commentary
The policy is grounded in the Data Processing Inequality, not fashion, and the pre-spawn checklist
makes the decision mechanical. In this very engagement the agent stayed single-thread and used
zero sub-agents — discipline observed, not just documented.
