import sys
import os

# Point to 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# Also point to project root for tests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from alzkb.ingestion.ingest_gwas import GWASLoader
# Import export manager using the same hack mechanism if needed, or rely on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from alzkb.ingestion.export_manager import run_export_pipeline

# Inline verify logic (keep as is or import if module fixed)
# Using inline logic for now
import importlib.util
spec = importlib.util.spec_from_file_location("verify_atn_status", os.path.join(os.path.dirname(__file__), "../../../tests/verify_atn_status.py"))
verify_module = importlib.util.module_from_spec(spec)
sys.modules["verify_atn_status"] = verify_module
spec.loader.exec_module(verify_module)
run_validation_suite = verify_module.run_validation_suite

def main():
    print("=== Phase VI: Real Data Ingestion & Validation ===")
    
    # Paths
    gwas_path = "alzkb/data/associations.tsv"
    
    if not os.path.exists(gwas_path):
        print(f"[X] Data file not found: {gwas_path}")
        return

    # 1. Ingestion
    print(f"[LOAD] Ingesting GWAS Catalog from {gwas_path}...")
    loader = GWASLoader()
    try:
        graph = loader.ingest_gwas_catalog(gwas_path)
        print(f"[✓] Ingestion Complete. Graph Nodes: {graph.number_of_nodes()}, Edges: {graph.number_of_edges()}")
    except Exception as e:
        print(f"[X] Ingestion Failed: {e}")
        return

    # 3. Export
    print("[EXPORT] Persisting Graph...")
    if run_export_pipeline(graph, "alzkb/data/alzkb_knowledge_graph.graphml"):
        print("\n[SUCCESS] Phase VII Connected: Graph Persisted to Disk.")
    else:
        print("\n[FAILURE] Graph Export Failed.")

if __name__ == "__main__":
    main()
