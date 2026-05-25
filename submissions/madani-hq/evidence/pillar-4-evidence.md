# Pillar 4 · Auto-Improvement Loop · L4 Optimizing

## What the audit detected
Scheduled, automated reflection and proposal loops feeding back into the system, plus a written
double-loop learning protocol.

## Substantiating artifacts
- `11_TOOLS/reflexion-runner.py` · daily cron (23:30) extracting lessons + correctness signals from session JSONL.
- `11_TOOLS/dreams-runner.py` · daily cron (03:00) "Dreams" PROPOSE stage suggesting new skills / improvements.
- `11_TOOLS/skill-staleness-detector.py` · Hermes auto-stale curator (02:30).
- `12_HARNESS/operativo/lessons-learned.md` · codified lessons L01–L05 (e.g. path-drift refactor, shared-component impact).
- `CLAUDE.md` §9.4 · Double-Loop Learning protocol (fix → why → which rule is missing → update the system).

## Operator commentary
The loop is cybernetic and unattended: Reflexion derives a binary correctness signal `r_k` that
feeds the metacognition capability profile's EMA update (see pillar 9). Improvement happens on a
schedule without a human kicking it off — the L3→L4 step.
