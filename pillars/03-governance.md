# Pillar 3 · Governance & Compliance

> **First principle**: *Every irreversible or externally-visible action must pass an explicit gate. No silent execution.*
> **Max score**: 10 points.

---

## Why this pillar exists

Agents have no inherent moral or operational reasoning · they need explicit gates. Without HARD RULES, agents drift toward compliance theater ("sure!") and irreversible actions (pushing to main · sending external messages · dropping tables). ~80% of agent-caused production harm in observed FDE engagements comes from missing approval gates on external actions.

---

## Scoring criteria · 10 binary checks

1. **[1.0]** Constitution document exists (`CONSTITUTION.md` or equivalent) · loaded into agent context.
2. **[1.0]** HARD RULES enumerated (numbered list · not buried in prose).
3. **[1.0]** Pre-output check exists · agent self-validates before significant emission.
4. **[1.0]** External-action approval gate (no auto-send Slack · email · git push to main).
5. **[1.0]** Destructive-action gate (no auto rm -rf · drop table · force-push · branch delete).
6. **[1.0]** Constitution versioned · changelog of rule changes.
7. **[1.0]** Compliance judge or audit mechanism · validates outputs against rules.
8. **[1.0]** Rules cross-link to evidence (incident · paper · explicit user decision).
9. **[1.0]** Documented escalation path · what happens when rule conflict arises.
10. **[1.0]** Per-project rules layered on top of global rules (no monolithic ruleset).

---

## Scoring rubric

| Score | Profile |
|-------|---------|
| **9-10** | Constitution · numbered HARD RULES · pre-output check · approval gates · compliance judge · cross-linked evidence · layered |
| **7-8** | Constitution · HARD RULES · most gates · ad-hoc compliance check |
| **5-6** | Some rules documented · partial gates · no compliance judge |
| **3-4** | Few scattered rules · most actions auto-execute |
| **0-2** | No constitution · no gates · agent acts on every request |

---

## Evidence sources

- **Anthropic Constitutional AI (arXiv 2212.08073)** · explicit principles outperform implicit alignment.
- **Madani HR15 PRE-OUTPUT compliance check** (5-criteria) · empirical drift reduction.
- **Production incident pattern** · ~80% of agent harm from missing external-action approval.
- **OWASP LLM Top 10** · LLM06: Insecure Output Handling.

---

## Anti-patterns

- ❌ "Be helpful" as the only rule · no enforcement mechanism
- ❌ Rules buried in 5000-word `CLAUDE.md` · agent can't find them at decision time
- ❌ Auto-send to Slack / email / API without per-action approval
- ❌ Git push to main without gate
- ❌ Rules without evidence · "we should probably..." style
- ❌ Conflicting rules with no resolution protocol

---

## Profiles

**Production-grade (9-10)**:
- `CONSTITUTION.md` (or equivalent) with numbered HARD RULES enumerated
- Pre-output compliance check (e.g., 5-criteria PASS / REFINE / BLOCK gate)
- Dedicated compliance-judge sub-agent or validation script
- Explicit gates: only owner pushes to main · external messages require approval · destructive ops gated
- Rules cross-link to documented incidents or research evidence
- Versioned constitution with changelog

**Prototype-stage (1-2)**:
- No `CLAUDE.md` / `AGENT.md` / equivalent
- Agent sends external messages (Slack · email) automatically
- No pre-output check · high redaction rate from user
- No git push gate · no approval flow for irreversible actions

---

## How to improve from low score

| From | To | Action |
|------|-----|--------|
| 0-3 | 5 | Write CONSTITUTION.md · enumerate 5-10 HARD RULES · document external-action approval flow |
| 4-6 | 7 | Add pre-output compliance check · add approval gates for git push / Slack send / API call |
| 7-8 | 9 | Implement compliance judge (sub-agent or check script) · cross-link rules to evidence |
| 9 | 10 | Layer per-project rules · document escalation · version constitution with changelog |

---

## Self-audit questions

- When did the agent last execute an external action (Slack / email / API write) · did it ask first?
- What happens when two rules conflict · who decides?
- Is the constitution loaded into agent context · or buried in a folder it never reads?
- Has any rule been added because of a documented incident · or are they all theoretical?
