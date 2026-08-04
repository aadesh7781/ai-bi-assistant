import html as html_lib

import requests
import streamlit as st
import pandas as pd

from ai_bi_assistant.utils.chart import create_chart

# =====================================================
# CONFIG / CONSTANTS
# =====================================================

BACKEND_URL = "http://127.0.0.1:8000"
ASK_ENDPOINT = f"{BACKEND_URL}/ask"

BG = "#121212"
CARD = "#181818"
CARD_ALT = "#282828"
GREEN = "#1DB954"
WHITE = "#FFFFFF"
MUTED = "#B3B3B3"

st.set_page_config(
    page_title="Spotify Intelligence Platform",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    f"""
    <style>

    /* ---------- Global ---------- */

    .stApp {{
        background-color: {BG};
        color: {WHITE};
    }}

    html, body, [class*="css"] {{
        font-family: -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    }}

    #MainMenu, footer, header {{ visibility: hidden; }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 7rem;
        max-width: 1020px;
    }}

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {{
        background-color: {CARD};
        border-right: 1px solid {CARD_ALT};
    }}

    section[data-testid="stSidebar"] .block-container {{
        padding-top: 2rem;
    }}

    .sb-brand {{
        font-size: 1.15rem;
        font-weight: 800;
        color: {WHITE};
        margin-bottom: 0.9rem;
    }}

    .sb-divider {{
        border: none;
        border-top: 1px solid #2a2a2a;
        margin: 1.1rem 0;
    }}

    .sb-section-title {{
        color: {MUTED};
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 0.55rem;
    }}

    .status-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.3rem 0.1rem;
        font-size: 0.85rem;
    }}

    .status-row .label {{
        color: {MUTED};
    }}

    .status-row .value {{
        color: {WHITE};
        font-weight: 600;
    }}

    .status-row .value.ok {{
        color: {GREEN};
    }}

    .status-row .value.bad {{
        color: #ff6b6b;
    }}

    /* Sidebar nav-style buttons */
    /* Targets both the wrapper div and the button's own testid          */
    /* (stBaseButton-*) directly, since the button is not always a       */
    /* direct/simple descendant of the wrapper across Streamlit builds.  */

    section[data-testid="stSidebar"] div[data-testid="stButton"] button,
    section[data-testid="stSidebar"] button[data-testid^="stBaseButton"] {{
        background-color: transparent !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 0.87rem !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 0.4rem 0.5rem !important;
        width: 100% !important;
        min-height: 0 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stButton"] button,
    section[data-testid="stSidebar"] div[data-testid="stButton"] button *,
    section[data-testid="stSidebar"] button[data-testid^="stBaseButton"],
    section[data-testid="stSidebar"] button[data-testid^="stBaseButton"] * {{
        color: {MUTED} !important;
        font-weight: 500 !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover,
    section[data-testid="stSidebar"] button[data-testid^="stBaseButton"]:hover {{
        background-color: {CARD_ALT} !important;
        border: none !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover,
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover *,
    section[data-testid="stSidebar"] button[data-testid^="stBaseButton"]:hover,
    section[data-testid="stSidebar"] button[data-testid^="stBaseButton"]:hover * {{
        color: {GREEN} !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stButton"] button:focus:not(:active),
    section[data-testid="stSidebar"] button[data-testid^="stBaseButton"]:focus:not(:active) {{
        color: {GREEN} !important;
    }}

    /* ---------- Hero header ---------- */

    .hero {{
        background: linear-gradient(135deg, {CARD} 0%, {CARD_ALT} 100%);
        border-radius: 18px 18px 0 0;
        padding: 2.6rem 2.2rem 2.2rem 2.2rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        border: 1px solid #2a2a2a;
        border-bottom: none;
    }}

    .hero-accent {{
        height: 4px;
        background: linear-gradient(90deg, {GREEN} 0%, #0f7a37 100%);
        border-radius: 0 0 18px 18px;
        margin-bottom: 2rem;
    }}

    .hero-title {{
        font-size: 2.5rem;
        font-weight: 800;
        color: {WHITE};
        margin: 0;
        letter-spacing: -0.5px;
    }}

    .hero-subtitle {{
        font-size: 1.05rem;
        color: {GREEN};
        font-weight: 700;
        margin-top: 0.35rem;
    }}

    .hero-tagline {{
        color: {MUTED};
        margin-top: 0.7rem;
        font-size: 0.92rem;
        letter-spacing: 0.2px;
    }}

    .badge-row {{
        margin-top: 1.3rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }}

    .tech-badge {{
        background-color: rgba(29, 185, 84, 0.12);
        color: {GREEN};
        border: 1px solid rgba(29, 185, 84, 0.35);
        padding: 0.28rem 0.85rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
    }}

    /* ---------- KPI cards ---------- */

    div[data-testid="stMetric"] {{
        background-color: {CARD};
        border: 1px solid #262626;
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }}

    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        border-color: {GREEN};
    }}

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] * {{
        color: {MUTED} !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }}

    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] * {{
        color: {WHITE} !important;
        font-weight: 800 !important;
    }}

    /* ---------- Global text-color safety net ---------- */
    /* Streamlit's own theme sometimes renders body/markdown text in a  */
    /* low-contrast grey. Force plain markdown text to white by default; */
    /* our custom classes below set their own color and remain untouched */
    /* since they are plain <div> blocks, not <p> tags. */

    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown span,
    .stMarkdown strong,
    .stMarkdown em,
    div[data-testid="stChatMessageContent"] p,
    div[data-testid="stChatMessageContent"] li {{
        color: {WHITE} !important;
    }}

    .stMarkdown a {{
        color: {GREEN} !important;
    }}

    /* ---------- Section titles ---------- */

    .section-title {{
        font-size: 1.15rem;
        font-weight: 700;
        color: {WHITE};
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    .eyebrow {{
        color: {GREEN};
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1.6rem;
    }}

    /* ---------- Welcome screen ---------- */

    .welcome-wrap {{
        text-align: center;
        padding: 0.4rem 1rem 0.4rem 1rem;
    }}

    .welcome-title {{
        font-size: 1.65rem;
        font-weight: 800;
        color: {WHITE};
        margin-top: 0.3rem;
    }}

    .welcome-sub {{
        color: {MUTED};
        margin-top: 0.5rem;
        margin-bottom: 2rem;
        font-size: 0.95rem;
    }}

    /* Main-area card-style buttons (welcome cards) */

    /* Base style for every button in the app (welcome cards, footer, etc). */
    /* The sidebar rule above has higher selector specificity so it always  */
    /* wins there - this rule only ends up styling main-area buttons.      */
    /* Two selector strategies combined for resilience across Streamlit    */
    /* builds: the wrapper div's testid, and the button's own testid       */
    /* (stBaseButton-*), since the exact DOM nesting can vary by version.  */

    div[data-testid="stButton"] button,
    button[data-testid^="stBaseButton"] {{
        background-color: {CARD} !important;
        border: 1px solid #262626 !important;
        border-radius: 14px !important;
        padding: 1.15rem 1.2rem !important;
        text-align: left !important;
        justify-content: flex-start !important;
        width: 100% !important;
        min-height: 76px;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        white-space: normal !important;
        box-shadow: none !important;
        transition: border-color 0.15s ease, transform 0.15s ease;
    }}

    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    button[data-testid^="stBaseButton"],
    button[data-testid^="stBaseButton"] * {{
        color: {WHITE} !important;
    }}

    div[data-testid="stButton"] button:hover,
    button[data-testid^="stBaseButton"]:hover {{
        border-color: {GREEN} !important;
        transform: translateY(-2px);
    }}

    div[data-testid="stButton"] button:hover,
    div[data-testid="stButton"] button:hover *,
    button[data-testid^="stBaseButton"]:hover,
    button[data-testid^="stBaseButton"]:hover * {{
        color: {WHITE} !important;
    }}

    div[data-testid="stButton"] button:focus:not(:active),
    button[data-testid^="stBaseButton"]:focus:not(:active) {{
        border-color: {GREEN} !important;
    }}

    /* ---------- Chat bubbles ---------- */

    div[data-testid="stChatMessage"] {{
        background-color: {CARD};
        border-radius: 16px;
        border: 1px solid #262626;
        padding: 0.4rem 0.4rem;
        margin-bottom: 0.7rem;
    }}

    div[data-testid="stChatMessageAvatarUser"] {{
        background-color: {GREEN} !important;
    }}

    div[data-testid="stChatMessageAvatarAssistant"] {{
        background-color: {CARD_ALT} !important;
    }}

    /* ---------- Chat input ---------- */

    div[data-testid="stBottom"],
    div[data-testid="stBottomBlockContainer"] {{
        background-color: {BG} !important;
    }}

    div[data-testid="stChatInput"] {{
        background-color: {CARD} !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 16px !important;
    }}

    div[data-testid="stChatInput"] textarea {{
        background-color: transparent !important;
        color: {WHITE} !important;
    }}

    div[data-testid="stChatInput"] textarea::placeholder {{
        color: {MUTED} !important;
    }}

    button[data-testid="stChatInputSubmitButton"] {{
        background-color: {GREEN} !important;
        border-radius: 999px !important;
    }}

    /* ---------- SQL panel ---------- */

    .sql-header {{
        font-weight: 700;
        color: {WHITE};
        font-size: 0.95rem;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }}

    div[data-testid="stCodeBlock"] pre {{
        background-color: #0d0d0d !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 12px !important;
    }}

    /* ---------- Custom BI table ---------- */

    .bi-table-wrap {{
        max-height: 450px;
        overflow: auto;
        border-radius: 12px;
        border: 1px solid #262626;
        background-color: {CARD};
    }}

    table.bi-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
    }}

    table.bi-table thead th {{
        position: sticky;
        top: 0;
        background-color: {CARD_ALT};
        color: {MUTED};
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.5px;
        font-weight: 700;
        padding: 0.65rem 0.9rem;
        text-align: left;
        border-bottom: 1px solid #333;
        white-space: nowrap;
    }}

    table.bi-table thead th.num {{
        text-align: right;
    }}

    table.bi-table tbody td {{
        padding: 0.55rem 0.9rem;
        color: {WHITE};
        border-bottom: 1px solid #202020;
        white-space: nowrap;
    }}

    table.bi-table tbody td.num {{
        text-align: right;
        font-variant-numeric: tabular-nums;
        color: {GREEN};
        font-weight: 600;
    }}

    table.bi-table tbody tr:hover {{
        background-color: {CARD_ALT};
    }}

    .table-note {{
        color: {MUTED};
        font-size: 0.75rem;
        padding: 0.5rem 0.3rem 0 0.3rem;
    }}

    /* ---------- Error / empty states ---------- */

    .error-card {{
        background-color: rgba(229, 57, 53, 0.08);
        border: 1px solid rgba(229, 57, 53, 0.35);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        color: #ff8a80;
        font-size: 0.9rem;
        margin: 0.6rem 0;
    }}

    .empty-card {{
        background-color: {CARD};
        border: 1px dashed #333;
        border-radius: 12px;
        padding: 1.1rem;
        color: {MUTED};
        font-size: 0.9rem;
        text-align: center;
        margin: 0.6rem 0;
    }}

    /* ---------- Footer ---------- */

    .footer-wrap {{
        text-align: center;
        color: {MUTED};
        font-size: 0.82rem;
        margin-top: 2.8rem;
        padding-top: 1.5rem;
        border-top: 1px solid #262626;
    }}

    .footer-badges {{
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 0.7rem;
    }}

    /* ---------- Responsive tweaks ---------- */

    @media (max-width: 640px) {{
        .hero-title {{ font-size: 1.75rem; }}
        .hero {{ padding: 1.8rem 1.3rem 1.6rem 1.3rem; }}
        .block-container {{ padding-left: 0.8rem; padding-right: 0.8rem; }}
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# FORMATTING HELPERS
# =====================================================

def format_currency(value):
    """972281 -> ₹972,281"""

    try:
        return f"₹{float(value):,.0f}"
    except (TypeError, ValueError):
        return str(value)


def format_number(value):
    """18652354 -> 18.65M"""

    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)

    abs_num = abs(num)

    if abs_num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    if abs_num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    if abs_num >= 1_000:
        return f"{num / 1_000:.2f}K"

    if float(num).is_integer():
        return f"{int(num):,}"

    return f"{num:,.2f}"


def format_percent(value):
    """0.673 -> 67.3%"""

    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)

    if abs(num) <= 1:
        num *= 100

    return f"{num:.1f}%"


def format_date(value):
    """2025-01-01 -> Jan 2025"""

    if value is None:
        return str(value)

    try:
        parsed = pd.to_datetime(value)
        return parsed.strftime("%b %Y")
    except (ValueError, TypeError):
        return str(value)


# =====================================================
# COLUMN TYPE DETECTION
# =====================================================

CURRENCY_HINTS = ["revenue", "price", "amount", "cost", "sales", "earning", "income"]
PERCENT_HINTS = ["percent", "rate", "ratio", "share", "popularity_pct"]
DATE_HINTS = ["date", "month", "year", "day", "period"]
COUNT_HINTS = ["stream", "play", "view", "count", "track", "song", "listener"]


def classify_column(col_name: str, series: pd.Series) -> str:
    """Classify a column as currency / percent / date / number / text."""

    name = col_name.lower()

    if any(h in name for h in CURRENCY_HINTS):
        return "currency"

    if any(h in name for h in PERCENT_HINTS):
        return "percent"

    if any(h in name for h in DATE_HINTS):
        sample = series.dropna().head(5)
        try:
            pd.to_datetime(sample)
            return "date"
        except (ValueError, TypeError):
            pass

    if pd.api.types.is_numeric_dtype(series):
        if any(h in name for h in COUNT_HINTS) or series.abs().max(skipna=True) >= 1000:
            return "number"
        return "raw_number"

    return "text"


def build_display_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df formatted for display only. Never mutates source data."""

    display_df = df.copy()

    for col in display_df.columns:
        col_type = classify_column(col, df[col])

        if col_type == "currency":
            display_df[col] = df[col].apply(format_currency)
        elif col_type == "percent":
            display_df[col] = df[col].apply(format_percent)
        elif col_type == "date":
            display_df[col] = df[col].apply(format_date)
        elif col_type == "number":
            display_df[col] = df[col].apply(format_number)

    return display_df


def render_table_html(display_df: pd.DataFrame, raw_df: pd.DataFrame, max_rows: int = 200):
    """Render a dark, dashboard-styled HTML table instead of the default st.dataframe."""

    if display_df is None or display_df.empty:
        return

    numeric_like_cols = set()
    for col in raw_df.columns:
        col_type = classify_column(col, raw_df[col])
        if col_type in ("currency", "percent", "number", "raw_number"):
            numeric_like_cols.add(col)

    truncated = len(display_df) > max_rows
    view_df = display_df.head(max_rows)

    header_cells = "".join(
        f'<th class="{"num" if c in numeric_like_cols else ""}">'
        f'{html_lib.escape(str(c).replace("_", " ").title())}</th>'
        for c in view_df.columns
    )

    row_chunks = []
    for _, row in view_df.iterrows():
        cells = "".join(
            f'<td class="{"num" if c in numeric_like_cols else ""}">'
            f'{html_lib.escape(str(row[c]))}</td>'
            for c in view_df.columns
        )
        row_chunks.append(f"<tr>{cells}</tr>")

    rows_html = "".join(row_chunks)

    note = ""
    if truncated:
        note = (
            f'<div class="table-note">Showing first {max_rows} '
            f'of {len(display_df)} rows</div>'
        )

    table_html = f"""
    <div class="bi-table-wrap">
        <table class="bi-table">
            <thead><tr>{header_cells}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    {note}
    """

    st.markdown(table_html, unsafe_allow_html=True)


# =====================================================
# KPI GENERATION
# =====================================================

def generate_kpis(df: pd.DataFrame):
    """Inspect the result set and auto-generate up to 4 relevant KPI cards.

    Priority: when a date column and a metric column are both present,
    show Total / Monthly Average / Best Month / Worst Month - the classic
    BI dashboard shape. Otherwise fall back to a generic column scan.
    """

    if df is None or df.empty:
        return []

    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    date_cols = [c for c in df.columns if classify_column(c, df[c]) == "date"]

    # ---------------- Priority path: date + metric ----------------

    if date_cols and numeric_cols:
        d_col = date_cols[0]
        m_col = numeric_cols[0]
        m_type = classify_column(m_col, df[m_col])

        if m_type == "currency":
            fmt = format_currency
        elif m_type == "percent":
            fmt = format_percent
        else:
            fmt = format_number

        try:
            grouped = df.groupby(d_col)[m_col].sum()

            total = grouped.sum()
            avg = grouped.mean()
            best = grouped.idxmax()
            worst = grouped.idxmin()

            label = m_col.replace("_", " ").title()

            return [
                (label, fmt(total)),
                ("Monthly Average", fmt(avg)),
                ("Best Month", format_date(best)),
                ("Worst Month", format_date(worst)),
            ]
        except (ValueError, TypeError, KeyError):
            pass

    # ---------------- Fallback: generic column scan ----------------

    kpis = []
    text_cols = [c for c in df.columns if c not in numeric_cols]

    for col in numeric_cols:
        col_type = classify_column(col, df[col])
        total = df[col].sum(skipna=True)
        avg = df[col].mean(skipna=True)
        label = col.replace("_", " ").title()

        if col_type == "currency":
            kpis.append((f"Total {label}", format_currency(total)))
            kpis.append((f"Avg {label}", format_currency(avg)))
        elif col_type == "number":
            kpis.append((f"Total {label}", format_number(total)))
        elif col_type == "percent":
            kpis.append((f"Avg {label}", format_percent(avg)))

    for col in text_cols:
        name = col.lower()
        if any(h in name for h in ["artist", "country", "genre", "album", "label"]):
            kpis.append((f"Unique {col.replace('_', ' ').title()}", str(df[col].nunique())))

    seen = set()
    unique_kpis = []
    for label, value in kpis:
        if label not in seen:
            unique_kpis.append((label, value))
            seen.add(label)

    return unique_kpis[:4]


def render_kpis(df: pd.DataFrame, title: str = "📈 Key Metrics"):
    kpis = generate_kpis(df)

    if not kpis:
        return

    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

    cols = st.columns(len(kpis))

    for col, (label, value) in zip(cols, kpis):
        with col:
            st.metric(label=label, value=value)


# =====================================================
# CHART THEMING
# =====================================================

def theme_chart(fig):
    """Re-skin an existing plotly figure with the Spotify dark palette."""

    if fig is None:
        return None

    fig.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=WHITE, family="-apple-system, Segoe UI, Helvetica Neue, Arial"),
        title_font=dict(color=WHITE, size=16),
        margin=dict(t=55, l=30, r=30, b=40),
        hoverlabel=dict(
            bgcolor=CARD_ALT,
            font_color=WHITE,
            bordercolor=GREEN,
        ),
        legend=dict(font=dict(color=MUTED)),
    )

    fig.update_xaxes(
        color=MUTED,
        gridcolor="#2a2a2a",
        zerolinecolor="#2a2a2a",
        title_font=dict(color=MUTED),
    )

    fig.update_yaxes(
        color=MUTED,
        gridcolor="#2a2a2a",
        zerolinecolor="#2a2a2a",
        title_font=dict(color=MUTED),
    )

    for trace in fig.data:
        if trace.type == "bar":
            trace.marker.color = GREEN
            trace.marker.line = dict(width=0)
            if hasattr(trace, "textfont"):
                trace.textfont = dict(color=WHITE)
        elif trace.type == "scatter":
            if trace.mode and "lines" in trace.mode:
                trace.line.color = GREEN
                trace.line.width = 3
            if trace.marker:
                trace.marker.color = GREEN

    return fig


