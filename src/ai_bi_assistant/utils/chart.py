import pandas as pd
import plotly.express as px


def create_chart(df: pd.DataFrame):
    """
    Automatically create the best chart based on the dataframe.
    """

    # Empty dataframe
    if df.empty:
        return None

    # Only support 2-column result sets for now
    if len(df.columns) != 2:
        return None

    x = df.columns[0]
    y = df.columns[1]

    # --------------------------------------------------
    # Convert numeric strings to numbers
    # Example:
    # "346994" -> 346994
    # --------------------------------------------------

    df = df.copy()

    df[y] = pd.to_numeric(df[y], errors="coerce")

    # If conversion failed for every row, don't create chart
    if df[y].isna().all():
        return None

    # --------------------------------------------------
    # Time-series detection
    # --------------------------------------------------

    x_lower = x.lower()

    if any(
        keyword in x_lower
        for keyword in [
            "date",
            "day",
            "month",
            "year",
        ]
    ):

        fig = px.line(
            df,
            x=x,
            y=y,
            markers=True,
            title=f"{y} over {x}",
        )

        fig.update_layout(
            height=450,
            xaxis_title=x,
            yaxis_title=y,
        )

        return fig

    # --------------------------------------------------
    # Default Bar Chart
    # --------------------------------------------------

    fig = px.bar(
        df,
        x=x,
        y=y,
        text=y,
        title=f"{y} by {x}",
    )

    fig.update_layout(
        height=450,
        xaxis_title=x,
        yaxis_title=y,
    )

    return fig