import unittest
import sys
import os
from unittest.mock import MagicMock

# Adjust path to import from src
# We are in alzkb/tests/, so src is ../src
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(TEST_DIR, "../src"))
sys.path.append(SRC_DIR)

# Import Phase IV Modules
from alzkb.retrieval.rag_wrapper import graph_to_text
from alzkb.retrieval.prompts import RAG_SYSTEM_PROMPT
from alzkb.retrieval.search import hybrid_search

class TestPhase4Retrieval(unittest.TestCase):

    def test_graph_to_text_tier2_safety(self):
        """Action Item 1: Verify In-Text Safety Stamping for Tier 2."""
        print("\n[Check] Verifying RAG Safety Stamp (Tier 2)...")
        
        # Mock Client Result
        mock_client = MagicMock()
        mock_client.get_rag_context.return_value = {
            "tier_level": "Tier_2",
            "skos_prefLabel": "NovelGeneX",
            "direct_parent_label": "GeneticMarker",
            "type": "GeneticMarker",
            "risk_level": "High",
            "provenance_source": "GWAS_2024"
        }
        
        narrative = graph_to_text("alzkb:NovelGeneX", mock_client)
        
        if "[WARNING: HYPOTHETICAL ASSOCIATION]" in narrative:
            print(f"[✓] Safety Stamp Detected: {narrative[:50]}...")
        else:
            self.fail("Tier 2 entity missing safety stamp!")

    def test_graph_to_text_tier1_clean(self):
        print("\n[Check] Verifying RAG Verified Tier 1...")
        mock_client = MagicMock()
        mock_client.get_rag_context.return_value = {
            "tier_level": "Tier_1",
            "skos_prefLabel": "APOE4",
            "direct_parent_label": "Allele",
            "provenance_source": "OMIM"
        }
        narrative = graph_to_text("alzkb:APOE4", mock_client)
        if "[VALIDATED: TIER 1 EVIDENCE]" in narrative:
            print("[✓] Validation Stamp Detected.")
        else:
            self.fail("Tier 1 entity missing validation stamp.")

    def test_system_prompt_integrity(self):
        """Action Item 2: Verify System Prompt Protocols."""
        print("\n[Check] Verifying System Prompt Protocols...")
        if "CITATION IS MANDATORY" in RAG_SYSTEM_PROMPT and "TIER 2 SKEPTICISM" in RAG_SYSTEM_PROMPT:
            print("[✓] Critical Protocols confirmed in Prompt.")
        else:
            self.fail("System Prompt missing core protocols.")

    def test_hybrid_search_rrf(self):
        """Action Item 3: Verify Hybrid Keywork Boosting."""
        print("\n[Check] Verifying Hybrid Search Logic...")
        
        # Setup: Vector results where "Target" is low ranked (e.g., rank 10)
        vector_res = [{'uri': f'u{i}', 'label': f'Item{i}'} for i in range(20)]
        target_uri = 'u10'
        vector_res[10]['label'] = 'TARGET_GENE' # This is u10
        
        # Keyword match finds u10 exactly
        keyword_matches = ['u10']
        
        # Run Search with query matching label
        # u10 should get boosted to the top
        final = hybrid_search("TARGET_GENE", vector_res, keyword_matches)
        
        # u10 was rank 10 in vector, but unique keyword match + boost -> should be #1
        top_hit = final[0]
        if top_hit['uri'] == 'u10':
            print(f"[✓] Hybrid Boost worked. Rank 10 promoted to Rank 1 (Score: {top_hit['final_score']:.4f})")
        else:
            self.fail(f"Hybrid Search failed to boost keyword match. Top hit: {top_hit['uri']}")

    def test_ontology_last_updated(self):
         """Action Item 4 (Engineer): Verify alzkb:last_updated in Ontology."""
         print("\n[Check] Verifying Ontology Schema Update...")
         onto_path = os.path.join(SRC_DIR, "alzkb/ontology/alzkb-ontology-v1.owl")
         with open(onto_path, 'r') as f:
             content = f.read()
         
         if ":last_updated" in content or "last_updated" in content:
             print("[✓] 'last_updated' property found in OWL.")
         else:
             self.fail("Ontology missing 'last_updated' property.")

if __name__ == '__main__':
    unittest.main()
