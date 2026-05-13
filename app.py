import streamlit as st

from src.data_loader import load_telemetry_csv
from src.preprocessing import clean_column_names, get_available_laps


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

    st.subheader("Data Preview")
    st.dataframe(df.head()) #first few rows

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