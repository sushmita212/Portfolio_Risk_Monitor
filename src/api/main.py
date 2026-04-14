from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from risk.var_historical import historical_var
from features.returns import compute_log_returns

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}


class VaRRequest(BaseModel):
    portfolio_id: str
    confidence_level: float = 0.95


@app.post("/var")
def compute_var_endpoint(request: VaRRequest):
    df = pd.read_csv(f"data/raw/{request.portfolio_id}.csv", index_col="Date", parse_dates=True)
    returns = compute_log_returns(df)

    var_value = historical_var(
        returns=returns,
        alpha=1 - request.confidence_level,
    )

    return {
        "portfolio_id": request.portfolio_id,
        "var": var_value,
        "confidence_level": request.confidence_level,
    }