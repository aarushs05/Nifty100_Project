"""
Sprint 6 - KMeans Financial Clustering.

Clusters all 92 companies into five financial archetypes using:

1. Return on Equity
2. Debt to Equity
3. Revenue CAGR - 5 year
4. Free Cash Flow CAGR - 5 year
5. Operating Profit Margin

Processing:
    SQLite database
        ↓
    Latest available company data
        ↓
    Calculate 5-year FCF CAGR
        ↓
    Join all 92 companies
        ↓
    Join sector information
        ↓
    Sector-median imputation
        ↓
    Overall-median fallback
        ↓
    StandardScaler
        ↓
    KMeans (k=5, random_state=42)
        ↓
    Cluster labels + centroid distance
        ↓
    CSV outputs + elbow plot
"""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "data" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"
REPORTS_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CLUSTERING FEATURES
# ============================================================

FEATURES = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct",
]


# ============================================================
# LOAD DATABASE DATA
# ============================================================


def load_data():
    """Load companies, sectors, financial ratios and cash-flow data."""

    print("\nLoading database...")

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)

    try:
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
            SELECT
                company_id,
                year,
                return_on_equity_pct,
                debt_to_equity,
                revenue_cagr_5yr,
                operating_profit_margin_pct,
                free_cash_flow_cr
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

        cashflow = pd.read_sql_query(
            """
            SELECT
                company_id,
                year,
                operating_activity,
                investing_activity,
                financing_activity,
                net_cash_flow
            FROM cashflow
            """,
            conn,
        )

    finally:
        conn.close()

    print(f"Companies loaded: {companies['company_id'].nunique()}")
    print(f"Financial ratio rows: {len(ratios)}")
    print(f"Sector rows: {len(sectors)}")
    print(f"Cash-flow rows: {len(cashflow)}")

    return companies, ratios, sectors, cashflow


# ============================================================
# CALCULATE FREE CASH FLOW CAGR
# ============================================================


def calculate_fcf_cagr_from_ratios(ratios):
    """
    Calculate five-year FCF CAGR using free_cash_flow_cr
    available in financial_ratios.
    """

    print("\nCalculating 5-year FCF CAGR...")

    df = ratios.copy()

    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce",
    )

    df["free_cash_flow_cr"] = pd.to_numeric(
        df["free_cash_flow_cr"],
        errors="coerce",
    )

    df = df.sort_values(["company_id", "year"])

    results = []

    for company_id, group in df.groupby("company_id"):

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

                # CAGR is meaningful only when both
                # beginning and ending values are positive.
                if (
                    pd.notna(start_value)
                    and pd.notna(end_value)
                    and start_value > 0
                    and end_value > 0
                ):

                    cagr = ((end_value / start_value) ** (1 / 5) - 1) * 100

                else:

                    cagr = np.nan

            results.append(
                {
                    "company_id": company_id,
                    "year": year,
                    "fcf_cagr_5yr": cagr,
                }
            )

    fcf_cagr = pd.DataFrame(results)

    result = df.merge(
        fcf_cagr,
        on=["company_id", "year"],
        how="left",
    )

    valid_count = result["fcf_cagr_5yr"].notna().sum()

    print(f"Valid FCF CAGR observations: {valid_count}")

    return result


# ============================================================
# SELECT LATEST AVAILABLE DATA
# ============================================================


def select_latest_data(ratios):
    """Select the latest available financial-ratio row for each company."""

    df = ratios.copy()

    df = df.sort_values(["company_id", "year"])

    latest = df.groupby("company_id", as_index=False).tail(1).reset_index(drop=True)

    return latest


# ============================================================
# BUILD COMPLETE 92-COMPANY DATASET
# ============================================================


