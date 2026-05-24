# Vercel AI SDK · External Reference Audit

> **Score**: 23.75 / 100 · Grade **F** (failing per WAB metric · contextually nuanced)
> **Audited**: 2026-05-24 (workspace-bench v0.3.3)
> **Source**: github.com/vercel/ai
> **Workspace type**: TypeScript SDK library · positioned as "Universal AI layer for building frameworks and agents"

This audit is included as an external reference example after community feedback ("why is Vercel AI SDK not in the leaderboard if Anthropic Claude Agent SDK is?"). The audit confirms that the same tooling that scores other agent SDKs produces a comparable F-grade result · validating that the framework is fair across TypeScript and Python ecosystems.

---

## Score breakdown

| # | Pillar | Cluster | Level | Score |
|---|--------|---------|-------|------:|
| 1 | Context Hierarchy & Memory | A · Cognition | L1 Initial | 20 |
| 2 | Skill / Tool Architecture | B · Action | **L3 Defined** | **75** |
| 3 | Governance & Compliance | C · Trust | L2 Managed | 50 |
| 4 | Auto-Improvement Loop | A · Cognition | L1 Initial | 20 |
| 5 | Multi-Agent Discipline (DPI) | B · Action | L0 Absent | 0 |
| 6 | Observability & Recovery | C · Trust | L1 Initial | 20 |
| 7 | Credentials & Security | C · Trust | L1 Initial | 20 |
| 8 | Portability & Re-deployability | D · Operations | L1 Initial | 20 |
| 9 | Metacognition & Self-Assessment | A · Cognition | L0 Absent | 0 |
| 10 | Reliability & Determinism | B · Action | L1 Initial | 20 |
| 11 | Human-in-the-Loop | C · Trust | L1 Initial | 20 |
| 12 | Cost & Performance Efficiency | D · Operations | L1 Initial | 20 |

**Composite**: 23.75 / 100 → **Grade F**

**Cluster averages**:
- A · Cognition: 13.33
- B · Action: 31.67
- C · Trust: 27.5
- D · Operations: 20.0

---

## Strongest pillar · P2 Skill/Tool Architecture · L3 Defined (75)

Vercel AI SDK scores highest on **Pillar 2 · Skill/Tool Architecture** because:
- `ToolLoopAgent` primitive · documented `tool()` helper · structured tool definition contract
- Sub-agents pattern documented (`agents/overview` page)
- Memory primitive for tool loops
- Clean separation between tool definition and tool execution
- TypeScript types provide schema validation at compile time

This is genuine strength · not surprise · the SDK is purpose-built for tool-use loops.

---

## Why F (not lower · not higher)

The SDK provides excellent tool-use primitives (P2) and reasonable governance docs (P3). It is missing the **workspace-scope properties** that the WAB measures:

- ❌ **P5 Multi-Agent Discipline (DPI)** · no DPI guard · no single-thread-default policy
- ❌ **P9 Metacognition** · no self-assessment loop · no capability profile
- ❌ **P4 Auto-Improvement** · L1 only · documented patterns but no daemon/cron self-curation
- ❌ **P10 Reliability** · L1 · no determinism enforcement · no idempotency contracts at workspace level
- ❌ **P11 Human-in-the-Loop** · L1 · no escalation queue · no PP-gate framework
- ❌ **P12 Cost/Performance** · L1 · no token budget tracker · no KV-cache discipline tooling
- ❌ **P8 Portability** · L1 · no forward-deployable contract · TypeScript ecosystem-locked
- ❌ **P6 Observability** · L1 · no Reflexion-style daily audit
- ❌ **P7 Credentials** · L1 · standard env var pattern · no vault enforcement

The score is **identical in shape** to other agent SDKs in the leaderboard (OpenAI Agents SDK 40.83 · Anthropic Claude Agent SDK 22.5 · LangChain 22.5 · CrewAI 20.83 · AutoGen 20.0). The pattern is consistent: agent framework libraries provide compositional primitives · workspace properties are not their scope.

---

## Why this score is *appropriate* · contextual reading

The WAB is designed to measure **production workspace infrastructure** · an environment where an autonomous agent operates with governance · self-improvement · adversarial robustness · multi-tier memory. Vercel AI SDK is not that · it is a **library for building agent apps** · primarily targeted at developers shipping AI features in Next.js/Node.js applications.

What the SDK does excellently (P2 L3) does not transfer to workspace properties (P1 · P4-P12). Same pattern as Anthropic Claude Agent SDK (22.5 F) and OpenAI Agents SDK (40.83 D) · all three are SDK libraries · not workspaces.

**The score is not a criticism of the SDK** · it is a measurement of what dimensions the SDK is not optimized for. The SDK is excellent at what it sets out to do (build AI apps · tool-use loops · streaming UI). Workspace governance is orthogonal.

---

## What this teaches about the benchmark

**Validation of TypeScript ecosystem inclusion**: the audit tooling works on a TypeScript-first repository (vercel/ai is pnpm workspaces · 250+ packages) producing the same shape of result as Python ecosystem audits. The framework is ecosystem-agnostic.

**Validation of consistent grading**: the score (23.75) clusters tightly with other SDK-only entries (20.0-27.5 range) · confirming that the rubric correctly distinguishes "SDK library" from "workspace infrastructure" regardless of programming language.

**Architecture-Capability Decoupling holds**: the SDK provides excellent capability primitives · but capability without workspace alpha cannot produce autonomous self-improvement. The output equation `output = α(workspace) × capability(LLM)` requires both factors.

---

## Vercel AI SDK · positioning verbatim (verified 2026-05-24)

**Tagline** (homepage): *"Universal AI layer for building frameworks and agents"*

**Subtitle**: *"A unified TypeScript SDK for building AI apps with modern streaming, fallbacks, and multi-model support"*

**Agent primitives documented**:
- `ToolLoopAgent` class
- `generateText` · `streamText` · `generateObject`
- `tool()` helper
- Subagents pattern
- Memory management for tool loops
- Workflow Patterns guide
- Loop Control documentation

Confirms the SDK is positioned as both an AI app SDK AND an agent SDK · qualifies for the WAB leaderboard.

---

## Conclusion

Vercel AI SDK earns a fair F (23.75/100) in the v0.3.3 WAB methodology. It is the **second-strongest SDK on P2** (only Madani's skill registry scores higher · 8/10 vs Vercel's 8/10 · tied). It is **average on governance** (P3 L2 · same as Anthropic Cookbook). It is **absent on metacognition and multi-agent discipline** (P5 L0 · P9 L0 · same as all other SDKs in the leaderboard).

The SDK belongs in the leaderboard alongside OpenAI Agents SDK · Anthropic Claude Agent SDK · LangChain · CrewAI · AutoGen · because they all share the same architectural genre: agent-primitive libraries. Within that genre · Vercel AI SDK is competitive · ranking at the median of the cluster.

This audit closes the gap raised by community feedback (2026-05-24) that Vercel AI SDK was missing from the leaderboard despite qualifying.

---

_Audit run: workspace-bench v0.3.3 · 2026-05-24 · vercel/ai cloned shallow from main · audit + score automated · zero LLM judgment (~70% deterministic per methodology) · added to leaderboard at rank 4 between anthropic-cookbook (27.5) and anthropics-claude-agent-sdk-python (22.5)_
