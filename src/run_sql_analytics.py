import sqlite3
import pandas as pd
import os

# Paths
processed_csv = 'data/processed/cleaned_online_retail.csv'
db_path = 'data/processed/ecommerce.db'

print("--- Step 1: Loading Cleaned Data into SQLite Database ---")
# Load cleaned dataset
df = pd.read_csv(processed_csv, low_memory=False)

# Connect to SQLite (creates database file if it doesn't exist)
conn = sqlite3.connect(db_path)

# Write dataframe into 'sales' table inside SQLite database
df.to_sql('sales', conn, if_exists='replace', index=False)
print(f"Loaded {len(df):,} rows into SQLite table 'sales'.\n")

print("--- Step 2: Executing Key Analytics Queries ---")

# Query 1 Execution
q1 = """
SELECT 
    COUNT(DISTINCT Invoice) AS total_orders,
    COUNT(DISTINCT StockCode) AS total_unique_products,
    SUM(Net_Quantity) AS total_units_sold,
    ROUND(SUM(Line_Revenue), 2) AS total_net_revenue
FROM sales;
"""
print("Query 1 Output (Executive KPIs):")
print(pd.read_sql_query(q1, conn))
print("\n" + "="*50 + "\n")

# Query 7 Execution
q7 = """
WITH ProductRevenue AS (
    SELECT 
        StockCode,
        Description,
        SUM(Net_Quantity) AS units_sold,
        ROUND(SUM(Line_Revenue), 2) AS total_revenue
    FROM sales
    GROUP BY StockCode, Description
)
SELECT 
    DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank,
    StockCode,
    Description,
    units_sold,
    total_revenue
FROM ProductRevenue
LIMIT 5;
"""
print("Query 7 Output (Top 5 Products by Revenue):")
print(pd.read_sql_query(q7, conn))

conn.close()
print("\nSQL Execution Completed successfully.")