"""
utils/currency.py
Simple static currency conversion (base = USD).
Update RATES to plug in a live FX API if desired.
"""

RATES = {
    "USD": {"symbol": "$", "rate": 1.0},
    "EUR": {"symbol": "€", "rate": 0.92},
    "EGP": {"symbol": "E£", "rate": 48.5},
}


def convert(amount_usd: float, currency: str) -> float:
    info = RATES.get(currency, RATES["USD"])
    return amount_usd * info["rate"]


def symbol(currency: str) -> str:
    return RATES.get(currency, RATES["USD"])["symbol"]


def format_amount(amount_usd: float, currency: str) -> str:
    return f"{symbol(currency)}{convert(amount_usd, currency):,.0f}"
