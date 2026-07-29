import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_pl,
    get_market_cap
)


def show():

    st.title("📈 Trend Analysis")

    companies = get_companies()

    if companies.empty:
        st.warning("No companies available.")
        return

    company = st.selectbox(
        "Select Company",
        companies["company_name"].tolist()
    )

    company_id = companies.loc[
        companies["company_name"] == company,
        "id"
    ].iloc[0]

    ratios = get_ratios(company_id)
    pl = get_pl(company_id)
    market = get_market_cap(company_id)

    if ratios.empty:
        st.warning("No financial data available.")
        return

    # =====================================================
    # KPI Cards
    # =====================================================

    latest = ratios.sort_values("year").iloc[-1]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "ROE",
        f"{latest['return_on_equity_pct']:.2f}%"
    )

    c2.metric(
        "ROCE",
        f"{latest['return_on_capital_employed_pct']:.2f}%"
    )

    c3.metric(
        "Debt / Equity",
        f"{latest['debt_to_equity']:.2f}"
    )

    c4.metric(
        "Quality Score",
        f"{latest['composite_quality_score']:.2f}"
    )

    # =====================================================
    # Revenue & Profit Trend
    # =====================================================

    st.divider()

    st.subheader("📊 Revenue vs Net Profit")

    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=pl["year"],
            y=pl["sales"],
            mode="lines+markers",
            name="Sales"
        )
    )

    fig1.add_trace(
        go.Scatter(
            x=pl["year"],
            y=pl["net_profit"],
            mode="lines+markers",
            name="Net Profit"
        )
    )

    fig1.update_layout(
        height=500
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        key="trend_sales_profit"
    )

    # =====================================================
    # ROE & ROCE Trend
    # =====================================================

    st.divider()

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=ratios["year"],
            y=ratios["return_on_equity_pct"],
            mode="lines+markers",
            name="ROE"
        )
    )

    fig2.add_trace(
        go.Scatter(
            x=ratios["year"],
            y=ratios["return_on_capital_employed_pct"],
            mode="lines+markers",
            name="ROCE"
        )
    )

    fig2.update_layout(
        title="ROE vs ROCE",
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="trend_roe_roce"
    )
    # =====================================================
    # EPS Trend
    # =====================================================

    st.divider()

    st.subheader("💰 Earnings Per Share")

    if not pl.empty:

        fig3 = px.bar(
            pl,
            x="year",
            y="eps",
            text="eps",
            title="EPS Trend"
        )

        fig3.update_layout(
            height=450
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
            key="trend_eps"
        )

    # =====================================================
    # Debt Trend
    # =====================================================

    st.divider()

    st.subheader("🏦 Debt to Equity")

    fig4 = px.line(
        ratios,
        x="year",
        y="debt_to_equity",
        markers=True,
        title="Debt / Equity Trend"
    )

    fig4.update_layout(
        height=450
    )

    st.plotly_chart(
        fig4,
        use_container_width=True,
        key="trend_debt"
    )

    # =====================================================
    # Quality Score Trend
    # =====================================================

    st.divider()

    st.subheader("⭐ Quality Score")

    fig5 = px.line(
        ratios,
        x="year",
        y="composite_quality_score",
        markers=True,
        title="Composite Quality Score"
    )

    fig5.update_layout(
        height=450
    )

    st.plotly_chart(
        fig5,
        use_container_width=True,
        key="trend_quality"
    )

    # =====================================================
    # Market Valuation Trend
    # =====================================================

    if not market.empty:

        st.divider()

        st.subheader("📈 Market Capitalization")

        fig6 = go.Figure()

        fig6.add_trace(
            go.Scatter(
                x=market["year"],
                y=market["market_cap_crore"],
                mode="lines+markers",
                name="Market Cap"
            )
        )

        fig6.add_trace(
            go.Scatter(
                x=market["year"],
                y=market["enterprise_value_crore"],
                mode="lines+markers",
                name="Enterprise Value"
            )
        )

        fig6.update_layout(
            height=500
        )

        st.plotly_chart(
            fig6,
            use_container_width=True,
            key="trend_marketcap"
        )

    # =====================================================
    # Growth Comparison
    # =====================================================

    st.divider()

    st.subheader("📊 Revenue CAGR vs PAT CAGR")

    fig7 = px.bar(
        ratios,
        x="year",
        y=[
            "revenue_cagr_5yr",
            "pat_cagr_5yr"
        ],
        barmode="group",
        title="Growth Trend"
    )

    fig7.update_layout(
        height=500
    )

    st.plotly_chart(
        fig7,
        use_container_width=True,
        key="trend_growth"
    )

    # =====================================================
    # Financial Ratios Table
    # =====================================================

    st.divider()

    st.subheader("📋 Financial Ratios")

    st.dataframe(
        ratios,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # Profit & Loss Table
    # =====================================================

    with st.expander("📑 Profit & Loss"):

        st.dataframe(
            pl,
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # Market Valuation Table
    # =====================================================

    if not market.empty:

        with st.expander("💹 Market Valuation"):

            st.dataframe(
                market,
                use_container_width=True,
                hide_index=True
            )

    # =====================================================
    # Footer
    # =====================================================

    st.divider()

    st.caption(
        "Nifty 100 Analytics Dashboard • Sprint 4 • Trend Analysis"
    )