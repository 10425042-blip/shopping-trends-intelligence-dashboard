from __future__ import annotations

from html import escape
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "shopping_trends.csv"

BACKGROUND_URL = "https://images.pexels.com/photos/5865240/pexels-photo-5865240.jpeg?auto=compress&cs=tinysrgb&w=1920"

SEASON_ORDER = ["Spring", "Summer", "Fall", "Winter"]
SIZE_ORDER = ["S", "M", "L", "XL"]
FREQUENCY_ORDER = ["Weekly", "Fortnightly", "Bi-Weekly", "Monthly", "Quarterly", "Every 3 Months", "Annually"]
DASHBOARD_VIEWS = [
    "Overview",
    "Customer Insights",
    "Product & Sales",
    "Data Explorer",
]

COLUMN_MAP = {
    "Customer ID": "customer_id",
    "Age": "age",
    "Gender": "gender",
    "Item Purchased": "item_purchased",
    "Category": "category",
    "Purchase Amount (USD)": "purchase_amount",
    "Location": "location",
    "Size": "size",
    "Color": "color",
    "Season": "season",
    "Review Rating": "review_rating",
    "Subscription Status": "subscription_status",
    "Payment Method": "payment_method",
    "Shipping Type": "shipping_type",
    "Discount Applied": "discount_applied",
    "Promo Code Used": "promo_code_used",
    "Previous Purchases": "previous_purchases",
    "Frequency of Purchases": "frequency_of_purchases",
}

DEFAULT_FILTERS = {
    "gender_filter": [],
    "subscription_filter": [],
    "age_filter": (18, 70),
    "rating_filter": (2.5, 5.0),
    "category_filter": [],
    "item_filter": [],
    "size_filter": [],
    "color_filter": [],
    "season_filter": [],
    "location_filter": [],
    "payment_filter": [],
    "shipping_filter": [],
    "discount_filter": [],
    "promo_filter": [],
    "frequency_filter": [],
    "amount_filter": (20, 100),
}

DASHBOARD_COLORS = {
    "primary": "#D7FF3F",
    "secondary": "#7C3AED",
    "success": "#38F7B0",
    "warning": "#FFB86C",
    "danger": "#FF4D8D",
    "surface": "#050506",
    "text": "#FAFAFA",
    "muted": "#A8AAB6",
    "grid": "rgba(250,250,250,0.10)",
}

COLORWAY = [
    DASHBOARD_COLORS["primary"],
    DASHBOARD_COLORS["success"],
    "#54D6FF",
    "#A78BFA",
    DASHBOARD_COLORS["danger"],
    DASHBOARD_COLORS["warning"],
    "#2DD4BF",
]

DISPLAY_LABELS = {
    "age": "Age",
    "age_group": "Age group",
    "avg_order": "Average order",
    "category": "Category",
    "color": "Color",
    "count": "Purchases",
    "customer_id": "Customer ID",
    "discount_applied": "Discount applied",
    "frequency_of_purchases": "Purchase frequency",
    "gender": "Gender",
    "item_purchased": "Item purchased",
    "location": "Location",
    "payment_method": "Payment method",
    "purchase_amount": "Purchase amount (USD)",
    "purchases": "Purchases",
    "review_rating": "Review rating",
    "season": "Season",
    "shipping_type": "Shipping type",
    "size": "Size",
    "subscription_status": "Subscription status",
    "total_sales": "Total spending (USD)",
}


