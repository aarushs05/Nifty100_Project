import streamlit as st
import pandas as pd
from pathlib import Path


def show():

    st.title("🧠 NLP Insights")

    root = Path(__file__).resolve().parents[3]

    try:
        df = pd.read_csv(
            root / "output" / "final_company_report.csv"
        )

    except Exception as e:
        st.error(
            f"Unable to load final_company_report.csv\n\n{e}"
        )
        return

    if df.empty:
        st.warning("No NLP insights available.")
        return

    company = st.selectbox(
        "Select Company",
        sorted(df["company_id"].unique())
    )

    row = df.loc[
        df["company_id"] == company
    ].iloc[0]

    st.divider()

    st.subheader("📊 Overall Assessment")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Overall Rating",
            row["overall_rating"]
        )

    with c2:
        st.metric(
            "Overall Score",
            round(float(row["overall_score"]), 2)
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.success("Pros")

        pros = str(row["pros"])

        if pros and pros != "nan":
            st.write(pros)

    with col2:

        st.error("Cons")

        cons = str(row["cons"])

        if cons and cons != "nan":
            st.write(cons)

    st.divider()

    st.subheader("💰 Cash Flow Intelligence")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Health",
        row["cashflow_health"]
    )

    c2.metric(
        "Risk",
        row["risk_level"]
    )

    c3.metric(
        "Score",
        row["cashflow_score"]
    )

    st.divider()

    st.subheader("🏦 Capital Allocation")

    c1, c2 = st.columns(2)

    c1.metric(
        "Quality",
        row["allocation_quality"]
    )

    c2.metric(
        "Score",
        row["allocation_score"]
    )

    st.divider()

    st.subheader("📝 AI Narrative")

    st.info(
        row["narrative"]
    )

    st.divider()

    with st.expander("View Full Record"):

        st.dataframe(
            pd.DataFrame([row]),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.caption(
        "Nifty 100 Analytics Dashboard • Sprint 5 • NLP Insights"
    )