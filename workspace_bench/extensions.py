"""Iter-2 · extension presence detection.

Each of the 11 extensions has a deterministic check that returns:
  status: "present" | "partial" | "absent"
  evidence: list of file paths or signals supporting the verdict

Extensions are cross-cutting first principles · binary/ternary signals rather
than L0-L4 because their nature resists fine-grained maturity scoring.
"""

from __future__ import annotations
import re
from pathlib import Path

# ─── Extension catalog ──────────────────────────────────────────────

EXTENSIONS = [
    {
        "id": "01-architecture-capability-decoupling",
        "title": "Architecture-Capability Decoupling",
        "cluster": "root-principle",
    },
    {
        "id": "02-information-theory",
        "title": "Information Theory · Signal-to-Noise",
        "cluster": "cross-cutting",
    },
    {
        "id": "03-causal-reasoning",
        "title": "Causal Reasoning Support",
        "cluster": "cross-cutting",
    },
    {
        "id": "04-adversarial-robustness",
        "title": "Adversarial Robustness",
        "cluster": "cross-cutting",
    },
    {
        "id": "05-compositionality",
        "title": "Compositionality",
        "cluster": "cross-cutting",
    },
    {
        "id": "06-temporal-coherence",
        "title": "Temporal Coherence",
        "cluster": "cross-cutting",
    },
    {
        "id": "07-embodied-awareness",
        "title": "Embodied / Situational Awareness",
        "cluster": "cross-cutting",
    },
    {
        "id": "08-knowledge-representation",
        "title": "Knowledge Representation Choice",
        "cluster": "cross-cutting",
    },
    {
        "id": "09-resilience-partial-failure",
        "title": "Resilience under Partial Failure",
        "cluster": "cross-cutting",
    },
    {
        "id": "10-index-density",
        "title": "Index Density & Semantic Coverage",
        "cluster": "cross-cutting",
    },
    {
        "id": "11-meta-measurement",
        "title": "Meta-Measurement",
        "cluster": "recursive",
    },
]


# ─── Per-extension detectors ──────────────────────────────────────────

def _safe_rglob(path: Path, pattern: str, max_results: int = 500) -> list:
    """Glob with cap · skip node_modules/.git/_archive/_legacy/_DEPRECATED."""
    SKIP_DIRS = {".git", "node_modules", "_archive", "_legacy", ".venv", "venv", "__pycache__", ".next", "dist", "build"}
    results = []
    try:
        for p in path.rglob(pattern):
            if any(part in SKIP_DIRS or part.startswith("_DEPRECATED") for part in p.parts):
                continue
            results.append(p)
            if len(results) >= max_results:
                break
    except Exception:
        pass
    return results


def _detect_01_architecture_capability(ws: Path) -> dict:
    """Architecture-Capability Decoupling · root principle awareness.

    Present if: workspace shows awareness that good architecture amplifies weak model.
    Heuristic: search for terms like "architecture × capability", "α(workspace)",
    "workspace > agent", "harness > model", or formal alpha formula in any doc.
    """
    patterns = [
        r"α\s*\(",  # alpha formula
        r"architecture.{0,30}capability",
        r"workspace\s*>\s*(agent|model)",
        r"harness\s*>\s*model",
        r"weak\s+model.{0,50}great\s+workspace",
        r"effective[- ]harness",
    ]
    matches = []
    for md in _safe_rglob(ws, "*.md", 200):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")[:50000]
            for pat in patterns:
                if re.search(pat, text, re.IGNORECASE):
                    matches.append(str(md.relative_to(ws)))
                    break
        except Exception:
            continue
        if len(matches) >= 5:
            break
    status = "present" if len(matches) >= 2 else ("partial" if matches else "absent")
    return {"status": status, "evidence": matches[:5]}


def _detect_02_information_theory(ws: Path) -> dict:
    """Info theory awareness · SNR · entropy · density metrics in workspace."""
    patterns = [r"signal[- ]to[- ]noise", r"shannon", r"entropy", r"α\s*=", r"information\s+density", r"snr"]
    matches = []
    for md in _safe_rglob(ws, "*.md", 200):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")[:30000]
            if any(re.search(p, text, re.IGNORECASE) for p in patterns):
                matches.append(str(md.relative_to(ws)))
        except Exception:
            continue
        if len(matches) >= 5:
            break
    status = "present" if len(matches) >= 3 else ("partial" if matches else "absent")
    return {"status": status, "evidence": matches[:5]}


