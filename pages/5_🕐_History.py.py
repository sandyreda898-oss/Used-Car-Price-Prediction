"""
pages/5_🕐_History.py
Displays every past prediction saved via utils/history.py.
"""

import streamlit as st
from utils.theme import apply_theme, logo, page_header, card_open, card_close
from utils.history import load_history, clear_history

st.set_page_config(page_title="History | LuxeCar", page_icon="🕐", layout="wide")
apply_theme()

with st.sidebar:
    logo()

page_header("PREDICTION HISTORY", "YOUR SAVED VALUATIONS", "Every prediction made in this app")

hist = load_history()

if hist.empty:
    card_open("🕐 No Predictions Yet")
    st.write("Go to the **Predict** page and run your first valuation — it will show up here automatically.")
    card_close()
else:
    card_open(f"📋 {len(hist)} Saved Predictions")
    st.dataframe(
        hist.sort_values("date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
    csv = hist.to_csv(index=False).encode("utf-8")
    dl_col, clear_col = st.columns(2)
    with dl_col:
        st.download_button("⬇️ Download Full History (CSV)", data=csv,
                            file_name="luxecar_history.csv", mime="text/csv",
                            use_container_width=True)
    with clear_col:
        if st.button("🗑️ Clear History", use_container_width=True):
            clear_history()
            st.rerun()
    card_close()
