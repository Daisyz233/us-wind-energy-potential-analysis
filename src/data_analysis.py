"""Visualization and clustering functions for the wind energy project."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans


def _save_or_show(filename: str | None = None, output_dir: str | Path = "visuals") -> None:
    """Save the current figure when a filename is provided; otherwise show it."""
    plt.tight_layout()
    if filename:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_dir / filename, dpi=300, bbox_inches="tight")
    plt.show()


def _total_wind_by_state(wind_df: pd.DataFrame) -> pd.Series:
    """Return total wind production by state, excluding date and national total."""
    return wind_df.drop(columns=["date", "united_states"], errors="ignore").sum(numeric_only=True).sort_values(ascending=False)


def _parse_wind_dates(date_series: pd.Series) -> pd.Series:
    """Parse dates that may look like 'Jan-01' or 'Jan 2001'."""
    cleaned = date_series.astype(str).str.replace("-", " ", regex=False)
    parsed = pd.to_datetime(cleaned, format="%b %y", errors="coerce")
    fallback = pd.to_datetime(cleaned, errors="coerce")
    return parsed.fillna(fallback)


# Analysis Part 1: Historical wind production

def plot_top10_states(wind_df: pd.DataFrame, save: bool = False) -> None:
    """Plot top 10 states by total wind energy production."""
    top10_states = _total_wind_by_state(wind_df).head(10)
    plt.figure(figsize=(8, 6))
    top10_states.plot(kind="bar")
    plt.title("Figure 1. Top 10 States by Total Wind Energy Production (2001–2023)")
    plt.ylabel("Total Production (GWh)")
    plt.xlabel("State")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    _save_or_show("figure_01_top_wind_production_bar.png" if save else None)


def plot_top10_pie(wind_df: pd.DataFrame, save: bool = False) -> None:
    """Plot top 10 states' share of total wind production."""
    top10_states = _total_wind_by_state(wind_df).head(10)
    plt.figure(figsize=(8, 8))
    top10_states.plot(kind="pie", autopct="%1.1f%%", startangle=140)
    plt.title("Figure 2. Top 10 States Share of Total Wind Production (2001–2023)")
    plt.ylabel("")
    _save_or_show("figure_02_top_wind_production_pie.png" if save else None)


def plot_bottom5_states(wind_df: pd.DataFrame, save: bool = False) -> None:
    """Plot bottom 5 states by total wind energy production."""
    bottom5_states = _total_wind_by_state(wind_df).tail(5)
    plt.figure(figsize=(8, 6))
    bottom5_states.plot(kind="bar")
    plt.title("Figure 3. Bottom 5 States by Total Wind Energy Production (2001–2023)")
    plt.ylabel("Total Production (GWh)")
    plt.xlabel("State")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    _save_or_show("figure_03_bottom_wind_production_bar.png" if save else None)


def plot_top5_growth_states(wind_df: pd.DataFrame, save: bool = False) -> None:
    """Plot the top 5 states by production growth from first to last year."""
    wind_df = wind_df.copy()
    wind_df["date"] = _parse_wind_dates(wind_df["date"])
    first_year = wind_df["date"].dt.year.min()
    last_year = wind_df["date"].dt.year.max()

    start = wind_df[wind_df["date"].dt.year == first_year]
    end = wind_df[wind_df["date"].dt.year == last_year]
    start_sum = start.drop(columns=["date", "united_states"], errors="ignore").sum(numeric_only=True)
    end_sum = end.drop(columns=["date", "united_states"], errors="ignore").sum(numeric_only=True)
    growth = (end_sum - start_sum).sort_values(ascending=False)

    plt.figure(figsize=(8, 6))
    growth.head(5).plot(kind="bar")
    plt.title(f"Figure 4. Top 5 Fastest Growing States ({first_year}–{last_year})")
    plt.ylabel("Growth in Production (GWh)")
    plt.xlabel("State")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    _save_or_show("figure_04_top5_growth_states.png" if save else None)