def _detect_03_causal_reasoning(ws: Path) -> dict:
    """Causal reasoning support · rules have explicit Why · post-mortem with chain."""
    rules_with_why = 0
    total_rules = 0
    for md in _safe_rglob(ws, "*.md", 100):
        path_str = str(md).lower()
        if any(x in path_str for x in ["rules/", "rule-", "policy", "constitution"]):
            total_rules += 1
            try:
                text = md.read_text(encoding="utf-8", errors="ignore")[:20000]
                if re.search(r"##?\s*Why\b|\*\*Why\*\*|\*\*Perché\*\*|## Reason", text, re.IGNORECASE):
                    rules_with_why += 1
            except Exception:
                continue
    lessons_files = _safe_rglob(ws, "lessons*.md", 20) + _safe_rglob(ws, "*post-mortem*", 20)
    ratio = rules_with_why / total_rules if total_rules > 0 else 0
    status = "present" if (ratio >= 0.5 and lessons_files) else ("partial" if (rules_with_why > 0 or lessons_files) else "absent")
    return {
        "status": status,
        "evidence": {
            "rules_with_why": rules_with_why,
            "total_rules": total_rules,
            "lessons_files_count": len(lessons_files),
        },
    }


def _detect_04_adversarial_robustness(ws: Path) -> dict:
    """Adversarial robustness · secret guard hook · provenance tagging · HITL gates."""
    hook_files = _safe_rglob(ws, "pre-tool-use.sh", 5) + _safe_rglob(ws, "*hook*", 30)
    has_secret_guard = False
    has_hitl_doc = False
    for f in hook_files[:10]:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")[:10000]
            if re.search(r"secret.{0,30}guard|sk[-_](live|ant|test)|EAAB|ghp_", text, re.IGNORECASE):
                has_secret_guard = True
                break
        except Exception:
            continue
    for md in _safe_rglob(ws, "*.md", 100):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")[:10000]
            if re.search(r"prompt\s+injection|jailbreak|HITL.{0,30}gate|external\s+comm.{0,30}approv", text, re.IGNORECASE):
                has_hitl_doc = True
                break
        except Exception:
            continue
    if has_secret_guard and has_hitl_doc:
        status = "present"
    elif has_secret_guard or has_hitl_doc:
        status = "partial"
    else:
        status = "absent"
    return {"status": status, "evidence": {"secret_guard_hook": has_secret_guard, "hitl_documented": has_hitl_doc}}


def _detect_05_compositionality(ws: Path) -> dict:
    """Compositionality · skill frontmatter contracts · idempotency declarations."""
    skill_dirs = list((ws / "10_SKILLS").iterdir()) if (ws / "10_SKILLS").is_dir() else []
    skill_dirs += list((ws / "skills").iterdir()) if (ws / "skills").is_dir() else []
    skills_with_contract = 0
    for sd in skill_dirs[:80]:
        if not sd.is_dir():
            continue
        skill_md = sd / "SKILL.md"
        if not skill_md.exists():
            continue
        try:
            text = skill_md.read_text(encoding="utf-8", errors="ignore")[:5000]
            if re.search(r"^---", text) and re.search(r"tools:|allowed-tools:", text):
                skills_with_contract += 1
        except Exception:
            continue
    total = sum(1 for sd in skill_dirs if sd.is_dir())
    ratio = skills_with_contract / total if total > 0 else 0
    status = "present" if ratio >= 0.7 else ("partial" if skills_with_contract > 0 else "absent")
    return {"status": status, "evidence": {"skills_with_contract": skills_with_contract, "total_skills": total}}


def _detect_06_temporal_coherence(ws: Path) -> dict:
    """Temporal coherence · absolute dates · reflexion cycles · session archives."""
    has_reflexion = bool(_safe_rglob(ws, "*reflexion*", 10) + _safe_rglob(ws, "*reflect*", 10))
    has_cronologia = (ws / "cronologia").is_dir() or bool(_safe_rglob(ws, "cronologia", 5))
    has_session_archive = bool(_safe_rglob(ws, "*session*", 30))
    # check date format in lessons
    abs_date_pat = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
    rel_date_pat = re.compile(r"\b(yesterday|last week|ieri|domani|tomorrow|next week)\b", re.IGNORECASE)
    abs_count = 0
    rel_count = 0
    for md in _safe_rglob(ws, "*.md", 50):
        path_str = str(md).lower()
        if "lessons" in path_str or "changelog" in path_str or "decision" in path_str:
            try:
                text = md.read_text(encoding="utf-8", errors="ignore")[:10000]
                abs_count += len(abs_date_pat.findall(text))
                rel_count += len(rel_date_pat.findall(text))
            except Exception:
                continue
    signals = sum([has_reflexion, has_cronologia, has_session_archive, abs_count > 10])
    if signals >= 3:
        status = "present"
    elif signals >= 1:
        status = "partial"
    else:
        status = "absent"
    return {
        "status": status,
        "evidence": {
            "reflexion_runner": has_reflexion,
            "cronologia_dir": has_cronologia,
            "session_archive": has_session_archive,
            "absolute_dates_count": abs_count,
            "relative_dates_count": rel_count,
        },
    }


