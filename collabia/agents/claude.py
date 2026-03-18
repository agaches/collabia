from anthropic import AsyncAnthropicVertex

from collabia.agents.base import AgentAnalysis, AgentCritique, AgentResponse, BaseAgent
from collabia.config import settings
from collabia.utils import parse_json
from collabia.prompts.analyzer import VOTER_SYSTEM, voter_prompt
from collabia.prompts.critic import CRITIC_SYSTEM, critic_prompt
from collabia.prompts.responder import RESPONDER_SYSTEM, responder_prompt


class ClaudeAgent(BaseAgent):
    def __init__(self, agent_id: str, display_name: str, model: str, location: str | None = None):
        super().__init__(agent_id=agent_id, display_name=display_name, model=model)
        self._client = AsyncAnthropicVertex(
            project_id=settings.gcp_project_id,
            region=location or settings.gcp_region,
        )

    async def respond(self, question: str, context: str, round_num: int) -> AgentResponse:
        message = await self._client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=RESPONDER_SYSTEM,
            messages=[{"role": "user", "content": responder_prompt(question, context)}],
        )
        return AgentResponse(
            agent_id=self.agent_id,
            text=message.content[0].text,
            round_num=round_num,
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
        )

    async def critique(self, question: str, responses: dict, round_num: int) -> AgentCritique:
        message = await self._client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=CRITIC_SYSTEM,
            messages=[{"role": "user", "content": critic_prompt(question, responses)}],
        )
        data = parse_json(message.content[0].text)
        return AgentCritique(
            agent_id=self.agent_id,
            critiques=data["critiques"],
            round_num=round_num,
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
        )

    async def analyze(
        self,
        question: str,
        responses: dict,
        critiques: list,
        round_num: int,
    ) -> AgentAnalysis:
        message = await self._client.messages.create(
            model=self.model,
            max_tokens=512,
            system=VOTER_SYSTEM,
            messages=[{"role": "user", "content": voter_prompt(question, responses, critiques)}],
        )
        data = parse_json(message.content[0].text)
        return AgentAnalysis(
            agent_id=self.agent_id,
            eliminate_agent_id=data["eliminate_agent_id"],
            reasoning=data["reasoning"],
            round_num=round_num,
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
        )
