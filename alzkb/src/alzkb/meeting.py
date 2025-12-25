"""Runs a meeting with LLM agents using Google GenAI."""

import os
from typing import Literal, List, Dict, Any, Union
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from alzkb.agents import Agent
from alzkb.constants import (
    MODEL_FLASH,
    SCIENTIFIC_CRITIC,
    PRINCIPAL_INVESTIGATOR,
)
from alzkb.meeting_result import MeetingResult, create_meeting_result


def run_meeting(
    meeting_type: Literal["team", "individual"],
    agenda: str,
    topic: str = "AlzKB Design",
    team_lead: Agent | None = None,
    team_members: tuple[Agent, ...] | None = None,
    team_member: Agent | None = None,
    num_rounds: int = 1,
    model_name: str = MODEL_FLASH,
    history: List[str] | None = None,
    generate_summaries: bool = True,
) -> MeetingResult:
    """
    Runs a meeting (multi-agent discussion) using Google Gemini Chat.

    :param meeting_type: "team" or "individual"
    :param agenda: The main goal/prompt for the meeting.
    :param topic: The topic of the meeting.
    :param team_lead: The lead agent (for team meetings).
    :param team_members: Tuple of member agents (for team meetings).
    :param team_member: The singular agent (for individual meetings).
    :param num_rounds: Number of discussion rounds.
    :param model_name: The Gemini model to use.
    :param history: Optional list of strings to seed the chat context.
    :param generate_summaries: Whether to generate narrative and structured summaries.
    :return: MeetingResult containing chat, summaries, and metadata.
    """
    
    # 1. Initialize Client (implicitly uses GOOGLE_API_KEY from env)
    client = genai.Client()
    
    # 2. Setup Team
    participants = []
    if meeting_type == "team":
        if not team_lead or not team_members:
            raise ValueError("Team meetings require a lead and members.")
        participants = [team_lead] + list(team_members)
    else:  # Individual
        if not team_member:
            raise ValueError("Individual meetings require a team_member.")
        participants = [team_member, SCIENTIFIC_CRITIC]

    # 3. Initialize Conversation (Chat Session)
    chat = client.chats.create(model=model_name)
    
    # Context string
    meeting_context = f"--- MEETING START: {topic} ---\nAGENDA: {agenda}\n"
    if history:
        meeting_context = "\n".join(history) + "\n" + meeting_context
        
    print(f"Starting {meeting_type} meeting on: {topic}")
    
    # 4. Meeting Loop
    for round_idx in range(num_rounds):
        print(f"\n--- Round {round_idx + 1}/{num_rounds} ---")
        
        for i, agent in enumerate(participants):
            # Construct the specific prompt for this agent's turn.
            turn_prompt = (
                f"ACT AS: {agent.title}\n"
                f"YOUR SPECIFIC INSTRUCTIONS: {agent.system_prompt}\n"
            )

            # If this is the VERY FIRST turn of the ENTIRE meeting, inject the context here.
            if round_idx == 0 and i == 0:
                turn_prompt += f"\n{meeting_context}\n"
            
            turn_prompt += (
                f"TASK: Contribute to the discussion above based on your expertise. "
                f"If you agree and have nothing to add, say 'Pass'.\n"
            )
            
            try:
                response = chat.send_message(turn_prompt)
                if response.text:
                    print(f"\n>> {agent.title}:\n{response.text[:200]}...")
                else:
                    print(f"\n>> {agent.title}: [No text response]")
            except Exception as e:
                print(f"Error calling model for {agent.title}: {e}")

    # 5. Determine summarizer
    summarizer = team_lead if team_lead else team_member
    summarizer_title = summarizer.title if summarizer else "System"

    # 6. Generate MeetingResult with summaries
    print("\n--- Generating Summaries ---")
    result = create_meeting_result(
        topic=topic,
        chat=chat,
        summarizer_title=summarizer_title,
        model_name=model_name,
        generate_summaries=generate_summaries,
    )
    
    if result.summary_text:
        print(f"\n>> SUMMARY:\n{result.summary_text[:300]}...")
    
    return result
