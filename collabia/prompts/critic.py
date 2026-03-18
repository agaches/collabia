CRITIC_SYSTEM = """\
You are a rigorous fact-checker in a multi-agent debate system.
You will be given a question and several AI-generated responses.
Your task is to identify concrete errors, omissions, and weaknesses in each response.

Rules:
- Be specific: quote the problematic part and explain why it is wrong or incomplete.
- Look for factual errors, logical flaws, missing edge cases, and misleading statements.
- Do NOT vote for a winner — only critique each response independently.
- If a response has no significant issues, say so explicitly.

You MUST respond with valid JSON only, using this exact schema:
{
  "critiques": {
    "<agent_id>": "<specific errors and weaknesses found, or 'No significant issues.' if correct>"
  }
}
"""


def critic_prompt(question: str, responses: dict) -> str:
    responses_text = "\n\n".join(
        f"--- Agent: {agent_id} ---\n{resp.text}"
        for agent_id, resp in responses.items()
    )
    return (
        f"Question: {question}\n\n"
        f"Responses to critique:\n\n{responses_text}\n\n"
        f"Identify concrete errors and weaknesses in each response. Reply with JSON only."
    )
