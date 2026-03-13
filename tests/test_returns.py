import pandas as pd
import numpy as np

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from risk.returns import compute_log_returns

def test_log_returns_basic():

    df = pd.DataFrame({
        "Close": [100, 110]
    })

    returns = compute_log_returns(df)

    expected = np.log(110/100)

    assert np.isclose(returns.iloc[0], expected)


def test_log_returns_length():

    df = pd.DataFrame({
        "Close": [100, 101, 102, 103]
    })

    returns = compute_log_returns(df)

    assert len(returns) == 3

def test_log_returns_no_nan():

    df = pd.DataFrame({
        "Close": [100, 101, 102]
    })

    returns = compute_log_returns(df)

    assert returns.isna().sum() == 0