def build_company_dataset(
    companies,
    latest_ratios,
    sectors,
):
    """Build a complete 92-company dataset including companies without ratios."""

    print("\nBuilding complete company universe...")

    # Start from companies table.
    # This guarantees all 92 companies remain.
    df = companies[
        [
            "company_id",
            "company_name",
        ]
    ].drop_duplicates("company_id")

    # Add latest ratio data.
    # Companies such as ATGL and SBIN may receive NaN values here.
    df = df.merge(
        latest_ratios,
        on="company_id",
        how="left",
    )

    # Add sector information.
    df = df.merge(
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

    print("Total companies in clustering dataset: " f"{df['company_id'].nunique()}")

    # Identify companies without financial ratio records.
    missing_ratio_companies = df[df["year"].isna()][
        [
            "company_id",
            "company_name",
            "broad_sector",
        ]
    ]

    if len(missing_ratio_companies) > 0:

        print("\nCompanies without financial-ratio records:")

        print(missing_ratio_companies.to_string(index=False))

    return df


# ============================================================
# SECTOR MEDIAN IMPUTATION
# ============================================================


def impute_missing_values(
    df,
    features,
):
    """Impute missing features using sector medians and overall medians."""

    print("\nMissing values BEFORE imputation:")

    print(df[features].isna().sum())

    result = df.copy()

    # --------------------------------------------------------
    # Sector median
    # --------------------------------------------------------

    for feature in features:

        result[feature] = result.groupby("broad_sector")[feature].transform(
            lambda x: x.fillna(x.median())
        )

    # --------------------------------------------------------
    # Overall median fallback
    # --------------------------------------------------------

    for feature in features:

        overall_median = result[feature].median()

        result[feature] = result[feature].fillna(overall_median)

    print("\nMissing values AFTER imputation:")

    print(result[features].isna().sum())

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    remaining_missing = result[features].isna().sum().sum()

    if remaining_missing > 0:

        raise ValueError(
            "Missing values remain after " "sector and overall median imputation."
        )

    return result


# ============================================================
# STANDARD SCALING
# ============================================================


def scale_features(df):
    """Standardize clustering features using StandardScaler."""

    print("\nApplying StandardScaler...")

    scaler = StandardScaler()

    X = df[FEATURES].astype(float)

    X_scaled = scaler.fit_transform(X)

    print("Scaled means:")

    print(
        np.round(
            X_scaled.mean(axis=0),
            6,
        )
    )

    print("Scaled standard deviations:")

    print(
        np.round(
            X_scaled.std(axis=0),
            6,
        )
    )

    return X_scaled, scaler


# ============================================================
# ELBOW METHOD
# ============================================================


def create_elbow_plot(X_scaled):
    """Calculate inertia for k=2 through k=10 and save elbow plot."""

    print("\nCalculating elbow curve...")

    k_values = list(range(2, 11))

    inertias = []

    for k in k_values:

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )

        model.fit(X_scaled)

        inertias.append(model.inertia_)

        print(f"k={k}: inertia={model.inertia_:.4f}")

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(9, 6))

    plt.plot(
        k_values,
        inertias,
        marker="o",
    )

    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Inertia")
    plt.title("KMeans Elbow Plot")

    plt.xticks(k_values)

    plt.grid(
        True,
        alpha=0.3,
    )

    plt.tight_layout()

    output_path = REPORTS_DIR / "elbow_plot.png"

    plt.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close()

    print("\nElbow plot saved to:")
    print(output_path)


# ============================================================
# KMEANS
# ============================================================


def run_kmeans(X_scaled):
    """Run reproducible five-cluster KMeans."""

    print("\nRunning final KMeans...")

    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10,
    )

    labels = model.fit_predict(X_scaled)

    return model, labels


# ============================================================
# DISTANCE FROM CENTROID
# ============================================================


def calculate_centroid_distances(
    X_scaled,
    model,
    labels,
):
    """Calculate Euclidean distance from each company's cluster centroid."""

    centroids = model.cluster_centers_

    distances = np.linalg.norm(
        X_scaled - centroids[labels],
        axis=1,
    )

    return distances


# ============================================================
# CLUSTER PROFILING
# ============================================================


def create_cluster_profiles(df):
    """Calculate mean and median financial profiles for each cluster."""

    mean_profile = df.groupby("cluster_id")[FEATURES].mean()

    median_profile = df.groupby("cluster_id")[FEATURES].median()

    return (
        mean_profile,
        median_profile,
    )


# ============================================================
# INITIAL CLUSTER NAMES
# ============================================================


