"""
Sprint 6 - Day 37
Cluster profiling, correlation analysis, outlier detection
and portfolio statistics.
"""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "data" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"
REPORTS_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 10 CORE KPIs
# ============================================================

KPIS = [
    "return_on_equity_pct",
    "return_on_assets_pct",
    "return_on_capital_employed_pct",
    "debt_to_equity",
    "interest_coverage",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "asset_turnover",
    "fcf_conversion_pct",
    "dividend_payout_ratio_pct",
]


# ============================================================
# CLUSTER NAMES
# ============================================================

# These names are based on the actual company membership
# observed in your KMeans results.

CLUSTER_NAMES = {
    0: "Diversified Core Compounders",
    1: "Financial Growth & Leverage",
    2: "Defense & Capital Goods Leaders",
    3: "Healthcare Outlier",
    4: "High-Quality Leaders",
}


# ============================================================
# LOAD DATA
# ============================================================


def load_database():
    """Load all required Day 37 data from SQLite."""

    conn = sqlite3.connect(DB_PATH)

    companies = pd.read_sql_query(
        """
        SELECT
            id AS company_id,
            company_name
        FROM companies
        """,
        conn,
    )

    ratios = pd.read_sql_query(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn,
    )

    sectors = pd.read_sql_query(
        """
        SELECT
            company_id,
            broad_sector,
            sub_sector,
            market_cap_category
        FROM sectors
        """,
        conn,
    )

    conn.close()

    return companies, ratios, sectors


# ============================================================
# LATEST DATA
# ============================================================


def get_latest_company_data(
    companies,
    ratios,
    sectors,
):
    """Build latest available KPI dataset for all 92 companies."""

    ratios = ratios.copy()
    # --------------------------------------------------------
    # Calculate 5-year FCF CAGR
    #
    # financial_ratios contains free_cash_flow_cr but does
    # not contain fcf_cagr_5yr, so calculate it here.
    # --------------------------------------------------------

    ratios["year"] = pd.to_numeric(
        ratios["year"],
        errors="coerce",
    )

    ratios["free_cash_flow_cr"] = pd.to_numeric(
        ratios["free_cash_flow_cr"],
        errors="coerce",
    )

    ratios = ratios.sort_values(["company_id", "year"])

    fcf_cagr_rows = []

    for company_id, group in ratios.groupby("company_id"):

        group = group.dropna(subset=["year"]).sort_values("year")

        fcf_by_year = group.drop_duplicates("year").set_index("year")[
            "free_cash_flow_cr"
        ]

        for year in group["year"].unique():

            year = int(year)
            start_year = year - 5

            if start_year not in fcf_by_year.index:
                cagr = np.nan

            else:

                start_value = fcf_by_year.loc[start_year]
                end_value = fcf_by_year.loc[year]

                if (
                    pd.notna(start_value)
                    and pd.notna(end_value)
                    and start_value > 0
                    and end_value > 0
                ):
                    cagr = ((end_value / start_value) ** (1 / 5) - 1) * 100
                else:
                    cagr = np.nan

            fcf_cagr_rows.append(
                {
                    "company_id": company_id,
                    "year": year,
                    "fcf_cagr_5yr": cagr,
                }
            )

    fcf_cagr = pd.DataFrame(fcf_cagr_rows)

    ratios = ratios.merge(
        fcf_cagr,
        on=["company_id", "year"],
        how="left",
    )

    ratios = ratios.sort_values(["company_id", "year"])

    latest = ratios.groupby("company_id", as_index=False).tail(1).reset_index(drop=True)

    # Start with ALL companies.
    result = companies[
        [
            "company_id",
            "company_name",
        ]
    ].drop_duplicates("company_id")

    result = result.merge(
        latest,
        on="company_id",
        how="left",
    )

    result = result.merge(
        sectors[
            [
                "company_id",
                "broad_sector",
                "sub_sector",
                "market_cap_category",
            ]
        ].drop_duplicates("company_id"),
        on="company_id",
        how="left",
    )

    return result


# ============================================================
# LOAD CLUSTERS
# ============================================================


def load_clusters():
    """Load cluster assignments generated on Day 36."""

    path = OUTPUT_DIR / "cluster_labels.csv"

    if not path.exists():
        raise FileNotFoundError(f"Missing clustering output: {path}")

    return pd.read_csv(path)


# ============================================================
# CLUSTER PROFILE
# ============================================================


def create_cluster_profiles(
    latest,
    clusters,
):
    """Calculate mean and median of the five clustering features."""

    clustering_features = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct",
    ]

    df = latest.merge(
        clusters[
            [
                "company_id",
                "cluster_id",
            ]
        ],
        on="company_id",
        how="inner",
    )

    mean_profile = df.groupby("cluster_id")[clustering_features].mean()

    median_profile = df.groupby("cluster_id")[clustering_features].median()

    mean_profile["cluster_name"] = mean_profile.index.map(CLUSTER_NAMES)

    median_profile["cluster_name"] = median_profile.index.map(CLUSTER_NAMES)

    return (
        df,
        mean_profile,
        median_profile,
    )


