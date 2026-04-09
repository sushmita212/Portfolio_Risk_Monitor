import pandas as pd
import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from portfolio.portfolio_stats import portfolio_mean_std

# 1. Basic correctness test
def test_portfolio_mean():
    df = pd.DataFrame({
        "A": [0.01, 0.02],
        "B": [0.03, 0.04]
    })
    weights = [0.5, 0.5]

    mu, _ = portfolio_mean_std(df, weights)

    expected_mu = 0.5 * df["A"].mean() + 0.5 * df["B"].mean()

    assert np.isclose(mu, expected_mu)

def test_portfolio_std():
    df = pd.DataFrame({
        "A": [0.01, 0.02],
        "B": [0.03, 0.04]
    })
    weights = [0.5, 0.5]

    _, sigma = portfolio_mean_std(df, weights)

    cov = df.cov().values
    expected_sigma = np.sqrt(np.array(weights) @ cov @ np.array(weights))

    assert np.isclose(sigma, expected_sigma)

# 2. Perfect correlation: Edge case
def test_perfect_correlation():
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [2, 4, 6]  # perfectly correlated with A
    })

    weights = [0.5, 0.5]

    _, sigma = portfolio_mean_std(df, weights)

    # With perfect correlation, sigma should behave like a scaled single asset
    assert sigma > 0

# 3. Single asset: Edge case
def test_single_asset():
    df = pd.DataFrame({
        "A": [0.01, 0.02, 0.03]
    })

    weights = [1.0]

    mu, sigma = portfolio_mean_std(df, weights)

    assert np.isclose(mu, df["A"].mean())
    assert np.isclose(sigma, df["A"].std())


# 4. Zero weights sanity check
def test_zero_weights():
    df = pd.DataFrame({
        "A": [0.01, 0.02],
        "B": [0.03, 0.04]
    })

    weights = [0.0, 0.0]

    mu, sigma = portfolio_mean_std(df, weights)

    assert np.isclose(mu, 0.0)
    assert np.isclose(sigma, 0.0)
