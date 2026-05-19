# Pillar 2 · Skill / Tool Architecture

> **First principle**: *A skill is a contract with the agent · contracts must be discoverable, fresh, and minimal.*
> **Max score**: 10 points.

---

## Why this pillar exists

As skill counts grow past 20, discovery degrades. Stale skills fire on wrong triggers and poison agent behavior. Determinism wins where possible (cheaper · faster · auditable). The Voyager (arXiv 2305.16291) and hermes-agent (NousResearch) patterns demonstrate that skill libraries are valuable *only if* they have growth + curation mechanisms.

---

## Scoring criteria · 10 binary checks

1. **[1.0]** Skills stored in dedicated location (e.g., `skills/` or `.claude/skills/`).
2. **[1.0]** Each skill is a self-contained unit (folder with SKILL.md + assets).
3. **[1.0]** Skills have frontmatter with name · description · trigger conditions.
4. **[1.0]** Auto-trigger / discovery mechanism (description matching, not just manual invoke).
5. **[1.0]** Staleness detection · cron or audit flags unused / outdated skills.
6. **[1.0]** Determinism preferred · deterministic tools count > 30% of total.
7. **[1.0]** Skills curated · roster file documents active/deprecated/experimental.
8. **[1.0]** Skill changelog or version field · track evolution.
9. **[1.0]** No "grab-bag" mega-skills (>2000 lines, multiple unrelated functions).
10. **[1.0]** Skills cross-reference · related skills linked explicitly.

---

## Scoring rubric

| Score | Profile |
|-------|---------|
| **9-10** | Auto-trigger · staleness cron · versioned · curated roster · determinism preferred · cross-linked |
| **7-8** | Dedicated location · frontmatter · most auto-trigger · some staleness check |
| **5-6** | Some structure · partial frontmatter · no staleness check |
| **3-4** | Scripts scattered · no frontmatter · manual invoke only |
| **0-2** | No skill layer · ad-hoc shell aliases |

---

## Evidence sources

- **NousResearch hermes-agent** · staleness curator pattern (auto-flag unused skills).
- **Voyager (arXiv 2305.16291)** · skill library compositional + iterative refinement.
- **Anthropic Skills documentation** · auto-trigger via description matching.
- **DGM (Discovery-Guided Mining)** · skill emergence from agent traces.

---

## Anti-patterns

- ❌ Grab-bag mega-skills (one skill that does everything · loses focus)
- ❌ No staleness check · 18 skills from 6 months ago that nobody uses
- ❌ Skills with LLM calls where shell commands would work
- ❌ Skills with no description · agent can't trigger correctly
- ❌ Skills that depend on deleted files / dead paths
- ❌ Skill registry as flat list · no curation tier

---

## Profiles

**Production-grade (8-10)**:
- Skills in dedicated location (`skills/` or `.claude/skills/` or `agents/skills/`)
- Active vs deprecated tier explicit (curated roster file)
- Auto-staleness cron (e.g., daily scan flags unused skills)
- Each skill is a folder with `SKILL.md` + assets + frontmatter (`name` · `description` · `triggers`)
- ≥30% deterministic tools (no LLM call) · prefer shell + Python over LLM where possible
- Skills cross-referenced (related skills linked)

**Prototype-stage (1-3)**:
- `scripts/` folder with random files · no frontmatter · no descriptions
- All require manual invocation by name
- No staleness check · half of them no longer run
- No distinction between active and deprecated

---

## How to improve from low score

| From | To | Action |
|------|-----|--------|
| 0-3 | 5 | Move scripts into `skills/` folders with SKILL.md per skill · add frontmatter |
| 4-6 | 7 | Implement auto-trigger via description matching · curate active/deprecated roster |
| 7-8 | 9 | Add staleness detector cron · audit for grab-bag skills · split mega-skills |
| 9 | 10 | Cross-link related skills · version each · prefer deterministic when possible |

---

## Self-audit questions

- How many skills exist · and how many fired in the last 30 days?
- What happens when a skill's underlying tool / API is deprecated?
- Can the agent discover the right skill from natural-language intent?
- Is there a deterministic shell command that does what an LLM-skill does?
