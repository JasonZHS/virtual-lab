import logging
from datetime import datetime
from typing import Dict, Any, Tuple, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_row(row: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validates a single ETL row for AlzKB based on Phase I specifications.
    
    PERFORMANCE NOTE: This function is optimized for streaming ETL (row-by-row).
    For batch processing >1M rows, prefer vectorized dataframe operations.
    
    Args:
        row (Dict[str, Any]): Data dict. Keys: 'birth_date', 'diagnosis_date', 'mmse_score'.
    
    Returns:
        Tuple[bool, List[str]]: (isValid, errorList)
    """
    is_valid = True
    errors = []
    
    # --- 1. Temporal Causality Check ---
    birth_date_str = row.get('birth_date')
    diagnosis_date_str = row.get('diagnosis_date')

    if birth_date_str and diagnosis_date_str:
        try:
            # Parsing ISO format
            birth_date = datetime.strptime(str(birth_date_str), "%Y-%m-%d")
            diagnosis_date = datetime.strptime(str(diagnosis_date_str), "%Y-%m-%d")

            if diagnosis_date <= birth_date:
                is_valid = False
                errors.append(
                    f"Temporal Causality Error: Diagnosis ({diagnosis_date_str}) "
                    f"precedes or equals Birth ({birth_date_str})."
                )
        except ValueError as e:
            is_valid = False
            errors.append(f"Date Parsing Error: {e}")
    
    # --- 2. Clinical Range Check (MMSE) ---
    mmse_val = row.get('mmse_score')
    
    if mmse_val is not None:
        try:
            mmse_score = float(mmse_val)
            # MMSE is strictly 0 to 30
            if not (0.0 <= mmse_score <= 30.0):
                is_valid = False
                errors.append(f"Range Error: MMSE {mmse_score} out of bounds [0,30].")
        except (ValueError, TypeError):
            is_valid = False
            errors.append(f"Type Error: MMSE '{mmse_val}' is not numeric.")
    
    return is_valid, errors
