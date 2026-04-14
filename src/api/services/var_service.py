import pandas as pd
import os

from src.risk.var_historical import historical_var
from src.features.returns import compute_log_returns


def compute_var(ticker: str, confidence_level: float):

    file_path = f"data/raw/{ticker}.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{ticker} not found")

    df = pd.read_csv(file_path, index_col="Date", parse_dates=True)

    returns = compute_log_returns(df)

    var_value = historical_var(
        returns=returns,
        alpha=1 - confidence_level,
    )

    return float(var_value)