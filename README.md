# Collabia

Multi-agent debate system where several LLMs critique each other's answers and iteratively eliminate the weakest response until one winner remains.

**Core idea:** A single LLM is often imperfect. Multiple AI models that exchange, critique, and vote against each other's weaknesses produce a significantly better final answer through iterative elimination.

## How it works

Each round has 3 phases:

1. **Respond** — all active agents answer the question in parallel
2. **Critique** — all agents (including eliminated ones) identify concrete errors and weaknesses in each response
3. **Eliminate** — all agents vote to remove the worst response; the agent with the most votes against them is eliminated

The loop continues until only one agent remains (the winner), or `max_rounds` is reached.

```
Round 1: [Gemini Pro] [Gemini Flash] [Gemini Lite]
         → critique each response
         → vote: eliminate Gemini Lite (weakest)

Round 2: [Gemini Pro] [Gemini Flash]
         → critique each response
         → vote: eliminate Gemini Flash

Winner: Gemini Pro ✓
```

Eliminated agents can no longer respond but still participate in critique and voting — their judgment still counts.

## Prerequisites

**1. GCP project with Vertex AI**

```bash
# Create a project and enable Vertex AI
gcloud projects create your-project-id --name="Your Project"
gcloud billing projects link your-project-id --billing-account=YOUR_BILLING_ACCOUNT_ID
gcloud services enable aiplatform.googleapis.com --project=your-project-id
```

Then open `console.cloud.google.com/vertex-ai?project=your-project-id` to accept the Terms of Service.

**2. Application Default Credentials**

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project your-project-id
```

**3. uv** — Python package manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

```bash
git clone <repo>
cd collabia
cp .env.example .env
# Edit .env: set GCP_PROJECT_ID=your-project-id
uv sync
```

## Configuration

`.env` file:

| Variable | Default | Description |
|---|---|---|
| `GCP_PROJECT_ID` | *(required)* | Your GCP project ID |
| `GCP_REGION` | `us-central1` | Vertex AI region |
| `GEMINI_MODEL` | `gemini-2.5-pro` | Primary agent model |
| `GEMINI_FLASH_MODEL` | `gemini-2.5-flash` | Secondary agent model |
| `GEMINI_LITE_MODEL` | `gemini-3.1-flash-lite-preview` | Third agent model |
| `MAX_ROUNDS` | `5` | Maximum debate rounds |

## Usage

**Verify setup:**
```bash
uv run collabia check-auth
```

**Ask a question:**
```bash
uv run collabia "What is the best way to learn machine learning?"
```

**With options:**
```bash
uv run collabia "Is Python better than JavaScript?" --rounds 3 --verbose
```

| Option | Default | Description |
|---|---|---|
| `--rounds` / `-r` | `5` | Max elimination rounds |
| `--verbose` / `-v` | off | Show full responses, critiques, and vote details |
