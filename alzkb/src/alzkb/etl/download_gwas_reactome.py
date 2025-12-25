#!/usr/bin/env python3
"""
ALZKB Data Downloaders - GWAS and Reactome (API-based)
------------------------------------------------------
Uses REST APIs instead of bulk file downloads to handle
the sources that are currently returning 403/404/timeout.
"""

import requests
import json
import time
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging
import sys

SCRIPT_DIR = Path(__file__).parent.resolve()
BASE_DIR = SCRIPT_DIR / "data" / "raw"
LOG_DIR = SCRIPT_DIR / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "api_download.log"), logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("AlzKB_API")


def download_gwas_alzheimers():
    """Download Alzheimer's GWAS associations via REST API."""
    logger.info("=" * 50)
    logger.info("GWAS CATALOG - Alzheimer's Associations via REST API")
    logger.info("=" * 50)
    
    output_dir = BASE_DIR / "gwas_catalog"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    base_url = "https://www.ebi.ac.uk/gwas/rest/api"
    
    # Search for Alzheimer's studies
    logger.info("Searching for Alzheimer's disease studies...")
    all_associations = []
    
    # Get studies by disease trait
    page = 0
    page_size = 100
    
    while True:
        try:
            url = f"{base_url}/studies/search/findByDiseaseTrait"
            params = {
                'diseaseTrait': "Alzheimer's disease",
                'page': page,
                'size': page_size
            }
            
            r = requests.get(url, params=params, headers={'Accept': 'application/json'}, timeout=60)
            
            if not r.ok:
                logger.warning(f"API returned {r.status_code}")
                break
            
            data = r.json()
            studies = data.get('_embedded', {}).get('studies', [])
            
            if not studies:
                logger.info("No more studies found.")
                break
            
            logger.info(f"Page {page + 1}: Found {len(studies)} studies")
            
            for study in studies:
                # Get associations for this study
                study_id = study.get('accessionId', '')
                
                if study_id:
                    try:
                        assoc_url = f"{base_url}/studies/{study_id}/associations"
                        ar = requests.get(assoc_url, headers={'Accept': 'application/json'}, timeout=30)
                        
                        if ar.ok:
                            assoc_data = ar.json()
                            associations = assoc_data.get('_embedded', {}).get('associations', [])
                            
                            for assoc in associations:
                                loci = assoc.get('loci', [])
                                snps = []
                                genes = []
                                
                                for locus in loci:
                                    for sr in locus.get('strongestRiskAlleles', []):
                                        if 'riskAlleleName' in sr:
                                            snps.append(sr['riskAlleleName'].split('-')[0])
                                    for gene in locus.get('authorReportedGenes', []):
                                        genes.append(gene.get('geneName', ''))
                                
                                all_associations.append({
                                    'study_id': study_id,
                                    'disease_trait': study.get('diseaseTrait', {}).get('trait', ''),
                                    'snps': ';'.join(snps),
                                    'genes': ';'.join(genes),
                                    'p_value': assoc.get('pvalue', ''),
                                    'risk_allele_frequency': assoc.get('riskFrequency', ''),
                                    'pubmed_id': study.get('publicationInfo', {}).get('pubmedId', ''),
                                })
                        
                        time.sleep(0.2)  # Rate limiting
                        
                    except Exception as e:
                        logger.warning(f"Error fetching associations for {study_id}: {e}")
            
            # Check pagination
            page_info = data.get('page', {})
            total_pages = page_info.get('totalPages', 1)
            
            if page + 1 >= total_pages or page >= 10:  # Limit to 10 pages for now
                break
            
            page += 1
            time.sleep(0.3)
            
        except Exception as e:
            logger.error(f"Error querying GWAS API: {e}")
            break
    
    # Save results
    if all_associations:
        df = pd.DataFrame(all_associations)
        output_file = output_dir / "ad_associations_api.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"Saved {len(df)} associations to {output_file}")
        
        # Provenance
        with open(output_dir / "provenance.json", 'w') as f:
            json.dump({
                "source": "gwas_catalog",
                "method": "REST API",
                "download_timestamp": datetime.utcnow().isoformat(),
                "api_base": base_url,
                "disease_trait": "Alzheimer's disease",
                "total_records": len(df)
            }, f, indent=2)
    else:
        logger.warning("No GWAS associations retrieved")
    
    return all_associations


