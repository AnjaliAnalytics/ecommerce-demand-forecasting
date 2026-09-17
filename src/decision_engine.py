import pandas as pd
import numpy as np

def generate_reorder_recommendations(inventory_csv_path, output_csv_path):
    """
    Computes mathematical Safety Stock, ROP, Reorder Quantities, 
    and actionable operational recommendations.
    """
    df = pd.read_csv(inventory_csv_path)
    
    Z_SCORE = 1.65          # 95% Service Level
    LEAD_TIME_WEEKS = 2     # 2-Week Lead Time
    TARGET_COVERAGE_WKS = 4 # 4-Week Coverage
    
    # Assign missing column to DataFrame
    df['Lead_Time_Weeks'] = LEAD_TIME_WEEKS
    
    df['Lead_Time_Demand'] = (df['Recent_Forecast_Demand'] * LEAD_TIME_WEEKS).round(2)
    df['Safety_Stock'] = np.ceil(Z_SCORE * df['Demand_Std_Dev'] * np.sqrt(LEAD_TIME_WEEKS))
    df['Reorder_Point'] = df['Lead_Time_Demand'] + df['Safety_Stock']
    
    df['Target_Stock'] = df['Recent_Forecast_Demand'] * TARGET_COVERAGE_WKS
    df['Inventory_Position'] = df['Simulated_Current_Stock']
    
    df['Reorder_Quantity'] = np.where(
        df['Inventory_Position'] <= df['Reorder_Point'],
        np.maximum(0, np.ceil(df['Target_Stock'] - df['Inventory_Position'])),
        0
    )
    
    def assign_action(row):
        if row['Inventory_Position'] <= row['Reorder_Point']:
            return 'REORDER IMMEDIATELY'
        elif row['Inventory_Position'] <= (row['Reorder_Point'] + row['Safety_Stock']):
            return 'MONITOR CLOSELY'
        elif row['Inventory_Position'] > (row['Reorder_Point'] * 2.5):
            return 'OVERSTOCKED - HALT PURCHASING'
        else:
            return 'STOCK LEVEL OPTIMAL'

    df['Recommended_Action'] = df.apply(assign_action, axis=1)
    
    rec_cols = [
        'StockCode', 'Recent_Forecast_Demand', 'Lead_Time_Weeks', 
        'Safety_Stock', 'Reorder_Point', 'Inventory_Position', 
        'Reorder_Quantity', 'Recommended_Action'
    ]
    rec_df = df[rec_cols].copy()
    rec_df.rename(columns={'Recent_Forecast_Demand': 'Forecast_Demand'}, inplace=True)
    
    rec_df.to_csv(output_csv_path, index=False)
    print(f"Reorder decision engine output saved to {output_csv_path}")
    return rec_df

if __name__ == "__main__":
    generate_reorder_recommendations(
        'data/processed/inventory_analysis_table.csv',
        'data/processed/reorder_recommendations.csv'
    )