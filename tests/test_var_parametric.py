import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from risk.var_parametric import parametric_var

# Basic correctness (known value)
def test_parametric_var_known_value():
    mu = 0.0
    sigma = 0.02
    alpha = 0.05

    var = parametric_var(mu, sigma, alpha)

    expected = mu + sigma * (-1.6448536269514729)  # norm.ppf(0.05)

    assert np.isclose(var, expected, atol=1e-6)

# Sign check (VaR should be negative)
def test_parametric_var_negative():
    mu = 0.001
    sigma = 0.02

    var = parametric_var(mu, sigma, alpha=0.05)

    assert var < 0

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

    assert np.isclose(violations, alpha, atol=0.01)