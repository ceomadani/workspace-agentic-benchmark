# Methodology · first-principles derivation

> Why these 12 pillars · why L0-L4 maturity scoring · what evidence grounds each decision.

---

## Design principles

**1. Architecture-Capability Decoupling** *(iter-2 formalization)*
The output quality of an agent equals workspace alpha multiplied by model capability: `output = α(workspace) × capability(LLM)`. The workspace term `α` is itself the geometric mean of file-quality and file-quantity, multiplied by index density: `α = √(quality × quantity) × density_indices`. Hypothesis: well-designed workspace × weak LLM outperforms poor workspace × strong LLM. The benchmark exists to measure `α` independently of model choice. See [`extensions/01-architecture-capability-decoupling.md`](extensions/01-architecture-capability-decoupling.md) for the full derivation and operational consequences.

**2. Evidence-based.**
Every pillar traces to peer-reviewed research, production case studies, or measurable production outcomes. No "best practices" without source citation.

**3. Deterministic where possible.**
~70% of the audit runs without an LLM call (file scanning · pattern matching · count metrics). LLM only used for qualitative assessment where deterministic signals run out.

**4. Forward-deployable.**
The framework must work across a wide variety of agentic stacks (Claude Code · Cursor · Cline · LangChain · CrewAI · AutoGen · custom). No assumption that the workspace looks like ours.

**5. First-principles, not feature-counting.**
A pillar measures **a property** (e.g., "memory tier separation is enforced"), not a feature ("uses pgvector"). Implementation details matter less than architectural property.

**6. Actionable maturity over opaque scores.**
0-10 per-pillar (v0.1-v0.2) was opaque ("a 7 means what?"). v0.3 adopts CMMI-inspired L0-L4 maturity levels: each level has a clear profile and a clear path to the next.

---

## The 12 pillars · derivation

### Cluster A · Cognition (the agent's mind)

#### Pillar 1 · Context Hierarchy & Memory

**Why it matters**: Context window is the agent's primary bottleneck. Naive workspaces stuff everything into context → context degradation → DPI violation (Stanford 2604.02460). Production workspaces use tiered memory (semantic / episodic / procedural / personalized / environment-dynamics) with explicit retrieval policy.

**First principle**: *Information should flow into context only when needed, only the parts needed.*

**Evidence**:
- arXiv 2604.02460 · DPI (Data Processing Inequality) · context utilization is the choke point.
- Cognition "Don't Build Multi-Agents" · context handoff loss compounds across agents.
- ECHO pattern (Shrivastava & Papailiopoulos 2026) · environment-dynamics as a distinct memory tier.
- CoALA (Cognitive Architectures for Language Agents) · semantic / episodic / procedural taxonomy foundation.
- MemGPT (arXiv 2310.08560) · virtual context management.

---

#### Pillar 4 · Auto-Improvement Loop

**Why it matters**: Workspaces decay. Without an auto-improvement loop, agent quality drifts down over time. Manual review doesn't scale.

**First principle**: *The workspace must learn from its own session history · automatically · on a schedule.*

**Evidence**:
- Reflexion (arXiv 2303.11366) · verbal reinforcement learning via session reflection.
- Voyager (arXiv 2305.16291) · skill library auto-grown from agent experience.
- Anthropic Managed Agents "Dreams" API · nightly compaction + improvement proposal.
- DGM Darwin-Gödel Machine (arXiv 2505.22954) · self-improving agents · SWE-bench 20 → 50%.
- A-MAC pattern · multi-factor proposal scoring.

---

#### Pillar 9 · Metacognition & Self-Assessment

**Why it matters**: Agents execute every task with implicit confidence, then fail silently or visibly. Prospective metacognition — assessing competence *before* execution — separates systems that know their boundaries from those producing confident garbage.

**First principle**: *An agent must know what it doesn't know · before acting · not after failing.*

