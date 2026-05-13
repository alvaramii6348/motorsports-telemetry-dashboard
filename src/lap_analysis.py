import pandas as pd


def get_fastest_lap(df: pd.DataFrame) -> pd.Series:
    """
    Return the row with the fastest lap time.
    """
    clean_laps = df.dropna(subset=["Lap time"])
    fastest_index = clean_laps["Lap time"].idxmin()
    return clean_laps.loc[fastest_index]


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