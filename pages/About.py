"""
pages/6_ℹ️_About.py
Project, dataset, model and developer information.
"""

import streamlit as st
from utils.theme import apply_theme, logo, page_header, card_open, card_close

st.set_page_config(page_title="About | LuxeCar", page_icon="ℹ️", layout="wide")
apply_theme()

with st.sidebar:
    logo()

page_header("ABOUT", "LUXECAR PREDICT", "AI Powered Premium Vehicle Valuation System")

c1, c2 = st.columns(2)

with c1:
    card_open("📖 Project Description")
    st.write(
        "LuxeCar Predict is an AI-powered web application that estimates the fair "
        "market value of used cars using a trained Machine Learning pipeline. "
        "It combines a premium dashboard experience with real-time market insights, "
        "vehicle comparison, prediction history, and downloadable PDF reports."
    )
    card_close()

    card_open("🗂️ Dataset Information")
    st.markdown(
        """
        - **File:** `used_car_cleaned.csv`
        - **Columns:** make_year, mileage_kmpl, engine_cc, fuel_type, owner_count,
          price_usd, brand, transmission, color, service_history,
          accidents_reported, insurance_valid
        """
    )
    card_close()

with c2:
    card_open("🤖 Machine Learning Model")
    st.markdown(
        """
        - **Type:** Linear Regression Pipeline (Scikit-Learn)
        - **File:** `linear_regression_pipeline.pkl`
        - **Inputs:** 11 vehicle features (numerical + categorical, preprocessed inside the pipeline)
        - **Output:** Estimated price in USD
        """
    )
    card_close()

    card_open("🛠️ Technologies Used")
    st.markdown(
        """
        Python • Streamlit • Pandas • Scikit-Learn • Plotly •
        Requests (Pexels API) • Pillow (PIL) • Joblib • ReportLab
        """
    )
    card_close()
