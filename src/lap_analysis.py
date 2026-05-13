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