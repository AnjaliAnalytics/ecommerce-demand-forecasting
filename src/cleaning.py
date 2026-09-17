import pandas as pd
import numpy as np

def run_cleaning_pipeline(raw_csv_path, output_csv_path):
    """
    Reads raw Online Retail II dataset, cleans administrative anomalies, 
    standardizes features, and exports clean net demand metrics.
    """
    df = pd.read_csv(raw_csv_path, low_memory=False)
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    for col in ['StockCode', 'Description', 'Country']:
        df[col] = df[col].astype(str).str.strip()
        
    # Drop duplicates
    df = df.drop_duplicates().reset_index(drop=True)
    
    # Impute missing Customer_ID
    df['Customer_ID'] = df['Customer_ID'].fillna(-1).astype(int)
    
    # Filter non-product codes
    non_product_codes = ['POST', 'D', 'M', 'BANK CHARGES', 'PADS', 'DOT', 'CRUK']
    invalid_code_mask = (
        df['StockCode'].str.upper().isin(non_product_codes) | 
        (df['StockCode'].str.len() < 4)
    )
    df = df[~invalid_code_mask].reset_index(drop=True)
    
    # Filter invalid price
    df = df[df['Price'] > 0].reset_index(drop=True)
    
    # Flag cancellations and calculate net metrics
    df['Is_Cancelled'] = df['Invoice'].astype(str).str.startswith('C') | (df['Quantity'] < 0)
    df['Quantity_Sold'] = np.where(df['Quantity'] > 0, df['Quantity'], 0)
    df['Quantity_Returned'] = np.where(df['Quantity'] < 0, np.abs(df['Quantity']), 0)
    df['Net_Quantity'] = df['Quantity']
    df['Line_Revenue'] = df['Net_Quantity'] * df['Price']
    
    # Export
    df.to_csv(output_csv_path, index=False)
    print(f"Pipeline complete. Processed dataset saved to {output_csv_path}")
    return df

if __name__ == "__main__":
    # Updated paths relative to the root folder (D:\ecommerce-demand-forecasting)
    run_cleaning_pipeline(
        'data/raw/online_retail_II.csv',
        'data/processed/cleaned_online_retail.csv'
    )