st.set_page_config(
    page_title="Shopping Trends Intelligence",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="auto",
)


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        :root {{
            --surface: #050506;
            --surface-soft: rgba(18, 18, 22, 0.74);
            --glass: rgba(255, 255, 255, 0.075);
            --glass-strong: rgba(255, 255, 255, 0.105);
            --line: rgba(255, 255, 255, 0.14);
            --line-strong: rgba(215, 255, 63, 0.34);
            --text: #FAFAFA;
            --muted: #A8AAB6;
            --primary: #D7FF3F;
            --secondary: #7C3AED;
            --success: #38F7B0;
            --warning: #FFB86C;
            --danger: #FF4D8D;
            --teal: #2DD4BF;
            --blue: #54D6FF;
            --pink: #F472B6;
            --radius: 24px;
            --shadow: 0 30px 110px rgba(0,0,0,0.64), inset 0 1px 0 rgba(255,255,255,0.13);
            --glow: 0 0 28px rgba(215,255,63,0.18), 0 0 68px rgba(124,58,237,0.12);
        }}

        html,
        body {{
            height: 100%;
            overflow: hidden;
        }}

        .stApp {{
            color: var(--text);
            position: relative;
            isolation: isolate;
            min-height: 100dvh;
            overflow: hidden;
            background:
                linear-gradient(180deg, rgba(5,5,6,0.76), rgba(5,5,6,0.94) 54%, rgba(0,0,0,0.98)),
                linear-gradient(115deg, rgba(215,255,63,0.10), transparent 36%),
                linear-gradient(245deg, rgba(124,58,237,0.20), transparent 42%),
                url("{BACKGROUND_URL}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            inset: -18% -10%;
            z-index: 0;
            pointer-events: none;
            background:
                linear-gradient(90deg, transparent 0 10%, rgba(255,255,255,0.055) 10.5%, transparent 12% 36%, rgba(84,214,255,0.035) 37%, transparent 39% 64%, rgba(215,255,63,0.045) 65%, transparent 67%),
                radial-gradient(ellipse at 50% 108%, rgba(215,255,63,0.20), transparent 46%),
                radial-gradient(ellipse at 12% 18%, rgba(84,214,255,0.15), transparent 34%),
                radial-gradient(ellipse at 86% 14%, rgba(244,114,182,0.12), transparent 34%),
                repeating-linear-gradient(90deg, rgba(255,255,255,0.025) 0 1px, transparent 1px 112px);
            filter: blur(18px) saturate(140%);
            opacity: 0.9;
        }}

        .stApp::after {{
            content: "";
            position: fixed;
            inset: auto -10% -12% -10%;
            height: 42vh;
            z-index: 0;
            pointer-events: none;
            background:
                radial-gradient(ellipse at 50% 70%, rgba(255,255,255,0.16), transparent 52%),
                linear-gradient(0deg, rgba(0,0,0,0.88), rgba(7,7,9,0.14) 70%, transparent);
            filter: blur(30px);
            opacity: 0.72;
        }}

        div[data-testid="stAppViewContainer"] {{
            position: relative;
            z-index: 2;
            height: 100dvh;
            overflow-x: hidden;
            overflow-y: auto;
            scrollbar-gutter: stable;
        }}

        header[data-testid="stHeader"] {{
            z-index: 5;
            background: rgba(5,5,6,0.26);
            backdrop-filter: blur(18px) saturate(140%);
        }}

        section[data-testid="stSidebar"] {{
            z-index: 3;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.035)),
                rgba(5,5,6,0.82);
            border-right: 1px solid rgba(255,255,255,0.14);
            box-shadow: 26px 0 80px rgba(0,0,0,0.42), inset -1px 0 0 rgba(255,255,255,0.05);
            backdrop-filter: blur(34px) saturate(170%);
        }}

        section[data-testid="stSidebar"] * {{
            color: var(--text);
        }}

        section[data-testid="stSidebar"] [role="radiogroup"] label {{
            padding: 8px 10px;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 999px;
            background: rgba(255,255,255,0.035);
        }}

        section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{
            border-color: rgba(215,255,63,0.48);
            background: rgba(215,255,63,0.10);
            box-shadow: 0 0 24px rgba(215,255,63,0.12);
        }}

        .block-container {{
            position: relative;
            z-index: 2;
            padding-top: 0.85rem;
            padding-bottom: 1.15rem;
            max-width: 1440px;
        }}

        div[data-testid="stButton"] > button {{
            width: 100%;
            min-height: 46px;
            color: #FAFAFA;
            background:
                linear-gradient(135deg, rgba(215,255,63,0.28), rgba(84,214,255,0.14)),
                rgba(255,255,255,0.08);
            border: 1px solid rgba(215,255,63,0.38);
            border-radius: 999px;
            box-shadow: 0 14px 44px rgba(215,255,63,0.13), inset 0 1px 0 rgba(255,255,255,0.18);
            font-weight: 800;
            backdrop-filter: blur(18px);
        }}

        div[data-testid="stButton"] > button:hover {{
            border-color: rgba(215,255,63,0.68);
            background:
                linear-gradient(135deg, rgba(215,255,63,0.38), rgba(124,58,237,0.16)),
                rgba(255,255,255,0.10);
            box-shadow: 0 20px 64px rgba(215,255,63,0.22), inset 0 1px 0 rgba(255,255,255,0.22);
        }}

        div[data-testid="stButton"] > button:focus-visible {{
            outline: 2px solid var(--success);
            outline-offset: 3px;
        }}

        div[data-testid="stPlotlyChart"],
        div[data-testid="stDataFrame"] {{
            position: relative;
            overflow: hidden;
            padding: 12px;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.095), rgba(255,255,255,0.032)),
                rgba(5,5,6,0.52);
            border: 1px solid var(--line);
            border-radius: 18px;
            box-shadow: var(--shadow), var(--glow);
            backdrop-filter: blur(24px) saturate(165%);
        }}

        div[data-testid="stPlotlyChart"]:hover,
        div[data-testid="stDataFrame"]:hover {{
            border-color: rgba(215,255,63,0.42);
            background:
                linear-gradient(180deg, rgba(255,255,255,0.12), rgba(255,255,255,0.04)),
                rgba(5,5,6,0.58);
        }}

        div[data-testid="stPlotlyChart"]::before,
        div[data-testid="stDataFrame"]::before,
        .hero-card::before {{
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(115deg, transparent 0%, rgba(255,255,255,0.15) 38%, transparent 62%),
                linear-gradient(180deg, rgba(255,255,255,0.08), transparent 28%);
            pointer-events: none;
        }}

        div[data-testid="stPlotlyChart"] svg .pielayer path {{
            transform-origin: center;
        }}

        .landing-wrap {{
            min-height: 0;
            display: grid;
            place-items: center;
            padding: clamp(32px, 8vh, 86px) 0 20px;
        }}

        .hero-card {{
            position: relative;
            width: min(980px, 100%);
            overflow: hidden;
            padding: 44px;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.035)),
                linear-gradient(130deg, rgba(215,255,63,0.09), rgba(124,58,237,0.13)),
                rgba(5,5,6,0.58);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 28px;
            box-shadow: var(--shadow), 0 0 90px rgba(215,255,63,0.08);
            backdrop-filter: blur(34px) saturate(170%);
        }}

        .hero-label {{
            margin: 0 0 10px 0;
            color: var(--primary);
            text-shadow: 0 0 22px rgba(215,255,63,0.20);
            font-size: 12px;
            font-weight: 900;
            letter-spacing: 0;
            text-transform: uppercase;
        }}

        .hero-title {{
            margin: 0;
            max-width: 860px;
            color: var(--text);
            font-size: clamp(40px, 7vw, 84px);
            font-weight: 300;
            line-height: 0.98;
            text-shadow: 0 18px 64px rgba(0,0,0,0.56);
        }}

        .hero-copy {{
            max-width: 780px;
            margin: 24px 0 28px 0;
            color: #D4D4D8;
            font-size: 18px;
            line-height: 1.65;
        }}

        .hero-stat-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
            margin-top: 24px;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 10px;
            margin: 8px 0 10px 0;
        }}

        .hero-stat,
        .kpi-card,
        .takeaway-card {{
            position: relative;
            overflow: hidden;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.105), rgba(255,255,255,0.03)),
                rgba(5,5,6,0.45);
            border: 1px solid var(--line);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            backdrop-filter: blur(22px) saturate(160%);
        }}

        .hero-stat:hover,
        .kpi-card:hover {{
            border-color: rgba(215,255,63,0.42);
            box-shadow: var(--shadow), 0 0 42px rgba(215,255,63,0.12);
            background:
                linear-gradient(180deg, rgba(255,255,255,0.13), rgba(255,255,255,0.04)),
                rgba(5,5,6,0.54);
        }}

        .hero-stat {{
            padding: 16px;
        }}

        .hero-stat span,
        .kpi-card span {{
            display: block;
            color: var(--muted);
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
        }}

        .hero-stat strong,
        .kpi-card strong {{
            display: block;
            margin-top: 8px;
            color: var(--text);
            font-size: 28px;
            font-weight: 500;
            line-height: 1;
            text-shadow: 0 0 24px rgba(255,255,255,0.10);
        }}

        .kpi-card {{
            min-height: 78px;
            padding: 12px 14px;
            border-radius: 16px;
        }}

        .kpi-card em {{
            display: none;
            margin-top: 6px;
            color: var(--muted);
            font-size: 11px;
            font-style: normal;
        }}

        .kpi-card strong {{
            margin-top: 7px;
            font-size: 22px;
        }}

        .section-title {{
            margin: 16px 0 6px 0;
            color: var(--text);
            font-size: 22px;
            font-weight: 650;
        }}

        .section-copy {{
            margin: 0 0 10px 0;
            color: var(--muted);
            font-size: 14px;
        }}

        .chart-caption {{
            margin: -2px 0 16px 0;
            padding: 0 4px;
            color: #C9CBD3;
            font-size: 13px;
            line-height: 1.45;
        }}

        .filter-summary {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 0 0 10px 0;
        }}

        .field-label {{
            color: #E7E7EA;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
        }}

        .field-label {{
            margin: 0 0 4px 0;
            color: var(--primary);
        }}

        .filter-chip {{
            padding: 8px 12px;
            color: #E7E7EA;
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.13);
            border-radius: 999px;
            font-size: 12px;
            font-weight: 750;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
        }}

        .takeaway-card {{
            display: grid;
            grid-template-columns: minmax(120px, 0.18fr) 1fr;
            gap: 4px 18px;
            align-items: center;
            margin: 8px 0 8px 0;
            padding: 12px 14px;
            border-radius: 16px;
        }}

        .takeaway-card span {{
            color: var(--primary);
            font-size: 11px;
            font-weight: 900;
            text-transform: uppercase;
        }}

        .takeaway-card strong {{
            color: var(--text);
            font-size: 15px;
            font-weight: 760;
            line-height: 1.35;
        }}

        .takeaway-card p {{
            grid-column: 2;
            margin: 0;
            color: var(--text);
            font-size: 13px;
            line-height: 1.45;
            opacity: 0.86;
        }}

        .filter-caption {{
            padding: 12px 14px;
            margin: 12px 0;
            color: #D4D4D8;
            background: rgba(255,255,255,0.055);
            border: 1px solid rgba(255,255,255,0.13);
            border-radius: 18px;
            font-size: 13px;
            line-height: 1.45;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
        }}

        .about-card {{
            max-width: 980px;
            margin: 20px auto 0 auto;
            padding: 18px 20px;
            color: #D4D4D8;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.085), rgba(255,255,255,0.03)),
                rgba(5,5,6,0.48);
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 18px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(22px) saturate(155%);
        }}

        .about-card h2 {{
            margin: 0 0 8px 0;
            color: var(--text);
            font-size: 18px;
        }}

        .about-card p {{
            margin: 0;
            font-size: 14px;
            line-height: 1.55;
        }}

        .about-card strong {{
            color: var(--primary);
        }}

        .no-data {{
            padding: 28px;
            color: #FDE68A;
            background: rgba(245,158,11,0.1);
            border: 1px solid rgba(245,158,11,0.32);
            border-radius: var(--radius);
        }}

        @media (max-width: 1200px) {{
            .kpi-grid {{
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }}
        }}

        @media (max-width: 900px) {{
            .block-container {{
                padding-top: 0.65rem;
                padding-bottom: 0.9rem;
            }}

            .hero-card {{
                padding: 24px;
                border-radius: 18px;
            }}

            .landing-wrap {{
                padding-top: 18px;
            }}

            .hero-title {{
                font-size: clamp(36px, 10vw, 48px);
                line-height: 1.03;
            }}

            .hero-copy {{
                font-size: 15px;
                line-height: 1.55;
            }}

            .hero-stat {{
                padding: 12px;
            }}

            .hero-stat strong {{
                font-size: 24px;
            }}

            .kpi-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}

            .takeaway-card {{
                grid-template-columns: 1fr;
            }}

            .takeaway-card p {{
                grid-column: 1;
            }}

            .hero-stat-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH).rename(columns=COLUMN_MAP)
    numeric_columns = ["age", "purchase_amount", "review_rating", "previous_purchases"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    text_columns = [column for column in df.columns if column not in numeric_columns]
    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 24, 34, 44, 54, 64, 120],
        labels=["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
        include_lowest=True,
    )
    return df


