import google.auth
import google.auth.transport.requests
import httpx

from collabia.agents.base import AgentAnalysis, AgentCritique, AgentResponse, BaseAgent
from collabia.config import settings
from collabia.utils import parse_json
from collabia.prompts.analyzer import VOTER_SYSTEM, voter_prompt
from collabia.prompts.critic import CRITIC_SYSTEM, critic_prompt
from collabia.prompts.responder import RESPONDER_SYSTEM, responder_prompt


class MistralVertexAgent(BaseAgent):
    def __init__(self, agent_id: str, display_name: str, model: str, location: str | None = None):
        super().__init__(agent_id=agent_id, display_name=display_name, model=model)
        self.location = location or settings.gcp_region
        self._credentials = None
        self._auth_request = google.auth.transport.requests.Request()

    def _get_token(self) -> str:
        if self._credentials is None:
            self._credentials, _ = google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        if not self._credentials.valid:
            self._credentials.refresh(self._auth_request)
        return self._credentials.token

    def _url(self) -> str:
        return (
            f"https://{self.location}-aiplatform.googleapis.com/v1"
            f"/projects/{settings.gcp_project_id}"
            f"/locations/{self.location}"
            f"/publishers/mistralai/models/{self.model}:rawPredict"
        )

    async def _chat(
        self,
        system: str,
        user_content: str,
        max_tokens: int = 2048,
        json_mode: bool = False,
    ) -> tuple[str, int, int]:
        payload: dict = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_content},
            ],
            "max_tokens": max_tokens,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                self._url(),
                json=payload,
                headers={
                    "Authorization": f"Bearer {self._get_token()}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()

        text = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        return text, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)

    async def respond(self, question: str, context: str, round_num: int) -> AgentResponse:
        text, inp, out = await self._chat(
            system=RESPONDER_SYSTEM,
            user_content=responder_prompt(question, context),
            max_tokens=2048,
        )
        return AgentResponse(
            agent_id=self.agent_id, text=text, round_num=round_num,
            input_tokens=inp, output_tokens=out,
        )

    async def critique(self, question: str, responses: dict, round_num: int) -> AgentCritique:
        text, inp, out = await self._chat(
            system=CRITIC_SYSTEM,
            user_content=critic_prompt(question, responses),
            max_tokens=1024,
            json_mode=True,
        )
        data = parse_json(text)
        return AgentCritique(
            agent_id=self.agent_id, critiques=data["critiques"], round_num=round_num,
            input_tokens=inp, output_tokens=out,
        )

    async def analyze(
        self, question: str, responses: dict, critiques: list, round_num: int
    ) -> AgentAnalysis:
        text, inp, out = await self._chat(
            system=VOTER_SYSTEM,
            user_content=voter_prompt(question, responses, critiques),
            max_tokens=512,
            json_mode=True,
        )
        data = parse_json(text)
        return AgentAnalysis(
            agent_id=self.agent_id,
            eliminate_agent_id=data["eliminate_agent_id"],
            reasoning=data["reasoning"],
            round_num=round_num,
            input_tokens=inp, output_tokens=out,
        )
