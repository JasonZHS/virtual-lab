# FINAL CONFIGURATION for alzkb/ingestion/config.py

# 1. EFO ALLOWLIST (Replaces Regex) - Strict Specificity
VALID_TRAIT_IDS = {
    "EFO_0000249",   # Alzheimer's disease
    "MONDO_0004975", # Alzheimer disease
    "EFO_0000732",   # Familial Alzheimer's disease
    "EFO_0000253",   # Late-onset Alzheimer's disease
    "HP_0002511"     # Alzheimer disease (HPO)
}

# 2. COLUMNS MAP
GWAS_COLUMNS = {
    'shorthand': {
        'pval': 'p_value',
        'beta': 'beta',
        'or': 'odds_ratio',
        'chrom': 'chromosome',
        'pos': 'base_pair_location',
        'ref': 'effect_allele', # varying standard, often effect
        'alt': 'other_allele',
        'rsid': 'variant_id',
        'trait_id': 'efo_id' 
    }
}
