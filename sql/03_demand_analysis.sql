-- Query 11: Weekly Aggregate Unit Demand
-- Business Question: What is our weekly demand timeline across all SKUs?
SELECT 
    STRFTIME('%Y-%W', InvoiceDate) AS sales_week,
    COUNT(DISTINCT Invoice) AS weekly_orders,
    SUM(Net_Quantity) AS weekly_unit_demand,
    ROUND(SUM(Line_Revenue), 2) AS weekly_revenue
FROM sales
GROUP BY sales_week
ORDER BY sales_week;

-- Query 12: Weekly Rolling Average Demand per Product (Window Functions)
-- Business Question: What is the 4-week moving average demand for top products?
WITH WeeklyProductDemand AS (
    SELECT 
        StockCode,
        STRFTIME('%Y-%W', InvoiceDate) AS sales_week,
        SUM(Net_Quantity) AS weekly_units
    FROM sales
    GROUP BY StockCode, sales_week
)
SELECT 
    StockCode,
    sales_week,
    weekly_units,
    ROUND(AVG(weekly_units) OVER (
        PARTITION BY StockCode 
        ORDER BY sales_week 
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_4wk_avg_demand
FROM WeeklyProductDemand;

-- Query 13: Customer Repeat Purchase Rate
-- Business Question: How many customers are repeat buyers versus one-time buyers?
WITH CustomerOrders AS (
    SELECT 
        Customer_ID,
        COUNT(DISTINCT Invoice) AS order_count
    FROM sales
    WHERE Customer_ID != -1
    GROUP BY Customer_ID
)
SELECT 
    CASE 
        WHEN order_count = 1 THEN 'One-Time Buyer'
        WHEN order_count BETWEEN 2 AND 5 THEN 'Repeat Buyer (2-5)'
        ELSE 'Frequent Buyer (>5)'
    END AS customer_segment,
    COUNT(Customer_ID) AS customer_count
FROM CustomerOrders
GROUP BY customer_segment;

-- Query 14: Day of Week Sales Distribution
-- Business Question: On which days of the week is buying velocity highest?
SELECT 
    CASE STRFTIME('%w', InvoiceDate)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END AS day_of_week,
    COUNT(DISTINCT Invoice) AS total_orders,
    SUM(Net_Quantity) AS total_units_sold
FROM sales
GROUP BY STRFTIME('%w', InvoiceDate)
ORDER BY STRFTIME('%w', InvoiceDate);