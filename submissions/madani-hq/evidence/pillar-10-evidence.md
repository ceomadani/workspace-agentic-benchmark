# Pillar 10 · Reliability & Determinism · L4 Optimizing

## What the audit detected
Mechanisms that make agent behavior repeatable under stress: deterministic task routing, KV-cache
prefix discipline, and explicit failure-mode awareness.

## Substantiating artifacts
- `11_TOOLS/cynefin-classifier.py` · routes tasks across 5 Cynefin domains so the same class of task takes the same path.
- `11_TOOLS/cache-prefix-validator.py` · guards the stable KV-cache prefix (deterministic context construction).
- `11_TOOLS/kv-cache-metric.py` · measures cache hit rate (target ≥70%) — reproducibility signal.
- `CLAUDE.md` §13 + lessons L01–L05 · MAST 14-failure-mode awareness, refactor-survival checklist (grep consumers + plist + cron before renames).

## Operator commentary
Determinism here is structural: a validated stable prefix means the same inputs reconstruct the
same context, and the Cynefin classifier removes ad-hoc routing variance. The refactor-survival
checklist (born from a real path-drift incident, L02) is the reliability practice that pushes this
to L4 — failure modes are catalogued and guarded, not discovered in production.
