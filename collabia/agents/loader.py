import yaml

from collabia.agents.base import BaseAgent
from collabia.agents.claude import ClaudeAgent
from collabia.agents.generic_gemini import GenericGeminiAgent
from collabia.agents.mistral import MistralVertexAgent


def load_agents(yaml_path: str) -> list[BaseAgent]:
    with open(yaml_path) as f:
        config = yaml.safe_load(f)
    agents = []
    for cfg in config["agents"]:
        provider = cfg["provider"]
        common = dict(
            agent_id=cfg["id"],
            display_name=cfg["display_name"],
            model=cfg["model"],
            location=cfg.get("location"),
        )
        if provider == "gemini":
            agents.append(GenericGeminiAgent(**common))
        elif provider == "claude":
            agents.append(ClaudeAgent(**common))
        elif provider == "mistral":
            agents.append(MistralVertexAgent(**common))
        else:
            raise ValueError(f"Unknown provider: {provider!r}")
    return agents
