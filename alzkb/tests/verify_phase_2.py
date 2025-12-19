import sys
import os
import unittest
from rdflib import Namespace, URIRef, Literal, XSD

# Adjust path to import from src
# We are in alzkb/tests/, so src is ../src
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(TEST_DIR, "../src"))
sys.path.append(SRC_DIR)

from alzkb.ingestion.ingest_csf import process_adni_csf_row, TRIPLE_BUFFER
# Need to clear buffer before tests
import alzkb.ingestion.ingest_csf as ingest_module

ALZKB = Namespace("http://alzkb.ai/ontology/")

class TestPhase2(unittest.TestCase):
    
    def setUp(self):
        # Reset buffer
        ingest_module.TRIPLE_BUFFER = []
        
        # Mock Data
        self.cn_stats = {'MEAN': 200.0, 'STD': 50.0}
        self.manifest = {'unit_type': 'ng/L', 'dataset_uri': 'http://adni.loni.usc.edu', 'reliability_score': 0.9}
        
    def test_ontology_baseline_resolvable(self):
        """
        Action Item 3 (Ontologist): Verify alzkb:ADNI_CN_Control_Baseline exists in Ontology.
        """
        print("\n[Check] Verifying Ontology Baseline Integrity...")
        onto_path = os.path.join(SRC_DIR, "alzkb/ontology/alzkb-ontology-v1.owl")
        
        with open(onto_path, 'r') as f:
            content = f.read()
            
        # We look for the definition of ADNI_CN_Control_Baseline
        if "ADNI_CN_Control_Baseline" in content:
            print("[\u2713] Baseline Found.")
        else:
            print("[\u2717] Baseline NOT Found in Ontology file!")
            # We don't fail here to allow other tests to run, but we log it.
            # In a strict test we might fail.
            self.fail("Ontology Missing 'ADNI_CN_Control_Baseline'")

    def test_ingestion_logic_happy_path(self):
        """
        Action Item 2 (Validation): Run calibration check (Happy Path).
        """
        print("\n[Check] Testing Ingestion Logic (Valid Row)...")
        row = {'RID': '001', 'VISCODE': 'bl', 'AB42': '250', 'MATRIX': 'CSF'}
        
        process_adni_csf_row(row, self.cn_stats, self.manifest)
        
        # Expect triples in buffer
        self.assertTrue(len(ingest_module.TRIPLE_BUFFER) > 0)
        
        # Check Z-Score Logic
        # Raw=250. Mean=200. Std=50. Z should be (250-200)/50 = 1.0
        found_z = False
        for s, p, o in ingest_module.TRIPLE_BUFFER:
            if p == ALZKB.zScore:
                self.assertEqual(float(o), 1.0)
                found_z = True
        
        if found_z:
            print("[\u2713] Z-Score Logic Verified (250 -> 1.0).")
        else:
            self.fail("Z-Score triple not generated.")

    def test_ingestion_filters(self):
        """
        Action Item 1 (Engineer): Verify filters work.
        """
        print("\n[Check] Testing Ingestion Filters...")
        # Case 1: Wrong Matrix
        ingest_module.TRIPLE_BUFFER = []
        process_adni_csf_row({'MATRIX': 'PLASMA', 'AB42': '200'}, self.cn_stats, self.manifest)
        self.assertEqual(len(ingest_module.TRIPLE_BUFFER), 0, "Failed to reject PLASMA")
        
        # Case 2: Negative Value (Quarantine)
        # Note: function prints QUARANTINE but doesn't return triples
        ingest_module.TRIPLE_BUFFER = []
        process_adni_csf_row({'RID': '002', 'VISCODE': 'bl', 'AB42': '-5', 'MATRIX': 'CSF'}, self.cn_stats, self.manifest)
        self.assertEqual(len(ingest_module.TRIPLE_BUFFER), 0, "Failed to reject Negative Value")
        
        print("[\u2713] Filters Verified.")

if __name__ == '__main__':
    unittest.main()
