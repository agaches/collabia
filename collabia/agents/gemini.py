import json

from google import genai
from google.genai import types

from collabia.agents.base import AgentAnalysis, AgentResponse, BaseAgent
from collabia.config import settings
from collabia.prompts.analyzer import ANALYZER_SYSTEM, analyzer_prompt
from collabia.prompts.responder import RESPONDER_SYSTEM, responder_prompt


class GeminiAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_id="gemini", display_name="Gemini 2.5 Pro")
        self._client = genai.Client(
            vertexai=True,
            project=settings.gcp_project_id,
            location=settings.gcp_region,
        )

    async def respond(self, question: str, context: str, round_num: int) -> AgentResponse:
        response = await self._client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=responder_prompt(question, context),
            config=types.GenerateContentConfig(
                system_instruction=RESPONDER_SYSTEM,
                max_output_tokens=2048,
            ),
        )
        text = response.text
        return AgentResponse(agent_id=self.agent_id, text=text, round_num=round_num)

    async def analyze(
        self,
        question: str,
        responses: dict,
        context: str,
        round_num: int,
    ) -> AgentAnalysis:
        response = await self._client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=analyzer_prompt(question, responses),
            config=types.GenerateContentConfig(
                system_instruction=ANALYZER_SYSTEM,
                max_output_tokens=2048,
                response_mime_type="application/json",
            ),
        )
        data = json.loads(response.text)
        return AgentAnalysis(
            agent_id=self.agent_id,
            preferred_agent_id=data["preferred_agent_id"],
            reasoning=data["reasoning"],
            weaknesses=data["weaknesses"],
            round_num=round_num,
        )
