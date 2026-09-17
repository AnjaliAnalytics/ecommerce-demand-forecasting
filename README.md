# AI-Driven E-Commerce Demand Forecasting & Inventory Optimization

> An enterprise-grade supply chain solution optimizing working capital, automating reorder points, and eliminating stockout risks using Python ML, Power BI, Google Gemini API, and Streamlit.

---

##  Executive Summary

E-commerce businesses face multi-million dollar trade-offs: stockouts lead to lost revenue and customer churn, while overstocking ties up critical working capital in holding costs. Traditional static reorder thresholds fail to adapt to demand volatility.

This project addresses these challenges by establishing an automated, data-driven pipeline that forecasts demand, quantifies safety stock buffers, automates dynamic reorder points, and surfaces real-time financial exposure across a multi-SKU portfolio.

---

##  Key Results & Impact

* **Optimal Forecast Generalizability:** Selected a **4-Week Moving Average** model evaluated on a 10-week out-of-sample holdout test (**WAPE = 50.34%**, **MAE = 325.50 units**), filtering out volatile demand spikes without overfitting.
* **Service Level Guarantee:** Automated dynamic Safety Stock buffers targeting a **95% Cycle Service Level (CSL)** using Z-score statistics ($Z = 1.65$).
* **Working Capital Prioritization:** Categorized inventory into clear risk tiers (`REORDER NOW`, `MONITOR`, `SUFFICIENT STOCK`, `POTENTIAL OVERSTOCK`) to align procurement budgets directly with critical SKUs.

---

##  Tech Stack & Architecture

```text
Raw Retail Data (CSV/Excel)
       │
       ▼
Data Cleaning & Feature Engineering (Pandas / NumPy)
       │
       ├──► Relational Data Warehouse (SQLite)
       │
       ├──► Time-Series ML Demand Forecasting (4-Week Moving Average Baseline)
       │
       ├──► Statistical Safety Stock & Dynamic Reorder Point Logic (95% CSL)
       │
       ├──► Star Schema Data Model Export (Dim/Fact CSVs)
       │
       ├──► Power BI Executive Suite (6 Interactive Pages + Custom DAX)
       │
       ├──► GenAI Executive Briefing Engine (Google Gemini API - gemini-3.6-flash)
       │
       └──► Interactive Streamlit Portfolio Web App (src/app.py)

       DomainTechnologies UsedData Processing & MLPython, Pandas, NumPy, Scikit-LearnDatabase & AnalyticsSQLite, SQL (Aggregations, Joins, Windowing)Business IntelligencePower BI Desktop, DAX, Star Schema Data ModelingGenerative AIGoogle GenAI SDK (gemini-3.6-flash)Web UI ApplicationStreamlit, MatplotlibVersion ControlGit, GitHub Inventory Decision FrameworkSafety Stock (SS): $Z \times \sigma_d \times \sqrt{L}$ (where $Z = 1.65$ for 95% CSL)Reorder Point (ROP): $\text{Forecasted Demand During Lead Time} + \text{Safety Stock}$Action Rules:REORDER NOW: Inventory Position $\le$ ROPMONITOR: ROP $<$ Inventory Position $\le 1.5 \times$ ROPSUFFICIENT STOCK: $1.5 \times \text{ROP} < \text{Inventory Position} \le 2.5 \times \text{ROP}$POTENTIAL OVERSTOCK: Inventory Position $> 2.5 \times$ ROPNote on Data Assumptions: Inventory positions and lead times are generated using deterministic empirical distributions derived from historical order variances. Deliverables & Interactive Interfaces1. Power BI Executive Dashboard (dashboard/powerbi/)Built on a production Star Schema (dim_product, dim_date, dim_risk_category, fact_inventory_risk) with custom DAX measures across 6 tailored pages:Executive Overview: High-level inventory valuation, stockout risk distribution, and critical KPIs.Sales & Demand Trends: Historical volume trends and chronological monthly performance.Demand Forecast: Model benchmarking metrics (WAPE, MAE) and 10-week holdout evaluation.Inventory Intelligence: Reorder Point vs. Inventory Position scatter matrix.Product Prioritization: Full-width Matrix with color-coded risk action tiers.AI Business Insights: Native Key Influencers visual paired with dynamic GenAI executive summaries.2. GenAI Interpretation Engine (src/genai_insights.py)Utilizes Google's gemini-3.6-flash model with strict temperature constraints (0.2) to summarize inventory risks without numerical hallucination.Fail-Safe Architecture: The pipeline and dashboards function smoothly even if the LLM API is unavailable.3. Streamlit Portfolio App (src/app.py)A lightweight, fast UI allowing recruiters and stakeholders to inspect individual SKUs, historical demand graphs, safety stock levels, and AI recommendations interactively.

       📂 Repository Structure

ecommerce-demand-forecasting/
├── dashboard/
│   └── powerbi/              # Star Schema CSV exports & .pbix configurations
├── data/
│   └── processed/            # Processed outputs (business_impact_summary.csv)
├── docs/
│   └── genai_architecture.md # GenAI governance & safety guidelines
├── reports/
│   └── genai_executive_briefing.md # Generated C-suite AI briefing
├── src/
│   ├── app.py                # Interactive Streamlit Web Application
│   ├── audit_system.py       # Automated end-to-end audit verification script
│   └── genai_insights.py     # Gemini API integration script
├── .gitignore
├── README.md
└── requirements.txt          # Python dependencies

1. Clone & Set Up Environment
Bash
git clone [https://github.com/AnjaliAnalytics/ecommerce-demand-forecasting.git](https://github.com/AnjaliAnalytics/ecommerce-demand-forecasting.git)
cd ecommerce-demand-forecasting

python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
2. Run Automated System Audit
Bash
python src/audit_system.py
3. Generate GenAI Executive Briefing (Optional)
Bash
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
python src/genai_insights.py
4. Launch Streamlit Web Application
Bash
streamlit run src/app.py
 Future Enhancements
Supplier Integration: Connect dynamic lead-time distributions directly to real-time vendor shipping APIs.

Advanced Architectures: Benchmark gradient boosting (XGBoost) and Prophet models against the moving average baseline.

Automated ERP Reordering: Push REORDER NOW flags automatically to procurement platforms via Webhooks.