def money(value: float | int) -> str:
    return f"${value:,.0f}"


def number(value: float | int) -> str:
    return f"{value:,.0f}"


def pct(value: float | int) -> str:
    return f"{value:.1f}%"


def label_for(column: str) -> str:
    return DISPLAY_LABELS.get(column, column.replace("_", " ").title())


def sorted_unique(df: pd.DataFrame, column: str, order: list[str] | None = None) -> list[str]:
    values = [value for value in df[column].dropna().unique().tolist() if value != ""]
    if order:
        ordered = [value for value in order if value in values]
        ordered.extend(sorted(value for value in values if value not in ordered))
        return ordered
    return sorted(values)


def initialize_state(df: pd.DataFrame) -> None:
    dynamic_defaults = DEFAULT_FILTERS.copy()
    dynamic_defaults["age_filter"] = (int(df["age"].min()), int(df["age"].max()))
    dynamic_defaults["rating_filter"] = (float(df["review_rating"].min()), float(df["review_rating"].max()))
    dynamic_defaults["amount_filter"] = (int(df["purchase_amount"].min()), int(df["purchase_amount"].max()))
    for key, value in dynamic_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if "entered_dashboard" not in st.session_state:
        st.session_state.entered_dashboard = False
    if "dashboard_view" not in st.session_state:
        st.session_state.dashboard_view = DASHBOARD_VIEWS[0]


