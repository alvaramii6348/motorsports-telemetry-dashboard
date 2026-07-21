import pandas as pd


def get_valid_laps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter out incomplete laps by requiring complete sector data.

    For Garage61 race summary CSVs, incomplete laps often have missing
    sector values. This keeps only laps where all sector columns are filled.
    """
    valid_df = df.copy()

    # Basic required columns
    valid_df = valid_df.dropna(subset=["Lap", "Lap time"])

    # Remove Lap 0 because it is usually not a complete timed lap
    valid_df = valid_df[valid_df["Lap"] > 0]

    # Find all sector columns, like "Sector 1", "Sector 2", etc.
    sector_columns = [
        col for col in valid_df.columns
        if col.startswith("Sector")
    ]

    # If sector columns exist, require all of them to be filled
    if len(sector_columns) > 0:
        valid_df = valid_df.dropna(subset=sector_columns)

    return valid_df


def get_fastest_lap(df: pd.DataFrame) -> pd.Series:
    """
    Return the fastest valid lap.
    """
    valid_laps = get_valid_laps(df)
    fastest_index = valid_laps["Lap time"].idxmin()
    return valid_laps.loc[fastest_index]


def get_lap_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return useful columns for lap summary analysis.
    """
    columns = [
        "Lap",
        "Lap time",
        "Clean",
        "Pit in",
        "Pit out",
        "Track temp",
        "Fuel level",
        "Sector 1",
        "Sector 2",
        "Sector 3",
        "Sector 4",
    ]

    available_columns = [col for col in columns if col in df.columns]

    return df[available_columns].copy()

def compare_laps(df: pd.DataFrame, lap_a: int, lap_b: int) -> pd.DataFrame:
    """
    Compare two laps using lap time and sector times.
    """
    lap_a_data = df[df["Lap"] == lap_a].iloc[0]
    lap_b_data = df[df["Lap"] == lap_b].iloc[0]

    comparison_rows = []

    columns_to_compare = ["Lap time", "Sector 1", "Sector 2", "Sector 3", "Sector 4"]

    for col in columns_to_compare:
        if col in df.columns:
            value_a = lap_a_data[col]
            value_b = lap_b_data[col]
            difference = value_a - value_b

            comparison_rows.append({
                "Metric": col,
                f"Lap {lap_a}": value_a,
                f"Lap {lap_b}": value_b,
                "Difference": difference,
                "Faster Lap": lap_a if value_a < value_b else lap_b
            })

    return pd.DataFrame(comparison_rows)

def get_race_stats(df: pd.DataFrame) -> dict:
    """
    Calculate summary statistics for valid race laps.
    """
    stats = {
        "valid_laps": len(df),
        "fastest_lap_time": df["Lap time"].min(),
        "average_lap_time": df["Lap time"].mean(),
        "lap_time_std": df["Lap time"].std(),
    }

    fastest_lap_row = df.loc[df["Lap time"].idxmin()]
    stats["fastest_lap_number"] = int(fastest_lap_row["Lap"])

    if "Clean" in df.columns:
        clean_laps = df[df["Clean"] == 1]

        if len(clean_laps) > 0:
            best_clean_row = clean_laps.loc[clean_laps["Lap time"].idxmin()]
            stats["best_clean_lap_number"] = int(best_clean_row["Lap"])
            stats["best_clean_lap_time"] = best_clean_row["Lap time"]
        else:
            stats["best_clean_lap_number"] = None
            stats["best_clean_lap_time"] = None

    return stats