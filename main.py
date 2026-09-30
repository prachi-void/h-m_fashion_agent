import os
import sys

# Ensure local modules can be imported
sys.path.insert(0, os.path.dirname(__file__))

from agents.orchestrator import FashionOrchestratorAgent

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "data")
    output_dir = os.path.join(base_dir, "output")
    
    orchestrator = FashionOrchestratorAgent(data_dir, output_dir)
    results = orchestrator.run_full_pipeline()
    
    print("\n--- TOP 3 PREDICTED STYLES ---")
    for s in results["top_styles"]:
        print(f"Rank #{s['rank']}: {s['style_key']} (Recent Units: {s['recent_units']}, Acceleration: {s['acceleration_pct']}%, Score: {round(s['composite_score'], 3)})")
        
    print("\n--- SEASONAL WINNERS (BONUS) ---")
    for season, s in results["seasonal_winners"].items():
        print(f"[{season}]: {s.get('style_key')} (Units: {s.get('recent_units')})")
