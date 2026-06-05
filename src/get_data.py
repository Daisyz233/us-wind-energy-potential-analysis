"""Data loading, cleaning, and merging functions for the wind energy project."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import BASE_DATA_DIR


def _data_path(filename: str, data_dir: str | Path = BASE_DATA_DIR) -> Path:
    """Return the expected path for a raw data file."""
    return Path(data_dir) / filename


def data_1_cleaning(data_dir: str | Path = BASE_DATA_DIR) -> pd.DataFrame:
    """Clean historical wind power production data.

    Keeps state-level wind production columns and removes broader regional
    aggregation columns so state comparisons are easier.
    """
    df1_raw = pd.read_csv(_data_path("wind-power-production-us.csv", data_dir), na_values=["--"])

    wind_colnames = [col for col in df1_raw.columns if "wind" in col.lower()]
    if wind_colnames and wind_colnames[0].lower() == "wind":
        wind_colnames = wind_colnames[1:]

    selected_cols = ["date"] + wind_colnames if "date" in df1_raw.columns else wind_colnames
    wind_df = df1_raw[selected_cols].copy()

    regions_to_exclude = [
        "wind_new_england",
        "wind_middle_atlantic",
        "wind_east_north_central",
        "wind_west_north_central",
        "wind_south_atlantic",
        "wind_east_south_central",
        "wind_west_south_central",
        "wind_mountain",
        "wind_pacific_contiguous",
        "wind_pacific_noncontiguous",
    ]

    filtered_columns = [
        col
        for col in wind_df.columns
        if col == "date" or (col.startswith("wind_") and col not in regions_to_exclude and col != "wind_united_states")
    ]

    if "wind_united_states" in wind_df.columns:
        filtered_columns.insert(1, "wind_united_states")

    wind_df = wind_df[filtered_columns].copy()
    wind_df.rename(columns=lambda x: x.replace("wind_", "") if x != "date" else x, inplace=True)

    numeric_cols = wind_df.columns.difference(["date"])
    wind_df[numeric_cols] = wind_df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    return wind_df


def data_2_cleaning() -> pd.DataFrame:
    """Scrape average wind speeds by state from LandGate."""
    url = "https://www.landgate.com/news/average-wind-speeds-by-state"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    all_dataframes = []

    for table in tables:
        rows = table.find_all("tr")
        table_data = []
        for row in rows:
            cols = [col.get_text(strip=True) for col in row.find_all(["td", "th"])]
            if cols:
                table_data.append(cols)
        if len(table_data) > 1:
            header = table_data[0]
            data = table_data[1:]
            all_dataframes.append(pd.DataFrame(data, columns=header))

    if not all_dataframes:
        raise ValueError("No wind speed tables were found on the LandGate page.")

    wind_avg_df = pd.concat(all_dataframes, ignore_index=True)
    wind_avg_df = wind_avg_df.iloc[:, :2].copy()
    wind_avg_df.columns = ["State", "Average Wind Speed (MPH)"]
    wind_avg_df["Average Wind Speed (MPH)"] = (
        wind_avg_df["Average Wind Speed (MPH)"].astype(str).str.replace(" mph", "", regex=False).astype(float)
    )
    return wind_avg_df


def data_3_cleaning(data_dir: str | Path = BASE_DATA_DIR) -> pd.DataFrame:
    """Clean tornado records to state/date/magnitude fields."""
    df3 = pd.read_csv(_data_path("tornados.csv", data_dir))
    tornados_df = df3[["date", "st", "mag"]].copy()
    tornados_df = tornados_df.drop_duplicates(subset=["date", "st"])
    return tornados_df


def data_4_cleaning(data_dir: str | Path = BASE_DATA_DIR) -> pd.DataFrame:
    """Load potential wind capacity data.

    Supports both the compact CSV used in this repository and the original
    WindExchange export that may contain metadata rows above the header.
    """
    file_path = _data_path("total_wind_capacity_80m.csv", data_dir)

    # First try the clean two-column version. If that fails, fall back to the
    # original course-project parsing logic with skipped metadata rows.
    df = pd.read_csv(file_path)
    if "State" not in df.columns or "Total 80m Capacity (MW)" not in df.columns:
        df = pd.read_csv(file_path, skiprows=3)
        df.rename(columns={df.columns[0]: "State"}, inplace=True)
        df = df.iloc[:-1]
        df = df.dropna(subset=["State"])
        df["Total 80m Capacity (MW)"] = df.iloc[:, 1:].sum(axis=1)

    wind_potential_df = df[["State", "Total 80m Capacity (MW)"]].copy()
    return wind_potential_df


def merge_data(tornados_df: pd.DataFrame, wind_avg_df: pd.DataFrame, wind_potential_df: pd.DataFrame) -> pd.DataFrame:
    """Merge wind speed, potential capacity, and tornado-frequency data by state."""
    states_data = {
        "State": [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
            "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
            "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
            "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
            "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
            "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
            "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
        ],
        "Abbreviation": [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",
            "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
            "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT",
            "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
            "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT",
            "VT", "VA", "WA", "WV", "WI", "WY",
        ],
    }

    state_lookup = pd.DataFrame(states_data)
    disaster_counts_by_state = tornados_df["st"].value_counts().reset_index()
    disaster_counts_by_state.columns = ["state", "total_disasters"]

    merged_df = pd.merge(state_lookup, disaster_counts_by_state, how="left", left_on="Abbreviation", right_on="state")
    merged_df.drop(columns=["state"], inplace=True)
    merged_df = pd.merge(merged_df, wind_avg_df, on="State", how="left")
    merged_df = pd.merge(merged_df, wind_potential_df, how="left", left_on="Abbreviation", right_on="State")
    merged_df.drop(columns=["State_y"], inplace=True)
    merged_df.rename(columns={"State_x": "State"}, inplace=True)
    merged_df.rename(
        columns={
            "total_disasters": "Tornadoes Disasters",
            "Total 80m Capacity (MW)": "Potential Wind Capacity (MW)",
        },
        inplace=True,
    )
    return merged_df


def run_all_data_cleaning_and_merge(data_dir: str | Path = BASE_DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run the full data-cleaning workflow and return key analysis datasets."""
    wind_df = data_1_cleaning(data_dir)
    wind_avg_df = data_2_cleaning()
    tornados_df = data_3_cleaning(data_dir)
    wind_potential_df = data_4_cleaning(data_dir)
    merged_df = merge_data(tornados_df, wind_avg_df, wind_potential_df)
    return wind_df, tornados_df, merged_df
