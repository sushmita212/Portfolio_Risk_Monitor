import pandas as pd
import numpy as np

def compute_log_returns(price_df, price_col="Close"):
    """
    Compute log returns from a single asset price series.

    Parameters
    ----------
    price_df : pd.DataFrame
        DataFrame with at least a 'Close' column
    price_col : str
        Column name for price (default 'Close')

    Returns
    -------
    pd.Series
        Log return series
    """
    price_df = price_df.sort_index()  # Ensure sorted by date
    return np.log(price_df[price_col] / price_df[price_col].shift(1)).dropna()


def build_returns_dataframe(price_data_dict, price_col="Close"):
    """
    price_data_dict: dict like { 'AAPL': df, 'SPY': df }

    returns: DataFrame with aligned returns
    """

    # Step 1: Build a price DataFrame (aligned at the price level)
    prices_dict = {}

    for ticker, df in price_data_dict.items():
        df = df.copy()

        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        prices_dict[ticker] = df[price_col]

    # Combine all price series into one DataFrame (THIS does alignment)
    df_prices = pd.DataFrame(prices_dict)

    # Step 2: Align prices (keep only common dates)
    df_prices = df_prices.dropna()

    # Step 3: Compute returns on aligned prices
    df_returns = np.log(df_prices / df_prices.shift(1)).dropna()

    return df_returns