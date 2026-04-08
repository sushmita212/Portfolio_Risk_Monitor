import pandas as pd
import numpy as np

def compute_log_returns(df, price_col="Close"):
    """
    df: DataFrame with OHLCV data
    returns: Series of log returns
    """
    prices = df[price_col]
    returns = np.log(prices / prices.shift(1))
    return returns.dropna()

def build_returns_dataframe(price_data_dict):
    """
    price_data_dict: dict like { 'AAPL': df, 'SPY': df }

    returns: DataFrame with aligned returns
    """
    returns_dict = {}

    for ticker, df in price_data_dict.items():
        returns_dict[ticker] = compute_log_returns(df)

    df_returns = pd.DataFrame(returns_dict)

    # align dates & drop missing
    df_returns = df_returns.dropna()

    return df_returns