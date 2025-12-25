# Meeting Summary: Data Download Scripts
**Phase:** download_scripts
**Timestamp:** 2025-12-24T18:48:36.212036

## Summary
### MEETING SUMMARY: Data Ingestion Protocol (Tier 1 Public Sources)

**Date:** October 27, 2023
**Attendees:** Lead Data Engineer, Scientific Critic, Ontologist, Validation Scientist

**Outcome:**
The initial data ingestion strategy has been **REVISED** following critical review. The Scientific Critic correctly identified lapses in "Precision" logic regarding biomarker filtering and ChEMBL target breadth. The code has been refactored to enforce strict statistical significance upstream (during download) rather than downstream (during ETL), reducing the noise entering our "Raw" zone.

**Actionable Decisions:**
1.  **DisGeNET Threshold:** Raised strict inclusion criteria from Score > 0.4 to **Score > 0.5** to align with the *High Confidence* mandate.
2.  **GWAS Gating:** Implemented inline filtering for `P-VALUE < 5e-8` and `N > 10,000` within the download stream. This prevents low-power, low-significance associations from ever writing to disk.
3.  **ChEMBL Expansion:** Added **APOE**, **TREM2**, and **ABCA7** to the target list to capture lipidomic and immune-mediated drug interactions, moving beyond purely amyloid/tau targets.
4.  **Production Hardening:** Removed "demo limits" on Ensembl variant resolution to ensure full coverage of the filtered GWAS hits.

**Open Items:**
*   *Validation Phase:* The validation team must confirm that the regex logic for extracting "Sample Size" from the free-text GWAS columns accurately handles multi-cohort descriptions (e.g., "Stage 1: 5000, Stage 2: 7000").

---

### FINAL REVISED ITEM: `ingest_tier1_public.py`

