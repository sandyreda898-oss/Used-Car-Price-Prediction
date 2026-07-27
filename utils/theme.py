"""
utils/theme.py
Central design system for LuxeCar Predict.
Dark luxury glassmorphism theme (black + gold), injected once per page.
"""

import streamlit as st

# ======================================================
# COLOR PALETTE
# ======================================================
BG = "#090909"
CARD = "#161616"
GOLD = "#D4AF37"
GOLD_HOVER = "#FFD700"
TEXT = "#F5F5F5"
MUTED = "#9A9A9A"
SUCCESS = "#1F8A47"
DANGER = "#C0392B"
WARNING = "#D9A400"

CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{ font-family: 'Manrope', sans-serif; }}

    .stApp {{
        background:
            radial-gradient(circle at 15% -10%, #1c1c1c 0%, {BG} 45%, #050505 100%);
        color: {TEXT};
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    div.block-container {{ padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1550px; }}

    /* ============== SIDEBAR ============== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0c0c0c 0%, #030303 100%);
        border-right: 1px solid rgba(212,175,55,0.30);
    }}
    [data-testid="stSidebarNav"] li a {{
        border-radius: 10px !important;
        color: #cfcfcf !important;
        font-weight: 600;
        margin-bottom: 2px;
    }}
    [data-testid="stSidebarNav"] li a:hover {{
        background: rgba(212,175,55,0.10) !important;
        color: {GOLD_HOVER} !important;
    }}
    [data-testid="stSidebarNav"] li a[aria-current="page"] {{
        background: linear-gradient(90deg, #B8860B, {GOLD_HOVER}) !important;
        color: #0a0a0a !important;
        font-weight: 800;
    }}

    .sb-logo {{ text-align:left; margin: 6px 0 26px 4px; }}
    .sb-logo .icon {{ font-size: 30px; }}
    .sb-logo .n1 {{ font-family:'Cinzel', serif; font-weight:900; font-size:21px; color:{GOLD_HOVER}; letter-spacing:2px; display:block; margin-top:4px;}}
    .sb-logo .n2 {{ font-size:11px; color:{GOLD}; letter-spacing:5px; display:block; }}

    /* ============== TITLES ============== */
    .lux-kicker {{ text-align:center; color:{GOLD}; letter-spacing:4px; font-size:13px; font-weight:700; margin-bottom: 2px;}}
    .lux-title {{ text-align:center; font-family:'Cinzel', serif; font-weight:900; font-size:42px; color:{GOLD_HOVER};
                  text-shadow: 0 0 24px rgba(255,215,0,0.35); letter-spacing:1.5px; }}
    .lux-sub {{ text-align:center; color:{MUTED}; font-size:13px; letter-spacing:3px; text-transform:uppercase; margin-bottom: 26px;}}

    /* ============== GLASS CARD ============== */
    .glass-card {{
        background: linear-gradient(145deg, rgba(22,22,22,0.85), rgba(9,9,9,0.85));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(212,175,55,0.35);
        border-radius: 18px;
        padding: 26px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.45), 0 0 0 1px rgba(212,175,55,0.05) inset;
        transition: 0.3s ease;
        margin-bottom: 20px;
    }}
    .glass-card:hover {{ box-shadow: 0 10px 40px rgba(212,175,55,0.15); border-color: rgba(212,175,55,0.55); }}
    .glass-card h4 {{
        color: {GOLD_HOVER}; font-family:'Cinzel', serif; letter-spacing:1px;
        border-bottom: 1px solid rgba(212,175,55,0.25); padding-bottom:10px; margin-bottom:18px;
    }}

    /* ============== KPI ============== */
    .kpi {{
        background: linear-gradient(145deg, rgba(22,22,22,0.9), rgba(9,9,9,0.9));
        border: 1px solid rgba(212,175,55,0.3); border-radius: 16px; padding: 18px 20px;
        text-align:center;
    }}
    .kpi .k {{ color:{MUTED}; font-size:11px; letter-spacing:1.5px; text-transform:uppercase; }}
    .kpi .v {{ color:{GOLD_HOVER}; font-family:'Cinzel', serif; font-weight:800; font-size:26px; margin-top:6px; }}

    /* ============== BUTTONS ============== */
    .stButton>button {{
        width: 100%; height: 54px; font-family:'Cinzel', serif; font-size:17px; font-weight:700;
        border-radius: 12px; background: linear-gradient(90deg, #B8860B, {GOLD_HOVER}, {GOLD});
        background-size: 200% auto; color:#0a0a0a; border:none; letter-spacing:1.5px;
        box-shadow: 0 4px 20px rgba(212,175,55,0.35); transition: 0.35s ease;
    }}
    .stButton>button:hover {{ background-position: right center; transform: translateY(-2px);
        box-shadow: 0 6px 28px rgba(255,215,0,0.6); }}
    .stDownloadButton>button {{
        width:100%; border-radius:12px; border:1px solid {GOLD}; background: rgba(212,175,55,0.08);
        color:{GOLD_HOVER}; font-weight:700;
    }}

    /* ============== INPUTS ============== */
    .stSelectbox > div > div, .stNumberInput > div > div, .stTextInput > div > div {{
        background-color:#111111 !important; border:1px solid {GOLD} !important; color:{GOLD_HOVER} !important;
        border-radius: 10px !important;
    }}
    .stSlider p {{ color:{GOLD_HOVER} !important; font-weight:600; }}
    [data-testid="stMetricValue"] {{ color:{GOLD_HOVER} !important; font-family:'Cinzel', serif; text-shadow: 0 0 10px rgba(255,215,0,0.4); }}
    [data-testid="stMetricLabel"] {{ color:{TEXT} !important; }}

    /* ============== BADGES ============== */
    .badge {{ display:inline-block; padding:6px 14px; border-radius:999px; font-weight:700; font-size:12px; letter-spacing:1px; }}
    .badge-good {{ background: rgba(31,138,71,0.15); color:#4CD680; border:1px solid #1F8A47; }}
    .badge-fair {{ background: rgba(217,164,0,0.15); color:#F2C230; border:1px solid {WARNING}; }}
    .badge-bad {{ background: rgba(192,57,43,0.15); color:#FF6B5B; border:1px solid {DANGER}; }}

    .stars {{ color:{GOLD_HOVER}; font-size:22px; letter-spacing:3px; }}

    hr {{ border-color: rgba(212,175,55,0.2) !important; }}
</style>
"""


def apply_theme():
    """Inject the global CSS once at the top of every page."""
    st.markdown(CSS, unsafe_allow_html=True)


def logo():
    st.markdown(
        """
        <div class="sb-logo">
            <span class="icon">🚗</span>
            <span class="n1">LUXECAR</span>
            <span class="n2">PREDICT</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(kicker: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="lux-kicker">{kicker}</div>
        <div class="lux-title">{title}</div>
        <div class="lux-sub">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def card_open(title: str = None):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if title:
        st.markdown(f"<h4>{title}</h4>", unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def kpi(label: str, value: str):
    st.markdown(
        f"""<div class="kpi"><div class="k">{label}</div><div class="v">{value}</div></div>""",
        unsafe_allow_html=True,
    )
