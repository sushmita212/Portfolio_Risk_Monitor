import numpy as np
import pandas as pd

def compute_portfolio_returns(df_returns, weights):
    """
    df_returns: DataFrame (rows = time, cols = assets)
    weights: list or array of weights

    returns: Series of portfolio returns
    """
    weights = np.array(weights)
    return df_returns @ weights