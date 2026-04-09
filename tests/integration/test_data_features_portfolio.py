import pandas as pd
import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from features.returns import build_returns_dataframe
from portfolio.portfolio import compute_portfolio_returns
from portfolio.portfolio_stats import portfolio_mean_std

def test_data_features_portfolio_returns():
    # Create synthetic price data for 3 assets
    dates = pd.date_range("2023-01-01", periods=5)
    df1 = pd.DataFrame({"Close": [100, 101, 102, 103, 104]}, index=dates)
    df2 = pd.DataFrame({"Close": [200, 201, 202, 203, 204]}, index=dates)
    df3 = pd.DataFrame({"Close": [300, 301, 302, 303, 304]}, index=dates)

    price_data = {"A": df1, "B": df2, "C": df3}

    # Build returns dataframe
    df_returns = build_returns_dataframe(price_data)

    # Define portfolio weights
    weights = [0.5, 0.3, 0.2]

    # Compute portfolio returns
    portfolio_returns = compute_portfolio_returns(df_returns, weights)

    # Check that portfolio returns is a Series with the same index as df_returns
    assert isinstance(portfolio_returns, pd.Series)
    assert portfolio_returns.index.equals(df_returns.index)

def test_data_features_portfolio_stats():
    # Create synthetic returns data for 3 assets
    dates = pd.date_range("2023-01-01", periods=5)
    df_returns = pd.DataFrame({
        "A": [0.01, 0.02, 0.015, 0.03, 0.025],
        "B": [0.005, 0.01, 0.007, 0.012, 0.009],
        "C": [0.02, 0.025, 0.03, 0.035, 0.04]
    }, index=dates)

    # Define portfolio weights
    weights = [0.5, 0.3, 0.2]

    # Compute portfolio mean and std
    port_mu, port_sigma = portfolio_mean_std(df_returns, weights)

    # Check that mean and std are floats
    assert isinstance(port_mu, float)
    assert isinstance(port_sigma, float)

    # Check that mean is between min and max of asset means
    asset_means = df_returns.mean()
    assert port_mu >= asset_means.min() and port_mu <= asset_means.max()

    # Check correctness of mean calculation (weighted average of asset means)
    expected = (df_returns * weights).sum(axis=1).mean()
    assert np.isclose(port_mu, expected)

def test_real_data_features_portfolio():
    # Load real price data for 3 assets
    df1 = pd.read_csv("data/raw/QQQ.US.csv", index_col="Date", parse_dates=True)
    df2 = pd.read_csv("data/raw/SPY.US.csv", index_col="Date", parse_dates=True)
    df3 = pd.read_csv("data/raw/XOM.US.csv", index_col="Date", parse_dates=True)

    price_data = {"QQQ": df1, "SPY": df2, "XOM": df3}

    # Build returns dataframe
    df_returns = build_returns_dataframe(price_data)

    # Define portfolio weights
    weights = [0.5, 0.3, 0.2]

    # Compute portfolio returns
    portfolio_returns = compute_portfolio_returns(df_returns, weights)

    # Compute portfolio mean and std
    port_mu, port_sigma = portfolio_mean_std(df_returns, weights)

    # Check that mean and std are reasonable (not NaN or infinite)
    assert np.isfinite(port_mu)
    assert np.isfinite(port_sigma)
    assert port_sigma >= 0