import pandas as pd
import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from portfolio.portfolio import compute_portfolio_returns


# 1. Basic correctness test
def test_portfolio_returns_basic():
    df_returns = pd.DataFrame({
        "A": [0.01, 0.02],
        "B": [0.03, 0.04]
    })

    weights = [0.3, 0.7]

    result = compute_portfolio_returns(df_returns, weights)

    expected = pd.Series([
        0.3*0.01 + 0.7*0.03,
        0.3*0.02 + 0.7*0.04
    ])

    pd.testing.assert_series_equal(result, expected, check_names=False)

# 2. Single asset: Edge case
def test_single_asset():
    df_returns = pd.DataFrame({
        "A": [0.01, 0.02, 0.03]
    })

    weights = [1.0]

    result = compute_portfolio_returns(df_returns, weights)

    pd.testing.assert_series_equal(result, df_returns["A"], check_names=False)

# 3. Zero weights: Edge case
def test_zero_weights():
    df_returns = pd.DataFrame({
        "A": [0.01, 0.02, 0.03],
        "B": [0.02, 0.01, 0.00]
    })

    weights = [0.0, 0.0]

    result = compute_portfolio_returns(df_returns, weights)

    expected = pd.Series([0.0, 0.0, 0.0])

    pd.testing.assert_series_equal(result, expected, check_names=False)

# 4. Output Shape
def test_output_length():
    df_returns = pd.DataFrame({
        "A": [0.01, 0.02, 0.03],
        "B": [0.02, 0.01, 0.00]
    })

    weights = [0.5, 0.5]

    result = compute_portfolio_returns(df_returns, weights)

    assert len(result) == len(df_returns)


# 5. Coulumn order should matter
def test_column_order():
    df_returns = pd.DataFrame({
        "A": [0.01],
        "B": [0.03]
    })

    weights = [0.7, 0.3]

    result1 = compute_portfolio_returns(df_returns, weights)

    # swap columns
    df_returns_swapped = df_returns[["B", "A"]]

    result2 = compute_portfolio_returns(df_returns_swapped, weights)

    # results should differ → shows order matters
    assert not result1.equals(result2)