def _detect_07_embodied_awareness(ws: Path) -> dict:
    """Embodied awareness · SessionStart hook · context injection at cold start."""
    hooks = _safe_rglob(ws, "session-start*", 5) + _safe_rglob(ws, "*SessionStart*", 5)
    has_session_start_hook = bool(hooks)
    has_cwd_injection = False
    has_branch_injection = False
    for f in hooks[:5]:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")[:10000]
            if re.search(r"pwd|cwd|working[- ]directory|MADANI_ROOT", text, re.IGNORECASE):
                has_cwd_injection = True
            if re.search(r"git.{0,10}branch|branch.{0,10}--show-current", text, re.IGNORECASE):
                has_branch_injection = True
        except Exception:
            continue
    signals = sum([has_session_start_hook, has_cwd_injection, has_branch_injection])
    if signals >= 3:
        status = "present"
    elif signals >= 1:
        status = "partial"
    else:
        status = "absent"
    return {
        "status": status,
        "evidence": {
            "session_start_hook": has_session_start_hook,
            "cwd_injection": has_cwd_injection,
            "branch_injection": has_branch_injection,
        },
    }


def _detect_08_knowledge_representation(ws: Path) -> dict:
    """Mix of representations · markdown + YAML + structured indexes."""
    has_yaml_indices = bool(_safe_rglob(ws, "*.yml", 30) + _safe_rglob(ws, "*.yaml", 30))
    has_json_indices = bool(_safe_rglob(ws, "*.json", 30))
    has_md_with_frontmatter = 0
    for md in _safe_rglob(ws, "*.md", 50):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")[:1000]
            if text.startswith("---"):
                has_md_with_frontmatter += 1
        except Exception:
            continue
    has_graph_or_vector = bool(_safe_rglob(ws, "*.embeddings*", 5) + _safe_rglob(ws, "*graph*", 5))
    signals = sum([has_yaml_indices, has_json_indices, has_md_with_frontmatter >= 5, has_graph_or_vector])
    if signals >= 3:
        status = "present"
    elif signals >= 1:
        status = "partial"
    else:
        status = "absent"
    return {
        "status": status,
        "evidence": {
            "yaml_files": has_yaml_indices,
            "json_files": has_json_indices,
            "md_with_frontmatter": has_md_with_frontmatter,
            "graph_or_vector_hint": has_graph_or_vector,
        },
    }


def _detect_09_resilience_partial_failure(ws: Path) -> dict:
    """Resilience · liveness watchdog · health endpoints · recovery runbooks."""
    has_liveness = bool(_safe_rglob(ws, "*liveness*", 10) + _safe_rglob(ws, "*watchdog*", 10))
    has_features_json = bool(_safe_rglob(ws, "features.json", 5))
    has_recovery_docs = False
    for md in _safe_rglob(ws, "*.md", 100):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")[:5000]
            if re.search(r"rollback|recovery\s+procedure|runbook|MTTR|MTTD|graceful\s+degrad", text, re.IGNORECASE):
                has_recovery_docs = True
                break
        except Exception:
            continue
    signals = sum([has_liveness, has_features_json, has_recovery_docs])
    if signals >= 3:
        status = "present"
    elif signals >= 1:
        status = "partial"
    else:
        status = "absent"
    return {
        "status": status,
        "evidence": {
            "liveness_watchdog": has_liveness,
            "features_json": has_features_json,
            "recovery_docs": has_recovery_docs,
        },
    }


