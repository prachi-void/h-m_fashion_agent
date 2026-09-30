import json
from mcp_tools.fashion_tools import tool_predict_top_styles

class TrendForecasterAgent:
    """
    Specialist Sub-Agent responsible for data aggregation, time-series feature engineering,
    and style winner forecasting.
    """
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.name = "TrendForecasterAgent"
        
    def execute_forecasting(self, season_filter=None, top_n=3):
        print(f"[{self.name}] Running multi-horizon style forecasting engine (Season: {season_filter or 'Overall'})...")
        res = tool_predict_top_styles(self.data_dir, season_filter=season_filter, top_n=top_n)
        print(f"[{self.name}] Identified Top {len(res['top_styles'])} Winning Styles successfully.")
        return res