def reset_filters(df: pd.DataFrame) -> None:
    st.session_state.gender_filter = []
    st.session_state.subscription_filter = []
    st.session_state.age_filter = (int(df["age"].min()), int(df["age"].max()))
    st.session_state.rating_filter = (float(df["review_rating"].min()), float(df["review_rating"].max()))
    st.session_state.category_filter = []
    st.session_state.item_filter = []
    st.session_state.size_filter = []
    st.session_state.color_filter = []
    st.session_state.season_filter = []
    st.session_state.location_filter = []
    st.session_state.payment_filter = []
    st.session_state.shipping_filter = []
    st.session_state.discount_filter = []
    st.session_state.promo_filter = []
    st.session_state.frequency_filter = []
    st.session_state.amount_filter = (int(df["purchase_amount"].min()), int(df["purchase_amount"].max()))


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()
    multi_filters = {
        "gender": st.session_state.gender_filter,
        "subscription_status": st.session_state.subscription_filter,
        "category": st.session_state.category_filter,
        "item_purchased": st.session_state.item_filter,
        "size": st.session_state.size_filter,
        "color": st.session_state.color_filter,
        "season": st.session_state.season_filter,
        "location": st.session_state.location_filter,
        "payment_method": st.session_state.payment_filter,
        "shipping_type": st.session_state.shipping_filter,
        "discount_applied": st.session_state.discount_filter,
        "promo_code_used": st.session_state.promo_filter,
        "frequency_of_purchases": st.session_state.frequency_filter,
    }
    for column, values in multi_filters.items():
        if values:
            filtered = filtered[filtered[column].isin(values)]

    age_min, age_max = st.session_state.age_filter
    rating_min, rating_max = st.session_state.rating_filter
    amount_min, amount_max = st.session_state.amount_filter
    filtered = filtered[filtered["age"].between(age_min, age_max)]
    filtered = filtered[filtered["review_rating"].between(rating_min, rating_max)]
    filtered = filtered[filtered["purchase_amount"].between(amount_min, amount_max)]
    return filtered


def active_filter_count(df: pd.DataFrame) -> int:
    defaults = {
        "age_filter": (int(df["age"].min()), int(df["age"].max())),
        "rating_filter": (float(df["review_rating"].min()), float(df["review_rating"].max())),
        "amount_filter": (int(df["purchase_amount"].min()), int(df["purchase_amount"].max())),
    }
    count = 0
    for key in DEFAULT_FILTERS:
        value = st.session_state.get(key)
        if isinstance(value, list) and value:
            count += 1
        elif key in defaults and tuple(value) != defaults[key]:
            count += 1
    return count


def active_filter_labels(df: pd.DataFrame) -> list[str]:
    defaults = {
        "age_filter": (int(df["age"].min()), int(df["age"].max())),
        "rating_filter": (float(df["review_rating"].min()), float(df["review_rating"].max())),
        "amount_filter": (int(df["purchase_amount"].min()), int(df["purchase_amount"].max())),
    }
    labels = []
    named_filters = {
        "gender_filter": "Gender",
        "subscription_filter": "Subscription",
        "category_filter": "Category",
        "item_filter": "Item",
        "size_filter": "Size",
        "color_filter": "Color",
        "season_filter": "Season",
        "location_filter": "Location",
        "payment_filter": "Payment",
        "shipping_filter": "Shipping",
        "discount_filter": "Discount",
        "promo_filter": "Promo",
        "frequency_filter": "Frequency",
    }
    for key, label in named_filters.items():
        values = st.session_state.get(key, [])
        if values:
            preview = ", ".join(str(value) for value in values[:2])
            suffix = f" +{len(values) - 2}" if len(values) > 2 else ""
            labels.append(f"{label}: {preview}{suffix}")

    age_range = st.session_state.get("age_filter")
    rating_range = st.session_state.get("rating_filter")
    amount_range = st.session_state.get("amount_filter")
    if age_range and tuple(age_range) != defaults["age_filter"]:
        labels.append(f"Age: {age_range[0]}-{age_range[1]}")
    if rating_range and tuple(rating_range) != defaults["rating_filter"]:
        labels.append(f"Rating: {rating_range[0]:.1f}-{rating_range[1]:.1f}")
    if amount_range and tuple(amount_range) != defaults["amount_filter"]:
        labels.append(f"Amount: ${amount_range[0]:,.0f}-${amount_range[1]:,.0f}")
    return labels


