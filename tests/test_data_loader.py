from src.config import RAW_CSV
from src.data_loader import REQUIRED_COLUMNS, load_facebook_data


def test_dataset_loads_with_required_schema():
    frame = load_facebook_data(RAW_CSV)
    assert frame.shape == (7050, 16)
    assert REQUIRED_COLUMNS.issubset(frame.columns)
    assert frame["status_id"].is_unique
