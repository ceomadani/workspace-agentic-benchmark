# Extension 09 · Resilience under Partial Failure

> The workspace must keep working when individual components fail · cron job dies · API down · file missing.

---

## Principle

A workspace is **resilient** when single-point failures don't cascade. A daemon crashes · the agent notices · keeps operating with degraded but coherent behavior · alerts surface for recovery.

The opposite is **brittle**: one cron job dies silently · its outputs go stale · downstream tools consume stale data · agent makes wrong decisions · weeks pass before anyone notices.

---

## Concrete failure modes (universal patterns)

| Mode | Generic example |
|------|-----------------|
| Cron / scheduler job silently dead | A daily job exits non-zero · no alerts wired · downstream artifacts grow stale · discovered manually when user notices output missing |
| Scheduler config orphaned by refactor | A folder rename / repo restructure leaves the launchd/cron/systemd config pointing at the old path · job fails on every invocation |
| Hook silently exits 0 with wrong schema | A PreToolUse hook returns the previous protocol's JSON shape · runtime ignores it · the intended safety check is bypassed unnoticed |
| Daemon supervisor up · workers empty | The supervisor process is alive (PID exists) but its worker pool is empty · status JSON shows zero active workers despite "running" state |

---

## Requirements

| Requirement | Mechanism |
|-------------|-----------|
| **Liveness watchdog** | A meta-job that scans all critical scheduled jobs (e.g., `launchctl list` · `systemctl --user list-units` · `crontab -l`) · checks recent exit codes · alerts on persistent failure |
| **Exit code surveillance** | Stop hook captures session outcome · append-only state file · trend visible over time |
| **Health endpoints** | Each long-running daemon exposes status (last_run · last_success · next_run) readable without invoking it |
| **Graceful degradation** | If a tool is down, the agent says so explicitly rather than producing garbage |
| **Recovery runbook** | Each critical component has documented "if X dies, do Y to recover" — not in operator's head |
| **Replay harness** | Failed tool calls can be replayed deterministically once root cause is fixed |
| **Backoff + retry** | External calls have explicit retry strategy · not infinite loop · not zero-retry |

---

## Measurement

- `mean_time_to_detect_failure` (MTTD · target ≤ 1 hour at L4)
- `mean_time_to_recover` (MTTR · target ≤ 1 day at L4)
- `% of critical components with health endpoint` (target ≥ 0.9 at L4)
- `% of failures that triggered a learning entry in lessons.md` (target ≥ 0.8 at L4 · double-loop)

---

## Anti-patterns

- ❌ Silent failure modes (exit code 0 even on functional failure).
- ❌ No watchdog · only humans notice problems.
- ❌ Single point of failure (e.g., one cron job whose death stops the daily report system).
- ❌ Recovery instructions in operator's head only · bus factor 1.

---

_Extension 09 · iter-2 · 2026-05-20 · derived from MAST 14 failure modes (Patil et al. 2025) + live audit data_
