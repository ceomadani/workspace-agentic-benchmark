# Workspace Agentic Benchmark

> First-principles framework to evaluate the effectiveness of **agentic workspace infrastructures** for forward deploy engineering.

**Target users**: Forward Deploy Engineers (Anthropic FDE · Palantir FDE) · AI infrastructure builders · enterprise AI teams · solo operators running long-horizon agentic systems.

---

## The problem

Most agent benchmarks (SWE-bench · TAU-bench · AgentBench · GAIA · OSWorld · MLE-bench) evaluate **single-task model capability**. None evaluate the **workspace-level infrastructure** that determines whether an agent succeeds in production over weeks/months:

- Multi-tier memory architecture (semantic · episodic · procedural · personalized · env-dynamics)
- Skill discovery + staleness detection
- Governance gates (HARD RULES · compliance checks · approval flows)
- Auto-improvement loops (Dreams · Reflexion · ECHO · Voyager · A-MAC scoring)
- Multi-agent discipline (DPI · Stanford 2604.02460)
- Observability (cron health · liveness watchdog · drift detection)
- Credentials security (zero plaintext · secret manager)

This is the **L3 architectural layer** · what separates a demo from a production-grade agentic system.

---

## How to use

```bash
git clone https://github.com/ceomadani/workspace-agentic-benchmark.git
cd workspace-agentic-benchmark

# Audit your workspace
python3 eval/audit.py /path/to/your/workspace > audit.json

# Score against 7 pillars
python3 eval/score.py audit.json > score.json

# Generate report
python3 eval/report.py score.json --output report.html
```

Output: a 0-70 score across 7 pillars · grade A/B/C/D · plus per-pillar deep-dive with concrete recommendations.

---

## The 9 pillars

| # | Pillar | First-principle | Max |
|---|--------|------------------|-----|
| **[1](pillars/01-context-memory.md)** | Context Hierarchy & Memory | KV-cache aware multi-tier memory · forgetting policy explicit · retrieval precision over recall | 10 |
| **[2](pillars/02-skill-tool.md)** | Skill / Tool Architecture | Bounded granularity · auto-trigger discovery · staleness detection · determinism preferred | 10 |
| **[3](pillars/03-governance.md)** | Governance & Compliance | Constitution explicit · HARD RULES enumerated · pre-output gates · approval for irreversible | 10 |
| **[4](pillars/04-auto-improvement.md)** | Auto-Improvement Loop | Dreams/SleepGate · Reflexion verbal RL · A-MAC scoring · cron-driven (not on-demand) | 10 |
| **[5](pillars/05-multi-agent-dpi.md)** | Multi-Agent Discipline (DPI) | Single-thread default · multi-agent only with evidence + 2× budget · Explore-only pre-auth | 10 |
| **[6](pillars/06-observability.md)** | Observability & Recovery | Centralized logs · liveness watchdog · aggregate health · drift detector | 10 |
| **[7](pillars/07-credentials-security.md)** | Credentials & Security | Zero plaintext · secret manager · approval gates · audit log | 10 |
| **[8](pillars/08-portability.md)** | Portability & Re-deployability ⭐ | Bootstrap doc · client-agnostic skills · vault isolation · time-to-redeploy measured | 10 |
| **[9](pillars/09-metacognition.md)** | Metacognition & Self-Assessment ⭐ | MCU verbalized + capability profile · composite confidence · conflict detection · EMA cybernetic | 10 |
| | | **Total** | **90** |

⭐ Pillars 8 and 9 are **unique to this benchmark** · no public benchmark measures workspace re-deployability for FDE engagements (Pillar 8) or prospective metacognition for delegation gating (Pillar 9).

**Grades**: A (76+) · B (58-75) · C (39-57) · D (<39).

Read [METHODOLOGY.md](METHODOLOGY.md) for the first-principles derivation of each pillar.

---

## Reference example

[`examples/madani-reference.md`](examples/madani-reference.md) · the Madani workspace (50M EUR portfolio · iter-38 · production grade) as a gold-standard reference. Use it as a high-score case study to compare against your own.

---

## What's different from existing benchmarks

| Existing benchmark | What it measures | Gap |
|---|---|---|
| SWE-bench | Code repair on GitHub issues | Single task · no workspace infra |
| TAU-bench (Anthropic) | Tool-use long-horizon dialog | Conversational · no governance |
| AgentBench (Tsinghua) | 8 environments multi-task | Closed-world · no memory tiers |
| GAIA (Meta) | General assistant capability | Q&A · no auto-improvement |
| OSWorld | Real OS task completion | Single agent · no multi-cron |
| MLE-bench (OpenAI) | ML engineering on Kaggle | Specific ML · no compliance |
| Anthropic Effective Harnesses | Agent harness eval | Pattern source · no scoring rubric |

**This benchmark fills the workspace-level gap**: how well is the *infrastructure around the agent* built? Not the agent's raw capability · the harness it lives in.

---

## Research sources

[`research/SOURCES.md`](research/SOURCES.md) · 30+ papers and frameworks that ground each pillar in evidence.

Key papers:
- arXiv 2604.02460 (Stanford · DPI for single vs multi-agent)
- arXiv 2605.17292 (MetaCogAgent · prospective metacognition · May 2026)
- arXiv 2303.11366 (Reflexion · verbal reinforcement learning)
- arXiv 2305.16291 (Voyager · open-ended embodied agent)
- Anthropic "Effective Harnesses" blog series
- Cognition "Don't Build Multi-Agents" (steel-man)
- NousResearch hermes-agent (staleness curator pattern)

---

## License

MIT · forward-deploy friendly · fork and adapt for your enterprise context.

---

## Contributing

PRs welcome. If you've evaluated a workspace with this framework and learned something, open an issue with your case study · we maintain a `examples/` directory for community references.

To propose a new pillar or revise a scoring rubric, open a discussion first · changes to pillars require evidence (paper · production case study · measurable outcome).
