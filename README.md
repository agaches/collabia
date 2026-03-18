# Collabia

Multi-agent conversational chatbot where several LLMs debate until reaching consensus.

**Core idea:** A single LLM is often imperfect. Multiple AI models that exchange, critique, and vote on each other's answers produce a significantly better final answer.

## How it works

Each round:
1. All active agents answer the question **in parallel**
2. All agents (including eliminated ones) **analyze** all answers and vote for the best
3. If a majority agrees → **consensus reached**, loop ends
4. Otherwise, the worst-performing agent is eliminated and the loop continues

```
Round 1: [Gemini Pro] [Gemini Flash] [Gemini Lite]  → vote → no consensus → eliminate worst
Round 2: [Gemini Pro] [Gemini Flash]                 → vote → consensus ✓
```

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
| `--rounds` / `-r` | `5` | Max consensus rounds |
| `--verbose` / `-v` | off | Show full responses and analysis details |
