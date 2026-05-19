# Pillar 12 · Cost & Performance Efficiency

> **Cluster D · Operations**
> **First principle**: *Token economics decide deployment viability · harness, not model.*
> **Weight**: 1/12 (equal-weighted baseline · v0.3 default)

---

## Why this pillar exists

The CLEAR framework (arXiv 2511.14136) documented **50× cost variations between agents achieving similar precision on enterprise tasks**. The Anthropic harness research (Nov 2025 + Mar 2026) demonstrated that swapping the harness alone — without changing the model — moved benchmark scores from 87.2% → 91.1% (+3.9pp). The dominant cost driver in production agentic systems is **harness design**, not model capability. Workspaces that don't measure cost-per-outcome ship demos that bankrupt their customers in production.

This pillar measures whether the workspace tracks the economics of its own operation.

---

## L0-L4 Maturity Rubric

| Level | Score | Profile |
|-------|------:|---------|
| **L0 Absent** | 0 | No cost tracking. No latency tracking. No notion of token economics. |
| **L1 Initial** | 20 | Aware that cost matters. Occasional manual check of provider dashboard. No instrumentation. |
| **L2 Managed** | 50 | Cost per session logged. Latency per action logged. Cache hit rate measured. |
| **L3 Defined** | 75 | Cost per outcome (business event · not per-token) tracked. Model routing policy documented (cheap for simple · expensive for hard). Cache prefix stability validated. |
| **L4 Optimizing** | 100 | Cost/outcome regression alerts. A/B tested model routing. Cache hit rate ≥ 80%. Cost-aware metacognition (`metacog` decides when expensive model is justified). |

---

## Sub-dimensions

### 12.1 · Cost tracking granularity
- L0: not tracked
- L1: aggregate provider invoice
- L2: per-session token + dollar logged
- L3: per-outcome cost (cost per business event · cost per delivered artifact)
- L4: cost-per-outcome regression alerts · monthly variance bands

### 12.2 · Latency measurement
- L0: not measured
- L1: anecdotal "feels slow"
- L2: time-to-first-token logged
- L3: latency percentiles (p50 · p95 · p99) per action class
- L4: latency budgets enforced · SLO alerts

### 12.3 · Cache utilization
- L0: cache not considered
- L1: aware of provider cache · no measurement
- L2: cache hit rate measured occasionally
- L3: prompt prefix stability audited · cache hit rate ≥ 60% on hot paths
- L4: cache hit rate ≥ 80% on hot paths · invalidation events instrumented

### 12.4 · Model routing policy
- L0: single model for everything
- L1: occasional manual override to cheaper model
- L2: documented routing policy (cheap default · expensive on hard tasks)
- L3: routing based on metacognitive confidence (P9) · cheap model where confidence high
- L4: A/B tested routing · cost-quality Pareto curve maintained

### 12.5 · Subscription vs API economics
- L0: API key for every call · no subscription consideration
- L1: aware of subscription option
- L2: subscription used for high-volume routine tasks · API for spike
- L3: cost model compared monthly · routing decisions evidence-based
- L4: subscription + API hybrid optimized for current volume + variance

---

## Evidence sources

- **CLEAR** (arXiv [2511.14136](https://arxiv.org/abs/2511.14136)) · 50× cost variation for same precision on enterprise tasks.
- **Anthropic harness research** (Nov 2025 + Mar 2026) · "the harness, not the model" · 87.2 → 91.1% from harness swap alone.
- **Anthropic prompt caching documentation** · 90% cost reduction on cached tokens · 5-minute TTL.
- **MindStudio agent benchmarks** · harness optimization beats model upgrade.
- **Focused Labs "Agent Benchmark Scores Are Measuring the Harness, Not the Model"** (2026) · empirical analysis.

---

## Anti-patterns

- ❌ **Premium model for every call** · 10-100× cost overhead with marginal quality lift on simple tasks.
- ❌ **Unstable prompt prefix** · destroys cache hit rate · every call is full-cost.
- ❌ **No latency budget** · agent times out under load · cascading failures.
- ❌ **API calls for routine tasks** when subscription would amortize cost (e.g., nightly cron jobs).
- ❌ **Cost tracked per-token only** · misses the only metric that matters: cost per business outcome.

---

## Profiles

**Production-grade (L3-L4)**:
- Cost per business outcome tracked monthly · regression alerts
- Latency p50/p95/p99 instrumented per action class · SLO budgets enforced
- Cache hit rate ≥ 80% on hot paths · prompt prefix audited
- Model routing based on metacognitive confidence (P9) or task class
- Subscription + API hybrid optimized for current volume + variance

**Prototype-stage (L0-L1)**:
- Provider invoice is a surprise each month
- Latency "feels OK" · no measurement
- Cache hit rate unknown
- Always uses the premium model "to be safe"
- Subscription unused even for high-volume routine work

---

## Relation to other pillars

- **P1 Context Memory** · KV-cache awareness shared concern · cache prefix stability is the bridge.
- **P9 Metacognition** · MetaCog confidence is the *signal* for model routing in this pillar.
- **P4 Auto-Improvement** · improvement loop uses cheaper model (Sonnet/Haiku) routinely · documented cost-aware pattern.
- **P6 Observability** · cost + latency metrics are part of the observability stack.

---

## How to improve from low level

| From | To | Action |
|------|-----|--------|
| L0 → L2 | Add cost/token logging per session. Measure cache hit rate via provider tools. Time-to-first-token instrumented for hot paths. |
| L2 → L3 | Define "outcome unit" (per business event · per artifact) · track cost-per-outcome. Document routing policy. Audit prompt prefix stability. |
| L3 → L4 | Set SLO budgets · alert on regression. A/B test routing decisions. Achieve cache hit ≥ 80% on hot paths · use metacognitive confidence to choose model. |

---

## Self-audit questions

- What does your most common task cost · per execution · in dollars and tokens?
- What is your cache hit rate on the hot path · this week?
- Does your workspace ever use a cheaper model (Sonnet · Haiku · open-source) · and on what criterion?
- If your agent had to run 1000× tomorrow, would your bill be predictable to ±20%?

---

_Pillar 12 · v0.3 · 2026-05-19 · pattern source CLEAR + Anthropic harness research + Focused Labs · novel addition to public agentic workspace benchmarks_
