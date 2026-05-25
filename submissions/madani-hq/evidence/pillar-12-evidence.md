# Pillar 12 · Cost & Performance Efficiency · L4 Optimizing

## What the audit detected
Workspace-level token economics: cache-hit measurement, a cost/budget gate, thin-context
resolution, and confidence-driven model routing.

## Substantiating artifacts
- `11_TOOLS/kv-cache-metric.py` · KV-cache hit-rate metric (Manus pattern, target ≥70%) — stable prefix to maximize cache reuse.
- `11_TOOLS/token-budget-tracker.py` · cost gate tied to HR#12; tracks token spend per task.
- `11_TOOLS/madani-resolve.py` · thin-context URI resolver — load pointers, not whole files, to cut token load.
- Confidence-driven model routing: metacognition (pillar 9) selects Haiku / Sonnet / Opus by task difficulty rather than always-Opus.

## Operator commentary
Cost is treated as a first-class, measured dimension at the workspace level (not just per task):
stable-prefix caching + thin-context resolution + metacog-gated model routing form a coherent
cost-per-outcome strategy. The presence of an actual budget tracker + cache metric (vs. a stated
intention) is the L4 marker.
