import base64
import html
from io import BytesIO

import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px

from src.analysis import (
    DATA_PATH,
    load_data,
    clean_sales_data,
    get_kpis,
    get_top_products,
    get_top_products_by_quantity,
    get_category_summary,
    get_region_summary,
    build_business_insights,
    get_date_column,
    find_column,
    build_business_recommendations,
)


st.set_page_config(page_title="Business Sales Analytics Dashboard", layout="wide")

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], .main .block-container {
        background: linear-gradient(180deg, #edf5ff 0%, #f4f8fd 100%);
    }
    .stApp {
        background: linear-gradient(180deg, #edf5ff 0%, #f4f8fd 100%);
    }
    div.block-container {
        padding-top: 1.0rem;
        padding-left: 1.3rem;
        padding-right: 1.3rem;
        max-width: 100%;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1d35 0%, #173a61 100%);
        border: none;
        box-shadow: 3px 0 16px rgba(8, 16, 26, 0.18);
    }
    [data-testid="stSidebarContent"] {
        padding: 0.9rem 0.9rem 1.2rem 0.9rem;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stDateInput label,
    [data-testid="stSidebar"] .stSlider label {
        color: #ffffff;
        font-weight: 700;
    }
    [data-testid="stSidebar"] .stSelectbox div[role="button"],
    [data-testid="stSidebar"] .stDateInput > div, 
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 10px;
        color: white;
    }
    .top-header {
        background: linear-gradient(135deg, #081b32 0%, #0f2f57 45%, #1d5ca6 100%);
        padding: 1.25rem 1.6rem;
        margin: 0 0 1.2rem 0;
        border-radius: 18px;
        box-shadow: 0 14px 28px rgba(15, 40, 68, 0.18);
    }
    .header-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin: 0;
    }
    .header-subtitle {
        color: rgba(255,255,255,0.82);
        font-size: 0.82rem;
        margin-top: 0.35rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .sample-note {
        color: #ffffff;
        font-size: 0.72rem;
        font-weight: 600;
        margin-top: 0.55rem;
        opacity: 0.92;
    }
    .pill {
        display: inline-block;
        background: rgba(255,255,255,0.1);
        color: #edf5ff;
        border: 1px solid rgba(255,255,255,0.18);
        font-size: 0.72rem;
        border-radius: 999px;
        padding: 0.45rem 0.7rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .kpi-card {
        background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
        border: 1px solid #dfeaf7;
        border-radius: 16px;
        padding: 0.85rem 0.7rem;
        box-shadow: 0 8px 18px rgba(19, 38, 65, 0.08);
        min-height: 120px;
        min-width: 0;
    }
    .kpi-label {
        color: #263d56;
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .kpi-value {
        margin-top: 0.65rem;
        font-size: 1.1rem;
        font-weight: 800;
        color: #14375f;
        line-height: 1.2;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-variant-numeric: tabular-nums;
    }
    .kpi-change {
        margin-top: 0.4rem;
        font-size: 0.72rem;
        color: #315c49;
        font-weight: 700;
    }
    [data-testid="stAlert"] p {
        color: #17354f !important;
        font-weight: 600;
    }
    .chart-card {
        background: #ffffff;
        border: 1px solid #edf2fb;
        border-radius: 16px;
        padding: 0.8rem 0.9rem 0.35rem;
        box-shadow: 0 8px 16px rgba(15, 25, 40, 0.05);
        min-height: 330px;
    }
    .chart-title {
        font-size: 1rem;
        font-weight: 800;
        color: #102f50;
        margin: 0 0 0.7rem 0;
    }
    [data-testid="stPlotlyChart"] {
        background: #ffffff;
        border: 1px solid #dfe7f1;
        border-radius: 12px;
        padding: 0.3rem;
    }
    .insight-box {
        background: linear-gradient(135deg, #edf5ff 0%, #f8fbff 100%);
        border-left: 4px solid #2a6bb7;
        border-radius: 12px;
        padding: 0.85rem 0.95rem;
        color: #123d69;
        line-height: 1.75;
        min-height: 120px;
    }
    .summary-card {
        background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        border: 1px solid #dae7f8;
        height: 100%;
        box-shadow: 0 8px 16px rgba(16, 35, 52, 0.04);
    }
    .summary-label {
        color: #334a63;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .summary-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #183e68;
        margin-top: 0.4rem;
    }
    .stDataFrame, .stTable {
        border-radius: 12px;
    }
    .stButton > button {
        width: 100%;
        background: rgba(255,255,255,0.10);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_processed_data():
    df = load_data(DATA_PATH)
    df = clean_sales_data(df)
    return df


def format_currency(value, decimals=2):
    if pd.isna(value):
        return "N/A"
    amount = f"{value:.{decimals}f}"
    whole, decimal_part = amount.split(".") if decimals else (amount, "")
    sign = "-" if whole.startswith("-") else ""
    whole = whole.lstrip("-")
    if len(whole) > 3:
        last_three = whole[-3:]
        leading = whole[:-3]
        groups = []
        while leading:
            groups.insert(0, leading[-2:])
            leading = leading[:-2]
        whole = ",".join(groups + [last_three])
    suffix = f".{decimal_part}" if decimals else ""
    return f"{sign}₹{whole}{suffix}"


def apply_indian_currency_axis(figure, values):
    numeric_values = pd.Series(pd.to_numeric(values, errors="coerce")).dropna()
    maximum = float(numeric_values.max()) if not numeric_values.empty else 0
    maximum = maximum if maximum > 0 else 1
    tick_values = [maximum * step / 4 for step in range(5)]
    figure.update_yaxes(
        tickmode="array",
        tickvals=tick_values,
        ticktext=[format_currency(value, decimals=0) for value in tick_values],
        rangemode="tozero",
        tickfont=dict(color="#263d56"),
        title_font=dict(color="#263d56"),
        gridcolor="#e5ebf2",
    )


def format_number(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f}"


def build_year_options(df):
    if "Year" in df.columns and df["Year"].notna().any():
        years = sorted(df["Year"].dropna().unique().tolist())
        return [int(y) for y in years if y is not None]
    return [2025, 2026]


def report_chart_image(data, x_column, y_column, title, chart_type="line", value_label="Revenue", currency=True):
    figure, axis = plt.subplots(figsize=(8, 3.2))
    if not data.empty:
        if chart_type == "bar":
            axis.bar(data[x_column].astype(str), data[y_column], color="#2f6bb2")
            axis.tick_params(axis="x", rotation=25)
        else:
            axis.plot(data[x_column].astype(str), data[y_column], color="#2f6bb2", marker="o", linewidth=2)
            axis.tick_params(axis="x", rotation=25)
    axis.set_title(title, color="#102f50", fontweight="bold")
    axis.set_ylabel(value_label)
    if not data.empty:
        maximum = float(pd.to_numeric(data[y_column], errors="coerce").max())
        maximum = maximum if maximum > 0 else 1
        tick_values = [maximum * step / 4 for step in range(5)]
        axis.set_ylim(bottom=0)
        axis.set_yticks(tick_values)
        tick_labels = (
            [format_currency(value, decimals=0) for value in tick_values]
            if currency
            else [format_number(value) for value in tick_values]
        )
        axis.set_yticklabels(tick_labels)
    axis.grid(axis="y", alpha=0.2)
    figure.tight_layout()
    image_buffer = BytesIO()
    figure.savefig(image_buffer, format="png", dpi=140, facecolor="white")
    plt.close(figure)
    encoded_image = base64.b64encode(image_buffer.getvalue()).decode("ascii")
    return f'<img alt="{html.escape(title)}" src="data:image/png;base64,{encoded_image}">' 


def build_executive_report(data, selected_year, start_date, end_date, recommendations):
    revenue_col = find_column(data, "Revenue", "revenue")
    profit_col = find_column(data, "Profit", "profit", "Gross Profit", "gross_profit")
    date_col = get_date_column(data)
    category_col = find_column(data, "Category", "category")
    region_col = find_column(data, "Region", "region")
    product_col = find_column(data, "Product", "product")
    order_id_col = find_column(data, "Order_ID", "Order ID", "order_id")
    quantity_col = find_column(data, "Quantity", "quantity")

    revenue = float(data[revenue_col].sum()) if revenue_col else 0
    profit = float(data[profit_col].sum()) if profit_col else 0
    orders = int(data[order_id_col].nunique()) if order_id_col else 0
    units = int(data[quantity_col].sum()) if quantity_col else 0
    average_order_value = revenue / orders if orders else 0
    margin = profit / revenue * 100 if revenue else 0
    profit_estimated_col = find_column(data, "Profit_Estimated", "profit_estimated")
    profit_is_estimated = bool(data[profit_estimated_col].fillna(True).any()) if profit_estimated_col else False
    profit_label = "Illustrative Profit" if profit_is_estimated else "Total Profit"
    margin_label = "Illustrative Margin" if profit_is_estimated else "Profit Margin"
    profit_note = "28% is a sample assumption, not based on actual cost data." if profit_is_estimated else "Calculated from available cost data."
    report_interpretation = (
        "Collect actual product cost and returns data before using margin to guide investment."
        if profit_is_estimated
        else "Validate cost coverage and returns before reallocating investment based on the calculated margins."
    )

    monthly_chart = ""
    if date_col and revenue_col and not data.empty:
        monthly_data = (
            data.assign(_month=data[date_col].dt.to_period("M").astype(str))
            .groupby("_month", as_index=False)[revenue_col]
            .sum()
            .rename(columns={"_month": "Month", revenue_col: "Revenue"})
        )
        monthly_chart = report_chart_image(monthly_data, "Month", "Revenue", "Monthly revenue trend")

    category_chart = ""
    if category_col and revenue_col and not data.empty:
        category_data = (
            data.groupby(category_col, as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .rename(columns={category_col: "Category", revenue_col: "Revenue"})
        )
        category_chart = report_chart_image(category_data, "Category", "Revenue", "Revenue by category", "bar")

    regional_chart = ""
    if region_col and revenue_col and not data.empty:
        regional_data = (
            data.groupby(region_col, as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .rename(columns={region_col: "Region", revenue_col: "Revenue"})
        )
        regional_chart = report_chart_image(regional_data, "Region", "Revenue", "Revenue by region", "bar")

    top_selling_chart = ""
    if product_col and quantity_col and not data.empty:
        top_selling_data = (
            data.groupby(product_col, as_index=False)[quantity_col]
            .sum()
            .sort_values(quantity_col, ascending=False)
            .head(10)
            .rename(columns={product_col: "Product", quantity_col: "Units Sold"})
        )
        top_selling_chart = report_chart_image(
            top_selling_data,
            "Product",
            "Units Sold",
            "Top-selling products by units",
            "bar",
            value_label="Units sold",
            currency=False,
        )

    key_findings = []
    if product_col and quantity_col and not data.empty:
        units_by_product = data.groupby(product_col)[quantity_col].sum()
        key_findings.append(f"Top-selling product by units: {units_by_product.idxmax()} ({format_number(units_by_product.max())} units).")
    if category_col and revenue_col and not data.empty:
        revenue_by_category = data.groupby(category_col)[revenue_col].sum()
        category_share = revenue_by_category.max() / revenue_by_category.sum() * 100 if revenue_by_category.sum() else 0
        key_findings.append(f"Highest-value category by revenue: {revenue_by_category.idxmax()} ({category_share:.1f}% of selected revenue).")
    if region_col and revenue_col and not data.empty:
        revenue_by_region = data.groupby(region_col)[revenue_col].sum().sort_values(ascending=False)
        key_findings.append(f"Regional revenue leader: {revenue_by_region.index[0]}; lowest-revenue region: {revenue_by_region.index[-1]}.")
    if date_col and revenue_col and not data.empty:
        revenue_by_month = data.groupby(data[date_col].dt.to_period("M"))[revenue_col].sum()
        if not revenue_by_month.empty:
            key_findings.append(f"Peak revenue month: {revenue_by_month.idxmax()} ({format_currency(revenue_by_month.max())}).")

    recommendation_html = "".join(f"<li>{html.escape(item)}</li>" for item in recommendations)
    findings_html = "".join(f"<li>{html.escape(item)}</li>" for item in key_findings)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Sales Executive Report {selected_year}</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;background:#f1f5fa;color:#1b3048;margin:0;padding:32px}}
main{{max-width:1100px;margin:auto;background:#fff;padding:32px;border-radius:16px}}
h1{{color:#12375e;margin:0}}h2{{color:#12375e;margin-top:30px}}.sub{{color:#52677d;margin:8px 0 24px}}
.kpis{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}.kpi{{background:#f1f6fc;padding:16px;border-radius:10px}}
.label{{font-size:12px;text-transform:uppercase;color:#40566f;font-weight:700}}.value{{font-size:24px;font-weight:800;color:#173d65;margin-top:5px}}
img{{width:100%;height:auto;margin:8px 0 20px}}li{{margin:10px 0;line-height:1.5}}.note{{background:#fff6df;padding:14px;border-left:4px solid #d99b24;line-height:1.55}}
small{{color:#546a81;line-height:1.6}}@media(max-width:700px){{body{{padding:12px}}main{{padding:18px}}.kpis{{grid-template-columns:repeat(2,1fr)}}}}
</style></head><body><main>
<h1>Business Sales Executive Report</h1>
<div class="sub">Sample dataset (Jan–Dec 2026). Not actual sales data.<br>Year {selected_year} · {html.escape(str(start_date))} to {html.escape(str(end_date))} · Generated from selected dashboard filters</div>
<section class="kpis">
<div class="kpi"><div class="label">Total Revenue</div><div class="value">{format_currency(revenue)}</div></div>
<div class="kpi"><div class="label">{profit_label}</div><div class="value">{format_currency(profit)}</div><small>{profit_note}</small></div>
<div class="kpi"><div class="label">Unique Orders</div><div class="value">{format_number(orders)}</div></div>
<div class="kpi"><div class="label">Average Order Value</div><div class="value">{format_currency(average_order_value)}</div></div>
<div class="kpi"><div class="label">Units Sold</div><div class="value">{format_number(units)}</div></div>
<div class="kpi"><div class="label">{margin_label}</div><div class="value">{margin:.1f}%</div><small>{profit_note}</small></div>
</section>
<h2>Key Findings</h2><ul>{findings_html}</ul>
<h2>Performance Charts</h2>{monthly_chart}{category_chart}{regional_chart}{top_selling_chart}
<h2>Actionable Recommendations</h2><ul>{recommendation_html}</ul>
<h2>KPI Definitions</h2><small>Revenue = sum of sales revenue. Orders = distinct order IDs. Average order value = revenue divided by distinct orders. Units sold = sum of quantity. Profit margin = profit divided by revenue. {html.escape(profit_note)}</small>
<h2>Data Preparation</h2><small>Dates are parsed as calendar dates and invalid dates are excluded. Exact duplicate rows are removed; category labels are trimmed, standardized, and missing labels are retained as Unknown. Numeric fields are coerced, missing discounts default to zero, and missing revenue is calculated from quantity, unit price, and discount. Missing profit is calculated from available total/per-unit costs when present; otherwise it uses the illustrative 28% assumption.</small>
<p class="note"><strong>Interpretation:</strong> Use revenue and order volume for current category/region decisions. {html.escape(report_interpretation)}</p>
</main></body></html>"""


df = get_processed_data()

# Header
st.markdown(
    """
    <div class="top-header">
        <div style="display:flex; align-items:center; justify-content:space-between; gap: 1rem; flex-wrap: wrap;">
            <div>
                <div class="pill">Executive View</div>
                <div class="header-title" style="margin-top: 0.8rem;">Business Sales Analytics Dashboard</div>
                <div class="header-subtitle">Sales performance • revenue growth • regional outlook</div>
                <div class="sample-note">Sample dataset (Jan–Dec 2026). Not actual sales data.</div>
            </div>
            <div style="font-size: 2.4rem; opacity: 0.9;">📊</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

year_options = build_year_options(df)
default_year = max(year_options) if year_options else 2026
date_col = get_date_column(df)


def reset_filters():
    st.session_state["year_filter"] = default_year
    default_year_dates = df.loc[df["Year"] == default_year, date_col] if date_col and "Year" in df else pd.Series(dtype="datetime64[ns]")
    default_min = default_year_dates.min().date() if not default_year_dates.empty else pd.Timestamp(default_year, 1, 1).date()
    default_max = default_year_dates.max().date() if not default_year_dates.empty else pd.Timestamp(default_year, 12, 31).date()
    st.session_state[f"date_range_{default_year}"] = [default_min, default_max]
    st.session_state["region_filter"] = "All"
    st.session_state["category_filter"] = "All"
    st.session_state["product_filter"] = "All"
    st.session_state["top_n_filter"] = 10
    st.session_state["trend_period_filter"] = "Monthly"


with st.sidebar:
    st.markdown(
        """
        <div style="color: white; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; margin: 0.2rem 0 1rem 0; font-size: 0.8rem;">
            Filters
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_year = st.selectbox("Year", year_options, index=year_options.index(default_year), key="year_filter")

    if date_col and "Year" in df:
        dates_in_year = df.loc[df["Year"] == selected_year, date_col].dropna()
        year_min_date = dates_in_year.min().date() if not dates_in_year.empty else pd.Timestamp(selected_year, 1, 1).date()
        year_max_date = dates_in_year.max().date() if not dates_in_year.empty else pd.Timestamp(selected_year, 12, 31).date()
    else:
        year_min_date = pd.Timestamp(selected_year, 1, 1).date()
        year_max_date = pd.Timestamp(selected_year, 12, 31).date()
    date_selection = st.date_input(
        f"Date Range ({selected_year})",
        [year_min_date, year_max_date],
        min_value=year_min_date,
        max_value=year_max_date,
        key=f"date_range_{selected_year}",
    )

    if isinstance(date_selection, (list, tuple)) and len(date_selection) == 2:
        start_date, end_date = date_selection
    elif isinstance(date_selection, (list, tuple)) and len(date_selection) == 1:
        start_date = end_date = date_selection[0]
    else:
        start_date = end_date = date_selection

    region_col = find_column(df, "Region", "region")
    category_col = find_column(df, "Category", "category")
    product_col = find_column(df, "Product", "product")

    region_options = ["All"] + sorted(df[region_col].dropna().unique().tolist()) if region_col else ["All"]
    selected_region = st.selectbox("Region", region_options, key="region_filter")

    category_options = ["All"] + sorted(df[category_col].dropna().unique().tolist()) if category_col else ["All"]
    selected_category = st.selectbox("Category", category_options, key="category_filter")

    product_options = ["All"] + sorted(df[product_col].dropna().unique().tolist()) if product_col else ["All"]
    selected_product = st.selectbox("Product", product_options, key="product_filter")

    top_n = st.selectbox("Top N Products", [5, 10, 15, 20], index=1, key="top_n_filter")
    trend_period = st.selectbox("Trend Granularity", ["Monthly", "Quarterly", "Yearly"], index=0, key="trend_period_filter")

    st.button("Reset Filters", on_click=reset_filters)

# Filter dataset
if date_col:
    df_filtered = df[(df[date_col] >= pd.Timestamp(start_date)) & (df[date_col] <= pd.Timestamp(end_date))].copy()
else:
    df_filtered = df.copy()

if "Year" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["Year"] == selected_year].copy()

if selected_region != "All" and region_col:
    df_filtered = df_filtered[df_filtered[region_col] == selected_region].copy()

if selected_category != "All" and category_col:
    df_filtered = df_filtered[df_filtered[category_col] == selected_category].copy()

if selected_product != "All" and product_col:
    df_filtered = df_filtered[df_filtered[product_col] == selected_product].copy()

revenue_col = find_column(df_filtered, "Revenue", "revenue")
quantity_col = find_column(df_filtered, "Quantity", "quantity")
order_id_col = find_column(df_filtered, "Order_ID", "Order ID", "order_id")
profit_col = find_column(df_filtered, "Profit", "profit", "Gross Profit", "gross_profit")
profit_estimated_col = find_column(df_filtered, "Profit_Estimated", "profit_estimated")
profit_is_estimated = bool(df_filtered[profit_estimated_col].fillna(True).any()) if profit_estimated_col else False
profit_label = "Illustrative Profit" if profit_is_estimated else "Total Profit"
margin_label = "Illustrative Margin" if profit_is_estimated else "Profit Margin"
profit_note = "28% is a sample assumption, not based on actual cost data." if profit_is_estimated else "Calculated from available cost data."

kpis = get_kpis(df_filtered)

summary_cards = [
    ("Total Revenue", format_currency(kpis.get("Total Revenue", 0)), "Revenue generated"),
    ("Total Orders", format_number(kpis.get("Total Orders", 0)), "Transactions processed"),
    (profit_label, format_currency(df_filtered[profit_col].sum()) if profit_col else "₹0.00", profit_note),
    ("Average Order Value", format_currency(kpis.get("Average Order Value", 0)), "Revenue per order"),
    ("Units Sold", format_number(kpis.get("Total Quantity", 0)), "Volume shipped"),
    (margin_label, f"{((df_filtered[profit_col].sum() / df_filtered[revenue_col].sum()) * 100) if profit_col and revenue_col and df_filtered[revenue_col].sum() else 0:.1f}%", profit_note),
]

kpi_cols = st.columns(len(summary_cards), gap="small")
for idx, (label, value, note) in enumerate(summary_cards):
    with kpi_cols[idx]:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-change">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

summary_col_1, summary_col_2, summary_col_3 = st.columns(3)
with summary_col_1:
    st.markdown(
        """
        <div class="summary-card">
            <div class="summary-label">Best Product</div>
            <div class="summary-value">""" + (
                f"{df_filtered.groupby(product_col)[revenue_col].sum().idxmax()}" if product_col and revenue_col and not df_filtered.empty else "N/A"
            ) + """</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with summary_col_2:
    st.markdown(
        """
        <div class="summary-card">
            <div class="summary-label">Top Region</div>
            <div class="summary-value">""" + (
                f"{df_filtered.groupby(region_col)[revenue_col].sum().idxmax()}" if region_col and revenue_col and not df_filtered.empty else "N/A"
            ) + """</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with summary_col_3:
    growth_text = "N/A"
    growth_detail = "Select at least two months"
    if date_col and revenue_col and not df_filtered.empty:
        monthly_growth = df_filtered.groupby(df_filtered[date_col].dt.to_period("M"))[revenue_col].sum().sort_index()
        if len(monthly_growth) >= 2 and monthly_growth.iloc[-2] != 0:
            growth = (monthly_growth.iloc[-1] - monthly_growth.iloc[-2]) / monthly_growth.iloc[-2] * 100
            growth_text = f"{growth:+.1f}%"
            growth_detail = f"{monthly_growth.index[-1].strftime('%b %Y')} vs {monthly_growth.index[-2].strftime('%b %Y')}"
    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-label">Month-over-month revenue change</div>
            <div class="summary-value">{growth_text}</div>
            <div class="kpi-change">{growth_detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Chart row 1
first_row = st.columns(2)

with first_row[0]:
    st.markdown('<div class="chart-title">Revenue Trend</div>', unsafe_allow_html=True)
    if date_col and revenue_col and not df_filtered.empty:
        period_map = {"Monthly": "M", "Quarterly": "Q", "Yearly": "Y"}
        period_key = period_map.get(trend_period, "M")
        trend_df = (
            df_filtered.assign(_period=df_filtered[date_col].dt.to_period(period_key).astype(str))
            .groupby("_period", as_index=False)[revenue_col]
            .sum()
            .rename(columns={"_period": "Period", revenue_col: "Revenue"})
        )
        trend_df["Revenue INR"] = trend_df["Revenue"].map(format_currency)
        trend_fig = px.line(trend_df, x="Period", y="Revenue", markers=True, line_shape="linear", color_discrete_sequence=["#1d5e99"], custom_data=["Revenue INR"])
        trend_fig.update_traces(hovertemplate="%{x}<br>Revenue: %{customdata[0]}<extra></extra>")
        trend_fig.update_layout(margin=dict(t=5, b=20, l=10, r=10), paper_bgcolor="white", plot_bgcolor="white", xaxis_title="Period", yaxis_title="Revenue", hovermode="x unified")
        trend_fig.update_xaxes(tickfont=dict(color="#263d56"), title_font=dict(color="#263d56"), gridcolor="#e5ebf2")
        apply_indian_currency_axis(trend_fig, trend_df["Revenue"])
        st.plotly_chart(trend_fig, width="stretch", config={"displayModeBar": False})
    else:
        st.info("Revenue trend is unavailable for the current selection.")

with first_row[1]:
    st.markdown('<div class="chart-title">Regional Performance</div>', unsafe_allow_html=True)
    if region_col and revenue_col and not df_filtered.empty:
        region_summary = (
            df_filtered.groupby(region_col, as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .rename(columns={region_col: "Region", revenue_col: "Revenue"})
        )
        region_summary["Revenue INR"] = region_summary["Revenue"].map(format_currency)
        bar_fig = px.bar(region_summary, x="Region", y="Revenue", custom_data=["Revenue INR"], color_discrete_sequence=["#1d5e99"])
        bar_fig.update_traces(hovertemplate="%{x}<br>Revenue: %{customdata[0]}<extra></extra>")
        bar_fig.update_layout(margin=dict(t=5, b=20, l=10, r=10), paper_bgcolor="white", plot_bgcolor="white", xaxis_title="Region", yaxis_title="Revenue")
        bar_fig.update_xaxes(tickfont=dict(color="#263d56"), title_font=dict(color="#263d56"), gridcolor="#e5ebf2")
        apply_indian_currency_axis(bar_fig, region_summary["Revenue"])
        st.plotly_chart(bar_fig, width="stretch", config={"displayModeBar": False})
    else:
        st.info("Regional performance data is unavailable.")

# Chart row 2
second_row = st.columns(2)

with second_row[0]:
    st.markdown('<div class="chart-title">High-Value Categories by Revenue</div>', unsafe_allow_html=True)
    if category_col and revenue_col and not df_filtered.empty:
        category_summary = (
            df_filtered.groupby(category_col, as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .rename(columns={category_col: "Category", revenue_col: "Revenue"})
        )
        category_summary["Revenue INR"] = category_summary["Revenue"].map(format_currency)
        pie_fig = px.pie(
            category_summary,
            names="Category",
            values="Revenue",
            hole=0.45,
            custom_data=["Revenue INR"],
            color_discrete_sequence=["#164E83", "#2468A0", "#317FB1", "#405D87", "#1A718B", "#28577A"],
        )
        pie_fig.update_traces(
            textinfo="label+percent",
            marker_line_color="#ffffff",
            marker_line_width=2,
            hovertemplate="%{label}<br>Revenue: %{customdata[0]}<br>Share: %{percent}<extra></extra>",
        )
        pie_fig.update_layout(margin=dict(t=5, b=5, l=5, r=5), paper_bgcolor="white", showlegend=False)
        st.plotly_chart(pie_fig, width="stretch", config={"displayModeBar": False})
    else:
        st.info("Category breakdown is unavailable.")

with second_row[1]:
    st.markdown('<div class="chart-title">Top Products by Revenue</div>', unsafe_allow_html=True)
    if product_col and revenue_col and not df_filtered.empty:
        top_df = (
            df_filtered.groupby(product_col, as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .head(top_n)
            .rename(columns={product_col: "Product", revenue_col: "Revenue"})
        )
        top_df["Revenue INR"] = top_df["Revenue"].map(format_currency)
        product_fig = px.bar(top_df, x="Product", y="Revenue", custom_data=["Revenue INR"], color_discrete_sequence=["#1d5e99"])
        product_fig.update_traces(hovertemplate="%{x}<br>Revenue: %{customdata[0]}<extra></extra>")
        product_fig.update_layout(margin=dict(t=5, b=20, l=10, r=10), paper_bgcolor="white", plot_bgcolor="white", xaxis_title="Product", yaxis_title="Revenue", showlegend=False)
        product_fig.update_xaxes(tickfont=dict(color="#263d56"), title_font=dict(color="#263d56"), gridcolor="#e5ebf2")
        apply_indian_currency_axis(product_fig, top_df["Revenue"])
        st.plotly_chart(product_fig, width="stretch", config={"displayModeBar": False})
    else:
        st.info("Top product data is unavailable.")

st.markdown("### Top-Selling Products by Units")
if product_col and quantity_col and not df_filtered.empty:
    top_selling = get_top_products_by_quantity(df_filtered, top_n).sort_values("Quantity", ascending=True)
    units_fig = px.bar(
        top_selling,
        x="Quantity",
        y="Product",
        orientation="h",
        color_discrete_sequence=["#1d5e99"],
    )
    units_fig.update_traces(hovertemplate="%{y}<br>Units sold: %{x:,.0f}<extra></extra>")
    units_fig.update_layout(
        margin=dict(t=5, b=20, l=10, r=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Units sold",
        yaxis_title="Product",
    )
    units_fig.update_xaxes(rangemode="tozero", tickfont=dict(color="#263d56"), title_font=dict(color="#263d56"), gridcolor="#e5ebf2")
    units_fig.update_yaxes(tickfont=dict(color="#263d56"), title_font=dict(color="#263d56"))
    st.plotly_chart(units_fig, width="stretch", config={"displayModeBar": False})
else:
    st.info("Top-selling product data is unavailable for the current selection.")

# Bottom row
# Bottom row
st.markdown("### Category Profitability")
if category_col and revenue_col and profit_col and not df_filtered.empty:
    category_profitability = (
        df_filtered.groupby(category_col, as_index=False)
        .agg(Revenue=(revenue_col, "sum"), Profit=(profit_col, "sum"))
        .sort_values("Profit", ascending=False)
        .rename(columns={category_col: "Category"})
    )
    category_profitability["Profit Margin"] = (
        category_profitability["Profit"] / category_profitability["Revenue"].replace(0, pd.NA) * 100
    )
    category_display = category_profitability.copy()
    category_display["Revenue"] = category_display["Revenue"].map(format_currency)
    category_display["Profit"] = category_display["Profit"].map(format_currency)
    category_display["Profit Margin"] = category_display["Profit Margin"].map(lambda value: f"{value:.1f}%" if pd.notna(value) else "N/A")
    st.dataframe(
        category_display,
        width="stretch",
        hide_index=True,
        column_config={
            "Category": st.column_config.TextColumn("Category", width="medium"),
            "Revenue": st.column_config.TextColumn("Revenue", width="large"),
            "Profit": st.column_config.TextColumn("Profit", width="large"),
            "Profit Margin": st.column_config.TextColumn("Profit Margin", width="medium"),
        },
    )
    st.caption(profit_note)
else:
    st.info("Category profit analysis is unavailable for the current selection.")

third_row = st.columns([1.2, 0.8])

with third_row[0]:
    st.markdown('<div class="chart-title">Business Insights</div>', unsafe_allow_html=True)
    insight_list = build_business_insights(df_filtered)
    st.markdown(
        '<div class="insight-box">' + '<br>'.join(f"• {item}" for item in insight_list) + '</div>',
        unsafe_allow_html=True,
    )

with third_row[1]:
    st.markdown('<div class="chart-title">Applied Filters</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-label">Current selection</div>
            <div class="summary-value">{selected_year}</div>
            <div style="margin-top: 0.7rem; color: #334a63; line-height: 1.8;">
                <strong>Dates:</strong> {start_date} to {end_date}<br>
                <strong>Region:</strong> {selected_region}<br>
                <strong>Category:</strong> {selected_category}<br>
                <strong>Product:</strong> {selected_product}<br>
                <strong>Matching rows:</strong> {len(df_filtered):,}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("### Actionable Recommendations")
recommendations = build_business_recommendations(df_filtered)
recommendation_columns = st.columns(2)
for index, recommendation in enumerate(recommendations):
    recommendation_columns[index % 2].info(recommendation)

profit_cleaning_note = (
    "Profit is estimated at 28% of revenue because actual cost and returns data are unavailable."
    if profit_is_estimated
    else "Profit is calculated from the available total or unit cost column; rows without cost use the clearly flagged estimate."
)

with st.expander("Data Cleaning and Metric Notes"):
    st.markdown(
        f"""
        - Dates are parsed with invalid values excluded; text labels are trimmed and standardized, with missing category/product/region labels retained as **Unknown**.
        - Exact duplicate rows are removed. Missing or non-positive quantity and unit-price values are excluded.
        - Numeric values are coerced; missing discounts default to zero, and missing revenue is derived from quantity, unit price, and discount.
        - {profit_cleaning_note}
        - Month-over-month revenue change compares the latest month in the selected range with the preceding month.
        """
    )

report_html = build_executive_report(df_filtered, selected_year, start_date, end_date, recommendations)
st.download_button("Download Executive Report", data=report_html, file_name=f"sales_executive_report_{selected_year}.html", mime="text/html")

with st.expander("Detailed Sales Data"):
    display_df = df_filtered.copy()
    money_columns = [column for column in display_df.columns if column.lower() in {"revenue", "profit", "gross profit", "unit_price", "unit price"}]
    for column in money_columns:
        display_df[column] = display_df[column].map(format_currency)
    st.dataframe(display_df, width="stretch")
    csv_data = df_filtered.to_csv(index=False)
    st.download_button("Download Filtered Data", csv_data, file_name=f"sales_data_{selected_year}.csv", mime="text/csv")