# ============================================================
# SAVE CLUSTER PROFILES
# ============================================================


def save_cluster_profiles(
    mean_profile,
    median_profile,
):
    """Save cluster mean and median profiles."""

    mean_path = OUTPUT_DIR / "cluster_profile_mean.csv"

    median_path = OUTPUT_DIR / "cluster_profile_median.csv"

    mean_profile.to_csv(mean_path)

    median_profile.to_csv(median_path)

    print(f"Saved: {mean_path}")

    print(f"Saved: {median_path}")


# ============================================================
# UPDATE CLUSTER LABELS
# ============================================================


def update_cluster_labels(
    clusters,
):
    """Replace initial cluster names with reviewed financial archetypes."""

    result = clusters.copy()

    result["cluster_name"] = result["cluster_id"].map(CLUSTER_NAMES)

    path = OUTPUT_DIR / "cluster_labels.csv"

    result.to_csv(
        path,
        index=False,
    )

    print(f"Updated cluster labels: {path}")

    return result


# ============================================================
# CORRELATION HEATMAP
# ============================================================


def create_correlation_heatmap(
    latest,
):
    """Create Pearson correlation heatmap for 10 core KPIs."""

    print("\nCreating correlation heatmap...")

    corr_data = latest[KPIS].copy()

    # Numeric conversion
    for column in KPIS:
        corr_data[column] = pd.to_numeric(
            corr_data[column],
            errors="coerce",
        )

    # Use median imputation only for correlation matrix
    # so the matrix can include the full company universe.
    corr_data = corr_data.fillna(corr_data.median())

    correlation = corr_data.corr(method="pearson")

    plt.figure(figsize=(13, 10))

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        square=True,
    )

    plt.title("Pearson Correlation Matrix - 10 Core KPIs")

    plt.xticks(
        rotation=45,
        ha="right",
    )

    plt.yticks(
        rotation=0,
    )

    plt.tight_layout()

    output_path = REPORTS_DIR / "correlation_heatmap.png"

    plt.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Correlation heatmap saved: {output_path}")

    return correlation


# ============================================================
# OUTLIER DETECTION
# ============================================================


def calculate_outliers(
    latest,
):
    """Detect KPI outliers using sector-level Z-scores above 3."""

    print("\nCalculating sector-level outliers...")

    df = latest.copy()

    outliers = []

    for sector, sector_df in df.groupby(
        "broad_sector",
        dropna=False,
    ):

        # If sector is missing, skip.
        if pd.isna(sector):
            continue

        for kpi in KPIS:

            values = pd.to_numeric(
                sector_df[kpi],
                errors="coerce",
            )

            mean = values.mean()

            std = values.std(ddof=0)

            # Cannot calculate Z-score
            # if there is no variation.
            if pd.isna(std) or std == 0:
                continue

            z_scores = (values - mean) / std

            for index, z_score in z_scores.items():

                if pd.notna(z_score) and abs(z_score) > 3:

                    row = df.loc[index]

                    outliers.append(
                        {
                            "company_id": row["company_id"],
                            "company_name": row["company_name"],
                            "broad_sector": sector,
                            "year": row.get(
                                "year",
                                np.nan,
                            ),
                            "field": kpi,
                            "value": row[kpi],
                            "sector_mean": mean,
                            "sector_std": std,
                            "z_score": z_score,
                            "issue": ("Absolute sector " "Z-score > 3"),
                        }
                    )

    result = pd.DataFrame(outliers)

    if not result.empty:
        result = result.sort_values(
            "z_score",
            key=lambda x: abs(x),
            ascending=False,
        )

    path = OUTPUT_DIR / "outlier_report.csv"

    result.to_csv(
        path,
        index=False,
    )

    print(f"Outlier records: {len(result)}")

    print(f"Outlier report saved: {path}")

    return result


# ============================================================
# PORTFOLIO STATISTICS
# ============================================================


def create_portfolio_statistics(
    latest,
):
    """Create P10-P90, mean and standard deviation for 10 KPIs."""

    print("\nCreating portfolio statistics...")

    df = latest[
        [
            "company_id",
            *KPIS,
        ]
    ].copy()

    # Convert all KPI columns to numeric
    for kpi in KPIS:
        df[kpi] = pd.to_numeric(
            df[kpi],
            errors="coerce",
        )

    # Median imputation allows the statistics table
    # to represent the complete 92-company universe.
    for kpi in KPIS:

        median = df[kpi].median()

        df[kpi] = df[kpi].fillna(median)

    rows = []

    for kpi in KPIS:

        values = df[kpi]

        rows.append(
            {
                "kpi": kpi,
                "P10": values.quantile(0.10),
                "P25": values.quantile(0.25),
                "P50": values.quantile(0.50),
                "P75": values.quantile(0.75),
                "P90": values.quantile(0.90),
                "Mean": values.mean(),
                "Std": values.std(),
            }
        )

    result = pd.DataFrame(rows)

    path = OUTPUT_DIR / "portfolio_stats.csv"

    result.to_csv(
        path,
        index=False,
    )

    print(f"Portfolio statistics saved: {path}")

    return result


