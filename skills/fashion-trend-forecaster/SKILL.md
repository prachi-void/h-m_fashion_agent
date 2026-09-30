---
name: fashion-trend-forecaster
description: Analytical framework for fashion style performance prediction, inventory bias correction, and generative product concept synthesis using H&M transactional and article data.
---

# Fashion Trend Forecaster & Generative Design Skill

This skill provides an agentic framework for fashion retail intelligence: forecasting style winners from transactional data, accounting for inventory limitations, and synthesizing next-season generative product concepts.

## Core Capabilities

1. **Style Aggregation & Attribute Clustering**:
   - Groups individual SKUs (`article_id`) into macro-styles using `garment_group_name`, `product_type_name`, `graphical_appearance_name`, and `colour_group_name`.
   - Prevents SKU-level demand noise and isolates aesthetic drivers.

2. **Style Performance & Momentum Scoring**:
   - Computes multi-horizon metric: Recent Volume ($V$), Acceleration Velocity ($A$), Revenue ($R$), and Exponential Momentum ($M$).
   - Predicts top 3 styles performing strongly for next season.

3. **Inventory & Stockout Censoring Audit**:
   - Analyzes transactions without stock-on-hand data.
   - Identifies stockout censoring (under-counted demand due to zero inventory) and markdown distortion (artificially inflated volume from end-of-season discounts).

4. **Generative Product Synthesis**:
   - Deconstructs winning style attributes into a "Style DNA".
   - Applies design transformation rules (silhouette, material, color, detailing) to generate novel, non-copied Next-Season concepts.
   - Synthesizes composite multi-concept lookbooks.

## Usage Protocol

- **Step 1**: Run `TrendForecasterAgent` to aggregate styles and run forecasting model.
- **Step 2**: Run `StockAuditAgent` to adjust rankings for inventory censoring and pricing dynamics.
- **Step 3**: Run `DesignSynthesizerAgent` to extract Style DNA and author generative AI design briefs.
- **Step 4**: Run `ConceptGeneratorAgent` to generate high-fidelity product concept images and compose the final multi-panel image.
- **Step 5**: Run `SeasonalView` to evaluate seasonal shift and generate season-specific variants.
