"""
Counterintuitive but high-signal metrics · advanced information theory layer.

Standard info_theory.py measures aggregate quality/quantity. This module dives
deeper into the *structure* of the workspace as a knowledge graph and surfaces
patterns that aren't visible from aggregate counts:

  - Knowledge graph centrality: which files are referenced by many others
  - Lonely documents: no inbound or outbound links
  - Echo chambers: groups of files that only reference each other
  - Stale ROI: stale + high centrality = high-value-to-update target
  - Diversity index: variation in how different folders use different patterns

These are the "counterintuitive but high signal" metrics: aggregate metrics
can look good while the graph is fundamentally fragmented; aggregate metrics
can look bad while the graph has a healthy core.
"""

from __future__ import annotations
import math
import os
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".next", "dist", "build", ".pytest_cache", ".mypy_cache"}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^\)]+)\)")
STALE_DAYS = 180


def _normalize_target(target: str) -> str:
    """Normalize a wiki-link target for matching."""
    # Strip .md extension, lowercase, strip whitespace
    t = target.strip().lower()
    if t.endswith(".md"):
        t = t[:-3]
    # Take only the slug part (after last /)
    if "/" in t:
        t = t.rsplit("/", 1)[1]
    return t


def build_link_graph(workspace: Path) -> dict:
    """
    Build the knowledge graph from wiki-style links and markdown references.

    Returns a dict with:
      - nodes: {slug: {path, mtime, size, ...}}
      - edges: list of (source_slug, target_slug) wiki-link edges
      - inbound: {slug: count of files linking TO it}
      - outbound: {slug: count of files linked FROM it}
    """
    workspace = workspace.resolve()
    nodes: dict[str, dict] = {}
    edges: list[tuple[str, str]] = []
    inbound: Counter = Counter()
    outbound: Counter = Counter()
    now = time.time()

    # First pass: collect nodes
    for dirpath, dirnames, filenames in os.walk(workspace):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and (not d.startswith(".") or d in {".claude", ".github"})]
        for fname in filenames:
            if not fname.endswith(".md"):
                continue
            fp = Path(dirpath) / fname
            slug = _normalize_target(fname)
            try:
                stat = fp.stat()
            except OSError:
                continue
            nodes[slug] = {
                "path": str(fp.relative_to(workspace)) if fp.is_relative_to(workspace) else str(fp),
                "mtime": stat.st_mtime,
                "size": stat.st_size,
                "stale": (now - stat.st_mtime) > (STALE_DAYS * 86400),
            }

    # Second pass: collect edges
    for slug, meta in nodes.items():
        full = workspace / meta["path"]
        try:
            content = full.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        # Wiki links
        for target in WIKILINK_RE.findall(content):
            tslug = _normalize_target(target)
            if tslug in nodes:
                edges.append((slug, tslug))
                outbound[slug] += 1
                inbound[tslug] += 1
        # Markdown links to local .md files only
        for _, url in MD_LINK_RE.findall(content):
            if url.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if not url.endswith(".md"):
                continue
            tslug = _normalize_target(url)
            if tslug in nodes:
                edges.append((slug, tslug))
                outbound[slug] += 1
                inbound[tslug] += 1

    return {"nodes": nodes, "edges": edges, "inbound": dict(inbound), "outbound": dict(outbound)}


