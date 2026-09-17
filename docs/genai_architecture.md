# GenAI Architecture & Governance

## Role of GenAI in Project
- **Deterministic Analytics (Python/DAX):** All time-series forecasting, safety stock formulas, reorder points, and financial risk amounts are calculated mathematically by Python and DAX.
- **Generative Interpretation (Gemini API):** Converts calculated numeric structured summaries into clear, C-suite narrative briefings.

## Safeguards & Hallucination Prevention
1. **Strict Context Boundary:** Only aggregated metric tables are passed to the prompt payload.
2. **Zero-Invention Constraint:** System instructions prohibit the LLM from generating unprovided numbers or speculative causal claims.
3. **Low Temperature:** Set to `0.2` for precise factual outputs.
4. **Graceful Fallback:** If the API key is missing or the network fails, the core pipeline (Data Models, Python Engines, and Power BI Dashboards) functions completely without interruption.