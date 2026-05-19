"""
Information theory layer · signal-to-noise · Shannon entropy · density.

Quantifies the *information quality* of a workspace beyond pillar maturity.
The L0-L4 measures capability presence; this module measures the underlying
information health that capability rests on.

Core principle (Shannon · Wiener · cybernetics):
    α(workspace) = quantity(information) × quality(information)

The benchmark α is the geometric-mean composite of quantity and quality
indices, where:
  - quantity = volume of structured · cross-linked · frontmatter-bearing content
  - quality  = signal-to-noise · low staleness · high specificity · few broken refs

Counterintuitive but high-signal:
  - High file count alone is anti-signal (noise)
  - High frontmatter rate is strong signal (structured intent)
  - High cross-link density correlates with team-knowledge graph health
  - High entropy of file types is signal (diverse capability)
  - Low entropy of content per file is signal (focused intent)
"""

from __future__ import annotations
import math
import os
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any


IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".next", "dist", "build", ".pytest_cache", ".mypy_cache"}
STALE_DAYS = 180  # files older than this contribute to staleness noise
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
ARXIV_RE = re.compile(r"arxiv[:\s]+(\d{4}\.\d{4,5})", re.IGNORECASE)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^\)]+)\)")


def shannon_entropy(distribution: dict[Any, int]) -> float:
    """Shannon entropy in bits, given a distribution dict."""
    total = sum(distribution.values())
    if total == 0:
        return 0.0
    h = 0.0
    for count in distribution.values():
        if count > 0:
            p = count / total
            h -= p * math.log2(p)
    return round(h, 3)


