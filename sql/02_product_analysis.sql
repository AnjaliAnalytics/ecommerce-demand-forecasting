-- Query 7: Top 10 Products by Revenue (Window Ranking)
-- Business Question: Which individual products generate the most revenue?
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
LIMIT 10;

-- Query 8: Top 10 Products by Net Volume (Units Sold)
-- Business Question: Which items move the fastest in terms of physical warehouse units?
SELECT 
    StockCode,
    Description,
    SUM(Net_Quantity) AS total_units_sold,
    ROUND(SUM(Line_Revenue), 2) AS total_revenue
FROM sales
GROUP BY StockCode, Description
ORDER BY total_units_sold DESC
LIMIT 10;

-- Query 9: Product Pareto Analysis (80/20 Revenue Contribution)
-- Business Question: What percentage of total revenue does each product contribute cumulatively?
WITH ProductTotals AS (
    SELECT 
        StockCode,
        ROUND(SUM(Line_Revenue), 2) AS product_revenue
    FROM sales
    GROUP BY StockCode
),
RankedProducts AS (
    SELECT 
        StockCode,
        product_revenue,
        SUM(product_revenue) OVER (ORDER BY product_revenue DESC) AS cumulative_revenue,
        SUM(product_revenue) OVER () AS global_revenue
    FROM ProductTotals
)
SELECT 
    StockCode,
    product_revenue,
    ROUND((cumulative_revenue / global_revenue) * 100, 2) AS cumulative_revenue_pct
FROM RankedProducts
ORDER BY product_revenue DESC;

-- Query 10: Slow-Moving / Low-Demand Products
-- Business Question: Which products have minimal total unit sales and risk becoming dead stock?
SELECT 
    StockCode,
    Description,
    SUM(Net_Quantity) AS total_units_sold,
    COUNT(DISTINCT Invoice) AS order_count
FROM sales
GROUP BY StockCode, Description
HAVING total_units_sold > 0 AND total_units_sold < 10
ORDER BY total_units_sold ASC
LIMIT 15;