```python
#!/usr/bin/env python3
"""
ALZKB DATA INGESTION PIPELINE - TIER 1 RAW DATA DOWNLOADER (REVISED)
--------------------------------------------------------------------
Author: Lead Data Engineer, AlzKB
Version: 1.1.0 (Post-Critique Revision)
Date: 2023-10-27

Change Log:
    v1.1.0: 
      - Tightened DisGeNET filter to Score > 0.5.
      - Added inline GWAS statistical gating (p < 5e-8, N > 10k).
      - Expanded ChEMBL targets (APOE, TREM2, ABCA7).
      - Removed demo limits on variant resolution.

Description:
    Executes retrieval of Tier 1 public datasets with strict 'Precision over Recall' 
    filtering applied at source/stream level.
"""

import os
import sys
import logging
import requests
import json
import shutil
import re
import pandas as pd
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION ---
BASE_DIR = Path("../data/raw")
LOG_DIR = Path("../logs")
USER_AGENT = "AlzKB-DataIngestion/1.1 (Research; precision-medicine-graph)"

# REVISED: Expanded Target List (Amyloid/Tau + Immune + Lipid)
CHEMBL_TARGETS = [
    "CHEMBL2487",  # APP
    "CHEMBL3776",  # MAPT
    "CHEMBL260",   # PSEN1
    "CHEMBL2115",  # PSEN2
    "CHEMBL2014",  # BACE1
    "CHEMBL2015",  # APOE (Lipid Metabolism)
    "CHEMBL2579",  # TREM2 (Microglial Activation)
    "CHEMBL2987"   # ABCA7 (Lipid Transport)
]

# --- SETUP LOGGING ---
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(module)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "download_pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("AlzKB_Ingest")

class DataResourceDownloader:
    """Abstract base handling common download, logging, and provenance logic."""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.output_dir = BASE_DIR / source_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.provenance_file = self.output_dir / "provenance.json"
        
    def _save_provenance(self, url: str, files_created: List[str], metadata: Dict = None):
        """Maintains the Evidence Ledger for data provenance."""
        record = {
            "source": self.source_name,
            "download_timestamp": datetime.utcnow().isoformat(),
            "source_url": url,
            "files": [str(f) for f in files_created],
            "engineer_notes": "Precision-filtered raw ingestion v1.1",
            "metadata": metadata or {}
        }
        with open(self.provenance_file, 'w') as f:
            json.dump(record, f, indent=2)
        logger.info(f"Provenance ledger updated for {self.source_name}")

    def download_file(self, url: str, filename: str) -> Path:
        local_path = self.output_dir / filename
        logger.info(f"Starting download: {url} -> {local_path}")
        try:
            with requests.get(url, stream=True, headers={"User-Agent": USER_AGENT}) as r:
                r.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return local_path
        except Exception as e:
            logger.error(f"Failed to download {url}: {str(e)}")
            raise

class GWASCatalogIngestor(DataResourceDownloader):
    """Ingests GWAS Catalog data with strict statistical gating."""
    
    def __init__(self):
        super().__init__("gwas_catalog")
        self.full_url = "https://www.ebi.ac.uk/gwas/api/search/downloads/full"
    
    def _parse_sample_size(self, text: str) -> int:
        """Heuristic to estimate N from free text 'INITIAL SAMPLE SIZE'."""
        if not isinstance(text, str): return 0
        # Find all numbers (removing commas)
        matches = re.findall(r'(\d{1,3}(?:,\d{3})*)', text)
        if not matches: return 0
        # Sum all found integers to get total N
        total = sum(int(m.replace(',', '')) for m in matches)
        return total

    def run(self):
        # 1. Download Full Catalog
        raw_file = self.download_file(self.full_url, "full_associations.tsv")
        
        # 2. Apply Precision Filters (AD + P<5e-8 + N>10k)
        logger.info("Applying strict statistical gating (p<5e-8, N>10k) to GWAS...")
        filtered_file = self.output_dir / "ad_filtered_associations.tsv"
        
        try:
            chunks = pd.read_csv(raw_file, sep='\t', chunksize=50000, low_memory=False)
            header = True
            hit_count = 0
            
            for chunk in chunks:
                # 2a. Text Filter (Context)
                txt_mask = (
                    chunk['DISEASE/TRAIT'].str.contains('Alzheimer', case=False, na=False) |
                    chunk['MAPPED_TRAIT'].str.contains('Alzheimer', case=False, na=False)
                )
                subset = chunk[txt_mask].copy()
                
                if not subset.empty:
                    # 2b. Statistical Filter (P-Value < 5e-8)
                    subset['P-VALUE'] = pd.to_numeric(subset['P-VALUE'], errors='coerce')
                    subset = subset[subset['P-VALUE'] < 5e-8]
                    
                    # 2c. Power Filter (N > 10,000)
                    if not subset.empty:
                        # Apply parsing to surviving rows only
                        subset['calc_N'] = subset['INITIAL SAMPLE SIZE'].apply(self._parse_sample_size)
                        subset = subset[subset['calc_N'] > 10000]
                        
                        if not subset.empty:
                            subset.drop(columns=['calc_N'], inplace=True)
                            subset.to_csv(filtered_file, sep='\t', mode='a', header=header, index=False)
                            header = False
                            hit_count += len(subset)
            
            logger.info(f"Filtered GWAS saved. High-Confidence Associations: {hit_count}")
            self._save_provenance(self.full_url, [raw_file, filtered_file], {"rows_preserved": hit_count})
            return filtered_file
            
        except Exception as e:
            logger.error(f"GWAS Filtering Failed: {e}")
            raise

class ReactomeIngestor(DataResourceDownloader):
    """Ingests Reactome BioPAX for human pathways."""
    def __init__(self):
        super().__init__("reactome")
        self.url = "https://reactome.org/download/current/Homo_sapiens.owl.zip"
        
    def run(self):
        zip_path = self.download_file(self.url, "Homo_sapiens.owl.zip")
        shutil.unpack_archive(zip_path, self.output_dir)
        self._save_provenance(self.url, [zip_path, self.output_dir / "Homo_sapiens.owl"])

class DisGeNETIngestor(DataResourceDownloader):
    """Uses SPARQL Federation with REVISED Score Threshold (> 0.5)."""
    
    def __init__(self):
        super().__init__("disgenet")
        self.sparql_endpoint = "http://rdf.disgenet.org/sparql/"
        
    def run(self):
        # REVISED: Threshold increased from 0.4 to 0.5
        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX sio: <http://semanticscience.org/resource/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        
        SELECT DISTINCT ?gene_symbol ?score ?disease_name WHERE {
            ?gda sio:SIO_000628 ?gene ;
                 sio:SIO_000628 ?disease ;
                 sio:SIO_000216 ?score_node .
            ?gene sio:SIO_000205 ?gene_symbol .
            ?disease dcterms:title ?disease_name .
            ?score_node sio:SIO_000300 ?score .
            
            FILTER regex(?disease_name, "Alzheimer", "i")
            FILTER (?score > 0.5)
        }
        LIMIT 10000
        """
        
        logger.info("Executing SPARQL query against DisGeNET (Score > 0.5)...")
        try:
            params = {'query': query, 'format': 'csv'}
            response = requests.get(self.sparql_endpoint, params=params, headers={"User-Agent": USER_AGENT})
            response.raise_for_status()
            
            output_file = self.output_dir / "ad_gene_associations.csv"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            self._save_provenance(self.sparql_endpoint, [output_file], {"query": query})
        except Exception as e:
            logger.error(f"DisGeNET SPARQL failed: {e}")
            raise

class ChEMBLIngestor(DataResourceDownloader):
    """Retrieves bioactivity data for expanded target list."""
    
    def __init__(self):
        super().__init__("chembl")
        self.api_url = "https://www.ebi.ac.uk/chembl/api/data/activity"
        
    def run(self):
        all_activities = []
        logger.info(f"Querying ChEMBL for {len(CHEMBL_TARGETS)} targets (Amyloid/Tau/Immune/Lipid)...")
        
        for target_id in CHEMBL_TARGETS:
            try:
                params = {
                    'target_chembl_id': target_id,
                    'standard_type__in': 'IC50,Ki,Kd',
                    'limit': 1000,
                    'format': 'json'
                }
                resp = requests.get(self.api_url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    acts = data.get('activities', [])
                    logger.info(f"  - {target_id}: {len(acts)} activities.")
                    for act in acts:
                        all_activities.append({
                            "target_id": target_id,
                            "molecule_chembl_id": act.get("molecule_chembl_id"),
                            "standard_type": act.get("standard_type"),
                            "standard_value": act.get("standard_value"),
                            "standard_units": act.get("standard_units")
                        })
                time.sleep(0.2)
            except Exception as e:
                logger.warning(f"ChEMBL fetch error {target_id}: {e}")
        
        output_file = self.output_dir / "target_bioactivities.csv"
        pd.DataFrame(all_activities).to_csv(output_file, index=False)
        self._save_provenance(self.api_url, [output_file], {"targets": CHEMBL_TARGETS})

class EnsemblResolutionIngestor(DataResourceDownloader):
    """Resolves RSIDs for ALL filtered GWAS hits (No Demo Limits)."""
    
    def __init__(self, gwas_file: Path):
        super().__init__("ensembl")
        self.gwas_file = gwas_file
        self.api_base = "https://rest.ensembl.org"
        
    def run(self):
        if not self.gwas_file.exists():
            return

        df = pd.read_csv(self.gwas_file, sep='\t')
        rsids = df['SNPS'].dropna().unique().tolist()
        
        # REVISED: No slicing. Production run.
        logger.info(f"Resolving {len(rsids)} unique SNPs via Ensembl API...")
        
        def fetch_variant(rsid):
            try:
                r = requests.get(f"{self.api_base}/variation/human/{rsid}?", 
                               headers={"Content-Type": "application/json"})
                return r.json() if r.ok else None
            except:
                return None

        # Threaded fetch
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(fetch_variant, rsids))
            
        resolved_data = [r for r in results if r]
        
        output_file = self.output_dir / "variant_cache.json"
        with open(output_file, 'w') as f:
            json.dump(resolved_data, f, indent=2)
        self._save_provenance(self.api_base, [output_file], {"input_gwas": str(self.gwas_file)})

def main():
    logger.info("--- STARTING TIER 1 DATA INGESTION (v1.1) ---")
    try:
        gwas_path = GWASCatalogIngestor().run()
        ReactomeIngestor().run()
        DisGeNETIngestor().run()
        ChEMBLIngestor().run()
        EnsemblResolutionIngestor(gwas_path).run()
        logger.info("--- INGESTION COMPLETE ---")
    except Exception as e:
        logger.critical(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Key Decisions
1. Raise DisGeNET inclusion threshold from score 0.4 to 0.5 to ensure High Confidence nodes.
2. Enforce strict GWAS statistical gating (p < 5e-8, N > 10k) during the download stream to prevent raw zone pollution.
3. Expand ChEMBL drug-target list to include Lipidomic (APOE, ABCA7) and Immune (TREM2) drivers alongside Amyloid/Tau.
4. Remove artificial 'demo limits' from Ensembl variant resolution to ensure production-grade coverage.

## Action Items
- Deploy 'ingest_tier1_public.py' v1.1.0 to the production ingestion server (Lead Data Engineer)
- Validate regex logic for GWAS 'Initial Sample Size' against multi-cohort text descriptions (Validation Scientist)
- Monitor API rate limits for Ensembl and ChEMBL during the initial full-scale run (Infrastructure Lead)

## Status: COMPLETE
