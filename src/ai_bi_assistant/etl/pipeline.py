from ai_bi_assistant.etl.extract import extract_dataset
from ai_bi_assistant.etl.transform import transform
from ai_bi_assistant.database.connection import engine
from ai_bi_assistant.etl.load import load_table
from ai_bi_assistant.etl.daily_streams import build_fact_daily_streams


def run_pipeline():

    # -----------------------------
    # EXTRACT
    # -----------------------------
    df = extract_dataset()

    # -----------------------------
    # TRANSFORM
    # -----------------------------
    warehouse = transform(df)

    # -----------------------------
    # BUILD DAILY STREAMS
    # -----------------------------
    fact_daily_streams = build_fact_daily_streams(
        warehouse.dim_tracks,
        warehouse.dim_countries,
    )

    # -----------------------------
    # LOAD TO POSTGRES
    # -----------------------------
    load_table(warehouse.dim_labels, "dim_labels", engine)
    load_table(warehouse.dim_genres, "dim_genres", engine)
    load_table(warehouse.dim_countries, "dim_countries", engine)
    load_table(warehouse.dim_artists, "dim_artists", engine)
    load_table(warehouse.dim_albums, "dim_albums", engine)
    load_table(warehouse.dim_tracks, "dim_tracks", engine)
    load_table(warehouse.fact_audio_features, "fact_audio_features", engine)
    load_table(warehouse.fact_streams, "fact_streams", engine)

    # NEW TABLE
    load_table(
        fact_daily_streams,
        "fact_daily_streams",
        engine,
    )

    # -----------------------------
    # PRINT RESULTS
    # -----------------------------
    print("\n========== LABELS ==========")
    print(warehouse.dim_labels.head())
    print(f"Total: {len(warehouse.dim_labels)}")

    print("\n========== GENRES ==========")
    print(warehouse.dim_genres.head())
    print(f"Total: {len(warehouse.dim_genres)}")

    print("\n========== COUNTRIES ==========")
    print(warehouse.dim_countries.head())
    print(f"Total: {len(warehouse.dim_countries)}")

    print("\n========== ARTISTS ==========")
    print(warehouse.dim_artists.head())
    print(f"Total: {len(warehouse.dim_artists)}")

    print("\n========== ALBUMS ==========")
    print(warehouse.dim_albums.head())
    print(f"Total: {len(warehouse.dim_albums)}")

    print("\n========== TRACKS ==========")
    print(warehouse.dim_tracks.head())
    print(f"Total: {len(warehouse.dim_tracks)}")

    print("\n========== AUDIO FEATURES ==========")
    print(warehouse.fact_audio_features.head())
    print(f"Total: {len(warehouse.fact_audio_features)}")

    print("\n========== STREAM METRICS ==========")
    print(warehouse.fact_streams.head())
    print(f"Total: {len(warehouse.fact_streams)}")

    print("\n========== DAILY STREAMS ==========")
    print(fact_daily_streams.head())
    print(f"Total: {len(fact_daily_streams):,}")


if __name__ == "__main__":
    run_pipeline()