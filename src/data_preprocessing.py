"""Cleaning, feature engineering, validation, and analytical summaries."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

NUMERIC_COLUMNS = [
    "num_reactions",
    "num_comments",
    "num_shares",
    "num_likes",
    "num_loves",
    "num_wows",
    "num_hahas",
    "num_sads",
    "num_angrys",
]


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Divide safely, returning zero where the denominator is zero."""

    result = np.divide(
        numerator.to_numpy(dtype=float),
        denominator.to_numpy(dtype=float),
        out=np.zeros(len(numerator), dtype=float),
        where=denominator.to_numpy(dtype=float) != 0,
    )
    return pd.Series(result, index=numerator.index)


def clean_and_engineer(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Clean raw records and create features supported by the dataset."""

    frame = raw.copy()
    initial_rows, initial_columns = frame.shape
    empty_columns = [column for column in frame if frame[column].isna().all()]
    frame = frame.drop(columns=empty_columns)
    frame.columns = (
        frame.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    duplicate_rows = int(frame.duplicated().sum())
    duplicate_ids = int(frame.duplicated("status_id").sum())
    frame = frame.drop_duplicates().drop_duplicates("status_id", keep="first")

    frame["status_type"] = frame["status_type"].astype(str).str.strip().str.lower()
    allowed_types = {"video", "photo", "status", "link"}
    invalid_types = sorted(set(frame["status_type"]) - allowed_types)
    if invalid_types:
        raise ValueError(f"Unexpected status types: {invalid_types}")

    for column in NUMERIC_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    numeric_missing_before = int(frame[NUMERIC_COLUMNS].isna().sum().sum())
    frame[NUMERIC_COLUMNS] = frame[NUMERIC_COLUMNS].fillna(0).clip(lower=0)
    frame[NUMERIC_COLUMNS] = frame[NUMERIC_COLUMNS].round().astype("int64")
    frame["status_published"] = pd.to_datetime(
        frame["status_published"], format="mixed", errors="coerce"
    )
    invalid_dates = int(frame["status_published"].isna().sum())
    frame = frame.dropna(subset=["status_published"]).copy()

    reaction_parts = [
        "num_likes",
        "num_loves",
        "num_wows",
        "num_hahas",
        "num_sads",
        "num_angrys",
    ]
    frame["reaction_components_total"] = frame[reaction_parts].sum(axis=1)
    frame["reaction_count_gap"] = (
        frame["num_reactions"] - frame["reaction_components_total"]
    )
    frame["total_engagement"] = (
        frame["num_reactions"] + frame["num_comments"] + frame["num_shares"]
    )
    frame["like_to_comment_ratio"] = safe_divide(
        frame["num_likes"], frame["num_comments"]
    )
    frame["share_to_engagement_ratio"] = safe_divide(
        frame["num_shares"], frame["total_engagement"]
    )
    frame["positive_reaction_percentage"] = 100 * safe_divide(
        frame["num_likes"] + frame["num_loves"] + frame["num_wows"],
        frame["reaction_components_total"],
    )
    frame["negative_reaction_percentage"] = 100 * safe_divide(
        frame["num_sads"] + frame["num_angrys"],
        frame["reaction_components_total"],
    )
    frame["posting_hour"] = frame["status_published"].dt.hour
    frame["day_of_week"] = frame["status_published"].dt.day_name()
    frame["month"] = frame["status_published"].dt.to_period("M").astype(str)
    frame["week_number"] = frame["status_published"].dt.isocalendar().week.astype(int)
    frame["is_weekend"] = frame["status_published"].dt.dayofweek.ge(5)
    frame["time_of_day"] = pd.cut(
        frame["posting_hour"],
        bins=[-1, 5, 11, 16, 20, 23],
        labels=["Overnight", "Morning", "Afternoon", "Evening", "Night"],
    ).astype(str)
    frame["engagement_category"] = pd.qcut(
        frame["total_engagement"].rank(method="first"),
        q=3,
        labels=["Low", "Medium", "High"],
    ).astype(str)

    q1 = float(frame["total_engagement"].quantile(0.25))
    q3 = float(frame["total_engagement"].quantile(0.75))
    iqr = q3 - q1
    outlier_threshold = q3 + 1.5 * iqr
    frame["engagement_outlier"] = frame["total_engagement"] > outlier_threshold
    frame = frame.sort_values("status_published").reset_index(drop=True)

    audit = {
        "initial_rows": initial_rows,
        "initial_columns": initial_columns,
        "empty_columns_removed": empty_columns,
        "duplicate_rows_removed": duplicate_rows,
        "duplicate_ids_removed": duplicate_ids,
        "numeric_missing_values_imputed": numeric_missing_before,
        "invalid_dates_removed": invalid_dates,
        "final_rows": int(len(frame)),
        "final_columns": int(frame.shape[1]),
        "outlier_method": "Upper Tukey fence on total_engagement",
        "outlier_threshold": outlier_threshold,
        "outlier_count": int(frame["engagement_outlier"].sum()),
        "reaction_gap_nonzero_rows": int(frame["reaction_count_gap"].ne(0).sum()),
    }
    validate_processed(frame)
    return frame, audit


def validate_processed(frame: pd.DataFrame) -> None:
    """Validate invariants used by downstream analysis."""

    required = {
        "total_engagement",
        "share_to_engagement_ratio",
        "posting_hour",
        "engagement_category",
    }
    if missing := required.difference(frame.columns):
        raise ValueError(f"Processed data missing features: {sorted(missing)}")
    if frame["status_id"].duplicated().any():
        raise ValueError("Processed data contains duplicate status IDs")
    if frame[NUMERIC_COLUMNS].isna().any().any():
        raise ValueError("Processed numeric data contain missing values")
    if (frame[NUMERIC_COLUMNS] < 0).any().any():
        raise ValueError("Processed engagement counts contain negative values")


def summarize_engagement(frame: pd.DataFrame) -> dict[str, Any]:
    """Calculate verified descriptive results for reports and dashboards."""

    by_type = (
        frame.groupby("status_type", observed=True)
        .agg(
            posts=("status_id", "count"),
            mean_reactions=("num_reactions", "mean"),
            median_reactions=("num_reactions", "median"),
            mean_comments=("num_comments", "mean"),
            mean_shares=("num_shares", "mean"),
            mean_total_engagement=("total_engagement", "mean"),
            median_total_engagement=("total_engagement", "median"),
        )
        .round(3)
        .sort_values("mean_total_engagement", ascending=False)
    )
    correlations = frame[
        ["num_reactions", "num_comments", "num_shares", "total_engagement"]
    ].corr(method="spearman")
    top = frame.nlargest(10, "total_engagement")[
        [
            "status_id",
            "status_type",
            "status_published",
            "num_reactions",
            "num_comments",
            "num_shares",
            "total_engagement",
        ]
    ]
    hour = (
        frame.groupby("posting_hour")
        .agg(
            posts=("status_id", "count"),
            median_engagement=("total_engagement", "median"),
        )
        .reset_index()
    )
    best_hour_row = hour.loc[hour["median_engagement"].idxmax()]
    return {
        "rows": int(len(frame)),
        "columns": int(frame.shape[1]),
        "date_min": frame["status_published"].min().isoformat(),
        "date_max": frame["status_published"].max().isoformat(),
        "total_reactions": int(frame["num_reactions"].sum()),
        "total_comments": int(frame["num_comments"].sum()),
        "total_shares": int(frame["num_shares"].sum()),
        "total_engagement": int(frame["total_engagement"].sum()),
        "median_engagement": float(frame["total_engagement"].median()),
        "mean_engagement": float(frame["total_engagement"].mean()),
        "outlier_count": int(frame["engagement_outlier"].sum()),
        "post_type_counts": {
            key: int(value)
            for key, value in frame["status_type"].value_counts().items()
        },
        "by_type": by_type.reset_index().to_dict(orient="records"),
        "spearman_correlations": correlations.round(4).to_dict(),
        "top_posts": top.assign(
            status_published=top["status_published"].astype(str)
        ).to_dict(orient="records"),
        "best_median_posting_hour": int(best_hour_row["posting_hour"]),
        "best_median_posting_hour_value": float(best_hour_row["median_engagement"]),
        "top_post_type_by_mean_engagement": str(by_type.index[0]),
        "top_post_type_mean_engagement": float(
            by_type.iloc[0]["mean_total_engagement"]
        ),
        "note": (
            "No reach or impression denominator exists, so the project does not "
            "mislabel total engagement as an engagement rate."
        ),
    }
