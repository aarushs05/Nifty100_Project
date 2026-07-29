"""
Nifty 100 Analytics Dashboard
Sprint 4

Main Streamlit Application
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# -------------------------------------------------------
# Project Root
# -------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# -------------------------------------------------------
# Streamlit Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------
# Import Dashboard Pages
# -------------------------------------------------------

from src.dashboard.views import (
    home,
    profile,
    screener,
    peers,
    trends,
    sectors,
    capital,
    reports,
)

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.title("📊 Nifty 100 Analytics")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🏢 Company Profile",
        "🔎 Screener",
        "⚖ Peer Comparison",
        "📈 Trend Analysis",
        "🏭 Sector Analysis",
        "🗺 Capital Allocation",
        "📑 Annual Reports",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("Sprint 4 Dashboard")
st.sidebar.caption("Bluestock Capstone Project")

# -------------------------------------------------------
# Navigation
# -------------------------------------------------------

if page == "🏠 Home":
    home.show()

elif page == "🏢 Company Profile":
    profile.show()

elif page == "🔎 Screener":
    screener.show()

elif page == "⚖ Peer Comparison":
    peers.show()

elif page == "📈 Trend Analysis":
    trends.show()

elif page == "🏭 Sector Analysis":
    sectors.show()

elif page == "🗺 Capital Allocation":
    capital.show()

elif page == "📑 Annual Reports":
    reports.show()