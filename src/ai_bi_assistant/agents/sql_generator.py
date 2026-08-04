from langchain_core.prompts import ChatPromptTemplate

from ai_bi_assistant.agents.llm import llm

prompt = ChatPromptTemplate.from_template(
"""
You are a senior PostgreSQL SQL developer.

Your task is to generate PostgreSQL SQL queries.

Rules:
- Return ONLY valid PostgreSQL SQL.
- Do NOT explain your answer.
- Do NOT use markdown.
- Do NOT wrap the SQL inside ```sql.
- Generate ONLY SELECT statements.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE or TRUNCATE.
- Use JOINs whenever multiple tables are needed.
- Use meaningful aliases.
- Prefer readable SQL.
- Always qualify column names with table aliases.
- Use aggregate functions whenever appropriate.
- If the question is about trends, growth, revenue, listeners, daily, weekly, monthly, yearly or time-series analysis, prefer using fact_daily_streams.
- Use DATE_TRUNC('month', date) for monthly analysis.
- Use DATE_TRUNC('week', date) for weekly analysis.
- Use DATE_TRUNC('year', date) for yearly analysis.
- Always ORDER BY the date or time period for time-series queries.
- If the question cannot be answered from the schema, return exactly:
SELECT 'Cannot answer with available data.' AS message;

Database Schema

dim_labels(
    label_id,
    label
)

dim_genres(
    genre_id,
    genre
)

dim_countries(
    country_id,
    country
)

dim_artists(
    artist_id,
    artist_name,
    label_id
)

dim_albums(
    album_id,
    artist_id,
    artist_name,
    album_name,
    release_date
)

dim_tracks(
    track_id,
    track_name,
    album_id,
    genre_id,
    duration_ms,
    explicit
)

fact_audio_features(
    track_id,
    danceability,
    energy,
    key,
    loudness,
    mode,
    instrumentalness,
    tempo
)

fact_streams(
    track_id,
    country_id,
    stream_count,
    popularity
)

This table stores overall streaming statistics.

fact_daily_streams(
    daily_stream_id,
    date,
    track_id,
    country_id,
    streams,
    revenue,
    listeners
)

This table stores daily business metrics and should be used for:
- revenue analysis
- listener analysis
- trend analysis
- monthly reports
- weekly reports
- yearly reports
- growth analysis
- time-series analysis

Question:
{question}
"""
)

chain = prompt | llm


def clean_sql(sql: str) -> str:
    """
    Remove markdown code fences from LLM output.
    """

    sql = sql.strip()

    if sql.startswith("```sql"):
        sql = sql.replace("```sql", "", 1)

    if sql.startswith("```"):
        sql = sql.replace("```", "", 1)

    if sql.endswith("```"):
        sql = sql[:-3]

    return sql.strip()


def generate_sql(question: str):
    """
    Generate SQL from a natural language question.
    """

    response = chain.invoke(
        {
            "question": question
        }
    )

    return clean_sql(response.content)