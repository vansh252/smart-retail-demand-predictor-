"""
Streamlit Dashboard for Smart Retail Demand Prediction System
Professional UI with Excel/CSV upload, auto-cleaning, and rich analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
import io
import json
from datetime import datetime

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))

from data_validator import DataValidator

# Page configuration
st.set_page_config(
    page_title="Smart Retail Demand Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_URL = "http://127.0.0.1:5000"

# ── Color Palette ──────────────────────────────────────────────
COLORS = {
    "primary": "#6366F1",       # Indigo
    "secondary": "#8B5CF6",     # Purple
    "accent": "#EC4899",        # Pink
    "success": "#10B981",       # Emerald
    "warning": "#F59E0B",       # Amber
    "danger": "#EF4444",        # Red
    "info": "#3B82F6",          # Blue
    "dark": "#1E293B",          # Slate 800
    "light": "#F8FAFC",         # Slate 50
}

CHART_PALETTE = [
    "#6366F1", "#EC4899", "#10B981", "#F59E0B",
    "#3B82F6", "#8B5CF6", "#14B8A6", "#F97316",
]

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        padding: 10px 0 0 0;
        letter-spacing: -0.5px;
    }
    .sub-header {
        text-align: center;
        color: #64748B;
        font-size: 16px;
        margin-bottom: 20px;
        font-weight: 400;
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99,102,241,0.12);
    }
    .metric-value {
        font-size: 32px;
        font-weight: 800;
        color: #1E293B;
        margin: 8px 0 4px 0;
    }
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #94A3B8;
    }
    .metric-delta {
        font-size: 13px;
        font-weight: 600;
        color: #10B981;
    }
    .upload-zone {
        border: 2px dashed #CBD5E1;
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
        transition: border-color 0.3s;
    }
    .upload-zone:hover { border-color: #6366F1; }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .badge-success { background: #ECFDF5; color: #059669; }
    .badge-warning { background: #FFFBEB; color: #D97706; }
    .badge-error { background: #FEF2F2; color: #DC2626; }
    .badge-info { background: #EFF6FF; color: #2563EB; }
    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: #1E293B;
        margin: 24px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #E2E8F0;
    }
    .cleaning-step {
        background: #F8FAFC;
        border-left: 4px solid #6366F1;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        font-size: 14px;
    }
    .prediction-card {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 60%, #EC4899 100%);
        padding: 48px 32px;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(99,102,241,0.3);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
    }
    div[data-testid="stSidebar"] .stMarkdown p,
    div[data-testid="stSidebar"] .stMarkdown li,
    div[data-testid="stSidebar"] label {
        color: #CBD5E1 !important;
    }
    div[data-testid="stSidebar"] h1,
    div[data-testid="stSidebar"] h2,
    div[data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Chart Template ─────────────────────────────────────────────
CHART_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", size=13, color="#334155"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=40, r=20, t=50, b=40),
    title_font=dict(size=16, color="#1E293B", family="Inter, sans-serif"),
    legend=dict(
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#E2E8F0",
        borderwidth=1,
        font=dict(size=12),
    ),
    xaxis=dict(gridcolor="#F1F5F9", linecolor="#E2E8F0", zerolinecolor="#E2E8F0"),
    yaxis=dict(gridcolor="#F1F5F9", linecolor="#E2E8F0", zerolinecolor="#E2E8F0"),
    hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Inter, sans-serif",
        bordercolor="#E2E8F0",
    ),
)


def styled_metric(label, value, icon="", delta=None, color="#6366F1"):
    """Render a styled metric card"""
    delta_html = ""
    if delta is not None:
        d_color = "#10B981" if delta >= 0 else "#EF4444"
        d_arrow = "▲" if delta >= 0 else "▼"
        delta_html = f'<div style="color:{d_color};font-size:13px;font-weight:600;">{d_arrow} {abs(delta):.1f}%</div>'
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size:28px;margin-bottom:4px;">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color};">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


# ── Data Loading Helpers ───────────────────────────────────────

# ── Column Alias Mapping ───────────────────────────────────────
# Maps common column name variations to our standard names
COLUMN_ALIASES = {
    "product_id": [
        "product_id", "productid", "product id", "prod_id", "prodid",
        "item_id", "itemid", "item id", "sku", "sku_id", "product_code",
        "product code", "prod_code", "id", "product", "item", "item_code",
    ],
    "sale_date": [
        "sale_date", "saledate", "sale date", "date", "order_date",
        "orderdate", "order date", "transaction_date", "trans_date",
        "purchase_date", "sold_date", "invoice_date", "billing_date",
        "created_at", "timestamp", "sale_dt", "order_dt",
    ],
    "region": [
        "region", "area", "zone", "location", "territory", "market",
        "sales_region", "sales_area", "geo", "geography", "state",
        "city", "branch", "store_location", "district",
    ],
    "category": [
        "category", "product_category", "productcategory", "product category",
        "cat", "item_category", "item category", "type", "product_type",
        "product type", "dept", "department", "group", "product_group",
        "segment", "class", "classification", "subcategory", "sub_category",
    ],
    "quantity_sold": [
        "quantity_sold", "quantitysold", "quantity sold", "qty_sold",
        "qty", "quantity", "units_sold", "units", "unit_sold", "sales_qty",
        "sold_quantity", "amount_sold", "num_sold", "count", "volume",
        "sales_volume", "demand", "order_qty", "order_quantity",
    ],
    "price": [
        "price", "unit_price", "unitprice", "unit price", "selling_price",
        "sell_price", "sale_price", "item_price", "product_price",
        "cost", "amount", "rate", "mrp", "retail_price", "list_price",
        "sp", "unit_cost", "value",
    ],
    "discount": [
        "discount", "disc", "discount_pct", "discount_percent",
        "discount_percentage", "disc_pct", "disc_percent", "offer",
        "discount_%", "rebate", "markdown", "promo", "promo_discount",
        "discount_rate", "off", "pct_off",
    ],
}


def _match_columns(df_columns):
    """Match DataFrame columns to standard names using alias mapping.
    Returns {original_col: standard_name} for matched columns,
    and a set of unmatched required columns."""
    mapping = {}          # original_col -> standard_name
    matched_std = set()   # which standard names have been matched

    # First pass: normalise and try exact alias match
    for orig_col in df_columns:
        clean = orig_col.strip().lower().replace(" ", "_").replace("-", "_")
        clean_no_underscore = clean.replace("_", "")
        for std_name, aliases in COLUMN_ALIASES.items():
            if std_name in matched_std:
                continue
            for alias in aliases:
                alias_clean = alias.strip().lower().replace(" ", "_").replace("-", "_")
                alias_no_underscore = alias_clean.replace("_", "")
                if clean == alias_clean or clean_no_underscore == alias_no_underscore:
                    mapping[orig_col] = std_name
                    matched_std.add(std_name)
                    break
            if orig_col in mapping:
                break

    # Second pass: substring/contains match for remaining
    for orig_col in df_columns:
        if orig_col in mapping:
            continue
        clean = orig_col.strip().lower()
        for std_name, aliases in COLUMN_ALIASES.items():
            if std_name in matched_std:
                continue
            for alias in aliases:
                if alias in clean or clean in alias:
                    mapping[orig_col] = std_name
                    matched_std.add(std_name)
                    break
            if orig_col in mapping:
                break

    required = set(COLUMN_ALIASES.keys())
    missing = required - matched_std
    return mapping, missing


def detect_data_format(df):
    """Detect the format/schema of uploaded data and report issues"""
    report = {"columns_found": list(df.columns), "issues": [], "format": "unknown", "usable": False}

    col_map, missing = _match_columns(df.columns)
    report["col_map"] = col_map

    if not missing:
        report["format"] = "retail_sales"
        report["usable"] = True
        # Show what was mapped
        renamed = {k: v for k, v in col_map.items() if k.strip().lower().replace(" ", "_") != v}
        if renamed:
            report["mapped_cols"] = renamed
    else:
        report["issues"].append(
            f"Missing required columns: {', '.join(missing)}. "
            f"Your columns: {', '.join(df.columns.tolist())}. "
            f"We tried to match automatically but couldn't find: {', '.join(missing)}"
        )

    # Check data types
    for col in df.columns:
        if df[col].isnull().all():
            report["issues"].append(f"Column '{col}' is entirely empty")
    if df.empty:
        report["issues"].append("The uploaded file contains no data rows")

    report["rows"] = len(df)
    report["col_count"] = len(df.columns)
    return report


def auto_clean_dataframe(df):
    """Fully automatic data cleaning pipeline that mirrors DataValidator"""
    log = []

    # 1. Smart column name mapping using aliases
    col_map, missing = _match_columns(df.columns)
    if col_map:
        df = df.rename(columns=col_map)
        renamed = {k: v for k, v in col_map.items() if k != v}
        if renamed:
            log.append(f"Mapped {len(renamed)} columns: " + ", ".join(f"'{k}' → '{v}'" for k, v in renamed.items()))
        else:
            log.append(f"All {len(col_map)} column names recognised")
    if missing:
        log.append(f"Note: Could not find columns for: {', '.join(missing)}")

    original_len = len(df)

    # 2. Remove completely empty rows
    df = df.dropna(how="all")
    dropped_empty = original_len - len(df)
    if dropped_empty:
        log.append(f"Removed {dropped_empty} completely empty rows")

    # 3. Handle dates
    if "sale_date" in df.columns:
        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
        bad_dates = df["sale_date"].isnull().sum()
        if bad_dates:
            df = df.dropna(subset=["sale_date"])
            log.append(f"Removed {bad_dates} rows with invalid dates")
        else:
            log.append("All dates parsed successfully")

    # 4. Numeric columns - coerce and fill
    for col in ["price", "discount", "quantity_sold"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            n_null = df[col].isnull().sum()
            if n_null:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                log.append(f"Filled {n_null} missing '{col}' values with median ({median_val:.2f})")

    # 5. Categorical columns - fill and standardise
    cat_map = {"category": ["Electronics", "Clothing", "Furniture"], "region": ["North", "South", "East", "West"]}
    for col, valid in cat_map.items():
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
            n_null = df[col].isin(["", "Nan", "None", "Na"]).sum()
            if n_null:
                mode_val = df.loc[~df[col].isin(["", "Nan", "None", "Na"]), col].mode()
                fill = mode_val.iloc[0] if len(mode_val) else valid[0]
                df.loc[df[col].isin(["", "Nan", "None", "Na"]), col] = fill
                log.append(f"Filled {n_null} missing '{col}' values with '{fill}'")

            # Correct close misspellings via mapping to closest valid value
            invalid_mask = ~df[col].isin(valid)
            invalid_count = invalid_mask.sum()
            if invalid_count:
                df.loc[invalid_mask, col] = valid[0]
                log.append(f"Corrected {invalid_count} invalid '{col}' values to '{valid[0]}'")

    # 6. Product ID
    if "product_id" in df.columns:
        df["product_id"] = df["product_id"].astype(str).str.strip()
        n_null = df["product_id"].isin(["", "nan", "None"]).sum()
        if n_null:
            df.loc[df["product_id"].isin(["", "nan", "None"]), "product_id"] = "UNKNOWN"
            log.append(f"Filled {n_null} missing product IDs with 'UNKNOWN'")

    # 7. Remove negatives
    for col in ["price", "quantity_sold"]:
        if col in df.columns:
            neg = (df[col] < 0).sum()
            if neg:
                df[col] = df[col].abs()
                log.append(f"Converted {neg} negative '{col}' values to positive")

    # 8. Clamp discount
    if "discount" in df.columns:
        over = (df["discount"] > 100).sum()
        if over:
            df.loc[df["discount"] > 100, "discount"] = 100.0
            log.append(f"Capped {over} discount values at 100%")
        under = (df["discount"] < 0).sum()
        if under:
            df.loc[df["discount"] < 0, "discount"] = 0.0
            log.append(f"Set {under} negative discount values to 0%")

    # 9. Remove duplicates
    dup = df.duplicated().sum()
    if dup:
        df = df.drop_duplicates()
        log.append(f"Removed {dup} duplicate rows")

    # 10. Remove zero quantity
    if "quantity_sold" in df.columns:
        zero = (df["quantity_sold"] == 0).sum()
        if zero:
            df = df[df["quantity_sold"] > 0]
            log.append(f"Removed {zero} rows with zero quantity sold")

    log.append(f"Final dataset: {len(df)} rows, {len(df.columns)} columns")
    return df.reset_index(drop=True), log


def load_file(uploaded_file):
    """Load CSV or Excel into a DataFrame"""
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif name.endswith((".xlsx", ".xls")):
        engine = "openpyxl" if name.endswith(".xlsx") else "xlrd"
        return pd.read_excel(uploaded_file, engine=engine)
    return None


def check_api_status():
    """Check if Flask API is running"""
    try:
        response = requests.get(f"{API_URL}/", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def make_prediction(price, discount, month, category, region, year=2024):
    """Call Flask API to make prediction"""
    try:
        payload = {
            "price": price, "discount": discount, "month": month,
            "category": category, "region": region, "year": year,
        }
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"API error: {e}")
        return None


# ── Header ─────────────────────────────────────────────────────

def show_header():
    st.markdown('<div class="main-header">Smart Retail Demand Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-powered demand forecasting &bull; Upload data &bull; Get insights instantly</div>', unsafe_allow_html=True)
    st.markdown("")


# ── Page: Upload & Process ─────────────────────────────────────

def show_upload_page():
    st.markdown('<div class="section-header">📁 Upload & Process Your Data</div>', unsafe_allow_html=True)

    # ── Step 1: Ask about data format ──────────────────────────
    st.markdown("#### Step 1 — What format is your data in?")
    col_fmt1, col_fmt2 = st.columns([2, 3])
    with col_fmt1:
        file_format = st.radio(
            "Select file type:",
            ["📊 Excel (.xlsx / .xls)", "📄 CSV (.csv)"],
            help="Choose the format of the file you want to upload",
        )
    with col_fmt2:
        st.info(
            "**Your data should contain info about:**\n"
            "Product ID, Sale Date, Region, Category, Quantity Sold, Price, Discount\n\n"
            "**Column names are flexible!** We auto-detect variations like:\n"
            "`Unit Price` → price, `Qty` → quantity_sold, `Product Category` → category, etc.\n\n"
            "If auto-detection fails, you can manually map columns."
        )

    st.markdown("---")

    # ── Step 2: Upload ─────────────────────────────────────────
    st.markdown("#### Step 2 — Upload your file")
    accepted = ["xlsx", "xls"] if "Excel" in file_format else ["csv"]
    uploaded_file = st.file_uploader(
        "Drag & drop or browse",
        type=["csv", "xlsx", "xls"],
        help="Accepted formats: CSV, XLSX, XLS",
    )

    if uploaded_file is None:
        # Show sample template
        st.markdown("---")
        st.markdown("#### Don't have data? Download a sample template")
        sample = pd.DataFrame({
            "product_id": ["P001", "P002", "P003", "P004", "P005"],
            "sale_date": ["2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19"],
            "region": ["North", "South", "East", "West", "North"],
            "category": ["Electronics", "Clothing", "Electronics", "Furniture", "Clothing"],
            "quantity_sold": [50, 120, 75, 30, 200],
            "price": [299.99, 49.99, 199.99, 599.99, 29.99],
            "discount": [10.0, 5.0, 15.0, 20.0, 0.0],
        })
        col_t1, col_t2 = st.columns([1, 1])
        with col_t1:
            csv_bytes = sample.to_csv(index=False).encode()
            st.download_button("⬇ Download CSV Template", csv_bytes, "sample_template.csv", "text/csv")
        with col_t2:
            buf = io.BytesIO()
            sample.to_excel(buf, index=False, engine="openpyxl")
            st.download_button("⬇ Download Excel Template", buf.getvalue(), "sample_template.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.dataframe(sample, use_container_width=True, height=220)
        return

    # ── Step 3: Load and detect format ─────────────────────────
    with st.spinner("Reading file..."):
        try:
            raw_df = load_file(uploaded_file)
        except Exception as e:
            st.error(f"Could not read file: {e}")
            return

    if raw_df is None or raw_df.empty:
        st.error("The file is empty or could not be parsed.")
        return

    st.markdown("---")
    st.markdown("#### Step 3 — Data Format Detection")
    report = detect_data_format(raw_df)

    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        styled_metric("Rows Found", f"{report['rows']:,}", "📋")
    with col_d2:
        styled_metric("Columns Found", str(report['col_count']), "📊")
    with col_d3:
        if report["usable"]:
            st.markdown('<span class="status-badge badge-success">✓ Format Recognised — Retail Sales Data</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge badge-error">✗ Format Issues Detected</span>', unsafe_allow_html=True)

    # Show auto-mapped columns
    if report.get("mapped_cols"):
        with st.expander("🔄 Columns automatically mapped", expanded=True):
            for orig, std in report["mapped_cols"].items():
                st.success(f"'{orig}' → **{std}**")

    if report["issues"]:
        with st.expander("⚠ Issues detected — click to view", expanded=True):
            for issue in report["issues"]:
                st.warning(issue)

    st.markdown("")
    with st.expander("👀 Preview raw uploaded data", expanded=False):
        st.dataframe(raw_df.head(50), use_container_width=True, height=300)

    # If auto-detection failed, offer manual column mapping
    if not report["usable"]:
        st.markdown("---")
        st.markdown("#### 🔧 Manual Column Mapping")
        st.info(
            "We couldn't auto-detect all required columns. "
            "Please map your columns below — select which of your columns corresponds to each required field."
        )

        col_map, missing = _match_columns(raw_df.columns)
        available_cols = ["-- Not in my data --"] + list(raw_df.columns)
        manual_map = {}
        required_names = list(COLUMN_ALIASES.keys())

        map_cols = st.columns(min(len(required_names), 4))
        for i, std_name in enumerate(required_names):
            with map_cols[i % len(map_cols)]:
                # Pre-select if already matched
                default_idx = 0
                for orig, mapped in col_map.items():
                    if mapped == std_name:
                        default_idx = available_cols.index(orig) if orig in available_cols else 0
                        break

                choice = st.selectbox(
                    f"**{std_name}**",
                    available_cols,
                    index=default_idx,
                    key=f"map_{std_name}",
                )
                if choice != "-- Not in my data --":
                    manual_map[choice] = std_name

        # Check if all required are mapped
        mapped_stds = set(manual_map.values())
        still_missing = set(required_names) - mapped_stds

        if still_missing:
            st.warning(f"Still unmapped: **{', '.join(still_missing)}**. Map all required columns to proceed.")
            return
        else:
            st.success("All required columns mapped! Click below to proceed.")
            # Update the report so the rest of the flow works
            report["col_map"] = manual_map
            report["usable"] = True
            report["issues"] = []

    # ── Step 4: Auto-clean ─────────────────────────────────────
    st.markdown("---")
    st.markdown("#### Step 4 — Automatic Data Cleaning")

    if st.button("🚀 Clean & Process Data", type="primary", use_container_width=True):
        with st.spinner("Running automated data pipeline..."):
            cleaned_df, cleaning_log = auto_clean_dataframe(raw_df.copy())

        # Show cleaning log
        st.markdown("##### Cleaning Pipeline Log")
        for i, entry in enumerate(cleaning_log, 1):
            icon = "✅" if "removed" not in entry.lower() and "corrected" not in entry.lower() else "🔧"
            st.markdown(f'<div class="cleaning-step">{icon} <strong>Step {i}:</strong> {entry}</div>', unsafe_allow_html=True)

        st.success(f"Data cleaned successfully! {len(cleaned_df)} records ready.")

        # Store in session state
        st.session_state["uploaded_data"] = cleaned_df
        st.session_state["data_source"] = "upload"

        # Save to disk
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(data_dir, f"uploaded_cleaned_{ts}.csv")
        cleaned_df.to_csv(save_path, index=False)
        st.info(f"Cleaned data saved to `data/uploaded_cleaned_{ts}.csv`")

        # Quick preview
        st.markdown("##### Cleaned Data Preview")
        st.dataframe(cleaned_df.head(20), use_container_width=True, height=300)

        # Quick stats
        st.markdown("##### Quick Statistics")
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            styled_metric("Total Records", f"{len(cleaned_df):,}", "📋", color="#6366F1")
        with col_s2:
            styled_metric("Total Units Sold", f"{cleaned_df['quantity_sold'].sum():,.0f}", "📦", color="#10B981")
        with col_s3:
            styled_metric("Avg Price", f"${cleaned_df['price'].mean():.2f}", "💰", color="#F59E0B")
        with col_s4:
            styled_metric("Categories", str(cleaned_df['category'].nunique()), "🏷", color="#EC4899")

        st.balloons()


# ── Page: Analytics ────────────────────────────────────────────

def show_sales_analytics(df):
    st.markdown('<div class="section-header">📈 Sales Analytics Dashboard</div>', unsafe_allow_html=True)

    if df is None or df.empty:
        st.warning("No sales data available. Please upload data first on the **📁 Upload Data** page, or load from CSV.")
        return

    df = df.copy()
    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
    df["month"] = df["sale_date"].dt.month
    df["year"] = df["sale_date"].dt.year
    df["month_name"] = df["sale_date"].dt.strftime("%b")
    df["quarter"] = df["sale_date"].dt.quarter
    df["day_of_week"] = df["sale_date"].dt.day_name()
    total_revenue = (df["price"] * df["quantity_sold"]).sum()

    # ── KPI Row ────────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        styled_metric("Total Records", f"{len(df):,}", "📋", color="#6366F1")
    with k2:
        styled_metric("Units Sold", f"{df['quantity_sold'].sum():,.0f}", "📦", color="#10B981")
    with k3:
        styled_metric("Revenue", f"${total_revenue:,.0f}", "💰", color="#F59E0B")
    with k4:
        styled_metric("Avg Price", f"${df['price'].mean():.2f}", "🏷", color="#3B82F6")
    with k5:
        styled_metric("Avg Discount", f"{df['discount'].mean():.1f}%", "🔖", color="#EC4899")

    st.markdown("")

    # ── Row 1: Category Breakdown + Region Donut ───────────────
    c1, c2 = st.columns(2)

    with c1:
        cat_df = df.groupby("category").agg(
            total_qty=("quantity_sold", "sum"),
            avg_price=("price", "mean"),
            total_revenue=("price", lambda x: (x * df.loc[x.index, "quantity_sold"]).sum()),
        ).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=cat_df["category"], y=cat_df["total_qty"],
            marker=dict(
                color=CHART_PALETTE[:len(cat_df)],
            ),
            text=cat_df["total_qty"].apply(lambda v: f"{v:,.0f}"),
            textposition="outside",
            textfont=dict(size=13, color="#334155", family="Inter"),
        ))
        fig.update_layout(
            **CHART_LAYOUT,
            title="Sales Volume by Category",
            yaxis_title="Quantity Sold",
            xaxis_title="",
            showlegend=False,
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        reg_df = df.groupby("region")["quantity_sold"].sum().reset_index()
        fig = go.Figure(go.Pie(
            labels=reg_df["region"], values=reg_df["quantity_sold"],
            hole=0.55,
            marker=dict(colors=CHART_PALETTE[:len(reg_df)]),
            textinfo="label+percent",
            textfont=dict(size=13, family="Inter"),
            hovertemplate="<b>%{label}</b><br>Qty: %{value:,.0f}<br>Share: %{percent}<extra></extra>",
        ))
        fig.update_layout(
            **{k: v for k, v in CHART_LAYOUT.items() if k not in ("xaxis", "yaxis")},
            title="Regional Sales Distribution",
            height=400,
            annotations=[dict(text=f"{reg_df['quantity_sold'].sum():,.0f}<br>units", x=0.5, y=0.5,
                              font_size=18, showarrow=False, font_color="#1E293B", font_family="Inter")],
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2: Sales Trend (Area) + Monthly Heatmap ────────────
    c3, c4 = st.columns(2)

    with c3:
        ts_df = df.groupby("sale_date")["quantity_sold"].sum().reset_index().sort_values("sale_date")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ts_df["sale_date"], y=ts_df["quantity_sold"],
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(99,102,241,0.08)",
            line=dict(color="#6366F1", width=2.5, shape="spline"),
            marker=dict(size=6, color="#6366F1", line=dict(width=2, color="white")),
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>Qty: %{y:,.0f}<extra></extra>",
        ))
        fig.update_layout(
            **CHART_LAYOUT,
            title="Sales Trend Over Time",
            yaxis_title="Quantity Sold",
            xaxis_title="",
            height=400,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        heat_df = df.groupby(["category", "region"])["quantity_sold"].sum().reset_index()
        pivot = heat_df.pivot(index="category", columns="region", values="quantity_sold").fillna(0)
        fig = go.Figure(go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale=[[0, "#EEF2FF"], [0.5, "#818CF8"], [1, "#4338CA"]],
            text=pivot.values.astype(int),
            texttemplate="%{text:,}",
            textfont=dict(size=14, family="Inter"),
            hovertemplate="<b>%{y} × %{x}</b><br>Qty: %{z:,.0f}<extra></extra>",
            colorbar=dict(title="Qty", tickfont=dict(size=11)),
        ))
        fig.update_layout(
            **{k: v for k, v in CHART_LAYOUT.items() if k not in ("xaxis", "yaxis")},
            title="Category × Region Heatmap",
            height=400,
            xaxis=dict(title="Region", tickfont=dict(size=12)),
            yaxis=dict(title="Category", tickfont=dict(size=12)),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 3: Price vs Qty Scatter + Discount Impact ──────────
    c5, c6 = st.columns(2)

    with c5:
        fig = px.scatter(
            df, x="price", y="quantity_sold",
            color="category", size="discount",
            color_discrete_sequence=CHART_PALETTE,
            hover_data={"price": ":.2f", "quantity_sold": True, "discount": ":.1f", "region": True},
        )
        fig.update_traces(
            marker=dict(opacity=0.8, line=dict(width=1, color="white")),
        )
        fig.update_layout(
            **CHART_LAYOUT,
            title="Price vs Quantity (bubble = discount %)",
            xaxis_title="Price ($)",
            yaxis_title="Quantity Sold",
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c6:
        # Discount bucket analysis
        df_copy = df.copy()
        df_copy["discount_bucket"] = pd.cut(
            df_copy["discount"], bins=[-0.1, 5, 10, 20, 100],
            labels=["0-5%", "5-10%", "10-20%", "20%+"],
        )
        disc_df = df_copy.groupby("discount_bucket", observed=False)["quantity_sold"].mean().reset_index()
        fig = go.Figure(go.Bar(
            x=disc_df["discount_bucket"].astype(str),
            y=disc_df["quantity_sold"],
            marker=dict(
                color=["#10B981", "#3B82F6", "#F59E0B", "#EF4444"],
            ),
            text=disc_df["quantity_sold"].apply(lambda v: f"{v:.0f}"),
            textposition="outside",
            textfont=dict(size=13, family="Inter"),
        ))
        fig.update_layout(
            **CHART_LAYOUT,
            title="Avg Quantity Sold by Discount Range",
            xaxis_title="Discount Range",
            yaxis_title="Avg Quantity",
            showlegend=False,
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 4: Top Products ────────────────────────────────────
    st.markdown('<div class="section-header">🏆 Top Performing Products</div>', unsafe_allow_html=True)
    top_n = st.slider("Show top N products", 3, 20, 10)
    top_df = df.groupby("product_id").agg(
        total_qty=("quantity_sold", "sum"),
        avg_price=("price", "mean"),
        orders=("product_id", "count"),
    ).reset_index().sort_values("total_qty", ascending=True).tail(top_n)

    fig = go.Figure(go.Bar(
        y=top_df["product_id"], x=top_df["total_qty"],
        orientation="h",
        marker=dict(
            color=top_df["total_qty"],
            colorscale=[[0, "#C7D2FE"], [1, "#4F46E5"]],
        ),
        text=top_df["total_qty"].apply(lambda v: f"  {v:,.0f} units"),
        textposition="outside",
        textfont=dict(size=12, family="Inter", color="#334155"),
        hovertemplate="<b>%{y}</b><br>Qty: %{x:,.0f}<br>Avg Price: $%{customdata:.2f}<extra></extra>",
        customdata=top_df["avg_price"],
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title=f"Top {top_n} Products by Quantity Sold",
        xaxis_title="Total Quantity Sold",
        yaxis_title="",
        height=max(300, top_n * 35),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Page: Prediction ───────────────────────────────────────────

def show_prediction_interface():
    st.markdown('<div class="section-header">🔮 Demand Prediction Engine</div>', unsafe_allow_html=True)

    api_status = check_api_status()
    if api_status:
        st.markdown('<span class="status-badge badge-success">● API Connected</span>', unsafe_allow_html=True)
    else:
        st.error("Backend API is not running. Please start it with `python backend/app.py`")
        return

    st.markdown("")

    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            price = st.number_input("Price ($)", 0.01, 10000.0, 299.99, 10.0)
            discount = st.number_input("Discount (%)", 0.0, 100.0, 10.0, 1.0)
        with col2:
            category = st.selectbox("Category", ["Electronics", "Clothing", "Furniture"])
            region = st.selectbox("Region", ["North", "South", "East", "West"])
        with col3:
            month = st.selectbox("Month", list(range(1, 13)),
                                 format_func=lambda x: datetime(2024, x, 1).strftime("%B"))
            year = st.number_input("Year", 2020, 2030, 2024)
        submitted = st.form_submit_button("🎯 Predict Demand", use_container_width=True, type="primary")

    if submitted:
        with st.spinner("Running prediction model..."):
            result = make_prediction(price, discount, month, category, region, year)

        if result and result.get("status") == "success":
            pred = result["predicted_demand"]

            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                st.markdown(f"""
                <div class="prediction-card">
                    <div style="font-size:18px;font-weight:600;opacity:0.9;">Predicted Demand</div>
                    <div style="font-size:72px;font-weight:800;margin:16px 0;">{pred:.0f}</div>
                    <div style="font-size:16px;opacity:0.85;">units / period</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("")

            # Input summary as a visual bar
            st.markdown("##### Prediction Inputs")
            inp_df = pd.DataFrame({
                "Parameter": ["💰 Price", "🔖 Discount", "📅 Month", "🏷 Category", "🌍 Region", "📆 Year"],
                "Value": [f"${price:.2f}", f"{discount}%", datetime(2024, month, 1).strftime("%B"),
                          category, region, str(year)],
            })
            st.table(inp_df)

            # Comparison chart — show predicted demand vs average by category
            if "uploaded_data" in st.session_state and st.session_state["uploaded_data"] is not None:
                hist_df = st.session_state["uploaded_data"]
                if "category" in hist_df.columns and "quantity_sold" in hist_df.columns:
                    cat_avg = hist_df.groupby("category")["quantity_sold"].mean()
                    compare_data = {"Category": [], "Quantity": [], "Type": []}
                    for cat in ["Electronics", "Clothing", "Furniture"]:
                        if cat in cat_avg.index:
                            compare_data["Category"].append(cat)
                            compare_data["Quantity"].append(cat_avg[cat])
                            compare_data["Type"].append("Historical Avg")
                    compare_data["Category"].append(category)
                    compare_data["Quantity"].append(pred)
                    compare_data["Type"].append("Your Prediction")

                    cmp_df = pd.DataFrame(compare_data)
                    fig = px.bar(cmp_df, x="Category", y="Quantity", color="Type", barmode="group",
                                 color_discrete_map={"Historical Avg": "#CBD5E1", "Your Prediction": "#6366F1"})
                    fig.update_layout(**CHART_LAYOUT, title="Your Prediction vs Historical Averages",
                                      height=350, showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Prediction failed. Please check inputs and try again.")


# ── Page: Data View ────────────────────────────────────────────

def show_data_table(df):
    st.markdown('<div class="section-header">📋 Data Explorer</div>', unsafe_allow_html=True)

    if df is None or df.empty:
        st.warning("No data loaded. Upload data on the **📁 Upload Data** page.")
        return

    df = df.copy()

    # Filters
    st.markdown("##### Filters")
    f1, f2, f3 = st.columns(3)
    with f1:
        cats = ["All"] + sorted(df["category"].unique().tolist()) if "category" in df.columns else ["All"]
        sel_cat = st.selectbox("Category", cats)
    with f2:
        regs = ["All"] + sorted(df["region"].unique().tolist()) if "region" in df.columns else ["All"]
        sel_reg = st.selectbox("Region", regs)
    with f3:
        prods = ["All"] + sorted(df["product_id"].unique().tolist()) if "product_id" in df.columns else ["All"]
        sel_prod = st.selectbox("Product", prods)

    filt = df.copy()
    if sel_cat != "All":
        filt = filt[filt["category"] == sel_cat]
    if sel_reg != "All":
        filt = filt[filt["region"] == sel_reg]
    if sel_prod != "All":
        filt = filt[filt["product_id"] == sel_prod]

    st.markdown(f"Showing **{len(filt):,}** of {len(df):,} records")
    st.dataframe(filt, use_container_width=True, height=450)

    c1, c2 = st.columns(2)
    with c1:
        csv_bytes = filt.to_csv(index=False).encode()
        st.download_button("⬇ Download CSV", csv_bytes, "filtered_data.csv", "text/csv", use_container_width=True)
    with c2:
        buf = io.BytesIO()
        filt.to_excel(buf, index=False, engine="openpyxl")
        st.download_button("⬇ Download Excel", buf.getvalue(), "filtered_data.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)


# ── Main ───────────────────────────────────────────────────────

def main():
    show_header()

    # ── Sidebar ────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        page = st.radio(
            "Go to:",
            ["📁 Upload Data", "📈 Analytics", "🔮 Prediction", "📋 Data Explorer"],
            label_visibility="collapsed",
        )
        st.markdown("---")

        # Quick data source info
        if "uploaded_data" in st.session_state and st.session_state["uploaded_data"] is not None:
            n = len(st.session_state["uploaded_data"])
            st.success(f"✓ {n:,} records loaded")
        else:
            st.warning("No data loaded yet")

        st.markdown("---")
        st.markdown(
            "**Smart Retail AI**\n\n"
            "Upload your sales data in **Excel** or **CSV** format. "
            "The system automatically detects issues, cleans the data, and generates insights.\n\n"
            "Built with Python, Scikit-learn, Flask & Streamlit"
        )

        # Load from existing CSV
        st.markdown("---")
        st.markdown("##### Load from saved file")
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        if os.path.exists(data_dir):
            csv_files = sorted([f for f in os.listdir(data_dir) if f.endswith(".csv")], reverse=True)
            if csv_files:
                sel_file = st.selectbox("Select CSV", csv_files, label_visibility="collapsed")
                if st.button("Load", use_container_width=True):
                    fpath = os.path.join(data_dir, sel_file)
                    st.session_state["uploaded_data"] = pd.read_csv(fpath)
                    st.session_state["data_source"] = "csv"
                    st.rerun()

    # ── Get data ───────────────────────────────────────────────
    df = st.session_state.get("uploaded_data", None)

    # ── Route pages ────────────────────────────────────────────
    if page == "📁 Upload Data":
        show_upload_page()
    elif page == "📈 Analytics":
        show_sales_analytics(df)
    elif page == "🔮 Prediction":
        show_prediction_interface()
    elif page == "📋 Data Explorer":
        show_data_table(df)


if __name__ == "__main__":
    main()
