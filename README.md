# Workspace Agentic Benchmark

> First-principles framework to evaluate the effectiveness of **agentic workspace infrastructures** for forward deploy engineering.

**Target users**: Forward Deploy Engineers (Anthropic FDE · Palantir FDE · OpenAI deployment teams) · AI infrastructure builders · enterprise AI teams · solo operators running long-horizon agentic systems.

**Current version**: v0.3 · 12 pillars in 4 clusters · L0-L4 maturity model + composite 0-100 weighted scoring.

---

## The problem

Most agent benchmarks (SWE-bench · TAU-bench · AgentBench · GAIA · OSWorld · MLE-bench) evaluate **single-task model capability**. None evaluate the **workspace-level infrastructure** that determines whether an agent succeeds in production over weeks and months.

This is the **L3 architectural layer** · what separates a demo from a production-grade agentic system. A weak model in a great workspace beats a strong model in a chaotic workspace. We measure the workspace.

> "Agent benchmark scores are measuring the harness, not the model." — Focused Labs (2026)

The Anthropic harness research (Nov 2025 + Mar 2026) demonstrated that swapping the harness alone moved benchmark scores from 87.2% → 91.1% (+3.9pp) *without changing the model*. This benchmark measures the harness.

---

## How to use

**Install** (recommended · pip from GitHub):

```bash
pip install git+https://github.com/ceomadani/workspace-agentic-benchmark.git
```

**Score your workspace in one command** (audit + score + HTML report with live progress):

```bash
workspace-bench run /path/to/your/workspace --output-dir ./bench-output
```

This produces a sophisticated terminal display (slash-context style · pillar maturity dots · cluster aggregation · improvement priorities) and writes `audit.json` · `score.json` · `report.html` to the output directory.

**Subcommands** (when you need them separately):

```bash
workspace-bench audit /path/to/workspace > audit.json
workspace-bench score audit.json --output score.json
workspace-bench report score.json --output report.html
```

**Or use the agent self-audit prompt** (no install required · copy into Claude Code · Cursor · or any LLM with file-system tools):

> Read https://github.com/ceomadani/workspace-agentic-benchmark/blob/main/METHODOLOGY.md . Then walk my workspace at `/path/to/workspace`, score it against the 12 pillars using L0-L4 maturity levels (0/20/50/75/100), and output a report with the top 3 improvement priorities. Be honest · default to lower levels when evidence is missing.

**Or clone + run via Python module** (no install · uses local code):

```bash
git clone https://github.com/ceomadani/workspace-agentic-benchmark.git
cd workspace-agentic-benchmark
python3 -m workspace_bench run /path/to/your/workspace --output-dir ./bench-output
```

Output: per-pillar maturity level (L0-L4) · weighted composite score (0-100) · grade (A/B/C/D/F) · per-pillar deep-dive · concrete improvement actions for advancing to the next level.

---

## The 12 pillars · 4 clusters

### Cluster A · Cognition (3 pillars · the agent's mind)

| # | Pillar | First-principle |
|---|--------|------------------|
| **[1](pillars/01-context-memory.md)** | Context Hierarchy & Memory | KV-cache aware multi-tier memory · forgetting policy explicit · retrieval precision over recall |
| **[4](pillars/04-auto-improvement.md)** | Auto-Improvement Loop | Workspace learns from its own session history · automatically · on a schedule |
| **[9](pillars/09-metacognition.md)** | Metacognition & Self-Assessment | Agent must know what it doesn't know · before acting · not after failing |

### Cluster B · Action (3 pillars · how it executes)

| # | Pillar | First-principle |
|---|--------|------------------|
| **[2](pillars/02-skill-tool.md)** | Skill / Tool Architecture | Bounded granularity · auto-trigger discovery · staleness detection · determinism preferred |
| **[5](pillars/05-multi-agent-dpi.md)** | Multi-Agent Discipline (DPI) | Single-thread default · multi-agent only with evidence + 2× budget · Explore-only pre-auth |
| **[10](pillars/10-reliability.md)** ⭐ | Reliability & Determinism | An agent that succeeds once in 8 tries is not a system · pass@k consistency measured |

### Cluster C · Trust (4 pillars · safety and governance)

| # | Pillar | First-principle |
|---|--------|------------------|
| **[3](pillars/03-governance.md)** | Governance & Compliance | Every irreversible action must pass an explicit gate · no silent execution |
| **[6](pillars/06-observability.md)** | Observability & Recovery | Failure is the default · detection must be automatic and fast · MTTD > MTBF |
| **[7](pillars/07-credentials-security.md)** | Credentials & Security | Zero plaintext credentials · ever · including placeholder patterns · OWASP LLM Top 10 mapped |
| **[11](pillars/11-human-in-the-loop.md)** ⭐ | Human-in-the-Loop | Most consequential decisions pass through a human gate · workspace makes the gate easy |

### Cluster D · Operations (2 pillars · production readiness)

