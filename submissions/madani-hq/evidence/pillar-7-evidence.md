# Pillar 7 · Credentials & Security · L3 Defined

## What the audit detected
The audit flagged 20 "plaintext secrets" and scored L3 / 70 (6/10 criteria). This pillar is the
clearest case in this submission where the keyword signal **understates** the real posture — but
there is also one genuine finding, reported honestly below.

## The 20 flagged hits, classified
- **18 false positives** · `sk-`-prefixed *slugs* matched by a naive regex — these are skill / task
  names, not secrets: `sk-initialization-pattern`, `sk-ghl-rispondere`, `sk-fireflies-monitor`,
  `sk-behavior-young-investors`, `sk-success-on-retrieval`, etc.
- **2 genuine** · a real Anthropic API key prefix embedded in an old session transcript under
  `cronologia/md-summary/2026-04/`. This is a real residue and the honest gap to L4.

## Substantiating artifacts
- `.claude/rules/credentials-policy.md` · HARD RULE: zero plaintext credentials; all secrets via `op://` 1Password vault resolved at runtime.
- `.envrc.template` · 23 services mapped to `op://Madani/...` references (committed); `.envrc` itself gitignored.
- `.claude/hooks/pre-tool-use.sh` · PreToolUse secret-guard that hard-blocks tool calls containing live third-party secret patterns (`sk_live_`, `EAAB`, `ghp_`).
- `.claude/rules/adversarial-robustness-policy.md` · threat model incl. credential exfiltration / confused-deputy; provenance discipline for tool output.

## Why L3 and not L4 (honest)
L3 is fair: the op:// migration is **incomplete** — the root API-MASTER.md and at least one old
cronologia transcript still contain real key material, and the Anthropic key prefix above should
be rotated. Closing that residue (rotate + purge from gitignored history) plus extending the
secret-guard regex to catch the Anthropic key family is the concrete L3→L4 path. The operational controls
(vault, guard hook, gitignore) are L4-grade; the data hygiene backlog is what holds the score.