def sidebar_filters(df: pd.DataFrame) -> None:
    with st.sidebar:
        st.markdown("### Filters")
        st.button("Reset filters", on_click=reset_filters, args=(df,))
        st.markdown(
            f"<div class='filter-caption'>All filters work together across the dashboard. Active filters: <b>{active_filter_count(df)}</b>.</div>",
            unsafe_allow_html=True,
        )

        with st.expander("Customer filters", expanded=True):
            st.multiselect("Gender", sorted_unique(df, "gender"), key="gender_filter")
            st.slider("Age range", int(df["age"].min()), int(df["age"].max()), key="age_filter")
            st.multiselect("Subscription status", sorted_unique(df, "subscription_status"), key="subscription_filter")
            st.slider(
                "Review rating range",
                float(df["review_rating"].min()),
                float(df["review_rating"].max()),
                key="rating_filter",
                step=0.1,
            )

        with st.expander("Product filters", expanded=False):
            st.multiselect("Category", sorted_unique(df, "category"), key="category_filter")
            st.multiselect("Item purchased", sorted_unique(df, "item_purchased"), key="item_filter")
            st.multiselect("Size", sorted_unique(df, "size", SIZE_ORDER), key="size_filter")
            st.multiselect("Color", sorted_unique(df, "color"), key="color_filter")

        with st.expander("Market filters", expanded=False):
            st.multiselect("Season", sorted_unique(df, "season", SEASON_ORDER), key="season_filter")
            st.multiselect("Location", sorted_unique(df, "location"), key="location_filter")

        with st.expander("Transaction filters", expanded=False):
            st.multiselect("Payment method", sorted_unique(df, "payment_method"), key="payment_filter")
            st.multiselect("Shipping type", sorted_unique(df, "shipping_type"), key="shipping_filter")
            st.multiselect("Discount applied", sorted_unique(df, "discount_applied"), key="discount_filter")
            st.multiselect("Promo code used", sorted_unique(df, "promo_code_used"), key="promo_filter")
            st.multiselect(
                "Purchase frequency",
                sorted_unique(df, "frequency_of_purchases", FREQUENCY_ORDER),
                key="frequency_filter",
            )
            st.slider(
                "Purchase amount range",
                int(df["purchase_amount"].min()),
                int(df["purchase_amount"].max()),
                key="amount_filter",
            )


def empty_figure(title: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text="No matching records. Reset filters or widen the selected range.",
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={"color": DASHBOARD_COLORS["muted"], "size": 14},
    )
    return style_figure(fig, title)


def style_figure(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title={"text": title, "x": 0.02, "xanchor": "left", "font": {"size": 18, "color": DASHBOARD_COLORS["text"]}},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "IBM Plex Sans, Inter, Segoe UI, Arial, sans-serif", "color": DASHBOARD_COLORS["text"], "size": 13},
        colorway=COLORWAY,
        height=430,
        margin={"t": 58, "r": 42, "b": 48, "l": 58},
        legend={"orientation": "h", "y": 1.03, "x": 1, "xanchor": "right", "font": {"color": DASHBOARD_COLORS["muted"]}},
        hoverlabel={"bgcolor": "#09090B", "font_color": "#FAFAFA", "bordercolor": DASHBOARD_COLORS["primary"]},
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=DASHBOARD_COLORS["grid"],
        zeroline=False,
        tickfont={"color": DASHBOARD_COLORS["muted"]},
        title_font={"color": DASHBOARD_COLORS["muted"]},
        automargin=True,
    )
    fig.update_yaxes(
        gridcolor=DASHBOARD_COLORS["grid"],
        linecolor=DASHBOARD_COLORS["grid"],
        zeroline=False,
        tickfont={"color": DASHBOARD_COLORS["muted"]},
        title_font={"color": DASHBOARD_COLORS["muted"]},
        automargin=True,
    )
    return fig


def product_demand_sunburst(df: pd.DataFrame) -> go.Figure:
    title = "Product Demand Map"
    if df.empty:
        return empty_figure(title)
    grouped = (
        df.groupby(["category", "item_purchased"], as_index=False)
        .agg(
            purchases=("customer_id", "count"),
            total_sales=("purchase_amount", "sum"),
            avg_order=("purchase_amount", "mean"),
        )
        .sort_values(["category", "purchases"], ascending=[True, False])
    )
    top_items = grouped.groupby("category", group_keys=False).head(5)
    fig = px.sunburst(
        top_items,
        path=["category", "item_purchased"],
        values="purchases",
        color="total_sales",
        color_continuous_scale=["#7C3AED", "#54D6FF", "#D7FF3F"],
        custom_data=["total_sales", "avg_order"],
        labels={
            "category": "Category",
            "item_purchased": "Item purchased",
            "purchases": "Purchases",
            "total_sales": "Total spending (USD)",
        },
    )
    fig.update_traces(
        branchvalues="total",
        insidetextorientation="radial",
        marker={"line": {"color": "rgba(5,5,6,0.72)", "width": 1.5}},
        textinfo="label+percent parent",
        hovertemplate="<b>%{label}</b><br>Purchases: %{value:,}<br>Total: $%{customdata[0]:,.0f}<br>Average order: $%{customdata[1]:.2f}<extra></extra>",
    )
    styled = style_figure(fig, title)
    styled.update_layout(
        coloraxis_showscale=False,
        margin={"t": 58, "r": 18, "b": 18, "l": 18},
        uniformtext={"minsize": 10, "mode": "hide"},
    )
    return styled


def subscription_gauge(df: pd.DataFrame) -> go.Figure:
    title = "Subscription Rate Gauge"
    if df.empty:
        return empty_figure(title)
    counts = df["subscription_status"].value_counts()
    subscribed = int(counts.get("Yes", 0))
    not_subscribed = int(counts.get("No", 0))
    subscription_rate = subscribed / len(df) * 100
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=subscription_rate,
            number={"suffix": "%", "font": {"size": 44, "color": DASHBOARD_COLORS["text"]}},
            domain={"x": [0.04, 0.96], "y": [0.18, 0.94]},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": DASHBOARD_COLORS["grid"],
                    "tickfont": {"color": DASHBOARD_COLORS["muted"], "size": 11},
                },
                "bar": {"color": DASHBOARD_COLORS["primary"], "thickness": 0.28},
                "bgcolor": "rgba(255,255,255,0.04)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 35], "color": "rgba(124,58,237,0.22)"},
                    {"range": [35, 65], "color": "rgba(45,212,191,0.18)"},
                    {"range": [65, 100], "color": "rgba(215,255,63,0.16)"},
                ],
                "threshold": {
                    "line": {"color": DASHBOARD_COLORS["warning"], "width": 3},
                    "thickness": 0.76,
                    "value": 50,
                },
            },
        )
    )
    styled = style_figure(fig, title)
    styled.update_layout(
        margin={"t": 58, "r": 24, "b": 50, "l": 24},
        annotations=[
            {
                "text": f"<b>{subscribed:,}</b><br>Subscribed",
                "x": 0.24,
                "y": 0.05,
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"color": DASHBOARD_COLORS["success"], "size": 13},
            },
            {
                "text": f"<b>{not_subscribed:,}</b><br>Not subscribed",
                "x": 0.76,
                "y": 0.05,
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"color": DASHBOARD_COLORS["muted"], "size": 13},
            },
        ],
    )
    return styled


