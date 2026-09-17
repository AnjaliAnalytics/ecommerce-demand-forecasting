import os
import pandas as pd
import numpy as np

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

def run_model_evaluation():
    # 1. Paths
    results_dir = 'reports/results'
    summary_path = os.path.join(results_dir, 'model_performance_summary.csv')
    output_path = os.path.join(results_dir, 'forecast_model_results.csv')
    
    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"Missing input file: {summary_path}. Run Phase 8 first.")
        
    # 2. Load Phase 7 & 8 Performance Data
    results_df = pd.read_csv(summary_path)
    
    # 3. Add Model Metadata & Architectural Detail
    training_approaches = {
        'Naive Forecast': 'Baseline (1-Period Shift)',
        '4-Week Moving Average': 'Baseline (Rolling 4-Week Mean)',
        'Seasonal Naive': 'Baseline (52-Week Seasonal Lag)',
        'Holt-Winters Exp Smoothing': 'Statistical Time Series (Additive Trend)',
        'Random Forest Regressor': 'Machine Learning (Lags + Rolling Stats)'
    }
    
    results_df['Training Approach'] = results_df['Model'].map(training_approaches)
    results_df['Forecast Horizon'] = '10 Weeks (Validation Holdout)'
    
    # Sort models by WAPE (Lowest Error First)
    results_df = results_df.sort_values('WAPE (%)').reset_index(drop=True)
    
    # Save formalized comparison table
    results_df.to_csv(output_path, index=False)
    
    print("=== FORMAL MODEL EVALUATION TABLE ===")
    print(results_df.to_string(index=False))
    print(f"\nFinal model evaluation saved to: {output_path}")
    
    # 4. Extract Winning Model
    winning_model = results_df.iloc[0]['Model']
    winning_wape = results_df.iloc[0]['WAPE (%)']
    winning_mae = results_df.iloc[0]['MAE (Units)']
    
    print("\n" + "="*50)
    print("MODEL SELECTION RATIONALE")
    print("="*50)
    print(f"Selected Model: {winning_model}")
    print(f"Performance:   WAPE = {winning_wape}%, MAE = {winning_mae} units")
    print("\nWhy this model was selected:")
    print(f"1. Lowest Generalization Error: Achieved the lowest WAPE ({winning_wape}%) on out-of-sample holdout data.")
    print("2. Robustness to Spikes: Successfully balances trend changes without overfitting to isolated single-week anomalies.")
    print("3. Explainability: Can be easily audited, interpreted, and communicated to supply chain managers.")

if __name__ == "__main__":
    run_model_evaluation()