**Evidence**:
- MetaCogAgent (arXiv 2605.17292) · primary reference · 82.4% accuracy · ECE 0.087 · -34% API calls.
- Kadavath et al. (arXiv 2207.05221) · "Language Models (Mostly) Know What They Know" · poor calibration baseline.
- Xiong et al. (arXiv 2306.13063) · confidence elicitation strategies.
- Guo et al. (ICML 2017) · Expected Calibration Error (ECE) metric.
- Flavell (1979) · metacognition framework (cognitive science origin).

---

### Cluster B · Action (how it executes)

#### Pillar 2 · Skill / Tool Architecture

**Why it matters**: As skill counts grow past 20, discovery degrades. Stale skills fire on wrong triggers and poison agent behavior. Determinism wins where possible.

**First principle**: *A skill is a contract with the agent · contracts must be discoverable, fresh, and minimal.*

**Evidence**:
- NousResearch hermes-agent · staleness curator pattern.
- Voyager (arXiv 2305.16291) · skill library compositional + iterative refinement.
- EvoSkill (arXiv 2603.02766) · auto skill discovery from failure analysis.
- SkillFlow (arXiv 2604.17308) · lifelong skill discovery + evolution benchmark.

---

#### Pillar 5 · Multi-Agent Discipline (DPI)

**Why it matters**: Multi-agent is fashionable but evidence-light. Stanford 2604.02460 shows single-agent dominates under equal token budget. Multi-agent only wins under 3 specific conditions.

**First principle**: *Default to single-thread. Multi-agent is an exception with explicit justification.*

**Evidence**:
- arXiv 2604.02460 (Tran/Kiela Stanford) · DPI theorem.
- Cognition "Don't Build Multi-Agents" · steel-man · context sharing is the bottleneck.
- MAST framework (arXiv 2503.13657) · 14 documented multi-agent failure modes · 41-86.7% failure rate.

---

#### Pillar 10 · Reliability & Determinism ⭐ NEW

**Why it matters**: CLEAR (arXiv 2511.14136) demonstrated agent performance drops from 60% single-run to 25% over 8 runs. MAST documents 41-86.7% multi-agent failure rates. Workspaces that don't measure determinism ship demos that fail under production load.

**First principle**: *An agent that succeeds once in eight tries is not a system — it is a coin flip.*

**Evidence**:
- CLEAR (arXiv 2511.14136) · pass@k consistency under cost control.
- MAST (arXiv 2503.13657) · 14 failure modes empirically catalogued.
- AgenTracer (arXiv 2509.03312) · multi-agent failure attribution.
- Google SRE Book · idempotency, retry budgets, circuit breakers.

---

### Cluster C · Trust (safety and governance)

#### Pillar 3 · Governance & Compliance

**Why it matters**: Agents have no inherent moral or operational reasoning · they need explicit gates. ~80% of agent-caused production harm comes from missing approval gates.

**First principle**: *Every irreversible or externally-visible action must pass an explicit gate. No silent execution.*

**Evidence**:
- Anthropic Constitutional AI (arXiv 2212.08073) · explicit principles outperform implicit alignment.
- NIST AI RMF 1.0 · Govern function as core control.
- AAGATE (arXiv 2510.25863) · NIST-aligned governance for agentic AI.
- Pre-output compliance check pattern · empirical drift reduction.

---

#### Pillar 6 · Observability & Recovery

**Why it matters**: Agents fail silently. Without centralized logs, liveness checks, drift detectors, you discover failures only when the user notices. MTTD is the key infrastructure metric.

**First principle**: *Failure is the default. Detection must be automatic and fast.*

**Evidence**:
- Anthropic Effective Harnesses · aggregate-report pattern.
- AgentTrace (arXiv 2602.10133) · structured logging · OTEL-native.
- OpenTelemetry GenAI semantic conventions (2025).
- Google SRE book · MTTD > MTBF for user trust.

---

#### Pillar 7 · Credentials & Security

