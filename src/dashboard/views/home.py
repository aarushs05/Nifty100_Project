"""
Home Dashboard
Sprint 4
"""

from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard.utils.db import (
    get_dashboard_data,
    get_years
)


def show():

    st.title("📈 Nifty 100 Dashboard")

    st.markdown(
        """
        Comprehensive Financial Analytics Dashboard
        """
    )

    st.divider()

    # ---------------------------------------------
    # Load Data
    # ---------------------------------------------

    df = get_dashboard_data()

    if df.empty:

        st.error("No dashboard data found.")

        return

    # ---------------------------------------------
    # Sidebar Filters
    # ---------------------------------------------

    years = sorted(df["year"].dropna().unique())

    selected_year = st.sidebar.selectbox(
        "Select Financial Year",
        years,
        index=len(years)-1
    )

    df = df[df["year"] == selected_year]

    st.subheader(f"Financial Year : {selected_year}")

    st.write("")

    # ---------------------------------------------
    # KPI Calculations
    # ---------------------------------------------

    total_companies = df["company_id"].nunique()

    avg_roe = df["return_on_equity_pct"].mean()

    avg_roce = df["return_on_capital_employed_pct"].mean()

    median_de = df["debt_to_equity"].median()

    avg_fcf = df["free_cash_flow_cr"].mean()

    avg_quality = df["composite_quality_score"].mean()

    # ---------------------------------------------
    # KPI Cards
    # ---------------------------------------------

    c1,c2,c3 = st.columns(3)

    with c1:

        st.metric(
            "Companies",
            total_companies
        )

        st.metric(
            "Average ROE",
            f"{avg_roe:.2f}%"
        )

    with c2:

        st.metric(
            "Average ROCE",
            f"{avg_roce:.2f}%"
        )

        st.metric(
            "Median Debt/Equity",
            f"{median_de:.2f}"
        )

    with c3:

        st.metric(
            "Average FCF",
            f"{avg_fcf:,.0f} Cr"
        )

        st.metric(
            "Quality Score",
            f"{avg_quality:.1f}"
        )

    st.divider()
        
        # -------------------------------------------------------
    # Sector Distribution
    # -------------------------------------------------------

    sector_data = (
        df.groupby("broad_sector")
          .size()
          .reset_index(name="Companies")
    )

    left, right = st.columns([2, 1])

    with left:

        st.subheader("Sector Distribution")

        fig = px.pie(
            sector_data,
            values="Companies",
            names="broad_sector",
            hole=0.55
        )

        fig.update_layout(height=500)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Top 5 Companies")

        top = (
            df.sort_values(
                "composite_quality_score",
                ascending=False
            )
            .head(5)
        )

        st.dataframe(
            top[
                [
                    "company_name",
                    "composite_quality_score",
                    "return_on_equity_pct"
                ]
            ],
            use_container_width=True
        )

        # -------------------------------------------------------
    # Sector Distribution
    # -------------------------------------------------------

    st.subheader("🏭 Sector Distribution")

    sector_data = (
        df.groupby("broad_sector", as_index=False)
          .agg(Companies=("company_id", "nunique"))
    )

    if not sector_data.empty:

        fig = px.pie(
            sector_data,
            values="Companies",
            names="broad_sector",
            hole=0.55,
            title="Companies by Sector"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # -------------------------------------------------------
    # Top Companies
    # -------------------------------------------------------

    st.subheader("🏆 Top 5 Companies by Quality Score")

    top5 = (
        df.sort_values(
            by="composite_quality_score",
            ascending=False
        )
        .drop_duplicates("company_id")
        .head(5)
    )

    display_df = top5[
        [
            "company_name",
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "composite_quality_score"
        ]
    ].copy()

    display_df.columns = [
        "Company",
        "ROE %",
        "ROCE %",
        "Quality Score"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

        # -------------------------------------------------------
    # Revenue CAGR & PAT CAGR
    # -------------------------------------------------------

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📈 Revenue CAGR (5 Years)")

        revenue = (
            df[
                [
                    "company_name",
                    "revenue_cagr_5yr"
                ]
            ]
            .dropna()
            .sort_values(
                "revenue_cagr_5yr",
                ascending=False
            )
            .head(10)
        )

        if not revenue.empty:

            fig = px.bar(
                revenue,
                x="revenue_cagr_5yr",
                y="company_name",
                orientation="h",
                text="revenue_cagr_5yr",
                title="Top 10 Revenue CAGR"
            )

            fig.update_layout(
                height=500,
                yaxis=dict(categoryorder="total ascending")
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("Revenue CAGR data unavailable.")

    with col2:

        st.subheader("💰 PAT CAGR (5 Years)")

        pat = (
            df[
                [
                    "company_name",
                    "pat_cagr_5yr"
                ]
            ]
            .dropna()
            .sort_values(
                "pat_cagr_5yr",
                ascending=False
            )
            .head(10)
        )

        if not pat.empty:

            fig = px.bar(
                pat,
                x="pat_cagr_5yr",
                y="company_name",
                orientation="h",
                text="pat_cagr_5yr",
                title="Top 10 PAT CAGR"
            )

            fig.update_layout(
                height=500,
                yaxis=dict(categoryorder="total ascending")
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("PAT CAGR data unavailable.")