AI-Driven E-Commerce Demand Forecasting & Inventory OptimizationAn end-to-end, enterprise-grade supply chain intelligence system that combines classical machine learning, statistical inventory decision frameworks, a 6-page interactive Power BI dashboard, an automated Gemini GenAI briefing engine, and an interactive Streamlit portfolio app.Executive Summary & Business ProblemE-commerce businesses face significant financial risks due to stockouts (lost revenue and degraded customer lifetime value) and overstocking (capital tied up in excess holding costs). Traditional reactive inventory management relies on static reorder thresholds that fail to capture demand volatility and seasonal patterns.This project addresses this challenge by establishing a data-driven pipeline to forecast demand, quantify safety stock, automate dynamic reorder thresholds, and surface financial exposure metrics across a multi-SKU retail portfolio.Key Project ResultsForecast Accuracy: The 4-Week Moving Average model achieved optimal generalizability on a 10-week out-of-sample holdout test with a WAPE of 50.34% and an MAE of 325.50 units, successfully filtering out transient noise without overfitting.Service Level Guarantee: Established dynamic Safety Stock buffers targeting a 95% Cycle Service Level (CSL) using Z-score statistics ($Z = 1.65$).Working Capital Intelligence: Segmented inventory into actionable risk categories (REORDER NOW, MONITOR, SUFFICIENT STOCK, POTENTIAL OVERSTOCK) to prioritize immediate capital allocation toward high-risk stockout SKUs while flagging excess working capital tied up in overstock.End-to-End ArchitectureRaw Retail Data (CSV/Excel)
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
       ├──► GenAI Executive Briefing Engine (Google Gemini API - `gemini-3.6-flash`)
       │
       └──► Interactive Streamlit Portfolio Web App (`src/app.py`)
Tech Stack & ToolingDomainTechnologies UsedData Processing & MLPython, Pandas, NumPy, Scikit-LearnDatabase & AnalyticsSQLite, SQL (Aggregations, Joins, Windowing)Business IntelligencePower BI Desktop, DAX, Star Schema Data ModelingGenerative AIGoogle GenAI SDK (gemini-3.6-flash)Web UI ApplicationStreamlit, MatplotlibVersion Control & CI/CDGit, GitHubInventory Decision Logic & FormulasSafety Stock Calculation:$$\text{Safety Stock} = Z \times \sigma_d \times \sqrt{L}$$where $Z = 1.65$ (95% CSL), $\sigma_d$ is the standard deviation of weekly demand, and $L$ is lead time in weeks.Dynamic Reorder Point (ROP):$$\text{Reorder Point} = \text{Forecasted Demand during Lead Time} + \text{Safety Stock}$$Action Framework & Classification:REORDER NOW: $\text{Inventory Position} \le \text{Reorder Point}$MONITOR: $\text{Reorder Point} < \text{Inventory Position} \le 1.5 \times \text{Reorder Point}$SUFFICIENT STOCK: $1.5 \times \text{Reorder Point} < \text{Inventory Position} \le 2.5 \times \text{Reorder Point}$POTENTIAL OVERSTOCK: $\text{Inventory Position} > 2.5 \times \text{Reorder Point}$Note on Inventory Assumptions: Inventory positions and lead times are generated using deterministic empirical distributions based on historical transactional lead-time variances.Power BI Executive Dashboard SuiteThe 6-page production report (dashboard/powerbi/) features a Star Schema (dim_product, dim_date, dim_risk_category, fact_inventory_risk) with dynamic measures:Page 1: Executive Overview: High-level KPIs, total working capital exposure, stockout risk distribution, and prioritized action cards.Page 2: Sales & Demand Trends: Historical demand volume trends, seasonal decomposition, and chronological monthly performance.Page 3: Demand Forecast: Model evaluation metrics (WAPE %, MAE), model comparison benchmarks, and 10-week out-of-sample holdout visualizations.Page 4: Inventory Intelligence: Reorder Point vs. Inventory Position scatter plots and capital required by SKU.Page 5: Product Prioritization: Action Matrix Table with conditional formatting for immediate procurement workflows.Page 6: AI Business Insights: Native Key Influencers visual paired with structured GenAI executive recommendation summaries.GenAI Integration & GovernanceThe Generative AI layer (src/genai_insights.py) utilizes the Google Gemini API (gemini-3.6-flash) to convert pre-computed quantitative risk outputs into C-suite briefings.Strict Context Boundary: Only aggregated metrics and calculated risk categories are passed to the prompt payload.Zero Numerical Invention: System instructions strictly prohibit the LLM from hallucinating numbers or making unsupported causal claims.Fail-Safe Fallback: The core pipeline, Power BI dashboards, and Streamlit application operate uninterrupted if no API key is provided.Project Repository StructurePlaintextecommerce-demand-forecasting/
├── dashboard/
│   └── powerbi/              # Star Schema CSV exports & .pbix configurations
├── data/
│   └── processed/            # Aggregated metrics (business_impact_summary.csv)
├── docs/
│   └── genai_architecture.md # GenAI governance & safety documentation
├── reports/
│   └── genai_executive_briefing.md # AI-generated executive briefing
├── src/
│   ├── app.py                # Interactive Streamlit application
│   ├── audit_system.py       # Automated end-to-end audit script
│   └── genai_insights.py     # Gemini API integration script
├── .gitignore
├── README.md
└── requirements.txt          # Dependencies list
How to Reproduce & Run Locally1. Clone the RepositoryBashgit clone https://github.com/AnjaliAnalytics/ecommerce-demand-forecasting.git
cd ecommerce-demand-forecasting
2. Set Up Virtual Environment & Install DependenciesBashpython -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
3. Run the Automated System AuditBashpython src/audit_system.py
4. Set Gemini API Key & Generate AI Insights (Optional)Bash$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
python src/genai_insights.py
5. Launch the Streamlit Interactive ApplicationBashstreamlit run src/app.py
Limitations & Future EnhancementsLead Time Variability: Current models utilize standard lead-time variance estimates. Future iterations can integrate real-time supplier shipping telemetry.Advanced ML Architectures: Future work includes benchmarking XGBoost and Prophet models against the 4-week moving average baseline.Automated Procurement API: Connecting reorder triggers directly to ERP endpoints (e.g., SAP, NetSuite) for automated purchase order drafting.