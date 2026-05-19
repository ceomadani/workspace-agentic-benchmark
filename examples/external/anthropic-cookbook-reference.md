# Anthropic Cookbook · External Reference Audit

> **Score**: 27.5 / 100 · Grade **F** (failing — but contextually appropriate)
> **Audited**: 2026-05-20 (workspace-bench v0.3.2)
> **Source**: github.com/anthropics/anthropic-cookbook
> **Workspace type**: code-sample repository (NOT a production workspace)

This audit is included as an **external reference example** to validate
vendor-neutrality of the benchmark: the same audit tooling that scores Madani
(81.25/100 · A on v0.3.2) is run on Anthropic's own public repository. The
result demonstrates that the benchmark correctly distinguishes between a
*production workspace* and a *code-sample repository*.

---

## Score breakdown

| # | Pillar | Cluster | Level | Score |
|---|--------|---------|-------|------:|
| 1 | Context Hierarchy & Memory | A · Cognition | L1 Initial | 20 |
| 2 | Skill / Tool Architecture | B · Action | L2 Managed | 50 |
| 3 | Governance & Compliance | C · Trust | L2 Managed | 50 |
| 4 | Auto-Improvement Loop | A · Cognition | L0 Absent | 0 |
| 5 | Multi-Agent Discipline (DPI) | B · Action | L0 Absent | 0 |
| 6 | Observability & Recovery | C · Trust | L1 Initial | 20 |
| 7 | Credentials & Security | C · Trust | L2 Managed | 50 |
| 8 | Portability & Re-deployability | D · Operations | L1 Initial | 20 |
| 9 | Metacognition & Self-Assessment | A · Cognition | L0 Absent | 0 |
| 10 | Reliability & Determinism | B · Action | L2 Managed | 50 |
| 11 | Human-in-the-Loop | C · Trust | L1 Initial | 20 |
| 12 | Cost & Performance Efficiency | D · Operations | L2 Managed | 50 |

**Composite**: 27.5 / 100 → **Grade F**

---

## Why this score is *appropriate* (not a failure of the repo)

The benchmark is designed to measure **production workspace infrastructure**.
A code-sample repository has different design goals: provide runnable examples
of API usage, illustrate patterns, host snippets that developers can copy.
Anthropic cookbook is excellent at what it's designed for.

The audit correctly identifies that the cookbook:
- ✅ Has skill/tool examples (P2 L2) — many notebooks and scripts present
- ✅ Has governance / compliance docs (P3 L2) — LICENSE · CONTRIBUTING · CLAUDE.md
- ✅ Mentions credentials handling (P7 L2) — examples show API key usage
- ✅ Cookbook reliability concepts (P10 L2) — retry/idempotency in examples
- ✅ Cost-efficient patterns documented (P12 L2) — caching examples present
- ❌ No auto-improvement loop (P4 L0) — not a workspace · no sessions to learn from
- ❌ No multi-agent policy (P5 L0) — not the cookbook's concern
- ❌ No metacognition layer (P9 L0) — not applicable to a static repo
- ❌ Limited observability (P6 L1) — example repos don't need cron monitoring
- ❌ Limited portability infrastructure (P8 L1) — not designed for FDE engagement

---

## What this teaches about the benchmark

**Validation of vendor-neutrality**: the audit doesn't favor Madani.
Anthropic's own publicly maintained repository scores F under the same rubric.
The L0-L4 model is strict and applies uniformly.

**The benchmark measures workspace, not codebase**: a great codebase can score
poorly on this benchmark if it's not designed *as a workspace*. The two
artifacts have different success criteria.

**Counter-positioning**: if you have a high score (B+ or A) on this benchmark,
you're operating at a different infrastructural altitude than typical
public repositories — including those maintained by frontier-lab teams.
The frontier labs invest in *model capability* publicly, but the workspace
discipline lives inside the FDE engagements (where Palantir's pattern
originated).

---

## How to interpret an F grade

An F grade on this benchmark is NOT a quality judgment of the repository.
It means:
- The repository is not designed as a production agentic workspace
- OR the workspace exists but is at prototype maturity
- OR the workspace infrastructure has not yet been built

For a code-sample repository like anthropic-cookbook, F is the expected and
correct score. Repositories that aspire to be production workspaces should
work through the improvement priorities documented in the per-pillar files.

---

## Reproduce this audit

```bash
git clone --depth 1 https://github.com/anthropics/anthropic-cookbook.git /tmp/anthropic-cookbook
pip install git+https://github.com/ceomadani/workspace-agentic-benchmark.git
workspace-bench audit /tmp/anthropic-cookbook --output audit.json
workspace-bench score audit.json --output score.json
workspace-bench report score.json --output report.html
```

---

## File index

- `anthropic-cookbook-audit.json` · raw audit signals
- `anthropic-cookbook-score.json` · L0-L4 + composite + grade
- `anthropic-cookbook-reference.md` · this document

---

_External reference example v0.3.3 · 2026-05-20 · validates vendor-neutrality_
