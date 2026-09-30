from mcp_tools.fashion_tools import tool_extract_style_dna, tool_generate_concept_prompt

class DesignSynthesizerAgent:
    """
    Specialist Sub-Agent responsible for deconstructing winning styles into Style DNA,
    authoring generative AI design briefs, and ensuring concept novelty without copying.
    """
    def __init__(self):
        self.name = "DesignSynthesizerAgent"
        
    def synthesize_concepts(self, top_styles, target_season="Next Season"):
        print(f"[{self.name}] Extracting Style DNA and authoring Generative Design Briefs for top {len(top_styles)} styles...")
        concepts = []
        for style in top_styles:
            dna = tool_extract_style_dna(style)
            brief = tool_generate_concept_prompt(dna, target_season=target_season)
            concepts.append({
                "style_rank": style.get("rank"),
                "style_key": style.get("style_key"),
                "dna": dna,
                "brief": brief
            })
        print(f"[{self.name}] Generative Design Briefs synthesized successfully.")
        return concepts
