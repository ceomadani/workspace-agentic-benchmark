# Pillar 8 · Portability & Re-deployability

> **First principle**: *A workspace must be re-deployable on a new engagement in days, not months. FDE-grade.*
> **Max score**: 10 points.

---

## Why this pillar exists

**Forward Deploy Engineering (FDE)** is the practice of deploying agentic systems to actual customer environments (Anthropic FDE · Palantir FDE model). The key FDE metric is **time-to-first-impact**: days from engagement embed to first business KPI delta. MIT research shows ~95% of AI pilots fail to convert to production. The differentiator between failed pilots and shipped systems is **harness portability** — can the same infrastructure be re-instantiated on the next client?

This pillar is **unique to this benchmark** — no public benchmark currently measures workspace re-deployability. Anthropic's "Effective Harnesses" doctrine doesn't address it. It is the FDE-specific differentiator.

---

## Scoring criteria · 10 binary checks

1. **[1.0]** Bootstrap procedure documented (1 page or less · ordered steps to instantiate on new machine).
2. **[1.0]** Skills are client-agnostic OR explicitly tagged client-specific (clear abstraction layer).
3. **[1.0]** Credentials per-engagement isolated (separate vault namespace · no cross-tenant leakage).
4. **[1.0]** Per-environment separation (dev / staging / prod · or client A / client B distinct).
5. **[1.0]** Workspace state externalized (not bound to single machine · cloud sync · git-backed).
6. **[1.0]** Template / scaffold exists for new project setup (`templates/` or `scaffold/`).
7. **[1.0]** Memory tiers per-engagement isolated (no semantic memory cross-contamination · compliance P0).
8. **[1.0]** Handoff artifact when operator rotates (session summary · handoff doc · architectural decision record).
9. **[1.0]** Time-to-bootstrap measured (last redeployment timed · or synthetic test documented).
10. **[1.0]** Same architecture instantiated more than once (proves repeatability · not single-snowflake).

---

## Scoring rubric

| Score | Profile |
|-------|---------|
| **9-10** | Bootstrap doc · client-agnostic skills · vault isolation · cross-engagement memory separation · timed redeployment · scaffold · repeatable |
| **7-8** | Bootstrap exists · most skills generalizable · vault isolation · handoff doc |
| **5-6** | Partial documentation · ad-hoc replication · single client used |
| **3-4** | Manual everything · everything entangled with single project |
| **0-2** | Workspace is a snowflake · cannot be replicated · personal-only |

---

## Evidence sources

- **Palantir FDE doctrine** · forward deployed engineering as a practice.
- **Anthropic FDE model** · embedded engineers · customer impact-driven.
- **MindStudio FDE analysis** · pilot-to-production conversion rates.
- **MIT AI pilot research** · 95% pilot failure rate · workspace infrastructure as differentiator.
- **HashiCorp Vault** · multi-tenant secret isolation patterns.

---

## Anti-patterns

- ❌ **Single-snowflake workspace**: bound to one machine · one user · one project. Cannot be replicated.
- ❌ **Cross-engagement memory leakage**: semantic memory contains facts from multiple clients · P0 compliance risk in regulated industries.
- ❌ **Hardcoded paths everywhere**: `/Users/yourname/...` in scripts · breaks on every other machine.
- ❌ **No handoff artifact**: when FDE rotates off, knowledge dies with them.
- ❌ **Skills hardcoded to single client's data shape**: re-writing for client B takes weeks.
- ❌ **Credentials in one shared vault for all clients**: blast radius = all clients on any leak.

---

## Examples

**Good (8/10 · Madani · still maturing in this dimension)**:
- 8 client subaccounts in GHL with separate location IDs (vault isolation good)
- Skills mostly client-agnostic in `10_SKILLS/` · client-specific in `08_CLIENTI/<client>/`
- Bootstrap doc partial · `ONBOARDING.md` exists but not yet timed
- Single-machine binding remains (paths `/Users/nourmatine/` hardcoded)
- No formal scaffold for new client onboarding yet

**Bad (1/10 · prototype)**:
- One person's Mac · scripts in `~/Desktop/work/`
- API keys for 3 clients in same `.env` file
- No bootstrap procedure · undocumented in head
- Skills assume specific spreadsheet from client X · breaks on client Y

---

## How to improve from low score

| From | To | Action |
|------|-----|--------|
| 0-3 | 5 | Move hardcoded paths to env vars · separate credentials per-engagement · write bootstrap doc |
| 4-6 | 7 | Create scaffold/template for new project · isolate memory tiers per client · add handoff artifact format |
| 7-8 | 9 | Time a real redeployment · document edge cases · automate bootstrap (script) |
| 9 | 10 | Demonstrate workspace running on 2+ machines / engagements concurrently with no state leakage |

---

## Self-audit questions

- If you handed this workspace to another engineer tomorrow, how long until they could deploy it on a new client?
- Is there any memory or credential that, if leaked, would expose multiple clients at once?
- When you onboard a new client, do you start from a scaffold or from a blank folder?
- Is the bootstrap procedure documented · or living in your head?
