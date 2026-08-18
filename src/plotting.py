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


def plot_single_channel(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    y_min=None,
    y_max=None
):
    """
    Create a line chart for one telemetry channel.
    """

    plot_df = df.dropna(
        subset=[x_column, y_column]
    ).copy()

    # Make sure telemetry is plotted in lap-distance order
    plot_df = plot_df.sort_values(by=x_column)

    fig = px.line(
        plot_df,
        x=x_column,
        y=y_column,
        title=title
    )

    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column,
        height=400
    )

    fig.update_xaxes(
        range=[0, 100],
        tickmode="array",
        tickvals=[0, 25, 50, 75, 100],
        ticktext=[
            "Start",
            "25%",
            "50%",
            "75%",
            "Finish"
        ],
        title="Lap Progress"
    )

    if y_min is not None or y_max is not None:
        fig.update_yaxes(
            range=[y_min, y_max]
        )

    return fig

def plot_channel_comparison(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    y_min=None,
    y_max=None
):
    """
    Overlay the same telemetry channel from two laps.
    """

    lap_a = df_a.dropna(
        subset=[x_column, y_column]
    ).copy()

    lap_b = df_b.dropna(
        subset=[x_column, y_column]
    ).copy()

    # Ensure both laps are drawn in lap-distance order
    lap_a = lap_a.sort_values(by=x_column)
    lap_b = lap_b.sort_values(by=x_column)

    # Add labels so Plotly knows which line belongs to which lap
    lap_a["Comparison Lap"] = "Lap A"
    lap_b["Comparison Lap"] = "Lap B"

    combined_df = pd.concat(
        [lap_a, lap_b],
        ignore_index=True
    )

    fig = px.line(
        combined_df,
        x=x_column,
        y=y_column,
        color="Comparison Lap",
        title=title
    )

    fig.update_layout(
        yaxis_title=y_column,
        height=400
    )

    fig.update_xaxes(
        range=[0, 100],
        tickmode="array",
        tickvals=[0, 25, 50, 75, 100],
        ticktext=[
            "Start",
            "25%",
            "50%",
            "75%",
            "Finish"
        ],
        title="Lap Progress"
    )

    if y_min is not None or y_max is not None:
        fig.update_yaxes(
            range=[y_min, y_max]
        )

    return fig

def plot_speed_delta(delta_df: pd.DataFrame):
    """
    Plot speed difference between two telemetry laps.
    """

    fig = px.line(
        delta_df,
        x="Lap Distance (%)",
        y="Speed Delta (mph)",
        title="Speed Delta"
    )

    # Zero represents equal speed
    fig.add_hline(
        y=0,
        line_dash="dash"
    )

    fig.update_layout(
        yaxis_title="Speed Difference (mph)",
        height=400
    )

    fig.update_xaxes(
        range=[0, 100],
        tickmode="array",
        tickvals=[0, 25, 50, 75, 100],
        ticktext=[
            "Start",
            "25%",
            "50%",
            "75%",
            "Finish"
        ],
        title="Lap Progress"
    )

    return fig