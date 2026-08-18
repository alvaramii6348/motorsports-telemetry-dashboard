import numpy as np
import pandas as pd


def calculate_speed_delta(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    num_points: int = 1001
) -> pd.DataFrame:
    """
    Align two telemetry laps by lap distance and calculate
    the speed difference between them.

    Positive delta = Lap A is faster.
    Negative delta = Lap B is faster.
    """

    # Keep only the columns needed for speed comparison
    lap_a = df_a[
        ["Lap Distance (%)", "Speed (mph)"]
    ].dropna().copy()

    lap_b = df_b[
        ["Lap Distance (%)", "Speed (mph)"]
    ].dropna().copy()

    # Sort samples by lap distance
    lap_a = lap_a.sort_values("Lap Distance (%)")
    lap_b = lap_b.sort_values("Lap Distance (%)")

    # Average duplicate distance samples if any exist
    lap_a = lap_a.groupby(
        "Lap Distance (%)",
        as_index=False
    )["Speed (mph)"].mean()

    lap_b = lap_b.groupby(
        "Lap Distance (%)",
        as_index=False
    )["Speed (mph)"].mean()

    # Find the distance range covered by BOTH laps
    start_distance = max(
        lap_a["Lap Distance (%)"].min(),
        lap_b["Lap Distance (%)"].min()
    )

    end_distance = min(
        lap_a["Lap Distance (%)"].max(),
        lap_b["Lap Distance (%)"].max()
    )

    # Create common points around the lap
    common_distance = np.linspace(
        start_distance,
        end_distance,
        num_points
    )

    # Estimate each lap's speed at those same positions
    speed_a = np.interp(
        common_distance,
        lap_a["Lap Distance (%)"],
        lap_a["Speed (mph)"]
    )

    speed_b = np.interp(
        common_distance,
        lap_b["Lap Distance (%)"],
        lap_b["Speed (mph)"]
    )

    result = pd.DataFrame({
        "Lap Distance (%)": common_distance,
        "Lap A Speed (mph)": speed_a,
        "Lap B Speed (mph)": speed_b
    })

    result["Speed Delta (mph)"] = (
        result["Lap A Speed (mph)"]
        - result["Lap B Speed (mph)"]
    )

    return result