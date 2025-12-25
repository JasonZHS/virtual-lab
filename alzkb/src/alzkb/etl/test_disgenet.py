#!/usr/bin/env python3
"""
DisGeNET Data Downloader - AlzKB Production Script
---------------------------------------------------
Downloads Alzheimer's disease gene associations using DisGeNET REST API.
Filters for AD/dementia-related diseases with score > 0.5.
"""

import requests
import json
import time
import pandas as pd
from pathlib import Path
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
API_KEY = "70fbf2fb-9900-49da-96f0-a3b2ca196ecb"
API_BASE = "https://api.disgenet.com/api/v1"
OUTPUT_DIR = Path(__file__).parent / "data" / "raw" / "disgenet"

# Key Alzheimer's-related genes (NCBI Gene IDs)
AD_GENES = {
    351: "APP",       # Amyloid precursor protein
    348: "APOE",      # Apolipoprotein E  
    4137: "MAPT",     # Tau protein
    5663: "PSEN1",    # Presenilin 1
    5664: "PSEN2",    # Presenilin 2
    23621: "BACE1",   # Beta-secretase 1
    54209: "TREM2",   # Triggering receptor on myeloid cells 2
    9619: "ABCA7",    # ATP-binding cassette transporter
    10347: "ABCA1",   # Cholesterol efflux
    1636: "ACE",      # Angiotensin converting enzyme
    80308: "BIN1",    # Bridging integrator 1
    8878: "SQSTM1",   # Sequestosome 1
    6622: "SNCA",     # Alpha-synuclein
    7124: "TNF",      # Tumor necrosis factor
    3553: "IL1B",     # Interleukin 1 beta
    3569: "IL6",      # Interleukin 6
    2475: "MTOR",     # mTOR
    1956: "EGFR",     # Epidermal growth factor receptor
    7422: "VEGFA",    # Vascular endothelial growth factor A
    5594: "MAPK1",    # Mitogen-activated protein kinase 1
}

def make_request(endpoint: str, params: dict) -> dict:
    """Make authenticated request to DisGeNET API."""
    headers = {'Authorization': API_KEY, 'accept': 'application/json'}
    url = f"{API_BASE}/{endpoint}"
    response = requests.get(url, params=params, headers=headers, verify=False, timeout=60)
    
    if response.status_code == 429:
        wait_time = int(response.headers.get('x-rate-limit-retry-after-seconds', 60))
        print(f"    Rate limited. Waiting {wait_time}s...")
        time.sleep(wait_time)
        response = requests.get(url, params=params, headers=headers, verify=False, timeout=60)
    
    response.raise_for_status()
    return response.json()

def main():
    print("=" * 60)
    print("DisGeNET Data Downloader - AlzKB")
    print("=" * 60)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_associations = []
    
    for gene_id, gene_symbol in AD_GENES.items():
        print(f"\n[*] Querying gene: {gene_symbol} (NCBI ID: {gene_id})")
        
        try:
            params = {'gene_ncbi_id': str(gene_id), 'page_number': 0}
            data = make_request("gda/summary", params)
            
            if data.get('status') == 'OK':
                paging = data.get('paging', {})
                total = paging.get('totalElements', 0)
                print(f"    Found {total} total disease associations")
                
                payload = data.get('payload', [])
                ad_count = 0
                for item in payload:
                    # Use correct field names from API
                    disease_name = item.get('diseaseName', '').lower()
                    score = item.get('score', 0)
                    
                    # Filter for Alzheimer's/dementia related + score > 0.5
                    if ('alzheimer' in disease_name or 'dementia' in disease_name) and score >= 0.5:
                        all_associations.append({
                            'gene_symbol': item.get('symbolOfGene', gene_symbol),
                            'gene_ncbi_id': gene_id,
                            'disease_name': item.get('diseaseName', ''),
                            'disease_id': item.get('diseaseId', ''),
                            'score': score,
                            'ei': item.get('ei', 0),
                            'el': item.get('el', ''),
                            'n_publications': item.get('numPMIDs', 0),
                            'year_initial': item.get('yearInitial', ''),
                            'year_final': item.get('yearFinal', ''),
                        })
                        ad_count += 1
                
                if ad_count > 0:
                    print(f"    -> {ad_count} Alzheimer's/dementia associations (score >= 0.5)")
            
            time.sleep(0.3)
            
        except Exception as e:
            print(f"    Error: {e}")
    
    # Save results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    if all_associations:
        df = pd.DataFrame(all_associations)
        df = df.drop_duplicates(subset=['gene_symbol', 'disease_name'])
        df = df.sort_values('score', ascending=False)
        
        output_file = OUTPUT_DIR / "ad_gene_associations.csv"
        df.to_csv(output_file, index=False)
        
        print(f"Total unique associations: {len(df)}")
        print(f"Output saved to: {output_file}")
        print(f"\nTop 15 gene-disease associations by score:")
        print(df[['gene_symbol', 'disease_name', 'score', 'n_publications']].head(15).to_string(index=False))
        
        # Provenance
        provenance = {
            "source": "disgenet",
            "download_timestamp": datetime.utcnow().isoformat(),
            "api_base": API_BASE,
            "genes_queried": list(AD_GENES.keys()),
            "filter": "Alzheimer/Dementia diseases, score >= 0.5",
            "total_records": len(df)
        }
        with open(OUTPUT_DIR / "provenance.json", 'w') as f:
            json.dump(provenance, f, indent=2)
            
        print(f"\nProvenance saved to: {OUTPUT_DIR / 'provenance.json'}")
    else:
        print("No associations retrieved!")

if __name__ == "__main__":
    main()
