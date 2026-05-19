# Methodology · first-principles derivation

> Why these 7 pillars · why this scoring · what evidence grounds each choice.

---

## Design principles

**1. Workspace > Agent.**
A weak model in a great workspace beats a strong model in a chaotic workspace. We measure the infrastructure, not the model.

**2. Evidence-based.**
Every pillar traces to peer-reviewed research, production case studies, or measurable production outcomes. No "best practices" without source citation.

**3. Deterministic where possible.**
70% of the audit runs without an LLM call (file scanning · pattern matching · count metrics). LLM only used for qualitative assessment where deterministic signals run out.

**4. Forward-deployable.**
The framework must work on a wide variety of agentic stacks (Claude Code · Cursor · Cline · custom). No assumption that the workspace looks like ours.

**5. First-principles, not feature-counting.**
A pillar measures **a property** (e.g., "memory tier separation is enforced"), not a feature ("uses pgvector"). Implementation details matter less than architectural property.

---

## Derivation · the 7 pillars

### Pillar 1 · Context Hierarchy & Memory

**Why it matters**: Context window is the agent's primary bottleneck. Naive workspaces stuff everything into context → context degradation → DPI violation (Stanford 2604.02460). Production workspaces use tiered memory (semantic / episodic / procedural / personalized / environment-dynamics) with explicit retrieval policy.

**First principle**: *Information should flow into context only when needed, only the parts needed.*

**Evidence**:
- arXiv 2604.02460 · DPI (Data Processing Inequality) · context utilization is the choke point.
- Cognition "Don't Build Multi-Agents" · context handoff loss compounds across agents.
- ECHO (iter-35 Madani · environment-dynamics tier added) · agents need to model env state separately from semantic facts.

**Anti-pattern**: single-file context dump · no forgetting policy · no retrieval scoring.

---

### Pillar 2 · Skill / Tool Architecture

**Why it matters**: As skill counts grow (>20), discovery degrades. Stale skills poison agent behavior (they fire on wrong triggers). Determinism wins where possible (cheaper · faster · auditable).

**First principle**: *A skill is a contract with the agent · contracts must be discoverable, fresh, and minimal.*

**Evidence**:
- NousResearch hermes-agent · staleness curator pattern (auto-flag unused/stale skills).
- Anthropic skills documentation · auto-trigger via description matching.
- Voyager (arXiv 2305.16291) · skill library compositional + iterative refinement.

**Anti-pattern**: 50+ skills with no staleness check · grab-bag mega-skills · pure LLM tools where deterministic suffices.

---

### Pillar 3 · Governance & Compliance

**Why it matters**: Agents have no inherent moral or operational reasoning · they need explicit gates. Without HARD RULES, agents drift toward compliance theater (saying "sure!") and irreversible actions (pushing to main, sending external messages, dropping tables).

**First principle**: *Every irreversible or externally-visible action must pass an explicit gate. No silent execution.*

**Evidence**:
- Anthropic Constitutional AI (arXiv 2212.08073) · explicit principles outperform implicit alignment.
- Production incident pattern · ~80% of agent-caused harm comes from missing approval gates on external actions (Slack send · email · git push).
- Madani HR15 PRE-OUTPUT compliance check (5-criteria) · empirical reduction of drift.

**Anti-pattern**: no constitution · no HARD RULES list · no pre-output check · automatic external actions.

---

### Pillar 4 · Auto-Improvement Loop

**Why it matters**: Workspaces decay. Without an auto-improvement loop, agent quality drifts down over time as patterns get stale, skills get stale, and corrections are forgotten. Manual review doesn't scale.

**First principle**: *The workspace must learn from its own session history · automatically · on a schedule.*

**Evidence**:
- Reflexion (arXiv 2303.11366) · verbal reinforcement learning via session reflection.
- Voyager (arXiv 2305.16291) · skill library auto-grown from agent experience.
- Anthropic Managed Agents "Dreams" API · nightly compaction + improvement proposal.
- Madani A-MAC 6-factor scoring (iter-37) · automated assessment of proposed improvements.

**Anti-pattern**: improvements happen only when user notices · no cron-driven reflection · no scoring of proposed changes.

---

### Pillar 5 · Multi-Agent Discipline (DPI)

**Why it matters**: Multi-agent is fashionable but evidence-light. Stanford 2604.02460 shows single-agent dominates under equal token budget. Multi-agent only wins under 3 specific conditions (context already degraded · 2× budget available · evidence of need).

**First principle**: *Default to single-thread. Multi-agent is an exception with explicit justification.*

**Evidence**:
- arXiv 2604.02460 (Tran/Kiela Stanford) · "single-agent LLMs outperform multi-agent on multi-hop reasoning under equal thinking token budgets".
- Cognition steel-man · "context sharing between agents is the bottleneck".
- MAST framework · 14 documented multi-agent failure modes.

**Anti-pattern**: orchestrator-worker by default · sub-agent recursion · parallel division of tasks that don't require it.

**Exception (pre-authorized)**: Explore-only sub-agent for read-only exploration · protects primary context from large file scans.

---

### Pillar 6 · Observability & Recovery

**Why it matters**: Agents fail silently. Without centralized logs, liveness checks, and drift detectors, you discover failures only when the user notices. MTTD (mean time to detect) is the key infrastructure metric.

**First principle**: *Failure is the default. Detection must be automatic and fast.*

