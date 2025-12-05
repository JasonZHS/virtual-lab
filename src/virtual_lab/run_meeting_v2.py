"""Runs a meeting with LLM agents (v2, simpler and more explicit orchestration)."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Literal, Iterable

from openai import OpenAI

from virtual_lab.agent import Agent
from virtual_lab.constants import (
    CONSISTENT_TEMPERATURE,
    DEFAULT_MODEL,
    MODEL_TO_INPUT_PRICE_PER_TOKEN,
    MODEL_TO_OUTPUT_PRICE_PER_TOKEN,
)
from virtual_lab.prompts import SCIENTIFIC_CRITIC
from virtual_lab.utils import save_meeting


# ---------------------------------------------------------------------------
# Small formatting helpers
# ---------------------------------------------------------------------------


def _format_block(title: str, lines: Iterable[str]) -> str:
    """Format a titled block, skipping empty content."""
    text = "\n".join(line for line in lines if line.strip())
    if not text.strip():
        return ""
    return f"{title}\n{text}\n\n"


def _format_contexts(contexts: tuple[str, ...]) -> str:
    return _format_block(
        "CONTEXT:",
        [f"- {ctx}" for ctx in contexts],
    )


def _format_summaries(summaries: tuple[str, ...]) -> str:
    return _format_block(
        "SUMMARIES OF PREVIOUS MEETINGS:",
        [f"- {summary}" for summary in summaries],
    )


def _format_agenda(agenda: str) -> str:
    return _format_block("AGENDA:", [agenda])


def _format_questions(questions: tuple[str, ...]) -> str:
    return _format_block(
        "AGENDA QUESTIONS (must be answered by the end of the meeting):",
        [f"{i+1}. {q}" for i, q in enumerate(questions)],
    )


def _format_rules(rules: tuple[str, ...]) -> str:
    return _format_block(
        "MEETING RULES (must be followed):",
        [f"- {r}" for r in rules],
    )


def _format_discussion_for_prompt(
    discussion: list[dict[str, str]],
    max_chars: int = 6000,
) -> str:
    """
    Render the current discussion as text for inclusion in a new prompt.

    We truncate from the beginning if the discussion becomes too long,
    to avoid blowing up the context window.
    """
    lines: list[str] = []
    for turn in discussion:
        lines.append(f"{turn['agent']}: {turn['message']}".strip())

    full_text = "\n\n".join(lines)
    if len(full_text) <= max_chars:
        return full_text

    # Truncate from the beginning
    return full_text[-max_chars:]


def _choose_model(explicit_model: str | None, *agents: Agent | None) -> str:
    """
    Decide which model to use:
      1. Explicit `model` argument if provided
      2. First non-empty `agent.model`
      3. DEFAULT_MODEL from constants
    """
    if explicit_model:
        return explicit_model

    for agent in agents:
        if agent is not None and getattr(agent, "model", None):
            return agent.model

    return DEFAULT_MODEL


def _print_usage_and_cost(
    model: str,
    total_prompt_tokens: int,
    total_completion_tokens: int,
    elapsed_seconds: float,
) -> None:
    """Print token usage, approximate USD cost, and elapsed time."""
    input_price = MODEL_TO_INPUT_PRICE_PER_TOKEN.get(model)
    output_price = MODEL_TO_OUTPUT_PRICE_PER_TOKEN.get(model)

    cost_str = "Cost: unknown (no pricing for this model)."
    if input_price is not None and output_price is not None:
        cost = total_prompt_tokens * input_price + total_completion_tokens * output_price
        cost_str = f"Cost: ${cost:.2f}"

    print(
        f"Input token count: {total_prompt_tokens:,}\n"
        f"Output token count: {total_completion_tokens:,}\n"
        f"{cost_str}"
    )
    minutes = int(elapsed_seconds // 60)
    seconds = int(elapsed_seconds % 60)
    print(f"Time: {minutes}:{seconds:02d}")


# ---------------------------------------------------------------------------
# Core orchestration
# ---------------------------------------------------------------------------


def run_meeting(
    meeting_type: Literal["team", "individual"],
    agenda: str,
    save_dir: Path,
    save_name: str = "discussion",
    team_lead: Agent | None = None,
    team_members: tuple[Agent, ...] | None = None,
    team_member: Agent | None = None,
    agenda_questions: tuple[str, ...] = (),
    agenda_rules: tuple[str, ...] = (),
    summaries: tuple[str, ...] = (),
    contexts: tuple[str, ...] = (),
    num_rounds: int = 0,
    temperature: float = CONSISTENT_TEMPERATURE,
    pubmed_search: bool = False,  # v2: used only as textual hint, no real tool calls
    return_summary: bool = False,
    model: str | None = None,
) -> str | None:
    """
    Runs a meeting with LLM agents (v2).

    This implementation keeps the same parameters as v1 but uses a simpler,
    explicit orchestration on top of `chat.completions`.

    For `meeting_type == "individual"`:
        - `team_member` is the main agent.
        - A built-in `SCIENTIFIC_CRITIC` provides critique and suggestions.
        - The main agent then revises its answer.
        - This pattern is repeated for `max(num_rounds, 1)` rounds.
        - The last message from the main agent is treated as the "summary".

    For `meeting_type == "team"`:
        - `team_lead` + `team_members` participate.
        - Each round, all participants speak in order.
        - After all rounds, `team_lead` produces a final structured summary.
        - The final summary is the last message.

    The entire discussion is saved (JSON + Markdown) via `save_meeting`.

    :param meeting_type: "team" or "individual".
    :param agenda: The agenda for the meeting.
    :param save_dir: Directory to save the discussion.
    :param save_name: Base name for the saved files (without extension).
    :param team_lead: Team lead for team meetings.
    :param team_members: Team members for team meetings.
    :param team_member: Single agent for individual meetings.
    :param agenda_questions: Questions that must be answered.
    :param agenda_rules: Rules that must be followed.
    :param summaries: Summaries of previous meetings.
    :param contexts: Additional context strings.
    :param num_rounds: Number of discussion rounds (0 => treated as 1).
    :param temperature: Sampling temperature for all calls.
    :param pubmed_search: If True, we tell the model it can conceptually
                          draw on PubMed knowledge, but v2 does not
                          actually call external tools.
    :param return_summary: If True, return the final summary message string.
    :param model: Optional explicit model name to use. If not provided,
                  we fall back to agents' `.model` fields or DEFAULT_MODEL.
    :return: Final summary string if `return_summary` else None.
    """
    # ------------------------
    # Basic argument validation
    # ------------------------
    if meeting_type == "team":
        if team_lead is None or team_members is None or len(team_members) == 0:
            raise ValueError("Team meeting requires team_lead and non-empty team_members.")
        if team_member is not None:
            raise ValueError("Team meeting does not use `team_member`.")
        if team_lead in team_members:
            raise ValueError("team_lead must be separate from team_members.")
        if len(set(team_members)) != len(team_members):
            raise ValueError("team_members must be unique.")
    elif meeting_type == "individual":
        if team_member is None:
            raise ValueError("Individual meeting requires `team_member`.")
        if team_lead is not None or team_members is not None:
            raise ValueError("Individual meeting does not use `team_lead` or `team_members`.")
    else:
        raise ValueError(f"Invalid meeting_type: {meeting_type!r}")

    # Ensure at least one round
    total_rounds = max(1, num_rounds)

    # Choose model
    if meeting_type == "individual":
        used_model = _choose_model(model, team_member)
    else:
        used_model = _choose_model(model, team_lead, *(team_members or ()))

    # Build the static "header" text that all agents will see
    header_parts = [
        _format_contexts(contexts),
        _format_summaries(summaries),
        _format_agenda(agenda),
        _format_questions(agenda_questions),
        _format_rules(agenda_rules),
    ]
    if pubmed_search:
        header_parts.append(
            "NOTE: You may conceptually draw on the biomedical literature (e.g. PubMed) "
            "and assume access to typical knowledge from recent publications, but you "
            "must still explain your reasoning in detail.\n\n"
        )
    header_text = "".join(header_parts).strip()

    # Discussion transcript we will save
    discussion: list[dict[str, str]] = []
    if header_text:
        discussion.append({"agent": "User", "message": header_text})

    client = OpenAI()
    start_time = time.time()
    total_prompt_tokens = 0
    total_completion_tokens = 0

    # ------------------------------------------------------------------
    # INDIVIDUAL MEETING: agent + critic + agent revision per round
    # ------------------------------------------------------------------
    if meeting_type == "individual":
        main_agent = team_member  # type: ignore[assignment]
        critic_agent = SCIENTIFIC_CRITIC

        for round_idx in range(total_rounds):
            # Main agent draft or refinement
            round_label = f"ROUND {round_idx + 1}/{total_rounds}"
            previous_text = _format_discussion_for_prompt(discussion)

            if round_idx == 0:
                instruction = (
                    f"{round_label} — Initial answer.\n"
                    "You are the primary scientist for this meeting.\n"
                    "Provide a detailed, technically rigorous response to the agenda.\n"
                    "Explicitly address all agenda questions and follow all meeting rules.\n"
                    "Your answer should be structured, step-by-step, and implementable."
                )
            else:
                instruction = (
                    f"{round_label} — Refined answer.\n"
                    "Improve and refine your previous answer given all prior discussion.\n"
                    "Clarify assumptions, add missing details, and fix any issues that "
                    "were revealed earlier.\n"
                    "At the end, present a consolidated, self-contained answer."
                )

            user_content = (
                f"{header_text}\n\n"
                f"PREVIOUS DISCUSSION:\n{previous_text or 'None yet.'}\n\n"
                f"{instruction}"
            )

            resp = client.chat.completions.create(
                model=used_model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": main_agent.prompt},
                    {"role": "user", "content": user_content},
                ],
            )

            message = resp.choices[0].message.content or ""
            discussion.append({"agent": main_agent.title, "message": message})

            if resp.usage:
                total_prompt_tokens += resp.usage.prompt_tokens or 0
                total_completion_tokens += resp.usage.completion_tokens or 0

            # Critic then analyses and suggests improvements
            previous_text = _format_discussion_for_prompt(discussion)
            critic_instruction = (
                f"{round_label} — Critique.\n"
                "Carefully critique the primary scientist's most recent answer.\n"
                "Identify weaknesses, missing considerations, questionable assumptions, "
                "and possible failure modes.\n"
                "Suggest concrete, actionable improvements. Do NOT rewrite the answer "
                "yourself; focus purely on critique and guidance."
            )
            critic_user_content = (
                f"{header_text}\n\n"
                f"PREVIOUS DISCUSSION:\n{previous_text}\n\n"
                f"{critic_instruction}"
            )

            resp_critic = client.chat.completions.create(
                model=used_model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": critic_agent.prompt},
                    {"role": "user", "content": critic_user_content},
                ],
            )

            critic_message = resp_critic.choices[0].message.content or ""
            discussion.append({"agent": critic_agent.title, "message": critic_message})

            if resp_critic.usage:
                total_prompt_tokens += resp_critic.usage.prompt_tokens or 0
                total_completion_tokens += resp_critic.usage.completion_tokens or 0

            # Final refinement by main agent in this round
            previous_text = _format_discussion_for_prompt(discussion)
            refinement_instruction = (
                f"{round_label} — Apply critique.\n"
                "Revise and improve your earlier answer based on the critic's feedback.\n"
                "You may substantially restructure your answer if needed.\n"
                "Ensure the result is clear, rigorous, and directly addresses the agenda "
                "and all agenda questions.\n"
                "This revised answer will replace your earlier answer for this round."
            )
            refinement_user_content = (
                f"{header_text}\n\n"
                f"PREVIOUS DISCUSSION:\n{previous_text}\n\n"
                f"{refinement_instruction}"
            )

            resp_refined = client.chat.completions.create(
                model=used_model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": main_agent.prompt},
                    {"role": "user", "content": refinement_user_content},
                ],
            )

            refined_message = resp_refined.choices[0].message.content or ""
            discussion.append({"agent": main_agent.title, "message": refined_message})

            if resp_refined.usage:
                total_prompt_tokens += resp_refined.usage.prompt_tokens or 0
                total_completion_tokens += resp_refined.usage.completion_tokens or 0

        # The final message from main_agent is treated as summary
        final_summary = discussion[-1]["message"]

    # ------------------------------------------------------------------
    # TEAM MEETING: multiple agents + final team_lead summary
    # ------------------------------------------------------------------
    else:  # meeting_type == "team"
        assert team_lead is not None
        assert team_members is not None

        participants: list[Agent] = [team_lead] + list(team_members)

        for round_idx in range(total_rounds):
            round_label = f"ROUND {round_idx + 1}/{total_rounds}"
            for agent in participants:
                previous_text = _format_discussion_for_prompt(discussion)

                if round_idx == 0:
                    if agent is team_lead:
                        instruction = (
                            f"{round_label} — Kickoff as Team Lead.\n"
                            "Propose an overall strategy and structure for addressing the agenda.\n"
                            "Highlight key decisions that need to be made and the roles of "
                            "each team member.\n"
                            "Provide an initial plan that the team can refine."
                        )
                    else:
                        instruction = (
                            f"{round_label} — Initial contribution as {agent.title}.\n"
                            "Provide your expert perspective on the agenda.\n"
                            "Identify key technical issues, risks, and opportunities "
                            "from your area of expertise.\n"
                            "Respond to any relevant agenda questions."
                        )
                else:
                    if agent is team_lead:
                        instruction = (
                            f"{round_label} — Integrate and steer the discussion.\n"
                            "Summarize the most important points raised so far, identify "
                            "agreements and disagreements, and propose next steps.\n"
                            "Refine the overall plan and keep the team focused on the agenda "
                            "and agenda questions."
                        )
                    else:
                        instruction = (
                            f"{round_label} — Follow-up as {agent.title}.\n"
                            "React to previous discussion, refine your earlier suggestions, "
                            "and address any open questions or concerns.\n"
                            "Be concrete and actionable."
                        )

                user_content = (
                    f"{header_text}\n\n"
                    f"PREVIOUS DISCUSSION:\n{previous_text or 'None yet.'}\n\n"
                    f"{instruction}"
                )

                resp = client.chat.completions.create(
                    model=used_model,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": agent.prompt},
                        {"role": "user", "content": user_content},
                    ],
                )

                message = resp.choices[0].message.content or ""
                discussion.append({"agent": agent.title, "message": message})

                if resp.usage:
                    total_prompt_tokens += resp.usage.prompt_tokens or 0
                    total_completion_tokens += resp.usage.completion_tokens or 0

        # Final structured summary by team_lead
        previous_text = _format_discussion_for_prompt(discussion)
        summary_instruction = (
            "FINAL SUMMARY.\n"
            "As the team lead, write a clear, structured summary of the meeting.\n"
            "You MUST:\n"
            "  - Summarize the main ideas and decisions.\n"
            "  - Explicitly answer all agenda questions.\n"
            "  - Highlight open issues and proposed next steps.\n"
            "  - Keep the summary self-contained (can be read without the transcript)."
        )
        summary_user_content = (
            f"{header_text}\n\n"
            f"FULL DISCUSSION (truncated if very long):\n{previous_text}\n\n"
            f"{summary_instruction}"
        )

        resp_summary = client.chat.completions.create(
            model=used_model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": team_lead.prompt},
                {"role": "user", "content": summary_user_content},
            ],
        )

        final_summary = resp_summary.choices[0].message.content or ""
        discussion.append({"agent": team_lead.title, "message": final_summary})

        if resp_summary.usage:
            total_prompt_tokens += resp_summary.usage.prompt_tokens or 0
            total_completion_tokens += resp_summary.usage.completion_tokens or 0

    # ------------------------------------------------------------------
    # Save + usage / cost reporting
    # ------------------------------------------------------------------
    elapsed = time.time() - start_time
    save_meeting(save_dir=save_dir, save_name=save_name, discussion=discussion)
    _print_usage_and_cost(
        model=used_model,
        total_prompt_tokens=total_prompt_tokens,
        total_completion_tokens=total_completion_tokens,
        elapsed_seconds=elapsed,
    )

    return final_summary if return_summary else None
