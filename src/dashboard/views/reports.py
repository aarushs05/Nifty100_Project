import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard.utils.db import get_dashboard_data


def show():

    st.title("📑 Reports & Downloads")

    df = get_dashboard_data()
    st.write(df.columns.tolist())
    if df.empty:
        st.warning("No report data available.")
        return

    # =====================================================
    # Latest Financial Year
    # =====================================================

    latest_year = df["year"].max()

    df = df[df["year"] == latest_year].copy()

    # =====================================================
    # Filters
    # =====================================================

    sectors = sorted(df["broad_sector"].dropna().unique())

    sector = st.selectbox(
        "Sector",
        ["All"] + sectors
    )

    if sector != "All":
        df = df[df["broad_sector"] == sector]

    search = st.text_input(
        "Search Company"
    )

    if search:

        df = df[
            df["company_name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # =====================================================
    # KPI Cards
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Companies",
        len(df)
    )

    c2.metric(
        "Average ROE",
        f"{df['return_on_equity_pct'].mean():.2f}%"
    )

    c3.metric(
        "Average ROCE",
        f"{df['return_on_capital_employed_pct'].mean():.2f}%"
    )

    c4.metric(
        "Average Quality",
        f"{df['composite_quality_score'].mean():.2f}"
    )

    # =====================================================
    # Quality Distribution
    # =====================================================

    st.divider()

    st.subheader("⭐ Quality Score Distribution")

    fig1 = px.histogram(
        df,
        x="composite_quality_score",
        nbins=20,
        color_discrete_sequence=["royalblue"]
    )

    fig1.update_layout(
        height=500
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        key="reports_quality"
    )

    # =====================================================
    # ROE vs ROCE
    # =====================================================

    st.divider()

    st.subheader("📈 ROE vs ROCE")

    fig2 = px.scatter(
        df,
        x="return_on_equity_pct",
        y="return_on_capital_employed_pct",
        color="composite_quality_score",
        size="composite_quality_score",
        hover_name="company_name"
)

    fig2.update_layout(
        height=550
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="reports_scatter"
    )

    # =====================================================
    # Top Companies
    # =====================================================

    st.divider()

    st.subheader("🏆 Top 20 Companies")

    top = df.sort_values(
        "composite_quality_score",
        ascending=False
    ).head(20)

    fig3 = px.bar(
        top,
        x="company_name",
        y="composite_quality_score",
        color="composite_quality_score",
        text="composite_quality_score"
    )

    fig3.update_layout(
        height=550
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
        key="reports_top"
    )

    # =====================================================
    # Company Report Table
    # =====================================================

    st.divider()

    st.subheader("📋 Company Report")

    report = df[
    [
        "company_name",
        "broad_sector",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "free_cash_flow_cr",
        "composite_quality_score"
    ]

    ].sort_values(
        "composite_quality_score",
        ascending=False
    )

    st.dataframe(
        report,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # Download CSV
    # =====================================================

    st.divider()

    st.subheader("📥 Download Report")

    csv = report.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Company Report (CSV)",
        data=csv,
        file_name="nifty100_company_report.csv",
        mime="text/csv"
    )

    # =====================================================
    # Best Company
    # =====================================================

    st.divider()

    st.subheader("⭐ Highest Quality Company")

    winner = report.iloc[0]

    col1, col2 = st.columns([3, 1])

    with col1:

        st.success(
            f"**{winner['company_name']}** ranks highest based on the composite quality score."
        )

        st.write(f"Sector : {winner['broad_sector']}")
        st.write(f"ROE : {winner['return_on_equity_pct']:.2f}%")
        st.write(f"ROCE : {winner['return_on_capital_employed_pct']:.2f}%")
        st.write(f"Free Cash Flow : ₹ {winner['free_cash_flow_cr']:,.0f} Cr")

    with col2:

        st.metric(
            "Quality Score",
            f"{winner['composite_quality_score']:.2f}"
        )

    # =====================================================
    # Summary Statistics
    # =====================================================

    st.divider()

    st.subheader("📊 Summary Statistics")

    summary = report.describe().T

    st.dataframe(
        summary,
        use_container_width=True
    )

    # =====================================================
    # Footer
    # =====================================================

    st.divider()

    st.caption(
        "Nifty 100 Analytics Dashboard • Sprint 4 • Reports & Downloads"
    )