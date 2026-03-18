RESPONDER_SYSTEM = """\
You are a highly capable AI assistant participating in a multi-agent consensus debate.
Your goal is to provide the best possible answer to the user's question.
Be thorough, accurate, and well-structured. You may refine your answer based on prior context.
"""


def responder_prompt(question: str, context: str) -> str:
    if context:
        return (
            f"Previous best answer from prior round:\n{context}\n\n"
            f"Now provide your own best answer to the following question. "
            f"You may improve upon the prior answer or take a different angle if you see fit.\n\n"
            f"Question: {question}"
        )
    return f"Question: {question}"
