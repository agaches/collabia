import yaml

from collabia.agents.base import BaseAgent
from collabia.agents.generic_gemini import GenericGeminiAgent


def load_agents(yaml_path: str) -> list[BaseAgent]:
    with open(yaml_path) as f:
        config = yaml.safe_load(f)
    agents = []
    for cfg in config["agents"]:
        if cfg["provider"] == "gemini":
            agents.append(GenericGeminiAgent(
                agent_id=cfg["id"],
                display_name=cfg["display_name"],
                model=cfg["model"],
                location=cfg.get("location"),
            ))
        else:
            raise ValueError(f"Unknown provider: {cfg['provider']}")
    return agents
