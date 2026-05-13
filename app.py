import streamlit as st

from src.data_loader import load_telemetry_csv
from src.preprocessing import clean_column_names, get_available_laps, detect_csv_type
from src.lap_analysis import get_fastest_lap, get_lap_summary, get_valid_laps
from src.plotting import plot_lap_times


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

        st.subheader("Lap Time Progression")
        fig = plot_lap_times(valid_laps)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Valid Lap Summary")
        lap_summary = get_lap_summary(valid_laps)
        st.dataframe(lap_summary)

        fastest_lap = get_fastest_lap(df)

        st.metric(
            label="Fastest Valid Lap",
            value=f"Lap {int(fastest_lap['Lap'])}",
            delta=f"{fastest_lap['Lap time']:.3f} sec"
        )

    st.subheader("Data Preview")
    st.dataframe(df.head())

    st.subheader("Columns")
    st.write(df.columns.tolist())

    laps = get_available_laps(df)

    if len(laps) == 0:
        st.warning("No 'Lap' column found. Check your CSV column names.")
    else:
        st.subheader("Lap Selection")

        col1, col2 = st.columns(2)

        with col1:
            lap_a = st.selectbox("Select Lap A", laps)

        with col2:
            lap_b = st.selectbox("Select Lap B", laps)

        st.success(f"Comparing Lap {lap_a} vs Lap {lap_b}")

else:
    st.info("Upload a CSV file to begin.")