import pandas as pd
import os

DATA_DIR = "data/raw"
ASSETS = [
    "SPY.US", "QQQ.US", "IWM.US", "XLF.US",
    "XLK.US", "XLE.US", "TLT.US", "LQD.US",
    "GLD.US", "SLV.US", "VNQ.US", "XOM.US"
    ] 

def fetch_stooq(symbol: str) -> pd.DataFrame:
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"
    df = pd.read_csv(url, on_bad_lines='skip')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    return df

def save_csv(symbol: str, df: pd.DataFrame):
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(os.path.join(DATA_DIR, f"{symbol}.csv"), index=False)

if __name__ == "__main__":
    for symbol in ASSETS:
        df = fetch_stooq(symbol)
        save_csv(symbol, df)
        print(f"{symbol} saved with {len(df)} rows")