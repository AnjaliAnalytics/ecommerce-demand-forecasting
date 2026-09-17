import pandas as pd
import numpy as np

def generate_business_impact_report(risk_csv_path, sales_csv_path, output_csv_path):
    """
    Translates inventory risk classifications into working capital metrics 
    and estimates overstock holding cost savings using transparent assumptions.
    """
    risk_df = pd.read_csv(risk_csv_path)
    sales_df = pd.read_csv(sales_csv_path)
    
    sku_prices = sales_df.groupby('StockCode')['Price'].mean().reset_index()
    impact_df = pd.merge(risk_df, sku_prices, on='StockCode', how='left')
    impact_df['Price'] = impact_df['Price'].fillna(impact_df['Price'].median())
    
    impact_df['Current_Stock_Value_GBP'] = impact_df['Inventory_Position'] * impact_df['Price']
    impact_df['Reorder_Capital_Required_GBP'] = impact_df['Reorder_Quantity'] * impact_df['Price']
    impact_df['Excess_Units'] = np.maximum(0, impact_df['Inventory_Position'] - (impact_df['Reorder_Point'] * 2.5))
    impact_df['Excess_Capital_Tied_Up_GBP'] = impact_df['Excess_Units'] * impact_df['Price']
    
    impact_df.to_csv(output_csv_path, index=False)
    print(f"Business impact dataset successfully saved to {output_csv_path}")
    return impact_df

if __name__ == "__main__":
    generate_business_impact_report(
        'data/processed/inventory_risk_prioritization.csv',
        'data/processed/cleaned_online_retail.csv',
        'data/processed/business_impact_summary.csv'
    )