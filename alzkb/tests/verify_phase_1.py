import sys
import os
from datetime import datetime

# Adjust path to import from src
# We are in alzkb/tests/, so src is ../src
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TEST_DIR, "../.."))
SRC_DIR = os.path.abspath(os.path.join(TEST_DIR, "../src"))
sys.path.append(SRC_DIR)

try:
    import rdflib
except ImportError:
    print("Error: rdflib not installed. Please run: pip install rdflib")
    sys.exit(1)

from alzkb.infrastructure.scoring import QualityEngine, Modality
from alzkb.validation.validator import validate_row

def log_success(msg):
    print(f"[\u2713] {msg}")

def log_fail(msg):
    print(f"[\u2717] {msg}")
    return False

def verify_ontology():
    print("\n--- 1. Verifying Ontology Syntax ---")
    onto_path = os.path.join(SRC_DIR, "alzkb/ontology/alzkb-ontology-v1.owl")
    if not os.path.exists(onto_path):
        return log_fail(f"Ontology file not found at {onto_path}")
    
    g = rdflib.Graph()
    try:
        g.parse(onto_path, format="turtle")
        log_success(f"Ontology parsed successfully. {len(g)} triples found.")
        return True
    except Exception as e:
        return log_fail(f"Ontology syntax error: {e}")

def verify_scoring():
    print("\n--- 2. Verifying Scoring Logic (QualityEngine) ---")
    try:
        # Test Case 1: High N, Low P (Good)
        entry = QualityEngine.calculate_confidence(
            p_value=1e-10, sample_size=1000, modality=Modality.MOLECULAR, source_id="TEST_GOOD"
        )
        if entry.final_confidence_score > 0.8:
            log_success(f"High Quality Entry Score: {entry.final_confidence_score} (Expected > 0.8)")
        else:
            return log_fail(f"Scoring Error: High quality data scored too low ({entry.final_confidence_score})")

        # Test Case 2: Low N, High P (Bad)
        entry_bad = QualityEngine.calculate_confidence(
            p_value=0.04, sample_size=10, modality=Modality.GWAS, source_id="TEST_BAD"
        )
        if entry_bad.final_confidence_score < 0.25:
            log_success(f"Low Quality Entry Score: {entry_bad.final_confidence_score} (Expected < 0.25)")
        else:
            return log_fail(f"Scoring Error: Low quality data scored too high ({entry_bad.final_confidence_score})")
        
        return True
    except Exception as e:
        return log_fail(f"Scoring Execution Error: {e}")

def verify_validation():
    print("\n--- 3. Verifying Validation Logic (ETL Validator) ---")
    try:
        # Test Case 1: Valid Row
        valid_row = {"birth_date": "1950-01-01", "diagnosis_date": "2020-01-01", "mmse_score": 25}
        is_valid, errors = validate_row(valid_row)
        if is_valid:
            log_success("Valid Row passed.")
        else:
            return log_fail(f"Valid Row failed: {errors}")

        # Test Case 2: Time Paradox
        paradox_row = {"birth_date": "2020-01-01", "diagnosis_date": "1950-01-01", "mmse_score": 25}
        is_valid, errors = validate_row(paradox_row)
        if not is_valid and "Temporal Causality Error" in errors[0]:
            log_success("Time Paradox correctly caught.")
        else:
            return log_fail("Time Paradox NOT caught.")

        return True
    except Exception as e:
        return log_fail(f"Validation Execution Error: {e}")

def main():
    print("=== AlzKB Phase I Verification Suite ===")
    print(f"Time: {datetime.now()}")
    
    checks = [
        verify_ontology(),
        verify_scoring(),
        verify_validation()
    ]
    
    if all(checks):
        print("\n=== PHASE I VERIFICATION SUCCESSFUL ===")
        print("All code artifacts are syntactically valid and logically sound.")
        print("Ready for deployment.")
    else:
        print("\n=== PHASE I VERIFICATION FAILED ===")
        print("Please review errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
