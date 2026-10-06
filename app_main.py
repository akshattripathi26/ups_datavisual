import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="UPS Parcel Analytics Dashboard",
    page_icon="📦",
    layout="wide"
)

# Load and Cache Data
@st.cache_data
def load_data():
    file_path = "data/main/UPS Parcel Dataset - 2025.xlsx"
    # Using header=2 to skip top decorative rows in the Excel file
    df = pd.read_excel(file_path, header=2)
    
    # Convert date columns to datetime
    date_cols = ['InvDate', 'ShipDate', 'CustomerStmtBeginPeriodDate']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    # Clean numeric columns
    if 'NetCharge' in df.columns:
        df['NetCharge'] = pd.to_numeric(df['NetCharge'], errors='coerce')
        
    return df

# Load Data
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data from `data/main/UPS Parcel Dataset - 2025.xlsx`: {e}")
    st.stop()

# Title
st.title("📦 UPS Parcel Shipment Dashboard")
st.markdown("Visualizing logistics costs, service distribution, and shipment trends.")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Carrier Filter
carriers = df['CarrierShortNm'].dropna().unique().tolist() if 'CarrierShortNm' in df.columns else []
selected_carrier = st.sidebar.multiselect("Select Carrier", options=carriers, default=carriers)

# Service Type Filter
services = df['ServiceTypeNm'].dropna().unique().tolist() if 'ServiceTypeNm' in df.columns else []
selected_service = st.sidebar.multiselect("Select Service Type", options=services, default=services)

# Month Filter
months = sorted(df['Combined Ship Month'].dropna().unique().tolist()) if 'Combined Ship Month' in df.columns else []
selected_month = st.sidebar.multiselect("Select Ship Month", options=months, default=months)

# Filter Dataframe
filtered_df = df.copy()

if selected_carrier:
    filtered_df = filtered_df[filtered_df['CarrierShortNm'].isin(selected_carrier)]
if selected_service:
    filtered_df = filtered_df[filtered_df['ServiceTypeNm'].isin(selected_service)]
if selected_month:
    filtered_df = filtered_df[filtered_df['Combined Ship Month'].isin(selected_month)]

# Key Performance Indicators (KPIs)
col1, col2, col3, col4 = st.columns(4)

total_net_charge = filtered_df['NetCharge'].sum() if 'NetCharge' in filtered_df.columns else 0
total_shipments = len(filtered_df)
avg_charge = filtered_df['NetCharge'].mean() if 'NetCharge' in filtered_df.columns else 0
unique_vendors = filtered_df['VendorNbr'].nunique() if 'VendorNbr' in filtered_df.columns else 0

col1.metric("Total Net Charge", f"${total_net_charge:,.2f}")
col2.metric("Total Shipments", f"{total_shipments:,}")
col3.metric("Avg Charge / Shipment", f"${avg_charge:,.2f}")
col4.metric("Unique Vendors", f"{unique_vendors}")

st.divider()

# Charts Section
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Net Spend by Service Type")
    if 'ServiceTypeNm' in filtered_df.columns and 'NetCharge' in filtered_df.columns:
        service_spend = filtered_df.groupby('ServiceTypeNm')['NetCharge'].sum().reset_index()
        fig_service = px.bar(
            service_spend,
            x='ServiceTypeNm',
            y='NetCharge',
            labels={'ServiceTypeNm': 'Service Type', 'NetCharge': 'Total Net Charge ($)'},
            color='ServiceTypeNm',
            text_auto='.2s'
        )
        fig_service.update_layout(showlegend=False)
        st.plotly_chart(fig_service, use_container_width=True)

with row1_col2:
    st.subheader("Monthly Shipping Spend Trend")
    if 'Combined Ship Month' in filtered_df.columns and 'NetCharge' in filtered_df.columns:
        monthly_spend = filtered_df.groupby('Combined Ship Month')['NetCharge'].sum().reset_index()
        fig_month = px.line(
            monthly_spend,
            x='Combined Ship Month',
            y='NetCharge',
            markers=True,
            labels={'Combined Ship Month': 'Ship Month', 'NetCharge': 'Total Net Charge ($)'}
        )
        st.plotly_chart(fig_month, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Carrier Share")
    if 'CarrierShortNm' in filtered_df.columns and 'NetCharge' in filtered_df.columns:
        carrier_spend = filtered_df.groupby('CarrierShortNm')['NetCharge'].sum().reset_index()
        fig_carrier = px.pie(
            carrier_spend,
            names='CarrierShortNm',
            values='NetCharge',
            hole=0.4
        )
        st.plotly_chart(fig_carrier, use_container_width=True)

with row2_col2:
    st.subheader("Top Vendors by Spend")
    if 'VendorNbr' in filtered_df.columns and 'NetCharge' in filtered_df.columns:
        vendor_spend = filtered_df.groupby('VendorNbr')['NetCharge'].sum().nlargest(10).reset_index()
        vendor_spend['VendorNbr'] = vendor_spend['VendorNbr'].astype(str)
        fig_vendor = px.bar(
            vendor_spend,
            x='VendorNbr',
            y='NetCharge',
            labels={'VendorNbr': 'Vendor Number', 'NetCharge': 'Total Net Charge ($)'},
            color_discrete_sequence=['#FFC000']
        )
        st.plotly_chart(fig_vendor, use_container_width=True)

# Raw Data Section
with st.expander("🔍 View Raw Filtered Data"):
    st.dataframe(filtered_df, use_container_width=True)
