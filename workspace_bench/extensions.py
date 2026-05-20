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
    """Glob with cap · skip common dependency/build/cache/version-control folders.

    Vendor-neutral: skip only ECOSYSTEM-STANDARD folders, not workspace-specific naming.
    """
    # Ecosystem-standard skip dirs · same across any project
    SKIP_DIRS = {
        ".git", ".hg", ".svn",                  # VCS
        "node_modules", ".npm",                 # JavaScript
        ".venv", "venv", "__pycache__",         # Python
        "vendor",                                # Go · PHP
        "target", "build", "dist", "out",       # Build outputs
        ".next", ".nuxt", ".cache",             # Frameworks
        ".idea", ".vscode",                     # IDE
    }
    # Lower-case path fragments suggesting "not currently active code"
    SEMANTIC_SKIP_FRAGMENTS = ("archive", "deprecated", "_old", "snapshot")
    results = []
    try:
        for p in path.rglob(pattern):
            parts = p.parts
            if any(part in SKIP_DIRS for part in parts):
                continue
            path_lower = str(p).lower()
            if any(frag in path_lower for frag in SEMANTIC_SKIP_FRAGMENTS):
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
    """Causal reasoning support · rules have explicit Why · post-mortem with chain.

    Detector v3 · vendor-neutral · language-agnostic:
      - Exclude SEMANTIC categories (archive · deprecated · vendor packages) via path heuristic
        rather than workspace-specific folder names.
      - Why-pattern accepts EN ("Why" · "Rationale" · "Reason" · "Why it matters") + IT
        ("Perché"). No workspace-specific terminology like custom frontmatter keys.
    """
    # Semantic exclusion patterns · apply to any workspace
    EXCLUDE_FRAGMENTS_LOWER = (
        "archive", "deprecated", "legacy", "_old/", "node_modules",
        ".git/", "vendor/", "__pycache__", "snapshot",
    )
    # Generic skill-internal pattern: "<anywhere>/skill-name/rules/"
    # (a single rules/ folder NESTED INSIDE a sub-package suggests skill/plugin scope,
    # not workspace-wide governance) — heuristic: rules folder ≥3 levels deep
    why_pattern = re.compile(
        r"^##?\s*Why\b|\*\*Why\*\*|^##?\s*Why\s+it\s+matters\b|"
        r"^##?\s*Rationale\b|^##?\s*Reason\b|"
        r"^##?\s*Perché\b|\*\*Perché\*\*",
        re.IGNORECASE | re.MULTILINE,
    )
    rules_with_why = 0
    total_rules = 0
    for md in _safe_rglob(ws, "*.md", 300):
        path_str = str(md).lower()
        # Path-based category match
        if not any(x in path_str for x in ["rules/", "rule-", "policy", "constitution"]):
            continue
        # Semantic exclusions
        if any(frag in path_str for frag in EXCLUDE_FRAGMENTS_LOWER):
            continue
        # Heuristic: skip rules nested deep inside packages (skill-internal pattern)
        # workspace-root rules are typically ≤3 levels deep relative to workspace
        try:
            depth = len(md.relative_to(ws).parts)
        except Exception:
            depth = 99
        # rules/ folder nested deeper than 4 levels is typically a vendored skill/plugin internal rules
        if depth > 4 and "rules/" in path_str and not path_str.endswith(("constitution.md", "policy.md")):
            # exclude unless it's a top-level policy/constitution file
            continue
        total_rules += 1
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")[:20000]
            if why_pattern.search(text):
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
            "total_rules_scoped": total_rules,
            "ratio": round(ratio, 2),
            "lessons_files_count": len(lessons_files),
        },
    }


