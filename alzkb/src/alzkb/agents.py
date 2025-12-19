"""The LLM agent class."""

class Agent:
    """An LLM agent."""

    def __init__(self, title: str, system_prompt: str) -> None:
        """Initializes the agent.

        :param title: The title of the agent (used for identity).
        :param system_prompt: The specific instructions/persona for the agent.
        """
        self.title = title
        self.system_prompt = system_prompt

    def __hash__(self) -> int:
        """Returns the hash of the agent."""
        return hash(self.title)

    def __eq__(self, other: object) -> bool:
        """Checks if the agent is equal to another agent (based on title)."""
        if not isinstance(other, Agent):
            return False

        return self.title == other.title

    def __str__(self) -> str:
        """Returns the string representation of the agent (i.e., the agent's title)."""
        return self.title

    def __repr__(self) -> str:
        """Returns the string representation of the agent (i.e., the agent's title)."""
        return self.title