def category_revenue_treemap(df: pd.DataFrame) -> go.Figure:
    title = "Category Revenue Share"
    if df.empty:
        return empty_figure(title)
    grouped = (
        df.groupby("category", as_index=False)
        .agg(total_sales=("purchase_amount", "sum"), avg_order=("purchase_amount", "mean"), purchases=("customer_id", "count"))
        .sort_values("total_sales", ascending=False)
    )
    fig = px.treemap(
        grouped,
        path=["category"],
        values="total_sales",
        color="avg_order",
        color_continuous_scale=["#7C3AED", "#54D6FF", "#D7FF3F"],
        custom_data=["purchases", "avg_order"],
        labels={"total_sales": "Total spending (USD)", "avg_order": "Average order"},
    )
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>$%{value:,.0f}",
        hovertemplate="<b>%{label}</b><br>Total: $%{value:,.0f}<br>Average order: $%{customdata[1]:.2f}<br>Purchases: %{customdata[0]:,.0f}<extra></extra>",
        marker={"line": {"color": "rgba(5,5,6,0.7)", "width": 2}},
    )
    styled = style_figure(fig, title)
    styled.update_layout(margin={"t": 58, "r": 20, "b": 20, "l": 20}, coloraxis_showscale=False)
    return styled


def seasonal_revenue_pulse(df: pd.DataFrame) -> go.Figure:
    title = "Seasonal Revenue Pulse"
    if df.empty:
        return empty_figure(title)
    grouped = (
        df.groupby("season", as_index=False)
        .agg(total_sales=("purchase_amount", "sum"), purchases=("customer_id", "count"), avg_order=("purchase_amount", "mean"))
    )
    grouped["season"] = pd.Categorical(grouped["season"], categories=SEASON_ORDER, ordered=True)
    grouped = grouped.sort_values("season")
    fig = go.Figure(
        go.Barpolar(
            r=grouped["total_sales"].tolist(),
            theta=grouped["season"].astype(str).tolist(),
            text=[money(value) for value in grouped["total_sales"]],
            customdata=grouped[["purchases", "avg_order"]].to_numpy(),
            marker={
                "color": grouped["total_sales"].tolist(),
                "colorscale": [[0, "#7C3AED"], [0.5, "#2DD4BF"], [1, "#D7FF3F"]],
                "line": {"color": "rgba(250,250,250,0.28)", "width": 1},
                "showscale": False,
            },
            opacity=0.9,
            hovertemplate="<b>%{theta}</b><br>Total: %{text}<br>Purchases: %{customdata[0]:,.0f}<br>Average order: $%{customdata[1]:.2f}<extra></extra>",
        )
    )
    styled = style_figure(fig, title)
    styled.update_layout(
        showlegend=False,
        margin={"t": 58, "r": 30, "b": 34, "l": 30},
        polar={
            "bgcolor": "rgba(0,0,0,0)",
            "radialaxis": {
                "showticklabels": False,
                "ticks": "",
                "gridcolor": "rgba(250,250,250,0.08)",
                "linecolor": "rgba(250,250,250,0.08)",
            },
            "angularaxis": {
                "direction": "clockwise",
                "gridcolor": "rgba(250,250,250,0.10)",
                "linecolor": "rgba(250,250,250,0.10)",
                "tickfont": {"color": DASHBOARD_COLORS["text"], "size": 13},
            },
        },
    )
    return styled


def customer_value_matrix(df: pd.DataFrame) -> go.Figure:
    title = "Customer Value Matrix"
    if df.empty:
        return empty_figure(title)
    grouped = (
        df.groupby(["age_group", "gender"], observed=False)
        .agg(
            purchases=("customer_id", "count"),
            avg_order=("purchase_amount", "mean"),
            repeat_depth=("previous_purchases", "mean"),
            avg_rating=("review_rating", "mean"),
        )
        .reset_index()
    )
    grouped = grouped[grouped["purchases"] > 0].copy()
    grouped["age_group"] = grouped["age_group"].astype(str)
    average_order = float(df["purchase_amount"].mean())
    fig = px.scatter(
        grouped,
        x="age_group",
        y="avg_order",
        color="gender",
        size="purchases",
        size_max=42,
        text="purchases",
        custom_data=["purchases", "repeat_depth", "avg_rating"],
        color_discrete_sequence=COLORWAY,
        category_orders={"age_group": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]},
        labels={
            "age_group": "Age group",
            "avg_order": "Average order (USD)",
            "gender": "Gender",
            "purchases": "Purchases",
        },
    )
    fig.update_traces(
        texttemplate="%{text}",
        textposition="middle center",
        textfont={"color": "#050506", "size": 11},
        marker={"line": {"color": "rgba(255,255,255,0.34)", "width": 1}},
        hovertemplate="<b>%{x} | %{legendgroup}</b><br>Average order: $%{y:.2f}<br>Purchases: %{customdata[0]:,}<br>Repeat depth: %{customdata[1]:.1f}<br>Avg. rating: %{customdata[2]:.2f}<extra></extra>",
    )
    fig.add_hline(
        y=average_order,
        line={"color": "rgba(215,255,63,0.45)", "width": 1.5, "dash": "dot"},
        annotation_text=f"Overall avg. {money(average_order)}",
        annotation_font={"color": DASHBOARD_COLORS["primary"], "size": 11},
        annotation_position="top left",
    )
    styled = style_figure(fig, title)
    styled.update_layout(
        legend={"orientation": "h", "y": 1.08, "x": 1, "xanchor": "right", "font": {"color": DASHBOARD_COLORS["muted"]}},
        margin={"t": 58, "r": 24, "b": 54, "l": 58},
    )
    styled.update_yaxes(tickprefix="$")
    return styled


