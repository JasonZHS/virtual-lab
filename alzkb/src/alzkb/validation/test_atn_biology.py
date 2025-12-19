from scipy.stats import mannwhitneyu
import numpy as np

def validate_atn_biology(cohort_df):
    """
    Revised Phase III Stress Test.
    Rejects Global Correlation. Enforces Group-Wise Contrast.
    """
    # 1. Segment Populations (Critic's Requirement)
    group_ad = cohort_df[cohort_df['diagnosis_code'] == 'AD']
    group_cn = cohort_df[cohort_df['diagnosis_code'] == 'CN']
    
    # 2. Extract Biomarkers (Normalized to pg/mL)
    ad_amyloid = group_ad['csf_abeta42'].dropna()
    cn_amyloid = group_cn['csf_abeta42'].dropna()
    
    ad_ptau = group_ad['csf_ptau181'].dropna()
    cn_ptau = group_cn['csf_ptau181'].dropna()
    
    # 3. Statistical Test: Mann-Whitney U
    # Amyloid should be LOWER in AD
    u_stat_a, p_val_a = mannwhitneyu(ad_amyloid, cn_amyloid, alternative='less')
    
    # p-Tau should be HIGHER in AD
    u_stat_t, p_val_t = mannwhitneyu(ad_ptau, cn_ptau, alternative='greater')
    
    # 4. Strict Pass/Fail
    if p_val_a < 0.05 and p_val_t < 0.05:
        return True, "VALIDATION PASSED: Significant biological separation observed."
    else:
        return False, f"VALIDATION FAILED: Biology violation. p-Amyloid={p_val_a}, p-Tau={p_val_t}"
