import numpy as np

def portfolio_mean_std(df_returns, weights):
    """
    Returns portfolio mean and standard deviation
    using covariance matrix approach.
    """
    weights = np.array(weights)

    mu = df_returns.mean().values
    cov = df_returns.cov().values

    port_mu = weights @ mu
    port_sigma = np.sqrt(weights @ cov @ weights)

    return port_mu, port_sigma