**Evidence**:
- Anthropic Effective Harnesses · aggregate-report pattern for health visibility.
- M08 6-state lifecycle (Madani iter-30+) · explicit state machine catches zombie tasks.
- Production reliability · MTTD reduction correlates with user trust more than MTBF.

**Anti-pattern**: scattered logs · no health summary · no zombie detector · "we'll notice if it breaks".

---

### Pillar 7 · Credentials & Security

**Why it matters**: Plaintext credentials in agent workspaces are the #1 production security incident. Agents have read access to everything by default. One leaked workspace = full credential dump.

**First principle**: *Zero plaintext credentials. Ever. Including "placeholder" patterns.*

**Evidence**:
- OWASP top 10 · A07 Identification and Authentication Failures.
- Production incident pattern · 60%+ of agent-related security incidents involve credentials checked into repos.
- 1Password CLI · HashiCorp Vault · runtime resolution patterns.

**Anti-pattern**: `.env` committed · API keys in markdown · tokens in URLs · placeholder `sk-ant-...` patterns.

---

## Scoring rubric

Each pillar scored 0-10 against a checklist of 10 binary criteria. Each criterion either passes (1.0), partially passes (0.5), or fails (0.0). Total clamped to 10.

**Grade thresholds** (total 0-90 · 9 pillars):
- **A** (76-90) · production-grade · forward-deployable
- **B** (58-75) · solid · needs hardening in 1-2 pillars
- **C** (39-57) · early-stage · multiple gaps
- **D** (0-38) · prototype · not production-ready

**Why these thresholds**: derived from Madani internal milestones (iter-20: C · iter-30: B · iter-37+: A) and empirical observation of FDE engagements where workspaces below the C threshold require infrastructure-first work before agent work. Thresholds remain proportional to the original 8-pillar scheme (A: ≥85% · B: ≥64% · C: ≥43%).

### Pillar 8 added · evidence

Initial 7-pillar framework was validated against 30+ existing benchmarks (research/SOURCES.md). The validation surfaced a **gap unique to FDE practice**: no public benchmark measures *re-deployability* of an agentic workspace across engagements. We added Pillar 8 (Portability & Re-deployability) based on:
- Palantir FDE doctrine (time-to-first-impact, harness portability)
- Anthropic FDE model (embedded engineers, customer-KPI-driven)
- MIT pilot failure research (95% of AI pilots fail · differentiator is infrastructure replicability)
- Cross-engagement memory leakage as documented P0 compliance risk in regulated industries

### Pillar 9 added · evidence (v0.2)

The 8-pillar framework had a measurement gap on multi-agent delegation: Pillar 5 (DPI) says "default single-thread unless evidence" but the "evidence" was operationally vague. The **MetaCogAgent paper** (arXiv 2605.17292v1 · Wang/Shu · 17 May 2026) provides the missing operational mechanism: prospective metacognition via Metacognitive Unit (MCU) with verbalized + profile-based composite confidence, conflict detection, and cybernetic feedback loop on capability profile.

We added Pillar 9 (Metacognition & Self-Assessment) based on:
- MetaCogAgent · 82.4% accuracy · -34% API calls · ECE 0.087 (well-calibrated · vs 0.194 Single-Agent overconfident)
- Kadavath et al. (arXiv 2207.05221) · LLMs "(mostly) know what they know" · poor calibration baseline
- Guo et al. (ICML 2017) · ECE metric for calibration measurement
- Direct operational pairing with Pillar 5: MetaCog `c < θ` *is* the DPI 3rd condition evidence trigger

This is the second pillar unique to this benchmark (alongside Pillar 8 · Portability). No public benchmark currently measures prospective metacognition for delegation gating.

---

## What this benchmark does NOT measure

- **Model quality** (use SWE-bench · TAU-bench · GAIA for that)
- **Cost per task** (orthogonal · model-dependent)
- **Domain-specific accuracy** (your job · we measure infrastructure that enables it)
- **UI/UX of the agent interface** (irrelevant at the infra layer)

These are downstream metrics. This benchmark measures the upstream conditions that make those metrics achievable.

---

## Limitations · honest disclosure

1. **Bias toward our reference architecture**: pillars 4 and 5 reflect Madani's choices (Dreams · Reflexion · DPI guard). Other valid architectures may score lower despite being effective. We welcome PRs documenting alternative valid architectures.

2. **Snapshot, not trajectory**: scores reflect current state · not improvement velocity. A score going from D → B in 3 months matters more than a static A. We recommend running the benchmark monthly and tracking deltas.

3. **Self-report risk**: the audit reads workspace files · it can be gamed by stuffing keywords. Use score as a starting point · validate qualitatively.

4. **Cultural variance**: governance pillars assume Western-style explicit-rule cultures. Workspaces operating in implicit-norm cultures may need rubric adjustment.

---

## Versioning

- **v0.1** (2026-05-19) · initial release · 7 pillars · Madani as reference.
- Future revisions: add pillars only with strong evidence (paper + production validation) · revise rubrics with documented case studies.

---

## Citation

If you use this benchmark in research or FDE engagements, cite:

```
Matine, N. (2026). Workspace Agentic Benchmark · First-Principles Framework for
Evaluating Agentic Workspace Infrastructures. https://github.com/ceomadani/workspace-agentic-benchmark
```
