import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names by stripping extra spaces.
    """
    df = df.copy()
    df.columns = df.columns.str.strip()
    return df


def get_available_laps(df: pd.DataFrame, lap_column: str = "Lap") -> list:
    """
    Return a sorted list of available lap numbers.
    """
    if lap_column not in df.columns:
        return []

    laps = df[lap_column].dropna().unique()
    return sorted(laps)

def detect_csv_type(df):
    """
    Detect what kind of motorsports CSV was uploaded.
    """

    columns = set(df.columns)

    telemetry_columns = {"Speed", "Brake", "Throttle", "LapDistPct"}
    race_summary_columns = {"Lap", "Lap time", "Sector 1", "Sector 2"}

    if telemetry_columns.issubset(columns):
        return "telemetry"

    if race_summary_columns.issubset(columns):
        return "race_summary"

    return "unknown"