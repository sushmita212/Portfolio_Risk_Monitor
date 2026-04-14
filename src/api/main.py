from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.api.services.var_service import compute_var

app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "ok"}


class VaRRequest(BaseModel):
    ticker: str
    confidence_level: float = 0.95


@app.post("/var")
def compute_var_endpoint(request: VaRRequest):

    try:
        var_value = compute_var(
            ticker=request.ticker,
            confidence_level=request.confidence_level,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Ticker data not found")

    return {
        "ticker": request.ticker,
        "var": var_value,
        "confidence_level": request.confidence_level,
    }