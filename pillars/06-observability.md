# Pillar 6 · Observability & Recovery

> **First principle**: *Failure is the default. Detection must be automatic and fast.*
> **Max score**: 10 points.

---

## Why this pillar exists

Agents fail silently. Without centralized logs, liveness checks, and drift detectors, you discover failures only when the user notices. MTTD (mean time to detect) is the key infrastructure metric. Production reliability research shows MTTD reduction correlates with user trust more strongly than MTBF (mean time between failures).

---

## Scoring criteria · 10 binary checks

1. **[1.0]** Centralized log directory · all cron + automation outputs in one place.
2. **[1.0]** Liveness watchdog · cron monitors for stuck / zombie tasks.
3. **[1.0]** Aggregate health report · daily summary across all systems.
4. **[1.0]** Drift detector · alerts when files / patterns / configs drift from expected state.
5. **[1.0]** Explicit task lifecycle state machine (e.g., 6-state: inbox → planning → active → review → closing → result).
6. **[1.0]** Stuck-task detection · tasks that haven't transitioned in N days flagged.
7. **[1.0]** Cron success rate tracked · failures alerted.
8. **[1.0]** Error logs separated from output logs (`*.err.log` vs `*.out.log`).
9. **[1.0]** Log rotation policy · no infinite growth.
10. **[1.0]** Recovery procedure documented · what to do when a cron fails.

---

## Scoring rubric

| Score | Profile |
|-------|---------|
| **9-10** | Centralized logs · liveness watchdog · aggregate report · drift detector · 6-state lifecycle · rotation · documented recovery |
| **7-8** | Logs centralized · most checks present · ad-hoc recovery |
| **5-6** | Scattered logs · partial health visibility |
| **3-4** | Logs exist but nobody reads them · no health summary |
| **0-2** | No logs · "we'll notice if it breaks" |

---

## Evidence sources

- **Anthropic Effective Harnesses** · aggregate-report pattern for health visibility.
- **M08 6-state lifecycle (Madani iter-30+)** · explicit state machine catches zombie tasks.
- **Google SRE book** · MTTD reduction > MTBF improvement for user trust.
- **Distributed systems observability** · USE (Utilization, Saturation, Errors) + RED (Rate, Errors, Duration) methods.

---

## Anti-patterns

- ❌ Scattered logs · each cron writes to its own random location
- ❌ No health summary · you check 7 different log files to know status
- ❌ No zombie detector · task gets stuck "in progress" for 3 weeks
- ❌ Stdout and stderr mixed · can't distinguish noise from errors
- ❌ Logs grow infinitely · eventually fill disk
- ❌ Recovery procedure exists in someone's head only

---

## Profiles

**Production-grade (8-10)**:
- All cron logs in a centralized `_logs/` directory
- Liveness watchdog hourly (scan for stuck / zombie tasks)
- Aggregate health report daily (e.g., 09:00 local · summary across all systems)
- Explicit task lifecycle state machine (e.g., 6-state: inbox → planning → active → review → closing → result)
- `*.out.log` + `*.err.log` separated for noise vs error distinction
- Recovery procedures documented in templates / runbooks

**Prototype-stage (0-2)**:
- One script writing to stdout · nothing captured
- No cron · everything on-demand
- When something fails, user finds out via complaint from downstream consumer
- No state machine · tasks stuck in undefined limbo

---

## How to improve from low score

| From | To | Action |
|------|-----|--------|
| 0-3 | 5 | Create central log dir · pipe all automation to it · separate `.out` and `.err` |
| 4-6 | 7 | Add liveness watchdog · daily aggregate report · explicit task lifecycle states |
| 7-8 | 9 | Add drift detector · stuck-task detection (N days threshold) · log rotation |
| 9 | 10 | Document recovery procedures · measure MTTD on synthetic failures · alert on cron failure |

---

## Self-audit questions

- If a cron job fails tonight, when will you find out · how?
- What's your mean time to detect a stuck task?
- Where do you check first when something feels "off" in the workspace?
- If disk fills up from logs, what happens?