def _detect_04_adversarial_robustness(ws: Path) -> dict:
    """Adversarial robustness · secret guard hook · provenance tagging · HITL gates.

    Vendor-neutral: scan hook files for secret patterns + dedicated security policy docs.
    Priority-scan for adversarial/security/HITL-named docs · then fallback to broad markdown scan.
    """
    hook_files = (
        _safe_rglob(ws, "pre-tool-use*", 5)
        + _safe_rglob(ws, "*PreToolUse*", 5)
        + _safe_rglob(ws, "*hook*.sh", 20)
        + _safe_rglob(ws, "*hook*.js", 20)
        + _safe_rglob(ws, "*hook*.py", 20)
    )
    has_secret_guard = False
    has_hitl_doc = False
    for f in hook_files[:20]:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")[:10000]
            if re.search(r"secret.{0,30}guard|sk[-_](live|ant|test)|EAAB[a-zA-Z]|ghp_[a-zA-Z]", text, re.IGNORECASE):
                has_secret_guard = True
                break
        except Exception:
            continue
    # Priority-scan: docs named for adversarial/security/HITL topics
    priority_md = (
        _safe_rglob(ws, "*adversar*", 5)
        + _safe_rglob(ws, "*hitl*", 5)
        + _safe_rglob(ws, "*security*polic*", 10)
        + _safe_rglob(ws, "*injection*", 5)
        + _safe_rglob(ws, "*jailbreak*", 5)
        + _safe_rglob(ws, "*threat*model*", 5)
    )
    hitl_pattern = re.compile(
        r"prompt\s+injection|jailbreak|HITL[\s.,·-]{0,30}gate|"
        r"external\s+comm.{0,30}approv|human[- ]in[- ]the[- ]loop|"
        r"adversarial\s+robust|threat\s+model",
        re.IGNORECASE,
    )
    for f in priority_md[:10]:
        if not str(f).endswith(".md"):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")[:15000]
            if hitl_pattern.search(text):
                has_hitl_doc = True
                break
        except Exception:
            continue
    # Fallback: broad scan if not found via priority
    if not has_hitl_doc:
        for md in _safe_rglob(ws, "*.md", 200):
            try:
                text = md.read_text(encoding="utf-8", errors="ignore")[:5000]
                if hitl_pattern.search(text):
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
    """Compositionality · skill frontmatter contracts · idempotency declarations.

    Vendor-neutral: scan multiple common skill-folder conventions.
    """
    # Common skill folder conventions across ecosystems
    SKILL_FOLDER_CANDIDATES = [
        "skills", "10_SKILLS", ".claude/skills", "agents", "plugins", "modules",
    ]
    skill_dirs = []
    for cand in SKILL_FOLDER_CANDIDATES:
        candidate_path = ws / cand
        if candidate_path.is_dir():
            try:
                skill_dirs += list(candidate_path.iterdir())
            except Exception:
                continue
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
    """Temporal coherence · absolute dates · reflection cycles · session archives.

    Vendor-neutral: scan generic concepts (reflection · session archive · changelog · history).
    """
    # Concept-based scan · multiple naming conventions
    has_reflection_cycle = bool(
        _safe_rglob(ws, "*reflexion*", 10)
        + _safe_rglob(ws, "*reflect*", 10)
        + _safe_rglob(ws, "*retrospective*", 10)
    )
    # Session archive (any naming · cronologia/history/sessions/snapshots/archive-sessions)
    has_session_archive = bool(
        _safe_rglob(ws, "*session-archive*", 5)
        + _safe_rglob(ws, "*sessions*", 30)
        + _safe_rglob(ws, "history*", 10)
        + _safe_rglob(ws, "cronologia*", 5)   # Italian convention · still permitted
        + _safe_rglob(ws, "snapshot*", 10)
    )
    has_changelog = bool(_safe_rglob(ws, "CHANGELOG*", 10) + _safe_rglob(ws, "*changelog*", 10))
    # Absolute dates in temporal-coherence-relevant files (lessons · changelog · decision logs)
    abs_date_pat = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
    rel_date_pat = re.compile(
        r"\b(yesterday|last\s+week|tomorrow|next\s+week|ieri|domani|hier|demain)\b",
        re.IGNORECASE,
    )
    abs_count = 0
    rel_count = 0
    for md in _safe_rglob(ws, "*.md", 100):
        path_str = str(md).lower()
        if any(x in path_str for x in ["lessons", "changelog", "decision", "history", "retrospective"]):
            try:
                text = md.read_text(encoding="utf-8", errors="ignore")[:10000]
                abs_count += len(abs_date_pat.findall(text))
                rel_count += len(rel_date_pat.findall(text))
            except Exception:
                continue
    signals = sum([has_reflection_cycle, has_session_archive, has_changelog, abs_count > 10])
    if signals >= 3:
        status = "present"
    elif signals >= 1:
        status = "partial"
    else:
        status = "absent"
    return {
        "status": status,
        "evidence": {
            "reflection_cycle": has_reflection_cycle,
            "session_archive": has_session_archive,
            "changelog_files": has_changelog,
            "absolute_dates_count": abs_count,
            "relative_dates_count": rel_count,
        },
    }


