from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class AgentResponse:
    agent_id: str
    text: str
    round_num: int


@dataclass
class AgentAnalysis:
    agent_id: str
    preferred_agent_id: str
    reasoning: str
    weaknesses: str
    round_num: int


class BaseAgent(ABC):
    def __init__(self, agent_id: str, display_name: str):
        self.agent_id = agent_id
        self.display_name = display_name
        self.is_eliminated: bool = False

    @abstractmethod
    async def respond(self, question: str, context: str, round_num: int) -> AgentResponse: ...

    @abstractmethod
    async def analyze(
        self,
        question: str,
        responses: dict[str, AgentResponse],
        context: str,
        round_num: int,
    ) -> AgentAnalysis: ...

    def __repr__(self) -> str:
        status = "eliminated" if self.is_eliminated else "active"
        return f"{self.__class__.__name__}(id={self.agent_id!r}, status={status})"
