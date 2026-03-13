import numpy as np

def historical_var(returns, alpha=0.05):
    """
    Calculate historical Value at Risk (VaR).

    Parameters
    ----------
    returns : pd.Series
        Series of log returns
    alpha : float
        Tail probability (0.05 for 95% VaR)

    Returns
    -------
    float
        Historical VaR
    """
    
    return np.quantile(returns, alpha)