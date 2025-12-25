"""Manages meeting context across phases."""

import json
from pathlib import Path
from typing import Dict, List, Optional

from alzkb.meeting_result import MeetingResult


class MeetingContext:
    """Manages the chain of meeting summaries across project phases.
    
    This class stores meeting results in memory and persists them to disk
    in both Markdown (human-readable) and JSON (programmatic) formats.
    
    Example:
        context = MeetingContext(project_name="AlzKB", storage_dir="../discussions")
        result = run_meeting(...)
        context.add_result("phase_1", result)
        
        # Later, get context for next phase
        prev_context = context.get_previous_context(["phase_1"])
    """
    
    def __init__(self, project_name: str, storage_dir: str):
        """Initialize the meeting context manager.
        
        :param project_name: Name of the project (e.g., "AlzKB").
        :param storage_dir: Directory to persist phase results.
        """
        self.project_name = project_name
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.phases: Dict[str, MeetingResult] = {}
    
    def add_result(self, phase_name: str, result: MeetingResult) -> None:
        """Store a meeting result and persist to disk.
        
        :param phase_name: Identifier for this phase (e.g., "phase_1", "team_selection").
        :param result: The MeetingResult from run_meeting().
        """
        self.phases[phase_name] = result
        self._save_phase(phase_name, result)
    
    def get_previous_context(self, phase_names: Optional[List[str]] = None) -> str:
        """Return formatted context from specified phases.
        
        :param phase_names: List of phase names to include. If None, includes all.
        :return: Formatted string suitable for injecting into the next meeting's agenda.
        """
        if phase_names is None:
            phase_names = list(self.phases.keys())
        
        if not phase_names:
            return ""
        
        context_parts = ["--- PREVIOUS PHASES CONTEXT ---"]
        
        for name in phase_names:
            if name not in self.phases:
                continue
            
            result = self.phases[name]
            structured = result.summary_structured
            
            # Build context from structured data if available
            phase_context = f"\n### {name.upper().replace('_', ' ')}\n"
            
            if structured.get("key_context"):
                phase_context += f"{structured['key_context']}\n"
            
            if structured.get("decisions"):
                phase_context += "\n**Key Decisions:**\n"
                for i, decision in enumerate(structured["decisions"], 1):
                    phase_context += f"  {i}. {decision}\n"
            
            if structured.get("action_items"):
                phase_context += "\n**Action Items:**\n"
                for item in structured["action_items"]:
                    phase_context += f"  - {item}\n"
            
            if structured.get("status"):
                phase_context += f"\n**Status:** {structured['status']}\n"
            
            context_parts.append(phase_context)
        
        context_parts.append("--- END PREVIOUS CONTEXT ---\n")
        return "\n".join(context_parts)
    
    def get_phase(self, phase_name: str) -> Optional[MeetingResult]:
        """Get a specific phase result by name.
        
        :param phase_name: The phase identifier.
        :return: The MeetingResult or None if not found.
        """
        return self.phases.get(phase_name)
    
    def list_phases(self) -> List[str]:
        """List all stored phase names in order of addition."""
        return list(self.phases.keys())
    
    def _save_phase(self, phase_name: str, result: MeetingResult) -> None:
        """Persist a phase result to disk in MD and JSON formats.
        
        :param phase_name: The phase identifier.
        :param result: The MeetingResult to save.
        """
        # Create phase-specific subdirectory
        phase_dir = self.storage_dir / phase_name
        phase_dir.mkdir(parents=True, exist_ok=True)
        
        # Save Markdown (narrative summary + full history)
        md_path = phase_dir / f"{phase_name}_summary.md"
        md_content = self._format_markdown(phase_name, result)
        md_path.write_text(md_content, encoding="utf-8")
        
        # Save JSON (structured data)
        json_path = phase_dir / f"{phase_name}_summary.json"
        json_content = {
            "topic": result.topic,
            "timestamp": result.timestamp,
            "summary_text": result.summary_text,
            "summary_structured": result.summary_structured,
        }
        json_path.write_text(json.dumps(json_content, indent=2), encoding="utf-8")
    
    def _format_markdown(self, phase_name: str, result: MeetingResult) -> str:
        """Format a MeetingResult as a Markdown document.
        
        :param phase_name: The phase identifier.
        :param result: The MeetingResult to format.
        :return: Markdown string.
        """
        lines = [
            f"# Meeting Summary: {result.topic}",
            f"**Phase:** {phase_name}",
            f"**Timestamp:** {result.timestamp}",
            "",
            "## Summary",
            result.summary_text,
            "",
        ]
        
        structured = result.summary_structured
        if structured.get("decisions"):
            lines.append("## Key Decisions")
            for i, decision in enumerate(structured["decisions"], 1):
                lines.append(f"{i}. {decision}")
            lines.append("")
        
        if structured.get("action_items"):
            lines.append("## Action Items")
            for item in structured["action_items"]:
                lines.append(f"- {item}")
            lines.append("")
        
        if structured.get("status"):
            lines.append(f"## Status: {structured['status']}")
            lines.append("")
        
        return "\n".join(lines)
    
    @classmethod
    def load(cls, project_name: str, storage_dir: str) -> "MeetingContext":
        """Reload context from existing files on disk.
        
        :param project_name: Name of the project.
        :param storage_dir: Directory containing persisted phase data.
        :return: A MeetingContext populated with loaded data.
        """
        context = cls(project_name=project_name, storage_dir=storage_dir)
        storage_path = Path(storage_dir)
        
        if not storage_path.exists():
            return context
        
        # Scan for phase subdirectories with JSON files
        for phase_dir in storage_path.iterdir():
            if not phase_dir.is_dir():
                continue
            
            json_file = phase_dir / f"{phase_dir.name}_summary.json"
            if not json_file.exists():
                continue
            
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                # Create a MeetingResult without the chat object (not serializable)
                result = MeetingResult(
                    topic=data.get("topic", phase_dir.name),
                    timestamp=data.get("timestamp", ""),
                    chat=None,  # Chat cannot be reloaded
                    summary_text=data.get("summary_text", ""),
                    summary_structured=data.get("summary_structured", {}),
                )
                context.phases[phase_dir.name] = result
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Could not load phase {phase_dir.name}: {e}")
        
        return context
