# RFC Process · proposing changes to the benchmark

> Request For Comments process for new pillars, rubric revisions, and structural changes.

---

## When to write an RFC

Required for:
- **New pillars** (e.g., proposing P13 · Privacy & Data Governance)
- **Structural changes** (e.g., cluster restructure · scoring model overhaul)
- **Major rubric revisions** (e.g., changing L0-L4 to L1-L5 · changing weights)
- **Pillar deprecation** (e.g., proposing P_N is redundant with P_M)

Not required for:
- Bug fixes in audit.py / score.py / report.py (just open a PR)
- Adding evidence sources to existing pillars (PR)
- Improving pillar markdown documentation (PR)
- Adding submissions or examples (PR)

If in doubt, open an issue first to ask.

---

## Process

### 1. Draft

1. Copy `RFC/template.md` to `RFC/{NNN}-{slug}.md` where:
   - `NNN` is the next sequential number (zero-padded · `001` · `002` · etc.)
   - `slug` is lowercase dash-separated descriptive name (e.g., `001-add-privacy-pillar`)
2. Fill all sections of the template

### 2. Evidence

Every RFC requires at least one of:
- Peer-reviewed paper grounding the proposed change
- Production case study with measurable outcome
- Production incident postmortem demonstrating the gap
- Empirical correlation analysis from 5+ existing audits

RFCs without evidence will be closed without discussion.

### 3. Open PR

```bash
git checkout -b rfc/{NNN}-{slug}
git add RFC/{NNN}-{slug}.md
git commit -m "rfc: {NNN} {short title}"
gh pr create --title "RFC {NNN}: {title}" --body "Evidence: {paper / case study / incident}"
```

### 4. Discussion

- Maintainers respond within 14 days
- Community discussion in PR thread (no time limit · 30 days minimum before merge)
- Reviewer requirements:
  - 2 maintainer approvals
  - 1 external reviewer (rotating from accepted submissions pool)
  - For breaking changes (major version bump): 4 maintainer approvals + 2 external

### 5. Decision

Three outcomes:
- **Accepted** · merged into `RFC/` · scheduled for next MINOR release · CHANGELOG updated
- **Rejected** · merged into `RFC/` with `status: rejected` · rationale documented (we keep rejected RFCs for future reference · evidence may strengthen over time)
- **Deferred** · merged with `status: deferred` · "interesting but premature" · revisit at next annual review

### 6. Annual review

All pending RFCs reviewed annually (target: January). Rejected RFCs revisited if new evidence emerges.

---

## Quality bar

Strong RFCs:
- Cite specific papers with arXiv numbers
- Explain why the proposed dimension is **orthogonal** to existing pillars (not redundant)
- Provide a measurable criterion for L0-L4 (or whatever scoring model)
- Estimate impact on existing audits (will scores rise / fall / stay)
- Acknowledge counter-arguments and steel-man them

Weak RFCs (will be rejected):
- "We should measure X" with no evidence why
- Vendor-specific proposals (e.g., "Pillar 13: Claude-specific features")
- Proposals that duplicate existing pillars
- LLM-judged criteria where deterministic checks would work

---

## Examples of likely RFCs (for v0.4+)

These are reasonable proposals to expect:

- **P13 · Privacy & Data Governance** · GDPR · PII handling · data retention · cross-engagement leakage
- **P14 · Interoperability & Standards** · MCP adoption · OpenAPI · OTEL GenAI conventions · A2A protocol
- **P15 · Multi-Modal Capability** · text + vision + audio + voice integration · cross-modal memory
- **Weight rebalancing** · empirical re-weighting from 10+ audit correlation analysis
- **Sub-criteria refinement** · per-criterion evidence weight (currently treated as binary)

We will not pre-empt these · they need to be proposed via this process with evidence.

---

_RFC/README.md · v0.3 · 2026-05-19_
