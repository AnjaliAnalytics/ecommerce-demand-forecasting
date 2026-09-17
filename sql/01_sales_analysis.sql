-- Query 1: Executive Key Performance Indicators (KPIs)
-- Business Question: What are our total net revenue, total net units sold, total orders, and unique active products?
SELECT 
    COUNT(DISTINCT Invoice) AS total_orders,
    COUNT(DISTINCT StockCode) AS total_unique_products,
    SUM(Net_Quantity) AS total_units_sold,
    ROUND(SUM(Line_Revenue), 2) AS total_net_revenue
FROM sales;

-- Query 2: Monthly Sales & Unit Revenue Trend
-- Business Question: How do revenue and order volumes fluctuate month over month?
SELECT 
    STRFTIME('%Y-%m', InvoiceDate) AS sales_month,
    COUNT(DISTINCT Invoice) AS monthly_orders,
    SUM(Net_Quantity) AS monthly_units,
    ROUND(SUM(Line_Revenue), 2) AS monthly_revenue
FROM sales
GROUP BY sales_month
ORDER BY sales_month;

-- Query 3: Month-over-Month Revenue Growth Percentage (Window Function)
-- Business Question: What is our MoM revenue growth rate?
WITH MonthlyRevenue AS (
    SELECT 
        STRFTIME('%Y-%m', InvoiceDate) AS sales_month,
        ROUND(SUM(Line_Revenue), 2) AS net_revenue
    FROM sales
    GROUP BY sales_month
)
SELECT 
    sales_month,
    net_revenue,
    LAG(net_revenue, 1) OVER (ORDER BY sales_month) AS previous_month_revenue,
    ROUND(
        ((net_revenue - LAG(net_revenue, 1) OVER (ORDER BY sales_month)) / 
        LAG(net_revenue, 1) OVER (ORDER BY sales_month)) * 100, 2
    ) AS mom_growth_percentage
FROM MonthlyRevenue;

-- Query 4: Cumulative / Running Total Revenue
-- Business Question: How does our cumulative revenue build up over time?
WITH MonthlyRevenue AS (
    SELECT 
        STRFTIME('%Y-%m', InvoiceDate) AS sales_month,
        ROUND(SUM(Line_Revenue), 2) AS net_revenue
    FROM sales
    GROUP BY sales_month
)
SELECT 
    sales_month,
    net_revenue,
    ROUND(SUM(net_revenue) OVER (ORDER BY sales_month), 2) AS running_total_revenue
FROM MonthlyRevenue;

-- Query 5: Average Order Value (AOV) Distribution
-- Business Question: What is the average dollar spend per unique transaction?
WITH OrderTotals AS (
    SELECT 
        Invoice,
        ROUND(SUM(Line_Revenue), 2) AS order_value
    FROM sales
    GROUP BY Invoice
)
SELECT 
    ROUND(AVG(order_value), 2) AS average_order_value,
    ROUND(MIN(order_value), 2) AS min_order_value,
    ROUND(MAX(order_value), 2) AS max_order_value
FROM OrderTotals
WHERE order_value > 0;

-- Query 6: Sales Performance by Country
-- Business Question: Which geographic regions generate the highest sales volume?
SELECT 
    Country,
    COUNT(DISTINCT Invoice) AS total_orders,
    SUM(Net_Quantity) AS total_units,
    ROUND(SUM(Line_Revenue), 2) AS total_revenue,
    ROUND((SUM(Line_Revenue) / (SELECT SUM(Line_Revenue) FROM sales)) * 100, 2) AS revenue_share_pct
FROM sales
GROUP BY Country
ORDER BY total_revenue DESC
LIMIT 10;