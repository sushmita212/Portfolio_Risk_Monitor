import pandas as pd
import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from features.returns import build_returns_dataframe

# 1. Correctness of columns
def test_columns():
    df = pd.DataFrame(
        {"Close": [100, 101, 102]},
        index=pd.date_range("2023-01-01", periods=3)
    )

    price_data = {"A": df, "B": df.copy()}

    df_returns = build_returns_dataframe(price_data)

    assert set(df_returns.columns) == {"A", "B"}


# 2. Output index is datetime
def test_datetime_index():
    df = pd.DataFrame(
        {"Close": [100, 101]},
        index=["2023-01-01", "2023-01-02"]
    )

    price_data = {"A": df}

    df_returns = build_returns_dataframe(price_data)

    assert isinstance(df_returns.index, pd.DatetimeIndex)


# 3. No NaNs after alignment
def test_no_nans():
    df = pd.DataFrame(
        {"Close": [100, 101, 102]},
        index=pd.date_range("2023-01-01", periods=3)
    )

    price_data = {"A": df}

    df_returns = build_returns_dataframe(price_data)

    assert df_returns.notna().all().all()

# 4. Alignment across assets (perfect alignment case)
def test_perfect_alignment():
    dates = pd.date_range("2023-01-01", periods=5)

    df1 = pd.DataFrame({"Close": [100, 101, 102, 103, 104]}, index=dates)
    df2 = pd.DataFrame({"Close": [200, 201, 202, 203, 204]}, index=dates)

    price_data = {"AAPL": df1, "SPY": df2}

    returns = build_returns_dataframe(price_data)

    expected_length = 4  # n - 1

    assert len(returns) == expected_length

# 5. Partial overlap case (only overlapping dates should be included)
def test_partial_overlap():
    df1 = pd.DataFrame({"Close": [100, 110, 120]}, index=pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]))
    df2 = pd.DataFrame({"Close": [200, 210, 220]}, index=pd.to_datetime(["2023-01-02", "2023-01-03", "2023-01-04"]))

    price_data = {"AAPL": df1, "SPY": df2}

    returns = build_returns_dataframe(price_data)

    # Only overlapping aligned dates contribute
    assert len(returns) == 1