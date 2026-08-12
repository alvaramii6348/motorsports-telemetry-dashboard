import streamlit as st

from src.data_loader import load_telemetry_csv
from src.preprocessing import clean_column_names, get_available_laps, detect_csv_type
from src.lap_analysis import (
    get_fastest_lap,
    get_lap_summary,
    get_valid_laps,
    compare_laps,
    get_race_stats
)
from src.plotting import (
    plot_lap_times,
    plot_sector_differences,
    plot_single_channel
)



st.set_page_config(
    page_title="Motorsports Telemetry Dashboard",
    layout="wide"
)

st.title("Motorsports Telemetry Dashboard")
st.write("Upload Garage61/iRacing-style telemetry CSV data and compare laps.")

uploaded_file = st.file_uploader("Upload a telemetry CSV", type=["csv"])

if uploaded_file is not None:
    df = load_telemetry_csv(uploaded_file)
    df = clean_column_names(df)

    csv_type = detect_csv_type(df)
    st.info(f"Detected CSV type: {csv_type}")

    if csv_type == "race_summary":
        st.subheader("Race Summary Mode")

        valid_laps = get_valid_laps(df)

        only_clean = st.checkbox("Only show clean laps", value=False)

        if only_clean and "Clean" in valid_laps.columns:
            valid_laps = valid_laps[valid_laps["Clean"] == 1]

        stats = get_race_stats(valid_laps)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Valid Laps",
            stats["valid_laps"]
        )

        col2.metric(
            "Fastest Lap",
            f"Lap {stats['fastest_lap_number']}",
            f"{stats['fastest_lap_time']:.3f} sec"
        )

        col3.metric(
            "Average Lap",
            f"{stats['average_lap_time']:.3f} sec"
        )

        col4.metric(
            "Consistency",
            f"{stats['lap_time_std']:.3f} sec"
        )

        st.subheader("Lap Time Progression")
        fig = plot_lap_times(valid_laps)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Valid Lap Summary")
        lap_summary = get_lap_summary(valid_laps)
        st.dataframe(lap_summary)

        fastest_lap = get_fastest_lap(valid_laps)

    elif csv_type == "telemetry":
    st.subheader("Telemetry Trace Mode")

    st.write(
        "Analyze individual telemetry channels across the lap."
    )

    telemetry_channels = [
        "Speed",
        "Throttle",
        "Brake",
        "RPM",
        "Gear",
        "SteeringWheelAngle"
    ]

    available_channels = [
        channel
        for channel in telemetry_channels
        if channel in df.columns
    ]

    selected_channel = st.selectbox(
        "Select telemetry channel",
        available_channels
    )

    fig = plot_single_channel(
        df,
        x_column="LapDistPct",
        y_column=selected_channel,
        title=f"{selected_channel} Trace"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    st.subheader("Columns")
    st.write(df.columns.tolist())

    if csv_type == "race_summary":
        if csv_type == "race_summary":
            laps = get_available_laps(valid_laps)
        else:
            laps = get_available_laps(df)

        if len(laps) == 0:
            st.warning("No valid laps found. Check your CSV column names or filtering logic.")
        else:
        st.subheader("Lap Selection")

        col1, col2 = st.columns(2)

        with col1:
            lap_a = st.selectbox("Select Lap A", laps, index=0)

        with col2:
            default_lap_b_index = 1 if len(laps) > 1 else 0
            lap_b = st.selectbox("Select Lap B", laps, index=default_lap_b_index)

        st.success(f"Comparing Lap {lap_a} vs Lap {lap_b}")

        if csv_type == "race_summary":
            st.subheader("Lap Comparison")

            comparison_df = compare_laps(valid_laps, lap_a, lap_b)

            if comparison_df.empty:
                st.warning("Could not compare these laps.")
            else:
                st.dataframe(comparison_df, hide_index=True)

                fig = plot_sector_differences(comparison_df)
                st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload a CSV file to begin.")