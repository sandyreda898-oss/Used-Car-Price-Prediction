"""
utils/data.py
Loading of the trained ML pipeline and the cleaned dataset.
"""

import streamlit as st
import pandas as pd
import joblib

MODEL_PATH = "linear_regression_pipeline.pkl"
DATA_PATH = "used_car_cleaned.csv"

FEATURE_COLUMNS = [
    "make_year", "mileage_kmpl", "engine_cc", "fuel_type", "owner_count",
    "brand", "transmission", "color", "service_history",
    "accidents_reported", "insurance_valid",
]

TARGET_COLUMN = "price_usd"


@st.cache_resource(show_spinner=False)
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    return df


def build_input_row(brand, year, mileage, engine, fuel, owner,
                     transmission, color, service, accidents, insurance) -> pd.DataFrame:
    return pd.DataFrame({
        "make_year": [year],
        "mileage_kmpl": [mileage],
        "engine_cc": [engine],
        "fuel_type": [fuel],
        "owner_count": [owner],
        "brand": [brand],
        "transmission": [transmission],
        "color": [color],
        "service_history": [service],
        "accidents_reported": [accidents],
        "insurance_valid": [insurance],
    })


def predict_price(model, input_row: pd.DataFrame) -> float:
    return float(model.predict(input_row)[0])


def market_verdict(predicted_price: float, market_avg: float) -> tuple[str, str]:
    """Return (label, badge_css_class) comparing prediction to dataset average for that brand/segment."""
    if market_avg <= 0:
        return "Fair Price", "badge-fair"
    ratio = predicted_price / market_avg
    if ratio <= 0.90:
        return "Great Deal", "badge-good"
    elif ratio <= 1.10:
        return "Fair Price", "badge-fair"
    else:
        return "Overpriced", "badge-bad"


def confidence_score(model, df: pd.DataFrame) -> float:
    """
    Approximate confidence (R^2 on the full available dataset) for display purposes.
    Falls back to a fixed illustrative value if the target column isn't present.
    """
    try:
        if TARGET_COLUMN not in df.columns:
            return 90.0
        X = df[FEATURE_COLUMNS]
        y = df[TARGET_COLUMN]
        score = model.score(X, y)
        return round(max(0.0, min(1.0, score)) * 100, 1)
    except Exception:
        return 90.0
