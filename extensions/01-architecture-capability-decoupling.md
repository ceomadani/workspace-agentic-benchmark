# Extension 01 · Architecture-Capability Decoupling

> Root principle iter-2 · supersedes "Workspace > Agent" by formalizing the multiplicative law that connects workspace quality to model capability.

---

## The principle

A workspace is **good** to the extent it amplifies a weak model and protects a strong one from degrading.

```
output_quality(task) = α(workspace) × capability(LLM)
```

Where:

```
α(workspace) = √( quality_files × quantity_files ) × density_indices
```

Three explicit terms:

| Term | What it measures | Maximization strategy |
|------|------------------|------------------------|
| **quality_files** | signal-to-noise · how much of each file is load-bearing information vs filler/stale/duplicate | edit ruthlessly · canonical references · single source of truth |
| **quantity_files** | completeness · whether all facts/patterns/entities the agent needs are present somewhere | systematic inventory · zero gaps in domain coverage |
| **density_indices** | how fast/precisely an agent can locate the right file via INDEX/registry/manifest layers | machine-readable indices · cross-linked · auto-updated · semantically queryable |

**The geometric mean** between quality and quantity is intentional: a workspace with infinite content (high quantity) and 5% signal (low quality) has the same α as a workspace with one perfect file and nothing else. **Both terms must be high simultaneously** · this is the architectural challenge.

---

## Hypothesis

> A well-designed workspace × weak LLM **outperforms** a poor workspace × strong LLM.

This is testable via a **capability sweep**: fix α (workspace), vary the model from a weak baseline (e.g., Haiku · 7B local) up to the frontier (e.g., Opus 4.7). Measure task success rate. The hypothesis predicts:

- Strong α + weak model ≥ Weak α + strong model (on tasks where the workspace context matters)
- The gap widens as task complexity / domain specificity increases
- α gain has higher ROI than model upgrade for tasks beyond ~6-month plateau in model improvement

This reframes the benchmark **away from model selection** and **toward workspace engineering**.

---

## Why this matters

The frontier LLM market is converging — capability gaps between top models narrow each cycle. The next decade of agentic productivity gains will come **not** from better models but from **better workspaces**. Most teams today invest 95% of their resources in prompts and 5% in workspace architecture; the leverage is reversed.

This extension is the **why** the rest of the benchmark exists. All 12 pillars + 9 extensions are operational facets of maximizing α.

---

## Operational consequences

### 1 · The benchmark must be model-agnostic

Audit tooling runs file-system + git scans + structural checks; LLM calls only for qualitative scoring where deterministic signals run out (~30% of total). The score must move when **the workspace** changes, not when the model upgrades.

### 2 · The role of indices

`density_indices` is not abstract — it's measured concretely (see Extension 10 · Index Density & Coverage). A workspace where the agent must do a recursive grep to find "where is daemon X" has lower density than one where a single `00_ENTITY-REGISTRY.md` (or equivalent) answers in <1 KB context.

The benchmark introduces an explicit `index_coverage_ratio`: fraction of governance entities (daemons · cron jobs · skills · tools · sub-agents · rules · pattern adapters · API integrations) that are findable through indices without `grep`.

### 3 · The role of memory tiers

Memory is the **temporal extension** of indices. An index gives you "what exists now"; the memory tiers (semantic · episodic · procedural · personalized) give you "what was true · what worked · what the user prefers." A weak model with strong memory + indices behaves as if it had longer context, better calibration, and personal knowledge.

### 4 · The role of skill/tool architecture

A skill is a **frozen index of capability** + an executable script. A workspace with 50 well-described skills lets a weak model invoke specialized behavior it couldn't generate from scratch.

### 5 · The role of HITL gates

α has an upper bound bounded by user trust. HITL gates protect the system from confidently-wrong outputs at the multiplication step (capability × α can produce wrong-but-confident if either factor goes off). HITL is not friction — it's the calibration mechanism for the product `output_quality`.

---

## Profile-aware audit

α is not a single number — it's contextual to the **use case**. Three reference profiles ship with the benchmark:

| Profile | Optimization priorities |
|---------|--------------------------|
| `solo-operator-private-repo` | Memory · Metacognition · Reliability are high-weight; Portability + Cost gate are low-weight (no team, subscription auth) |
| `team-saas-production` | Credentials · Portability · Cost · HITL are high-weight; the team must ship and not leak |
| `enterprise-multi-tenant` | All clusters balanced; Governance + Observability are high-weight for audit/compliance |

The composite score is computed as `Σ (pillar_score × pillar_weight)` where weights come from the profile. A single workspace can score differently under different profiles — this is by design.

---

## Evidence

- **Anthropic Effective Harnesses** (Nov 2025 + Mar 2026) · 87.2 → 91.1% benchmark improvement from harness swap alone · constant model · proves α ≠ 1.
- **Cognition "Don't Build Multi-Agents"** · the lift from removing bad architecture is larger than the lift from adding model capacity.
- **MetaCogAgent** (arXiv 2605.17292) · prospective metacognition adds ~10% accuracy across model scales · independent of base capability.
- **Manus context engineering** · KV-cache hit rate is the single highest leverage metric for cost/latency · property of the workspace, not the model.

---

## Anti-patterns blocked

- ❌ "We need to upgrade to model X to fix this" — try fixing α first; measure the delta; then decide.
- ❌ "More files = better workspace" — quality_files term collapses; α flat or down.
- ❌ "We have perfect docs but no index" — quantity high, density zero; α multiplied by ≈0.
- ❌ "Index lists 100 things but 80 are stale" — quality term tanks; density misleadingly high.
- ❌ Single number score independent of use case — α is profile-dependent.

---

## How to maximize α

In order of expected impact for most workspaces:

1. **Build the index layer** (Extension 10 · Index Density). If your indices are bad, no other improvement compounds.
2. **Prune the workspace** (raise quality_files). Delete duplicates · archive stale · merge variants. Pain in the moment, compound win after.
3. **Fill the gaps** (raise quantity_files). Inventory what the agent needs by domain · close the missing-coverage holes.
4. **Tier the memory** (Pillar 1). Semantic for facts · procedural for rules · episodic for events · personalized for user prefs · environment-dynamics for affordances.
5. **Codify the skills** (Pillar 2). Move repeated procedures into versioned skill modules with frontmatter + executable scripts.
6. **Wire the metacognition** (Pillar 9). Self-assess pre-task — α can't compensate for hallucinated confidence at the multiplication point.

---

_Extension 01 · iter-2 · 2026-05-20 · author: Nour Matine (formula) · Madani Lab · supersedes METHODOLOGY.md §1 "Workspace > Agent"_
