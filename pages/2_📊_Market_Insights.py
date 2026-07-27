"""
pages/2_📊_Market_Insights.py
Interactive market dashboard: KPI cards, filters, and multiple chart types.
"""

import streamlit as st
import plotly.express as px
from utils.theme import apply_theme, logo, page_header, card_open, card_close, kpi
from utils.data import load_data

st.set_page_config(page_title="Market Insights | LuxeCar", page_icon="📊", layout="wide")
apply_theme()

PLOTLY_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E5E7EB",
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)
GOLD_SCALE = ["#3a2f00", "#7a6100", "#B8860B", "#D4AF37", "#FFD700"]

with st.sidebar:
    logo()

try:
    df = load_data()
except Exception as e:
    st.error(f"تعذر تحميل الداتا: {e}")
    st.stop()

page_header("MARKET INSIGHTS", "INTERACTIVE ANALYTICS DASHBOARD", "Explore the full used-car dataset")

# ================= FILTERS =================
card_open("🔎 FILTERS")
f1, f2, f3, f4 = st.columns(4)
with f1:
    brands = st.multiselect("Brand", sorted(df["brand"].unique()))
with f2:
    fuels = st.multiselect("Fuel Type", sorted(df["fuel_type"].unique()))
with f3:
    transmissions = st.multiselect("Transmission", sorted(df["transmission"].unique()))
with f4:
    yr_min, yr_max = int(df["make_year"].min()), int(df["make_year"].max())
    year_range = st.slider("Year Range", yr_min, yr_max, (yr_min, yr_max))
card_close()

fdf = df.copy()
if brands:
    fdf = fdf[fdf["brand"].isin(brands)]
if fuels:
    fdf = fdf[fdf["fuel_type"].isin(fuels)]
if transmissions:
    fdf = fdf[fdf["transmission"].isin(transmissions)]
fdf = fdf[(fdf["make_year"] >= year_range[0]) & (fdf["make_year"] <= year_range[1])]

has_price = "price_usd" in fdf.columns

# ================= KPI ROW =================
k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    kpi("Total Cars", f"{len(fdf):,}")
with k2:
    kpi("Avg Price", f"${fdf['price_usd'].mean():,.0f}" if has_price and len(fdf) else "—")
with k3:
    kpi("Avg Engine", f"{fdf['engine_cc'].mean():,.0f} cc" if len(fdf) else "—")
with k4:
    kpi("Avg Year", f"{fdf['make_year'].mean():,.0f}" if len(fdf) else "—")
with k5:
    kpi("Top Brand", fdf["brand"].value_counts().idxmax() if len(fdf) else "—")
with k6:
    if has_price and len(fdf):
        cheapest_brand = fdf.groupby("brand")["price_usd"].mean().idxmin()
    else:
        cheapest_brand = "—"
    kpi("Lowest Avg Brand", cheapest_brand)

st.markdown("<br>", unsafe_allow_html=True)

if fdf.empty:
    st.warning("لا توجد بيانات مطابقة للفلاتر المختارة.")
    st.stop()

# ================= CHARTS ROW 1 =================
r1c1, r1c2 = st.columns(2)
with r1c1:
    card_open("📈 Price Distribution (Histogram)")
    if has_price:
        fig = px.histogram(fdf, x="price_usd", nbins=30, color_discrete_sequence=["#D4AF37"])
        fig.update_layout(**PLOTLY_TEMPLATE, height=340)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("عمود price_usd غير موجود في الداتا.")
    card_close()

with r1c2:
    card_open("🎯 Price vs. Mileage (Scatter)")
    if has_price:
        fig = px.scatter(fdf, x="mileage_kmpl", y="price_usd", color="brand",
                          color_discrete_sequence=px.colors.sequential.YlOrBr)
        fig.update_layout(**PLOTLY_TEMPLATE, height=340)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("عمود price_usd غير موجود في الداتا.")
    card_close()

# ================= CHARTS ROW 2 =================
r2c1, r2c2 = st.columns(2)
with r2c1:
    card_open("🥧 Fuel Type Share (Pie)")
    fig = px.pie(fdf, names="fuel_type", color_discrete_sequence=GOLD_SCALE, hole=0.0)
    fig.update_layout(**PLOTLY_TEMPLATE, height=340)
    st.plotly_chart(fig, use_container_width=True)
    card_close()

with r2c2:
    card_open("🍩 Transmission Share (Donut)")
    fig = px.pie(fdf, names="transmission", color_discrete_sequence=GOLD_SCALE, hole=0.55)
    fig.update_layout(**PLOTLY_TEMPLATE, height=340)
    st.plotly_chart(fig, use_container_width=True)
    card_close()

# ================= CHARTS ROW 3 =================
r3c1, r3c2 = st.columns(2)
with r3c1:
    card_open("📉 Average Price by Year (Line)")
    if has_price:
        trend = fdf.groupby("make_year")["price_usd"].mean().reset_index()
        fig = px.line(trend, x="make_year", y="price_usd", markers=True,
                      color_discrete_sequence=["#FFD700"])
        fig.update_layout(**PLOTLY_TEMPLATE, height=340)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("عمود price_usd غير موجود في الداتا.")
    card_close()

with r3c2:
    card_open("📊 Car Count by Brand (Bar)")
    counts = fdf["brand"].value_counts().reset_index()
    counts.columns = ["brand", "count"]
    fig = px.bar(counts, x="brand", y="count", color="count", color_continuous_scale=GOLD_SCALE)
    fig.update_layout(**PLOTLY_TEMPLATE, height=340)
    st.plotly_chart(fig, use_container_width=True)
    card_close()

# ================= TOP 10 TABLES =================
if has_price:
    t1, t2 = st.columns(2)
    with t1:
        card_open("💎 Top 10 Most Expensive Cars")
        top10 = fdf.sort_values("price_usd", ascending=False).head(10)[
            ["brand", "make_year", "mileage_kmpl", "price_usd"]
        ]
        st.dataframe(top10, use_container_width=True, hide_index=True)
        card_close()

    with t2:
        card_open("🏷️ Top 10 Cheapest Cars")
        bottom10 = fdf.sort_values("price_usd", ascending=True).head(10)[
            ["brand", "make_year", "mileage_kmpl", "price_usd"]
        ]
        st.dataframe(bottom10, use_container_width=True, hide_index=True)
        card_close()