def _detect_07_embodied_awareness(ws: Path) -> dict:
    """Embodied awareness · SessionStart hook · context injection at cold start.

    Vendor-neutral: generic patterns for cwd/branch injection in any hook script.
    """
    hooks = _safe_rglob(ws, "session-start*", 5) + _safe_rglob(ws, "*SessionStart*", 5) + _safe_rglob(ws, "*startup*", 10)
    has_session_start_hook = bool(hooks)
    has_cwd_injection = False
    has_branch_injection = False
    # Generic env-var pattern for workspace-root injection (any naming · *_ROOT or *_HOME or WORKSPACE)
    workspace_var_pattern = re.compile(
        r"\bpwd\b|\bcwd\b|working[- ]directory|"
        r"\b[A-Z][A-Z_]{2,}_(ROOT|HOME|DIR|PATH|BASE)\b|"
        r"\bWORKSPACE\b",
        re.IGNORECASE,
    )
    for f in hooks[:5]:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")[:10000]
            if workspace_var_pattern.search(text):
                has_cwd_injection = True
            if re.search(r"git.{0,10}branch|branch.{0,10}--show-current|HEAD\.ref|git\s+rev-parse", text, re.IGNORECASE):
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
    """Resilience · liveness watchdog · health endpoints · recovery runbooks.

    Vendor-neutral: scan for concept-level signals (health monitoring · state snapshots · recovery docs).
    """
    has_liveness = bool(
        _safe_rglob(ws, "*liveness*", 10)
        + _safe_rglob(ws, "*watchdog*", 10)
        + _safe_rglob(ws, "*health-check*", 10)
        + _safe_rglob(ws, "*healthcheck*", 10)
    )
    # State snapshot files (any naming · features.json/health.json/status.json/state.json)
    has_state_snapshot = bool(
        _safe_rglob(ws, "features.json", 5)
        + _safe_rglob(ws, "health*.json", 5)
        + _safe_rglob(ws, "status.json", 5)
        + _safe_rglob(ws, "state.json", 5)
    )
    has_recovery_docs = False
    for md in _safe_rglob(ws, "*.md", 100):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")[:5000]
            if re.search(r"rollback|recovery\s+procedure|runbook|MTTR|MTTD|graceful\s+degrad|fault\s+tolerance|circuit\s+break", text, re.IGNORECASE):
                has_recovery_docs = True
                break
        except Exception:
            continue
    signals = sum([has_liveness, has_state_snapshot, has_recovery_docs])
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
            "state_snapshot_file": has_state_snapshot,
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
    """Meta-measurement · audit liveness · score decay · cross-pillar consistency awareness.

    Vendor-neutral: scan for concept signals (compliance/audit logs · meta-measurement docs · benchmark history).
    """
    has_compliance_log = bool(
        _safe_rglob(ws, "*compliance*log*", 10)
        + _safe_rglob(ws, "*audit*log*", 10)
    )
    has_compliance_tool = bool(
        _safe_rglob(ws, "*compliance*check*", 10)
        + _safe_rglob(ws, "*compliance*verify*", 10)
        + _safe_rglob(ws, "*audit-tool*", 10)
    )
    has_workspace_bench = (ws / ".workspace-bench").is_dir() or (ws / "bench-output").is_dir()
    has_anti_gaming_doc = False
    for md in _safe_rglob(ws, "*.md", 200):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")[:5000]
            if re.search(r"goodhart|gaming|anti[- ]gaming|score\s+decay|metric\s+gaming|measurement\s+target", text, re.IGNORECASE):
                has_anti_gaming_doc = True
                break
        except Exception:
            continue
    signals = sum([has_compliance_log, has_compliance_tool, has_workspace_bench, has_anti_gaming_doc])
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
            "compliance_check_tool": has_compliance_tool,
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
