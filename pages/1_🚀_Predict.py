"""
pages/1_🚀_Predict.py
Core prediction page: vehicle form -> ML prediction -> Pexels image ->
prediction card (confidence, rating, verdict) -> currency -> PDF report -> history.
"""

import streamlit as st

from utils.theme import apply_theme, logo, page_header, card_open, card_close
from utils.data import load_model, load_data, build_input_row, predict_price, market_verdict, confidence_score
from utils.images import get_car_image
from utils.currency import format_amount, RATES
from utils.pdf import generate_pdf_report
from utils.history import add_record


st.set_page_config(page_title="Predict | LuxeCar", page_icon="🚀", layout="wide")
apply_theme()

with st.sidebar:
    logo()
    currency = st.selectbox("💱 Currency", list(RATES.keys()), index=0)

page_header("PREDICTION ENGINE", "ESTIMATE YOUR CAR'S VALUE", "Fill in the vehicle details below")

try:
    model = load_model()
    df = load_data()
except Exception as e:
    st.error(f"تعذر تحميل الموديل أو البيانات: {e}")
    st.stop()

if "predicted" not in st.session_state:
    st.session_state.predicted = False

left, right = st.columns([1.4, 1], gap="large")

# ==================================================
# LEFT: Vehicle Information form
# ==================================================
with left:
    card_open("🚘 VEHICLE INFORMATION")
    c1, c2 = st.columns(2)
    with c1:
        brand = st.selectbox("Brand", sorted(df["brand"].unique()))
        mileage = st.slider("Mileage (km/L)", float(df["mileage_kmpl"].min()), float(df["mileage_kmpl"].max()), 18.0)
        fuel = st.selectbox("Fuel Type", sorted(df["fuel_type"].unique()))
        owner = st.selectbox("Owner Count", sorted(df["owner_count"].unique()))
        service = st.selectbox("Service History", sorted(df["service_history"].unique()))
    with c2:
        year = st.slider("Manufacturing Year", int(df["make_year"].min()), int(df["make_year"].max()), 2020)
        engine = st.slider("Engine Capacity (CC)", int(df["engine_cc"].min()), int(df["engine_cc"].max()), 1800)
        transmission = st.selectbox("Transmission", sorted(df["transmission"].unique()))
        color = st.selectbox("Color", sorted(df["color"].unique()))
        accidents = st.selectbox("Accidents Reported", sorted(df["accidents_reported"].unique()))

    insurance = st.selectbox("Insurance Valid", sorted(df["insurance_valid"].unique()))

    st.markdown("<br>", unsafe_allow_html=True)
    go = st.button("🚀 PREDICT PRICE", use_container_width=True)
    card_close()

# ==================================================
# Run prediction
# ==================================================
if go:
    input_row = build_input_row(brand, year, mileage, engine, fuel, owner,
                                 transmission, color, service, accidents, insurance)
    with st.spinner("Analyzing vehicle & running the model..."):
        price = predict_price(model, input_row)
        image_url = get_car_image(brand, color, year)

        # market average for this brand, for the verdict badge
        seg = df[df["brand"] == brand]
        market_avg = seg["price_usd"].mean() if "price_usd" in df.columns and not seg.empty else price
        verdict, badge_class = market_verdict(price, market_avg)
        conf = confidence_score(model, df)
        stars_n = max(1, min(5, round((conf / 100) * 5)))
        rating_str = "★" * stars_n + "☆" * (5 - stars_n)

    st.session_state.predicted = True
    st.session_state.pred_price = price
    st.session_state.pred_image = image_url
    st.session_state.pred_verdict = verdict
    st.session_state.pred_badge = badge_class
    st.session_state.pred_conf = conf
    st.session_state.pred_rating = rating_str
    st.session_state.pred_details = {
        "Brand": brand, "Year": year, "Mileage (km/L)": mileage, "Engine (CC)": engine,
        "Fuel": fuel, "Transmission": transmission, "Owner Count": owner, "Color": color,
        "Service History": service, "Accidents Reported": accidents, "Insurance Valid": insurance,
    }

    add_record({
        "brand": brand, "year": year, "mileage": mileage, "engine_cc": engine,
        "fuel": fuel, "transmission": transmission, "owner_count": owner, "color": color,
        "service_history": service, "accidents": accidents, "insurance": insurance,
        "predicted_price_usd": round(price, 2), "verdict": verdict,
    })

# ==================================================
# RIGHT: Image + Prediction card (only after clicking Predict)
# ==================================================
with right:
    if st.session_state.get("predicted"):
        if st.session_state.pred_image:
            st.markdown(
                f"""
                <div style="border-radius:18px;overflow:hidden;border:1px solid rgba(212,175,55,0.4);
                            box-shadow:0 0 30px rgba(212,175,55,0.25); margin-bottom:18px;">
                    <img src="{st.session_state.pred_image}" style="width:100%;display:block;">
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("No image found (add a PEXELS_API_KEY in .streamlit/secrets.toml to enable photos).")

        price_fmt = format_amount(st.session_state.pred_price, currency)

        card_open("💰 PREDICTION RESULT")
        st.markdown(
            f"""
            <div style="text-align:center;">
                <div style="font-family:'Cinzel',serif;font-weight:900;font-size:40px;color:#FFD700;
                            text-shadow:0 0 18px rgba(255,215,0,0.5);">{price_fmt}</div>
                <div class="stars">{st.session_state.pred_rating}</div>
                <div style="margin-top:10px;">
                    <span class="badge {st.session_state.pred_badge}">{st.session_state.pred_verdict}</span>
                </div>
                <div style="margin-top:14px;color:#B9AE8C;font-size:13px;">
                    Model Confidence: <b style="color:#FFD700;">{st.session_state.pred_conf}%</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        card_close()

        # PDF download
        pdf_buffer = generate_pdf_report(
            details=st.session_state.pred_details,
            predicted_price=price_fmt,
            rating=st.session_state.pred_rating,
            verdict=st.session_state.pred_verdict,
            image_url=st.session_state.pred_image,
        )
        st.download_button(
            "📄 Download PDF Report",
            data=pdf_buffer,
            file_name="luxecar_valuation_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        card_open("💰 PREDICTION RESULT")
        st.write("Fill in the vehicle details and click **PREDICT PRICE** to see the estimated value, "
                 "a matching photo, and a downloadable PDF report.")
        card_close()