| # | Pillar | First-principle |
|---|--------|------------------|
| **[8](pillars/08-portability.md)** ⭐ | Portability & Re-deployability | Re-deployable on new engagement in days, not months · FDE-grade · cross-engagement isolation |
| **[12](pillars/12-cost-performance.md)** ⭐ | Cost & Performance Efficiency | Token economics decide deployment viability · harness not model · cache hit ≥ 80% |

⭐ = unique to this benchmark · no public benchmark currently measures these dimensions for workspace-level evaluation.

---

## Scoring system · L0-L4 maturity + composite 0-100

**Per-pillar maturity levels** (CMMI-inspired):

| Level | Score | Profile |
|-------|------:|---------|
| **L0 Absent** | 0 | Pillar doesn't exist in workspace |
| **L1 Initial** | 20 | Ad-hoc · undocumented · operator's head only |
| **L2 Managed** | 50 | Documented · manually executed |
| **L3 Defined** | 75 | Enforced via tools/hooks · automated |
| **L4 Optimizing** | 100 | Auto-improves · measured · cybernetic feedback loop |

**Composite score** = weighted average across 12 pillars (default: equal weight 1/12 per pillar).

**Grades** (composite 0-100):
- **A** (≥85) · production-grade · forward-deployable
- **B** (≥70) · solid · needs hardening in 1-2 pillars
- **C** (≥50) · early-stage · multiple gaps
- **D** (≥30) · prototype · not production-ready
- **F** (<30) · failing · infrastructure-first work required

Why L0-L4: pure 0-10 is opaque ("a 7 means what?"). CMMI-inspired levels are **actionable** ("you're L2 · here's how to reach L3"). Used by AWS Well-Architected, NIST AI RMF, MLPerf, OWASP — proven in industry for two decades.

Read [METHODOLOGY.md](METHODOLOGY.md) for the first-principles derivation of each pillar and scoring decisions.

---

## Reference examples

[`examples/`](examples/) ships with real audits from production workspaces — see [`examples/README.md`](examples/README.md) for the catalog. The included case studies span:

- A high-score solo-operator workspace (composite 85.75 · grade A) · in `madani-reference.md` + time-series `madani-v0XX/` showing iter-1 → iter-2 evolution
- External audits of public agentic stacks (OpenAI Agents · LangChain · CrewAI · AutoGen · Anthropic Cookbook · Anthropic Claude SDK) in `examples/external/` for cross-stack comparison

These are reference points to calibrate L3/L4 expectations. **Do NOT copy them to your workspace** — your audit produces its own files when you run `workspace-bench`. PRs adding additional case studies welcome.

---

## What's different from existing benchmarks

| Existing | What it measures | Gap |
|---|---|---|
| SWE-bench | Code repair on GitHub issues | Single task · no workspace infra |
| TAU-bench | Tool-use long-horizon dialog | Conversational · no governance |
| AgentBench | 8 environments multi-task | Closed-world · no memory tiers |
| GAIA | General assistant capability | Q&A · no auto-improvement |
| OSWorld | Real OS task completion | Single agent · no multi-cron |
| MLE-bench | ML engineering on Kaggle | Specific ML · no compliance |
| CLEAR | Enterprise cost-controlled eval | Trajectory-based · no workspace structural axes |
| MAST | Multi-agent failure taxonomy | Post-hoc failure analysis · not prospective measurement |
| HELM | LLM holistic evaluation | Model-centric · not workspace-centric |
| Anthropic Effective Harnesses | Agent harness doctrine | Prescriptive blog · no scoring rubric |

**This benchmark fills the workspace-level gap**: how well is the *infrastructure around the agent* built? Not the agent's raw capability · the harness it lives in.

---

## Research foundation

[`research/SOURCES.md`](research/SOURCES.md) · 40+ papers and frameworks that ground each pillar in evidence.

Key papers:
- arXiv 2604.02460 (Stanford · DPI for single vs multi-agent)
- arXiv 2605.17292 (MetaCogAgent · prospective metacognition · May 2026)
- arXiv 2511.14136 (CLEAR · enterprise cost-controlled eval · Nov 2025)
- arXiv 2503.13657 (MAST · 14 multi-agent failure modes · NeurIPS 2025)
- arXiv 2303.11366 (Reflexion · verbal reinforcement learning)
- arXiv 2305.16291 (Voyager · skill library + auto-curriculum)
- NIST AI RMF 1.0 + AAGATE (arXiv 2510.25863) · governance frameworks
- OWASP LLM Top 10 2025
- Anthropic "Effective Harnesses" + "Demystifying Evals for AI Agents"

---

## Contribute

PRs welcome. If you've evaluated a workspace with this framework and learned something, open an issue with your case study · we maintain a `examples/` directory for community references.

To propose a new pillar or revise a scoring rubric, use the [RFC process](RFC/README.md) · changes to pillars require evidence (paper · production case study · measurable outcome).

To submit your workspace audit to the public leaderboard, see [`submissions/README.md`](submissions/README.md) (MLPerf-style PR-based · evidence required).

See [CONTRIBUTING.md](CONTRIBUTING.md) for full contribution guidelines.

---

## Known biases · validity threats