def _detect_10_index_density(ws: Path) -> dict:
    """Index Density & Semantic Coverage · the vehicle of α."""
    # Count index-type files (heuristic patterns)
    structural_indices = len(_safe_rglob(ws, "INDEX.md", 100))
    root_indices = len([p for p in ws.glob("00_*") if p.is_file() and p.suffix == ".md"])
    manifests = len(_safe_rglob(ws, "*MANIFEST*", 20))
    entity_registry = (ws / "00_ENTITY-REGISTRY.md").exists() or bool(_safe_rglob(ws, "ENTITY-REGISTRY*", 5))
    llms_txt = (ws / "llms.txt").exists()
    agents_md = (ws / "00_AGENTS.md").exists() or (ws / "AGENTS.md").exists()

    total_indices = structural_indices + root_indices + manifests
    has_entity_layer = entity_registry or agents_md

    signals = 0
    signals += 1 if structural_indices >= 5 else 0
    signals += 1 if root_indices >= 2 else 0
    signals += 1 if manifests >= 1 else 0
    signals += 1 if has_entity_layer else 0
    signals += 1 if llms_txt else 0
    signals += 1 if entity_registry else 0  # explicit entity registry bonus

    if signals >= 5:
        status = "present"
    elif signals >= 2:
        status = "partial"
    else:
        status = "absent"

    return {
        "status": status,
        "evidence": {
            "INDEX_md_count": structural_indices,
            "root_00_files": root_indices,
            "manifests": manifests,
            "entity_registry": entity_registry,
            "llms_txt": llms_txt,
            "agents_md": agents_md,
            "signals": signals,
        },
    }


def _detect_11_meta_measurement(ws: Path) -> dict:
    """Meta-measurement · audit liveness · score decay · cross-pillar consistency awareness."""
    has_compliance_log = bool(_safe_rglob(ws, "*compliance*log*", 10))
    has_compliance_check = bool(_safe_rglob(ws, "compliance-check.py", 5) + _safe_rglob(ws, "*compliance*check*", 10))
    has_workspace_bench = (ws / ".workspace-bench").is_dir() or (ws / "bench-output").is_dir()
    has_anti_gaming_doc = False
    for md in _safe_rglob(ws, "*.md", 200):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")[:5000]
            if re.search(r"goodhart|gaming|anti[- ]gaming|score\s+decay", text, re.IGNORECASE):
                has_anti_gaming_doc = True
                break
        except Exception:
            continue
    signals = sum([has_compliance_log, has_compliance_check, has_workspace_bench, has_anti_gaming_doc])
    if signals >= 3:
        status = "present"
    elif signals >= 1:
        status = "partial"
    else:
        status = "absent"
    return {
        "status": status,
        "evidence": {
            "compliance_log_dir": has_compliance_log,
            "compliance_check_tool": has_compliance_check,
            "workspace_bench_history": has_workspace_bench,
            "anti_gaming_doc": has_anti_gaming_doc,
        },
    }


# ─── Registry · maps id → detector ───────────────────────────────────

DETECTORS = {
    "01-architecture-capability-decoupling": _detect_01_architecture_capability,
    "02-information-theory": _detect_02_information_theory,
    "03-causal-reasoning": _detect_03_causal_reasoning,
    "04-adversarial-robustness": _detect_04_adversarial_robustness,
    "05-compositionality": _detect_05_compositionality,
    "06-temporal-coherence": _detect_06_temporal_coherence,
    "07-embodied-awareness": _detect_07_embodied_awareness,
    "08-knowledge-representation": _detect_08_knowledge_representation,
    "09-resilience-partial-failure": _detect_09_resilience_partial_failure,
    "10-index-density": _detect_10_index_density,
    "11-meta-measurement": _detect_11_meta_measurement,
}

# Map shorter slugs (without "NN-" prefix) for profile YAML references
SHORT_ID_MAP = {ext["id"].split("-", 1)[1]: ext["id"] for ext in EXTENSIONS}
# also accept full id
SHORT_ID_MAP.update({ext["id"]: ext["id"] for ext in EXTENSIONS})


def detect_extensions(workspace_path: Path) -> dict:
    """Run all 11 detectors · return dict {ext_id: {status, evidence, title, cluster}}."""
    results = {}
    for ext in EXTENSIONS:
        eid = ext["id"]
        try:
            det_result = DETECTORS[eid](workspace_path)
        except Exception as e:
            det_result = {"status": "error", "evidence": str(e)}
        results[eid] = {
            "title": ext["title"],
            "cluster": ext["cluster"],
            **det_result,
        }
    return results


def resolve_extension_id(short_or_full: str) -> str | None:
    """Profile YAML may reference extensions by short slug (e.g., 'index-density') or full id."""
    return SHORT_ID_MAP.get(short_or_full)
