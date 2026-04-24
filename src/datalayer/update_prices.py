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

# ASSETS = [
#     "SPY", "QQQ", "IWM", "XLF",
#     "XLK", "XLE", "TLT", "LQD",
#     "GLD", "SLV", "VNQ", "XOM"
# ]
ASSETS = ["SPY"]

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
        f.write(json.dumps(entry, indent=2) + "\n")

def get_csv_path(symbol):
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, f"{symbol}.csv")

# -----------------------------
# Main refresh logic
# -----------------------------
def refresh_assets():
    metadata = load_metadata()

    log_entry = {
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "assets": {},
        "summary": {
            "refreshed": [],
            "skipped": [],
            "errors": []
        }
    }

    for symbol in ASSETS:
        try:
            last_refresh = metadata.get(symbol, {}).get("last_refresh")

            # Safe incremental start
            start = pd.to_datetime(last_refresh, utc=True) if last_refresh else None
            end = datetime.now(timezone.utc)

            df_new = fetch_prices(symbol, start=start, end=end)

            csv_path = get_csv_path(symbol)
            file_exists = os.path.exists(csv_path)

            # Append or create
            if file_exists:
                df_new.to_csv(csv_path, mode="a", header=False, index=False)
            else:
                df_new.to_csv(csv_path, index=False)

            # Update metadata
            metadata[symbol] = {
                "last_refresh": end.isoformat(),
                "rows": len(df_new)
            }

            # Log success
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

    save_metadata(metadata)
    append_log(log_entry)

    print("Refresh completed. Log appended.")

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    refresh_assets()