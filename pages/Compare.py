"""
pages/4_⚖️_Compare.py
Side-by-side comparison of two vehicles, each predicted independently.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.theme import apply_theme, logo, page_header, card_open, card_close
from utils.data import load_model, load_data, build_input_row, predict_price

st.set_page_config(page_title="Compare | LuxeCar", page_icon="⚖️", layout="wide")
apply_theme()

with st.sidebar:
    logo()

try:
    model = load_model()
    df = load_data()
except Exception as e:
    st.error(f"تعذر تحميل الموديل أو البيانات: {e}")
    st.stop()

page_header("COMPARE CARS", "SIDE-BY-SIDE VALUATION", "Compare two vehicles head to head")

PLOTLY_TEMPLATE = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E5E7EB")


def vehicle_form(label: str, key_prefix: str):
    card_open(f"🚘 {label}")
    brand = st.selectbox("Brand", sorted(df["brand"].unique()), key=f"{key_prefix}_brand")
    year = st.slider("Year", int(df["make_year"].min()), int(df["make_year"].max()), 2020, key=f"{key_prefix}_year")
    mileage = st.slider("Mileage (km/L)", float(df["mileage_kmpl"].min()), float(df["mileage_kmpl"].max()), 18.0, key=f"{key_prefix}_mileage")
    engine = st.slider("Engine (CC)", int(df["engine_cc"].min()), int(df["engine_cc"].max()), 1800, key=f"{key_prefix}_engine")
    fuel = st.selectbox("Fuel Type", sorted(df["fuel_type"].unique()), key=f"{key_prefix}_fuel")
    transmission = st.selectbox("Transmission", sorted(df["transmission"].unique()), key=f"{key_prefix}_trans")
    owner = st.selectbox("Owner Count", sorted(df["owner_count"].unique()), key=f"{key_prefix}_owner")
    color = st.selectbox("Color", sorted(df["color"].unique()), key=f"{key_prefix}_color")
    service = st.selectbox("Service History", sorted(df["service_history"].unique()), key=f"{key_prefix}_service")
    accidents = st.selectbox("Accidents Reported", sorted(df["accidents_reported"].unique()), key=f"{key_prefix}_acc")
    insurance = st.selectbox("Insurance Valid", sorted(df["insurance_valid"].unique()), key=f"{key_prefix}_ins")
    card_close()
    return dict(brand=brand, year=year, mileage=mileage, engine=engine, fuel=fuel,
                transmission=transmission, owner=owner, color=color, service=service,
                accidents=accidents, insurance=insurance)


c1, c2 = st.columns(2)
with c1:
    car_a = vehicle_form("Car A", "a")
with c2:
    car_b = vehicle_form("Car B", "b")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("⚖️ COMPARE PRICES", use_container_width=True):
    row_a = build_input_row(car_a["brand"], car_a["year"], car_a["mileage"], car_a["engine"], car_a["fuel"],
                             car_a["owner"], car_a["transmission"], car_a["color"], car_a["service"],
                             car_a["accidents"], car_a["insurance"])
    row_b = build_input_row(car_b["brand"], car_b["year"], car_b["mileage"], car_b["engine"], car_b["fuel"],
                             car_b["owner"], car_b["transmission"], car_b["color"], car_b["service"],
                             car_b["accidents"], car_b["insurance"])

    price_a = predict_price(model, row_a)
    price_b = predict_price(model, row_b)

    r1, r2 = st.columns(2)
    with r1:
        card_open(f"💰 {car_a['brand']} — Result")
        st.markdown(f"<div style='font-family:Cinzel,serif;font-size:32px;color:#FFD700;text-align:center;'>${price_a:,.0f}</div>", unsafe_allow_html=True)
        card_close()
    with r2:
        card_open(f"💰 {car_b['brand']} — Result")
        st.markdown(f"<div style='font-family:Cinzel,serif;font-size:32px;color:#FFD700;text-align:center;'>${price_b:,.0f}</div>", unsafe_allow_html=True)
        card_close()

    card_open("📊 Comparison Table")
    comp = pd.DataFrame({
        "Attribute": ["Predicted Price", "Year", "Mileage (km/L)", "Engine (CC)", "Fuel", "Transmission"],
        "Car A": [f"${price_a:,.0f}", car_a["year"], car_a["mileage"], car_a["engine"], car_a["fuel"], car_a["transmission"]],
        "Car B": [f"${price_b:,.0f}", car_b["year"], car_b["mileage"], car_b["engine"], car_b["fuel"], car_b["transmission"]],
    })
    st.dataframe(comp, use_container_width=True, hide_index=True)
    card_close()

    card_open("📈 Predicted Price — Bar Comparison")
    bar_df = pd.DataFrame({"Car": [f"A: {car_a['brand']}", f"B: {car_b['brand']}"], "Price": [price_a, price_b]})
    fig = px.bar(bar_df, x="Car", y="Price", color="Car", color_discrete_sequence=["#D4AF37", "#FFD700"])
    fig.update_layout(**PLOTLY_TEMPLATE, height=340, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    card_close()
