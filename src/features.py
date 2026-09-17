import pandas as pd
import numpy as np

def generate_demand_features(weekly_df):
    """
    Creates lag, rolling, demand growth, and calendar features 
    for time-series forecasting. Strictly prevents data leakage.
    """
    df = weekly_df.copy()
    df['Week_Start'] = pd.to_datetime(df['Week_Start'])
    df = df.sort_values(['StockCode', 'Week_Start']).reset_index(drop=True)
    
    # 1. Weekly Lag Features (Past Demand)
    df['lag_1'] = df.groupby('StockCode')['Quantity'].shift(1)
    df['lag_2'] = df.groupby('StockCode')['Quantity'].shift(2)
    df['lag_4'] = df.groupby('StockCode')['Quantity'].shift(4)
    
    # 2. Demand Growth Feature (Percentage change between last week and 2 weeks ago)
    # Adding small constant (+1e-5) to prevent division by zero during zero-demand weeks
    df['demand_growth_1w'] = (df['lag_1'] - df['lag_2']) / (df['lag_2'] + 1e-5)
    
    # 3. Rolling Statistics (Computed on lag_1 to enforce time causality)
    df['rolling_mean_4'] = df.groupby('StockCode')['lag_1'].transform(lambda x: x.rolling(4).mean())
    df['rolling_std_4']  = df.groupby('StockCode')['lag_1'].transform(lambda x: x.rolling(4).std())
    df['rolling_mean_8'] = df.groupby('StockCode')['lag_1'].transform(lambda x: x.rolling(8).mean())
    
    # 4. Calendar & Seasonal Features
    df['month'] = df['Week_Start'].dt.month
    df['quarter'] = df['Week_Start'].dt.quarter
    df['week_of_year'] = df['Week_Start'].dt.isocalendar().week.astype(int)
    
    return df

if __name__ == "__main__":
    input_path = 'data/processed/weekly_sku_demand.csv'
    output_path = 'data/processed/weekly_sku_features.csv'
    
    print("--- Step 1: Reading Weekly SKU Demand Data ---")
    weekly_data = pd.read_csv(input_path)
    
    print("--- Step 2: Generating Leakage-Free Feature Set ---")
    featured_df = generate_demand_features(weekly_data)
    
    # Drop initial NaN rows created by 8-week rolling windows
    clean_featured_df = featured_df.dropna().reset_index(drop=True)
    
    # Save output for model training
    clean_featured_df.to_csv(output_path, index=False)
    
    print(f"\nFeature engineering complete. Saved to: {output_path}")
    print(f"Total Processed Rows: {len(clean_featured_df):,}")
    print("\nFeatures Generated:")
    print(list(clean_featured_df.columns))