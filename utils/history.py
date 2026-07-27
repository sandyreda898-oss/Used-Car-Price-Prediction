"""
utils/history.py
Persists every prediction made in the app to a local CSV file so it
survives across reruns/sessions (data/history.csv).
"""

import os
import pandas as pd
from datetime import datetime

HISTORY_PATH = os.path.join("data", "history.csv")

COLUMNS = [
    "date", "brand", "year", "mileage", "engine_cc", "fuel", "transmission",
    "owner_count", "color", "service_history", "accidents", "insurance",
    "predicted_price_usd", "verdict",
]


def _ensure_file():
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    if not os.path.exists(HISTORY_PATH):
        pd.DataFrame(columns=COLUMNS).to_csv(HISTORY_PATH, index=False)


def add_record(record: dict):
    _ensure_file()
    record = {**record, "date": datetime.now().strftime("%Y-%m-%d %H:%M")}
    df = pd.read_csv(HISTORY_PATH)
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv(HISTORY_PATH, index=False)


def load_history() -> pd.DataFrame:
    _ensure_file()
    return pd.read_csv(HISTORY_PATH)


def clear_history():
    _ensure_file()
    pd.DataFrame(columns=COLUMNS).to_csv(HISTORY_PATH, index=False)