def plot_top5_growth_trend(wind_df: pd.DataFrame, save: bool = False) -> None:
    """Plot monthly wind production trends for top 5 fastest-growing states."""
    wind_df = wind_df.copy()
    wind_df["date"] = _parse_wind_dates(wind_df["date"])
    first_year = wind_df["date"].dt.year.min()
    last_year = wind_df["date"].dt.year.max()

    start = wind_df[wind_df["date"].dt.year == first_year]
    end = wind_df[wind_df["date"].dt.year == last_year]
    start_sum = start.drop(columns=["date", "united_states"], errors="ignore").sum(numeric_only=True)
    end_sum = end.drop(columns=["date", "united_states"], errors="ignore").sum(numeric_only=True)
    top5_states = (end_sum - start_sum).sort_values(ascending=False).head(5).index.tolist()

    plt.figure(figsize=(10, 7))
    for state in top5_states:
        plt.plot(wind_df["date"], wind_df[state], label=state)
    plt.title(f"Figure 5. Trend of Top 5 Fastest Growing States ({first_year}–{last_year})")
    plt.xlabel("Year")
    plt.ylabel("Wind Production (GWh)")
    plt.legend(title="State")
    plt.grid(True)
    _save_or_show("figure_05_top5_growth_trend.png" if save else None)


def analysis_one_a(wind_df: pd.DataFrame, save: bool = False) -> None:
    plot_top10_states(wind_df, save=save)
    plot_top10_pie(wind_df, save=save)


def analysis_one_b(wind_df: pd.DataFrame, save: bool = False) -> None:
    plot_top5_growth_states(wind_df, save=save)
    plot_top5_growth_trend(wind_df, save=save)


# Analysis Part 2: Tornado risk

def state_tornadoes(tornados_df: pd.DataFrame, save: bool = False) -> None:
    """Plot tornado event counts per state."""
    df_clean = tornados_df.dropna(subset=["st"])
    disaster_counts = df_clean["st"].value_counts().sort_values(ascending=False)
    plt.figure(figsize=(14, 6))
    disaster_counts.plot(kind="bar")
    plt.title("Figure 6. Total Number of Tornado Events per State (1950–2022)")
    plt.xlabel("State")
    plt.ylabel("Number of Tornadoes")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    _save_or_show("figure_06_tornado_events_by_state.png" if save else None)


def plot_mag_distribution_top5_fixed_states(tornados_df: pd.DataFrame, save: bool = False) -> None:
    """Plot tornado magnitude distribution for selected high-risk states."""
    df_clean = tornados_df.dropna(subset=["st", "mag"])
    top5_states = ["TX", "FL", "KS", "OK", "NE"]
    df_top5 = df_clean[df_clean["st"].isin(top5_states)]
    df_top5 = df_top5[df_top5["mag"].isin([0.0, 1.0, 2.0, 3.0])]
    mag_counts = pd.crosstab(df_top5["st"], df_top5["mag"])
    mag_counts["Total"] = mag_counts.sum(axis=1)
    mag_counts = mag_counts.sort_values(by="Total", ascending=False).drop(columns="Total")

    mag_counts.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="Set2")
    plt.title("Figure 7. Tornado Counts by Magnitude (0–3) in Top 5 States")
    plt.xlabel("State")
    plt.ylabel("Number of Tornadoes")
    plt.xticks(rotation=0)
    plt.legend(title="Magnitude", loc="upper right")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    _save_or_show("figure_07_tornado_magnitude_top5.png" if save else None)


def analysis_tornadoes(tornados_df: pd.DataFrame, save: bool = False) -> None:
    state_tornadoes(tornados_df, save=save)
    plot_mag_distribution_top5_fixed_states(tornados_df, save=save)


# Analysis Part 3: Correlation and clustering

