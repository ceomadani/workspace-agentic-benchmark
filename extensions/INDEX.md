# Extensions · iter-2 framework

> Eleven extensions to the 12-pillar baseline · ground the benchmark in first principles beyond the initial CMMI-derived maturity layers.

---

## Why extensions exist

The 12 pillars cover what the literature consistently identifies as critical. The extensions cover what's necessary but **not yet** standard in the agentic workspace discipline: first principles that hold regardless of framework choice · regardless of model · regardless of stack.

iter-1 of this benchmark (Apr 2026) shipped with 12 pillars. iter-2 (May 2026) adds these extensions after applying the benchmark to the Madani workspace and identifying systematic blind spots.

---

## The eleven extensions

| # | Title | What it adds |
|---|-------|--------------|
| [01](01-architecture-capability-decoupling.md) | **Architecture-Capability Decoupling** | The α formula · root principle that supersedes "Workspace > Agent" |
| [02](02-information-theory.md) | **Information Theory · Signal-to-Noise** | Operationalizes file quality via Shannon entropy |
| [03](03-causal-reasoning.md) | **Causal Reasoning Support** | The workspace encodes cause-effect explicitly · not just patterns |
| [04](04-adversarial-robustness.md) | **Adversarial Robustness** | Protection against prompt injection · poisoned tool output |
| [05](05-compositionality.md) | **Compositionality** | Modules compose without combinatorial degradation |
| [06](06-temporal-coherence.md) | **Temporal Coherence** | Decisions made in session N hold in session N+100 |
| [07](07-embodied-awareness.md) | **Embodied / Situational Awareness** | Time · place · git state · active rules · injected at session start |
| [08](08-knowledge-representation.md) | **Knowledge Representation Choice** | Right form (prose/YAML/vector/graph) for each use case |
| [09](09-resilience-partial-failure.md) | **Resilience under Partial Failure** | Component dies → workspace keeps working coherently |
| [10](10-index-density.md) | **Index Density & Semantic Coverage** | The vehicle through which α reaches the agent |
| [11](11-meta-measurement.md) | **Meta-Measurement** | Guards against Goodhart gaming of the benchmark itself |

---

## How extensions relate to pillars

Extensions are **cross-cutting**: each extension touches multiple pillars rather than being a 13th pillar. Examples:

| Extension | Pillars it strengthens |
|-----------|------------------------|
| 01 · α formula | All 12 (the root principle) |
| 02 · Info theory | P01 Memory · P02 Skills · P06 Observability |
| 03 · Causal | P01 Memory · P03 Governance · P04 Auto-improvement |
| 04 · Adversarial | P07 Credentials · P03 Governance · P11 HITL |
| 05 · Compositionality | P02 Skills · P05 Multi-agent DPI · P10 Reliability |
| 06 · Temporal | P01 Memory · P04 Auto-improvement |
| 07 · Embodied | P01 Memory · P11 HITL |
| 08 · KR choice | P01 Memory · P02 Skills |
| 09 · Resilience | P06 Observability · P10 Reliability |
| 10 · Index density | P01 Memory · P02 Skills · P06 Observability · P12 Cost |
| 11 · Meta-measurement | All 12 (recursive defense) |

---

## How to use extensions in audit

The CLI's `score` command will (iter-2) report **pillar scores** + **extension liveness checks** as separate sections. Extensions are scored on a binary (`present` / `absent` / `partial`) since their qualitative nature resists fine numeric grading.

A workspace can:
- Score L4 on all 12 pillars but lack 5+ extensions → high pillar composite but real fragility
- Score L3 on most pillars but have all 11 extensions → lower composite but more architecturally complete

Both are valid states. The benchmark surfaces the asymmetry rather than collapsing it.

---

## Open questions for iter-3

- Should extensions become **weighted pillars** (13th-23rd) instead of binary checks? (Trade-off: more granularity vs. resistance to gaming.)
- How to score extensions automatically vs. requiring human review?
- Are there extensions we still don't see? (Submissions welcome via RFC process.)

---

_Extensions index · iter-2 · 2026-05-20 · Madani Lab_
