# Pillar 11 · Human-in-the-Loop

> **Cluster C · Trust**
> **First principle**: *The most consequential decisions must pass through a human gate · and the workspace must make that gate easy to use.*
> **Weight**: 1/12 (equal-weighted baseline · v0.3 default)

---

## Why this pillar exists

The MAST failure taxonomy (arXiv 2503.13657) found that **41.77% of multi-agent system failures stem from specification ambiguity** — the top failure mode across 7 frameworks. Most of these failures could have been prevented by escalation to a human operator before execution. Yet escalation paths are systematically under-measured in agentic workspaces.

This pillar measures whether the workspace has well-designed approval flows, escalation paths, and feedback collection — the seams where humans and agents collaborate.

---

## L0-L4 Maturity Rubric

| Level | Score | Profile |
|-------|------:|---------|
| **L0 Absent** | 0 | No human gates. Agent ships any output anywhere. No feedback loop. |
| **L1 Initial** | 20 | Operator manually reviews high-stakes outputs (in their head · undocumented). No structured feedback mechanism. |
| **L2 Managed** | 50 | Approval gates for irreversible / external actions documented in policy. Operator can `/approve` or `/reject` in conversation. Feedback collected ad-hoc. |
| **L3 Defined** | 75 | Approval gates enforced via hooks or middleware (cannot be bypassed). Escalation criteria documented per task class (e.g., low metacognitive confidence → escalate). Feedback collection structured (positive/negative signal extracted from session). |
| **L4 Optimizing** | 100 | Approval friction measured (time-to-approve · approval rate · revoked actions). Feedback loop closes back into capability profile (P9 Metacognition) and skill staleness (P2). Auto-escalation on confidence drop. |

---

## Sub-dimensions

### 11.1 · Approval gate enforcement
- L0: agent auto-executes everything
- L1: agent asks "should I?" inconsistently
- L2: documented list of actions requiring approval (external messages · git push · payments · destructive ops)
- L3: approval gate enforced via hooks (cannot proceed without explicit `yes`)
- L4: approval gate + dry-run mode by default · explicit `--ship` flag required

### 11.2 · Escalation criteria
- L0: no escalation
- L1: ad-hoc "I'm not sure" prompts
- L2: documented escalation rules (e.g., "for legal questions, escalate")
- L3: escalation triggered by signals (low MetaCog confidence · novel domain · conflicting rules)
- L4: escalation cost-aware · routes to right human (legal vs technical vs business) · SLA tracked

### 11.3 · Feedback collection structure
- L0: no feedback captured
- L1: operator types corrections inline · lost after session
- L2: corrections logged but not structured
- L3: structured extraction of `r_k` ∈ {0, 1} per task · feeds capability profile
- L4: positive feedback also captured (validated approaches) · feedback drives skill discovery

### 11.4 · Approval friction measurement
- L0: not measured
- L1: anecdotal
- L2: occasional review
- L3: time-to-approve tracked · approval rate per category logged
- L4: friction-adjusted: high-trust paths require less approval over time · low-trust expanded

### 11.5 · Bypass detection
- L0: bypasses go unnoticed
- L1: occasional discovery via incident
- L2: bypass log exists
- L3: every approval-required action either passed the gate or has logged exception
- L4: zero unapproved external actions in last N days · invariant enforced

---

## Evidence sources

- **MAST** (arXiv [2503.13657](https://arxiv.org/abs/2503.13657)) · specification failure = 41.77% of MAS failures · top mode · escalation is the prevention.
- **Anthropic "Effective Harnesses"** · operator-as-collaborator pattern · approval-friction tradeoffs.
- **NIST AI RMF 1.0** · Govern function · human oversight as core control.
- **AAGATE** (arXiv [2510.25863](https://arxiv.org/abs/2510.25863)) · NIST-aligned governance for agentic AI · explicit human-in-the-loop functions.
- **Production incident postmortems** · the most-cited cause of agent-caused harm is *automated execution that should have escalated* (Slack send · email · git push · API write).

---

## Anti-patterns

- ❌ **"Just ship it" mode by default** without explicit escalation policy.
- ❌ **Approval gates that can be bypassed** with a flag (`--force`) used routinely.
- ❌ **Asking for approval on everything** · approval fatigue · operator rubber-stamps.
- ❌ **Feedback only collected on failure** · validated successes also feed the loop.
- ❌ **Escalation that loops back to same agent** instead of routing to a human.

---

## Profiles

**Production-grade (L3-L4)**:
- Approval gates listed in constitution · enforced by middleware
- Escalation criteria documented (low confidence · novel domain · destructive op · external action)
- Structured feedback extraction from sessions (positive AND negative signal)
- Approval friction measured monthly · adjustable per task class
- Zero unapproved external actions in audit log

**Prototype-stage (L0-L1)**:
- Agent sends external messages without asking
- No escalation criteria · operator catches things by accident
- Feedback "I should remember this" lives only in operator's head
- No approval log · no audit trail

---

## Relation to other pillars

- **P3 Governance** · governance defines *what* requires approval · this pillar measures *how well* approval gates function operationally.
- **P9 Metacognition** · MetaCog confidence drop triggers escalation here · clean handoff.
- **P4 Auto-Improvement** · structured feedback from this pillar feeds the improvement loop's outcome signal.

---

## How to improve from low level

| From | To | Action |
|------|-----|--------|
| L0 → L2 | List actions that require approval (external messages · git push · payments · destructive). Document escalation rules. Begin manual review tracking. |
| L2 → L3 | Enforce gates via hooks (`pre-tool-use`, `pre-action` middleware). Add escalation triggers based on metacognitive confidence. Structure feedback as binary `r_k` signal. |
| L3 → L4 | Measure approval friction (time-to-approve · rate). Close feedback loop into capability profile. Add bypass detection invariant. |

---

## Self-audit questions

- Which external actions can your agent perform without explicit human approval?
- When the agent isn't sure, what triggers escalation · and to whom?
- If the operator corrects an output, does that correction shape future behavior or vanish?
- How long does it take to approve a typical action · is that latency tracked?

---

_Pillar 11 · v0.3 · 2026-05-19 · pattern source MAST taxonomy + NIST AI RMF · novel addition to public agentic workspace benchmarks_
