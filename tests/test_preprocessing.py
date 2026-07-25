import numpy as np

from src.config import RAW_CSV
from src.data_loader import load_facebook_data
from src.data_preprocessing import clean_and_engineer, safe_divide


def test_cleaning_removes_empty_columns_and_preserves_rows():
    processed, audit = clean_and_engineer(load_facebook_data(RAW_CSV))
    assert len(processed) == 7050
    assert audit["empty_columns_removed"] == [
        "Column1",
        "Column2",
        "Column3",
        "Column4",
    ]
    assert processed["status_id"].is_unique
    assert not processed.isna().any().any()
    assert (processed["total_engagement"] >= 0).all()


def test_safe_divide_handles_zero_denominator():
    import pandas as pd

    result = safe_divide(pd.Series([4, 3]), pd.Series([2, 0]))
    assert np.allclose(result, [2.0, 0.0])
