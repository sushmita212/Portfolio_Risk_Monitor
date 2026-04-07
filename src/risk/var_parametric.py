from scipy.stats import norm

def parametric_var(mu, sigma, alpha=0.05):
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
    return mu + sigma * z