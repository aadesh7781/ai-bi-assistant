from pathlib import Path

import pandas as pd

# Path to our raw dataset
DATASET_PATH = Path("data/spotify_tracks.csv")


def extract_dataset() -> pd.DataFrame:
    """
    Read the raw Spotify dataset.

    Returns
    -------
    pd.DataFrame
        Raw Spotify dataset.
    """

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATASET_PATH}"
        )

    print("=" * 60)
    print("EXTRACT STAGE")
    print("=" * 60)

    print(f"Loading dataset: {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)

    print(f"Rows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]}")

    return df