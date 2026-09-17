import os
import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="E-Commerce Demand & Inventory Intelligence",
    page_icon="📦",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load pre-calculated outputs."""
    sales_path = 'data/processed/cleaned_online_retail.csv'
    impact_path = 'data/processed/business_impact_summary.csv'
    briefing_path = 'reports/genai_executive_briefing.md'

    sales_df = pd.read_csv(sales_path) if os.path.exists(sales_path) else pd.DataFrame()
    impact_df = pd.read_csv(impact_path) if os.path.exists(impact_path) else pd.DataFrame()
    
    briefing_text = ""
    if os.path.exists(briefing_path):
        with open(briefing_path, 'r', encoding='utf-8') as f:
            briefing_text = f.read()

    return sales_df, impact_df, briefing_text

# Load datasets
sales_df, impact_df, briefing_text = load_data()

st.title("📦 E-Commerce Demand Forecasting & Inventory Control")
st.markdown("Interactive portfolio viewer using pre-calculated ML forecasts and risk decision logic.")

# Sidebar - Product Selector
st.sidebar.header("Product Selection")

if not impact_df.empty:
    # Ensure string keys
    impact_df['StockCode'] = impact_df['StockCode'].astype(str)
    
    selected_sku = st.sidebar.selectbox(
        "Select Product SKU (StockCode):",
        options=impact_df['StockCode'].unique()
    )

    # Filter data for selected product
    prod_impact = impact_df[impact_df['StockCode'] == selected_sku].iloc[0]

    st.subheader(f"SKU Analysis: {selected_sku}")
    
    # Row 1: Key Metrics Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Forecast Demand", f"{prod_impact.get('Forecast_Demand', 0):,.0f} units")
    col2.metric("Inventory Position", f"{prod_impact.get('Inventory_Position', 0):,.0f} units")
    col3.metric("Reorder Point (ROP)", f"{prod_impact.get('Reorder_Point', 0):,.0f} units")
    col4.metric("Recommended Action", str(prod_impact.get('Risk_Action', 'N/A')))

    st.markdown("---")

    # Row 2: Inventory Risk & Safety Stock
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 📊 Inventory & Risk Breakdown")
        st.write(f"**Risk Category:** {prod_impact.get('Risk_Category', 'N/A')}")
        st.write(f"**Safety Stock (CSL 95%):** {prod_impact.get('Safety_Stock', 0):,.0f} units")
        st.write(f"**Reorder Quantity:** {prod_impact.get('Reorder_Quantity', 0):,.0f} units")
        st.write(f"**Current Stock Value:** £{prod_impact.get('Current_Stock_Value_GBP', 0):,.2f}")
        
    with col_right:
        st.markdown("### 🎯 Model Performance Baseline")
        st.write("**Winning Model:** 4-Week Moving Average")
        st.write("**Validation WAPE:** 50.34%")
        st.write("**Validation MAE:** 325.50 units")
        st.write("**Forecast Horizon:** 10-Week Out-of-Sample Holdout")

    # Row 3: Historical Demand Trend Plot
    if not sales_df.empty:
        st.markdown("---")
        st.markdown("### 📈 Historical Weekly Demand Trend")
        
        sales_df['StockCode'] = sales_df['StockCode'].astype(str)
        sales_df['InvoiceDate'] = pd.to_datetime(sales_df['InvoiceDate'])
        
        sku_sales = sales_df[sales_df['StockCode'] == selected_sku].copy()
        
        if not sku_sales.empty:
            weekly_sales = sku_sales.resample('W-MON', on='InvoiceDate')['Quantity'].sum().reset_index()
            st.line_chart(weekly_sales.set_index('InvoiceDate')['Quantity'])
        else:
            st.info("No historical sales records found for this specific SKU.")

    # Row 4: GenAI Executive Briefing Tab
    st.markdown("---")
    st.markdown("### 🤖 AI-Generated Business Summary")
    if briefing_text:
        with st.expander("View Executive Briefing (Generated via Gemini API)", expanded=False):
            st.markdown(briefing_text)
    else:
        st.info("No AI briefing file found at `reports/genai_executive_briefing.md`.")

else:
    st.error("Processed impact summary CSV not found. Ensure `data/processed/business_impact_summary.csv` exists.")