**Why it matters**: Plaintext credentials are the #1 production security incident. OWASP LLM Top 10 2025 added Excessive Agency (LLM06) and System Prompt Leakage (LLM07) explicitly for agentic workspaces.

**First principle**: *Zero plaintext credentials. Ever. Including "placeholder" patterns.*

**Evidence**:
- OWASP LLM Top 10 2025 · LLM02 Sensitive Disclosure · LLM06 Excessive Agency · LLM07 System Prompt Leakage · LLM10 Unbounded Consumption.
- RAS-Eval (arXiv 2506.15253) · 80 cases × 3802 attacks · 11 CWE categories.
- Agent Security Bench (arXiv 2410.02644) · 10 scenarios × 400 tools × 27 attack/defense × 7 metrics.
- SEC-bench (arXiv 2506.11791) · containerized security tasks.

---

#### Pillar 11 · Human-in-the-Loop ⭐ NEW

**Why it matters**: MAST taxonomy: specification ambiguity = 41.77% of multi-agent failures (top mode). Escalation prevents most of these. Yet escalation paths are systematically under-measured.

**First principle**: *The most consequential decisions must pass through a human gate · and the workspace must make that gate easy to use.*

**Evidence**:
- MAST (arXiv 2503.13657) · spec failure top mode at 41.77%.
- NIST AI RMF 1.0 · Govern function · human oversight as core control.
- AAGATE (arXiv 2510.25863) · explicit human-in-the-loop functions.
- Production postmortems · most-cited cause of agent-caused harm is automated execution that should have escalated.

---

### Cluster D · Operations (production readiness)

#### Pillar 8 · Portability & Re-deployability

**Why it matters**: Forward Deploy Engineering (FDE) key metric is time-to-first-impact. MIT shows 95% of AI pilots fail. Differentiator between failed pilots and shipped systems is harness portability.

**First principle**: *A workspace must be re-deployable on a new engagement in days, not months. FDE-grade.*

**Evidence**:
- Palantir FDE doctrine · time-to-first-impact · harness portability.
- Anthropic FDE model · embedded engineers · customer-KPI-driven.
- MIT pilot failure research · 95% failure rate · infrastructure replicability as differentiator.
- Cross-engagement memory leakage · documented P0 compliance risk.

---

#### Pillar 12 · Cost & Performance Efficiency ⭐ NEW

**Why it matters**: CLEAR documented 50× cost variations for same precision. Anthropic harness research: harness swap = +4pp benchmark gain without changing model. Workspaces ignoring cost economics bankrupt customers in production.

**First principle**: *Token economics decide deployment viability · harness, not model.*

**Evidence**:
- CLEAR (arXiv 2511.14136) · 50× cost variation enterprise tasks.
- Anthropic harness research (Nov 2025 + Mar 2026) · "harness, not model".
- Focused Labs "Agent Benchmark Scores Are Measuring the Harness, Not the Model" (2026).
- Anthropic prompt caching · 90% cost reduction on cached tokens · 5-min TTL.

---

## Scoring system

### L0-L4 maturity per pillar (CMMI-inspired)

| Level | Score | Profile |
|-------|------:|---------|
| **L0 Absent** | 0 | Pillar doesn't exist in workspace |
| **L1 Initial** | 20 | Ad-hoc · undocumented · operator's head only |
| **L2 Managed** | 50 | Documented · manually executed |
| **L3 Defined** | 75 | Enforced via tools/hooks · automated |
| **L4 Optimizing** | 100 | Auto-improves · measured · cybernetic feedback loop |

**Why L0-L4 over 0-10**:
- 0-10 is opaque ("what's a 7?"). L0-L4 is actionable ("you're L2 · here's how to reach L3").
- CMMI proven in industry for 30+ years (ISO 15504 adjacent).
- Adopted by AWS Well-Architected, NIST AI RMF, MLPerf, OWASP — established convention.
- Each level has a binary "you crossed the threshold" criterion · less subjective.