def chart_section_title(fig) -> str:
    if fig is not None and fig.layout.title and fig.layout.title.text:
        return f"📊 {fig.layout.title.text.title()}"
    return "📋 Results"


# =====================================================
# BACKEND CONNECTION CHECK
# =====================================================

def check_backend_connection():
    try:
        resp = requests.get(BACKEND_URL, timeout=2)
        return resp.status_code == 200
    except requests.exceptions.RequestException:
        return False


# =====================================================
# RESULT RENDERING (chart + table, responsive)
# =====================================================

def render_sql(sql: str):
    st.markdown('<div class="sql-header">🧠 Generated SQL</div>', unsafe_allow_html=True)
    st.code(sql or "-- no SQL generated for this question", language="sql")


def render_results(rows, kpi_title="📈 Key Metrics"):
    if not rows:
        st.markdown(
            '<div class="empty-card">No rows were returned for this question.</div>',
            unsafe_allow_html=True,
        )
        return

    df = pd.DataFrame(rows)

    if df.empty:
        st.markdown(
            '<div class="empty-card">No rows were returned for this question.</div>',
            unsafe_allow_html=True,
        )
        return

    render_kpis(df, title=kpi_title)

    fig = theme_chart(create_chart(df))
    display_df = build_display_dataframe(df)

    st.markdown(
        f'<div class="section-title">{chart_section_title(fig)}</div>',
        unsafe_allow_html=True,
    )

    if fig is not None:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            render_table_html(display_df, df)
    else:
        # No chart available - show only the table, full width
        render_table_html(display_df, df)


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


