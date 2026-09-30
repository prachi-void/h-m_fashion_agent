import os
import pandas as pd
import json
from models.style_forecaster import StyleForecaster

def tool_predict_top_styles(data_dir, season_filter=None, top_n=3):
    """
    MCP-compatible tool to run forecasting model on H&M transaction data.
    """
    forecaster = StyleForecaster(data_dir)
    top_df, full_df = forecaster.predict_top_styles(season_filter=season_filter, top_n=top_n)
    
    top_list = top_df.to_dict(orient='records')
    return {
        "status": "success",
        "season_filter": season_filter or "All-Season Overall",
        "top_styles": top_list,
        "total_styles_analyzed": len(full_df)
    }

def tool_audit_stock_limitations(data_dir):
    """
    MCP-compatible tool to analyze inventory distortion, stockout censoring, and markdown noise.
    """
    tx_df = pd.read_csv(os.path.join(data_dir, "transactions_train.csv"))
    
    # Calculate price dispersion per article to detect markdown discounting activity
    price_stats = tx_df.groupby('article_id')['price'].agg(['min', 'max', 'mean', 'std', 'count']).reset_index()
    price_stats['markdown_flag'] = (price_stats['max'] - price_stats['min']) > (0.2 * price_stats['max'])
    
    discounted_articles = int(price_stats['markdown_flag'].sum())
    total_articles = len(price_stats)
    
    audit_findings = {
        "limitation_summary": "Dataset lacks stock-on-hand, lead times, and out-of-stock timestamps.",
        "key_impacts": [
            {
                "issue": "Stockout Censoring",
                "effect": "Fast-selling winner styles suffer prematurely depleted inventory. Observed transaction drops are misinterpreted as declining popularity rather than stockout.",
                "mitigation": "Style aggregation across colorways and momentum velocity weighting over 12-week windows."
            },
            {
                "issue": "Markdown Volume Inflation",
                "effect": "Slow-moving items experiencing end-of-season price cuts show artificial sales volume spikes.",
                "mitigation": "Filtering transaction velocity by price variance stability."
            }
        ],
        "discounted_articles_ratio": f"{discounted_articles} / {total_articles} ({round(discounted_articles/total_articles*100, 1)}%)"
    }
    return audit_findings

def tool_extract_style_dna(style_dict):
    """
    Extract aesthetic attributes and structural DNA from winning style metadata.
    """
    return {
        "rank": style_dict.get("rank"),
        "garment_group": style_dict.get("garment_group"),
        "product_type": style_dict.get("product_type"),
        "graphical_appearance": style_dict.get("graphical_appearance"),
        "colour_group": style_dict.get("colour_group"),
        "recent_units": style_dict.get("recent_units"),
        "acceleration_pct": style_dict.get("acceleration_pct"),
        "sample_articles": style_dict.get("sample_articles"),
        "original_description": style_dict.get("detail_desc"),
        "style_dna_summary": f"Rank #{style_dict.get('rank')}: {style_dict.get('colour_group')} {style_dict.get('graphical_appearance')} {style_dict.get('product_type')} ({style_dict.get('garment_group')})"
    }

def tool_generate_concept_prompt(style_dna, target_season="Next Season", innovation_theme="Elevated Modern Minimalist"):
    """
    Generates a high-potency prompt for Generative AI Image creation,
    carrying forward core winning qualities while introducing genuine design changes.
    """
    g_group = style_dna.get("garment_group")
    p_type = style_dna.get("product_type")
    color = style_dna.get("colour_group")
    desc = style_dna.get("original_description")
    
    if "Blazer" in p_type or "Outerwear" in g_group:
        concept_name = "The Sculptural Asymmetrical Tailored Blazer"
        prompt = (
            f"A high-end editorial product fashion photograph of a next-season women's tailored outerwear concept. "
            f"Inspired by {color} {p_type} ({desc}). "
            f"Key modifications: Asymmetrical architectural wrap front, elevated Italian double-face wool blend, "
            f"sculpted waist line, polished matte horn hardware, in a contemporary refined {target_season} palette. "
            f"Clean studio lighting, luxury lookbook aesthetic, high resolution, photorealistic studio shot."
        )
        changes = "Architectural wrap closure, sculpted waist, upgraded double-face wool-blend fabric, metallic horn hardware."
    elif "Trousers" in p_type or "Lower" in g_group:
        concept_name = "The Fluid Origami Pleated Wide-Leg Trouser"
        prompt = (
            f"A luxury fashion studio product shot of a next-season wide-leg trouser concept. "
            f"Inspired by classic {color} {p_type}. "
            f"Key modifications: Deep origami front pleating, fluid Japanese viscose-linen blend drape, "
            f"extended high-waist waistband with subtle side buckle hardware. "
            f"Soft minimalist studio lighting, pristine detail, editorial lookbook photo."
        )
        changes = "Origami twin front pleating, extended tab waistband with brushed metal buckle, fluid viscose-linen blend."
    elif "Knitwear" in g_group or "Sweater" in p_type:
        concept_name = "The Architectural Ribbed Funnel Neck Knit"
        prompt = (
            f"A luxury editorial product photograph of a modern next-season knitwear concept. "
            f"Inspired by {color} chunky rib sweater. "
            f"Key modifications: Sculpted funnel neckline, variable diagonal rib stitching, "
            f"ethically-sourced alpaca-merino yarn blend with subtle tactile texture in a warm cream palette. "
            f"Studio photography, ultra high detail, high fashion lookbook."
        )
        changes = "Sculpted funnel collar, multi-directional rib placement, premium alpaca-merino blend yarn."
    else:
        concept_name = f"Elevated Next-Season {p_type} Concept"
        prompt = (
            f"A luxury fashion lookbook studio product photograph of a novel next-season {p_type} concept. "
            f"Carrying forward {color} aesthetic with upgraded luxury draping, refined hardware, and modern silhouette. "
            f"Photorealistic 8k, soft studio backdrop."
        )
        changes = "Modernized silhouette, premium material upgrade, custom hardware detailing."
        
    return {
        "concept_name": concept_name,
        "prompt": prompt,
        "design_changes": changes,
        "carried_forward_dna": f"{color} tone, {p_type} archetype, {desc}"
    }
