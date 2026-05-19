# Pillar 9 · Metacognition & Self-Assessment

> **First principle**: *An agent must know what it doesn't know · before acting · not after failing.*
> **Max score**: 10 points.

---

## Why this pillar exists

Most agents execute every task with implicit confidence, then fail silently or visibly. **Prospective metacognition** — assessing competence *before* execution — is the difference between a system that knows its boundaries and one that produces confident garbage on tasks outside its expertise.

This pillar is grounded in the **MetaCogAgent** paper (arXiv 2605.17292v1 · Wang/Shu · May 2026), which demonstrates:
- **82.4% accuracy** on MetaCog-Eval (700 tasks · 5 cognitive dimensions) · +8.7% over Majority-Vote
- **-34% API calls** vs Majority-Vote · -5% vs AutoGen
- **ECE 0.087** (well-calibrated) vs **0.194** for Single-Agent (overconfident)
- **+7% Hard-task robustness** · -11.5% drop vs -18.5% Single-Agent

The mechanism is a **Metacognitive Unit (MCU)** per agent with three components:
1. **Self-Assessment**: verbalized confidence + capability profile lookup → composite score
2. **Adaptive Delegation**: `c < θ` → broadcast to peers → route to argmax confidence
3. **Capability Boundary Learning**: EMA update `p^(t+1) = p^(t) + α(r - p^(t))` from outcome

---

## Why pair this with Pillar 5 (Multi-Agent DPI)

Stanford 2604.02460 says "default single-thread unless evidence of context degradation". The "evidence" was historically vague. **MetaCog provides operational evidence**: `c < θ` is the trigger. This pillar makes Pillar 5's third condition measurable.

---

## Scoring criteria · 10 binary checks

1. **[1.0]** Pre-task self-assessment exists · documented procedure to assess confidence before significant tasks.
2. **[1.0]** Verbalized confidence mechanism · tool/prompt that elicits confidence rating (e.g., Likert 0-100 across multiple axes).
3. **[1.0]** Capability profile maintained · per-dimension competence vector (reasoning · retrieval · coding · etc.) with explicit values.
4. **[1.0]** Composite confidence formula · combines verbalized + profile (`c = λ·c^v + (1-λ)·c^p` or equivalent).
5. **[1.0]** Conflict detection (2nd-order) · monitors `δ = |c^v - c^p|` · flags epistemic uncertainty about uncertainty.
6. **[1.0]** Decision gate · explicit threshold (e.g., `θ=0.5`) that determines execute vs delegate vs escalate.
7. **[1.0]** Post-task profile update · cybernetic loop · profile adjusts from outcomes (EMA or equivalent).
8. **[1.0]** Calibration tracked · workspace measures Expected Calibration Error (ECE) or equivalent over time.
9. **[1.0]** Anti-pattern documentation · explicit list of misuse cases (e.g., "verbalized-only · profile-only · recursive metacog").
10. **[1.0]** Integration with delegation policy · MetaCog signal explicitly feeds the multi-agent DPI gate.

---

## Scoring rubric

| Score | Profile |
|-------|---------|
| **9-10** | MCU runner · capability profile · composite formula · conflict detection · ECE tracked · EMA update · DPI integration · documented anti-patterns |
| **7-8** | Self-assessment + profile + composite + decision gate · partial conflict/calibration tracking |
| **5-6** | Verbalized confidence implemented · no profile · no cybernetic loop |
| **3-4** | Ad-hoc "I'm not sure about this" prompts · no measurement · no profile |
| **0-2** | Agent acts on every request with implicit full confidence · no metacognition layer |

---

## Evidence sources

- **MetaCogAgent (arXiv 2605.17292v1)** · Wang/Shu · primary reference. 82.4% acc · ECE 0.087.
- **Kadavath et al. (arXiv 2207.05221)** · "Language Models (Mostly) Know What They Know" · verbalized confidence calibration.
- **Xiong et al. (arXiv 2306.13063)** · confidence elicitation strategies in LLMs.
- **Guo et al. (ICML 2017)** · Expected Calibration Error metric.
- **Flavell (1979)** · metacognition framework (cognitive science origin).
- **MAST (arXiv 2503.13657)** · 14 failure modes in multi-agent · self-assessment gap documented.

