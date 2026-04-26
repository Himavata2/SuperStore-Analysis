import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar

# Set page config for a wider layout
st.set_page_config(page_title="Superstore Sales Analysis", layout="wide")

st.title("📊 Superstore Sales Optimization Dashboard")

# -----------------------------
# 1. Optimized Data Loading (Matches "milliseconds" claim)
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r'C:\Users\lenovo\Pandas Project 2\train.csv')
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['order_date'])
    df['order_month'] = df['order_date'].dt.month.astype(int)
    return df

df = load_data()

# -----------------------------
# 2. Multi-Page Setup (Matches "Built a multi-page app" claim)
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview & filtering", "Deep Dive Analytics"])

# -----------------------------
# 3. 3-Tier Filtering System (Matches "3-tier filtering system" claim)
# -----------------------------
st.sidebar.header("3-Tier Filters")

# Tier 1: Region
region_options = ["All"] + df['region'].unique().tolist()
selected_region = st.sidebar.selectbox("1. Select Region", region_options)

# Apply Tier 1 Filter
if selected_region != "All":
    filtered_df = df[df['region'] == selected_region]
else:
    filtered_df = df.copy()

# Tier 2: Category (Dynamic based on Region)
category_options = ["All"] + filtered_df['category'].unique().tolist()
selected_category = st.sidebar.selectbox("2. Select Category", category_options)

# Apply Tier 2 Filter
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

# Tier 3: Sub-Category (Dynamic based on Category)
subcategory_options = ["All"] + filtered_df['sub-category'].unique().tolist()
selected_subcategory = st.sidebar.selectbox("3. Select Sub-Category", subcategory_options)

# Apply Tier 3 Filter
if selected_subcategory != "All":
    filtered_df = filtered_df[filtered_df['sub-category'] == selected_subcategory]


# -----------------------------
# Page 1: Overview & Filtering
# -----------------------------
if page == "Overview & filtering":
    st.header(f"Sales Overview")
    
    # Quick Metrics (Great for highlighting the "West Region 31% market share" insight)
    total_sales = filtered_df['sales'].sum()
    total_orders = filtered_df['order_id'].nunique()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Avg Order Value", f"${(total_sales/total_orders if total_orders > 0 else 0):,.2f}")
    
    st.subheader("Filtered Data")
    st.dataframe(filtered_df.head(100)) # Show preview

# -----------------------------
# Page 2: Deep Dive Analytics
# -----------------------------
elif page == "Deep Dive Analytics":
    st.header("Visual Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Category Sales
        st.subheader("Category vs Sales")
        category_sales = filtered_df.groupby('category')['sales'].sum()
        if not category_sales.empty:
            fig, ax = plt.subplots(figsize=(6, 4))
            category_sales.plot(kind='bar', color='teal', ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.write("No data available for this filter combination.")

    with col2:
        # Monthly Trend (Matches "Discovered a 20% MoM sales surge" claim)
        st.subheader("Monthly Sales Trend")
        monthly_sales = filtered_df.groupby('order_month')['sales'].sum().sort_index()
        if not monthly_sales.empty:
            monthly_sales.index = monthly_sales.index.map(lambda x: calendar.month_abbr[int(x)])
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            monthly_sales.plot(kind='line', marker='o', color='coral', ax=ax2)
            plt.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig2)
        else:
            st.write("No data available for this filter combination.")

    # Top Products
    st.subheader("Top 10 Products by Revenue")
    top_products = filtered_df.groupby('product_name')['sales'].sum().sort_values(ascending=False).head(10)
    if not top_products.empty:
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        top_products.sort_values().plot(kind='barh', color='indigo', ax=ax3)
        plt.xlabel("Total Sales ($)")
        plt.ylabel("")
        st.pyplot(fig3)
    else:
        st.write("No data available.")