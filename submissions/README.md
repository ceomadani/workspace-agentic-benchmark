# Submissions · Workspace Agentic Benchmark Leaderboard

> **API-only flow.** No pull request required. Sign in once on `madani.agency/research`, run the audit on your own machine with any LLM, and the result lands on the public leaderboard in a single POST.

---

## Why submit

The leaderboard gains credibility with each documented audit. Your submission becomes:
- A reference example for other workspaces in the same domain / stack
- A data point for empirical weight derivation in v0.4+
- Public recognition of your workspace's maturity

The leaderboard is **not a competition** — it's a maturity map. A Grade B with documented improvement velocity is more valuable than a static A.

---

## Submission flow (single POST · no PR)

### 1. Sign in with GitHub

Visit https://www.madani.agency/research and sign in with your GitHub account. The site mints a `submit_token` derived from your GitHub numeric user id — it is bound to *your* account and cannot be used to submit on anyone else's behalf.

### 2. Get your credentials

After sign-in, open https://www.madani.agency/api/bench/whoami in another tab. You get back:

```json
{
  "ok": true,
  "github_user_id": "<your numeric GitHub id>",
  "github_username": "<your login>",
  "submit_token": "<32-char hex>",
  "submit_endpoint": "https://www.madani.agency/api/bench/submit"
}
```

Or — easier — copy the personalized prompt shown directly on the `/research` page. It already has all four values embedded.

### 3. Run the audit

On your workspace, with any LLM:

```bash
pip install --upgrade workspace-bench
workspace-bench audit /path/to/your/workspace --output ./out
workspace-bench score ./out --output ./out
```

You get `audit.json` + `score.json`. The audit tool emits sanitized output by default (no raw secret content · file paths only with pattern family + count). You're free to inspect both files before submitting — nothing private has to leave your machine if you don't want it to.

### 4. POST to the API

```bash
curl -X POST https://www.madani.agency/api/bench/submit \
  -H "Content-Type: application/json" \
  -d @- <<JSON
{
  "submit_token": "<your token>",
  "github_user_id": "<your numeric id>",
  "github_username": "<your login>",
  "repo": "<owner/repo>",
  "sha": "<commit sha · optional>",
  "audit": $(cat ./out/audit.json),
  "score": $(cat ./out/score.json)
}
JSON
```

Server-side it verifies the HMAC, sanitizes the payload (paths → `/Users/_/...`, client folders → anonymized, credentials → `[REDACTED-CREDENTIAL]`), and writes the entry to Vercel KV. The leaderboard updates within seconds.

### 5. (Optional) Drive the whole flow with an LLM

Paste the personalized prompt from `/research` into any chat-style LLM with shell + HTTP capabilities (Claude Code, Cursor, OpenAI CLI tools, etc.). The prompt is self-contained: it tells the agent to clone the workspace if needed, install workspace-bench, run audit + score, and POST the result with your token.

---

## Editing or removing your submission

Same `submit_token` authenticates an owner-only delete:

```bash
curl -X DELETE \
  -H "x-submit-token: <your token>" \
  "https://www.madani.agency/api/bench/submission?key=<username>:<repo_slug>"
```

This removes the leaderboard entry, the latest snapshot, and the user/repo membership. Historical point-in-time records (`wab:history:*:<ts>`) are intentionally retained so the audit trail isn't silently rewritten — if you also want those purged, open an issue on the benchmark repo.

To resubmit (e.g. after improving your harness), just POST again. The leaderboard tracks `best_composite` per user, plus full trend history per repo.

---

## Privacy & safety guarantees

- The server **never publishes `audit_full`** on the public submission endpoint — only score, pillar levels, cluster averages, and metadata. The audit JSON stays in KV for owner-only retrieval.
- Absolute home paths (`/Users/<x>/`, `/home/<x>/`) and known client folder names get anonymized server-side before storage.
- Plaintext credential patterns (`sk-ant-*`, `ghp_*`, `sk_live_*`, JWTs, AWS keys, GCP keys, Slack tokens) get redacted server-side as a defense-in-depth layer, on top of the audit tool's own sanitization.
- The leaderboard links to your GitHub *profile* (`github.com/<your-login>`), not to the audited repo — browsing the classifica does not expose other submitters' workspace structure.

---

## What about the old PR-based flow?

The previous version of this README described a PR-based, MLPerf-style review process (open a PR with `submissions/<slug>/metadata.yaml` + per-pillar evidence files). That flow has been retired in favor of the API. Reasons:

- An API submission scales to thousands of audits per day without manual review bandwidth.
- The privacy guarantees above can only be enforced server-side at write time — a PR-based flow would have leaked workspace internals in public git history before any reviewer saw them.
- The "evidence" the old flow required is already encoded in `audit.json`'s per-pillar signals (counts, paths, presence flags) — the LLM that ran the audit *is* the evidence.

If you have a workspace that genuinely needs human review before going on the leaderboard, open an issue on this repo and tag it `discuss`.

---

## Reference implementation

The submission endpoint, owner purge, sanitizer, and personalized prompt builder all live in [`ceomadani/madani-website`](https://github.com/ceomadani/madani-website) under `app/api/bench/*` and `auth.ts`. The audit tool itself (with the sanitization baseline) lives in this repo under `workspace_bench/`.

---

_submissions/README.md · v0.4 · API-only flow · 2026-05-25_
