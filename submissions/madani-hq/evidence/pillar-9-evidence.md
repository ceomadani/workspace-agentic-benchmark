# Pillar 9 · Metacognition & Self-Assessment · L3 Defined

## What the audit detected
9 of 10 criteria passed: a metacognition tool, a capability profile, verbalized-confidence
mechanism, documented composite formula, conflict detection, decision gate, EMA update, anti-pattern
docs, DPI integration, and a cited backing paper. The **one** missing criterion is
ECE / calibration tracking.

## Substantiating artifacts
- `11_TOOLS/metacog-self-assess.py` · prospective self-assessment: c_verbalized + c_profile → c_composite, conflict δ, decision gate (EXECUTE_DIRECT / CONSIDER_DELEGATION / ESCALATE_NOUR).
- `.claude/rules/metacognition-policy.md` · full policy, thresholds (θ=0.55, λ=0.6, α=0.1, γ=0.2), 4 worked examples, anti-patterns.
- `12_HARNESS/memory-engine/procedural/capability_profile_madani.md` · per-dimension capability profile with EMA update loop.
- `12_HARNESS/pattern-transfer/metacognition-adapter.md` · pattern adapter; backing arXiv 2605.17292 (MetaCogAgent, Wang/Shu 2026).

## Why L3 and not L4 (honest)
The mechanism is fully defined and tool-mediated, but there is **no calibration tracking** (ECE) of
predicted-vs-actual confidence yet — so the system self-assesses but does not yet measure whether
its confidence is well-calibrated. Adding ECE logging against the Reflexion `r_k` signal is the
single criterion that takes this pillar to L4.
