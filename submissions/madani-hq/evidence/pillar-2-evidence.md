# Pillar 2 · Skill / Tool Architecture · L4 Optimizing

## What the audit detected
A large, schema-governed skill library with SKILL.md frontmatter, plus automated curation of
stale/unused skills.

## Substantiating artifacts
- `10_SKILLS/` · 57 skill directories, each with a `SKILL.md` (trigger + prescriptive workflow).
- `10_SKILLS/CLAUDE.md` · canonical skill schema — required frontmatter: name · title · summary · description · model · tools · provenance · version · last_updated · changelog_inline.
- `11_TOOLS/skill-staleness-detector.py` · "Hermes" daily cron (02:30) flagging stale / unused / incomplete skills.
- `CLAUDE.md` HR#12 + HR#15 · skill-discovery-FIRST and auto-discover/auto-create/auto-update discipline before generating any content.

## Operator commentary
Skills are versioned and provenance-tracked, and the Hermes curator closes the loop by detecting
decay automatically — so the library improves iteration-over-iteration rather than freezing at v1.
That auto-curation is the L3→L4 differentiator.
