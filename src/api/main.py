from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator
from typing import Literal, List

from src.api.services.var_service import compute_var
from src.api.services.var_service import compute_portfolio_var

app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "ok"}


class VaRRequest(BaseModel):
    ticker: str
    confidence_level: float = Field(0.95, gt=0, lt=1)
    method: Literal["historical", "parametric"] = "historical"
    time_horizon: int = Field(1, gt=0)
    use_drift: bool = False


class PortfolioVaRRequest(BaseModel):
    tickers: List[str]
    weights: List[float]
    confidence_level: float = Field(0.95, gt=0, lt=1)
    method: Literal["historical", "parametric"] = "historical"
    time_horizon: int = Field(1, gt=0)
    use_drift: bool = False

    @model_validator(mode="after")
    def validate_portfolio_inputs(self):
        if len(self.tickers) == 0:
            raise ValueError("portfolio cannot be empty")
        
        if len(self.tickers) != len(self.weights):
            raise ValueError("tickers and weights must have the same length")

        if abs(sum(self.weights) - 1.0) > 1e-6:
            raise ValueError("weights must sum to 1")

        return self


@app.post("/var")
def compute_var_endpoint(request: VaRRequest):

    try:
        var_value = compute_var(
            ticker=request.ticker,
            confidence_level=request.confidence_level,
            method=request.method,
            time_horizon=request.time_horizon,
            use_drift=request.use_drift
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Ticker data not found")

    return {
        "ticker": request.ticker,
        "var": var_value,
        "confidence_level": request.confidence_level,
        "method": request.method,
        "time_horizon": request.time_horizon,
        "use_drift": request.use_drift
    }


@app.post("/portfolio/var")
def compute_portfolio_var_endpoint(request: PortfolioVaRRequest):

    try:
        var_value = compute_portfolio_var(
            tickers=request.tickers,
            weights=request.weights,
            confidence_level=request.confidence_level,
            method=request.method,
            time_horizon=request.time_horizon,
            use_drift=request.use_drift
        )

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="One or more tickers not found")

    return {
        "tickers": request.tickers,
        "weights": request.weights,
        "var": float(var_value),
        "confidence_level": request.confidence_level,
        "method": request.method,
        "time_horizon": request.time_horizon,
        "use_drift": request.use_drift
    }