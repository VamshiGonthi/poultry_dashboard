
import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================
#            LOAD DATA FROM GITHUB
# ==============================================
DATA_URL = "https://raw.githubusercontent.com/VamshiGonthi/poultry_dashboard/main/Superstore.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(DATA_URL, sheet_name="Orders")
    return df

df = load_data()

# ==============================================
#                 PAGE TITLE
# ==============================================
st.title("📊 Superstore Sales Dashboard")
st.markdown("Interactive dashboard with filters and 4 clean visualizations.")

# ==============================================
#              GLOBAL FILTERS (TOP)
# ==============================================
st.sidebar.header("FILTERS")

categories = sorted(df["Category"].unique())
subcats = sorted(df["Sub-Category"].unique())
regions = sorted(df["Region"].unique())
years = sorted(df["Order Date"].dt.year.unique())

selected_category = st.sidebar.multiselect("Category", categories, default=categories)
selected_subcat = st.sidebar.multiselect("Sub-Category", subcats, default=subcats)
selected_region = st.sidebar.multiselect("Region", regions, default=regions)
selected_year = st.sidebar.multiselect("Year", years, default=years)

# Apply filters
df_filtered = df[
    (df["Category"].isin(selected_category)) &
    (df["Sub-Category"].isin(selected_subcat)) &
    (df["Region"].isin(selected_region)) &
    (df["Order Date"].dt.year.isin(selected_year))
]

# ==============================================
#               4 DASHBOARD CHARTS
# ==============================================

# ----- 1. Sales by Category -----
cat_sales = df_filtered.groupby("Category")["Sales"].sum().reset_index()
fig1 = px.bar(cat_sales, x="Category", y="Sales", title="Sales by Category")

# ----- 2. Profit by Sub-Category -----
sub_profit = df_filtered.groupby("Sub-Category")["Profit"].sum().reset_index()
fig2 = px.bar(sub_profit, x="Sub-Category", y="Profit", title="Profit by Sub-Category")

# ----- 3. Sales Trend Over Time -----
df_filtered["Year"] = df_filtered["Order Date"].dt.year
yearly_sales = df_filtered.groupby("Year")["Sales"].sum().reset_index()
fig3 = px.line(yearly_sales, x="Year", y="Sales", markers=True, title="Year-wise Sales Trend")

# ----- 4. Region-wise Sales -----
region_sales = df_filtered.groupby("Region")["Sales"].sum().reset_index()
fig4 = px.pie(region_sales, names="Region", values="Sales", title="Sales Share by Region")

# ==============================================
#             SHOW CHARTS
# ==============================================
st.subheader("📌 Chart 1 — Sales by Category")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📌 Chart 2 — Profit by Sub-Category")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📌 Chart 3 — Sales Trend Over Years")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📌 Chart 4 — Region-wise Sales Distribution")
st.plotly_chart(fig4, use_container_width=True)
