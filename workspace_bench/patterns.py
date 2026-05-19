"""
Pattern adapter registry · 50+ external research patterns mapped to pillars.

Each pattern is a piece of published research or production case study that
informs one or more pillars. The catalog is what turns the benchmark from
"opinion" into "literature-grounded" — every L3+ score should trace back to
at least one adapted pattern here.
"""

from __future__ import annotations
from typing import NamedTuple


class Pattern(NamedTuple):
    """One external pattern adapted into the benchmark."""
    name: str               # canonical name
    source: str             # paper/repo/blog URL or arXiv id
    year: int
    category: str           # foundational · production · governance · doctrine · industry
    pillars: list[int]      # pillar numbers this pattern informs
    abstract: str           # one-sentence summary
    contribution: str       # what this pattern contributes uniquely


# ─── 50+ patterns catalogued ──────────────────────────────────────────────
# Organized by category. Each contributes to one or more of the 12 pillars.

PATTERNS: list[Pattern] = [
    # ─── FOUNDATIONAL · agentic architecture (15) ─────────────────────────
    Pattern(
        "Reflexion (Shinn et al.)", "arXiv:2303.11366", 2023, "foundational",
        [1, 4],
        "Language agents with verbal reinforcement learning · episodic memory buffer.",
        "Self-reflection as a non-gradient learning loop · grounds episodic memory tier.",
    ),
    Pattern(
        "Voyager (Wang et al. · NVIDIA)", "arXiv:2305.16291", 2023, "foundational",
        [2, 4],
        "Open-ended embodied agent with skill library + auto-curriculum.",
        "Skill library that grows from experience · grounds skill staleness + auto-improvement.",
    ),
    Pattern(
        "MetaCogAgent (Wang, Shu)", "arXiv:2605.17292", 2026, "foundational",
        [5, 9],
        "Metacognitive multi-agent LLM framework with MCU · 82.4% acc · ECE 0.087.",
        "Prospective metacognition · composite confidence · operationalizes DPI 3rd condition.",
    ),
    Pattern(
        "Stanford DPI (Tran, Kiela)", "arXiv:2604.02460", 2026, "foundational",
        [5],
        "Single-agent LLMs outperform multi-agent under fixed token budgets.",
        "Data Processing Inequality theorem · grounds single-thread default policy.",
    ),
    Pattern(
        "Darwin Gödel Machine (Sakana + Clune)", "arXiv:2505.22954", 2025, "foundational",
        [4],
        "Self-improving agents · SWE-bench 20→50% via evolutionary archive.",
        "Evolutionary self-modification · grounds Dreams pipeline propose-review-apply.",
    ),
    Pattern(
        "CoALA (Sumers et al.)", "arXiv:2309.02427", 2024, "foundational",
        [1],
        "Cognitive Architectures for Language Agents · semantic/episodic/procedural taxonomy.",
        "Memory tier taxonomy foundation · grounds 5-tier memory architecture.",
    ),
    Pattern(
        "MemGPT (Packer et al.)", "arXiv:2310.08560", 2023, "foundational",
        [1],
        "Virtual context management for LLMs · OS-style page-swap memory.",
        "Hierarchical memory management · informs context budget allocation.",
    ),
    Pattern(
        "Tree of Thoughts (Yao et al.)", "arXiv:2305.10601", 2023, "foundational",
        [9],
        "Deliberate problem-solving through tree-structured exploration.",
        "Explicit reasoning paths · informs metacognitive deliberation patterns.",
    ),
    Pattern(
        "ECHO (Shrivastava, Papailiopoulos)", "research:2026", 2026, "foundational",
        [1, 4],
        "Environment dynamics as auxiliary supervision signal in agent RL.",
        "Environment-dynamics tier as distinct memory layer · failed trajectories as data.",
    ),
    Pattern(
        "EvoSkill", "arXiv:2603.02766", 2026, "foundational",
        [2, 4],
        "Auto skill discovery via failure analysis · Claude Code 60.6 → 67.9%.",
        "Skills emerge from failure patterns · grounds Pillar 2 staleness detection.",
    ),
    Pattern(
        "SkillFlow", "arXiv:2604.17308", 2026, "foundational",
        [2],
        "Lifelong skill discovery and evolution benchmark.",
        "Skill lifecycle measurement · grounds skill changelog + versioning.",
    ),
    Pattern(
        "Anatomy of Agentic Memory", "arXiv:2602.19320", 2026, "foundational",
        [1],
        "Taxonomy and empirical analysis of memory eval gaps.",
        "Cross-tier interaction measurement · grounds memory query layer.",
    ),
    Pattern(
        "Procedural Memory Retrieval Benchmark", "arXiv:2511.21730", 2025, "foundational",
        [1, 2],
        "Isolates procedural recall from execution capability.",
        "Procedural memory as distinct measurable tier.",
    ),
    Pattern(
        "Active Context Compression", "arXiv:2601.07190", 2026, "foundational",
        [1, 12],
        "Autonomous memory management in LLM agents.",
        "Context compression as cost optimization · cache prefix stability.",
    ),
    Pattern(
        "Constitutional AI (Anthropic)", "arXiv:2212.08073", 2022, "foundational",
        [3],
        "Explicit principles outperform implicit alignment.",
        "Constitution document pattern · grounds HARD RULES enumeration.",
    ),

    # ─── PRODUCTION · failure analysis · operations (12) ──────────────────
    Pattern(
        "MAST (UC Berkeley Sky Lab)", "arXiv:2503.13657", 2025, "production",
        [5, 6, 10, 11],
        "Why Do Multi-Agent LLM Systems Fail? · 14 failure modes · NeurIPS 2025 spotlight.",
        "41.77% spec failure top mode · 41-86.7% MAS failure rate empirical.",
    ),
    Pattern(
        "CLEAR Framework", "arXiv:2511.14136", 2025, "production",
        [10, 12],
        "Cost-controlled enterprise agent evaluation · CNA + pass@k.",
        "50× cost variation enterprise tasks · 60→25% pass@k drop over 8 runs.",
    ),
    Pattern(
        "AgentCompass", "arXiv:2509.14647", 2025, "production",
        [6],
        "Production agentic workflow eval · hierarchical error taxonomy + dual memory.",
        "Production monitoring patterns · grounds aggregate health report.",
    ),
    Pattern(
        "AgentTrace", "arXiv:2602.10133", 2026, "production",
        [6],
        "Structured logging: cognitive/operational/contextual surfaces · OTEL-native.",
        "Three-surface trace taxonomy · grounds OTEL GenAI adoption.",
    ),
    Pattern(
        "AgenTracer", "arXiv:2509.03312", 2025, "production",
        [6, 10],
        "Attribution of failure in multi-agent traces.",
        "Causal failure attribution · grounds replay harness + MAST coverage.",
    ),
    Pattern(
        "Agentic Harness Engineering", "arXiv:2604.25850", 2026, "production",
        [4, 6],
        "Observability-driven automatic evolution of coding-agent harnesses.",
        "Auto-improvement loop driven by observability · grounds Dreams pipeline.",
    ),
    Pattern(
        "Trainee-Bench (Agent's First Day)", "arXiv:2601.08173", 2026, "production",
        [8],
        "Context-aware scheduling · prudent info acquisition · continuous evolution.",
        "Onboarding benchmark for agentic workspaces · grounds time-to-bootstrap metric.",
    ),
    Pattern(
        "PaperClip / Sentra Company Brain", "research:2026", 2026, "production",
        [1, 4],
        "Memoria persistente come architettura, non add-on · $5M seed.",
        "Memory-as-architecture · 4-tier formalization · grounds memory engine.",
    ),
    Pattern(
        "Manus Context Engineering", "blog:2025", 2025, "production",
        [1, 12],
        "KV-cache hit rate is the single most important production metric.",
        "10× cost reduction via cache · cached $0.30/MTok vs uncached $3/MTok.",
    ),
    Pattern(
        "Hermes-agent (NousResearch)", "github:NousResearch/hermes-agent", 2024, "production",
        [1, 2],
        "Agent-curated memory · autonomous skill creation · FTS5 search.",
        "Skill staleness curator pattern · grounds Hermes auto-stale cron.",
    ),
    Pattern(
        "OpenCode (anomalyco)", "github:anomalyco/opencode", 2024, "production",
        [2, 3],
        "build/plan/research mode toggle · provider-agnostic · client/server.",
        ".opencode/ folder convention · informs .claude/ structure.",
    ),
    Pattern(
        "WalkingLabs Harness Engineering", "blog:2026", 2026, "production",
        [4, 6],
        "Observability-driven harness evolution patterns.",
        "Production harness improvement loop · grounds A-MAC scoring.",
    ),

    # ─── GOVERNANCE · safety · security (10) ──────────────────────────────
    Pattern(
        "OWASP LLM Top 10 (2025)", "owasp:llm-top-10-2025", 2025, "governance",
        [7, 11],
        "LLM02 Sensitive Info · LLM06 Excessive Agency · LLM07 System Prompt Leakage.",
        "Industry security standard · grounds Pillar 7 anti-pattern catalog.",
    ),
    Pattern(
        "NIST AI RMF 1.0", "nist:ai-100-1", 2023, "governance",
        [3, 11],
        "4 functions: Govern · Map · Measure · Manage. Process framework.",
        "Federal-grade governance framework · grounds Pillar 3 + 11.",
    ),
    Pattern(
        "AAGATE", "arXiv:2510.25863", 2025, "governance",
        [3, 11],
        "NIST AI RMF-aligned governance platform for agentic AI.",
        "Operational NIST AI RMF · grounds compliance judge + escalation criteria.",
    ),
    Pattern(
        "Agent Security Bench (ASB)", "arXiv:2410.02644", 2024, "governance",
        [7],
        "10 scenarios × 400 tools × 27 attack/defense × 7 metrics.",
        "Agent-specific security benchmark · grounds OWASP LLM mapping.",
    ),
    Pattern(
        "RAS-Eval", "arXiv:2506.15253", 2025, "governance",
        [7],
        "80 cases × 3802 attacks · 11 CWE categories · env-var secret handling.",
        "Agent security with focus on secrets · grounds vault integration.",
    ),
    Pattern(
        "SEC-bench", "arXiv:2506.11791", 2025, "governance",
        [7],
        "Containerized security tasks for agents.",
        "Container-grade security audit · grounds runtime isolation patterns.",
    ),
    Pattern(
        "Cognition · Don't Build Multi-Agents", "blog:cognition.ai/2024", 2024, "governance",
        [5],
        "Context sharing between agents is the bottleneck · steel-man.",
        "Anti-multi-agent steel-man · grounds Pillar 5 anti-pattern catalog.",
    ),
    Pattern(
        "Cynefin Framework (Snowden)", "research:1999", 1999, "governance",
        [3, 11],
        "Sense-making framework: Clear · Complicated · Complex · Chaotic.",
        "Domain-context decision routing · grounds escalation criteria.",
    ),
    Pattern(
        "MITRE ATLAS", "mitre:atlas", 2024, "governance",
        [7],
        "Adversarial threat landscape for AI systems · tactics + techniques.",
        "Adversary modeling for agentic systems · informs governance threat model.",
    ),
    Pattern(
        "ISO/IEC 42001 AI Management System", "iso:42001", 2024, "governance",
        [3],
        "Management system standard for AI · audit-able governance.",
        "ISO-grade AI governance · grounds versioned constitution.",
    ),

    # ─── DOCTRINE · forward deploy · practitioner (10) ────────────────────
    Pattern(
        "Anthropic Effective Harnesses", "anthropic:effective-harnesses", 2025, "doctrine",
        [4, 6, 8],
        "Engineering doctrine · progress files · session protocols · external memory.",
        "Long-running agent doctrine · grounds session capture + Reflexion.",
    ),
    Pattern(
        "Anthropic Demystifying Evals", "anthropic:demystifying-evals", 2025, "doctrine",
        [10],
        "pass@k as core metric · operational eval practice.",
        "Pass@k empirical importance · grounds Pillar 10 measurement.",
    ),
    Pattern(
        "Anthropic Cache Diagnostics", "anthropic:cache-diagnostics-2026", 2026, "doctrine",
        [1, 12],
        "Diagnose cache miss via API · 4 cache_miss_reason types · beta.",
        "KV-cache observability · grounds Pillar 12 cache hit measurement.",
    ),
    Pattern(
        "Focused Labs · Harness Not Model", "focused:harness-not-model", 2026, "doctrine",
        [12],
        "Agent benchmark scores measure the harness, not the model.",
        "Empirical 87.2→91.1% from harness swap · grounds Pillar 12.",
    ),
    Pattern(
        "Palantir FDE Model", "palantir:ai-fde", 2024, "doctrine",
        [8],
        "Forward Deployed Engineer · embedded · customer-KPI-driven.",
        "FDE practice canonical · grounds Pillar 8 portability metric.",
    ),
    Pattern(
        "MindStudio FDE Analysis", "mindstudio:fde", 2026, "doctrine",
        [8],
        "Anthropic + OpenAI copying Palantir FDE model · industry trend.",
        "FDE economic viability empirical · grounds Pillar 8 ROI.",
    ),
    Pattern(
        "OpenTelemetry GenAI Conventions", "otel:genai-2025", 2025, "doctrine",
        [6],
        "Semantic conventions for AI agent observability traces.",
        "Standard observability vocabulary · grounds Pillar 6 OTEL adoption.",
    ),
    Pattern(
        "Anthropic Skills Documentation", "anthropic:skills-docs", 2025, "doctrine",
        [2],
        "Auto-trigger via description matching · skill folder convention.",
        "Skill structure standard · grounds Pillar 2 frontmatter requirements.",
    ),
    Pattern(
        "Google SRE Book", "google:sre-book", 2016, "doctrine",
        [6, 10],
        "Idempotency · retry budgets · circuit breakers · MTTD > MTBF.",
        "Production reliability doctrine · grounds Pillar 10 retry policy.",
    ),
    Pattern(
        "MLPerf Submission Rules", "mlcommons:submission", 2018, "doctrine",
        [8],
        "Formal submission process · compliance tests · review committee.",
        "Benchmark governance standard · grounds submissions/ PR process.",
    ),

    # ─── INDUSTRY · benchmarks · tooling (10) ─────────────────────────────
    Pattern(
        "SWE-bench / Verified / Pro", "arXiv:2310.06770", 2023, "industry",
        [10],
        "Resolve real GitHub issues · patch generation · pass/fail per issue.",
        "Code-task benchmark canonical · informs reliability measurement.",
    ),
    Pattern(
        "TAU-bench (Sierra)", "arXiv:2406.12045", 2024, "industry",
        [10],
        "Tool-Agent-User multi-turn · pass^k reliability · policy adherence.",
        "Multi-turn agent benchmark · informs reliability measurement.",
    ),
    Pattern(
        "AgentBench (Tsinghua)", "arXiv:2308.03688", 2023, "industry",
        [2],
        "8 environments multi-task evaluation.",
        "Environment-coverage breadth · informs Pillar 2 tool diversity.",
    ),
    Pattern(
        "GAIA (Meta + HF)", "arXiv:2311.12983", 2023, "industry",
        [9],
        "General assistant · reasoning + multimodal + tool use · 466 Qs.",
        "Cross-domain assistant benchmark · informs metacognition routing.",
    ),
    Pattern(
        "OSWorld (XLang)", "arXiv:2404.07972", 2024, "industry",
        [2],
        "369 real computer tasks · GUI+keyboard+mouse · NeurIPS 2024.",
        "OS-level agent capability · informs deterministic tooling.",
    ),
    Pattern(
        "HELM (Stanford CRFM)", "arXiv:2211.09110", 2022, "industry",
        [10, 12],
        "7 metrics × 16 scenarios · holistic LLM eval.",
        "Multi-metric holistic eval pattern · grounds composite scoring.",
    ),
    Pattern(
        "Chatbot Arena (LMSYS)", "lmsys:arena", 2023, "industry",
        [10],
        "Bradley-Terry MLE → Elo presentation · 1M+ human votes.",
        "Human-in-the-loop pairwise eval · informs Pillar 11 feedback structure.",
    ),
    Pattern(
        "AWS Well-Architected", "aws:well-architected", 2015, "industry",
        [3, 8],
        "6 pillars · question-based · risk rating per question.",
        "Cluster-pillar structure precedent · grounds 4-cluster organization.",
    ),
    Pattern(
        "CMMI Maturity Levels", "cmmi:levels", 2002, "industry",
        [4, 8],
        "Maturity Level L1-L5 (staged) · ISO 15504 adjacent.",
        "L0-L4 maturity model precedent · grounds scoring system.",
    ),
    Pattern(
        "LangSmith Eval (LangChain)", "langchain:smith", 2023, "industry",
        [6, 10],
        "Trajectory · tool calls · LLM-judge · pairwise · online/offline.",
        "Production agent observability platform · informs Pillar 6.",
    ),
]


def patterns_by_category(category: str) -> list[Pattern]:
    return [p for p in PATTERNS if p.category == category]


def patterns_by_pillar(pillar_n: int) -> list[Pattern]:
    return [p for p in PATTERNS if pillar_n in p.pillars]


def pattern_coverage_per_pillar() -> dict[int, int]:
    """How many patterns inform each pillar."""
    counts: dict[int, int] = {i: 0 for i in range(1, 13)}
    for p in PATTERNS:
        for pn in p.pillars:
            counts[pn] += 1
    return counts


CATEGORIES = [
    ("foundational", "Foundational · agentic architecture"),
    ("production", "Production · failure analysis · operations"),
    ("governance", "Governance · safety · security"),
    ("doctrine", "Doctrine · forward deploy · practitioner"),
    ("industry", "Industry · benchmarks · tooling"),
]


def total_patterns() -> int:
    return len(PATTERNS)
