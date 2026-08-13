import plotly.express as px
import streamlit as st

from src.dashboard.utils.db import get_dashboard_data


def show():

    st.title("💰 Capital Allocation Analysis")

    df = get_dashboard_data()
    st.write(df.columns.tolist())
    if df.empty:
        st.warning("No capital allocation data available.")
        return

    # =====================================================
    # Keep Latest Year
    # =====================================================

    latest_year = df["year"].max()

    df = df[df["year"] == latest_year].copy()

    # =====================================================
    # KPI Cards
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Companies", len(df))

    c2.metric("Average ROCE", f"{df['return_on_capital_employed_pct'].mean():.2f}%")

    c3.metric("Average ROE", f"{df['return_on_equity_pct'].mean():.2f}%")

    c4.metric("Average FCF", f"{df['free_cash_flow_cr'].mean():,.0f} Cr")

    # =====================================================
    # ROCE Distribution
    # =====================================================

    st.divider()

    st.subheader("📈 ROCE Distribution")

    fig1 = px.histogram(
        df,
        x="return_on_capital_employed_pct",
        nbins=20,
        color_discrete_sequence=["royalblue"],
    )

    fig1.update_layout(height=500)

    st.plotly_chart(fig1, use_container_width=True, key="capital_roce_distribution")

    # =====================================================
    # ROE vs Free Cash Flow
    # =====================================================

    st.divider()

    st.subheader("💵 ROE vs Free Cash Flow")

    fig2 = px.scatter(
        df,
        x="return_on_equity_pct",
        y="free_cash_flow_cr",
        color="composite_quality_score",
        size="composite_quality_score",
        hover_name="company_name",
    )

    fig2.update_layout(height=550)

    st.plotly_chart(fig2, use_container_width=True, key="capital_roe_fcf")

    # =====================================================
    # Buyback Yield
    # =====================================================

    st.divider()

    st.subheader("📊 Buyback Yield")

    if "buyback_yield_pct" in df.columns:

        fig3 = px.bar(
            df.sort_values("buyback_yield_pct", ascending=False).head(20),
            x="company_name",
            y="buyback_yield_pct",
            color="buyback_yield_pct",
            text="buyback_yield_pct",
        )

        fig3.update_layout(height=500)

        st.plotly_chart(fig3, use_container_width=True, key="capital_buyback")

    # =====================================================
    # Dividend Yield
    # =====================================================

    if "dividend_yield_pct" in df.columns:

        st.divider()

        st.subheader("💸 Dividend Yield")

        fig4 = px.bar(
            df.sort_values("dividend_yield_pct", ascending=False).head(20),
            x="company_name",
            y="dividend_yield_pct",
            color="dividend_yield_pct",
            text="dividend_yield_pct",
        )

        fig4.update_layout(height=500)

        st.plotly_chart(fig4, use_container_width=True, key="capital_dividend")

    # =====================================================
    # Top Capital Allocators
    # =====================================================

    st.divider()

    st.subheader("🏆 Top Capital Allocators")

    ranking = df.sort_values("composite_quality_score", ascending=False).head(20)

    fig5 = px.bar(
        ranking,
        x="company_name",
        y="composite_quality_score",
        color="composite_quality_score",
        text="composite_quality_score",
    )

    fig5.update_layout(height=550)

    st.plotly_chart(fig5, use_container_width=True, key="capital_quality")

    # =====================================================
    # Best Capital Allocator
    # =====================================================

    st.divider()

    st.subheader("⭐ Best Capital Allocator")

    winner = df.sort_values("composite_quality_score", ascending=False).iloc[0]

    col1, col2 = st.columns([3, 1])

    with col1:

        st.success(
            f"**{winner['company_name']}** has the highest capital allocation score."
        )

        st.write(f"ROE : {winner['return_on_equity_pct']:.2f}%")

        st.write(f"ROCE : {winner['return_on_capital_employed_pct']:.2f}%")

        st.write(f"Free Cash Flow : ₹ {winner['free_cash_flow_cr']:,.0f} Cr")

        if "buyback_yield_pct" in df.columns:
            st.write(f"Buyback Yield : {winner['buyback_yield_pct']:.2f}%")

        if "dividend_yield_pct" in df.columns:
            st.write(f"Dividend Yield : {winner['dividend_yield_pct']:.2f}%")

    with col2:

        st.metric("Quality Score", f"{winner['composite_quality_score']:.2f}")

    # =====================================================
    # Capital Allocation Table
    # =====================================================

    st.divider()

    st.subheader("📋 Company Capital Allocation")

    columns = [
        "company_name",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "free_cash_flow_cr",
        "composite_quality_score",
    ]

    if "buyback_yield_pct" in df.columns:
        columns.append("buyback_yield_pct")

    if "dividend_yield_pct" in df.columns:
        columns.append("dividend_yield_pct")

    st.dataframe(
        df[columns].sort_values("composite_quality_score", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    # =====================================================
    # Footer
    # =====================================================

    st.divider()

    st.caption("Nifty 100 Analytics Dashboard • Sprint 4 • Capital Allocation")
