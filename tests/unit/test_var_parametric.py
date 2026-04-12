import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))
from risk.var_parametric import parametric_var

# Basic correctness (known value)
def test_parametric_var_known_value():
    mu = 0.0
    sigma = 0.02
    alpha = 0.05

    var = parametric_var(mu, sigma, alpha)

    expected = mu + sigma * (-1.6448536269514729)  # norm.ppf(0.05)

    assert np.isclose(var, expected, atol=1e-6)

# Higher confidence → more extreme VaR
def test_parametric_var_confidence_levels():
    mu = 0.0
    sigma = 0.02

    var_95 = parametric_var(mu, sigma, alpha=0.05)
    var_99 = parametric_var(mu, sigma, alpha=0.01)

    assert var_99 < var_95

# Zero volatility → VaR should equal mean
def test_parametric_var_zero_volatility():
    mu = 0.001
    sigma = 0.0

    var = parametric_var(mu, sigma, alpha=0.05)

    assert var == mu

# Violation rate should match alpha
def test_parametric_var_violation_rate():
    np.random.seed(0)

    mu = 0.0
    sigma = 0.02
    alpha = 0.05

    returns = np.random.normal(mu, sigma, 10000)

    var = parametric_var(mu, sigma, alpha)

    violations = (returns < var).mean()
    
    # Under null hypothesis, violations ~ Binomial(n, alpha)
    # Standard error of proportion = sqrt(alpha(1-alpha)/n)
    # Use 3-sigma tolerance for statistical consistency check
    se = np.sqrt(alpha * (1 - alpha) / len(returns))
    tol = 3 * se
    assert abs(violations - alpha) < tol

# Higher volatility should lead to more negative VaR
def test_var_increases_with_volatility():
    mu = 0.0

    var_low = parametric_var(mu, 0.01, 0.05)
    var_high = parametric_var(mu, 0.02, 0.05)

    assert var_high < var_low