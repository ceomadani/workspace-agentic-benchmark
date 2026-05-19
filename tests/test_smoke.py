"""End-to-end smoke tests for workspace-bench."""

import json
from pathlib import Path

import pytest

from workspace_bench.audit import run_audit, workspace_stats
from workspace_bench.score import score_audit
from workspace_bench.html_report import render_html
from workspace_bench.compare import compare_scores, save_to_history, load_history
from workspace_bench.info_theory import compute_info_theory
from workspace_bench.info_theory_advanced import compute_advanced_metrics
from workspace_bench.data import PILLARS, grade, equal_weights


def test_pillars_count():
    """12 pillars · 4 clusters."""
    assert len(PILLARS) == 12
    clusters = {p.cluster_letter for p in PILLARS}
    assert clusters == {"A", "B", "C", "D"}


def test_grade_thresholds():
    assert grade(85) == "A"
    assert grade(84) == "B"
    assert grade(70) == "B"
    assert grade(50) == "C"
    assert grade(30) == "D"
    assert grade(0) == "F"


def test_audit_on_empty_workspace(empty_workspace):
    audit = run_audit(empty_workspace)
    assert audit["version"]
    assert audit["workspace"] == str(empty_workspace.resolve())
    assert len(audit["pillars"]) == 12


def test_audit_on_structured_workspace(structured_workspace):
    audit = run_audit(structured_workspace)
    score = score_audit(audit)
    assert "composite" in score
    assert "grade" in score
    assert score["composite"] >= 0
    assert score["composite"] <= 100
    assert score["grade"] in {"A", "B", "C", "D", "F"}


def test_structured_scores_higher_than_empty(empty_workspace, structured_workspace):
    empty_score = score_audit(run_audit(empty_workspace))
    structured_score = score_audit(run_audit(structured_workspace))
    assert structured_score["composite"] > empty_score["composite"], \
        "structured workspace should score strictly higher than empty"


def test_html_report_renders(structured_workspace):
    audit = run_audit(structured_workspace)
    score = score_audit(audit)
    html = render_html(score, language="en")
    assert "<!DOCTYPE html>" in html
    assert "Workspace" in html
    assert score["grade"] in html
    # Multi-language smoke
    html_it = render_html(score, language="it")
    assert "Pillar" in html_it or "Cluster" in html_it


def test_compare_two_scores(structured_workspace, empty_workspace):
    score_a = score_audit(run_audit(empty_workspace))
    score_b = score_audit(run_audit(structured_workspace))
    diff = compare_scores(score_a, score_b)
    assert diff["composite_delta"] >= 0  # structured ≥ empty
    assert len(diff["pillar_diffs"]) == 12


def test_history_roundtrip(structured_workspace, tmp_path):
    audit = run_audit(structured_workspace)
    score = score_audit(audit)
    hist_dir = tmp_path / "history"
    snap = save_to_history(audit, score, hist_dir)
    assert snap.exists()
    history = load_history(hist_dir)
    assert len(history) == 1
    assert history[0]["composite"] == score["composite"]


def test_info_theory_computed(structured_workspace):
    info = compute_info_theory(structured_workspace)
    assert "alpha" in info
    assert "snr" in info
    assert "entropy_bits" in info
    assert 0 <= info["alpha"] <= 100
    assert info["snr"] >= 0


def test_advanced_metrics_computed(structured_workspace):
    advanced = compute_advanced_metrics(structured_workspace)
    assert "knowledge_graph" in advanced
    assert "centrality_top" in advanced
    assert "lonely_documents" in advanced
    assert "interpretation" in advanced


def test_workspace_stats(structured_workspace):
    stats = workspace_stats(structured_workspace)
    assert stats["files"] > 0
    assert stats["bytes"] > 0


def test_equal_weights_sum_to_one():
    weights = equal_weights()
    assert abs(sum(weights.values()) - 1.0) < 1e-6
