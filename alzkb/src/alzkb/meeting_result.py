"""Data structures and utilities for meeting results."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from google import genai


@dataclass
class MeetingResult:
    """Encapsulates the output of a meeting session.
    
    Attributes:
        topic: The meeting topic/title.
        timestamp: ISO format timestamp when the meeting concluded.
        chat: The raw chat object (for accessing .get_history()).
        summary_text: LLM-generated narrative summary.
        summary_structured: Structured summary with decisions, action items, status.
    """
    topic: str
    timestamp: str
    chat: Any
    summary_text: str
    summary_structured: Dict[str, Any] = field(default_factory=dict)
    
    def get_history(self) -> List[Any]:
        """Convenience method to access chat history."""
        return self.chat.get_history() if self.chat else []


def generate_narrative_summary(
    chat: Any,
    summarizer_title: str,
    model_name: str,
) -> str:
    """Generate a narrative (freeform text) summary of the meeting.
    
    :param chat: The chat session object containing the discussion history.
    :param summarizer_title: Title of the agent generating the summary.
    :param model_name: The Gemini model to use for generation.
    :return: A narrative summary string.
    """
    from alzkb.constants import SUMMARY_PROMPT
    
    summary_instruction = (
        f"ACT AS: {summarizer_title}\n"
        f"{SUMMARY_PROMPT}"
    )
    
    try:
        response = chat.send_message(summary_instruction)
        return response.text if response.text else "[No summary generated]"
    except Exception as e:
        return f"[Error generating summary: {e}]"


def generate_structured_summary(
    chat: Any,
    summarizer_title: str,
    model_name: str,
) -> Dict[str, Any]:
    """Generate a structured JSON summary of the meeting.
    
    :param chat: The chat session object containing the discussion history.
    :param summarizer_title: Title of the agent generating the summary.
    :param model_name: The Gemini model to use for generation.
    :return: A dictionary with decisions, action_items, status, and key_context.
    """
    from alzkb.constants import STRUCTURED_SUMMARY_PROMPT
    
    summary_instruction = (
        f"ACT AS: {summarizer_title}\n"
        f"{STRUCTURED_SUMMARY_PROMPT}"
    )
    
    try:
        response = chat.send_message(summary_instruction)
        if response.text:
            # Try to parse JSON from the response
            text = response.text.strip()
            # Handle markdown code blocks if present
            if text.startswith("```"):
                # Extract content between code fences
                lines = text.split("\n")
                json_lines = []
                in_block = False
                for line in lines:
                    if line.startswith("```"):
                        in_block = not in_block
                        continue
                    if in_block:
                        json_lines.append(line)
                text = "\n".join(json_lines)
            
            return json.loads(text)
        return _default_structured_summary()
    except json.JSONDecodeError as e:
        return {
            **_default_structured_summary(),
            "parse_error": str(e),
            "raw_response": response.text[:500] if response and response.text else None
        }
    except Exception as e:
        return {
            **_default_structured_summary(),
            "error": str(e)
        }


def _default_structured_summary() -> Dict[str, Any]:
    """Returns a default structured summary template."""
    return {
        "decisions": [],
        "action_items": [],
        "status": "UNKNOWN",
        "key_context": ""
    }


def create_meeting_result(
    topic: str,
    chat: Any,
    summarizer_title: str,
    model_name: str,
    generate_summaries: bool = True,
) -> MeetingResult:
    """Factory function to create a MeetingResult with generated summaries.
    
    :param topic: The meeting topic.
    :param chat: The chat session object.
    :param summarizer_title: Title of the agent generating summaries.
    :param model_name: The Gemini model to use.
    :param generate_summaries: Whether to generate summaries (set False to skip).
    :return: A complete MeetingResult object.
    """
    timestamp = datetime.now().isoformat()
    
    if generate_summaries:
        summary_text = generate_narrative_summary(chat, summarizer_title, model_name)
        summary_structured = generate_structured_summary(chat, summarizer_title, model_name)
    else:
        summary_text = ""
        summary_structured = _default_structured_summary()
    
    return MeetingResult(
        topic=topic,
        timestamp=timestamp,
        chat=chat,
        summary_text=summary_text,
        summary_structured=summary_structured,
    )
