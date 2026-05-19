# RFC NNN: {Title}

- **Status**: draft | accepted | rejected | deferred
- **Author**: Your Name · your.email@example.com
- **Created**: YYYY-MM-DD
- **Affects**: {pillar X · cluster Y · scoring model · etc.}
- **Target version**: 0.X.0

---

## Summary

One paragraph explaining the proposed change. What changes · what stays the same.

## Motivation

Why does this change matter? What is the gap in the current framework?

Required: cite at least one of:
- Peer-reviewed paper (with arXiv link or DOI)
- Production case study with measurable outcome
- Production incident postmortem
- Empirical correlation analysis from existing audits

## Proposed change

Detailed specification.

### If adding a new pillar
- Cluster: A · Cognition / B · Action / C · Trust / D · Operations
- First principle (one sentence)
- L0-L4 maturity rubric (full text)
- Sub-criteria (3-5)
- Evidence sources
- Anti-patterns to block
- How it integrates with existing pillars
- Default weight

### If revising a rubric
- Current rubric (excerpt)
- Proposed rubric (excerpt)
- Diff explanation

### If structural change
- What changes in audit.py · score.py · report.py
- Migration path for existing submissions
- Backward compatibility considerations

## Orthogonality argument

Why is this proposal *not redundant* with existing pillars? Map your proposed dimension against each of the 12 current pillars and explain why it doesn't fit any of them.

## Impact on existing scores

Estimate how a typical Grade A workspace would score under the new structure. Would scores rise · fall · stay flat? Why?

If you have audited a workspace, include before / after numbers.

## Alternatives considered

What other approaches could solve this problem? Why is your proposal the best?

Steel-man the strongest counter-argument and respond to it.

## Open questions

What aspects of this proposal need community input?

## References

- [Paper or source 1](https://arxiv.org/abs/...)
- [Paper or source 2](https://...)

---

## Discussion (filled by maintainers)

### Reviewer notes

(Reviewers add comments here · or in PR thread)

### Decision

- **Outcome**: TBD
- **Decided by**: TBD
- **Decided on**: TBD
- **Rationale**: TBD

### Next steps if accepted

- [ ] Update `pillars/{NN}-{slug}.md`
- [ ] Update `eval/audit.py`
- [ ] Update `eval/score.py`
- [ ] Update `eval/report.py`
- [ ] Update `eval/weights.json` if weight changes
- [ ] Update `METHODOLOGY.md`
- [ ] Update `README.md`
- [ ] Update `research/SOURCES.md`
- [ ] Update `CHANGELOG.md`
- [ ] Re-audit `examples/madani-reference.md` (and any other reference workspaces)

---

_RFC template v0.3 · 2026-05-19_
