import pandas as pd

from ai_bi_assistant.etl.warehouse import Warehouse


def build_dimension(
    df: pd.DataFrame,
    source_column: str,
    id_column: str,
) -> pd.DataFrame:
    """
    Generic function to build a dimension table.
    """

    dimension = (
        df[[source_column]]
        .drop_duplicates()
        .sort_values(source_column)
        .reset_index(drop=True)
    )

    dimension.insert(
        0,
        id_column,
        range(1, len(dimension) + 1),
    )

    return dimension


def build_dim_labels(df: pd.DataFrame) -> pd.DataFrame:
    return build_dimension(
        df=df,
        source_column="label",
        id_column="label_id",
    )


def build_dim_genres(df: pd.DataFrame) -> pd.DataFrame:
    return build_dimension(
        df=df,
        source_column="genre",
        id_column="genre_id",
    )


def build_dim_countries(df: pd.DataFrame) -> pd.DataFrame:
    return build_dimension(
        df=df,
        source_column="country",
        id_column="country_id",
    )
def build_dim_artists(
    df: pd.DataFrame,
    dim_labels: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the Artist Dimension table.
    Assumption:
    Artist names are unique.
    """

    artists = (
        df[["artist_name", "label"]]
        .sort_values("artist_name")
        .drop_duplicates(subset="artist_name", keep="first")
        .reset_index(drop=True)
    )

    artists = artists.merge(
        dim_labels,
        on="label",
        how="left",
    )

    artists = artists.drop(columns="label")

    artists.insert(
        0,
        "artist_id",
        range(1, len(artists) + 1),
    )

    return artists
def build_dim_albums(
    df: pd.DataFrame,
    dim_artists: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the Album Dimension table.
    """

    # Keep one row per artist + album
    albums = (
        df[["artist_name", "album_name", "release_date"]]
        .drop_duplicates(subset=["artist_name", "album_name"])
        .sort_values(["artist_name", "album_name"])
        .reset_index(drop=True)
    )

    # Add artist_id
    albums = albums.merge(
        dim_artists[["artist_id", "artist_name"]],
        on="artist_name",
        how="left",
    )


    # Reorder columns
    albums = albums[
    [
        "artist_id",
        "artist_name",
        "album_name",
        "release_date",
    ]
]

    # Add surrogate key
    albums.insert(
        0,
        "album_id",
        range(1, len(albums) + 1),
    )

    return albums

def build_dim_tracks(
    df: pd.DataFrame,
    dim_albums: pd.DataFrame,
    dim_genres: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the Track Dimension table.
    """

    tracks = df[
        [
            "track_id",
            "track_name",
            "artist_name",
            "album_name",
            "genre",
            "duration_ms",
            "explicit",
        ]
    ].copy()

    # Join with albums using the business key
    tracks = tracks.merge(
        dim_albums[
            [
                "album_id",
                "artist_name",
                "album_name",
            ]
        ],
        on=["artist_name", "album_name"],
        how="left",
    )

    # Join with genres
    tracks = tracks.merge(
        dim_genres,
        on="genre",
        how="left",
    )

    # Final warehouse columns
    tracks = tracks[
        [
            "track_id",
            "track_name",
            "album_id",
            "genre_id",
            "duration_ms",
            "explicit",
        ]
    ]

    return tracks.drop_duplicates()

def build_fact_audio_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the Audio Features fact table.
    """

    audio_features = df[
        [
            "track_id",
            "danceability",
            "energy",
            "key",
            "loudness",
            "mode",
            "instrumentalness",
            "tempo",
        ]
    ].copy()

    return audio_features.drop_duplicates()

def build_fact_streams(
    df: pd.DataFrame,
    dim_countries: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the Stream Metrics fact table.
    """

    streams = df[
        [
            "track_id",
            "country",
            "stream_count",
            "popularity",
        ]
    ].copy()

    # Replace country with country_id
    streams = streams.merge(
        dim_countries,
        on="country",
        how="left",
    )

    streams = streams[
        [
            "track_id",
            "country_id",
            "stream_count",
            "popularity",
        ]
    ]

    return streams.drop_duplicates()

def transform(df: pd.DataFrame) -> Warehouse:
    """
    Transform the raw dataset into a normalized warehouse.
    """

    dim_labels = build_dim_labels(df)

    dim_genres = build_dim_genres(df)

    dim_countries = build_dim_countries(df)

    dim_artists = build_dim_artists(
        df,
        dim_labels,
    )

    dim_albums = build_dim_albums(
        df,
        dim_artists,
    )
    dim_tracks = build_dim_tracks(
    df,
    dim_albums,
    dim_genres,
)
    fact_audio_features = build_fact_audio_features(df)

    fact_streams = build_fact_streams(
    df,
    dim_countries,
)

    return Warehouse(
        dim_labels=dim_labels,
        dim_artists=dim_artists,
        dim_albums=dim_albums,
        dim_genres=dim_genres,
        dim_countries=dim_countries,
        dim_tracks=dim_tracks,
        fact_audio_features=fact_audio_features,
        fact_streams=fact_streams,
    )
