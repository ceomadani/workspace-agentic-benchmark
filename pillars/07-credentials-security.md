# Pillar 7 · Credentials & Security

> **Cluster C · Trust**
> **First principle**: *Zero plaintext credentials. Ever. Including "placeholder" patterns.*
> **Weight**: 1/12 (equal-weighted baseline · v0.3 default)

---

## Why this pillar exists

Plaintext credentials in agent workspaces are the #1 production security incident. Agents have read access to everything by default · one leaked workspace = full credential dump. OWASP top 10 lists A07 (Identification and Authentication Failures) as a top concern · 60%+ of agent-related security incidents involve credentials checked into repos.

---

## Scoring criteria · 10 binary checks

1. **[1.0]** Zero plaintext credentials in repo · audited (grep for common patterns: `sk-`, `ghp_`, `Bearer `, `api_key:`, `password:`).
2. **[1.0]** Secret manager integrated (1Password CLI · HashiCorp Vault · AWS Secrets Manager · Doppler).
3. **[1.0]** Runtime resolution via env (direnv · op:// references · vault read).
4. **[1.0]** `.env` files gitignored · not committed.
5. **[1.0]** Approval gate for external actions (no auto-call to APIs that send messages to humans).
6. **[1.0]** Audit log of credential access · who/when/what.
7. **[1.0]** Secret rotation documented · cadence + procedure.
8. **[1.0]** No credentials in commit history (git filter-branch / BFG used if leak found).
9. **[1.0]** No credentials in URL query strings (logged in plaintext).
10. **[1.0]** Per-environment separation (dev / staging / prod credentials distinct).

---

## L0-L4 Maturity Rubric

| Level | Score | Profile |
|-------|------:|---------|
| **L0 Absent** | 0 | Credentials in markdown · scripts · commit messages · no rotation · plaintext everywhere. |
| **L1 Initial** | 20 | Credentials in `.env` files · `.env` not gitignored or recently leaked · no vault. |
| **L2 Managed** | 50 | Mix of vault + plaintext · `.env` gitignored · old leaks may remain in git history · partial rotation. |
| **L3 Defined** | 75 | Zero plaintext in current repo · secret manager integrated (1Password / Vault / Doppler / AWS SM) · runtime resolution via `op://` or equivalent · `.envrc.template` checked in · pre-commit hook blocks plaintext patterns. |
| **L4 Optimizing** | 100 | All OWASP LLM Top 10 2025 vectors mitigated (LLM02 Sensitive Information Disclosure · LLM06 Excessive Agency · LLM07 System Prompt Leakage · LLM09 Misinformation · LLM10 Unbounded Consumption) · rotation cadence enforced (quarterly) · per-env separation tested · audit log reviewed monthly. |

---

## Evidence sources

- **OWASP LLM Top 10** · A07 Identification and Authentication Failures.
- **Production incident pattern** · 60%+ agent security incidents from leaked credentials.
- **1Password CLI documentation** · `op://` runtime resolution pattern.
- **HashiCorp Vault** · enterprise-grade dynamic secrets.
- **Madani HR13** · zero plaintext · 23 services in op://Madani vault.

---

## Anti-patterns

- ❌ `.env` committed · even once · history is forever (use git filter-branch/BFG)
- ❌ API keys in markdown docs (`## My key: sk-...`)
- ❌ Hardcoded in scripts (`const KEY = "sk-..."`)
- ❌ Token in URL (`https://api.example.com?key=...` · logged in plaintext)
- ❌ Credentials in commit message
- ❌ Credentials in error log / stack trace
- ❌ "Placeholder" patterns that look real (`sk-ant-...`) · grep can't distinguish
- ❌ Single set of credentials for dev + staging + prod

---

## Profiles

**Production-grade (9-10)**:
- `.envrc.template` checked in · `.envrc` resolved at runtime via secret manager CLI (1Password / Vault / Doppler / AWS SM)
- All services mapped to runtime references (`op://...` · `vault://...` · `aws-sm://...`)
- Zero plaintext in repo (audited via grep + git-history scan with TruffleHog / gitleaks)
- direnv hook auto-loads on entering workspace directory
- Plaintext-prohibition rule in constitution · enforced via pre-commit hook
- Audit trail of credential access (vault access log enabled)

**Prototype-stage (0-2)**:
- `.env` committed in initial commit
- API keys in markdown docs (e.g., `notes.md`)
- Single key used across personal dev + production
- Tokens in URL query strings (`?key=...` · logged in plaintext)

---

## How to improve from low score

| From | To | Action |
|------|-----|--------|
| 0-3 | 5 | Move credentials to `.env` · gitignore · scan history with truffleHog/gitleaks · rotate any leaked |
| 4-6 | 7 | Integrate secret manager (1Password / Vault / Doppler) · resolve at runtime |
| 7-8 | 9 | Add approval gates for external action APIs · separate per-environment credentials |
| 9 | 10 | Audit access log · document rotation cadence · pre-commit hook to block plaintext patterns |

---

## Self-audit questions

- Run `grep -rE "sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|Bearer [a-zA-Z0-9]{30,}"` over the repo · what comes back?
- If a contractor gets read access to the repo tomorrow, do they get your credentials?
- When was the last credential rotation · what was the procedure?
- If an API key leaks, what's your incident response time?
