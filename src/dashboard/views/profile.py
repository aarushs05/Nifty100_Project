import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.dashboard.utils.db import (
    get_analysis,
    get_bs,
    get_cf,
    get_companies,
    get_company_profile,
    get_market_cap,
    get_pl,
    get_pros_cons,
    get_ratios,
    get_reports,
)


def show():

    st.title("🏢 Company Profile")

    # =====================================================
    # Company Selection
    # =====================================================

    companies = get_companies()

    if companies.empty:
        st.error("No companies found.")
        return

    company = st.selectbox("Select Company", companies["company_name"].tolist())

    company_id = companies.loc[companies["company_name"] == company, "id"].iloc[0]

    # =====================================================
    # Load Data
    # =====================================================

    profile = get_company_profile(company_id)

    if profile is None:
        st.warning("Company profile unavailable.")
        return

    ratios = get_ratios(company_id)
    analysis = get_analysis(company_id)
    pl = get_pl(company_id)
    bs = get_bs(company_id)
    cf = get_cf(company_id)
    market = get_market_cap(company_id)
    pros_cons = get_pros_cons(company_id)
    reports = get_reports(company_id)

    # =====================================================
    # Company Information
    # =====================================================

    st.divider()

    left, right = st.columns([1, 3])

    with left:

        logo = profile["company_logo"]

        if pd.notna(logo) and str(logo).strip():
            st.image(str(logo), width=130)

    with right:

        st.subheader(profile["company_name"])

        about = profile["about_company"]
        if pd.notna(about):
            st.write(about)

        website = profile["website"]
        if pd.notna(website):
            st.markdown(f"🌐 **Website:** {website}")

        nse = profile["nse_profile"]
        if pd.notna(nse):
            st.markdown(f"📈 **NSE:** {nse}")

        bse = profile["bse_profile"]
        if pd.notna(bse):
            st.markdown(f"🏦 **BSE:** {bse}")

    # =====================================================
    # Snapshot Cards
    # =====================================================

    st.divider()

    st.subheader("📊 Company Snapshot")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Book Value", f"{profile['book_value']:,.2f}")

    with c2:
        st.metric("Face Value", f"{profile['face_value']:,.2f}")

    with c3:
        st.metric("ROE %", f"{profile['roe_percentage']:.2f}")

    with c4:
        st.metric("ROCE %", f"{profile['roce_percentage']:.2f}")

    # =====================================================
    # Financial Performance
    # =====================================================

    st.divider()

    st.subheader("📈 Financial Performance")

    if not pl.empty:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(x=pl["year"], y=pl["sales"], mode="lines+markers", name="Sales")
        )

        fig.add_trace(
            go.Scatter(
                x=pl["year"],
                y=pl["net_profit"],
                mode="lines+markers",
                name="Net Profit",
            )
        )

        fig.update_layout(
            title="Sales vs Net Profit",
            xaxis_title="Year",
            yaxis_title="₹ Crore",
            hovermode="x unified",
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.bar(pl, x="year", y="eps", text="eps", title="EPS Trend")

        fig2.update_layout(height=450)

        st.plotly_chart(fig2, use_container_width=True)

    else:

        st.info("Profit & Loss data unavailable.")

        # =====================================================
    # Financial Ratios
    # =====================================================

    st.divider()

    st.subheader("📊 Financial Ratios")

    if not ratios.empty:

        col1, col2 = st.columns(2)

        with col1:

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=ratios["year"],
                    y=ratios["return_on_equity_pct"],
                    mode="lines+markers",
                    name="ROE",
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=ratios["year"],
                    y=ratios["return_on_capital_employed_pct"],
                    mode="lines+markers",
                    name="ROCE",
                )
            )

            fig.update_layout(
                title="ROE vs ROCE",
                xaxis_title="Year",
                yaxis_title="Percentage",
                hovermode="x unified",
                height=450,
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=ratios["year"], y=ratios["debt_to_equity"], name="Debt to Equity"
                )
            )

            fig.update_layout(
                title="Debt to Equity",
                xaxis_title="Year",
                yaxis_title="Ratio",
                height=450,
            )

            st.plotly_chart(fig, use_container_width=True)

    else:

        st.info("Financial ratio data unavailable.")

        # =====================================================
    # Margin Analysis
    # =====================================================

    if not ratios.empty:

        col1, col2 = st.columns(2)

        with col1:

            fig = px.line(
                ratios,
                x="year",
                y="net_profit_margin_pct",
                markers=True,
                title="Net Profit Margin",
            )

            fig.update_layout(height=420)

            st.plotly_chart(fig, use_container_width=True)

        with col2:

            fig = px.line(
                ratios,
                x="year",
                y="operating_profit_margin_pct",
                markers=True,
                title="Operating Profit Margin",
            )

            fig.update_layout(height=420)

            st.plotly_chart(fig, use_container_width=True)

        # =====================================================
    # Balance Sheet Overview
    # =====================================================

    st.divider()

    st.subheader("🏦 Balance Sheet Overview")

    if not bs.empty:

        col1, col2 = st.columns(2)

        with col1:

            fig = go.Figure()

            fig.add_trace(
                go.Bar(x=bs["year"], y=bs["total_assets"], name="Total Assets")
            )

            fig.add_trace(
                go.Bar(
                    x=bs["year"], y=bs["total_liabilities"], name="Total Liabilities"
                )
            )

            fig.update_layout(
                barmode="group",
                title="Assets vs Liabilities",
                xaxis_title="Year",
                yaxis_title="₹ Crore",
                height=450,
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=bs["year"],
                    y=bs["equity_capital"],
                    mode="lines+markers",
                    name="Equity Capital",
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=bs["year"],
                    y=bs["borrowings"],
                    mode="lines+markers",
                    name="Borrowings",
                )
            )

            fig.update_layout(
                title="Equity vs Borrowings",
                xaxis_title="Year",
                yaxis_title="₹ Crore",
                height=450,
            )

            st.plotly_chart(fig, use_container_width=True)

    else:

        st.info("Balance Sheet data unavailable.")

        # =====================================================
    # Cash Flow Analysis
    # =====================================================

    st.divider()

    st.subheader("💰 Cash Flow Analysis")

    if not cf.empty:

        fig = go.Figure()

        fig.add_trace(
            go.Bar(x=cf["year"], y=cf["operating_activity"], name="Operating")
        )

        fig.add_trace(
            go.Bar(x=cf["year"], y=cf["investing_activity"], name="Investing")
        )

        fig.add_trace(
            go.Bar(x=cf["year"], y=cf["financing_activity"], name="Financing")
        )

        fig.update_layout(
            barmode="group",
            title="Cash Flow Activities",
            xaxis_title="Year",
            yaxis_title="₹ Crore",
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.info("Cash Flow data unavailable.")

        # =====================================================
    # Market Valuation
    # =====================================================

    st.divider()

    st.subheader("💹 Market Valuation")

    if not market.empty:

        latest = market.sort_values("year").iloc[-1]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Market Cap", f"{latest['market_cap_crore']:,.0f} Cr")

        c2.metric("Enterprise Value", f"{latest['enterprise_value_crore']:,.0f} Cr")

        c3.metric("P/E Ratio", f"{latest['pe_ratio']:.2f}")

        c4.metric("P/B Ratio", f"{latest['pb_ratio']:.2f}")

    else:

        st.info("Market valuation data unavailable.")
        # =====================================================
    # Pros & Cons
    # =====================================================

    st.divider()

    st.subheader("⭐ Pros & Cons")

    if not pros_cons.empty:

        col1, col2 = st.columns(2)

        with col1:

            st.success("Pros")

            for item in pros_cons["pros"].dropna():
                st.markdown(f"• {item}")

        with col2:

            st.error("Cons")

            for item in pros_cons["cons"].dropna():
                st.markdown(f"• {item}")

    else:

        st.info("Pros & Cons not available.")
        # =====================================================
    # Annual Reports
    # =====================================================

    st.divider()

    st.subheader("📄 Annual Reports")

    if not reports.empty:

        reports = reports.sort_values("Year", ascending=False)

        for _, row in reports.iterrows():

            st.markdown(f"**{row['Year']}**  \n{row['Annual_Report']}")

    else:

        st.info("No annual reports available.")
        # =====================================================
    # Financial Statements
    # =====================================================

    st.divider()

    with st.expander("📑 Profit & Loss"):

        st.dataframe(pl, use_container_width=True, hide_index=True)

    with st.expander("🏦 Balance Sheet"):

        st.dataframe(bs, use_container_width=True, hide_index=True)

    with st.expander("💰 Cash Flow"):

        st.dataframe(cf, use_container_width=True, hide_index=True)

    with st.expander("📊 Financial Ratios"):

        st.dataframe(ratios, use_container_width=True, hide_index=True)
        # =====================================================
    # Analysis Summary
    # =====================================================

    st.divider()

    st.subheader("📈 Analysis Summary")

    if not analysis.empty:

        st.dataframe(analysis, use_container_width=True, hide_index=True)

    else:

        st.info("No analysis available.")
        # =====================================================
    # Footer
    # =====================================================

    st.divider()
    st.divider()

    st.divider()


st.caption("Nifty 100 Analytics Dashboard • Sprint 5 • Company Profile")
