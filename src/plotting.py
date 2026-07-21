import plotly.express as px
import pandas as pd


def plot_lap_times(df: pd.DataFrame):
    """
    Plot lap time over lap number.
    """
    fig = px.line(
        df,
        x="Lap",
        y="Lap time",
        markers=True,
        title="Lap Time Progression"
    )

    fig.update_layout(
        xaxis_title="Lap",
        yaxis_title="Lap Time (seconds)",
        height=450
    )

    return fig


def plot_sector_differences(comparison_df):
    """
    Plot sector/lap time differences between two selected laps.
    """
    sector_rows = comparison_df[comparison_df["Metric"].str.startswith("Sector")]

    fig = px.bar(
        sector_rows,
        x="Metric",
        y="Difference",
        title="Sector Time Difference"
    )

    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Difference in Seconds",
        height=400
    )

    return fig