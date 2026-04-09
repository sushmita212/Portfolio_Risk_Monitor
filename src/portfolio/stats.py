import numpy as np

def portfolio_mean_std(df_returns, weights):
    """
    Returns portfolio mean and standard deviation
    using covariance matrix approach.
    """
    weights = np.array(weights)

    if len(weights) != df_returns.shape[1]:
        raise ValueError("Weights must match number of assets")

    mu = df_returns.mean()
    cov = df_returns.cov()

    port_mu = weights @ mu
    port_sigma = np.sqrt(weights @ cov @ weights)

    return port_mu, port_sigma