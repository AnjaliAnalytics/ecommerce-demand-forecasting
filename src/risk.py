import pandas as pd
import numpy as np

def run_risk_prioritization(input_csv, output_csv):
    """
    Applies rule-based risk logic to classify inventory status 
    and exports a prioritized inventory management table.
    """
    df = pd.read_csv(input_csv)
    
    def classify_row(row):
        inv_pos = row['Inventory_Position']
        rop = row['Reorder_Point']
        ss = row['Safety_Stock']
        
        if inv_pos <= rop:
            return 'HIGH STOCKOUT RISK', 'REORDER NOW', 1
        elif inv_pos <= (rop + ss):
            return 'MODERATE RISK', 'MONITOR', 2
        elif inv_pos <= (rop * 2.5):
            return 'SUFFICIENT STOCK', 'SUFFICIENT STOCK', 4
        else:
            return 'POTENTIAL OVERSTOCK', 'POTENTIAL OVERSTOCK', 3

    risk_results = df.apply(classify_row, axis=1)
    
    df['Risk_Category'] = [r[0] for r in risk_results]
    df['Risk_Action'] = [r[1] for r in risk_results]
    df['Priority_Rank'] = [r[2] for r in risk_results]
    
    prioritized_df = df.sort_values(
        by=['Priority_Rank', 'Forecast_Demand'], 
        ascending=[True, False]
    ).reset_index(drop=True)
    
    output_cols = [
        'StockCode', 'Forecast_Demand', 'Safety_Stock', 
        'Reorder_Point', 'Inventory_Position', 'Reorder_Quantity', 
        'Risk_Category', 'Risk_Action'
    ]
    
    res_df = prioritized_df[output_cols]
    res_df.to_csv(output_csv, index=False)
    print(f"Risk classification completed. Output saved to: {output_csv}")
    return res_df

if __name__ == "__main__":
    run_risk_prioritization(
        'data/processed/reorder_recommendations.csv',
        'data/processed/inventory_risk_prioritization.csv'
    )