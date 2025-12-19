"""Runs a meeting with LLM agents using Google GenAI."""

import os
from typing import Literal, List, Dict, Any
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

def run_meeting(
    meeting_type: Literal["team", "individual"],
    agenda: str,
    topic: str = "AlzKB Design",
    team_lead: Agent | None = None,
    team_members: tuple[Agent, ...] | None = None,
    team_member: Agent | None = None,
    num_rounds: int = 1,
    model_name: str = MODEL_FLASH, # Allow selection
    history: List[str] | None = None, # Optional initial history (legacy, or to seed chat)
) -> Any: # Returns the chat object or transcript
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
    :return: The chat object containing history.
    """
    
    # 1. Initialize Client (implicitly uses GOOGLE_API_KEY from env)
    # The user has configured .zshrc, but we also check for .env using load_dotenv just in case.
    # Note: Jupyter kernels might need a restart to pick up new .zshrc changes.
    client = genai.Client()
    
    # 2. Setup Team
    participants = []
    if meeting_type == "team":
        if not team_lead or not team_members:
            raise ValueError("Team meetings require a lead and members.")
        participants = [team_lead] + list(team_members)
    else: # Individual
        if not team_member:
            raise ValueError("Individual meetings require a team_member.")
        participants = [team_member, SCIENTIFIC_CRITIC]

    # 3. Initialize Conversation (Chat Session)
    # We create a chat session. The 'history' logic here is handled by the model.
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
            
            # Base persona instruction
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

    # 5. Summary
    # If team_lead is present (Team meeting), they summarize.
    # If individual meeting, the team_member (e.g. PI) summarizes.
    summarizer = team_lead
    if not summarizer and meeting_type == "individual":
        summarizer = team_member

    if summarizer:
        print("\n--- Generating Summary ---")
        # Use the specific SUMMARY_PROMPT defined in constants
        from alzkb.constants import SUMMARY_PROMPT
        
        summary_instruction = (
            f"ACT AS: {summarizer.title}\n"
            f"{SUMMARY_PROMPT}"
        )
        try:
             response = chat.send_message(summary_instruction)
             if response.text:
                print(f"\n>> SUMMARY ({summarizer.title}):\n{response.text[:200]}...")
        except Exception as e:
            print(f"Error generating summary: {e}")

    return chat # Return the chat object so we can access .get_history()
