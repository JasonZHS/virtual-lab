import networkx as nx
import pandas as pd
from alzkb.ingestion.config import VALID_TRAIT_IDS

class GWASLoader:
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def ingest_gwas_catalog(self, filepath: str):
        """
        Ingests GWAS Catalog data with 'Sentinel Logic' LD Pruning.
        """
        # Load Data
        df = pd.read_csv(filepath, sep='\t')
        
        # Filter by Allowlist
        df = df[df['MAPPED_TRAIT_URI'].apply(self._is_valid_trait)]
        
        # LD Pruning Strategy (Sentinel Logic)
        # Group by (MAPPED_GENE, CHROMOSOME) -> Select MIN(P_VALUE)
        # Note: This is a simplified implementation of the "Sentinel" logic.
        # In a real scenario, we would use window-based pruning.
        # Here we use the simplified group-by as per spec.
        
        # Ensure numeric columns
        df['P-VALUE'] = pd.to_numeric(df['P-VALUE'], errors='coerce')
        df['OR or BETA'] = pd.to_numeric(df['OR or BETA'], errors='coerce')
        
        # Drop rows without P-value
        df = df.dropna(subset=['P-VALUE'])
        
        # Sentinel Selection
        sentinels = df.loc[df.groupby(['MAPPED_GENE', 'CHR_ID'])['P-VALUE'].idxmin()]
        
        for _, row in sentinels.iterrows():
            self._add_association(row)
            
        return self.graph

    def _is_valid_trait(self, trait_uri):
        if pd.isna(trait_uri): return False
        # trait_uri format: http://www.ebi.ac.uk/efo/EFO_0000249
        id_part = trait_uri.split('/')[-1]
        return id_part in VALID_TRAIT_IDS

    def _add_association(self, row):
        """
        Constructs BioLink-compliant triples.
        """
        snp_id = f"dbSNP:{row['SNPS']}"
        disease_id = "MONDO:0004975" # Normalized from EFO
        gene_symbol = row['MAPPED_GENE']
        gene_id = f"HGNC:{gene_symbol}" # Simplified mapping
        
        # Topology 1: GWAS Association (SNP -> Disease)
        self.graph.add_edge(
            snp_id, 
            disease_id, 
            predicate="biolink:condition_associated_with_sequence_variant",
            p_value=float(row['P-VALUE']),
            source="GWAS_Catalog",
            risk_allele=row.get('STRONGEST SNP-RISK ALLELE', 'Unknown'),
            pubmed_id=str(row.get('PUBMEDID', ''))
        )
        
        # Topology 2: Genomic Location (SNP -is_variant_of-> Gene)
        if pd.notna(gene_symbol):
            self.graph.add_edge(
                snp_id, 
                gene_id,
                predicate="biolink:is_sequence_variant_of",
                source="Entrez/Ensembl_Mapping"
            )

if __name__ == "__main__":
    # Example Usage Stub
    print("GWAS Loader Module Loaded.")
