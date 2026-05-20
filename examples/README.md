# Examples · case studies

> Reference audits from real-world workspaces · for illustration of what `audit.json`, `score.json`, and report output look like. **These are NOT prescriptive templates** — every workspace produces its own audit when scored.

---

## What's in here

| Path | What it is |
|------|-----------|
| `madani-audit.json` · `madani-score.json` · `madani-reference.md` · `madani-report.md` | Latest case study: Madani workspace (private B2B services portfolio · solo-operator profile) · the workspace this benchmark was authored against · transparent reference point |
| `madani-v031/` · `madani-v032/` · `madani-v033/` | Time-series · same workspace at different benchmark versions · shows how scoring evolved across iter-1 → iter-2 |
| `external/` | Audits of public agentic projects (OpenAI Agents · Anthropic Claude SDK · LangChain · CrewAI · AutoGen · Anthropic Cookbook) · for cross-stack comparison |

---

## How to use these

**For your own workspace · do NOT copy these files.** Instead:

```bash
# 1. Install the CLI
pip install git+https://github.com/ceomadani/workspace-agentic-benchmark.git

# 2. Run on YOUR workspace · the audit is fresh per workspace
workspace-bench run /path/to/your/workspace --profile solo-operator-private-repo
```

Use case studies here for:
- Understanding the **shape** of audit.json / score.json output
- Calibrating expectations of what L3/L4 maturity looks like in practice
- Comparing your workspace to known reference points (Madani at composite 85.75 A · OpenAI Agents at 40.83 D · etc.)

---

## Adding your own case study

If you've audited your workspace and want to share (PR welcome):

```
examples/
  your-workspace-name/
    audit.json          # workspace-bench audit output
    score.json          # workspace-bench score output (profile applied)
    README.md           # what stack · what use case · what you learned
```

Anonymize anything sensitive before submitting.

---

## License

Case studies under MIT (same as parent repo). The benchmark is structure-agnostic · examples are illustrative.

---

_examples/ README · iter-2 · 2026-05-20_
