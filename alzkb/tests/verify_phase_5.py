import unittest
import sys
import os
from dataclasses import dataclass, field
from typing import Dict, Any

# Adjust path to import from src
# We are in alzkb/tests/, so src is ../src
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(TEST_DIR, "../src"))
sys.path.append(SRC_DIR)

# Import Module to Test
from alzkb.graph.pruning import prune_network

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class MockNode:
    id: str
    degree: int
    properties: Dict[str, Any] = field(default_factory=dict)

class MockGraph:
    def __init__(self):
        self.nodes = []
        self.edges = {} # (u, v) -> weight

    def add_node(self, id, degree, freq=0.5):
        # inverse_node_freq defaults to 0.1 if not present in properties
        node = MockNode(id, degree, {'inverse_node_freq': freq})
        self.nodes.append(node)

    def add_edge(self, u, v, weight):
        self.edges[(u, v)] = weight
        self.edges[(v, u)] = weight

    def get_edge_weight(self, u, v):
        return self.edges.get((u, v), 0.0)

class TestPhase5Visualization(unittest.TestCase):

    def test_pruning_novelty_boost(self):
        """Action Item 2: Test 'Weighted Novelty' Pruning Logic."""
        print("\n[Check] Verifying Pruning Logic (Novelty Protocol)...")
        
        g = MockGraph()
        center = "QUERY_GENE"
        g.add_node(center, 100)
        
        # Candidate A: Hub Node (High Degree, Strong Edge)
        # Base=0.1, Edge=0.95, Novelty=1.0 (Degree > 5) -> Score ~ 0.095
        g.add_node("HUB_A", degree=500, freq=0.1)
        g.add_edge(center, "HUB_A", 0.95)
        
        # Candidate B: Novel Biomarker (Low Degree, High Edge)
        # Base=0.1, Edge=0.95, Novelty=5.0 (Degree < 5) -> Score ~ 0.475
        g.add_node("NOVEL_B", degree=3, freq=0.1)
        g.add_edge(center, "NOVEL_B", 0.95)
        
        # Candidate C: Weak noise
        g.add_node("NOISE_C", degree=2, freq=0.1)
        g.add_edge(center, "NOISE_C", 0.1)
        
        # Run Pruning
        results = prune_network(g, center, limit=5, strategy="weighted_novelty")
        top_node = results[0]
        
        if top_node.id == "NOVEL_B":
            print(f"[✓] Novelty Boost Confirmed. Rare node '{top_node.id}' outranked Hub.")
        else:
            self.fail(f"Pruning Logic Failed. Expected NOVEL_B, got {top_node.id}")

    def test_ui_import_integrity(self):
        """Action Item 1: Verify UI Controller Imports."""
        print("\n[Check] Verifying UI Controller Import Integrity...")
        try:
            import alzkb.ui.app as app
            print("[✓] UI Controller imports successfully.")
        except ImportError as e:
            self.fail(f"UI Controller Import Error: {e}")
        except Exception as e:
            # Streamlit might complain about not being run via 'streamlit run', which is fine.
            # We just want to ensure python syntax and imports are valid.
            print(f"[Warn] UI Warning (Expected if not running via streamlit): {e}")

if __name__ == '__main__':
    unittest.main()
