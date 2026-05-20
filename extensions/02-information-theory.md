# Extension 02 · Information Theory · Signal-to-Noise

> Operationalizes the `quality_files` term of α via Shannon entropy and signal-to-noise ratio applied to workspace content.

---

## Principle

Workspace files have an information content (bits of unique signal) and an information cost (bytes of total content). The ratio is the file's effective density. A workspace's total signal is the sum, but its **effective** signal — what the agent can use — is gated by retrieval (Extension 10).

```
file_SNR = signal_bytes / total_bytes
workspace_signal_total = Σ (file_SNR × file_size × file_retrieval_probability)
```

A file with SNR 0.9 that's never retrieved contributes near zero. A file with SNR 0.4 that's retrieved in every session matters more.

---

## What is signal vs noise

| Signal | Noise |
|--------|-------|
| Concrete facts · numbers · dates · paths | Hedge language · "as noted above" · "it's worth mentioning" |
| Canonical rule + reason + how-to-apply | Discussion of why the rule was considered · what alternatives existed |
| Actionable pointers (file paths · IDs · API endpoints) | Re-explanations of what's covered elsewhere |
| Examples that differ in meaningful structure | 3 examples that all teach the same point |
| Decisions + rationale | History of how the decision was reached (belongs in changelog, not main doc) |

---

## Measurement

- `compression_ratio` = `gzipped_size / original_size`. Higher ratio = more repetition/filler. Target ≤ 0.35 across workspace.
- `unique_n-gram_density` = fraction of 5-grams that are unique to a file vs duplicated across the workspace. Target ≥ 0.6.
- `human_audit_signal_score` = sample 10 files · score 0-1 by "useful content / total content" · target ≥ 0.7.

---

## Anti-patterns blocked

- ❌ Files that recap context from other files (duplication = noise).
- ❌ "Comprehensive" docs that explain everything possible · agent context cost ≫ retrieval benefit.
- ❌ Stylistic prose where structured data would suffice (YAML > paragraph).

---

## Maturity

| L0 | No SNR awareness · files grow unbounded |
| L1 | Periodic manual reviews · ad-hoc pruning |
| L2 | Documented standards (e.g., "one fact one place") · enforced manually |
| L3 | Linter checks (duplication detector · n-gram analysis) · enforced via hook |
| L4 | Auto-compression cron · SNR tracked over time · regression alerts |

---

_Extension 02 · iter-2 · 2026-05-20_
