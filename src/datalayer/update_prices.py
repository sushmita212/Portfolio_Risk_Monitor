import os
import pandas as pd
import json
from datetime import datetime, timezone
from downloader import fetch_prices

# -----------------------------
# Configuration
# -----------------------------
DATA_DIR = "data/raw"
METADATA_FILE = "data/metadata.json"
LOG_FILE = "logs/refresh.jsonl"

ASSETS = [
    "SPY", "QQQ", "IWM", "XLF",
    "XLK", "XLE", "TLT", "LQD",
    "GLD", "SLV", "VNQ", "XOM"
]
# ASSETS = ["SPY","QQQ"]

DEFAULT_START = "2000-01-01"

# -----------------------------
# Helpers
# -----------------------------
def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)

def append_log(entry):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")  # JSONL format

def get_csv_path(symbol):
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, f"{symbol}.csv")

# -----------------------------
# Main refresh logic
# -----------------------------
def refresh_assets():
    metadata = load_metadata()
    now = datetime.now(timezone.utc)

    log_entry = {
        "time_utc": now.isoformat(),
        "assets": {},
        "summary": {
            "refreshed": [],
            "skipped": [],
            "errors": []
        }
    }

    for symbol in ASSETS:
        try:
            csv_path = get_csv_path(symbol)

            # -----------------------------
            # Determine start date
            # -----------------------------
            if os.path.exists(csv_path):
                df_old = pd.read_csv(csv_path)
                df_old["Date"] = pd.to_datetime(df_old["Date"])

                if not df_old.empty:
                    last_date = df_old["Date"].max()
                    start = last_date + pd.Timedelta(days=1)
                else:
                    df_old = None
                    start = pd.to_datetime(DEFAULT_START)
            else:
                df_old = None
                start = pd.to_datetime(DEFAULT_START)

            # -----------------------------
            # EXPECTATION CHECK (skip)
            # -----------------------------
            if start.date() >= now.date():
                log_entry["assets"][symbol] = {
                    "status": "skipped",
                    "reason": "no new trading day"
                }
                log_entry["summary"]["skipped"].append(symbol)
                continue

            # -----------------------------
            # FETCH (raises if empty)
            # -----------------------------
            df_new = fetch_prices(symbol, start=start, end=now)

            # -----------------------------
            # MERGE + DEDUPE
            # -----------------------------
            if df_old is not None:
                df = pd.concat([df_old, df_new])
                df = df.drop_duplicates(subset=["Date"]).sort_values("Date")
            else:
                df = df_new

            # -----------------------------
            # SAVE
            # -----------------------------
            df.to_csv(csv_path, index=False)

            # -----------------------------
            # UPDATE METADATA
            # -----------------------------
            metadata[symbol] = {
                "last_refresh": now.isoformat(),
                "rows": len(df)
            }

            # -----------------------------
            # LOG SUCCESS
            # -----------------------------
            log_entry["assets"][symbol] = {
                "status": "refreshed",
                "rows_added": len(df_new)
            }
            log_entry["summary"]["refreshed"].append(symbol)


        except Exception as e:
            log_entry["assets"][symbol] = {
                "status": "error",
                "message": str(e)
            }
            log_entry["summary"]["errors"].append(symbol)

    # -----------------------------
    # Persist metadata + logs
    # -----------------------------
    save_metadata(metadata)
    append_log(log_entry)

    print("Refresh completed. Log appended.")


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    refresh_assets()