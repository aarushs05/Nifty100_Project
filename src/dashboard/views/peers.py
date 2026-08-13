import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.utils.db import (
    get_company_profile,
    get_peer_groups,
    get_peers,
    get_ratios,
)


def show():

    st.title("🤝 Peer Comparison")

    groups = get_peer_groups()

    if groups.empty:
        st.warning("No peer groups available.")
        return

    peer_group = st.selectbox("Select Peer Group", groups["peer_group_name"].tolist())

    peers = get_peers(peer_group)

    if peers.empty:
        st.warning("No companies found.")
        return

    records = []

    for company_id in peers["company_id"]:

        profile = get_company_profile(company_id)
        ratios = get_ratios(company_id)

        if profile is None or ratios.empty:
            continue

        latest = ratios.sort_values("year").iloc[-1]

        records.append(
            {
                "Company": profile["company_name"],
                "ROE": latest["return_on_equity_pct"],
                "ROCE": latest["return_on_capital_employed_pct"],
                "Debt/Equity": latest["debt_to_equity"],
                "Revenue CAGR": latest["revenue_cagr_5yr"],
                "PAT CAGR": latest["pat_cagr_5yr"],
                "Quality Score": latest["composite_quality_score"],
            }
        )

    df = pd.DataFrame(records)

    if df.empty:
        st.warning("No comparison data available.")
        return

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("Companies", len(df))

    c2.metric("Average ROE", f"{df['ROE'].mean():.2f}%")

    c3.metric("Average Quality", f"{df['Quality Score'].mean():.2f}")

    st.divider()

    st.subheader("📋 Peer Comparison Table")

    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button("⬇ Download Comparison", csv, "peer_comparison.csv", "text/csv")
    # =====================================================
    # ROE vs ROCE Scatter
    # =====================================================

    st.divider()

    st.subheader("📈 ROE vs ROCE Comparison")

    fig = px.scatter(
        df,
        x="ROE",
        y="ROCE",
        color="Quality Score",
        size="Quality Score",
        hover_name="Company",
        text="Company",
    )

    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # Quality Ranking
    # =====================================================

    st.divider()

    st.subheader("🏆 Quality Score Ranking")

    quality = df.sort_values("Quality Score", ascending=False)

    fig = px.bar(
        quality,
        x="Company",
        y="Quality Score",
        color="Quality Score",
        text="Quality Score",
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # Revenue CAGR Comparison
    # =====================================================

    st.divider()

    st.subheader("📊 Revenue CAGR")

    fig = px.bar(
        df.sort_values("Revenue CAGR", ascending=False),
        x="Company",
        y="Revenue CAGR",
        text="Revenue CAGR",
        color="Revenue CAGR",
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # PAT CAGR Comparison
    # =====================================================

    st.divider()

    st.subheader("💰 PAT CAGR")

    fig = px.bar(
        df.sort_values("PAT CAGR", ascending=False),
        x="Company",
        y="PAT CAGR",
        text="PAT CAGR",
        color="PAT CAGR",
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # Financial Ratios Heatmap
    # =====================================================

    st.divider()

    st.subheader("📋 Peer Metrics")

    metrics = df.set_index("Company")

    st.dataframe(metrics, use_container_width=True, height=400)

    # =====================================================
    # Best Company
    # =====================================================

    st.divider()

    st.subheader("⭐ Best Overall Performer")

    winner = df.sort_values("Quality Score", ascending=False).iloc[0]

    c1, c2 = st.columns([2, 1])

    with c1:

        st.success(
            f"**{winner['Company']}** has the highest composite quality score in this peer group."
        )

        st.write(f"ROE : {winner['ROE']:.2f}%")
        st.write(f"ROCE : {winner['ROCE']:.2f}%")
        st.write(f"Debt/Equity : {winner['Debt/Equity']:.2f}")
        st.write(f"Revenue CAGR : {winner['Revenue CAGR']:.2f}%")
        st.write(f"PAT CAGR : {winner['PAT CAGR']:.2f}%")

    with c2:

        st.metric("Quality Score", f"{winner['Quality Score']:.2f}")

    # =====================================================
    # Ranking Table
    # =====================================================

    st.divider()

    st.subheader("🏅 Overall Ranking")

    ranking = df.sort_values("Quality Score", ascending=False).reset_index(drop=True)

    ranking.index += 1

    st.dataframe(ranking, use_container_width=True)

    # =====================================================
    # Footer
    # =====================================================

    st.divider()

    st.caption("Nifty 100 Analytics Dashboard • Sprint 4 • Peer Comparison")
    # =====================================================

    # =====================================================
