import json
from zipfile import ZipFile

from src.config import ANALYSIS_SUMMARY, REPORT, ROOT


def test_reports_and_verified_summary_exist():
    for filename in ("report.md", "report.docx", "report.pdf"):
        path = REPORT / filename
        assert path.exists() and path.stat().st_size > 10_000
    summary = json.loads(ANALYSIS_SUMMARY.read_text(encoding="utf-8"))
    assert summary["engagement"]["rows"] == 7050
    assert summary["exercises"]["exercise_1"]["matrix_symmetric"] is True


def test_docx_contains_student_and_project_title():
    with ZipFile(REPORT / "report.docx") as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    assert "S. M. Monowar Kayser" in xml
    assert "Visual Analytics and Network Analysis" in xml


def test_configured_paths_are_relative_to_project_root():
    for path in (REPORT, ANALYSIS_SUMMARY):
        assert path.is_relative_to(ROOT)