def ask_question(q: str):
    st.session_state.pending_question = q


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown('<div class="sb-brand">🎵 Spotify Intelligence</div>', unsafe_allow_html=True)

    backend_up = check_backend_connection()

    st.markdown('<div class="sb-section-title">🟢 System Status</div>', unsafe_allow_html=True)

    backend_value = (
        '<span class="value ok">Online</span>' if backend_up
        else '<span class="value bad">Offline</span>'
    )

    st.markdown(
        f"""
        <div class="status-row"><span class="label">Backend</span>{backend_value}</div>
        <div class="status-row"><span class="label">LLM</span><span class="value">Llama 3.3</span></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<hr class="sb-divider" />', unsafe_allow_html=True)

    st.markdown('<div class="sb-section-title">📊 SQL Analytics</div>', unsafe_allow_html=True)

    sql_questions = {
        "Top Genres": "What are the top genres by popularity?",
        "Monthly Revenue": "Show monthly revenue",
        "Top Artists": "Who are the top artists by popularity?",
        "Countries": "Show revenue by country",
    }
    for label, q in sql_questions.items():
        st.button(label, key=f"nav_{label}", on_click=ask_question, args=(q,), use_container_width=True)

    st.markdown('<hr class="sb-divider" />', unsafe_allow_html=True)

    st.markdown('<div class="sb-section-title">📄 Report Intelligence</div>', unsafe_allow_html=True)

    report_questions = {
        "AI Strategy": "What is Spotify's AI strategy according to the annual report?",
        "Financial Risks": "What are the financial risks mentioned in the annual report?",
        "CEO Letter": "Summarize the CEO letter from the annual report.",
        "Business Model": "Describe Spotify's business model from the annual report.",
    }
    for label, q in report_questions.items():
        st.button(label, key=f"nav_{label}", on_click=ask_question, args=(q,), use_container_width=True)

    st.markdown('<hr class="sb-divider" />', unsafe_allow_html=True)

    st.markdown('<div class="sb-section-title">🤖 Hybrid Analysis</div>', unsafe_allow_html=True)

    hybrid_questions = {
        "Revenue Comparison": "Compare our revenue with Spotify's reported revenue.",
        "Growth Comparison": "Compare our growth with Spotify's reported growth.",
    }
    for label, q in hybrid_questions.items():
        st.button(label, key=f"nav_{label}", on_click=ask_question, args=(q,), use_container_width=True)

    st.markdown('<hr class="sb-divider" />', unsafe_allow_html=True)

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

# =====================================================
# HERO HEADER
# =====================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🎵 Spotify Intelligence Platform</div>
        <div class="hero-subtitle">Enterprise AI Business Intelligence</div>
        <div class="hero-tagline">Natural Language SQL &bull; Annual Report Intelligence &bull; Hybrid Analytics</div>
        <div class="badge-row">
            <span class="tech-badge">Llama 3.3</span>
            <span class="tech-badge">FastAPI</span>
            <span class="tech-badge">PostgreSQL</span>
            <span class="tech-badge">LangChain</span>
            <span class="tech-badge">Chroma</span>
        </div>
    </div>
    <div class="hero-accent"></div>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# TODAY'S INSIGHTS (KPI strip from most recent result)
# =====================================================

last_assistant_rows = None
for msg in reversed(st.session_state.messages):
    if msg["role"] == "assistant" and msg.get("rows"):
        last_assistant_rows = msg["rows"]
        break

if last_assistant_rows:
    render_kpis(pd.DataFrame(last_assistant_rows), title="📈 Today's Insights")

# =====================================================
# WELCOME SCREEN
# =====================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome-wrap">
            <div class="eyebrow">Today's Insights</div>
            <div class="welcome-title">🎵 Welcome to Spotify Intelligence</div>
            <div class="welcome-sub">Ask anything about business metrics, revenue, Spotify reports, or hybrid analysis.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    example_cards = [
        ("📊 Business", "Ask about metrics & KPIs", "Show me our key business metrics"),
        ("💰 Revenue", "Monthly revenue breakdown", "Show monthly revenue"),
        ("📄 Reports", "Annual report intelligence", "Summarize the AI strategy from the annual report."),
        ("🔀 Hybrid", "Blend data with reports", "Compare our revenue with Spotify's reported figures."),
    ]

    row1 = st.columns(2)
    row2 = st.columns(2)
    card_slots = row1 + row2

    for col, (title, desc, q) in zip(card_slots, example_cards):
        with col:
            st.button(
                title,
                key=f"card_{title}",
                help=desc,
                on_click=ask_question,
                args=(q,),
                use_container_width=True,
            )

# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            if "sql" in message:
                with st.expander("🧠 Generated SQL", expanded=False):
                    st.code(message["sql"], language="sql")

            if "rows" in message:
                rows = message["rows"]

                if rows:
                    df = pd.DataFrame(rows)

                    if not df.empty:
                        fig = theme_chart(create_chart(df))
                        display_df = build_display_dataframe(df)

                        st.markdown(
                            f'<div class="section-title">{chart_section_title(fig)}</div>',
                            unsafe_allow_html=True,
                        )

                        if fig is not None:
                            col1, col2 = st.columns([1, 1])

                            with col1:
                                st.plotly_chart(fig, use_container_width=True)

                            with col2:
                                render_table_html(display_df, df)
                        else:
                            render_table_html(display_df, df)

# =====================================================
# CHAT INPUT
# =====================================================

typed_question = st.chat_input("Ask a business question...")

question = None

if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None
elif typed_question:
    question = typed_question

# =====================================================
# PROCESS QUESTION
# =====================================================

if question:

    st.chat_message("user").markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.spinner("🎵 Spotify AI is analyzing your data..."):

        try:
            response = requests.post(
                ASK_ENDPOINT,
                json={"question": question},
                timeout=120,
            )

            if response.status_code == 200:

                data = response.json()

                answer = data.get("answer", "")
                sql = data.get("generated_sql", "")
                rows = data.get("rows", [])

                with st.chat_message("assistant"):

                    st.markdown(answer)

                    render_sql(sql)

                    render_results(rows)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sql": sql,
                        "rows": rows,
                    }
                )

            else:
                with st.chat_message("assistant"):
                    st.markdown(
                        f"""
                        <div class="error-card">
                            ⚠️ The backend returned an error (status {response.status_code}).
                            Please try rephrasing your question or try again shortly.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        except requests.exceptions.RequestException:
            with st.chat_message("assistant"):
                st.markdown(
                    """
                    <div class="error-card">
                        ⚠️ Couldn't reach the Spotify Intelligence backend. Please make sure
                        the API server is running and try again.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer-wrap">
        <div class="footer-badges">
            <span class="tech-badge">FastAPI</span>
            <span class="tech-badge">PostgreSQL</span>
            <span class="tech-badge">LangChain</span>
            <span class="tech-badge">Groq</span>
            <span class="tech-badge">Chroma</span>
            <span class="tech-badge">Streamlit</span>
        </div>
        Built with FastAPI &middot; PostgreSQL &middot; LangChain &middot; Groq &middot; Chroma &middot; Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)