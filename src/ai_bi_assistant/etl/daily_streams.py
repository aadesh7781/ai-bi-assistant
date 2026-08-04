import numpy as np
import pandas as pd


def build_fact_daily_streams(
    tracks,
    countries,
):
    """
    Generate one year of synthetic streaming data.
    """

    np.random.seed(42)

    dates = pd.date_range(
        start="2025-01-01",
        end="2025-12-31",
        freq="D",
    )

    records = []

    tracks = tracks.head(1000)

    for _, track in tracks.iterrows():

        base_streams = np.random.randint(
            1000,
            15000,
        )

        country_id = np.random.choice(
            countries["country_id"]
        )

        for date in dates:

            growth = np.random.normal(
                1.0,
                0.10,
            )

            streams = max(
                100,
                int(base_streams * growth),
            )

            revenue = round(
                streams * 0.004,
                2,
            )

            listeners = int(
                streams * np.random.uniform(
                    0.45,
                    0.75,
                )
            )

            records.append(
                [
                    date,
                    track["track_id"],
                    country_id,
                    streams,
                    revenue,
                    listeners,
                ]
            )

    return pd.DataFrame(
        records,
        columns=[
            "date",
            "track_id",
            "country_id",
            "streams",
            "revenue",
            "listeners",
        ],
    )