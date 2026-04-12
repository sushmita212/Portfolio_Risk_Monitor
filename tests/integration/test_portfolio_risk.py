import pandas as pd
import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from features.returns import build_returns_dataframe
from portfolio.portfolio import compute_portfolio_returns
from portfolio.portfolio_stats import portfolio_mean_std
from risk.var_historical import historical_var
from risk.var_parametric import parametric_var


def test_portfolio_to_var():
    import pandas as pd
    import numpy as np

    # Create synthetic price data (3 assets)
    dates = pd.date_range("2026-01-01", periods=6)

    df1 = pd.DataFrame({
        "Close": [100, 102, 101, 103, 104, 105]
    }, index=dates)

    df2 = pd.DataFrame({
        "Close": [200, 198, 202, 204, 203, 205]
    }, index=dates)

    df3 = pd.DataFrame({
        "Close": [300, 303, 306, 309, 312, 315]
    }, index=dates)

    price_data = {"A": df1, "B": df2, "C": df3}

    weights = [0.5, 0.3, 0.2]

    # Pipeline
    df_returns = build_returns_dataframe(price_data)
    port_returns = compute_portfolio_returns(df_returns, weights)
    mu, sigma = portfolio_mean_std(df_returns, weights)

    var_hist = historical_var(port_returns, alpha=0.05)
    var_param = parametric_var(mu, sigma, alpha=0.05)


    # Assertions
    assert np.isfinite(var_hist)
    assert np.isfinite(var_param)


def test_parametric_vs_historical_consistency():
    returns = pd.DataFrame({
        "A": np.random.normal(0, 0.02, 10000),
        "B": np.random.normal(0, 0.02, 10000)
    })

    weights = [0.5, 0.5]

    port_returns = compute_portfolio_returns(returns, weights)
    mu, sigma = portfolio_mean_std(returns, weights)

    var_hist = historical_var(port_returns, alpha=0.05)
    var_param = parametric_var(mu, sigma, alpha=0.05)

    assert np.isclose(var_hist, var_param, atol=0.005)
