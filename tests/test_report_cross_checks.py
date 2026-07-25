"""Cross-check report claims against the machine-readable analytical summary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report"
PUBLIC = ROOT / "public"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_exercise_claims_match_verified_summary() -> None:
    summary = json.loads(
        (ROOT / "outputs" / "analysis_summary.json").read_text(encoding="utf-8")
    )
    markdown = (REPORT / "report.md").read_text(encoding="utf-8")
    exercises = summary["exercises"]

    exercise_1 = exercises["exercise_1"]
    assert f"density of {exercise_1['density']:.4f}" in markdown
    assert f"{exercise_1['total_recorded_distance_km']:,} km" in markdown
    assert f"{exercise_1['longest_route']['distance_km']} km" in markdown

    exercise_2 = exercises["exercise_2"]
    assert f"density {exercise_2['density']:.4f}" in markdown
    assert f"diameter {exercise_2['diameter']}" in markdown
    assert f"**{exercise_2['average_clustering']:.3f}**" in markdown

    exercise_3 = exercises["exercise_3"]
    assert f"{exercise_3['enrollments']} enrollment records" in markdown
    assert f"{exercise_3['bipartite_density']:.4f}" in markdown
    assert f"{exercise_3['mean_courses_per_student']:.2f} courses" in markdown

    exercise_4 = exercises["exercise_4"]
    assert f"mean was {exercise_4['mean_weight']:.3f}" in markdown
    assert f"median was {exercise_4['median_weight']:.1f}" in markdown
    assert f"{exercise_4['total_edge_weight']:,}" in markdown

    exercise_5 = exercises["exercise_5"]
    for record in exercise_5["records"]:
        assert f"{record['Density']:.3f}" in markdown
        assert f"{record['Average Clustering']:.3f}" in markdown

    exercise_6 = exercises["exercise_6"]
    assert f"{exercise_6['edges']} directed follow edges" in markdown
    assert f"{exercise_6['density']:.4f}" in markdown
    assert f"{exercise_6['minimum_in_degree']} to " in markdown
    assert f"{exercise_6['maximum_in_degree']}" in markdown

    exercise_7 = exercises["exercise_7"]
    assert f"{exercise_7['density']:.4f}" in markdown
    assert f"{exercise_7['top_betweenness_value']:.4f}" in markdown
    assert "Edge distance was defined as (1 / strength)" in markdown


def test_public_report_copies_are_identical() -> None:
    for suffix in ("md", "docx", "pdf"):
        assert _sha256(REPORT / f"report.{suffix}") == _sha256(
            PUBLIC / f"report.{suffix}"
        )
