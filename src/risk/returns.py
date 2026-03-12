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
    return np.log(price_df[price_col] / price_df[price_col].shift(1)).dropna()