def download_reactome_pathways():
    """Download Alzheimer's-related pathways via Reactome Content Service."""
    logger.info("=" * 50)
    logger.info("REACTOME - Alzheimer's Pathways via Content Service")
    logger.info("=" * 50)
    
    output_dir = BASE_DIR / "reactome"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    base_url = "https://reactome.org/ContentService"
    
    all_pathways = []
    
    # Search for Alzheimer's related pathways
    search_terms = ["Alzheimer", "amyloid", "tau", "neurodegeneration", "APOE"]
    
    for term in search_terms:
        logger.info(f"Searching for '{term}'...")
        
        try:
            url = f"{base_url}/search/query"
            params = {
                'query': term,
                'species': 'Homo sapiens',
                'types': 'Pathway',
                'cluster': 'true'
            }
            
            r = requests.get(url, params=params, timeout=60)
            
            if r.ok:
                data = r.json()
                results = data.get('results', [])
                
                for result in results:
                    entries = result.get('entries', [])
                    for entry in entries:
                        pathway_id = entry.get('stId', '')
                        
                        # Get pathway details
                        if pathway_id and pathway_id not in [p['pathway_id'] for p in all_pathways]:
                            try:
                                detail_url = f"{base_url}/data/query/{pathway_id}"
                                dr = requests.get(detail_url, timeout=30)
                                
                                if dr.ok:
                                    detail = dr.json()
                                    all_pathways.append({
                                        'pathway_id': pathway_id,
                                        'pathway_name': detail.get('displayName', ''),
                                        'species': detail.get('species', [{}])[0].get('displayName', '') if detail.get('species') else '',
                                        'is_disease': detail.get('isInDisease', False),
                                        'has_diagram': detail.get('hasDiagram', False),
                                        'search_term': term,
                                    })
                                
                                time.sleep(0.2)
                                
                            except Exception as e:
                                logger.warning(f"Error fetching pathway {pathway_id}: {e}")
                
                logger.info(f"  Found {len(results)} result groups")
            else:
                logger.warning(f"Search for '{term}' returned {r.status_code}")
            
            time.sleep(0.3)
            
        except Exception as e:
            logger.error(f"Error searching Reactome for '{term}': {e}")
    
    # Also get pathways for key AD genes
    ad_genes = ['P05067', 'P02649', 'P10636', 'P49768', 'Q99497']  # APP, APOE, MAPT, PSEN1, BACE1
    
    for gene in ad_genes:
        logger.info(f"Getting pathways for protein {gene}...")
        
        try:
            url = f"{base_url}/data/pathways/low/entity/{gene}"
            r = requests.get(url, timeout=30)
            
            if r.ok:
                pathways = r.json()
                for pw in pathways:
                    pathway_id = pw.get('stId', '')
                    if pathway_id and pathway_id not in [p['pathway_id'] for p in all_pathways]:
                        all_pathways.append({
                            'pathway_id': pathway_id,
                            'pathway_name': pw.get('displayName', ''),
                            'species': pw.get('species', {}).get('displayName', ''),
                            'is_disease': pw.get('isInDisease', False),
                            'has_diagram': pw.get('hasDiagram', False),
                            'search_term': f'gene:{gene}',
                        })
            
            time.sleep(0.3)
            
        except Exception as e:
            logger.warning(f"Error fetching pathways for {gene}: {e}")
    
    # Save results
    if all_pathways:
        df = pd.DataFrame(all_pathways)
        df = df.drop_duplicates(subset=['pathway_id'])
        output_file = output_dir / "ad_pathways_api.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"Saved {len(df)} unique pathways to {output_file}")
        
        with open(output_dir / "provenance.json", 'w') as f:
            json.dump({
                "source": "reactome",
                "method": "Content Service API",
                "download_timestamp": datetime.utcnow().isoformat(),
                "api_base": base_url,
                "search_terms": search_terms,
                "genes_queried": ad_genes,
                "total_pathways": len(df)
            }, f, indent=2)
    else:
        logger.warning("No Reactome pathways retrieved")
    
    return all_pathways


if __name__ == "__main__":
    logger.info("Starting API-based data downloads...")
    
    # GWAS
    gwas_result = download_gwas_alzheimers()
    print(f"\nGWAS: {len(gwas_result)} associations")
    
    # Reactome
    reactome_result = download_reactome_pathways()
    print(f"Reactome: {len(reactome_result)} pathways")
    
    logger.info("Download complete!")
