import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar

st.title("📊 Superstore Sales Analysis")

# Load dataset
df = pd.read_csv(r'C:\Users\lenovo\Pandas Project 2\train.csv')

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Convert dates
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df = df.dropna(subset=['order_date'])  # remove invalid dates

# Create month column
df['order_month'] = df['order_date'].dt.month.astype(int)

# Sidebar
st.sidebar.header("Filters")

selected_region = st.sidebar.selectbox("Select Region", df['region'].unique())

# Filter data
filtered_df = df[df['region'] == selected_region]

# Show data
st.subheader("Filtered Data")
st.write(filtered_df.head())

# -----------------------------
# Category Sales
st.subheader("Category vs Sales")

category_sales = filtered_df.groupby('category')['sales'].sum()

fig, ax = plt.subplots()
category_sales.plot(kind='bar', ax=ax)

st.pyplot(fig)

# -----------------------------
# Monthly Trend
st.subheader("Monthly Sales Trend")

monthly_sales = filtered_df.groupby('order_month')['sales'].sum().sort_index()
monthly_sales.index = monthly_sales.index.map(lambda x: calendar.month_abbr[int(x)])

fig2, ax2 = plt.subplots()
monthly_sales.plot(kind='line', marker='o', ax=ax2)

st.pyplot(fig2)

# -----------------------------
# Top Products
st.subheader("Top 10 Products")

top_products = filtered_df.groupby('product_name')['sales'].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots()
top_products.sort_values().plot(kind='barh', ax=ax3)

st.pyplot(fig3)