def compute_info_theory(workspace: Path) -> dict:
    """
    Compute information-theoretic metrics over a workspace.

    Returns dict with:
      - quantity_index (0-100)
      - quality_index (0-100)
      - alpha (0-100, geometric mean)
      - snr (signal-to-noise ratio)
      - entropy (Shannon entropy of file-type distribution, bits)
      - density (information density: structured content / total content)
      - per-component breakdown
    """
    workspace = workspace.resolve()
    now = time.time()
    stale_threshold = now - (STALE_DAYS * 86400)

    file_count = 0
    md_count = 0
    code_count = 0
    config_count = 0
    asset_count = 0
    other_count = 0

    total_bytes = 0
    md_bytes = 0
    structured_bytes = 0  # bytes inside frontmatter-having files

    files_with_frontmatter = 0
    cross_link_total = 0
    arxiv_refs_total = 0
    md_link_total = 0

    stale_files = 0
    empty_files = 0
    near_empty_files = 0

    file_type_dist: Counter = Counter()
    extension_dist: Counter = Counter()

    for dirpath, dirnames, filenames in os.walk(workspace):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and (not d.startswith(".") or d in {".claude", ".github"})]
        for fname in filenames:
            fp = Path(dirpath) / fname
            try:
                stat = fp.stat()
            except OSError:
                continue
            file_count += 1
            size = stat.st_size
            total_bytes += size
            mtime = stat.st_mtime
            ext = fp.suffix.lower()
            extension_dist[ext] += 1

            if size == 0:
                empty_files += 1
                continue
            if size < 100:
                near_empty_files += 1

            if mtime < stale_threshold:
                stale_files += 1

            if ext in (".md", ".rst", ".txt"):
                md_count += 1
                md_bytes += size
                file_type_dist["docs"] += 1
                try:
                    content = fp.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                if FRONTMATTER_RE.search(content):
                    files_with_frontmatter += 1
                    structured_bytes += size
                cross_link_total += len(WIKILINK_RE.findall(content))
                arxiv_refs_total += len(ARXIV_RE.findall(content))
                md_link_total += len(MD_LINK_RE.findall(content))
            elif ext in (".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".c", ".cpp", ".h", ".rb", ".sh", ".bash"):
                code_count += 1
                file_type_dist["code"] += 1
            elif ext in (".json", ".yaml", ".yml", ".toml", ".ini", ".env", ".plist"):
                config_count += 1
                file_type_dist["config"] += 1
            elif ext in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".mp4", ".mov", ".webp"):
                asset_count += 1
                file_type_dist["asset"] += 1
            else:
                other_count += 1
                file_type_dist["other"] += 1

    # ─── Quantity index (volume of structured content) ─────────────────────
    # Caps at 100 with diminishing returns past 500 docs · prevents gaming by file-stuffing
    docs_volume_score = min(100, 100 * math.log10(max(md_count, 1) + 1) / math.log10(501))
    frontmatter_rate = (files_with_frontmatter / max(md_count, 1)) * 100
    cross_link_density = min(100, 100 * math.log10(max(cross_link_total, 1) + 1) / math.log10(501))

    quantity_index = round(0.5 * docs_volume_score + 0.3 * frontmatter_rate + 0.2 * cross_link_density, 2)

    # ─── Quality index (signal-to-noise) ──────────────────────────────────
    # Components:
    #   - low stale rate (files modified recently)
    #   - low empty/near-empty rate
    #   - high citation density (arxiv refs · md links)
    #   - high structured-content ratio (frontmatter bytes / total md bytes)
    stale_rate = (stale_files / max(file_count, 1)) * 100
    emptiness_rate = ((empty_files + near_empty_files) / max(file_count, 1)) * 100
    citation_density = min(100, 100 * (arxiv_refs_total + md_link_total) / max(md_count * 5, 1))
    structure_ratio = (structured_bytes / max(md_bytes, 1)) * 100

    quality_index = round(
        0.30 * (100 - stale_rate)
        + 0.20 * (100 - emptiness_rate)
        + 0.30 * citation_density
        + 0.20 * structure_ratio,
        2,
    )
    quality_index = max(0, min(100, quality_index))

    # ─── Alpha = geometric mean of quantity × quality ─────────────────────
    alpha = round(math.sqrt(max(quantity_index, 0) * max(quality_index, 0)), 2)

    # ─── Signal-to-noise ratio ────────────────────────────────────────────
    # Signal = (frontmatter + cross-link + citation) · Noise = (stale + empty + redundant)
    signal = files_with_frontmatter + cross_link_total + arxiv_refs_total + md_link_total
    noise = stale_files + empty_files + near_empty_files
    snr = round(signal / max(noise, 1), 2)
    snr_db = round(10 * math.log10(max(snr, 1e-6)), 2)  # decibel format

    # ─── Shannon entropy of file-type distribution ────────────────────────
    file_type_entropy = shannon_entropy(file_type_dist)
    # Max entropy with 5 categories is log2(5) ≈ 2.32
    max_entropy = math.log2(len(file_type_dist)) if file_type_dist else 1.0
    normalized_entropy = round((file_type_entropy / max(max_entropy, 1e-6)) * 100, 2)

    # ─── Information density (per file) ───────────────────────────────────
    avg_md_size = md_bytes / max(md_count, 1)
    density = round(min(100, (avg_md_size / 4000) * 100), 2)  # 4KB target

    return {
        "alpha": alpha,
        "quantity_index": quantity_index,
        "quality_index": quality_index,
        "snr": snr,
        "snr_db": snr_db,
        "entropy_bits": file_type_entropy,
        "entropy_normalized": normalized_entropy,
        "density": density,
        "components": {
            "files_total": file_count,
            "files_docs": md_count,
            "files_code": code_count,
            "files_config": config_count,
            "files_assets": asset_count,
            "files_other": other_count,
            "files_with_frontmatter": files_with_frontmatter,
            "frontmatter_rate_pct": round(frontmatter_rate, 2),
            "cross_links_total": cross_link_total,
            "arxiv_citations": arxiv_refs_total,
            "md_links": md_link_total,
            "files_stale_pct": round(stale_rate, 2),
            "files_empty_or_near_empty_pct": round(emptiness_rate, 2),
            "citation_density_pct": round(citation_density, 2),
            "structure_ratio_pct": round(structure_ratio, 2),
        },
        "signal": signal,
        "noise": noise,
        "interpretation": _interpret(alpha, snr, quantity_index, quality_index, normalized_entropy),
    }


def _interpret(alpha: float, snr: float, q_idx: float, qual_idx: float, entropy_n: float) -> dict[str, str]:
    """Generate human-readable interpretation labels."""
    labels = {}

    if alpha >= 70:
        labels["alpha"] = "high · workspace optimizes both quantity AND quality"
    elif alpha >= 50:
        labels["alpha"] = "solid · room to push on the weaker dimension"
    elif alpha >= 30:
        labels["alpha"] = "early · invest in structure (frontmatter · cross-links · citations)"
    else:
        labels["alpha"] = "prototype · build quantity of structured content first"

    if snr >= 5:
        labels["snr"] = "excellent · signal dominates noise"
    elif snr >= 2:
        labels["snr"] = "healthy · more signal than noise"
    elif snr >= 1:
        labels["snr"] = "marginal · noise approaching signal"
    else:
        labels["snr"] = "poor · noise dominates · prune stale and empty files"

    if entropy_n >= 80:
        labels["entropy"] = "diverse file ecosystem · multi-modal capability"
    elif entropy_n >= 50:
        labels["entropy"] = "balanced distribution"
    else:
        labels["entropy"] = "concentrated · workspace specializes (good if intentional)"

    if q_idx > qual_idx * 1.5:
        labels["balance"] = "quantity > quality · structure existing content before adding more"
    elif qual_idx > q_idx * 1.5:
        labels["balance"] = "quality > quantity · ready to grow volume of structured content"
    else:
        labels["balance"] = "balanced quantity and quality"

    return labels
