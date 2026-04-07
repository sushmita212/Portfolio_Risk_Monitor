import pandas as pd
import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from risk.var_historical import historical_var

def test_historical_var_basic():

    returns = pd.Series([-0.05, -0.02, -0.01, 0.01, 0.02])

    var = historical_var(returns, alpha=0.2)

    assert np.isclose(var, -0.026, atol=1e-6)

def test_var_confidence_levels():

    returns = pd.Series([-0.05, -0.03, -0.02, -0.01, 0.01])

    var_5 = historical_var(returns, alpha=0.05)
    var_20 = historical_var(returns, alpha=0.2)

    assert var_5 <= var_20

def test_var_violation_rate():

    # generate synthetic returns
    # normal distribution not required, but is convenient for testing
    np.random.seed(0)
    returns = pd.Series(np.random.normal(0, 0.02, 10000))

    alpha = 0.05
    var = historical_var(returns, alpha)

    # count fraction of violations
    violations = (returns < var).mean()

    # check it's close to alpha
    # loose tolerance avoids flaky test due to randomness
    assert abs(violations - alpha) < 0.01