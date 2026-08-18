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

def detect_braking_zones(
    df: pd.DataFrame,
    brake_threshold: float = 5.0
) -> pd.DataFrame:
    """
    Detect braking zones based on brake pedal application.

    A braking zone begins when Brake (%) rises above the threshold
    and ends when it falls back below the threshold.
    """

    brake_df = df[
        ["Lap Distance (%)", "Brake (%)"]
    ].dropna().copy()

    brake_df = brake_df.sort_values("Lap Distance (%)")

    brake_df["Braking"] = (
        brake_df["Brake (%)"] >= brake_threshold
    )

    zones = []
    zone_start = None

    for i in range(len(brake_df)):
        is_braking = brake_df.iloc[i]["Braking"]

        if is_braking and zone_start is None:
            zone_start = i

        elif not is_braking and zone_start is not None:
            zone_end = i - 1

            zone_data = brake_df.iloc[
                zone_start:zone_end + 1
            ]

            zones.append({
                "Start (%)": zone_data["Lap Distance (%)"].iloc[0],
                "End (%)": zone_data["Lap Distance (%)"].iloc[-1],
                "Peak Brake (%)": zone_data["Brake (%)"].max()
            })

            zone_start = None

    zones_df = pd.DataFrame(zones)

    if not zones_df.empty:
        zones_df.insert(
            0,
            "Zone",
            range(1, len(zones_df) + 1)
        )

        zones_df = zones_df.round({
            "Start (%)": 2,
            "End (%)": 2,
            "Peak Brake (%)": 1
        })

    return zones_df