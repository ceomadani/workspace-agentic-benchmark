"""Pillar metadata · clusters · levels · centralized definitions."""

from __future__ import annotations
from typing import NamedTuple


LEVEL_SCORES = {0: 0, 1: 20, 2: 50, 3: 70, 4: 95}
# v0.4 anti-bias soft cap: L4 max=95 (reserves 5 pts for runtime-enforcement
# evidence in v0.5) · L3 lowered to 70 for proportional ladder distance.
# Rationale: pure documentation-based scoring saturates too easily for
# workspaces that authored the rubric (genesis bias) · runtime probing tests
# (v0.5) will fill the remaining 5 pts only when policies are demonstrably
# enforced. Disclosure in README "Known biases · validity threats".
LEVEL_NAMES = {
    0: "L0 Absent",
    1: "L1 Initial",
    2: "L2 Managed",
    3: "L3 Defined",
    4: "L4 Optimizing",
}
LEVEL_SHORT = {0: "L0", 1: "L1", 2: "L2", 3: "L3", 4: "L4"}
LEVEL_DESCRIPTIONS = {
    0: "Pillar doesn't exist in workspace",
    1: "Ad-hoc · undocumented · operator's head only",
    2: "Documented · manually executed",
    3: "Enforced via tools/hooks · automated",
    4: "Auto-improves · measured · cybernetic feedback loop",
}


GRADE_THRESHOLDS = [
    ("A", 85, "Production-grade · forward-deployable · FDE-engagement ready"),
    ("B", 70, "Solid · 1-2 pillars need hardening before scale"),
    ("C", 50, "Early-stage · multiple gaps · workspace work needed alongside agent work"),
    ("D", 30, "Prototype · not production-ready · infrastructure-first work required"),
    ("F", 0, "Failing · workspace not fit for purpose"),
]


def grade(total: float) -> str:
    for letter, threshold, _ in GRADE_THRESHOLDS:
        if total >= threshold:
            return letter
    return "F"


def grade_description(g: str) -> str:
    for letter, _, desc in GRADE_THRESHOLDS:
        if letter == g:
            return desc
    return ""


class Pillar(NamedTuple):
    n: int
    key: str
    title: str
    cluster: str
    cluster_letter: str
    principle: str
    is_new_v03: bool


PILLARS: list[Pillar] = [
    Pillar(1, "1_context_memory", "Context Hierarchy & Memory", "Cognition", "A",
           "Information flows into context only when needed, only the parts needed.", False),
    Pillar(2, "2_skill_tool", "Skill / Tool Architecture", "Action", "B",
           "A skill is a contract with the agent. Contracts must be discoverable, fresh, and minimal.", False),
    Pillar(3, "3_governance", "Governance & Compliance", "Trust", "C",
           "Every irreversible action must pass an explicit gate. No silent execution.", False),
    Pillar(4, "4_auto_improvement", "Auto-Improvement Loop", "Cognition", "A",
           "The workspace learns from its own session history · automatically · on a schedule.", False),
    Pillar(5, "5_multi_agent_dpi", "Multi-Agent Discipline (DPI)", "Action", "B",
           "Default to single-thread. Multi-agent is an exception with explicit justification.", False),
    Pillar(6, "6_observability", "Observability & Recovery", "Trust", "C",
           "Failure is the default. Detection must be automatic and fast.", False),
    Pillar(7, "7_credentials_security", "Credentials & Security", "Trust", "C",
           "Zero plaintext credentials. Ever. Including placeholder patterns.", False),
    Pillar(8, "8_portability", "Portability & Re-deployability", "Operations", "D",
           "Re-deployable on new engagement in days, not months. FDE-grade.", False),
    Pillar(9, "9_metacognition", "Metacognition & Self-Assessment", "Cognition", "A",
           "An agent must know what it doesn't know · before acting · not after failing.", False),
    Pillar(10, "10_reliability", "Reliability & Determinism", "Action", "B",
           "An agent that succeeds once in eight tries is not a system — it is a coin flip.", True),
    Pillar(11, "11_human_in_the_loop", "Human-in-the-Loop", "Trust", "C",
           "The most consequential decisions must pass through a human gate.", True),
    Pillar(12, "12_cost_performance", "Cost & Performance Efficiency", "Operations", "D",
           "Token economics decide deployment viability · harness, not model.", True),
]


CLUSTERS = [
    ("A", "Cognition", "the agent's mind · memory · learning · self-assessment"),
    ("B", "Action", "how it executes · skills · multi-agent discipline · reliability"),
    ("C", "Trust", "safety and governance · gates · observability · security · human-in-the-loop"),
    ("D", "Operations", "production readiness · portability · cost economics"),
]


def pillars_by_cluster(letter: str) -> list[Pillar]:
    return [p for p in PILLARS if p.cluster_letter == letter]


def pillar_by_key(key: str) -> Pillar | None:
    for p in PILLARS:
        if p.key == key:
            return p
    return None


def equal_weights() -> dict[str, float]:
    return {p.key: 1.0 / len(PILLARS) for p in PILLARS}