def category_season_heatmap(df: pd.DataFrame) -> go.Figure:
    title = "Category Performance by Season"
    if df.empty:
        return empty_figure(title)
    grouped = df.groupby(["category", "season"], as_index=False)["purchase_amount"].sum()
    totals = grouped.groupby("category")["purchase_amount"].sum().sort_values(ascending=False)
    pivot = (
        grouped.pivot(index="category", columns="season", values="purchase_amount")
        .reindex(index=totals.index, columns=[season for season in SEASON_ORDER if season in grouped["season"].unique()])
        .fillna(0)
    )
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale=[[0, "#22143F"], [0.5, "#2DD4BF"], [1, "#D7FF3F"]],
            colorbar={"title": "Sales"},
            hovertemplate="<b>%{y}</b><br>Season: %{x}<br>Total: $%{z:,.0f}<extra></extra>",
        )
    )
    fig.update_xaxes(title_text="Season")
    fig.update_yaxes(title_text="Category")
    return style_figure(fig, title)


def kpi_values(df: pd.DataFrame, full_df: pd.DataFrame) -> list[dict[str, str]]:
    if df.empty:
        return [
            {"label": "Total sales", "value": "$0", "note": "No matching records"},
            {"label": "Purchases", "value": "0", "note": "0.0% of dataset"},
            {"label": "Average order", "value": "$0", "note": "No matching orders"},
            {"label": "Avg. rating", "value": "-", "note": "No matching reviews"},
            {"label": "Subscription rate", "value": "0.0%", "note": "No matching customers"},
            {"label": "Repeat depth", "value": "0.0", "note": "Previous purchases avg."},
        ]
    share = len(df) / len(full_df) * 100
    subscription_rate = df["subscription_status"].eq("Yes").mean() * 100
    return [
        {"label": "Total sales", "value": money(df["purchase_amount"].sum()), "note": "Filtered revenue"},
        {"label": "Purchases", "value": number(len(df)), "note": f"{share:.1f}% of full data"},
        {"label": "Average order", "value": money(df["purchase_amount"].mean()), "note": "Mean purchase amount"},
        {"label": "Avg. rating", "value": f"{df['review_rating'].mean():.2f}", "note": "Customer review score"},
        {"label": "Subscription rate", "value": pct(subscription_rate), "note": "Subscription status = Yes"},
        {"label": "Repeat depth", "value": f"{df['previous_purchases'].mean():.1f}", "note": "Previous purchases avg."},
    ]


def takeaway_value(df: pd.DataFrame, view: str) -> dict[str, str]:
    if df.empty:
        return {
            "title": "No matching purchases",
            "copy": "Reset filters or widen the selected ranges to bring records back into the dashboard.",
        }
    category = df.groupby("category")["purchase_amount"].sum().sort_values(ascending=False)
    season = df.groupby("season")["purchase_amount"].sum().sort_values(ascending=False)
    subscription_rate = df["subscription_status"].eq("Yes").mean() * 100
    item = df["item_purchased"].value_counts()
    age_group = df.groupby("age_group", observed=False)["purchase_amount"].mean().sort_values(ascending=False)

    view_takeaways = {
        "Overview": {
            "title": f"{category.index[0]} leads revenue, with {season.index[0]} as the strongest season.",
            "copy": f"Filtered sales total {money(df['purchase_amount'].sum())} across {number(len(df))} purchases, with an average order of {money(df['purchase_amount'].mean())}.",
        },
        "Customer Insights": {
            "title": f"{pct(subscription_rate)} of selected customers are subscribed.",
            "copy": f"The average review rating is {df['review_rating'].mean():.2f}, and {age_group.index[0]} has the highest average order value by age group.",
        },
        "Product & Sales": {
            "title": f"{item.index[0]} is the top purchased item.",
            "copy": f"{category.index[0]} drives the most revenue, while the heatmap shows how category demand changes by season.",
        },
        "Data Explorer": {
            "title": f"{number(len(df))} filtered records are ready to inspect or export.",
            "copy": f"The current selection represents {money(df['purchase_amount'].sum())} in spending with an average order of {money(df['purchase_amount'].mean())}.",
        },
    }
    return view_takeaways.get(view, view_takeaways["Overview"])


