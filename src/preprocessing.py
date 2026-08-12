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

def prepare_telemetry_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare Garage61 telemetry data for dashboard display.

    Creates display-friendly columns for:
    - lap distance percentage
    - speed in mph
    - throttle percentage
    - brake percentage
    """
    telemetry_df = df.copy()

    # Convert lap distance from 0.0-1.0 to 0-100%
    if "LapDistPct" in telemetry_df.columns:
        telemetry_df["Lap Distance (%)"] = (
            telemetry_df["LapDistPct"] * 100
        )

    # Convert speed from meters/second to miles/hour
    if "Speed" in telemetry_df.columns:
        telemetry_df["Speed (mph)"] = (
            telemetry_df["Speed"] * 2.23694
        )

    # Garage61 throttle data may be stored from 0.0-1.0
    if "Throttle" in telemetry_df.columns:
        if telemetry_df["Throttle"].max() <= 1.01:
            telemetry_df["Throttle (%)"] = (
                telemetry_df["Throttle"] * 100
            )
        else:
            telemetry_df["Throttle (%)"] = telemetry_df["Throttle"]

    # Garage61 brake data may be stored from 0.0-1.0
    if "Brake" in telemetry_df.columns:
        if telemetry_df["Brake"].max() <= 1.01:
            telemetry_df["Brake (%)"] = (
                telemetry_df["Brake"] * 100
            )
        else:
            telemetry_df["Brake (%)"] = telemetry_df["Brake"]

    #steering 
    if "SteeringWheelAngle" in telemetry_df.columns:
        telemetry_df["Steering Angle (deg)"] = (
            telemetry_df["SteeringWheelAngle"] * (180 / 3.141592653589793)
        )

    return telemetry_df