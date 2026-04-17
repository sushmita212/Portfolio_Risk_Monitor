import numpy as np

def historical_var(returns, alpha=0.05, time_horizon: int = 1):
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
    if time_horizon > 1:
        returns = returns.rolling(time_horizon).sum().dropna()

    returns = np.asarray(returns)
    
    return np.quantile(returns, alpha)