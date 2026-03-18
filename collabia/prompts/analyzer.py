ANALYZER_SYSTEM = """\
You are an expert evaluator in a multi-agent consensus system.
You will be given a question and several AI-generated responses.
Your task is to select the best response and explain your reasoning.

You MUST respond with valid JSON only, using this exact schema:
{
  "preferred_agent_id": "<agent_id of the best response>",
  "reasoning": "<why this response is best>",
  "weaknesses": "<weaknesses of the other responses, or weaknesses of the chosen one>"
}
"""


def analyzer_prompt(question: str, responses: dict) -> str:
    responses_text = "\n\n".join(
        f"--- Agent: {agent_id} ---\n{resp.text}"
        for agent_id, resp in responses.items()
    )
    return (
        f"Question: {question}\n\n"
        f"Responses to evaluate:\n\n{responses_text}\n\n"
        f"Select the best response. Reply with JSON only."
    )
