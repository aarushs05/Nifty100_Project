import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard.utils.db import get_dashboard_data


def show():

    st.title("🏭 Sector Analysis")

    df = get_dashboard_data()

    if df.empty:
        st.warning("No sector data available.")
        return

    # =====================================================
    # Sector Summary
    # =====================================================

    sector = (
        df.groupby("broad_sector", as_index=False)
        .agg(
            Companies=("company_id", "nunique"),
            Avg_ROE=("return_on_equity_pct", "mean"),
            Avg_ROCE=("return_on_capital_employed_pct", "mean"),
            Avg_Quality=("composite_quality_score", "mean"),
            Avg_Debt=("debt_to_equity", "mean"),
            Avg_FCF=("free_cash_flow_cr", "mean")
        )
    )

    # =====================================================
    # KPI Cards
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Sectors",
        len(sector)
    )

    c2.metric(
        "Companies",
        sector["Companies"].sum()
    )

    c3.metric(
        "Average ROE",
        f"{sector['Avg_ROE'].mean():.2f}%"
    )

    c4.metric(
        "Average Quality",
        f"{sector['Avg_Quality'].mean():.2f}"
    )

    # =====================================================
    # Sector Distribution
    # =====================================================

    st.divider()

    st.subheader("📊 Companies by Sector")

    fig1 = px.pie(
        sector,
        values="Companies",
        names="broad_sector",
        hole=0.5
    )

    fig1.update_layout(
        height=550
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        key="sector_pie"
    )

    # =====================================================
    # Average Quality
    # =====================================================

    st.divider()

    st.subheader("⭐ Average Quality Score")

    fig2 = px.bar(
        sector.sort_values(
            "Avg_Quality",
            ascending=False
        ),
        x="broad_sector",
        y="Avg_Quality",
        color="Avg_Quality",
        text="Avg_Quality"
    )

    fig2.update_layout(
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="sector_quality"
    )

    # =====================================================
    # ROE vs ROCE
    # =====================================================

    st.divider()

    st.subheader("📈 ROE vs ROCE")

    fig3 = px.scatter(
        sector,
        x="Avg_ROE",
        y="Avg_ROCE",
        size="Companies",
        color="Avg_Quality",
        hover_name="broad_sector"
    )

    fig3.update_layout(
        height=550
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
        key="sector_scatter"
    )
    # =====================================================
    # Free Cash Flow Comparison
    # =====================================================

    st.divider()

    st.subheader("💰 Average Free Cash Flow")

    fig4 = px.bar(
        sector.sort_values(
            "Avg_FCF",
            ascending=False
        ),
        x="broad_sector",
        y="Avg_FCF",
        color="Avg_FCF",
        text="Avg_FCF"
    )

    fig4.update_layout(
        height=500,
        xaxis_title="Sector",
        yaxis_title="Average Free Cash Flow (₹ Cr)"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True,
        key="sector_fcf"
    )

    # =====================================================
    # Debt Comparison
    # =====================================================

    st.divider()

    st.subheader("🏦 Average Debt / Equity")

    fig5 = px.bar(
        sector.sort_values(
            "Avg_Debt"
        ),
        x="broad_sector",
        y="Avg_Debt",
        color="Avg_Debt",
        text="Avg_Debt"
    )

    fig5.update_layout(
        height=500,
        xaxis_title="Sector",
        yaxis_title="Debt / Equity"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True,
        key="sector_debt"
    )

    # =====================================================
    # Sector Ranking
    # =====================================================

    st.divider()

    st.subheader("🏆 Sector Ranking")

    ranking = sector.sort_values(
        "Avg_Quality",
        ascending=False
    ).reset_index(drop=True)

    ranking.index += 1

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=False
    )

    # =====================================================
    # Best Performing Sector
    # =====================================================

    st.divider()

    st.subheader("⭐ Best Performing Sector")

    winner = sector.sort_values(
        "Avg_Quality",
        ascending=False
    ).iloc[0]

    col1, col2 = st.columns([3, 1])

    with col1:

        st.success(
            f"**{winner['broad_sector']}** has the highest average quality score."
        )

        st.write(f"Companies : {winner['Companies']}")
        st.write(f"Average ROE : {winner['Avg_ROE']:.2f}%")
        st.write(f"Average ROCE : {winner['Avg_ROCE']:.2f}%")
        st.write(f"Average Debt/Equity : {winner['Avg_Debt']:.2f}")
        st.write(f"Average Free Cash Flow : ₹ {winner['Avg_FCF']:,.0f} Cr")

    with col2:

        st.metric(
            "Quality Score",
            f"{winner['Avg_Quality']:.2f}"
        )

    # =====================================================
    # Sector Summary Table
    # =====================================================

    st.divider()

    st.subheader("📋 Complete Sector Summary")

    st.dataframe(
        sector.sort_values(
            "Avg_Quality",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # Footer
    # =====================================================

    st.divider()

    st.caption(
        "Nifty 100 Analytics Dashboard • Sprint 4 • Sector Analysis"
    )