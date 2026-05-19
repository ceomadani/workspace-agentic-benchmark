# Submissions · Workspace Agentic Benchmark Leaderboard

> MLPerf-style PR-based submission process for the public leaderboard.

---

## Why submit

The leaderboard gains credibility with each documented audit. Your submission becomes:
- A reference example for other workspaces in the same domain / stack
- A data point for empirical weight derivation in v0.4+
- Public recognition of your workspace's maturity

The leaderboard is **not a competition** — it's a maturity map. A Grade B with documented improvement velocity is more valuable than a static A.

---

## Submission process

### 1. Run the audit

```bash
cd workspace-agentic-benchmark
python3 eval/audit.py /path/to/your/workspace > audit.json
python3 eval/score.py audit.json > score.json
python3 eval/report.py score.json --output report.md
```

### 2. Create your submission folder

```
submissions/
└── {your-workspace-slug}/        # e.g., "anthropic-fde-cwc", "acme-corp-prod"
    ├── metadata.yaml              # required · see template below
    ├── audit.json                 # required · output of audit.py
    ├── score.json                 # required · output of score.py
    ├── report.md                  # required · output of report.py
    └── evidence/                  # required · 3-5 substantiating artifacts
        ├── pillar-N-evidence.md   # one per pillar with score ≥ L3
        └── ...
```

### 3. Fill metadata.yaml

See `template/metadata.yaml.template` for the schema:

```yaml
workspace_name: "Acme Corp Internal Agent"
slug: "acme-corp-prod"
domain: "financial-services"  # or healthcare · ecommerce · saas · public-sector · personal · other
stack:
  - "Claude Code"
  - "n8n"
  - "Custom Python tools"
  - "Supabase"
size:
  total_files: 1247
  total_loc: 89000
  age_months: 14
submitted_by: "Your Name · your.email@example.com"
submitted_at: "2026-06-15"
benchmark_version: "0.3.0"
public: true  # set false to leave off public leaderboard but keep on file
confidentiality:
  redacted_paths: false  # set true if you redacted internal paths
  redacted_credentials: true  # always true for safety
notes: |
  Optional notes about your workspace · constraints · domain-specific decisions ·
  what you'd score yourself differently and why.
```

### 4. Substantiate high-scoring pillars

For each pillar scoring L3 or L4, add evidence in `evidence/pillar-N-evidence.md`:

```markdown
# Pillar N · {Title} · L3 / L4 evidence

## What the audit detected
{summary of signals found}

## Substantiating artifacts (3-5 minimum)
- `path/to/file-or-commit-1` · {one-line description of what this proves}
- `path/to/file-or-commit-2` · {description}
- `sha:abc1234` · {description}

## Operator commentary (optional)
{any context that helps the reviewer understand why this pillar reached this level}
```

This prevents score gaming · the audit can be fooled by keyword stuffing · the evidence cannot.

### 5. Open a PR

```bash
git checkout -b submission/{your-workspace-slug}
git add submissions/{your-workspace-slug}/
git commit -m "submission: {workspace-name} · Grade {X} · v0.3"
git push origin submission/{your-workspace-slug}
gh pr create --title "Submission: {workspace-name}" \
  --body "Composite: {X}/100 · Grade {Y} · {domain} · {stack}"
```

### 6. Review

- 2 maintainers review the submission
- 1 external reviewer (rotating · drawn from prior accepted submissions)
- Target turnaround: 14 days
- Reviewer checks: evidence sufficiency · audit reproducibility · metadata accuracy · confidentiality redactions

On merge:
- Entry appears on the leaderboard (website v0.4+)
- Cited in CHANGELOG for the version that accepted it
- Submitter invited to be a rotating external reviewer for future submissions

---

## Confidentiality and redaction

Acceptable redactions:
- Internal paths (e.g., `/Users/alice/work/proj` → `/Users/REDACTED/proj`)
- Customer / client names (use placeholders · `customer_A`, `customer_B`)
- Internal tool names (rename to `internal-tool-1` if needed)

NOT acceptable:
- Removing failing signals to inflate the score
- Stripping evidence pointers entirely
- Modifying the audit.json or score.json output (must be unmodified tool output)

If you cannot disclose enough to substantiate L3+ scores, set `public: false` in metadata.yaml. You'll receive a private confirmation but no leaderboard entry. Useful for compliance-sensitive submissions.

---

## Re-submissions

Workspaces evolve. Re-submit any time:
- Same slug, increment `metadata.yaml` version field
- New `audit.json` + `score.json` + `report.md`
- Diff with previous submission in PR description

Tracking deltas over time is more valuable than static scores. Quarterly re-submission encouraged.

---

## Disqualification criteria

Submissions will be rejected if:
- Audit output was manually edited
- Evidence pointers don't substantiate the claimed score
- Workspace is fictional / not actually deployed
- Single-person workspace claiming team-grade portability without isolation evidence

We will not name and shame · simply close the PR with explanation.

---

_submissions/README.md · v0.3 · MLPerf-inspired process · 2026-05-19_
