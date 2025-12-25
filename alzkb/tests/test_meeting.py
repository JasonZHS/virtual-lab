"""Tests for the meeting module."""

import sys
import os

# Ensure src is in pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from alzkb.meeting import run_meeting
from alzkb.meeting_result import MeetingResult
from alzkb.meeting_context import MeetingContext
from alzkb.constants import PRINCIPAL_INVESTIGATOR, SCIENTIFIC_CRITIC, MODEL_FLASH


def test_individual_meeting():
    """Test that individual meetings return a MeetingResult."""
    print("Testing Individual Meeting...")
    
    result = run_meeting(
        meeting_type="individual",
        agenda="Define the core schema for the AlzKB knowledge graph.",
        topic="Test Meeting",
        team_member=PRINCIPAL_INVESTIGATOR,
        num_rounds=1,
        model_name=MODEL_FLASH
    )
    
    # Validate return type
    assert isinstance(result, MeetingResult), f"Expected MeetingResult, got {type(result)}"
    assert result.topic == "Test Meeting"
    assert result.timestamp is not None
    assert result.chat is not None
    assert result.summary_text is not None
    assert isinstance(result.summary_structured, dict)
    
    print(f"✓ MeetingResult returned with topic: {result.topic}")
    print(f"✓ Summary text length: {len(result.summary_text)}")
    print(f"✓ Structured summary keys: {list(result.summary_structured.keys())}")
    
    return result


def test_meeting_context():
    """Test MeetingContext storage and retrieval."""
    import tempfile
    import shutil
    
    print("\nTesting MeetingContext...")
    
    # Create temp directory for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        context = MeetingContext(project_name="TestProject", storage_dir=temp_dir)
        
        # Run a quick meeting
        result = run_meeting(
            meeting_type="individual",
            agenda="Quick test.",
            topic="Context Test",
            team_member=PRINCIPAL_INVESTIGATOR,
            num_rounds=1,
            model_name=MODEL_FLASH
        )
        
        # Add to context
        context.add_result("test_phase", result)
        
        # Verify storage
        phase_dir = os.path.join(temp_dir, "test_phase")
        assert os.path.exists(phase_dir), "Phase directory not created"
        assert os.path.exists(os.path.join(phase_dir, "test_phase_summary.md")), "MD file not created"
        assert os.path.exists(os.path.join(phase_dir, "test_phase_summary.json")), "JSON file not created"
        
        print(f"✓ Files saved to: {phase_dir}")
        
        # Test context retrieval
        prev_context = context.get_previous_context(["test_phase"])
        assert "PREVIOUS PHASES CONTEXT" in prev_context
        print(f"✓ Previous context retrieved ({len(prev_context)} chars)")
        
        # Test reload
        loaded_context = MeetingContext.load("TestProject", temp_dir)
        assert "test_phase" in loaded_context.phases
        print("✓ Context reloaded from disk successfully")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("\nAll MeetingContext tests passed!")


if __name__ == "__main__":
    print("=" * 50)
    print("MEETING MODULE TESTS")
    print("=" * 50)
    
    test_individual_meeting()
    print("\n" + "=" * 50)
    test_meeting_context()
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
