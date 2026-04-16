import pandas as pd
import os

from src.risk.var_historical import historical_var
from src.risk.var_parametric import parametric_var
from src.features.returns import compute_log_returns
from src.features.returns import build_returns_dataframe
from src.portfolio.portfolio import compute_portfolio_returns
from src.portfolio.portfolio_stats import portfolio_mean_std



def compute_var(ticker: str, confidence_level: float, method: str = "historical") -> float:

    file_path = f"data/raw/{ticker}.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{ticker} not found")

    df = pd.read_csv(file_path, index_col="Date", parse_dates=True)

    returns = compute_log_returns(df)

    if method == "historical":
        var_value = historical_var(
            returns=returns,
            alpha=1 - confidence_level,
        )
    elif method == "parametric":
        mu = returns.mean()
        sigma = returns.std()
        var_value = parametric_var(
            mu=mu,
            sigma=sigma,
            alpha=1 - confidence_level,
        )
    else:
        raise ValueError("Invalid method. Choose 'historical' or 'parametric'.")

    return float(var_value)

def compute_portfolio_var(tickers: list, weights: list, confidence_level: float, method: str = "historical") -> float:
    price_data = {}

    # Load price data for each ticker
    for ticker in tickers:
        file_path = f"data/raw/{ticker}.csv"
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{ticker} not found")
        df = pd.read_csv(file_path, index_col="Date", parse_dates=True)
        price_data[ticker] = df
    
    # Build returns dataframe
    df_returns = build_returns_dataframe(price_data)

    # Compute portfolio returns
    portfolio_returns = compute_portfolio_returns(df_returns, weights)

    if method == "historical":
        portfolio_var = historical_var(
            returns=portfolio_returns,
            alpha=1 - confidence_level,
        )
    elif method == "parametric":
        port_mu, port_sigma = portfolio_mean_std(df_returns, weights)
        portfolio_var = parametric_var(
            mu=port_mu,
            sigma=port_sigma,
            alpha=1 - confidence_level,
        )
    else:
        raise ValueError("Invalid method. Choose 'historical' or 'parametric'.")

    return portfolio_var