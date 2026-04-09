import numpy as np
import pandas as pd

def compute_portfolio_returns(df_returns, weights):
    """
    df_returns: DataFrame (rows = time, cols = assets)
    weights: list or array of weights

    returns: Series of portfolio returns
    """
    weights = np.array(weights)

    if len(weights) != df_returns.shape[1]:
        raise ValueError("Length of weights must match number of assets (columns in df_returns)")
    
    return df_returns @ weights