def assign_cluster_names(
    mean_profile,
):
    """
    Assign descriptive names using relative cluster characteristics.

    These names are initial financial archetypes and should be reviewed
    against the actual companies after clustering.
    """

    profiles = mean_profile.copy()

    # --------------------------------------------------------
    # Rank each cluster on important characteristics
    # --------------------------------------------------------

    profiles["roe_rank"] = profiles["return_on_equity_pct"].rank(
        ascending=False,
        method="first",
    )

    profiles["de_rank"] = profiles["debt_to_equity"].rank(
        ascending=True,
        method="first",
    )

    profiles["revenue_rank"] = profiles["revenue_cagr_5yr"].rank(
        ascending=False,
        method="first",
    )

    profiles["fcf_rank"] = profiles["fcf_cagr_5yr"].rank(
        ascending=False,
        method="first",
    )

    profiles["opm_rank"] = profiles["operating_profit_margin_pct"].rank(
        ascending=False,
        method="first",
    )

    # --------------------------------------------------------
    # Score quality/growth/defensive characteristics
    # --------------------------------------------------------

    profiles["quality_score"] = (
        profiles["roe_rank"].max()
        - profiles["roe_rank"]
        + profiles["opm_rank"].max()
        - profiles["opm_rank"]
        + profiles["de_rank"].max()
        - profiles["de_rank"]
    )

    profiles["growth_score"] = (
        profiles["revenue_rank"].max()
        - profiles["revenue_rank"]
        + profiles["fcf_rank"].max()
        - profiles["fcf_rank"]
    )

    profiles["defensive_score"] = (
        profiles["de_rank"].max()
        - profiles["de_rank"]
        + profiles["roe_rank"].max()
        - profiles["roe_rank"]
    )

    # --------------------------------------------------------
    # Determine archetypes
    # --------------------------------------------------------

    names = {}

    remaining = list(profiles.index)

    # Highest quality
    quality_cluster = max(
        remaining,
        key=lambda c: profiles.loc[c, "quality_score"],
    )

    names[quality_cluster] = "High-Quality Compounders"

    remaining.remove(quality_cluster)

    # Highest growth
    growth_cluster = max(
        remaining,
        key=lambda c: profiles.loc[c, "growth_score"],
    )

    names[growth_cluster] = "Emerging Growth"

    remaining.remove(growth_cluster)

    # Most defensive
    defensive_cluster = max(
        remaining,
        key=lambda c: profiles.loc[c, "defensive_score"],
    )

    names[defensive_cluster] = "Defensive Dividend Payers"

    remaining.remove(defensive_cluster)

    # Lowest quality / highest leverage
    distressed_cluster = min(
        remaining,
        key=lambda c: profiles.loc[c, "quality_score"],
    )

    names[distressed_cluster] = "Distressed or Turnaround"

    remaining.remove(distressed_cluster)

    # Remaining cluster
    if remaining:
        names[remaining[0]] = "Value Cyclicals"

    return names


# ============================================================
# SAVE OUTPUT
# ============================================================


def save_outputs(
    df,
    mean_profile,
    median_profile,
    cluster_names,
):
    """Save cluster labels and cluster profiling outputs."""

    # --------------------------------------------------------
    # Add cluster names
    # --------------------------------------------------------

    df["cluster_name"] = df["cluster_id"].map(cluster_names)

    # --------------------------------------------------------
    # Cluster labels
    # --------------------------------------------------------

    labels = df[
        [
            "company_id",
            "cluster_id",
            "cluster_name",
            "distance_from_centroid",
        ]
    ].copy()

    labels = labels.sort_values(
        [
            "cluster_id",
            "company_id",
        ]
    )

    labels_path = OUTPUT_DIR / "cluster_labels.csv"

    labels.to_csv(
        labels_path,
        index=False,
    )

    # --------------------------------------------------------
    # Mean profile
    # --------------------------------------------------------

    mean_output = mean_profile.copy()

    mean_output["cluster_name"] = mean_output.index.map(cluster_names)

    mean_path = OUTPUT_DIR / "cluster_profile_mean.csv"

    mean_output.to_csv(mean_path)

    # --------------------------------------------------------
    # Median profile
    # --------------------------------------------------------

    median_output = median_profile.copy()

    median_output["cluster_name"] = median_output.index.map(cluster_names)

    median_path = OUTPUT_DIR / "cluster_profile_median.csv"

    median_output.to_csv(median_path)

    print("\nOutput files created:")

    print(f"  {labels_path}")
    print(f"  {mean_path}")
    print(f"  {median_path}")

    return labels


# ============================================================
# VALIDATION
# ============================================================


def validate_results(
    labels,
):
    """Validate the final clustering output."""

    print("\nValidating clustering output...")

    row_count = len(labels)

    unique_companies = labels["company_id"].nunique()

    cluster_ids = sorted(labels["cluster_id"].unique())

    duplicate_count = labels["company_id"].duplicated().sum()

    missing_cluster_count = labels["cluster_id"].isna().sum()

    print(f"Rows: {row_count}")
    print(f"Unique companies: {unique_companies}")
    print(f"Cluster IDs: {cluster_ids}")
    print(f"Duplicate companies: {duplicate_count}")
    print(f"Missing cluster IDs: {missing_cluster_count}")

    # --------------------------------------------------------
    # Hard validation
    # --------------------------------------------------------

    if row_count != 92:
        raise ValueError(f"Expected 92 output rows, got {row_count}.")

    if unique_companies != 92:
        raise ValueError("Expected 92 unique companies.")

    if duplicate_count != 0:
        raise ValueError("Duplicate company IDs found.")

    if missing_cluster_count != 0:
        raise ValueError("Missing cluster IDs found.")

    if cluster_ids != [0, 1, 2, 3, 4]:
        raise ValueError(f"Expected clusters [0,1,2,3,4], " f"found {cluster_ids}.")

    print("\nVALIDATION PASSED")


