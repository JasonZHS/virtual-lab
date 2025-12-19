
import sys
import os

# Ensure src is in pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from alzkb.meeting import run_meeting
from alzkb.constants import PRINCIPAL_INVESTIGATOR, SCIENTIFIC_CRITIC, MODEL_FLASH

def test_individual_meeting():
    print("Testing Individual Meeting...")
    
    # Simple PI vs Critic meeting
    chat = run_meeting(
        meeting_type="individual",
        agenda="Define the core schema for the AlzKB knowledge graph.",
        team_member=PRINCIPAL_INVESTIGATOR,
        num_rounds=1,
        model_name=MODEL_FLASH
    )
    
    print("\nTest Complete.")
    return chat

if __name__ == "__main__":
    test_individual_meeting()
