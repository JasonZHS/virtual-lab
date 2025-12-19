"""The LLM agent class."""


class Agent:
    """An LLM agent."""

    def __init__(self, title: str, pmpt_id: str) -> None:
        """Initializes the agent.

        :param title: The title of the agent.
        :param pmpt_id: The prompt ID of the agent.
        """
        self.title = title
        self.pmpt_id = pmpt_id

    def __hash__(self) -> int:
        """Returns the hash of the agent."""
        return hash(self.title)

    def __eq__(self, other: object) -> bool:
        """Checks if the agent is equal to another agent (based on title)."""
        if not isinstance(other, Agent):
            return False

        return (
            self.title == other.title
            and self.pmpt_id == other.pmpt_id
        )

    def __str__(self) -> str:
        """Returns the string representation of the agent (i.e., the agent's title)."""
        return self.title

    def __repr__(self) -> str:
        """Returns the string representation of the agent (i.e., the agent's title)."""
        return self.title
