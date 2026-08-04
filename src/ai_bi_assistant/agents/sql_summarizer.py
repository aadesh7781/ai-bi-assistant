import pandas as pd


def summarize_sql(rows):

    if not rows:
        return "No SQL results."

    df = pd.DataFrame(rows)

    summary = []

    summary.append(f"Rows returned: {len(df)}")

    summary.append(f"Columns: {', '.join(df.columns)}")

    summary.append(df.head(10).to_markdown(index=False))

    return "\n".join(summary)