import unittest
import os
import sys
from rdflib import Graph, URIRef

# We are in alzkb/tests/, so src is ../src
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(TEST_DIR, "../src"))
sys.path.append(SRC_DIR)

from alzkb.validation.test_atn_biology import validate_atn_biology
# Verify Haplotype Computer via direct import
from alzkb.ingestion.haplotype_computer import compute_haplotype

class TestPhase3Verification(unittest.TestCase):

    def test_ontology_extensions(self):
        print("\n[Check] Verifying Phase III Ontology Extensions...")
        g = Graph()
        onto_path = os.path.join(SRC_DIR, "alzkb/ontology/alzkb-ontology-v1.owl")
        g.parse(onto_path, format="turtle")
        
        # Check for new classes
        has_ev = (URIRef("http://alzkb.org/ontology/v1#Ev_eQTL_Brain"), None, None) in g
        has_e4 = (URIRef("http://alzkb.org/ontology/v1#APOE_e4e4"), None, None) in g
        
        if has_ev and has_e4:
            print("[✓] Ontology extensions found (eQTL, APOE genotypes).")
        else:
            self.fail("Ontology missing Phase III definitions.")

    def test_haplotype_logic(self):
        print("\n[Check] Verifying Haplotype Computer...")
        # Quick check of the logic
        res = compute_haplotype('C/C', 'C/C')
        if res['label'] == 'e4/e4':
            print("[✓] Haplotype Computer correctly identifies e4/e4.")
        else:
            self.fail("Haplotype Computer failed basic logic.")

    def test_tier_promotion_query_exists(self):
        print("\n[Check] Verifying Tier Promotion Query...")
        query_path = os.path.join(SRC_DIR, "alzkb/resolution/tier_promotion.sparql")
        if os.path.exists(query_path):
             print("[✓] SPARQL Query file exists.")
        else:
             self.fail("Missing tier_promotion.sparql")

if __name__ == '__main__':
    unittest.main()
