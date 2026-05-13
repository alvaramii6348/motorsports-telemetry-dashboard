import pandas as pd


def load_telemetry_csv(file) -> pd.DataFrame:
    """
    Load telemetry data from a CSV file.

    The file can be either:
    - a file path string
    - an uploaded Streamlit file object
    """
    return pd.read_csv(file)