# ============================================================
# CLUSTER MEMBERSHIP REPORT
# ============================================================


def create_cluster_membership_report(
    latest,
    clusters,
):
    """Create a readable cluster membership CSV."""

    result = latest.merge(
        clusters[
            [
                "company_id",
                "cluster_id",
                "cluster_name",
                "distance_from_centroid",
            ]
        ],
        on="company_id",
        how="left",
    )

    columns = [
        "company_id",
        "company_name",
        "broad_sector",
        "sub_sector",
        "market_cap_category",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid",
    ]

    result = result[[column for column in columns if column in result.columns]]

    result = result.sort_values(
        [
            "cluster_id",
            "distance_from_centroid",
        ]
    )

    path = OUTPUT_DIR / "cluster_membership_report.csv"

    result.to_csv(
        path,
        index=False,
    )

    print(f"Cluster membership report saved: {path}")


# ============================================================
# MAIN
# ============================================================


def main():
    """Run the complete Day 37 statistics pipeline."""

    print("=" * 80)
    print("SPRINT 6 - DAY 37")
    print("CLUSTER PROFILING & STATISTICS")
    print("=" * 80)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    (
        companies,
        ratios,
        sectors,
    ) = load_database()

    clusters = load_clusters()

    print(f"\nCompanies: {companies['company_id'].nunique()}")

    print(f"Cluster records: {len(clusters)}")

    # --------------------------------------------------------
    # Latest company data
    # --------------------------------------------------------

    latest = get_latest_company_data(
        companies,
        ratios,
        sectors,
    )

    print(f"Latest company dataset: {len(latest)} rows")

    # --------------------------------------------------------
    # Cluster profiles
    # --------------------------------------------------------

    (
        _clustered_data,
        mean_profile,
        median_profile,
    ) = create_cluster_profiles(
        latest,
        clusters,
    )

    print("\nCLUSTER MEAN PROFILES")

    print(mean_profile.round(3).to_string())

    print("\nCLUSTER MEDIAN PROFILES")

    print(median_profile.round(3).to_string())

    save_cluster_profiles(
        mean_profile,
        median_profile,
    )

    # --------------------------------------------------------
    # Update names
    # --------------------------------------------------------

    clusters = update_cluster_labels(clusters)

    # --------------------------------------------------------
    # Cluster membership
    # --------------------------------------------------------

    create_cluster_membership_report(
        latest,
        clusters,
    )

    # --------------------------------------------------------
    # Correlation heatmap
    # --------------------------------------------------------

    create_correlation_heatmap(latest)

    # --------------------------------------------------------
    # Outliers
    # --------------------------------------------------------

    calculate_outliers(latest)

    # --------------------------------------------------------
    # Portfolio statistics
    # --------------------------------------------------------

    create_portfolio_statistics(latest)

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    labels = pd.read_csv(OUTPUT_DIR / "cluster_labels.csv")

    print("\n" + "=" * 80)

    print("DAY 37 VALIDATION")

    print("=" * 80)

    print(f"Cluster rows: {len(labels)}")

    print(f"Unique companies: " f"{labels['company_id'].nunique()}")

    print(f"Clusters: " f"{labels['cluster_id'].nunique()}")

    print("\nCluster counts:")

    print(
        labels.groupby(
            [
                "cluster_id",
                "cluster_name",
            ]
        )
        .size()
        .to_string()
    )

    # --------------------------------------------------------
    # Required files
    # --------------------------------------------------------

    required_files = [
        OUTPUT_DIR / "cluster_labels.csv",
        OUTPUT_DIR / "cluster_profile_mean.csv",
        OUTPUT_DIR / "cluster_profile_median.csv",
        OUTPUT_DIR / "outlier_report.csv",
        OUTPUT_DIR / "portfolio_stats.csv",
        OUTPUT_DIR / "cluster_membership_report.csv",
        REPORTS_DIR / "correlation_heatmap.png",
    ]

    print("\nRequired files:")

    all_present = True

    for path in required_files:

        exists = path.exists()

        print(f"{'✓' if exists else '✗'} {path}")

        if not exists:
            all_present = False

    if (
        len(labels) == 92
        and labels["company_id"].nunique() == 92
        and labels["cluster_id"].nunique() == 5
        and all_present
    ):

        print("\nDAY 37 VALIDATION PASSED")

    else:

        raise ValueError("Day 37 validation failed.")

    print("\n" + "=" * 80)

    print("DAY 37 COMPLETE")

    print("=" * 80)


if __name__ == "__main__":
    main()
