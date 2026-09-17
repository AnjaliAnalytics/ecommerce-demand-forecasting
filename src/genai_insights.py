import os
import pandas as pd
from google import genai
from google.genai import types

def generate_executive_briefing(impact_csv_path, output_md_path):
    """
    Reads calculated inventory metrics and uses Gemini to produce 
    an executive business briefing. Fails gracefully if no API key is present.
    """
    print("--- Phase 17: GenAI Insight Generation ---")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[WARNING] GEMINI_API_KEY environment variable not found.")
        print("[FALLBACK] GenAI layer skipped. Python and Power BI modules remain 100% operational.")
        return False

    if not os.path.exists(impact_csv_path):
        print(f"[ERROR] Input file {impact_csv_path} not found.")
        return False
        
    df = pd.read_csv(impact_csv_path)
    
    high_risk = df[df['Risk_Category'] == 'HIGH STOCKOUT RISK'].head(5)
    overstock = df[df['Risk_Category'] == 'POTENTIAL OVERSTOCK'].head(5)
    
    total_val = df['Current_Stock_Value_GBP'].sum()
    reorder_val = df['Reorder_Capital_Required_GBP'].sum()
    excess_val = df['Excess_Capital_Tied_Up_GBP'].sum()
    
    prompt_payload = f"""
    You are an expert Supply Chain Director reviewing pre-calculated inventory metrics.
    
    === STRICT GROUNDING RULES ===
    1. NEVER invent or hallucinate numerical values. Use ONLY the data provided below.
    2. Explicitly distinguish factual observations from recommended strategic actions.
    3. Do NOT provide speculative or unsupported causal explanations for demand changes.
    
    === CALCULATED EXECUTIVE METRICS ===
    - Total Working Capital in Stock: £{total_val:,.2f}
    - Capital Required for Reorders: £{reorder_val:,.2f}
    - Excess Capital Tied Up in Overstock: £{excess_val:,.2f}
    
    === SAMPLE HIGH STOCKOUT RISK SKUs ===
    {high_risk[['StockCode', 'Forecast_Demand', 'Inventory_Position', 'Reorder_Point']].to_string(index=False)}
    
    === SAMPLE OVERSTOCKED SKUs ===
    {overstock[['StockCode', 'Forecast_Demand', 'Inventory_Position', 'Reorder_Point']].to_string(index=False)}
    
    === REQUIRED OUTPUT STRUCTURE ===
    Please structure your executive briefing with the following exact headers:
    1. Executive Situation Summary
    2. Inventory Risk Exposure Analysis
    3. Recommended Supply Chain Actions
    """

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt_payload,
            config=types.GenerateContentConfig(
                temperature=0.2 
            )
        )
        
        os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"[SUCCESS] Executive AI briefing generated and saved to: {output_md_path}")
        return True

    except Exception as e:
        print(f"[API ERROR] Failed to generate GenAI insights: {str(e)}")
        print("[FALLBACK] System execution uninterrupted.")
        return False

if __name__ == "__main__":
    generate_executive_briefing(
        'data/processed/business_impact_summary.csv',
        'reports/genai_executive_briefing.md'
    )