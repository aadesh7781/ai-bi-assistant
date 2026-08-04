from dataclasses import dataclass

import pandas as pd


@dataclass
class Warehouse:
    dim_labels: pd.DataFrame
    dim_artists: pd.DataFrame
    dim_albums: pd.DataFrame
    dim_genres: pd.DataFrame
    dim_countries: pd.DataFrame
    dim_tracks: pd.DataFrame
    fact_audio_features: pd.DataFrame
    fact_streams: pd.DataFrame