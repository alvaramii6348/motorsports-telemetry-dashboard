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