import math
from dataclasses import dataclass
from enum import Enum

# ==========================================
# MODULE: AlzKB Data Ingestion & Quality
# COMPONENT: Context-Aware Evidence Scorer (FINAL)
# ==========================================

class Modality(Enum):
    GWAS = "GWAS"           # Large scale genomic studies
    CLINICAL = "CLINICAL"   # Cognitive scores, observational cohorts
    MOLECULAR = "MOLECULAR" # CSF, PET, fluid biomarkers (invasive/expensive)

@dataclass
class EvidenceLedgerEntry:
    source_id: str
    modality: str
    raw_p_value: float
    raw_sample_size: int
    normalized_significance: float
    normalized_power: float
    final_confidence_score: float

class QualityEngine:
    """
    Handles strict 'Precision over Recall' normalization and scoring 
    for molecular and clinical associations in AD research.
    """

    GWAS_SIGNIFICANCE_THRESHOLD = 5e-8
    MIN_P_VALUE_CLAMP = 1e-100

    # Critic Feedback: Modality-specific baselines for 'Perfect' Power (1.0)
    # These values represent the N required to be considered 'high confidence' in that field.
    BASELINES = {
        Modality.GWAS: 50000,      # Meta-analysis scale
        Modality.CLINICAL: 2000,   # Large observational cohort
        Modality.MOLECULAR: 500    # High-N for invasive biomarkers
    }

    @staticmethod
    def _normalize_significance(p_value: float) -> float:
        """
        Normalizes p-value to 0-1 scale relative to GWAS threshold.
        """
        if p_value >= 0.05:
            return 0.0
        if p_value <= 0:
            p_value = QualityEngine.MIN_P_VALUE_CLAMP
            
        neg_log_p = -math.log10(p_value)
        neg_log_threshold = -math.log10(QualityEngine.GWAS_SIGNIFICANCE_THRESHOLD)
        
        score = neg_log_p / neg_log_threshold
        return min(1.0, max(0.0, score))

    @staticmethod
    def _normalize_power(n: int, modality: Modality) -> float:
        """
        Normalizes sample size based on the specific modality context.
        """
        if n <= 0:
            return 0.0
            
        baseline = QualityEngine.BASELINES.get(modality, 10000) # Fallback if unknown
        
        # Log scale normalization relative to modality-specific baseline
        log_n = math.log10(n)
        log_baseline = math.log10(baseline)
        
        score = log_n / log_baseline
        return min(1.0, max(0.0, score))

    @staticmethod
    def calculate_confidence(p_value: float, sample_size: int, modality: Modality, source_id: str) -> EvidenceLedgerEntry:
        """
        Executes the Official Phase I Scoring Formula:
        Score = (0.6 * Significance) + (0.4 * Power)
        """
        # 1. Normalize Inputs
        sig_score = QualityEngine._normalize_significance(p_value)
        pow_score = QualityEngine._normalize_power(sample_size, modality)
        
        # 2. Apply Formula
        WEIGHT_SIG = 0.6
        WEIGHT_POW = 0.4
        
        confidence = (WEIGHT_SIG * sig_score) + (WEIGHT_POW * pow_score)
        
        return EvidenceLedgerEntry(
            source_id=source_id,
            modality=modality.value,
            raw_p_value=p_value,
            raw_sample_size=sample_size,
            normalized_significance=round(sig_score, 4),
            normalized_power=round(pow_score, 4),
            final_confidence_score=round(confidence, 4)
        )

# Validation Check
if __name__ == "__main__":
    # Scenario A: CSF Biomarker Study (N=600 is excellent)
    csf_entry = QualityEngine.calculate_confidence(
        p_value=1e-5, 
        sample_size=600, 
        modality=Modality.MOLECULAR, 
        source_id="ADNI_CSF_SUBSET"
    )
    # Scenario B: GWAS Study (N=600 is poor)
    gwas_entry = QualityEngine.calculate_confidence(
        p_value=1e-5, 
        sample_size=600, 
        modality=Modality.GWAS, 
        source_id="SMALL_GWAS_PILOT"
    )
    
    print(f"CSF Score (N=600): {csf_entry.final_confidence_score}")  # Should be higher due to context
    print(f"GWAS Score (N=600): {gwas_entry.final_confidence_score}") # Should be lower
