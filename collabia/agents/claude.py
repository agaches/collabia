import json

from anthropic import AsyncAnthropicVertex

from collabia.agents.base import AgentAnalysis, AgentResponse, BaseAgent
from collabia.config import settings
from collabia.prompts.analyzer import ANALYZER_SYSTEM, analyzer_prompt
from collabia.prompts.responder import RESPONDER_SYSTEM, responder_prompt


class ClaudeAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_id="claude", display_name="Claude Sonnet")
        self._client = AsyncAnthropicVertex(
            project_id=settings.gcp_project_id,
            region=settings.gcp_region,
        )

    async def respond(self, question: str, context: str, round_num: int) -> AgentResponse:
        message = await self._client.messages.create(
            model=settings.claude_model,
            max_tokens=2048,
            system=RESPONDER_SYSTEM,
            messages=[{"role": "user", "content": responder_prompt(question, context)}],
        )
        text = message.content[0].text
        return AgentResponse(agent_id=self.agent_id, text=text, round_num=round_num)

    async def analyze(
        self,
        question: str,
        responses: dict,
        context: str,
        round_num: int,
    ) -> AgentAnalysis:
        message = await self._client.messages.create(
            model=settings.claude_model,
            max_tokens=1024,
            system=ANALYZER_SYSTEM,
            messages=[{"role": "user", "content": analyzer_prompt(question, responses)}],
        )
        raw = message.content[0].text
        data = json.loads(raw)
        return AgentAnalysis(
            agent_id=self.agent_id,
            preferred_agent_id=data["preferred_agent_id"],
            reasoning=data["reasoning"],
            weaknesses=data["weaknesses"],
            round_num=round_num,
        )
