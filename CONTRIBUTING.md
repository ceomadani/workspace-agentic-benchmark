# Contributing to the Workspace Agentic Benchmark

Thanks for your interest in contributing. This benchmark survives or fails based on community input — your audits, your edge cases, your proposed pillars.

---

## Three ways to contribute

### 1. Score your workspace · submit as reference example

The leaderboard gains credibility with each documented audit. To add yours:

1. Run the audit on your workspace:
   ```bash
   python3 eval/audit.py /path/to/your/workspace > audit.json
   python3 eval/score.py audit.json > score.json
   python3 eval/report.py score.json --output report.md
   ```
2. Fork the repo · add your audit to `submissions/` (see [submissions/README.md](submissions/README.md) for the MLPerf-style template)
3. Open a PR with:
   - `submissions/{your-workspace-name}/metadata.yaml` · stack · domain · contact
   - `submissions/{your-workspace-name}/audit.json` + `score.json` + `report.md`
   - `submissions/{your-workspace-name}/evidence/` · 3-5 file paths or commit SHAs that substantiate the highest-scoring criteria
4. Maintainers review (target: 14 days)
5. On merge: entry appears on the leaderboard

**Confidentiality**: redact paths/keys if needed · maintain audit reproducibility for at least the 3-5 evidence pointers.

---

### 2. Propose new pillars / rubric revisions · RFC process

If you've found a workspace dimension this benchmark misses, or a rubric that doesn't match production reality:

1. Read existing pillars and the methodology
2. Draft an RFC using the template at `RFC/template.md`
3. Required evidence (at least one of):
   - Peer-reviewed paper grounding the dimension
   - Production case study with measurable outcome
   - Production incident postmortem demonstrating the gap
4. Open a PR adding `RFC/{NNN}-{slug}.md` (number sequentially)
5. Discussion in PR thread · 2 maintainers + 1 external reviewer required for merge
6. Accepted RFCs enter the next MINOR release (annual cadence target)

**Evidence quality matters more than evidence quantity**. One well-cited paper or one documented incident with measurable impact beats five vague references.

---

### 3. Audit script + evidence improvements

`workspace_bench/audit.py` is deterministic but heuristic. If your workspace has a legitimate signal we're missing:

1. Add the signal detection to the relevant `scan_pillar_N` function
2. Test against the reference workspaces in `examples/` — the score on those existing audits should NOT change unless you're fixing a real bug (anti-gaming · the detector must be vendor-neutral)
3. Open a PR with:
   - Description of the signal · what it detects · why it matters
   - A test workspace (fixture in `tests/`) where the signal is present
   - A test workspace where it's absent
   - The detector must match the signal **by semantic pattern**, not by hardcoded path/filename specific to one workspace's naming convention

False positives are worse than false negatives. Be conservative. Vendor-neutral always.

---

## Quality bar

We aim to keep the bar high on:

- **Evidence**: every claim cites a paper · production incident · or measurable production outcome
- **Vendor neutrality**: framework infrastructure is agnostic · case studies live in `examples/` only
- **Determinism**: ~70% of the audit runs without LLM calls · prefer pattern matching over LLM-judging
- **Actionability**: every L0-L4 level should describe a concrete profile a reader can recognize

We will reject contributions that:

- Add features without evidence (no "we should probably measure X")
- Inflate scoring (every workspace deserves criticism on at least one pillar)
- Add vendor-specific patterns to the framework (only to `examples/`)
- Add LLM-judging where a deterministic check would work

---

## Communication

- Issues for clarifications, bug reports, edge cases
- PRs for code, rubric, documentation changes
- RFC for structural changes (new pillars, new clusters, scoring model changes)
- Discussions for "is this a pillar gap?" exploratory questions

---

## Code of conduct

Be precise. Be honest. Be skeptical of every claim — including ours. The benchmark is only useful if it's defensible under scrutiny.

When in doubt, cite a paper.

---

_CONTRIBUTING.md · v0.3 · 2026-05-19_
