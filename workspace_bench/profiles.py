"""Iter-2 · profile loader · contextual weighting.

Profiles live in `<repo>/profiles/*.yml` · they declare:
  - weights: per-pillar float multiplier (1.0 = standard, 0.0 = ignore, 2.0 = double)
  - extensions_required: list of extension short-ids that MUST be present
  - extensions_optional: list of extension short-ids that are nice-to-have

The CLI's `--profile <name>` flag references the profile by `profile_id` (the
slug without .yml). Default behavior with no profile = iter-1 equal weights.
"""

from __future__ import annotations
from pathlib import Path

try:
    import yaml  # type: ignore
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

# Map between profile YAML pillar names and internal pillar keys
PILLAR_NAME_MAP = {
    "P01_context_memory": "1_context_memory",
    "P02_skill_tool": "2_skill_tool",
    "P03_governance": "3_governance",
    "P04_auto_improvement": "4_auto_improvement",
    "P05_multi_agent_dpi": "5_multi_agent_dpi",
    "P06_observability": "6_observability",
    "P07_credentials_security": "7_credentials_security",
    "P08_portability": "8_portability",
    "P09_metacognition": "9_metacognition",
    "P10_reliability": "10_reliability",
    "P11_human_in_the_loop": "11_human_in_the_loop",
    "P12_cost_performance": "12_cost_performance",
}


def _profiles_dir() -> Path:
    """Locate `profiles/` relative to package install."""
    pkg_dir = Path(__file__).resolve().parent
    # Try sibling of workspace_bench/ first (repo layout)
    repo_root = pkg_dir.parent
    if (repo_root / "profiles").is_dir():
        return repo_root / "profiles"
    # Fallback: inside package (if shipped that way)
    if (pkg_dir / "profiles").is_dir():
        return pkg_dir / "profiles"
    return repo_root / "profiles"  # default · may not exist


def _parse_yaml_simple(text: str) -> dict:
    """Minimal YAML parser for the simple format we use (no PyYAML dependency).

    Handles: top-level scalars · `weights:` dict of float values · list under `extensions_required:` etc.
    Not robust for arbitrary YAML · only our profile shape.
    """
    if HAVE_YAML:
        return yaml.safe_load(text)
    # Minimal hand-rolled parser
    result: dict = {}
    current_key = None
    current_dict = None
    current_list = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and not line.startswith("\t"):
            # top-level
            if ":" in line:
                key, _, val = line.partition(":")
                key = key.strip()
                val = val.strip()
                if val == "":
                    # block start
                    current_key = key
                    if key in ("weights",):
                        current_dict = {}
                        result[key] = current_dict
                    else:
                        current_list = []
                        result[key] = current_list
                else:
                    val = val.strip().strip('"').strip("'")
                    # strip block scalars
                    if val == ">":
                        current_key = key
                        result[key] = ""
                        continue
                    result[key] = val
                    current_key = None
                    current_dict = None
                    current_list = None
            continue
        # indented
        stripped = line.lstrip()
        if current_dict is not None and ":" in stripped:
            key, _, val = stripped.partition(":")
            try:
                current_dict[key.strip()] = float(val.strip())
            except ValueError:
                current_dict[key.strip()] = val.strip()
        elif current_list is not None and stripped.startswith("- "):
            item = stripped[2:].strip().strip('"').strip("'")
            current_list.append(item)
        elif isinstance(result.get(current_key), str) and current_key:
            # block scalar continuation
            result[current_key] += stripped + " "
    return result


def load_profile(profile_id: str) -> dict | None:
    """Load profile by id · returns dict with weights + extensions_required + extensions_optional.

    Returns None if profile not found.
    """
    profiles_dir = _profiles_dir()
    candidate = profiles_dir / f"{profile_id}.yml"
    if not candidate.exists():
        candidate = profiles_dir / f"{profile_id}.yaml"
    if not candidate.exists():
        return None
    try:
        text = candidate.read_text(encoding="utf-8")
        return _parse_yaml_simple(text)
    except Exception:
        return None


def available_profiles() -> list[str]:
    """List profile_ids found in profiles/ directory."""
    profiles_dir = _profiles_dir()
    if not profiles_dir.is_dir():
        return []
    return sorted([p.stem for p in profiles_dir.glob("*.yml") if not p.name.startswith("README")])


def profile_to_pillar_weights(profile: dict) -> dict[str, float]:
    """Convert profile's weights dict (P01_context_memory: 1.5) to internal pillar keys (1_context_memory: 1.5)."""
    raw = profile.get("weights", {}) or {}
    weights = {}
    for profile_key, w in raw.items():
        internal = PILLAR_NAME_MAP.get(profile_key)
        if internal:
            try:
                weights[internal] = float(w)
            except (TypeError, ValueError):
                continue
    # Default missing pillars to 1.0
    for internal in PILLAR_NAME_MAP.values():
        if internal not in weights:
            weights[internal] = 1.0
    return weights


def evaluate_extensions_against_profile(
    profile: dict, extensions_result: dict
) -> dict:
    """Check which required/optional extensions are present · return summary.

    Returns:
      {
        "required": [{"id": ..., "status": "present|partial|absent"}],
        "optional": [...],
        "required_present_count": N,
        "required_total": M,
        "required_compliance_ratio": 0.0-1.0,
      }
    """
    from .extensions import resolve_extension_id

    req = profile.get("extensions_required", []) or []
    opt = profile.get("extensions_optional", []) or []

    def _check(slug: str) -> dict:
        ext_id = resolve_extension_id(slug)
        if ext_id is None:
            return {"id": slug, "status": "unknown_extension"}
        result = extensions_result.get(ext_id, {})
        return {
            "id": ext_id,
            "title": result.get("title", ""),
            "status": result.get("status", "absent"),
        }

    required_results = [_check(s) for s in req]
    optional_results = [_check(s) for s in opt]

    req_present = sum(1 for r in required_results if r["status"] == "present")
    req_partial = sum(1 for r in required_results if r["status"] == "partial")
    req_total = len(required_results)
    # "present" counts 1.0 · "partial" counts 0.5
    req_compliance = (req_present + 0.5 * req_partial) / req_total if req_total > 0 else 1.0

    return {
        "required": required_results,
        "optional": optional_results,
        "required_present_count": req_present,
        "required_partial_count": req_partial,
        "required_total": req_total,
        "required_compliance_ratio": round(req_compliance, 3),
    }
