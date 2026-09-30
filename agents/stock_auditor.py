from mcp_tools.fashion_tools import tool_audit_stock_limitations

class StockAuditAgent:
    """
    Specialist Sub-Agent responsible for inventory limitation auditing,
    detecting stockout censoring and price markdown volume distortions.
    """
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.name = "StockAuditAgent"
        
    def execute_audit(self):
        print(f"[{self.name}] Auditing dataset for missing inventory, stockouts, and markdown noise...")
        audit_res = tool_audit_stock_limitations(self.data_dir)
        print(f"[{self.name}] Inventory Audit complete. Identified stockout censoring & price variance impacts.")
        return audit_res
