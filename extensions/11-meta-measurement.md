# Extension 11 · Meta-Measurement · Guard Against Goodhart's Law

> What we measure shapes behavior · including the behavior of the workspace measuring itself. Without meta-measurement · the benchmark becomes a target to game · not a guide to improve.

---

## Principle

Goodhart's Law: *"When a measure becomes a target, it ceases to be a good measure."*

The 12 pillars + 10 extensions are excellent inputs to a workspace audit. They are also **exactly the surface a workspace will game** if scoring becomes high-stakes (vendor evaluation · cert · public ranking). Defenses against gaming must be baked in.

---

## Gaming modes the benchmark must resist

| Mode | Counter |
|------|---------|
| **Index inflation** · register 100 entities to boost coverage · 80 are stubs | Stub detection · index entries must point to live · non-empty artifacts |
| **Skill spam** · create 50 trivial skills to boost P02 score | Skill quality threshold · `description` length + tools count + usage frequency over time |
| **Documentation theater** · write rules nobody enforces · score them L4 | Audit must verify hook/cron enforcement · not just file existence |
| **Compliance log padding** · synthesize compliance check entries to look active | Sample real session histories · check log entries match actual events |
| **Benchmark version pinning** · stay on old benchmark version · old criteria | Auto-deprecate scores >6 months old |
| **Profile-shopping** · pick the profile that scores best · misrepresent use case | Profile selection is declarative · cross-verified against workspace artifacts (e.g., team profile requires team-membership artifacts) |

---

## Requirements

| Requirement | Implementation |
|-------------|----------------|
| **Liveness probes** | Each pillar measurement requires not just artifact existence but recent invocation evidence (cron logs · session logs · git activity) |
| **Cross-pillar consistency** | Audit checks that P02 (skills count) is consistent with P04 (auto-improvement · do skills actually improve?) |
| **Adversarial audit mode** | Optional flag `--adversarial` runs the benchmark with anti-gaming heuristics tightened |
| **Score decay** | Composite score decays 10%/month after audit · re-audit required for currency |
| **External verification** | High-stakes scores require evidence URL · publicly inspectable artifacts |

---

## Measurement of the meta-measurement

- `gaming_resistance_score`: red-team team builds a workspace optimized only for score · does it actually work for real tasks? (target: optimized workspace is at most 5% above honestly-built equivalent)
- `audit_consistency`: 3 independent reviewers score the same workspace · variance ≤ 5 points composite

---

## Anti-patterns

- ❌ Headline score with no decay · workspaces game once then coast.
- ❌ No liveness check · pure file-existence scoring is gameable in a day.
- ❌ No external evidence requirement · scores are self-reported truth.

---

_Extension 11 · iter-2 · 2026-05-20 · the recursive layer that protects the benchmark from itself_
