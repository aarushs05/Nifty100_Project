from pathlib import Path

import pandas as pd
import streamlit as st


def show():
    """Display NLP-generated company insights."""

    st.title("🧠 NLP Insights")

    root = Path(__file__).resolve().parents[3]

    try:
        df = pd.read_csv(root / "output" / "final_company_report.csv")
    except (OSError, ValueError) as e:
        st.error(f"Unable to load final_company_report.csv\n\n{e}")
        return

    if df.empty:
        st.warning("No NLP insights available.")
        return

    company = st.selectbox(
        "Select Company",
        sorted(df["company_id"].unique()),
    )

    row = df.loc[df["company_id"] == company].iloc[0]

    st.divider()
    st.subheader("📊 Overall Assessment")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Overall Rating", row["overall_rating"])

    with c2:
        st.metric(
            "Overall Score",
            round(float(row["overall_score"]), 2),
        )

    with c3:
        st.metric(
            "Confidence Score",
            round(float(row["confidence_score"]), 2),
        )

    st.divider()
    st.subheader("✅ Strengths & Risks")

    col1, col2 = st.columns(2)

    with col1:
        st.success("Pros")

        if pd.notna(row["pros"]):
            st.write(row["pros"])
        else:
            st.info("No major strengths identified.")

    with col2:
        st.error("Cons")

        if pd.notna(row["cons"]):
            st.write(row["cons"])
        else:
            st.info("No major concerns identified.")

    st.divider()
    st.subheader("💰 Cash Flow Intelligence")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Health", row["cashflow_health"])

    with c2:
        st.metric("Risk Level", row["risk_level"])

    with c3:
        st.metric("Cash Flow Score", row["cashflow_score"])

    st.divider()
    st.subheader("🏦 Capital Allocation Intelligence")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Allocation Quality",
            row["allocation_quality"],
        )

    with c2:
        st.metric(
            "Allocation Score",
            row["allocation_score"],
        )

    st.divider()
    st.subheader("📝 AI Generated Narrative")

    st.info(row["narrative"])

    st.divider()
    st.subheader("📈 Score Summary")

    score_df = pd.DataFrame(
        {
            "Metric": [
                "Confidence Score",
                "Cash Flow Score",
                "Allocation Score",
                "Overall Score",
            ],
            "Score": [
                row["confidence_score"],
                row["cashflow_score"],
                row["allocation_score"],
                row["overall_score"],
            ],
        }
    )

    st.bar_chart(score_df.set_index("Metric"))

    st.divider()

    with st.expander("🔍 View Full Record"):
        st.dataframe(
            pd.DataFrame([row]),
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.caption(
        "Nifty 100 Analytics Dashboard • Sprint 5 • NLP Intelligence Module"
    )