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

def merge_nearby_braking_zones(
    zones_df: pd.DataFrame,
    max_gap: float = 1.0
) -> pd.DataFrame:
    """
    Merge braking zones separated by a very short gap.

    max_gap is measured as percentage of lap distance.
    """

    if zones_df.empty:
        return zones_df

    merged_zones = []

    current_zone = zones_df.iloc[0].copy()

    for i in range(1, len(zones_df)):
        next_zone = zones_df.iloc[i]

        gap = (
            next_zone["Start (%)"]
            - current_zone["End (%)"]
        )

        if gap <= max_gap:
            # Extend the current braking zone
            current_zone["End (%)"] = next_zone["End (%)"]

            # Keep the highest brake pressure from either section
            current_zone["Peak Brake (%)"] = max(
                current_zone["Peak Brake (%)"],
                next_zone["Peak Brake (%)"]
            )

        else:
            merged_zones.append(current_zone)
            current_zone = next_zone.copy()

    # Add the final zone
    merged_zones.append(current_zone)

    result = pd.DataFrame(merged_zones)

    result.insert(
    0,
    "Zone",
    range(1, len(result) + 1)
    )

    return result.round({
        "Start (%)": 2,
        "End (%)": 2,
        "Peak Brake (%)": 1
    })

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

    if zones_df.empty:
        return zones_df

    # Merge brake applications that are separated
    # by only a small gap in lap distance
    zones_df = merge_nearby_braking_zones(
        zones_df,
        max_gap=1.0
    )

    return zones_df


def compare_braking_zones(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    max_start_difference: float = 3.0
) -> pd.DataFrame:
    """
    Compare braking zones between two telemetry laps.

    Zones are matched based on the closest braking start position.

    Start Delta:
        positive = Lap B brakes later
        negative = Lap A brakes later
    """

    zones_a = detect_braking_zones(df_a)
    zones_b = detect_braking_zones(df_b)

    if zones_a.empty or zones_b.empty:
        return pd.DataFrame()

    comparison_rows = []

    # Keep track of Lap B zones that have already been matched
    available_b_indices = set(zones_b.index)

    for _, zone_a in zones_a.iterrows():

        if not available_b_indices:
            break

        # Find the Lap B zone whose braking start is closest
        closest_b_index = min(
            available_b_indices,
            key=lambda index: abs(
                zones_b.loc[index, "Start (%)"]
                - zone_a["Start (%)"]
            )
        )

        zone_b = zones_b.loc[closest_b_index]

        start_delta = (
            zone_b["Start (%)"]
            - zone_a["Start (%)"]
        )

        # Ignore matches that are too far apart on the track
        if abs(start_delta) > max_start_difference:
            continue

        comparison_rows.append({
            "Zone": zone_a["Zone"],

            "Lap A Start (%)": zone_a["Start (%)"],
            "Lap B Start (%)": zone_b["Start (%)"],
            "Start Delta (%)": start_delta,

            "Lap A End (%)": zone_a["End (%)"],
            "Lap B End (%)": zone_b["End (%)"],
            "End Delta (%)": (
                zone_b["End (%)"]
                - zone_a["End (%)"]
            ),

            "Lap A Peak Brake (%)": zone_a["Peak Brake (%)"],
            "Lap B Peak Brake (%)": zone_b["Peak Brake (%)"]
        })

        # Don't allow the same Lap B braking zone
        # to match multiple Lap A zones
        available_b_indices.remove(closest_b_index)

    comparison_df = pd.DataFrame(comparison_rows)

    if not comparison_df.empty:
        comparison_df = comparison_df.round(2)

    return comparison_df