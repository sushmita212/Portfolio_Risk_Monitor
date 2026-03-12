# src/data/update_prices.py
import os
import pandas as pd
import json
from datetime import datetime, timezone
from downloader import fetch_stooq  # your existing downloader.py function

# -----------------------------
# Configuration
# -----------------------------
DATA_DIR = "data/raw"
METADATA_FILE = "data/metadata.json"
LOG_FILE = "logs/refresh.jsonl"
ASSETS =  [
    "SPY.US", "QQQ.US", "IWM.US", "XLF.US",
    "XLK.US", "XLE.US", "TLT.US", "LQD.US",
    "GLD.US", "SLV.US", "VNQ.US", "XOM.US"
    ]  
REFRESH_INTERVAL_DAYS = 1  # intended refresh frequency

# -----------------------------
# Helper functions
# -----------------------------
def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_metadata(metadata):
    os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)

def append_log(entry):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry, indent=2) + "\n")

def save_csv(symbol, df):
    os.makedirs(DATA_DIR, exist_ok=True)
    csv_path = os.path.join(DATA_DIR, f"{symbol}.csv")
    df.to_csv(csv_path, index=False)
    return csv_path

# -----------------------------
# Main refresh logic
# -----------------------------
def refresh_assets():
    metadata = load_metadata()
    log_entry = {
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "refresh_interval_days": REFRESH_INTERVAL_DAYS,
        "assets": {},
        "summary": {"refreshed": [], "skipped": [], "errors": []}
    }

    for symbol in ASSETS:
        try:
            # Check last refresh to see if we need to skip
            last_refresh = metadata.get(symbol, {}).get("last_refresh")
            if last_refresh:
                last_refresh_dt = datetime.fromisoformat(last_refresh)
                delta_days = (datetime.now() - last_refresh_dt).days
                if delta_days < REFRESH_INTERVAL_DAYS:
                    log_entry["assets"][symbol] = {
                        "status": "skipped",
                        "reason": f"last refresh {last_refresh}, interval {REFRESH_INTERVAL_DAYS} days"
                    }
                    log_entry["summary"]["skipped"].append(symbol)
                    continue

            # Fetch new data
            df_new = fetch_stooq(symbol)

            # Load existing CSV if exists
            csv_path = os.path.join(DATA_DIR, f"{symbol}.csv")
            if os.path.exists(csv_path):
                df_old = pd.read_csv(csv_path)
                df_old['Date'] = pd.to_datetime(df_old['Date'])
                df_new['Date'] = pd.to_datetime(df_new['Date'])
                # Append only new rows
                df_append = df_new[df_new['Date'] > df_old['Date'].max()]
                if len(df_append) > 0:
                    df_append.to_csv(csv_path, mode='a', header=False, index=False)
                    rows_added = len(df_append)
                else:
                    rows_added = 0
            else:
                df_new.to_csv(csv_path, index=False)
                rows_added = len(df_new)

            # Update metadata
            metadata[symbol] = {
                "last_refresh": datetime.now().isoformat(),
                "rows": len(df_new)
            }

            # Update log
            status = "refreshed" if rows_added > 0 else "skipped"
            log_entry["assets"][symbol] = {
                "status": status,
                "rows_added": rows_added
            }
            log_entry["summary"][status].append(symbol)

        except Exception as e:
            log_entry["assets"][symbol] = {
                "status": "error",
                "message": str(e)
            }
            log_entry["summary"]["errors"].append(symbol)

    # Save updated metadata and log
    save_metadata(metadata)
    append_log(log_entry)
    print("Refresh completed. Log appended to", LOG_FILE)

# -----------------------------
# Run script
# -----------------------------
if __name__ == "__main__":
    refresh_assets()