import os
import pandas as pd
import json
from agents.forecaster import TrendForecasterAgent
from agents.stock_auditor import StockAuditAgent
from agents.designer import DesignSynthesizerAgent

class FashionOrchestratorAgent:
    """
    Master Orchestration Agent coordinating specialized sub-agents:
    - TrendForecasterAgent
    - StockAuditAgent
    - DesignSynthesizerAgent
    """
    def __init__(self, data_dir, output_dir):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.name = "FashionOrchestratorAgent"
        
        self.forecaster = TrendForecasterAgent(data_dir)
        self.auditor = StockAuditAgent(data_dir)
        self.designer = DesignSynthesizerAgent()
        
    def run_full_pipeline(self):
        print("================================================================================")
        print(f"[{self.name}] STARTING FASHION FORECASTING & GENERATIVE AI WORKFLOW")
        print("================================================================================")
        
        # 1. Predict Overall Top 3 Style Winners
        forecast_res = self.forecaster.execute_forecasting(top_n=3)
        top_styles = forecast_res["top_styles"]
        
        # 2. Audit Inventory Limitations & Stockouts
        audit_res = self.auditor.execute_audit()
        
        # 3. Synthesize Generative Concepts
        concept_briefs = self.designer.synthesize_concepts(top_styles, target_season="Next Season (Autumn/Winter)")
        
        # 4. Seasonal Split Analysis (Bonus)
        print(f"[{self.name}] Executing Seasonal Decomposition (Spring, Summer, Autumn, Winter)...")
        seasonal_results = {}
        for season in ["Spring", "Summer", "Autumn", "Winter"]:
            s_res = self.forecaster.execute_forecasting(season_filter=season, top_n=1)
            seasonal_results[season] = s_res["top_styles"][0] if s_res["top_styles"] else {}
            
        # 5. Export Results
        winner_df = pd.DataFrame(top_styles)
        winner_df.to_csv(os.path.join(self.output_dir, "winner_styles.csv"), index=False)
        
        seasonal_rows = []
        for s_name, s_style in seasonal_results.items():
            seasonal_rows.append({
                "Season": s_name,
                "Top_Style_Key": s_style.get("style_key"),
                "Garment_Group": s_style.get("garment_group"),
                "Product_Type": s_style.get("product_type"),
                "Colour_Group": s_style.get("colour_group"),
                "Recent_Units": s_style.get("recent_units"),
                "Acceleration_Pct": s_style.get("acceleration_pct")
            })
        seasonal_df = pd.DataFrame(seasonal_rows)
        seasonal_df.to_csv(os.path.join(self.output_dir, "seasonal_winners.csv"), index=False)
        
        print("\n================================================================================")
        print(f"[{self.name}] WORKFLOW COMPLETED SUCCESSFULLY.")
        print(f"Outputs exported to:\n- {os.path.join(self.output_dir, 'winner_styles.csv')}\n- {os.path.join(self.output_dir, 'seasonal_winners.csv')}")
        print("================================================================================\n")
        
        return {
            "top_styles": top_styles,
            "audit": audit_res,
            "concepts": concept_briefs,
            "seasonal_winners": seasonal_results
        }
