# Research Sources

> Evidence base for the 8 pillars · 30+ papers and frameworks 2022-2026.

---

## Existing benchmarks · what each measures and where it falls short

| Name | Org | Year | Focus | Gap (why we need pillar X) | URL |
|---|---|---|---|---|---|
| **SWE-bench / Verified / Pro** | Princeton + OpenAI | 2023-25 | Resolve real GitHub issues; patch generation | Single-shot task · no memory/state across runs · measures model+harness conflated | [2310.06770](https://arxiv.org/abs/2310.06770) · [Pro 2509.16941](https://arxiv.org/abs/2509.16941) |
| **TAU-bench (τ-bench)** | Sierra (Anthropic-adjacent) | 2024 | Tool-Agent-User multi-turn · policy adherence · pass^k reliability | Domain-specific (retail/airline) · no workspace/memory tier · ignores skill discovery | [2406.12045](https://arxiv.org/abs/2406.12045) |
| **AgentBench** | Tsinghua | 2023 | 8 environments (OS, DB, web, KG, card, household, mind2web, alfworld) | Stateless episodes · no auto-improvement · no observability axis | [2308.03688](https://arxiv.org/abs/2308.03688) |
| **GAIA** | Meta + HuggingFace + AutoGPT | 2023 | General assistant: reasoning + multimodal + tool use; 466 Qs | Single-question framing · no long-running state · human 92% vs GPT-4 15% | [2311.12983](https://arxiv.org/abs/2311.12983) |
| **OSWorld** | XLang (HKU/Tianjin) | 2024 | 369 real computer tasks; GUI+keyboard+mouse · NeurIPS 2024 | OS-bound · ignores credentials policy · memory architecture | [2404.07972](https://arxiv.org/abs/2404.07972) |
| **MLE-bench** | OpenAI | 2024 | 75 Kaggle ML eng. competitions · medal-rate scoring | ML-engineering only · no governance/memory/multi-agent assessment | [2410.07095](https://arxiv.org/abs/2410.07095) |
| **WebArena** | CMU | 2023 | 812 tasks across 4 self-hosted web apps | Browser-only · no skill library · no auto-improvement loop | [2307.13854](https://arxiv.org/abs/2307.13854) |
| **AgentBoard** | HKUST | 2024 NeurIPS | Fine-grained progress rate · 9 tasks · 1013 envs · sub-skill breakdown | No memory-tier evaluation · no credentials/security axis | [2401.13178](https://arxiv.org/abs/2401.13178) |
| **Anthropic "Effective Harnesses"** | Anthropic | 2025 | Engineering doctrine: progress files · session protocols · external memory · incremental commits | Prescriptive blog post, NOT a benchmark · no scoring rubric | [anthropic.com](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| **LangSmith eval** | LangChain | 2023+ | Trajectory · tool calls · LLM-judge · pairwise · online/offline | Tooling platform · no canonical scoring · vendor-coupled | [langchain.com](https://www.langchain.com/langsmith/evaluation) |
| **DeepEval** | Confident AI | 2024 | 50+ metrics: tool correctness · plan quality · goal accuracy · trace | Per-call metrics · no system-level workspace lens | [deepeval.com](https://deepeval.com/) |
| **Spider 2.0** | XLang / Stanford | 2024 ICLR | Enterprise text-to-SQL agentic · 632 tasks · multi-dialect | DB domain only | [2411.07763](https://arxiv.org/abs/2411.07763) |
| **HELM** | Stanford CRFM | 2022+ | 7 metrics × 16 scenarios: accuracy · calibration · robustness · fairness · bias · toxicity · efficiency | Model-centric, not agentic-workspace centric | [2211.09110](https://arxiv.org/abs/2211.09110) |

---

## Key papers 2023-2026 · pillar grounding

| Paper | arXiv | Year | Pillar(s) | Insight |
|---|---|---|---|---|
| **Single-Agent LLMs Outperform Multi-Agent** (Tran, Kiela Stanford) | [2604.02460](https://arxiv.org/abs/2604.02460) | 2026 | **5** | DPI: single-thread wins under fixed token budget unless context degraded |
| **MetaCogAgent · Metacognitive Multi-Agent LLM Framework** (Wang, Shu) | [2605.17292](https://arxiv.org/abs/2605.17292) | 2026 | **5, 9** | Prospective metacognition · MCU (verbalized + profile composite confidence) · adaptive delegation · cybernetic feedback. 82.4% acc · -34% API calls · ECE 0.087 |
| **Language Models (Mostly) Know What They Know** (Kadavath et al.) | [2207.05221](https://arxiv.org/abs/2207.05221) | 2022 | **9** | LLMs exhibit some ability to verbalize confidence but are poorly calibrated · baseline for MetaCog |
| **Can LLMs Express Their Uncertainty?** (Xiong et al.) | [2306.13063](https://arxiv.org/abs/2306.13063) | 2023 | **9** | Empirical evaluation of confidence elicitation strategies in LLMs |
| **On Calibration of Modern Neural Networks** (Guo et al.) | ICML 2017 | 2017 | **9** | Expected Calibration Error (ECE) metric definition |
| **Why Do Multi-Agent LLM Systems Fail? (MAST)** | [2503.13657](https://arxiv.org/abs/2503.13657) | 2025 NeurIPS spotlight | **5, 6** | 14 failure modes in 3 categories · 41-86% MAS failure rate |
| **Darwin Gödel Machine** (Sakana + Clune) | [2505.22954](https://arxiv.org/abs/2505.22954) | 2025 | **4** | Self-improving agents · SWE-bench 20→50% · evolutionary archive |
| **Reflexion** (Shinn et al.) | [2303.11366](https://arxiv.org/abs/2303.11366) | 2023 | **1, 4** | Verbal RL via episodic memory buffer · +22% AlfWorld |
| **Voyager** (Wang et al. · NVIDIA) | [2305.16291](https://arxiv.org/abs/2305.16291) | 2023 | **2, 4** | Skill library + auto-curriculum · lifelong learning |
| **EvoSkill** | [2603.02766](https://arxiv.org/abs/2603.02766) | 2026 | **2, 4** | Auto skill discovery via failure analysis · Claude Code 60.6→67.9% |
| **SkillFlow** | [2604.17308](https://arxiv.org/abs/2604.17308) | 2026 | **2** | Lifelong skill discovery + evolution benchmark |
| **Anatomy of Agentic Memory** | [2602.19320](https://arxiv.org/abs/2602.19320) | 2026 | **1** | Taxonomy + empirical analysis of memory eval gaps |
| **Procedural Memory Retrieval Benchmark** | [2511.21730](https://arxiv.org/abs/2511.21730) | 2025 | **1** | Isolates procedural recall from execution |
| **AgentCompass** | [2509.14647](https://arxiv.org/abs/2509.14647) | 2025 | **6** | Production agentic workflow eval · hierarchical error taxonomy + dual memory |
| **AgentTrace** | [2602.10133](https://arxiv.org/abs/2602.10133) | 2026 | **6** | Structured logging: cognitive/operational/contextual surfaces · OTEL-native |
| **RAS-Eval** | [2506.15253](https://arxiv.org/abs/2506.15253) | 2025 | **7** | 80 cases × 3802 attacks · 11 CWE categories · env-var secret handling |
| **Agent Security Bench (ASB)** | [2410.02644](https://arxiv.org/abs/2410.02644) | 2024 | **7** | 10 scenarios × 400 tools × 27 attack/defense × 7 metrics |
| **SEC-bench** | [2506.11791](https://arxiv.org/abs/2506.11791) | 2025 | **7** | Containerized security tasks |
| **Active Context Compression** | [2601.07190](https://arxiv.org/abs/2601.07190) | 2026 | **1** | Autonomous memory mgmt in LLM agents |
| **Agentic Harness Engineering** | [2604.25850](https://arxiv.org/abs/2604.25850) | 2026 | **4, 6** | Observability-driven automatic evolution of coding-agent harnesses |
| **Agent's First Day (Trainee-Bench)** | [2601.08173](https://arxiv.org/abs/2601.08173) | 2026 | **8** | Context-aware scheduling · prudent info acquisition · continuous evolution |
| **AgenTracer** | [2509.03312](https://arxiv.org/abs/2509.03312) | 2025 | **6** | Attribution of failure in multi-agent traces |

---

## Forward Deploy Engineering · what FDEs actually measure

Empirical signals from Palantir AI FDE docs · Anthropic deployment posts · MindStudio analyses:

| Signal | What it measures | Why it matters | Maps to pillar |
|--------|------------------|-----------------|----------------|
| **Time-to-first-impact** | Days from embed to first KPI delta | Pilot-to-prod conversion · MIT 95% failure baseline | **8** |
| **Pilot-to-production conversion rate** | % of pilots reaching production | Differentiates demo from product | **8** |
| **Customer-KPI delta** | Business metric movement (revenue · cycle time · error rate) | Not model accuracy · actual outcome | (downstream of all) |
| **Harness portability** | Can same harness redeploy on next client in N days? | FDE economic viability | **8** |
| **Workflow penetration** | % of customer workflows routing through agent | Adoption vs. parallel-to-existing | **8** |
| **Trust regressions** | Rate of human escalations · overrides over time | Should decay · signals reliability | **3, 6** |
| **Compute cost per outcome** | $ per business event (not $ per token) | True economics | **4** |

### Common FDE pain points

- **Credentials sprawl across clients** (each engagement = new vault) → **Pillar 7 + 8**
- **Skills written for client A don't generalize to client B** (no abstraction layer) → **Pillar 2 + 8**
- **Multi-agent demos that don't survive contact with production data volume** → **Pillar 5**
- **Memory leaks across customer accounts** (semantic memory cross-contamination · P0 compliance risk) → **Pillar 1 + 8**
- **No standard handoff artifact when FDE rotates off engagement** → **Pillar 8**

---

## Gap analysis · what makes this benchmark unique

**No public benchmark covers all 8 pillars simultaneously.**

Closest in spirit:
- **AgentCompass** (production monitoring · hierarchical error taxonomy · dual memory) → lacks DPI · skill staleness · credentials axes.
- **AgentBoard** (fine-grained sub-skill scoring) → lacks memory · governance · portability axes.
- **Anthropic "Effective Harnesses"** (engineering doctrine) → prescriptive, not measurable · no rubric.

What this benchmark adds (8 pillars vs. landscape):

| Pillar | Closest existing measure | What we add |
|---|---|---|
| **1 · Memory** | LoCoMo · Anatomy of Agentic Memory · MemMachine | Cross-tier *interaction* (demotion · promotion · staleness · conflict resolution) |
| **2 · Skills** | Voyager · EvoSkill · SkillFlow · Hermes catalog | Discoverability + staleness + dependency graph + REGISTRY governance |
| **3 · Governance** | MAST (post-hoc only) | Prospective: rule cascade coherence · HARD RULES · PRE-OUTPUT compliance judge |
| **4 · Auto-improve** | DGM · Reflexion · EvoSkill | Cron-scheduled loops with quality gates · pattern-transfer REGISTRY |
| **5 · DPI** | Stanford 2604.02460 (theory only) | Operational DPI guard with 3-condition gate + spawn auditing |
| **6 · Observability** | OTEL GenAI · AgentTrace | Workspace-level: query layer (MCP-based) · session handoff format · centralized session history |
| **7 · Credentials** | RAS-Eval · ASB · SEC-bench | Workspace property: zero plaintext · op:// resolution · vault topology |
| **8 · Portability** | (no public benchmark) ⭐ | **Unique** · FDE re-deployability · cross-engagement isolation |
| **9 · Metacognition** | MetaCogAgent (2605.17292) is the source · NO public benchmark measures it ⭐ | **Unique** · prospective metacognition · MCU runner · capability profile · EMA cybernetic loop · operationalizes DPI 3rd condition |

---

## Standards & adjacent work

- **OpenTelemetry GenAI semantic conventions** · [opentelemetry.io](https://opentelemetry.io/blog/2025/ai-agent-observability/) · adopt for observability traces.
- **OWASP LLM Top 10** · LLM06 (Insecure Output Handling) · LLM07 (Insecure Plugin Design) · used for governance + credentials anti-patterns.
- **CoALA framework** (Cognitive Architectures for Language Agents) · semantic / episodic / procedural taxonomy foundation.
- **Harness Engineering awesome list** · [github.com/ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering)

### FDE practice references

- [Palantir AI FDE docs](https://www.palantir.com/docs/foundry/ai-fde/overview)
- [MindStudio FDE analysis · Anthropic + OpenAI copying Palantir model](https://www.mindstudio.ai/blog/anthropic-openai-copying-palantir-forward-deployed-engineer-model)

---

## Risks · honest disclosure

1. **Stanford 2604.02460 cited cautiously.** Empirical scope is 3 model families on multi-hop reasoning only · do not overclaim generality.
2. **Pattern naming provenance.** Some pattern names referenced in this benchmark (e.g., Crafft, Dreams, ECHO) may be informal or research-internal labels. Where canonical published equivalents exist (e.g., Reflexion = arXiv 2303.11366, Voyager = arXiv 2305.16291), we cite them directly. Future revisions will track explicit provenance and remove informal labels where ambiguous.
3. **Goodhart's law risk.** Once published, people will optimize for the score. Pre-register multiple rubric variants and rotate. Prefer measurement of *outcomes* (MTTD, time-to-first-impact) over *checkbox presence*.
4. **Model-agnostic scoring.** Audit should not assume Claude-specific behaviors · validate on at least 2 model families before publishing official scores.
5. **OpenTelemetry adoption preferred.** Don't reinvent observability conventions · adopt OTEL GenAI semantic conventions for pillar 6.

---

_SOURCES.md · v0.1 · 2026-05-19 · enriched from autoresearch run · 30+ canonical references_