def render_landing(df: pd.DataFrame) -> None:
    total_sales = money(df["purchase_amount"].sum())
    avg_order = money(df["purchase_amount"].mean())
    avg_rating = f"{df['review_rating'].mean():.2f}"
    categories = df["category"].nunique()
    locations = df["location"].nunique()
    st.markdown(
        f"""
        <div class="landing-wrap">
          <div class="hero-card">
            <p class="hero-label">Shopping Trends Intelligence Dashboard</p>
            <h1 class="hero-title">Shopping Trends Intelligence</h1>
            <p class="hero-copy">
              A focused retail analytics dashboard for understanding revenue drivers, customer behavior,
              and seasonal product demand across {len(df):,} shopping records.
            </p>
            <div class="hero-stat-grid">
              <div class="hero-stat"><span>Total sales</span><strong>{total_sales}</strong></div>
              <div class="hero-stat"><span>Purchases</span><strong>{len(df):,}</strong></div>
              <div class="hero-stat"><span>Average order</span><strong>{avg_order}</strong></div>
              <div class="hero-stat"><span>Review score</span><strong>{avg_rating}</strong></div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, center, right = st.columns([1.7, 1, 1.7])
    with center:
        if st.button("Explore Dashboard", key="explore_dashboard"):
            st.session_state.entered_dashboard = True
            st.rerun()
    st.markdown(
        f"""
        <div class="about-card">
          <h2>About Dataset</h2>
          <p>
            This dashboard uses <strong>{len(df):,} shopping records</strong> across <strong>{categories}</strong> product
            categories and <strong>{locations}</strong> locations. Global filters let users narrow customer, product,
            market, and transaction fields while the main views stay focused on the strongest visual signals.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(df: pd.DataFrame, full_df: pd.DataFrame) -> None:
    cards = "".join(
        "<div class='kpi-card'>"
        f"<span>{escape(item['label'])}</span>"
        f"<strong>{escape(item['value'])}</strong>"
        f"<em>{escape(item['note'])}</em>"
        "</div>"
        for item in kpi_values(df, full_df)
    )
    st.markdown(f"<div class='kpi-grid'>{cards}</div>", unsafe_allow_html=True)


def render_takeaway(df: pd.DataFrame, view: str) -> None:
    takeaway = takeaway_value(df, view)
    st.markdown(
        "<div class='takeaway-card'>"
        "<span>Key takeaway</span>"
        f"<strong>{escape(takeaway['title'])}</strong>"
        f"<p>{escape(takeaway['copy'])}</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def section(title: str, copy: str) -> None:
    st.markdown(f"<h2 class='section-title'>{title}</h2><p class='section-copy'>{copy}</p>", unsafe_allow_html=True)


def render_active_filters(full_df: pd.DataFrame) -> None:
    labels = active_filter_labels(full_df)
    if not labels:
        labels = ["No filters active"]
    chips = "".join(f"<span class='filter-chip'>{escape(label)}</span>" for label in labels)
    st.markdown(f"<div class='filter-summary'>{chips}</div>", unsafe_allow_html=True)


def render_data_table(df: pd.DataFrame) -> None:
    display_columns = [
        "customer_id",
        "age",
        "gender",
        "item_purchased",
        "category",
        "purchase_amount",
        "location",
        "season",
        "review_rating",
        "subscription_status",
        "payment_method",
        "shipping_type",
        "discount_applied",
        "promo_code_used",
        "previous_purchases",
        "frequency_of_purchases",
    ]
    export_df = df[display_columns].copy()
    csv = export_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered CSV",
        data=csv,
        file_name="filtered_shopping_trends.csv",
        mime="text/csv",
        width="stretch",
    )
    table_df = export_df.copy()
    table_df["purchase_amount"] = table_df["purchase_amount"].map(lambda value: f"${value:,.0f}")
    st.dataframe(table_df, width="stretch", height=520, hide_index=True)


def chart_caption(text: str) -> None:
    st.markdown(f"<p class='chart-caption'>{escape(text)}</p>", unsafe_allow_html=True)


def render_chart(fig: go.Figure, caption: str) -> None:
    st.plotly_chart(fig, width="stretch")
    chart_caption(caption)


def render_selected_view(df: pd.DataFrame, view: str) -> None:
    if view == "Overview":
        section("Overview", "The fastest read on what drives revenue and when spending changes.")
        c1, c2 = st.columns([1.2, 1])
        with c1:
            render_chart(
                category_revenue_treemap(df),
                "Shows which categories contribute the largest share of filtered revenue. Larger blocks mean stronger sales impact.",
            )
        with c2:
            render_chart(
                seasonal_revenue_pulse(df),
                "Shows each season as a revenue pulse. Longer, brighter segments mark stronger shopping periods.",
            )
    elif view == "Customer Insights":
        section("Customer Insights", "A focused view of customer membership and spending behavior.")
        c1, c2 = st.columns(2)
        with c1:
            render_chart(
                subscription_gauge(df),
                "Shows the share of selected customers who are subscribed, with counts for subscribed and non-subscribed customers.",
            )
        with c2:
            render_chart(
                customer_value_matrix(df),
                "Compares age and gender groups by average order value. Larger bubbles represent more purchases.",
            )
    elif view == "Product & Sales":
        section("Product & Sales", "The clearest product demand signals without repeating the full dataset.")
        c1, c2 = st.columns(2)
        with c1:
            render_chart(
                product_demand_sunburst(df),
                "Maps product demand from category to item. Larger slices mean more purchases within the current filters.",
            )
        with c2:
            render_chart(
                category_season_heatmap(df),
                "Highlights category revenue by season, helping show where demand changes across the year.",
            )
    else:
        section("Data Explorer", "Filtered records for checking details behind the charts.")
        render_data_table(df)


def render_dashboard(df: pd.DataFrame, full_df: pd.DataFrame) -> None:
    sidebar_filters(full_df)
    summary_col, view_col, back_col = st.columns([2.1, 1, 0.85])
    with summary_col:
        render_active_filters(full_df)
    with view_col:
        st.markdown("<p class='field-label'>Dashboard view</p>", unsafe_allow_html=True)
        if st.session_state.dashboard_view not in DASHBOARD_VIEWS:
            st.session_state.dashboard_view = DASHBOARD_VIEWS[0]
        view = st.selectbox("Dashboard view", DASHBOARD_VIEWS, key="dashboard_view", label_visibility="collapsed")
    with back_col:
        st.markdown("<p class='field-label'>Navigation</p>", unsafe_allow_html=True)
        if st.button("Back to Landing", key="back_to_landing"):
            st.session_state.entered_dashboard = False
            st.rerun()

    if df.empty:
        st.markdown("<div class='no-data'>No purchases match the current filters. Use Reset filters or widen the ranges.</div>", unsafe_allow_html=True)

    render_kpis(df, full_df)
    render_takeaway(df, view)
    render_selected_view(df, view)


def main() -> None:
    inject_css()
    df = load_data()
    initialize_state(df)
    if not st.session_state.entered_dashboard:
        render_landing(df)
        return
    filtered = apply_filters(df)
    render_dashboard(filtered, df)


if __name__ == "__main__":
    main()
