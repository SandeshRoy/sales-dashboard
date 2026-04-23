import streamlit as st
import pandas as pd

# -------------------------------
# Load Data
# -------------------------------
df = pd.read_csv("superstore.csv", encoding='latin1')

# Fix date
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Feature Engineering
df['Profit Margin'] = df['Profit'] / df['Sales']
df['Profit Margin'] = df['Profit Margin'].replace([float('inf'), -float('inf')], 0).fillna(0)

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.title("Filters")

region = st.sidebar.selectbox("Region", ["All"] + list(df['Region'].unique()))
category = st.sidebar.selectbox("Category", ["All"] + list(df['Category'].unique()))

# Apply filters
filtered = df.copy()

if region != "All":
    filtered = filtered[filtered['Region'] == region]

if category != "All":
    filtered = filtered[filtered['Category'] == category]

# -------------------------------
# Title
# -------------------------------
st.title("📊 Advanced Sales & Revenue Dashboard")

# -------------------------------
# KPIs
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{filtered['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"{filtered['Profit'].sum():,.0f}")
col3.metric("Avg Profit Margin", f"{filtered['Profit Margin'].mean():.2f}")

# -------------------------------
# Charts
# -------------------------------
st.subheader("📈 Sales Trend")
sales_trend = filtered.groupby('Order Date')['Sales'].sum()
st.line_chart(sales_trend)

st.subheader("💰 Profit by Category")
st.bar_chart(filtered.groupby('Category')['Profit'].sum())

st.subheader("📦 Profit by Sub-Category")
st.bar_chart(filtered.groupby('Sub-Category')['Profit'].sum())

st.subheader("🎯 Discount Impact on Profit")
st.line_chart(filtered.groupby('Discount')['Profit'].mean())

st.subheader("📊 Sales vs Profit")
st.scatter_chart(filtered[['Sales', 'Profit']])

# -------------------------------
# Top Products (ADDED)
# -------------------------------
st.subheader("🏆 Top 10 Products")
top_products = filtered.groupby('Product Name')['Sales'].sum() \
                       .sort_values(ascending=False).head(10)
st.bar_chart(top_products)

# -------------------------------
# Loss-Making Products
# -------------------------------
st.subheader("⚠ Loss-Making Products")
loss = filtered[filtered['Profit'] < 0].sort_values(by='Profit')
st.dataframe(loss[['Product Name', 'Sales', 'Profit']].head(10))

# -------------------------------
# Key Insights (IMPORTANT)
# -------------------------------
st.subheader("📌 Key Insights")

st.write("""
- High discounts significantly reduce profit  
- Some products generate high sales but negative profit  
- Technology category contributes high revenue  
- Profit varies significantly across regions  
""")