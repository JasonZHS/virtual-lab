from typing import List, Dict, Any

def hybrid_search(query: str, vector_results: List[Dict[str, Any]], keyword_matches: List[str]) -> List[Dict[str, Any]]:
    """
    Implements Hybrid Search Logic using Reciprocal Rank Fusion (RRF).
    
    Logic:
    - Query A (Vector): Dense Retrieval (Semantic intent).
    - Query B (Keyword): BM25 on field content_text_exact (Mapped to skos:prefLabel).
    - Weighting: If Query B matches a gene symbol exactly, boost score by 3.0x.
    
    Args:
        query: The search query string.
        vector_results: List of dicts with 'uri', 'score', 'label'.
        keyword_matches: List of URIs that matched exact keywords.
        
    Returns:
        List of re-ranked results.
    """
    
    # 1. Initialize Scores
    rrf_scores = {}
    
    # Constants
    K = 60.0 # RRF constant
    BOOST_FACTOR = 3.0
    
    # 2. Process Vector Results
    # Rank is index + 1
    for rank, res in enumerate(vector_results):
        uri = res['uri']
        # standard RRF: 1 / (k + rank)
        score = 1.0 / (K + rank + 1)
        
        # Initialize
        if uri not in rrf_scores:
            rrf_scores[uri] = {'dat': res, 'score': 0.0}
            
        rrf_scores[uri]['score'] += score

    # 3. Process Keyword Boosts (Simulating BM25 Exact Match Boost)
    # In a real system, we'd fuse ranked lists. Here, we apply a boost if the URI was a keyword match.
    for uri in rrf_scores:
        if uri in keyword_matches:
            # Check if query looks like an exact symbol match (simplified logic)
            # If the label of the result matches the query exactly (case-insensitive)
            label = rrf_scores[uri]['dat'].get('label', '').upper()
            if label == query.upper().strip():
                 rrf_scores[uri]['score'] *= BOOST_FACTOR
    
    # 4. Sort by Final Score
    sorted_uris = sorted(rrf_scores.keys(), key=lambda u: rrf_scores[u]['score'], reverse=True)
    
    final_results = []
    for u in sorted_uris:
        item = rrf_scores[u]['dat']
        item['final_score'] = rrf_scores[u]['score']
        final_results.append(item)
        
    return final_results
