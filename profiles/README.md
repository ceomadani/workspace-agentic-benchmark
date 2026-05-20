# Profiles · contextual weighting

> Three reference profiles that weight pillars + require extensions based on use case. A single workspace scores differently under different profiles — by design.

---

## Why profiles

A solo-operator workspace shouldn't be penalized for lacking team-deployment portability. A production multi-tenant platform shouldn't get a free pass on compliance just because the operator decided "we'll add that later."

Profiles encode the realistic priority ordering for distinct deployment shapes:

| Profile | When to use | Critical clusters |
|---------|-------------|--------------------|
| [solo-operator-private-repo](solo-operator-private-repo.yml) | Single dev · private repo · subscription auth · personal workspace | Cognition + Action |
| [team-saas-production](team-saas-production.yml) | 3+ devs · production users · API token costs · multi-env | Trust + Operations |
| [enterprise-multi-tenant](enterprise-multi-tenant.yml) | 10+ devs · multi-tenant · compliance | All clusters · max Trust |

---

## How to use

```bash
# Specify profile at audit time
python3 -m workspace_bench run /path/to/workspace --profile solo-operator-private-repo

# Or in workspace-bench.yml config:
profile: solo-operator-private-repo
```

The composite score is computed with the profile's weights. The audit report calls out:
- Pillars where you exceed the profile threshold (strengths)
- Pillars where you fall short (priority actions)
- Required extensions missing (architectural gaps for this use case)

---

## Anti-gaming

Profile selection is **declarative + verified**: declaring `team-saas-production` requires producing artifacts consistent with team operation (multi-author git history · documented onboarding · staging/prod env separation). Workspaces that select a profile they don't actually inhabit get flagged in the audit output.

---

## Adding new profiles

Profiles are YAML. Add a new file to this folder. Required fields:
- `profile_id` · slug
- `description` · paragraph
- `weights` · all 12 pillars with float weight (1.0 = standard · 0.0 = ignore · 2.0 = doubled)
- `extensions_required` · list of extension slugs that must be present
- `extensions_optional` · list of extension slugs that are nice-to-have
- `notes` · paragraph explaining tradeoffs

Submit via PR with a real-world use case justification.

---

_Profiles README · iter-2 · 2026-05-20_