---

## Anti-patterns

- ❌ **Verbalized-only** · poorly calibrated · LLMs "know what they know" but overestimate confidence consistently.
- ❌ **Profile-only** · profile becomes stale · new task types not reflected · prompt-driven shifts missed.
- ❌ **Delegation without cross-evaluation** · routing to peer without peer-confidence check → Skill-Fixed baseline 70.2% acc (per paper).
- ❌ **Recursive metacognition** · sub-agent runs its own MCU → stack overflow potential · paper restricts N=3 agents.
- ❌ **Metacognition on every turn** · over-engineering · LLM-cost × turns. Only PRE-significant tasks (long-horizon · high-stakes · cross-domain · low-profile dimension).
- ❌ **No post-task update** · profile becomes stationary · cybernetic loop broken · no learning.
- ❌ **Ad-hoc threshold tuning** · `θ` must be documented decision · not silently modified.

---

## Examples

**Production-grade (9-10)**:
- MCU tool (e.g., `metacog.py assess "<task>"`) pre-significant tasks
- Capability profile vector P = [p_reasoning · p_retrieval · p_coding · ...] in procedural memory tier
- Composite `c = λ·c^v + (1-λ)·c^p` with documented λ (typically 0.6)
- Conflict detection `δ > 0.3` triggers threshold tightening
- EMA update post-task `α=0.1` · 10-task memory horizon
- ECE measured monthly · target ≤ 0.10
- Anti-pattern list documented in policy file
- DPI policy explicitly cites MetaCog `c < θ` as 3rd-condition evidence

**Bad (1/10 · prototype)**:
- Agent attempts every task
- Confidence never measured
- Failures noticed only when user complains
- No calibration · no profile · no update mechanism

---

## How to improve from low score

| From | To | Action |
|------|-----|--------|
| 0-2 | 4 | Add a "self-assess" prompt template for high-stakes tasks (verbalized 3-axis: expertise / approach / knowledge). Manual invocation initially. |
| 3-4 | 6 | Build a tool that runs the prompt (cheaper model like Sonnet/Haiku) · output structured JSON · skip on trivial tasks. |
| 5-6 | 8 | Add capability profile per-dimension (start with 5-6 dimensions · bootstrap with reasonable priors). Add composite formula. Add conflict detection. |
| 7-8 | 9 | Implement EMA post-task update from outcome signal (e.g., Reflexion-extracted correctness). Track ECE. |
| 9 | 10 | Integrate with DPI multi-agent gate · `c < θ` becomes the operational delegation trigger. Document threshold rationale. |

---

## Self-audit questions

- When the agent attempted a task outside its competence in the last 30 days, what triggered the failure detection — internal signal or user complaint?
- Does the workspace measure calibration (ECE) or only accuracy?
- If you asked the agent right now "how confident are you about Python type-system edge cases vs distributed systems consensus vs music theory" · would you get 3 different calibrated numbers or 3 similar overconfident estimates?
- When a task lies outside any single skill profile (cross-domain), does the workspace have an explicit signal to escalate vs proceed?
- Is the capability profile updated by outcomes · or is it a static document written once?

---

## Relation to Pillar 5 (Multi-Agent DPI)

Pillar 5 is necessary but insufficient. It says "default single-thread · multi-agent only with evidence". MetaCog operationalizes that evidence:

```
DPI condition 3 ("evidence of need") ⇔ MetaCog (c < θ)
```

A workspace scoring high on Pillar 5 but low on Pillar 9 has a policy without measurement. A workspace high on both has a measurable, evidence-based delegation system.

---

_Pillar 9 v0.1 · 2026-05-19 · pattern source MetaCogAgent arXiv 2605.17292v1 · prospective metacognition · novel addition to public agentic workspace benchmarks_
