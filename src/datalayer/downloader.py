import pandas as pd
import yfinance as yf

def fetch_prices(symbol: str, start=None, end=None):

    df = yf.download(symbol, start="2000-01-01", end=end, progress=False)

    if df.empty:
        raise ValueError(f"No data returned for {symbol}")

    # -----------------------------
    # Fix MultiIndex (safe)
    # -----------------------------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    # -----------------------------
    # Drop bad rows (THIS FIXES YOUR NaT/SPY ROW)
    # -----------------------------
    df = df.dropna(subset=["Date"])

    # -----------------------------
    # Keep only expected columns
    # -----------------------------
    expected = ["Date", "Open", "High", "Low", "Close", "Volume"]
    df = df[[c for c in expected if c in df.columns]]

    # -----------------------------
    # Force numeric conversion (CRITICAL FIX)
    # -----------------------------
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # -----------------------------
    # Clean + sort
    # -----------------------------
    df = df.dropna(subset=["Close"])
    df = df.sort_values("Date").reset_index(drop=True)

    return df