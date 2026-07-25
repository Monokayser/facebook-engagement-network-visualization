"""Project-wide configuration and reproducibility constants."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_GENERATED = ROOT / "data" / "generated"
OUTPUTS = ROOT / "outputs"
TABLES = OUTPUTS / "tables"
EXERCISE_SUMMARIES = OUTPUTS / "exercise_summaries"
STATIC = ROOT / "visualizations" / "static"
INTERACTIVE = ROOT / "visualizations" / "interactive"
REPORT = ROOT / "report"
REPORT_FIGURES = REPORT / "figures"
PUBLIC = ROOT / "public"
WEBSITE = ROOT / "website"
NOTEBOOKS = ROOT / "notebooks"

RAW_CSV = DATA_RAW / "Live_20210128.csv"
PROCESSED_CSV = DATA_PROCESSED / "facebook_live_sellers_cleaned.csv"
ANALYSIS_SUMMARY = OUTPUTS / "analysis_summary.json"
SEED = 42

STUDENT = {
    "name": "S. M. Monowar Kayser",
    "id": "253-25-019",
    "course_name": "Data Visualization",
    "course_code": "CSE628",
    "semester": "Summer 2026",
    "teacher": "Sadat Hasan",
    "designation": "Adjunct Faculty",
    "department": "Department of Computer Science and Engineering",
    "university": "Daffodil International University",
}

DATASET = {
    "title": "Facebook Live Sellers in Thailand",
    "author": "Nassim Dehouche",
    "publisher": "UCI Machine Learning Repository",
    "doi": "10.24432/C5R60S",
    "official_url": (
        "https://archive.ics.uci.edu/dataset/488/"
        "facebook%2Blive%2Bsellers%2Bin%2Bthailand"
    ),
    "kaggle_mirror": (
        "https://www.kaggle.com/datasets/ashishg21/"
        "facebook-live-sellers-in-thailand-uci-ml-repo"
    ),
    "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
    "download_date": "2026-07-25",
    "file_format": "CSV",
    "raw_sha256": "ea6a31aab095b15d3fd0c24a63d5d59822f1dd34922b09295179ea9c464a8d5b",
    "acquisition": (
        "Downloaded from the official UCI repository because Kaggle API "
        "credentials were not configured. The Kaggle mirror is documented "
        "for discoverability; it was not used for acquisition."
    ),
}


def ensure_directories() -> None:
    """Create the project's generated-output directories."""

    for directory in (
        DATA_RAW,
        DATA_PROCESSED,
        DATA_GENERATED,
        TABLES,
        EXERCISE_SUMMARIES,
        STATIC,
        INTERACTIVE,
        REPORT,
        REPORT_FIGURES,
        PUBLIC / "interactive",
        PUBLIC / "images",
        PUBLIC / "data",
        WEBSITE,
        NOTEBOOKS,
    ):
        directory.mkdir(parents=True, exist_ok=True)
