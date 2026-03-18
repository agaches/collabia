"""Pricing table for Vertex AI models.

Prices in USD per million tokens — update as needed.
Sources: Vertex AI pricing pages (2026-03).
"""

# model_id → (input_usd_per_M, output_usd_per_M)
PRICING: dict[str, tuple[float, float]] = {
    # Claude on Vertex AI
    "claude-sonnet-4-5": (3.0, 15.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    # Gemini on Vertex AI
    "gemini-2.5-pro": (1.25, 10.0),
    "gemini-2.5-flash": (0.30, 2.50),
    "gemini-3.1-flash-lite-preview": (0.25, 1.50),
    # Mistral on Vertex AI
    "mistral-medium-3": (0.40, 2.00),
}

USD_TO_EUR = 0.92  # approximate — update periodically


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    if model not in PRICING:
        return 0.0
    inp, out = PRICING[model]
    return (input_tokens * inp + output_tokens * out) / 1_000_000


def cost_eur(model: str, input_tokens: int, output_tokens: int) -> float:
    return cost_usd(model, input_tokens, output_tokens) * USD_TO_EUR