def compute_advanced_metrics(workspace: Path) -> dict:
    """
    Compute counterintuitive but high-signal information theory metrics.

    Returns dict with:
      - knowledge_graph: nodes count · edges count · density
      - centrality: top 10 most-referenced files (high signal hubs)
      - lonely_documents: files with zero inbound AND zero outbound links
      - echo_chambers: SCC-like clusters of files that only reference each other
      - stale_high_value: files that are stale but highly referenced (update targets)
      - diversity: pattern diversity across folders
      - interpretation: human-readable labels
    """
    graph = build_link_graph(workspace)
    nodes = graph["nodes"]
    edges = graph["edges"]
    inbound = graph["inbound"]
    outbound = graph["outbound"]

    n_nodes = len(nodes)
    n_edges = len(edges)

    # ─── Graph density ────────────────────────────────────────────────────
    # Density = edges / (n * (n-1)) · ratio of present to possible edges
    max_possible = n_nodes * (n_nodes - 1) if n_nodes > 1 else 1
    density = round(n_edges / max(max_possible, 1) * 100, 4)  # percentage

    # ─── Centrality (top 10 by inbound) ──────────────────────────────────
    top_central = sorted(inbound.items(), key=lambda kv: -kv[1])[:10]
    centrality_top = [
        {
            "slug": slug,
            "inbound_links": count,
            "path": nodes[slug]["path"],
            "stale": nodes[slug]["stale"],
        }
        for slug, count in top_central
    ]

    # ─── Lonely documents (no inbound, no outbound) ─────────────────────
    lonely = [
        {"slug": slug, "path": meta["path"]}
        for slug, meta in nodes.items()
        if inbound.get(slug, 0) == 0 and outbound.get(slug, 0) == 0
    ]
    lonely_rate = round((len(lonely) / max(n_nodes, 1)) * 100, 2)

    # ─── Echo chambers (rough heuristic: files where all outbound links
    #     point to a small set, AND that set links back exclusively) ─────
    # Approximate: find pairs of files where slug_a → slug_b AND slug_b → slug_a
    edge_set = set(edges)
    mutual_pairs = []
    seen = set()
    for a, b in edges:
        if (b, a) in edge_set and (a, b) not in seen and (b, a) not in seen:
            mutual_pairs.append({"a": a, "b": b})
            seen.add((a, b))
            seen.add((b, a))
    echo_chamber_signal = len(mutual_pairs)

    # ─── Stale ROI: stale + high centrality ─────────────────────────────
    # High value to update: stale=True AND inbound >= 3
    stale_roi = []
    for slug, meta in nodes.items():
        inb = inbound.get(slug, 0)
        if meta["stale"] and inb >= 3:
            stale_roi.append({
                "slug": slug,
                "path": meta["path"],
                "inbound_links": inb,
                "age_days": round((time.time() - meta["mtime"]) / 86400, 1),
            })
    stale_roi.sort(key=lambda x: -x["inbound_links"])
    stale_roi_top = stale_roi[:10]

    # ─── Diversity index across folders ─────────────────────────────────
    # How many unique top-level folders contain documents?
    folder_dist: Counter = Counter()
    for meta in nodes.values():
        top_folder = meta["path"].split("/", 1)[0]
        folder_dist[top_folder] += 1
    folder_entropy = _shannon(folder_dist)
    max_folder_entropy = math.log2(len(folder_dist)) if folder_dist else 1
    folder_entropy_normalized = round((folder_entropy / max(max_folder_entropy, 1e-6)) * 100, 2)

    # ─── Interpretation ─────────────────────────────────────────────────
    interpretation = {}
    if lonely_rate > 30:
        interpretation["lonely"] = f"{lonely_rate}% files lonely · workspace fragmented · invest in cross-linking"
    elif lonely_rate > 15:
        interpretation["lonely"] = f"{lonely_rate}% files lonely · moderate · most files connected"
    else:
        interpretation["lonely"] = f"{lonely_rate}% files lonely · excellent · highly cross-linked"

    if density >= 1.0:
        interpretation["density"] = f"{density}% graph density · dense knowledge graph · agent can navigate"
    elif density >= 0.3:
        interpretation["density"] = f"{density}% graph density · moderate connectivity"
    else:
        interpretation["density"] = f"{density}% graph density · sparse · agent retrieval will struggle"

    if len(stale_roi_top) > 0:
        interpretation["stale_roi"] = f"{len(stale_roi_top)} stale-but-central files · prioritize updates"
    else:
        interpretation["stale_roi"] = "no stale + central files · knowledge is fresh OR not well-linked"

    if echo_chamber_signal > 5:
        interpretation["echo"] = f"{echo_chamber_signal} mutual link pairs · possible echo chambers"
    else:
        interpretation["echo"] = "no significant echo chambers detected"

    return {
        "knowledge_graph": {
            "nodes": n_nodes,
            "edges": n_edges,
            "density_pct": density,
        },
        "centrality_top": centrality_top,
        "lonely_documents": {
            "count": len(lonely),
            "rate_pct": lonely_rate,
            "sample": lonely[:5],
        },
        "echo_chamber_signal": {
            "mutual_link_pairs": echo_chamber_signal,
            "sample": mutual_pairs[:5],
        },
        "stale_roi_top": stale_roi_top,
        "folder_diversity": {
            "folders": len(folder_dist),
            "entropy_bits": round(folder_entropy, 3),
            "entropy_normalized_pct": folder_entropy_normalized,
        },
        "interpretation": interpretation,
    }


def _shannon(distribution: dict) -> float:
    total = sum(distribution.values())
    if total == 0:
        return 0.0
    h = 0.0
    for count in distribution.values():
        if count > 0:
            p = count / total
            h -= p * math.log2(p)
    return h
