# H&M Data-Driven Style Forecasting & Agentic Generative AI System

An end-to-end multi-agent AI system designed for fashion retailers to forecast next-season high-performing product styles from historical transaction data, audit inventory distortion limitations, and synthesize novel look-alike generative product concepts.

---

## Key Features

1. **Multi-Horizon Style Forecasting Engine**:
   - Aggregates article SKUs into macro-styles (`Garment Group` + `Product Type` + `Graphical Appearance` + `Color Group`).
   - Evaluates performance using a composite **Performance & Growth Score (PGS)** incorporating recent sales volume ($V_{12w}$), acceleration velocity ($A_{vel}$), and revenue contribution ($R$).

2. **Inventory & Stockout Censoring Audit**:
   - Specifically addresses the dataset limitation (absence of stock-on-hand / availability history).
   - Audits stockout censoring (demand truncation) and markdown price variance noise.

3. **Generative Product Synthesis**:
   - Extracts "Style DNA" from predicted winning styles.
   - Formulates generative AI design briefs that preserve winning aesthetic drivers while introducing meaningful structural innovations (silhouette, fabric, hardware, detailing).

4. **Multi-Agent Architecture**:
   - **`FashionOrchestratorAgent`**: Master orchestrator controlling sub-agent execution flow and export pipelines.
   - **`TrendForecasterAgent`**: Handles style aggregation and statistical/ML momentum forecasting.
   - **`StockAuditAgent`**: Audits inventory bias, stockouts, and price discounting signals.
   - **`DesignSynthesizerAgent`**: Extracts Style DNA and authors generative design briefs.
   - **`ConceptGeneratorAgent`**: Executes AI image generation and stitches composite lookbook images.

5. **Seasonal Decomposition (Bonus)**:
   - Evaluates style momentum across all 4 distinct seasons (Spring, Summer, Autumn, Winter) to track aesthetic shifts throughout the year.

---

## Repository Structure

```
hm_fashion_agent/
├── data/
│   ├── articles.csv                  # H&M article metadata
│   ├── transactions_train.csv        # Multi-year transactional history
│   └── images/                       # Reference article catalogue images
├── agents/
│   ├── orchestrator.py               # Master Orchestrator Agent
│   ├── forecaster.py                 # Specialist Trend Forecaster Sub-Agent
│   ├── stock_auditor.py              # Specialist Stock Audit Sub-Agent
│   ├── designer.py                   # Specialist Design Synthesizer Sub-Agent
│   └── concept_generator.py          # Concept Generator Sub-Agent
├── mcp_tools/
│   └── fashion_tools.py              # MCP-compatible tool wrappers
├── models/
│   └── style_forecaster.py           # Statistical/ML Style Forecasting Engine
├── skills/
│   └── fashion-trend-forecaster/
│       └── SKILL.md                  # Reusable Agent Skill definition
├── output/
│   ├── winner_styles.csv             # Top predicted style winners data
│   ├── seasonal_winners.csv          # Seasonally-decomposed style performance
│   └── final_next_season_concepts.png# Final 3-concept visual lookbook
├── scripts/
│   ├── prepare_dataset.py            # Dataset initialization script
│   └── build_final_composite_image.py# Lookbook visual composite stitcher
├── main.py                           # Application entrypoint
└── README.md                         # System documentation
```

---

## Quick Start Guide

### 1. Run the Multi-Agent System
```bash
python main.py
```

### 2. View Output Files
- **Predicted Winners Data**: `output/winner_styles.csv`
- **Seasonal Breakdown Data**: `output/seasonal_winners.csv`
- **Final Composite Image**: `output/final_next_season_concepts.png`
