from typing import Any, Dict

def graph_to_text(subject_uri: str, graph_client: Any) -> str:
    """
    Deterministically converts an entity subgraph into a narrative paragraph 
    for Vector Indexing.
    
    CRITICAL: 
    1. Implements 'In-Text Safety Stamping' for Tier 2 nodes.
    2. Enforces 'Semantic Restraint' (Direct Parent only).
    3. Requires Provenance Citation.
    """
    # Fetch Data: Direct Node + 1-Hop Neighbors + Direct Parent
    # Uses SKOS:prefLabel for all naming
    # graph_client is expected to have a get_rag_context method returning a dict-like object or Bunch
    data = graph_client.get_rag_context(subject_uri)
    
    narrative_buffer = []

    # --- 1. SAFETY STAMPING (Critic's Directive) ---
    # If the entity is predictive/inferred (Tier 2), inject hard skepticism.
    if data.get("tier_level") == "Tier_2":
        narrative_buffer.append(
            "[WARNING: HYPOTHETICAL ASSOCIATION] "
            "Computational inference suggests a relationship here, "
            "but this entity lacks in-vivo clinical validation. "
            "Treat findings as exploratory. "
        )
    else:
        narrative_buffer.append("[VALIDATED: TIER 1 EVIDENCE] ")

    # --- 2. IDENTITY & HIERARCHY (Ontologist's Directive) ---
    # Limit to Direct Parent (Semantic Restraint)
    narrative_buffer.append(
        f"Subject: {data.get('skos_prefLabel', 'Unknown')}. "
        f"Ontological Classification: {data.get('direct_parent_label', 'Unknown')}. "
    )

    # --- 3. BIOLOGICAL CONTEXT ---
    # Gene Template
    if data.get("type") == "GeneticMarker":
        pathways = ", ".join(data.get("pathways", []))
        narrative_buffer.append(
            f"This biological entity is involved in pathways: {pathways}. "
            f"Risk Association: {data.get('risk_level', 'Unknown')}. "
        )
    # Pathology Template
    elif data.get("type") == "Neuropathology":
        locations = ", ".join(data.get("locations", []))
        narrative_buffer.append(
            f"Found in anatomical location: {locations}. "
            f"Associated Braak Stage: {data.get('braak_stage', 'Unknown')}. "
        )

    # --- 4. PROVENANCE (Engineer's Directive) ---
    # Must cite the specific study or dataset ID
    source_id = data.get("provenance_source", "Unknown")
    narrative_buffer.append(f"(Source Authority: {source_id})")

    # Join and return
    return " ".join(narrative_buffer)