This benchmark was developed by [Madani](https://madani.agency) and Madani's workspace currently ranks #1 (87.08/100 · grade A under v0.4 cap). That is a credibility red flag if not disclosed. This section discloses the limitations openly · readers can adjust their trust accordingly.

### Genesis bias · framework shaped by Madani case-study

The 12 pillars and their L0-L4 maturity descriptors were derived studying what works in the Madani workspace as a positive case-study, alongside peer-reviewed research. Patterns that Madani implements (Hermes-stale daily cron · Curator weekly · Reflexion 23:30 · auto-promote-engine · 5-tier memory · capability profile EMA) are codified as audit criteria. The framework was not designed in vacuum then applied to Madani · it was co-developed.

**Concrete consequence**: workspaces architecturally similar to Madani score higher · not because they are objectively better at all goals, but because they are better at the goals this rubric measures.

**Mitigation in v0.4 · L4 soft cap 95/100**: pure documentation-based scoring saturated too easily for workspaces that authored the rubric (Madani had 3 pillars at L4=100 → cluster B average 100.0 · structurally suspicious). v0.4 caps L4=95 and L3=70 · reserving 5 points per pillar for **runtime enforcement evidence** to be measured in v0.5. The cap deflates genesis-biased scores proportionally: Madani -4.59 (had many L4) · Hermes -2.50 (some L4) · workspaces with mostly L0-L2 unchanged. Proportional deflation = agnostic correction.

**Mitigation in v0.3.3**: ~70% of audit is deterministic file-pattern matching (low LLM judgment surface). Vendor neutrality tested: Anthropic Cookbook scores F (27.5) despite Anthropic being the model provider Madani uses · LangChain/CrewAI/AutoGen all F · Hermes-agent (NousResearch · 165k★ · zero Madani contamination) C (50.83) · scores reflect architecture quality, not vendor allegiance.

### Scoring is deterministic · selection is not

The 12-pillar list and the 10 criteria per pillar were chosen · choosing what to measure is itself a worldview. A UX-focused benchmark would rank Aider/Cursor/Cline higher. An adoption-focused benchmark would rank LangChain (massive ecosystem) higher. A production-scale benchmark would rank Vercel AI SDK (streaming efficiency) higher.

**WAB benchmarks autonomous workspace governance.** That is one valid dimension of agentic quality. It is not the only dimension.

### What WAB does NOT measure

| Dimension | Not measured | Where to look instead |
|-----------|--------------|------------------------|
| Developer UX / DX | ❌ | SWE-Bench · HumanEval · qualitative reviews |
| Adoption / ecosystem health | ❌ | GitHub stars · npm/pip downloads · contributor count |
| Ease of getting started | ❌ | Tutorial completion benchmarks · time-to-first-success |
| Production scale efficiency | ❌ | Inference cost benchmarks · latency P99 measurements |
| Plugin / extension ecosystem | ❌ | Marketplace size · third-party integration count |
| Model integration breadth | ❌ | Provider matrix audits |
| End-user task completion | ❌ | TaskBench · AgentBench · WebArena |

**Read WAB alongside these, not instead of them.** A workspace can be excellent for its purpose and score low here · the question is whether autonomous governance is one of its design priorities.

### What we are doing to reduce bias (v0.4 roadmap)

- **External rubric review** · invite maintainers of Hermes · OpenClaw · Cline · Aider · LangChain to propose pillar modifications via the RFC process · audit log all changes
- **Multi-profile scoring** · publish alternative weight profiles (UX-focused · adoption-focused · production-scale · DX-focused) alongside the default · users select the lens that matches their goal
- **Pillar provenance disclosure** · annotate each pillar with whether it derives from peer-reviewed paper, external case study, or Madani case study · transparency
- **Independent reproduction badge** · invite third parties to audit the Madani workspace and verify the 91.67 score reproduces · publish their findings unaltered
- **Inter-rater reliability protocol** · publish two-evaluator score comparisons to quantify subjectivity remaining after determinism

### Reading guidance

- Treat WAB as a **specific lens** on a specific dimension (autonomous governance)
- Madani's #1 rank is real within that lens · not a universal claim of "best agentic workspace"
- A grade-F result in WAB is not a criticism of the workspace audited · it is a measurement of how much of its architecture is shaped by the properties this rubric measures
- If your priority is something else (UX, adoption, ease, plugins), the WAB score is information but not the answer

---

## License

MIT · forward-deploy friendly · fork and adapt for your enterprise context.

---

## Roadmap

- **v0.3** (current · May 2026) · 12 pillars · L0-L4 + composite · MAST + OWASP integration · submissions scaffold
- **v0.4** (target Q3 2026) · 3+ external workspace audits · website live · CLI package (`pip install workspace-bench`)
- **v0.5** (target Q4 2026) · NeurIPS / ICLR workshop paper · LangSmith / AgentOps adapters · inter-rater reliability protocol
- **v1.0** (target Q1 2027) · vendor-neutral org migration · MLCommons-style consortium · de-facto standard for FDE engagements

See [CHANGELOG.md](CHANGELOG.md) for version history.
