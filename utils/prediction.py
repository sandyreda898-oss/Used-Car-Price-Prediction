import streamlit as st
import pandas as pd
import joblib
import os

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Predict Car Price",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Used Car Price Prediction")
st.write("Fill in the car details below to estimate its market value.")

# -----------------------------
# Load Model & Dataset
# -----------------------------
model = joblib.load("linear_regression_pipeline.pkl")
df = pd.read_csv("used_car_cleaned.csv")

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([2, 1])

# =============================
# LEFT SIDE (Inputs)
# =============================
with left:

    st.subheader("📋 Car Information")

    brand = st.selectbox(
        "Brand",
        sorted(df["brand"].unique())
    )

    year = st.slider(
        "Manufacturing Year",
        min_value=int(df["make_year"].min()),
        max_value=int(df["make_year"].max()),
        value=2020
    )

    mileage = st.slider(
        "Mileage (km/L)",
        min_value=float(df["mileage_kmpl"].min()),
        max_value=float(df["mileage_kmpl"].max()),
        value=18.0
    )

    engine = st.slider(
        "Engine Capacity (CC)",
        min_value=int(df["engine_cc"].min()),
        max_value=int(df["engine_cc"].max()),
        value=1800
    )

    fuel = st.selectbox(
        "Fuel Type",
        sorted(df["fuel_type"].unique())
    )

    transmission = st.selectbox(
        "Transmission",
        sorted(df["transmission"].unique())
    )

    owner = st.selectbox(
        "Previous Owners",
        sorted(df["owner_count"].unique())
    )

    color = st.selectbox(
        "Color",
        sorted(df["color"].unique())
    )

    service = st.selectbox(
        "Service History",
        sorted(df["service_history"].unique())
    )

    accidents = st.selectbox(
        "Accidents Reported",
        sorted(df["accidents_reported"].unique())
    )

    insurance = st.selectbox(
        "Insurance Valid",
        sorted(df["insurance_valid"].unique())
    )

# =============================
# RIGHT SIDE (Image)
# =============================
with right:

    st.subheader("🚘 Car Preview")

    image_path = f"assets/brands/{brand}.jpg"

    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.image("assets/brands/default.jpg", use_container_width=True)

# =============================
# Prediction Button
# =============================
st.markdown("---")

if st.button("🚀 Estimate Price", use_container_width=True):

    input_data = pd.DataFrame({
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
        "insurance_valid": [insurance]
    })

    with st.spinner("Predicting..."):

        prediction = model.predict(input_data)[0]

    st.success("Prediction Completed Successfully!")

    st.metric(
        label="💰 Estimated Car Price",
        value=f"${prediction:,.0f}"
    )

    st.markdown("---")

    st.subheader("🚗 Car Profile")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Brand:** {brand}")
        st.write(f"**Year:** {year}")
        st.write(f"**Fuel:** {fuel}")
        st.write(f"**Transmission:** {transmission}")
        st.write(f"**Engine:** {engine} CC")

    with col2:
        st.write(f"**Mileage:** {mileage} km/L")
        st.write(f"**Owners:** {owner}")
        st.write(f"**Color:** {color}")
        st.write(f"**Service History:** {service}")
        st.write(f"**Insurance:** {insurance}")