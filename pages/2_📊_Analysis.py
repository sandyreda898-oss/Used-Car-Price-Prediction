"""
pages/3_📈_Analytics.py
Deeper analytics: correlations, segment comparisons, and model-relevant
feature relationships (distinct from the general Market Insights dashboard).
"""

import streamlit as st
import plotly.express as px
import numpy as np
from utils.theme import apply_theme, logo, page_header, card_open, card_close
from utils.data import load_data

st.set_page_config(page_title="Analytics | LuxeCar", page_icon="📈", layout="wide")
apply_theme()

PLOTLY_TEMPLATE = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E5E7EB")

with st.sidebar:
    logo()

try:
    df = load_data()
except Exception as e:
    st.error(f"تعذر تحميل الداتا: {e}")
    st.stop()

page_header("ANALYTICS", "FEATURE & PRICE RELATIONSHIPS", "Deeper statistical view of the dataset")

has_price = "price_usd" in df.columns

# ================= CORRELATION HEATMAP =================
card_open("🧩 Numerical Feature Correlation")
num_cols = [c for c in ["make_year", "mileage_kmpl", "engine_cc", "owner_count", "price_usd"] if c in df.columns]
if len(num_cols) >= 2:
    corr = df[num_cols].corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale=["#0a0a0a", "#B8860B", "#FFD700"], aspect="auto")
    fig.update_layout(**PLOTLY_TEMPLATE, height=380)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("لا توجد أعمدة رقمية كافية لحساب الارتباط.")
card_close()

# ================= PRICE BY SEGMENT =================
r1, r2 = st.columns(2)
with r1:
    card_open("⛽ Avg Price by Fuel Type")
    if has_price:
        seg = df.groupby("fuel_type")["price_usd"].mean().reset_index()
        fig = px.bar(seg, x="fuel_type", y="price_usd", color="price_usd",
                     color_continuous_scale=["#3a2f00", "#D4AF37", "#FFD700"])
        fig.update_layout(**PLOTLY_TEMPLATE, height=340)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("عمود price_usd غير متاح.")
    card_close()

with r2:
    card_open("⚙️ Avg Price by Transmission")
    if has_price:
        seg = df.groupby("transmission")["price_usd"].mean().reset_index()
        fig = px.bar(seg, x="transmission", y="price_usd", color="price_usd",
                     color_continuous_scale=["#3a2f00", "#D4AF37", "#FFD700"])
        fig.update_layout(**PLOTLY_TEMPLATE, height=340)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("عمود price_usd غير متاح.")
    card_close()

# ================= ACCIDENTS / SERVICE IMPACT =================
r3, r4 = st.columns(2)
with r3:
    card_open("💥 Price Impact — Accidents Reported")
    if has_price:
        seg = df.groupby("accidents_reported")["price_usd"].mean().reset_index()
        fig = px.bar(seg, x="accidents_reported", y="price_usd", color_discrete_sequence=["#FFD700"])
        fig.update_layout(**PLOTLY_TEMPLATE, height=320)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("عمود price_usd غير متاح.")
    card_close()

with r4:
    card_open("🛠️ Price Impact — Service History")
    if has_price:
        seg = df.groupby("service_history")["price_usd"].mean().reset_index()
        fig = px.bar(seg, x="service_history", y="price_usd", color_discrete_sequence=["#D4AF37"])
        fig.update_layout(**PLOTLY_TEMPLATE, height=320)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("عمود price_usd غير متاح.")
    card_close()

# ================= ENGINE VS MILEAGE (BUBBLE) =================
card_open("🔧 Engine Capacity vs. Mileage (bubble size = price)")
if has_price:
    fig = px.scatter(
        df, x="engine_cc", y="mileage_kmpl", size="price_usd", color="brand",
        size_max=35, color_discrete_sequence=px.colors.sequential.YlOrBr,
    )
    fig.update_layout(**PLOTLY_TEMPLATE, height=420)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("عمود price_usd غير متاح لعرض حجم الفقاعة.")
card_close()
