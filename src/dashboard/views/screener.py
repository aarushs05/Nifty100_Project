import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard.utils.db import get_dashboard_data


def show():

    st.title("🔍 Nifty 100 Stock Screener")

    # =====================================================
    # Load Data
    # =====================================================

    df = get_dashboard_data()

    if df.empty:
        st.error("No data found.")
        return

    # =====================================================
    # Sidebar Filters
    # =====================================================

    st.sidebar.header("Screening Filters")

    years = sorted(df["year"].dropna().unique())

    selected_year = st.sidebar.selectbox(
        "Financial Year",
        years,
        index=len(years)-1
    )

    df = df[df["year"] == selected_year]

    sectors = sorted(df["broad_sector"].dropna().unique())

    selected_sector = st.sidebar.multiselect(
        "Sector",
        sectors,
        default=sectors
    )

    df = df[df["broad_sector"].isin(selected_sector)]

    # =====================================================
    # Company Search
    # =====================================================

    search = st.text_input(
        "🔎 Search Company"
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
    # Financial Filters
    # =====================================================

    st.sidebar.subheader("Financial Filters")

    min_roe = st.sidebar.slider(
        "Minimum ROE %",
        0.0,
        60.0,
        10.0
    )

    min_roce = st.sidebar.slider(
        "Minimum ROCE %",
        0.0,
        60.0,
        10.0
    )

    max_debt = st.sidebar.slider(
        "Maximum Debt / Equity",
        0.0,
        5.0,
        2.0
    )

    min_quality = st.sidebar.slider(
        "Minimum Quality Score",
        0.0,
        100.0,
        50.0
    )

    df = df[
        (df["return_on_equity_pct"] >= min_roe)
        &
        (df["return_on_capital_employed_pct"] >= min_roce)
        &
        (df["debt_to_equity"] <= max_debt)
        &
        (df["composite_quality_score"] >= min_quality)
    ]

    # =====================================================
    # KPI Cards
    # =====================================================

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Companies",
        len(df)
    )

    c2.metric(
        "Average ROE",
        f"{df['return_on_equity_pct'].mean():.2f}%"
        if not df.empty else "-"
    )

    c3.metric(
        "Average ROCE",
        f"{df['return_on_capital_employed_pct'].mean():.2f}%"
        if not df.empty else "-"
    )

    c4.metric(
        "Average Quality",
        f"{df['composite_quality_score'].mean():.2f}"
        if not df.empty else "-"
    )

    # =====================================================
    # Screener Results
    # =====================================================

    st.divider()

    st.subheader("📋 Filtered Companies")

    display = df[
        [
            "company_name",
            "broad_sector",
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "composite_quality_score"
        ]
    ].copy()

    display.columns = [
        "Company",
        "Sector",
        "ROE %",
        "ROCE %",
        "Debt/Equity",
        "Free Cash Flow",
        "Revenue CAGR %",
        "PAT CAGR %",
        "Quality Score"
    ]

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # Download CSV
    # =====================================================

    csv = display.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Filtered Results",
        csv,
        file_name="nifty100_screener.csv",
        mime="text/csv"
    )
        # =====================================================
    # ROE vs ROCE Scatter Plot
    # =====================================================

    st.divider()

    st.subheader("📈 ROE vs ROCE Analysis")

    if not df.empty:

        fig = px.scatter(
            df,
            x="return_on_equity_pct",
            y="return_on_capital_employed_pct",
            color="broad_sector",
            size="composite_quality_score",
            hover_name="company_name",
            title="ROE vs ROCE"
        )

        fig.update_layout(height=600)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # Top Quality Companies
    # =====================================================

    st.divider()

    st.subheader("🏆 Top 10 Quality Companies")

    top_quality = (
        df.sort_values(
            "composite_quality_score",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_quality,
        x="company_name",
        y="composite_quality_score",
        color="broad_sector",
        text="composite_quality_score",
        title="Top Quality Companies"
    )

    fig.update_layout(
        xaxis_title="Company",
        yaxis_title="Quality Score",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # Sector Quality
    # =====================================================

    st.divider()

    st.subheader("🏭 Sector Quality Analysis")

    sector = (
        df.groupby("broad_sector", as_index=False)
        .agg(
            Avg_Quality=("composite_quality_score", "mean"),
            Avg_ROE=("return_on_equity_pct", "mean"),
            Avg_ROCE=("return_on_capital_employed_pct", "mean"),
            Companies=("company_name", "count")
        )
    )

    fig = px.bar(
        sector,
        x="broad_sector",
        y="Avg_Quality",
        text="Avg_Quality",
        color="Companies",
        title="Average Quality by Sector"
    )

    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Average Quality Score",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # Quality Distribution
    # =====================================================

    st.divider()

    st.subheader("📊 Quality Score Distribution")

    fig = px.histogram(
        df,
        x="composite_quality_score",
        nbins=20,
        title="Quality Score Distribution"
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # Revenue CAGR vs PAT CAGR
    # =====================================================

    st.divider()

    st.subheader("📈 Growth Comparison")

    fig = px.scatter(
        df,
        x="revenue_cagr_5yr",
        y="pat_cagr_5yr",
        color="broad_sector",
        size="composite_quality_score",
        hover_name="company_name",
        title="Revenue CAGR vs PAT CAGR"
    )

    fig.update_layout(height=600)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # Best Performing Companies
    # =====================================================

    st.divider()

    st.subheader("⭐ Best Performing Companies")

    ranking = (
        df.sort_values(
            [
                "composite_quality_score",
                "return_on_equity_pct"
            ],
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        ranking[
            [
                "company_name",
                "broad_sector",
                "return_on_equity_pct",
                "return_on_capital_employed_pct",
                "debt_to_equity",
                "revenue_cagr_5yr",
                "pat_cagr_5yr",
                "composite_quality_score"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # Footer
    # =====================================================

    st.divider()

    st.caption(
        "Nifty 100 Analytics Dashboard • Sprint 4 • Stock Screener"
    )