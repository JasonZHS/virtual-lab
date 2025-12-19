# FILE: alzkb/graph/pruning.py

def prune_network(graph, center_node, limit, strategy="weighted_novelty"):
    """
    Selects the most scientifically relevant nodes to visualize.
    """
    scored_nodes = []
    
    # Assuming graph.nodes is iterable of objects with .id, .properties, .degree attributes
    # and graph has get_edge_weight(u, v)
    
    for node in graph.nodes:
        if node.id == center_node:
            continue
            
        # 1. Base Score: Global Centrality (Pre-computed)
        # Note: We use Inverse Frequency to down-weight generic hubs like 'Protein'
        base_score = node.properties.get('inverse_node_freq', 0.1)
        
        # 2. Edge Weight: Strength of connection to the query
        edge_weight = graph.get_edge_weight(center_node, node.id)
        
        # 3. Novelty Boost (The Critic's Logic)
        # If a node is rare (low global degree) but has a strong edge 
        # to the query, we boost its score massively.
        novelty_boost = 1.0
        if strategy == "weighted_novelty":
            # Assuming node.degree is an integer
            if node.degree < 5 and edge_weight > 0.9:
                novelty_boost = 5.0 # Highlight emerging biomarkers
        
        final_score = base_score * edge_weight * novelty_boost
        scored_nodes.append((node, final_score))
        
    # Return top N sorted by specific relevance, not just popularity
    scored_nodes.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in scored_nodes[:limit]]
