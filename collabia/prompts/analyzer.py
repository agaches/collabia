VOTER_SYSTEM = """\
You are a judge in a multi-agent debate system.
You will be given a question, several AI-generated responses, and critiques of each response written by other agents.
Your task is to identify the WORST response — the one that should be eliminated from the debate.

Consider: factual errors, logical flaws, omissions, misleading statements, and overall usefulness.

You MUST respond with valid JSON only, using this exact schema:
{
  "eliminate_agent_id": "<agent_id of the worst response to eliminate>",
  "reasoning": "<why this response is the weakest>"
}
"""


def voter_prompt(question: str, responses: dict, critiques: list) -> str:
    responses_text = "\n\n".join(
        f"--- Agent: {agent_id} ---\n{resp.text}"
        for agent_id, resp in responses.items()
    )
    critiques_text = ""
    for critique in critiques:
        critiques_text += f"\n\n=== Critiques by {critique.agent_id} ===\n"
        for agent_id, text in critique.critiques.items():
            critiques_text += f"  [{agent_id}]: {text}\n"

    return (
        f"Question: {question}\n\n"
        f"Responses:\n\n{responses_text}\n\n"
        f"Critiques from all agents:{critiques_text}\n\n"
        f"Select the WORST response to eliminate. Reply with JSON only."
    )
