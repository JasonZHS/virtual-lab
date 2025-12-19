import logging
from typing import Tuple, Dict, Any

# Configure module-level logger
logger = logging.getLogger("alzkb.etl.genotype")

def compute_haplotype(
    rs429358_val: str, 
    rs7412_val: str, 
    rs429358_gq: float = 99.0, 
    rs7412_gq: float = 99.0
) -> Dict[str, Any]:
    """
    Computes APOE genotype with strand normalization and quality-weighted confidence.
    
    Args:
        rs429358_val (str): Raw alleles (e.g., 'T/C', 'A/G').
        rs7412_val (str): Raw alleles (e.g., 'C/C').
        rs429358_gq (float): Genotype Quality score (0-99) from VCF.
        rs7412_gq (float): Genotype Quality score (0-99) from VCF.

    Returns:
        Dict: Graph node attributes including URI, normalized label, and weighted confidence.
    """
    
    # DNA Complement Map for Strand Flipping (A<->T, C<->G)
    COMPLEMENT_MAP = str.maketrans("ACGT", "TGCA")

    def normalize_alleles(val: str) -> Tuple[str, str]:
        """Cleans separators, sorts alleles, and flips negative strand (A/G) to positive (T/C)."""
        if not val:
            raise ValueError("Empty allele string")
            
        clean_val = val.replace('|', '/').replace(':', '/').upper().strip()
        parts = clean_val.split('/')
        
        if len(parts) != 2:
            raise ValueError(f"Ploidy Error: Expected 2 alleles, got {len(parts)} in '{val}'")

        # Detect Negative Strand: APOE variants are canonically T/C. 
        # If we see A or G, we assume negative strand reporting and flip.
        if any(b in {'A', 'G'} for b in parts):
            parts = [b.translate(COMPLEMENT_MAP) for b in parts]
            
        if not all(base in {'C', 'T'} for base in parts):
             # If after flipping we still don't have C/T, it's a non-canonical variant or error
             raise ValueError(f"Non-canonical bases detected: {val} -> {parts}")
             
        return tuple(sorted(parts))

    try:
        snp_429358 = normalize_alleles(rs429358_val)
        snp_7412 = normalize_alleles(rs7412_val)
    except ValueError as e:
        logger.warning(f"APOE Normalization Failed: {e}")
        return {
            'uri': 'alzkb:Genotype_Indeterminate',
            'label': 'Indeterminate',
            'risk_uri': 'alzkb:Risk_Unknown',
            'confidence': 0.0,
            'provenance': str(e)
        }

    # Biological Mapping
    # (rs429358, rs7412) -> (URI, Label, Risk URI)
    genotype_map = {
        (('T', 'T'), ('T', 'T')): ('alzkb:APOE_e2e2', 'e2/e2', 'alzkb:Risk_Protective'),
        (('T', 'T'), ('C', 'T')): ('alzkb:APOE_e2e3', 'e2/e3', 'alzkb:Risk_NeutralProtective'),
        (('T', 'T'), ('C', 'C')): ('alzkb:APOE_e3e3', 'e3/e3', 'alzkb:Risk_Neutral'),
        (('C', 'T'), ('C', 'T')): ('alzkb:APOE_e2e4', 'e2/e4', 'alzkb:Risk_Intermediate'), 
        (('C', 'T'), ('C', 'C')): ('alzkb:APOE_e3e4', 'e3/e4', 'alzkb:Risk_High'),
        (('C', 'C'), ('C', 'C')): ('alzkb:APOE_e4e4', 'e4/e4', 'alzkb:Risk_VeryHigh'),
    }

    result = genotype_map.get((snp_429358, snp_7412))

    if result:
        uri, label, risk_uri = result
        
        # Calculate Confidence Score (0.0 - 1.0)
        # 1. Base confidence derived from lowest input GQ (normalized to 0-1)
        base_conf = min(rs429358_gq, rs7412_gq) / 100.0
        
        # 2. Penalty for Double Heterozygotes (e2/e4) due to lack of phasing
        # Unless we have long-reads, we assume trans, but cis (e1/e3) is theoretically possible.
        phasing_penalty = 0.05 if label == 'e2/e4' else 0.0
        
        final_conf = max(0.0, base_conf - phasing_penalty)

        return {
            'uri': uri,
            'label': label,
            'risk_uri': risk_uri,
            'confidence': round(final_conf, 3),
            'provenance': f"Derived from rs429358(GQ:{rs429358_gq}) + rs7412(GQ:{rs7412_gq})"
        }
    else:
        return {
            'uri': 'alzkb:APOE_RareVariant',
            'label': 'Rare/Unknown Combination',
            'risk_uri': 'alzkb:Risk_Unknown',
            'confidence': 0.5,  # Low confidence in utility, high confidence in rarity
            'provenance': f"Valid alleles {snp_429358}+{snp_7412} do not map to standard isoforms."
        }
