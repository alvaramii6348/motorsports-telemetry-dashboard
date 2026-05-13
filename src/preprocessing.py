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