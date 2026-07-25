"""Input loading and schema validation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "status_id",
    "status_type",
    "status_published",
    "num_reactions",
    "num_comments",
    "num_shares",
    "num_likes",
    "num_loves",
    "num_wows",
    "num_hahas",
    "num_sads",
    "num_angrys",
}


def load_facebook_data(path: Path) -> pd.DataFrame:
    """Load the Facebook dataset and fail clearly on a schema mismatch."""

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. See data/README.md for download instructions."
        )
    frame = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    return frame
