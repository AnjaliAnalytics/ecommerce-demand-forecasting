import os
import pandas as pd
import numpy as np

def export_powerbi_tables():
    """
    Exports clean Fact and Dimension tables formatted for Power BI Star Schema import.
    Standardizes StockCodes to uppercase and drops duplicates to ensure primary key uniqueness.
    """
    output_dir = os.path.join('dashboard', 'powerbi')
    
    if os.path.exists(output_dir) and not os.path.isdir(output_dir):
        os.remove(output_dir)
        
    os.makedirs(output_dir, exist_ok=True)
    
    print("--- Step 1: Loading Processed Datasets ---")
    sales_df = pd.read_csv('data/processed/cleaned_online_retail.csv')
    impact_df = pd.read_csv('data/processed/business_impact_summary.csv')
    
    # Standardize StockCode formatting (Uppercase + Trim Spaces)
    sales_df['StockCode'] = sales_df['StockCode'].astype(str).str.upper().str.strip()
    impact_df['StockCode'] = impact_df['StockCode'].astype(str).str.upper().str.strip()
    
    # -------------------------------------------------------------
    # 1. Create Deduplicated Product Dimension (dim_product)
    # -------------------------------------------------------------
    print("--- Step 2: Extracting dim_product ---")
    dim_product = sales_df.groupby('StockCode', as_index=False).agg(
        Description=('Description', 'first'),
        UnitPrice=('Price', 'mean')
    )
    
    # Explicitly drop any remaining duplicates on StockCode
    dim_product = dim_product.drop_duplicates(subset=['StockCode']).reset_index(drop=True)
    dim_product.to_csv(os.path.join(output_dir, 'dim_product.csv'), index=False)
    
    # -------------------------------------------------------------
    # 2. Create Risk Category Dimension (dim_risk_category)
    # -------------------------------------------------------------
    print("--- Step 3: Extracting dim_risk_category ---")
    dim_risk_category = pd.DataFrame({
        'Risk_Category': ['HIGH STOCKOUT RISK', 'MODERATE RISK', 'POTENTIAL OVERSTOCK', 'SUFFICIENT STOCK'],
        'Priority_Order': [1, 2, 3, 4],
        'Risk_Color_Code': ['#D9534F', '#F0AD4E', '#5BC0DE', '#5CB85C']
    })
    dim_risk_category.to_csv(os.path.join(output_dir, 'dim_risk_category.csv'), index=False)
    
    # -------------------------------------------------------------
    # 3. Create Fact Inventory Risk Table (fact_inventory_risk)
    # -------------------------------------------------------------
    print("--- Step 4: Formatting fact_inventory_risk ---")
    target_cols = [
        'StockCode', 'Forecast_Demand', 'Safety_Stock', 'Reorder_Point', 
        'Inventory_Position', 'Reorder_Quantity', 'Risk_Category', 'Risk_Action',
        'Current_Stock_Value_GBP', 'Reorder_Capital_Required_GBP',
        'Excess_Capital_Tied_Up_GBP'
    ]
    
    available_cols = [col for col in target_cols if col in impact_df.columns]
    fact_inventory = impact_df[available_cols].copy()
    fact_inventory = fact_inventory.drop_duplicates(subset=['StockCode']).reset_index(drop=True)
    fact_inventory['Lead_Time_Weeks'] = 2
    
    fact_inventory.to_csv(os.path.join(output_dir, 'fact_inventory_risk.csv'), index=False)
    
    # -------------------------------------------------------------
    # 4. Create Calendar Date Dimension (dim_date)
    # -------------------------------------------------------------
    print("--- Step 5: Generating dim_date ---")
    sales_df['InvoiceDate'] = pd.to_datetime(sales_df['InvoiceDate'])
    min_date = sales_df['InvoiceDate'].min()
    max_date = sales_df['InvoiceDate'].max()
    
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    dim_date = pd.DataFrame({'Date': date_range})
    
    dim_date['Year'] = dim_date['Date'].dt.year
    dim_date['Month'] = dim_date['Date'].dt.month
    dim_date['MonthName'] = dim_date['Date'].dt.strftime('%B')
    dim_date['Quarter'] = 'Q' + dim_date['Date'].dt.quarter.astype(str)
    dim_date['WeekOfYear'] = dim_date['Date'].dt.isocalendar().week.astype(int)
    dim_date['DayOfWeek'] = dim_date['Date'].dt.day_name()
    
    dim_date.to_csv(os.path.join(output_dir, 'dim_date.csv'), index=False)
    
    print("\n[SUCCESS] Deduplicated Power BI Data Model CSVs exported successfully.")

if __name__ == "__main__":
    export_powerbi_tables()