### Composite weighted score (0-100)

```
composite = Σ (pillar_level_score × pillar_weight)
```

**Default weights** (v0.3): equal weight 1/12 per pillar. Justification: equal weights reduce subjective judgment about pillar importance · easier to defend · alternative weightings can be derived empirically in v0.4 via correlation analysis across 10+ workspace audits.

**Weights file**: `eval/weights.json` · users can override for domain-specific evaluation (e.g., financial services may up-weight Pillars 3, 7, 11).

### Grade thresholds

| Grade | Composite | Profile |
|-------|----------:|---------|
| **A** | ≥ 85 | Production-grade · forward-deployable · FDE-engagement ready |
| **B** | ≥ 70 | Solid · 1-2 pillars need hardening before scale |
| **C** | ≥ 50 | Early-stage · multiple gaps · workspace work needed alongside agent work |
| **D** | ≥ 30 | Prototype · not production-ready · infrastructure-first work required |
| **F** | < 30 | Failing · workspace not fit for purpose |

**Why these thresholds**: empirically derived from grade conventions in AWS Well-Architected · OWASP risk tiers · MLPerf compliance gates · academic grading scales. Provides A-F distribution under bell-curve assumption across diverse workspaces.

---

## What this benchmark does NOT measure

- **Model quality** (use SWE-bench · TAU-bench · GAIA for that)
- **Single-task accuracy** (orthogonal · model-dependent)
- **Domain-specific accuracy** (your job · we measure infrastructure that enables it)
- **UI/UX of the agent interface** (irrelevant at the infra layer)

These are downstream metrics. This benchmark measures the upstream conditions that make those metrics achievable.

---

## Limitations · honest disclosure

1. **Bias toward reference architecture patterns**: pillars 4 and 5 are informed by specific patterns (Dreams · Reflexion · DPI guard). Other valid architectures may score lower despite being effective. PRs documenting alternative valid architectures welcome — particularly from teams using different stacks (LangChain · LangGraph · CrewAI · AutoGen · custom).

2. **Snapshot, not trajectory**: scores reflect current state · not improvement velocity. A score going from D → B in 3 months matters more than a static A. Recommended: run benchmark monthly · track deltas.

3. **Self-report risk**: the audit reads workspace files · it can be gamed by stuffing keywords. Use score as a starting point · validate qualitatively · require evidence artifacts in submissions/.

4. **Cultural variance**: governance pillars assume Western-style explicit-rule cultures. Workspaces in implicit-norm cultures may need rubric adjustment.

5. **Goodhart's law risk**: once people optimize for the score, rubrics need to evolve. v0.3 introduces RFC process for rubric revision · annual major version refresh planned.

6. **Equal weights are a starting point**: v0.3 uses 1/12 per pillar by default. v0.4 will derive empirical weights from correlation analysis once we have 10+ external audits.

---

## Versioning

- **v0.1** (2026-05-19) · initial release · 7 pillars · 0-10 scoring.
- **v0.2** (2026-05-19) · added Pillar 8 (Portability) · 8-pillar release.
- **v0.2.1** (2026-05-19) · added Pillar 9 (Metacognition · MetaCogAgent integration) · vendor-neutral cleanup.
- **v0.3** (2026-05-19) · 12 pillars in 4 clusters · L0-L4 maturity model + weighted composite 0-100 · 3 new pillars: Reliability/Determinism (10), Human-in-the-Loop (11), Cost/Performance (12). MAST + OWASP LLM Top 10 + NIST AI RMF integrated. Submissions and RFC scaffolds.

See [CHANGELOG.md](CHANGELOG.md) for full version history.

---

## Citation

If you use this benchmark in research or FDE engagements, cite:

```
Matine, N. (2026). Workspace Agentic Benchmark · First-Principles Framework for
Evaluating Agentic Workspace Infrastructures (v0.3). Madani Lab.
https://github.com/ceomadani/workspace-agentic-benchmark
```