def plot_correlation_matrix(merged_df: pd.DataFrame, save: bool = False) -> None:
    """Plot a correlation heatmap for key wind-development variables."""
    plt.figure(figsize=(8, 6))
    corr = merged_df[["Average Wind Speed (MPH)", "Potential Wind Capacity (MW)", "Tornadoes Disasters"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
    plt.xticks(rotation=10)
    plt.title("Figure 8. Correlation Matrix of Key Variables")
    _save_or_show("figure_08_correlation_matrix.png" if save else None)


def plot_potential_vs_windspeed(merged_df: pd.DataFrame, save: bool = False) -> None:
    """Plot potential wind capacity against average wind speed."""
    plt.figure(figsize=(8, 6))
    sns.regplot(x="Average Wind Speed (MPH)", y="Potential Wind Capacity (MW)", data=merged_df)
    plt.title("Figure 9. Potential Wind Yield vs Average Wind Speed")
    plt.grid(True)
    _save_or_show("figure_09_potential_vs_windspeed.png" if save else None)


def plot_potential_vs_disasters(merged_df: pd.DataFrame, save: bool = False) -> None:
    """Plot tornado event frequency against potential wind capacity."""
    plt.figure(figsize=(8, 6))
    sns.regplot(x="Potential Wind Capacity (MW)", y="Tornadoes Disasters", data=merged_df)
    plt.title("Figure 10. Disasters vs Potential Wind Yield")
    plt.grid(True)
    _save_or_show("figure_10_potential_vs_disasters.png" if save else None)


def determine_n_cluster(merged_df: pd.DataFrame, max_k: int = 10, save: bool = False) -> pd.DataFrame:
    """Plot the Elbow Method curve for K-Means cluster selection."""
    X = merged_df[["Average Wind Speed (MPH)", "Potential Wind Capacity (MW)", "Tornadoes Disasters"]].dropna()
    inertia = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
        kmeans.fit(X)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, max_k + 1), inertia, marker="o")
    plt.title("Figure 11. Elbow Method for Optimal k")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Inertia (Within-Cluster Sum of Squares)")
    plt.grid(True)
    _save_or_show("figure_11_elbow_method.png" if save else None)
    return X


def cluster_states(merged_df: pd.DataFrame, n_clusters: int = 3, save: bool = False) -> tuple[pd.DataFrame, list[str]]:
    """Cluster states by wind speed, potential capacity, and tornado risk."""
    X = merged_df[["Average Wind Speed (MPH)", "Potential Wind Capacity (MW)", "Tornadoes Disasters"]].dropna()
    clustered_df = merged_df.loc[X.index].copy()

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    clustered_df["Cluster"] = kmeans.fit_predict(X)

    plt.figure(figsize=(10, 8))
    sns.scatterplot(x="Average Wind Speed (MPH)", y="Potential Wind Capacity (MW)", hue="Cluster", data=clustered_df, palette="Set2")
    plt.title("Figure 12. State Clusters Based on Wind and Disasters")
    plt.grid(True)
    _save_or_show("figure_12_cluster_windspeed_capacity.png" if save else None)

    plt.figure(figsize=(10, 8))
    sns.scatterplot(x="Tornadoes Disasters", y="Potential Wind Capacity (MW)", hue="Cluster", data=clustered_df, palette="Set2")
    plt.title("Figure 13. State Clusters Based on Potential and Disasters")
    plt.grid(True)
    _save_or_show("figure_13_cluster_disasters_capacity.png" if save else None)

    high_potential_cluster_states = clustered_df[clustered_df["Cluster"] == 2]["State"].tolist()
    print("States in Cluster 2:")
    print(high_potential_cluster_states)
    return clustered_df, high_potential_cluster_states


def plot_potential_vs_windspeed_disaster(merged_df: pd.DataFrame, save: bool = False) -> None:
    plot_potential_vs_windspeed(merged_df, save=save)
    plot_potential_vs_disasters(merged_df, save=save)


def analysis_three_cluster(merged_df: pd.DataFrame, n_clusters: int = 3, save: bool = False) -> None:
    determine_n_cluster(merged_df, save=save)
    cluster_states(merged_df, n_clusters=n_clusters, save=save)
