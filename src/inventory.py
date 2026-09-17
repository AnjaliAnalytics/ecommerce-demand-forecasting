import pandas as pd
import numpy as np

def calculate_inventory_metrics(weekly_demand_path, lead_time_weeks=2, z_score=1.65):
    """
    Computes Safety Stock, Reorder Point, and simulated inventory risk status for SKUs.
    """
    weekly_df = pd.read_csv(weekly_demand_path)
    
    # Compute demand statistics
    inv_df = weekly_df.groupby('StockCode').agg(
        Avg_Weekly_Demand=('Quantity', 'mean'),
        Demand_Std_Dev=('Quantity', 'std'),
        Recent_Forecast_Demand=('Quantity', lambda x: x.tail(4).mean())
    ).reset_index()
    
    # Formulas
    inv_df['Lead_Time_Weeks'] = lead_time_weeks
    inv_df['Lead_Time_Demand'] = (inv_df['Avg_Weekly_Demand'] * lead_time_weeks).round(2)
    inv_df['Safety_Stock'] = np.ceil(z_score * inv_df['Demand_Std_Dev'] * np.sqrt(lead_time_weeks))
    inv_df['Reorder_Point'] = inv_df['Lead_Time_Demand'] + inv_df['Safety_Stock']
    
    # Simulation (Explicitly labeled)
    np.random.seed(42)
    var_factor = np.random.uniform(0.5, 1.8, size=len(inv_df))
    inv_df['Simulated_Current_Stock'] = np.round(inv_df['Reorder_Point'] * var_factor)
    
    # Risk logic
    inv_df['Stockout_Risk'] = np.where(
        inv_df['Simulated_Current_Stock'] <= inv_df['Reorder_Point'], 'HIGH',
        np.where(inv_df['Simulated_Current_Stock'] <= (inv_df['Reorder_Point'] + inv_df['Safety_Stock']), 'MEDIUM', 'LOW')
    )
    
    inv_df['Overstock_Risk'] = np.where(
        inv_df['Simulated_Current_Stock'] > (inv_df['Reorder_Point'] * 2.5), 'HIGH', 'LOW'
    )
    
    return inv_df

if __name__ == "__main__":
    input_csv = 'data/processed/weekly_sku_demand.csv'
    output_csv = 'data/processed/inventory_analysis_table.csv'
    
    res_df = calculate_inventory_metrics(input_csv)
    res_df.to_csv(output_csv, index=False)
    print(f"Inventory analytics table exported successfully to: {output_csv}")