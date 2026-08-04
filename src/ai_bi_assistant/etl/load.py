import pandas as pd
from sqlalchemy import create_engine


def load_table(df: pd.DataFrame, table_name: str, engine):
    """
    Load a dataframe into PostgreSQL.
    """

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False,
    )

    print(f"✅ {table_name}: {len(df):,} rows loaded.")