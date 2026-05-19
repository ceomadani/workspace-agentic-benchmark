# Changelog

All notable changes to the Workspace Agentic Benchmark are documented here.

Format inspired by [Keep a Changelog](https://keepachangelog.com/). Versioning follows [SemVer](https://semver.org/) with `MAJOR.MINOR.PATCH`.

---

## [0.3.2] · 2026-05-20

### Added · onboarding · i18n · information theory · 50+ patterns · tree-heavy HTML

- **`workspace-bench init`** · interactive onboarding wizard
  - Rich-prompts UI · single-folder or multi-folder workspace
  - Auto-detect language from workspace files (en/it/fr/es/de/pt)
  - Auto-detect stack (Python · Node.js · Next.js · TypeScript · Rust · Go · Ruby · PHP · Java · Docker · Terraform · GitHub Actions · Claude Code · Cursor · n8n · Supabase · Vercel · ...)
  - Save `.workspace-bench.yaml` config that `workspace-bench run` auto-loads
- **`workspace_bench/i18n.py`** · multi-language support
  - 6 languages: en · it · fr · es · de · pt
  - Function-word marker detection from sampled markdown
  - Translation tables · falls back to English for missing keys
- **`workspace_bench/info_theory.py`** · information theory layer
  - α = √(quantity × quality) · geometric-mean composite
  - Signal-to-noise ratio (linear + dB)
  - Shannon entropy of file-type distribution
  - Information density (avg structured content per file)
  - Stale-rate · empty-rate · citation density · structure ratio
  - Interpretive labels (high/healthy/marginal/poor · balanced/quantity-heavy/quality-heavy)
- **`workspace_bench/patterns.py`** · 50+ pattern adapter catalog
  - 5 categories: foundational · production · governance · doctrine · industry
  - Each pattern mapped to pillars it informs (1-12)
  - Coverage matrix · how many patterns inform each pillar
  - Sources include Reflexion · Voyager · MetaCogAgent · MAST · CLEAR · DGM · MemGPT · CoALA · NIST AI RMF · AAGATE · OWASP · CMMI · Anthropic Effective Harnesses · Manus · PaperClip · Hermes-agent · OpenCode · etc.
- **HTML report v3 · tree-heavy · Madani branded · localized**
  - Inline SVG Madani Lab logo header
  - Multi-language full content (executive summary · cluster averages · pillar table · trees · improvement priorities · pattern catalog · info-theory · legend)
  - 5+ tree visualizations: pillar trees per cluster · pattern catalog trees per category · pattern coverage tree · info-theory components tree
  - Information theory section with α · SNR · entropy · density · quality vs quantity cards
  - 108KB self-contained (up from 30KB in v0.3.1) · same print-friendly + responsive

### Changed

- `cli.py` · new `init` subcommand · `run` auto-loads `.workspace-bench.yaml` · `report` accepts `--language` and auto-detects
- `run` pipeline now computes information theory metrics during audit
- HTML report renders in detected language by default

### Files

- `workspace_bench/onboarding.py` (NEW · 240 lines)
- `workspace_bench/i18n.py` (NEW · 280 lines)
- `workspace_bench/info_theory.py` (NEW · 220 lines)
- `workspace_bench/patterns.py` (NEW · 360 lines · 50+ patterns)
- `workspace_bench/html_report.py` (REWRITE · 470 lines · trees · branded · localized)
- `workspace_bench/cli.py` (UPDATE · 240 lines · init + i18n + info-theory integration)

---

## [0.3.1] · 2026-05-20

### Added · sophisticated CLI experience

- **`workspace_bench/` Python package** · proper distribution structure
- **`pyproject.toml`** · `pip install` ready · console_scripts entry point (`workspace-bench` command)
- **Rich-powered terminal UI** · `slash context`-style ultra-detailed visualization
  - Composite hero card with 12-block pillar visualization (one block per pillar · colored by maturity)
  - Tree-indented per-cluster breakdown (`▸ Cluster X` · `├─ P0N`)
  - Per-pillar maturity dots (⬤⬤⬤○ = L3 · ⬤⬤⬤⬤ = L4)
  - Improvement priorities panel with cluster tags and next-level transition
  - L0-L4 legend panel with score mapping
  - Live progress bar during audit (spinner · bar · M/N · elapsed time)
- **Polished HTML report** (29KB · self-contained)
  - Composite hero card with grade badge
  - Cluster grid (responsive · 2-4 column auto-fit)
  - Pillar maturity table with colored cells (4-cell L0-L4 bar)
  - Improvement priority cards with counter-incremented numbering
  - L0-L4 legend section
  - Print-friendly CSS (white background · dark text on @media print)
  - Responsive mobile breakpoint at 720px
  - Google Fonts JetBrains Mono integration
- **Unified CLI subcommands** via Click: `audit`, `score`, `report`, `run`
- **`workspace-bench run`** · full pipeline (audit + score + HTML report) in one command with live progress
- **Agent self-audit prompt** documented in README · copy-paste into any LLM with file-system tools

### Changed

- `eval/audit.py` · `eval/score.py` · `eval/report.py` are now thin backwards-compatible shims forwarding to `workspace_bench` package
- Score output now includes `cluster_averages` with cluster names (not just letter codes)
- Audit output `tool` field renamed from `workspace-agentic-benchmark/audit.py` to `workspace-bench`

### Dependencies

- `rich>=13.0` · sophisticated terminal rendering
- `click>=8.0` · CLI structure with subcommands

---

## [0.3.0] · 2026-05-19

### Added

- **3 new pillars** in 4-cluster structure:
  - **Pillar 10 · Reliability & Determinism** (Cluster B · Action) · pass@k consistency · MAST taxonomy coverage · retry+idempotency · replay harness
  - **Pillar 11 · Human-in-the-Loop** (Cluster C · Trust) · approval gates · escalation criteria · feedback collection · approval friction measurement
  - **Pillar 12 · Cost & Performance Efficiency** (Cluster D · Operations) · token economics · cache hit rate · model routing · cost-per-outcome
- **L0-L4 maturity scoring model** (CMMI-inspired) replacing 0-10 banded scoring
  - L0 Absent (0) · L1 Initial (20) · L2 Managed (50) · L3 Defined (75) · L4 Optimizing (100)
  - Composite 0-100 weighted score with letter grades A/B/C/D/F
- **4 cluster structure**: Cognition (A) · Action (B) · Trust (C) · Operations (D)
- `eval/weights.json` · configurable pillar weights (default equal 1/12)
- `submissions/` · MLPerf-style PR-based submission scaffold
- `RFC/` · proposal process for new pillars and rubric revisions
- `CHANGELOG.md` (this file)
- `CONTRIBUTING.md` · contribution guidelines
- 15+ new research sources: CLEAR · MAST · NIST AI RMF · AAGATE · OWASP LLM Top 10 2025 · OpenTelemetry GenAI conventions · CoALA · MemGPT
- MAST 14 failure modes mapped to Pillar 6 (Observability) sub-criteria
- OWASP LLM Top 10 (2025) mapped to Pillar 7 (Credentials/Security) sub-criteria

### Changed

- Pillars now organized into 4 clusters (not flat list of 9)
- Scoring rubrics rewritten as L0-L4 maturity ladders with concrete profiles per level
- `audit.py` · added scan functions for new pillars 10/11/12
- `score.py` · L0-L4 level determination logic · weighted composite computation · cluster aggregation
- `report.py` · L0-L4 visualization · cluster averages · improvement priorities
- Grade thresholds: A ≥85 · B ≥70 · C ≥50 · D ≥30 · F <30 (was A ≥68 / B ≥51 / C ≥34 of v0.2)
- Madani reference example re-audited under v0.3 rubric: 81.25/100 · Grade B (was Grade A on v0.2's looser rubric)

### Documented

- Methodology rewritten with per-pillar evidence + L0-L4 derivation
- README rewritten with cluster grouping + scoring model explanation
- All pillar files updated with cluster designation + weight + L0-L4 rubric

---

## [0.2.1] · 2026-05-19

### Changed

- Framework infrastructure now **vendor-neutral** · all Madani-specific references removed
- Pillar files: "Examples (Good/Bad with Madani names)" → "Profiles (abstract production-grade vs prototype-stage)"
- `audit.py` · path conventions generalized (`00_HARD_RULES` removed · `08_CLIENTI` removed · use `clients/customers/engagements/tenants`)
- `METHODOLOGY.md` · Madani-specific naming replaced with research citations (e.g., "Madani HR15 PRE-OUTPUT" → "Pre-output compliance check pattern · 5-criteria PASS/REFINE/BLOCK gate")
- `research/SOURCES.md` · internal naming replaced with neutral pattern descriptions
- `README.md` · reference example reframed as community case study

### Madani case study moved

- All Madani references now confined to `examples/madani-reference.md` only
- Framework infrastructure (pillars, methodology, eval scripts) fully agnostic

---

## [0.2.0] · 2026-05-19

### Added

- **Pillar 9 · Metacognition & Self-Assessment** (NEW)
  - Based on MetaCogAgent (arXiv 2605.17292v1 · Wang/Shu · May 17, 2026 · 4 days from publication to integration)
  - Operationalizes DPI 3rd condition (Pillar 5) with measurable evidence trigger
  - 10 binary criteria · ECE tracking · capability profile · EMA cybernetic loop
- `pillars/09-metacognition.md` · 320-line pillar specification
- `eval/audit.py` v0.2 · `scan_pillar_9_metacognition` scanner
- `eval/score.py` v0.2 · `score_pillar_9` scorer · updated grade thresholds for 9 pillars
- 4 new research sources: MetaCogAgent · Kadavath (2207.05221) · Xiong (2306.13063) · Guo ECE (ICML 2017)

### Changed

- 8 pillars → 9 pillars (added Pillar 9)
- Grade thresholds: A ≥68 (was 60) · B ≥51 (was 45) · C ≥34 (was 30) · proportional to 90-point total
- README + METHODOLOGY updated for 9-pillar structure

---

## [0.1.0] · 2026-05-19

### Added

- Initial release · 7 pillars · 0-10 scoring per pillar · 0-70 composite
- 7 pillars:
  - P1 Context Hierarchy & Memory
  - P2 Skill / Tool Architecture
  - P3 Governance & Compliance
  - P4 Auto-Improvement Loop
  - P5 Multi-Agent Discipline (DPI)
  - P6 Observability & Recovery
  - P7 Credentials & Security
- `eval/audit.py` · deterministic workspace scanner (no LLM)
- `eval/score.py` · 7-pillar scorer (0-10 per pillar · grade A/B/C/D)
- `eval/report.py` · markdown + HTML report generator
- `research/SOURCES.md` · 30+ papers and benchmarks 2022-2026
- `examples/madani-reference.md` · first reference workspace audit
- MIT License · forward-deploy friendly forking
- **Pillar 8 · Portability & Re-deployability** added shortly after initial release as v0.1 wrap-up

---

## Versioning policy

- **PATCH** (0.x.Y) · vendor-neutrality fixes · evidence updates · audit script improvements
- **MINOR** (0.X.0) · new pillars · scoring model changes · structural rubric revisions
- **MAJOR** (X.0.0) · backwards-incompatible scoring · pillar removal · cluster restructure

Annual rubric refresh planned (avoid Goodhart's law). Pillar additions require RFC process (`RFC/` directory · evidence required: paper · production case study · measurable outcome).

---

## Roadmap

### v0.4 (target Q3 2026)

- 3+ external workspace audits (Anthropic FDE · Palantir · OpenAI agents-SDK example)
- Website live at workspace-bench.org with sortable leaderboard
- `pip install workspace-bench` CLI package
- Empirical weight derivation from correlation analysis across 10+ audits
- LangSmith / AgentOps adapters

### v0.5 (target Q4 2026)

- NeurIPS / ICLR workshop paper
- Inter-rater reliability (κ statistic) protocol published
- Multi-model audit support (validate not Claude-specific)
- Domain-specific weight profiles (financial · healthcare · public sector)

### v1.0 (target Q1 2027)

- Vendor-neutral organization migration (MLCommons-style consortium)
- 30+ public workspace audits on leaderboard
- De-facto standard for FDE engagement evaluation

---

_CHANGELOG.md · maintained as part of v0.3 release · 2026-05-19_
