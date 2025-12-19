# FILE: alzkb_ui_controller.py
# FINAL SPECIFICATION - PHASE V

import sys
import os
# Add 'src' to pythonpath so alzkb can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
from alzkb.backend import GraphDriver, RAGEngine, VizBuilder

def main():
    st.set_page_config(layout="wide", page_title="AlzKB Discovery")

    # --- 1. INVESTIGATOR CONTROLS ---
    with st.sidebar:
        st.header("Investigation Parameters")
        
        # DECISION: Dynamic Mode Toggling (Core vs. Exploratory)
        # This switches both the Ranking Metric and the Confidence Threshold
        mode = st.radio("Evidence Scope", ["Core (Validated)", "Exploratory (Predicted)"])
        
        if mode == "Core (Validated)":
            ranking_metric = "rank_core"         # Pre-calculated on trusted subset
            min_conf = 0.85                      # Strict threshold
            pruning_strategy = "weighted_novelty" # Prioritize rare, strong signals
        else:
            ranking_metric = "rank_exploratory"
            min_conf = 0.50
            pruning_strategy = "hub_bridging"     # Allow broader connections

    # --- 2. SEARCH INTERFACE ---
    query = st.text_input("Target Entity (Gene, Phenotype, Pathology):", placeholder="e.g., TREM2")

    if query:
        # --- 3. RETRIEVAL LAYER ---
        # Decoupled Retrieval: 
        # 'context_graph' is for the LLM (Deep)
        # 'visual_graph' is for the UI (Clean)
        
        context_graph = GraphDriver.get_deep_context(query, min_conf)
        
        visual_graph = GraphDriver.get_visual_subgraph(
            query,
            context_graph, 
            limit=50, 
            strategy=pruning_strategy, 
            rank_by=ranking_metric
        )

        # --- 4. DUAL-PANE LAYOUT ---
        col_viz, col_evidence = st.columns([3, 2])

        with col_viz:
            st.subheader(f"Network Topology: {mode}")
            
            # ONCOLOGIST DIRECTIVE: BioLink Styling & Virtual Edge Flattening
            # Edges are colored by predicate, Nodes by Category
            selected_node = VizBuilder.render_interactive(
                visual_graph,
                style_profile="biolink_strict",
                flatten_reified_edges=True 
            )

        with col_evidence:
            st.subheader("Clinical Narrative")
            
            # RAG SCIENTIST DIRECTIVE: Safety Stamping
            # Generates text where every claim is suffixed with a visual badge
            # [Validated] (Green) or [Inferred] (Yellow)
            narrative = RAGEngine.generate_safe_narrative(
                query, 
                context_graph, 
                strictness=(mode=="Core (Validated)")
            )
            
            # Render HTML with click-to-highlight functionality
            st.markdown(narrative.html_content, unsafe_allow_html=True)
            
            # METADATA SIDEBAR (Triggered by Graph Click)
            if selected_node:
                GraphDriver.display_provenance(selected_node['id'])

if __name__ == "__main__":
    main()