# ============================================================
# MAIN
# ============================================================


def main():
    """Execute the complete Sprint 6 clustering pipeline."""

    print("=" * 70)
    print("SPRINT 6 - KMEANS CLUSTERING")
    print("=" * 70)

    print("\nDatabase:")
    print(DB_PATH)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    (
        companies,
        ratios,
        sectors,
        _cashflow,
    ) = load_data()

    # --------------------------------------------------------
    # Basic database validation
    # --------------------------------------------------------

    company_count = companies["company_id"].nunique()

    if company_count != 92:
        raise ValueError(
            f"Expected 92 companies in companies table, " f"found {company_count}."
        )

    print(f"\nCompanies in database: {company_count}")

    # --------------------------------------------------------
    # Calculate FCF CAGR
    # --------------------------------------------------------

    ratios = calculate_fcf_cagr_from_ratios(ratios)

    # --------------------------------------------------------
    # Latest ratio record
    # --------------------------------------------------------

    latest_ratios = select_latest_data(ratios)

    print(
        f"\nCompanies with latest ratio records: "
        f"{latest_ratios['company_id'].nunique()}"
    )

    # --------------------------------------------------------
    # Build complete 92-company dataset
    # --------------------------------------------------------

    df = build_company_dataset(
        companies,
        latest_ratios,
        sectors,
    )

    print("\nFinal clustering dataset:")

    print(f"Rows: {len(df)}")

    print("Unique companies: " f"{df['company_id'].nunique()}")

    # --------------------------------------------------------
    # Validate all 92 companies
    # --------------------------------------------------------

    if df["company_id"].nunique() != 92:
        raise ValueError("The clustering dataset does not contain all 92 companies.")

    # --------------------------------------------------------
    # Missing-value imputation
    # --------------------------------------------------------

    df = impute_missing_values(
        df,
        FEATURES,
    )

    # --------------------------------------------------------
    # StandardScaler
    # --------------------------------------------------------

    X_scaled, _scaler = scale_features(df)

    # --------------------------------------------------------
    # Elbow plot
    # --------------------------------------------------------

    create_elbow_plot(X_scaled)

    # --------------------------------------------------------
    # Final KMeans
    # --------------------------------------------------------

    model, labels = run_kmeans(X_scaled)

    df["cluster_id"] = labels

    # --------------------------------------------------------
    # Distance from centroid
    # --------------------------------------------------------

    df["distance_from_centroid"] = calculate_centroid_distances(
        X_scaled,
        model,
        labels,
    )

    # --------------------------------------------------------
    # Cluster profiles
    # --------------------------------------------------------

    (
        mean_profile,
        median_profile,
    ) = create_cluster_profiles(df)

    print("\nCluster MEAN profiles:")

    print(mean_profile.round(3).to_string())

    print("\nCluster MEDIAN profiles:")

    print(median_profile.round(3).to_string())

    # --------------------------------------------------------
    # Cluster names
    # --------------------------------------------------------

    cluster_names = assign_cluster_names(mean_profile)

    print("\nInitial cluster names:")

    for cluster_id in sorted(cluster_names):

        print(f"Cluster {cluster_id}: " f"{cluster_names[cluster_id]}")

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    labels = save_outputs(
        df,
        mean_profile,
        median_profile,
        cluster_names,
    )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    validate_results(labels)

    # --------------------------------------------------------
    # Cluster counts
    # --------------------------------------------------------

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
    # Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)

    print("DAY 36 CLUSTERING COMPLETE")

    print("=" * 70)

    print("Companies clustered: " f"{labels['company_id'].nunique()}")

    print("Clusters: " f"{labels['cluster_id'].nunique()}")

    print("\nRequired deliverables:")

    print(f"✓ {OUTPUT_DIR / 'cluster_labels.csv'}")

    print(f"✓ {REPORTS_DIR / 'elbow_plot.png'}")

    print(f"✓ {OUTPUT_DIR / 'cluster_profile_mean.csv'}")

    print(f"✓ {OUTPUT_DIR / 'cluster_profile_median.csv'}")

    print("\nNOTE:")

    print("Cluster names are initial financial archetypes.")

    print("Review the actual companies in each cluster " "before final sign-off.")


# ============================================================
# ENTRY POINT
# ============================================================


if __name__ == "__main__":
    main()
