# Research Sources

> Evidence base for the 12 pillars · 40+ papers and frameworks 2022-2026.

---

## Existing benchmarks · what each measures and where it falls short

| Name | Org | Year | Focus | Gap (why we need pillar X) | URL |
|---|---|---|---|---|---|
| **SWE-bench / Verified / Pro** | Princeton + OpenAI | 2023-25 | Resolve real GitHub issues; patch generation | Single-shot · no memory/state · measures model+harness conflated | [2310.06770](https://arxiv.org/abs/2310.06770) · [Pro 2509.16941](https://arxiv.org/abs/2509.16941) |
| **TAU-bench (τ-bench)** | Sierra Research | 2024 | Tool-Agent-User multi-turn · policy adherence · pass^k reliability | Domain-specific (retail/airline) · no workspace/memory tier | [2406.12045](https://arxiv.org/abs/2406.12045) |
| **AgentBench** | Tsinghua | 2023 | 8 environments multi-task | Stateless episodes · no auto-improvement · no observability axis | [2308.03688](https://arxiv.org/abs/2308.03688) |
| **GAIA** | Meta + HF + AutoGPT | 2023 | General assistant: reasoning + multimodal + tool use · 466 Qs | Single-question · no long-running state · human 92% vs GPT-4 15% | [2311.12983](https://arxiv.org/abs/2311.12983) |
| **OSWorld** | XLang (HKU/Tianjin) | 2024 | 369 real computer tasks · GUI+keyboard+mouse · NeurIPS 2024 | OS-bound · ignores credentials policy · memory architecture | [2404.07972](https://arxiv.org/abs/2404.07972) |
| **MLE-bench** | OpenAI | 2024 | 75 Kaggle ML eng. competitions · medal-rate scoring | ML-engineering only · no governance/memory/multi-agent | [2410.07095](https://arxiv.org/abs/2410.07095) |
| **WebArena** | CMU | 2023 | 812 tasks across 4 self-hosted web apps | Browser-only · no skill library · no auto-improvement | [2307.13854](https://arxiv.org/abs/2307.13854) |
| **AgentBoard** | HKUST | 2024 NeurIPS | Fine-grained progress · 9 tasks · 1013 envs · sub-skill breakdown | No memory-tier · no credentials/security axis | [2401.13178](https://arxiv.org/abs/2401.13178) |
| **HELM** | Stanford CRFM | 2022+ | 7 metrics × 16 scenarios: accuracy · calibration · robustness · etc | Model-centric · not workspace-centric | [2211.09110](https://arxiv.org/abs/2211.09110) |
| **CLEAR** | (CLEAR authors) | 2025 | Cost · Latency · Efficacy · Assurance · Reliability · enterprise focus | Trajectory-based · no workspace structural axes | [2511.14136](https://arxiv.org/abs/2511.14136) |
| **MetaCogAgent / MEDLEY-BENCH** | Wang/Shu | 2026 | Behavioral metacognition · MCU · 130 ambiguous instances | Metacognition-only · not full workspace | [2605.17292](https://arxiv.org/abs/2605.17292) · [2604.16009](https://arxiv.org/abs/2604.16009) |
| **Anthropic Effective Harnesses** | Anthropic | 2025 | Engineering doctrine: progress files · session protocols · external memory | Prescriptive blog · NOT a benchmark · no scoring rubric | [anthropic.com](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| **LangSmith Eval** | LangChain | 2023+ | Trajectory · tool calls · LLM-judge · pairwise · online/offline | Tooling platform · no canonical scoring · vendor-coupled | [langchain.com](https://www.langchain.com/langsmith/evaluation) |
| **DeepEval** | Confident AI | 2024 | 50+ metrics: tool correctness · plan quality · goal accuracy · trace | Per-call metrics · no system-level workspace lens | [deepeval.com](https://deepeval.com/) |
| **Spider 2.0** | XLang / Stanford | 2024 ICLR | Enterprise text-to-SQL agentic · 632 tasks · multi-dialect | DB domain only | [2411.07763](https://arxiv.org/abs/2411.07763) |
| **MLPerf** | MLCommons | 2018+ | Throughput/latency raw + normalized · 3 divisions | ML hardware/runtime · not workspace · no agentic axes | [mlcommons.org](https://docs.mlcommons.org/inference/submission/) |

---

## Key papers 2023-2026 · pillar grounding

| Paper | arXiv | Year | Pillar(s) | Insight |
|---|---|---|---|---|
| **Single-Agent LLMs Outperform Multi-Agent** (Tran, Kiela Stanford) | [2604.02460](https://arxiv.org/abs/2604.02460) | 2026 | **5** | DPI: single-thread wins under fixed token budget unless context degraded |
| **MetaCogAgent** (Wang, Shu) | [2605.17292](https://arxiv.org/abs/2605.17292) | 2026 | **5, 9** | Prospective metacognition · MCU composite confidence · adaptive delegation · 82.4% acc · ECE 0.087 |
| **CLEAR Framework** | [2511.14136](https://arxiv.org/abs/2511.14136) | 2025 | **10, 12** | Cost-Latency-Efficacy-Assurance-Reliability · 50× cost variation · pass@k consistency 60→25% |
| **MAST** (Why Do Multi-Agent LLM Systems Fail?) | [2503.13657](https://arxiv.org/abs/2503.13657) | 2025 NeurIPS spotlight | **5, 6, 10, 11** | 14 failure modes · 41-86.7% MAS failure rate · spec failure 41.77% (top mode) |
| **Darwin Gödel Machine** (Sakana + Clune) | [2505.22954](https://arxiv.org/abs/2505.22954) | 2025 | **4** | Self-improving agents · SWE-bench 20→50% · evolutionary archive |
| **Reflexion** (Shinn et al.) | [2303.11366](https://arxiv.org/abs/2303.11366) | 2023 | **1, 4** | Verbal RL via episodic memory buffer · +22% AlfWorld |
| **Voyager** (Wang et al. · NVIDIA) | [2305.16291](https://arxiv.org/abs/2305.16291) | 2023 | **2, 4** | Skill library + auto-curriculum · lifelong learning |
| **EvoSkill** | [2603.02766](https://arxiv.org/abs/2603.02766) | 2026 | **2, 4** | Auto skill discovery from failure · Claude Code 60.6→67.9% |
| **SkillFlow** | [2604.17308](https://arxiv.org/abs/2604.17308) | 2026 | **2** | Lifelong skill discovery + evolution benchmark |
| **Anatomy of Agentic Memory** | [2602.19320](https://arxiv.org/abs/2602.19320) | 2026 | **1** | Taxonomy + empirical analysis of memory eval gaps |
| **Procedural Memory Retrieval Benchmark** | [2511.21730](https://arxiv.org/abs/2511.21730) | 2025 | **1** | Isolates procedural recall from execution |
| **AgentCompass** | [2509.14647](https://arxiv.org/abs/2509.14647) | 2025 | **6** | Production agentic workflow eval · hierarchical error taxonomy + dual memory |
| **AgentTrace** | [2602.10133](https://arxiv.org/abs/2602.10133) | 2026 | **6** | Structured logging: cognitive/operational/contextual surfaces · OTEL-native |
| **AgenTracer** | [2509.03312](https://arxiv.org/abs/2509.03312) | 2025 | **6, 10** | Attribution of failure in multi-agent traces |
| **RAS-Eval** | [2506.15253](https://arxiv.org/abs/2506.15253) | 2025 | **7** | 80 cases × 3802 attacks · 11 CWE categories · env-var secret handling |
| **Agent Security Bench (ASB)** | [2410.02644](https://arxiv.org/abs/2410.02644) | 2024 | **7** | 10 scenarios × 400 tools × 27 attack/defense × 7 metrics |
| **SEC-bench** | [2506.11791](https://arxiv.org/abs/2506.11791) | 2025 | **7** | Containerized security tasks |
| **AAGATE** | [2510.25863](https://arxiv.org/abs/2510.25863) | 2025 | **3, 11** | NIST AI RMF-aligned governance platform for agentic AI |
| **Active Context Compression** | [2601.07190](https://arxiv.org/abs/2601.07190) | 2026 | **1** | Autonomous memory management in LLM agents |
| **Agentic Harness Engineering** | [2604.25850](https://arxiv.org/abs/2604.25850) | 2026 | **4, 6** | Observability-driven automatic evolution of coding-agent harnesses |
| **Trainee-Bench / Agent's First Day** | [2601.08173](https://arxiv.org/abs/2601.08173) | 2026 | **8** | Context-aware scheduling · prudent info acquisition · continuous evolution |
| **Language Models (Mostly) Know What They Know** (Kadavath et al.) | [2207.05221](https://arxiv.org/abs/2207.05221) | 2022 | **9** | LLMs verbalize confidence but poorly calibrated · baseline for MetaCog |
| **Can LLMs Express Their Uncertainty?** (Xiong et al.) | [2306.13063](https://arxiv.org/abs/2306.13063) | 2023 | **9** | Empirical evaluation of confidence elicitation strategies |
| **On Calibration of Modern Neural Networks** (Guo et al.) | ICML 2017 | 2017 | **9** | Expected Calibration Error (ECE) metric definition |
| **MemGPT** | [2310.08560](https://arxiv.org/abs/2310.08560) | 2023 | **1** | Virtual context management |

---

## Standards & frameworks · governance and operations

| Framework | Org | Pillars | URL |
|-----------|-----|---------|-----|
| **NIST AI RMF 1.0** | NIST | **3, 11** | 4 functions: Govern · Map · Measure · Manage. Process framework, not pass/fail. | [nvlpubs.nist.gov](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf) |
| **OWASP LLM Top 10 (2025)** | OWASP | **7, 11** | LLM02 Sensitive Info · LLM06 Excessive Agency · LLM07 System Prompt Leakage · LLM10 Unbounded Consumption | [genai.owasp.org](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) |
| **CMMI Levels** | CMMI Institute | **all** | Maturity Level L1-L5 (staged) · cumulative capability · appraiser-driven | [cmmiinstitute.com](https://cmmiinstitute.com/learning/appraisals/levels) |
| **AWS Well-Architected** | AWS | **all** | 6 pillars · question-based · risk rating per question | [aws.amazon.com](https://aws.amazon.com/architecture/well-architected/) |
| **OpenTelemetry GenAI** | OTEL | **6** | Semantic conventions for AI agent observability traces | [opentelemetry.io](https://opentelemetry.io/blog/2025/ai-agent-observability/) |
| **CoALA framework** | Sumers et al. | **1, 9** | Cognitive Architectures for Language Agents · semantic/episodic/procedural taxonomy | [arXiv 2309.02427](https://arxiv.org/abs/2309.02427) |
| **Constitutional AI** | Anthropic | **3** | Explicit principles outperform implicit alignment | [arXiv 2212.08073](https://arxiv.org/abs/2212.08073) |
| **Google SRE Book** | Google | **6, 10** | Idempotency · retry budgets · circuit breakers · MTTD > MTBF | sre.google |

---

## Forward Deploy Engineering · what FDEs actually measure

Empirical signals from Palantir AI FDE docs · Anthropic deployment posts · MindStudio analyses:

| Signal | What it measures | Maps to pillar |
|--------|------------------|----------------|
| **Time-to-first-impact** | Days from embed to first KPI delta | **8** Portability |
| **Pilot-to-production conversion rate** | % of pilots reaching production | **8** Portability |
| **Customer-KPI delta** | Business metric movement | (downstream of all) |
| **Harness portability** | Can same harness redeploy in N days? | **8** Portability |
| **Workflow penetration** | % of customer workflows routing through agent | **8** Portability |
| **Trust regressions** | Rate of human escalations · overrides over time | **3, 6** Governance + Observability |
| **Compute cost per outcome** | $ per business event (not $ per token) | **12** Cost/Performance |

### FDE practice references

- [Palantir AI FDE docs](https://www.palantir.com/docs/foundry/ai-fde/overview)
- [MindStudio FDE analysis · Anthropic + OpenAI copying Palantir model](https://www.mindstudio.ai/blog/anthropic-openai-copying-palantir-forward-deployed-engineer-model)
- [Anthropic · Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Focused Labs · Agent Benchmark Scores Are Measuring the Harness, Not the Model (2026)](https://focused.io/lab/agent-benchmarks-measure-the-harness)
- [Awesome Harness Engineering list](https://github.com/ai-boost/awesome-harness-engineering)

---

## Gap analysis · what makes this benchmark unique

**No public benchmark covers all 12 pillars simultaneously.**

Closest in spirit:
- **AgentCompass** (production monitoring · hierarchical error taxonomy · dual memory) → lacks DPI · skill staleness · credentials axes
- **AgentBoard** (fine-grained sub-skill scoring) → lacks memory · governance · portability axes
- **CLEAR** (enterprise cost-controlled eval) → trajectory-based · no workspace structural axes
- **Anthropic "Effective Harnesses"** (engineering doctrine) → prescriptive, not measurable · no rubric

What this benchmark adds (12 pillars vs. landscape):

| Pillar | Closest existing measure | What we add |
|---|---|---|
| **1 · Memory** | CoALA · LoCoMo · Anatomy of Agentic Memory | Cross-tier *interaction* (demotion · promotion · staleness · conflict resolution) |
| **2 · Skills** | Voyager · EvoSkill · SkillFlow · Hermes catalog | Discoverability + staleness + dependency graph + REGISTRY governance |
| **3 · Governance** | MAST (post-hoc only) · NIST AI RMF (process only) | Prospective: rule cascade coherence · HARD RULES · PRE-OUTPUT compliance judge |
| **4 · Auto-improve** | DGM · Reflexion · EvoSkill | Cron-scheduled loops with quality gates · pattern-transfer REGISTRY |
| **5 · DPI** | Stanford 2604.02460 (theory only) | Operational DPI guard with 3-condition gate + spawn auditing |
| **6 · Observability** | OTEL GenAI · AgentTrace · AgentCompass | Workspace-level: query layer · session handoff · explicit state machine · MAST mapping |
| **7 · Credentials** | RAS-Eval · ASB · SEC-bench · OWASP LLM 2025 | Workspace property: zero plaintext · runtime resolution · vault topology |
| **8 · Portability** | (no public benchmark) ⭐ | **Unique** · FDE re-deployability · cross-engagement isolation |
| **9 · Metacognition** | MetaCogAgent (2605.17292) is the source · NO public benchmark measures it ⭐ | **Unique** · prospective metacognition · MCU · operationalizes DPI 3rd condition |
| **10 · Reliability** | CLEAR (cost-controlled trajectory) · MAST (failure taxonomy) | **Unique workspace lens** · pass@k consistency · idempotency · MAST coverage · replay harness |
| **11 · HITL** | NIST AI RMF (process) · AAGATE | **Unique measurable** · approval gates · escalation criteria · friction measured |
| **12 · Cost/Performance** | CLEAR (enterprise focus) · Anthropic prompt cache docs | **Unique workspace lens** · cost-per-outcome · cache hit rate · model routing · harness economics |

---

## Risks · honest disclosure

1. **Stanford 2604.02460 cited cautiously.** Empirical scope is 3 model families on multi-hop reasoning only · do not overclaim generality.
2. **Pattern naming provenance.** Some pattern names referenced (e.g., Crafft, Dreams, ECHO) may be informal or research-internal labels. Where canonical published equivalents exist (e.g., Reflexion = arXiv 2303.11366, Voyager = arXiv 2305.16291), we cite them directly. Future revisions will track explicit provenance.
3. **Goodhart's law risk.** Once published, people optimize for the score. Pre-register multiple rubric variants and rotate. Prefer outcome measurement (MTTD · time-to-first-impact · pass@k) over checkbox presence.
4. **Model-agnostic scoring.** Audit should not assume Claude-specific behaviors · validate on at least 2 model families before publishing official scores.
5. **OpenTelemetry adoption preferred.** Don't reinvent observability conventions · adopt OTEL GenAI semantic conventions for pillar 6.
6. **Single-reference example bias.** v0.3 has one reference workspace · v0.4 target: 3+ external workspace audits to validate criteria not biased to one stack.
7. **Equal-weight default is provisional.** v0.3 uses 1/12 per pillar. v0.4 will derive empirical weights from correlation analysis once 10+ external audits exist. Domain-specific overrides via `eval/weights.json`.

---

_SOURCES.md · v0.3 · 2026-05-19 · 40+ canonical references · enriched with CLEAR · MAST · NIST AI RMF · OWASP LLM Top 10 2025 · AAGATE · OpenTelemetry GenAI conventions_
