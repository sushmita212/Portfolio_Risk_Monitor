from scipy.stats import norm
import numpy as np

def parametric_var(mu: float,
    sigma: float,
    alpha: float = 0.05,
    time_horizon: int = 1,
    use_drift: bool = False):
    """
    Compute parametric VaR given mean and standard deviation.

    Parameters:
        mu (float): portfolio mean return
        sigma (float): portfolio standard deviation
        alpha (float): tail probability (e.g., 0.05 for 95% VaR)

    Returns:
        float: VaR (can be negative)
    """
    z = norm.ppf(alpha)  # left-tail quantile (negative)
   
    if use_drift:
        mu_t = mu * time_horizon
    else:
        mu_t = 0.0

    sigma_t = sigma * np.sqrt(time_horizon)

    var = mu_t + sigma_t * z

    return var