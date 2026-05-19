# Pillar 10 · Reliability & Determinism

> **Cluster B · Action**
> **First principle**: *An agent that succeeds once in eight tries is not a system — it is a coin flip.*
> **Weight**: 1/12 (equal-weighted baseline · v0.3 default)

---

## Why this pillar exists

The CLEAR enterprise framework (arXiv 2511.14136) demonstrated that agent performance on the same task degrades from ~60% single-run success to ~25% under `pass@k=8` consistency requirements. The MAST taxonomy (arXiv 2503.13657) documents 41-86.7% failure rates across 7 multi-agent frameworks. Workspaces that don't measure determinism ship demos that fail under production load.

This pillar measures whether the workspace produces **repeatable** behavior under repeated runs of the same task.

---

## L0-L4 Maturity Rubric

| Level | Score | Profile |
|-------|------:|---------|
| **L0 Absent** | 0 | No notion of repeatability. Same task can yield wildly different outputs · no logging of variance. |
| **L1 Initial** | 20 | Awareness of non-determinism. Operator manually re-runs and picks best. No measurement. |
| **L2 Managed** | 50 | Logged variance across runs. Retry logic exists for known-flaky operations. Idempotency considered for external actions. |
| **L3 Defined** | 75 | `pass@k` measured on representative tasks. Retry logic with exponential backoff for transient failures. Idempotency enforced via keys for all external writes. MAST failure-mode coverage documented (which of 14 modes are detectable). |
| **L4 Optimizing** | 100 | `pass@k=8` regression tracked over time (target ≥ 0.8). Replay harness for failed runs. Automated triage of failure modes per MAST taxonomy. Determinism budget set per task class. |

---

## Sub-dimensions (assessed independently · pillar score = mean)

### 10.1 · Pass@k consistency measurement
- L0: not measured
- L1: anecdotal awareness
- L2: occasional spot-check
- L3: tracked on representative task set
- L4: continuous monitoring · regression alerts

### 10.2 · Retry & backoff logic
- L0: errors crash without retry
- L1: ad-hoc `try/except` around some calls
- L2: retry logic for known-flaky operations
- L3: documented backoff strategy (exponential · jitter · max retries)
- L4: retry policy per error class · circuit breaker pattern

### 10.3 · Idempotency for external actions
- L0: no consideration · double-writes possible
- L1: aware of risk · informal mitigation
- L2: idempotency considered for critical paths
- L3: idempotency keys on all external writes (API · DB · message queue)
- L4: idempotency enforced via type-level guarantees or schema validation

### 10.4 · MAST failure-mode coverage (14 modes · arXiv 2503.13657)
- L0: no awareness of MAST
- L1: aware · no instrumentation
- L2: 1-4 modes detectable in logs
- L3: 5-9 modes detectable + 3+ mitigated
- L4: 10+ modes detectable + 7+ mitigated · auto-triage

The 14 MAST failure modes (paraphrased):
1. Specification ambiguity (41.77% of observed failures · top mode)
2. Role drift
3. Inter-agent inconsistency
4. Termination failure
5. Reasoning errors
6. Tool-call malformation
7. Hallucinated state
8. Lost context across hops
9. Loop / repetition
10. Verification skipped
11. Premature halt
12. Wrong delegation
13. Goal abandonment
14. Output formatting failure

### 10.5 · Replay & failure forensics
- L0: failures discarded
- L1: failures logged but not replayable
- L2: structured logs allow manual replay
- L3: replay harness for any failed run from logged trace
- L4: automated root-cause clustering across failures

---

## Evidence sources

- **CLEAR** (arXiv [2511.14136](https://arxiv.org/abs/2511.14136)) · agent performance under cost control · pass@k consistency metric. Demonstrated 60→25% drop over 8 runs.
- **MAST** (arXiv [2503.13657](https://arxiv.org/abs/2503.13657)) · "Why Do Multi-Agent LLM Systems Fail?" · UC Berkeley Sky Lab · 14 failure modes across 3 categories · 41-86.7% MAS failure rate empirically.
- **AgenTracer** (arXiv [2509.03312](https://arxiv.org/abs/2509.03312)) · attribution of failures in multi-agent traces.
- **Google SRE Book** · idempotency, retry budgets, circuit breakers (chapter "Handling Overload").
- **Anthropic Demystifying Evals for AI Agents** · pass@k as core metric.

---

## Anti-patterns

- ❌ **Single-run benchmarks** as proof of production readiness. Run it 8 times.
- ❌ **Retry loops without backoff** · amplifies transient failures into cascading outages.
- ❌ **No idempotency keys** on external writes · double-charged customers · duplicated messages.
- ❌ **"It worked on my machine" deployment** without replay harness.
- ❌ **Generic error handling** that swallows failure-mode specifics (no MAST classification).

---

## Profiles

**Production-grade (L3-L4)**:
- `pass@k=8` tracked weekly on a fixed task suite · regression detected automatically
- Retry policy documented per error class · circuit breaker for downstream services
- Idempotency keys generated and enforced on every external action
- MAST taxonomy mapped: 5+ failure modes detectable in observability layer
- Replay harness: any failed run can be re-played from log trace + workspace snapshot

**Prototype-stage (L0-L1)**:
- Same task run twice gives different output · no tracking
- API errors crash the agent with no retry
- External actions can double-fire under network jitter
- "Sometimes it works" is the operator's mental model

---

## How to improve from low level

| From | To | Action |
|------|-----|--------|
| L0 → L2 | Document the existing non-determinism. Add `try/except + retry-once` to obvious flaky calls. Add idempotency keys to writes that matter (payments, messages, DB inserts). |
| L2 → L3 | Define a 10-task regression suite. Run `pass@k=8` weekly. Document retry policy per error class. Map workspace's observable failures to MAST taxonomy. |
| L3 → L4 | Build replay harness · failed run + workspace state → reproducible re-run. Auto-cluster failures by signature. Track determinism budget per task class. |

---

## Self-audit questions

- If you ran the most important task in your workspace 8 times right now, what would the success rate be?
- When a tool call fails transiently, what happens · how is "transient" defined?
- If your agent processed the same payment webhook twice, what would happen?
- Which of the 14 MAST failure modes can you currently detect in logs?

---

_Pillar 10 · v0.3 · 2026-05-19 · pattern source CLEAR (2511.14136) + MAST (2503.13657) · novel addition to public agentic workspace benchmarks_
