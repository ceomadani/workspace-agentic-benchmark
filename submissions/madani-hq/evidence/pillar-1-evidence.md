# Pillar 1 · Context Hierarchy & Memory · L4 Optimizing

## What the audit detected
Explicit multi-tier memory architecture, a layered CLAUDE.md context hierarchy, and automated
memory admission/promotion — not knowledge living in the operator's head.

## Substantiating artifacts
- `~/.claude/CLAUDE.md` · L1 global operating system (identity, filesystem map, routing, 15 hard rules) — auto-loaded every turn.
- `CLAUDE.md` §12 · documents the 5-level context hierarchy (L1 global → L2 global rules → L3 project → L4 project rules → L5 local) with an explicit "never duplicate across levels" principle.
- `12_HARNESS/memory-engine/{semantic,episodic,procedural}/` · CoALA-style 4-tier memory engine (semantic / episodic / procedural split on disk).
- `11_TOOLS/a-mac-scoring.py` · A-MAC memory admission control (5-factor scoring) — decides what is worth persisting.
- `11_TOOLS/memory-promote.py` · daily cron promoting semantic → procedural memory.

## Operator commentary
The hierarchy is enforced, not aspirational: a stable-prefix injection (Manus KV-cache pattern)
re-asserts the procedural tier each session, and the A-MAC gate prevents low-signal memories from
polluting the store. L4 rather than L3 because admission + promotion are automated, not manual.
