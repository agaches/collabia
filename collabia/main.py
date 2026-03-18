import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console

from collabia.config import settings
from collabia.display.terminal import Display

app = typer.Typer(
    help="Collabia — multi-agent consensus chatbot",
    no_args_is_help=True,
)
console = Console()

DEFAULT_CONFIG = "agents/default.yaml"


def _make_agents(config_path: str):
    from collabia.agents.loader import load_agents

    return load_agents(config_path)


def _save_result(question: str, config_path: str, result, agents) -> Path:
    from collabia.pricing import cost_eur

    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    config_label = Path(config_path).stem
    out_dir = Path("tests/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{ts}_{config_label}.json"

    cost_breakdown = [
        {
            "agent_id": m.agent_id,
            "model": m.model,
            "input_tokens": m.input_tokens,
            "output_tokens": m.output_tokens,
            "cost_eur": round(cost_eur(m.model, m.input_tokens, m.output_tokens), 6),
        }
        for m in result.metrics.values()
    ]

    data = {
        "question": question,
        "config": config_path,
        "timestamp": datetime.now().isoformat(),
        "rounds_run": result.winner.round_num,
        "winner": {
            "agent_id": result.winner.agent_id,
            "model": next((a.model for a in agents if a.agent_id == result.winner.agent_id), ""),
            "text": result.winner.text,
        },
        "first_response": (
            {
                "agent_id": result.first_response.agent_id,
                "text": result.first_response.text,
            }
            if result.first_response
            else None
        ),
        "cost_breakdown": cost_breakdown,
        "total_cost_eur": round(result.total_cost_eur(), 6),
    }

    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return out_path


@app.command(name="ask", help="Ask a question and run the consensus loop.")
def ask(
    question: str = typer.Argument(..., help="The question to ask"),
    rounds: int = typer.Option(settings.max_rounds, "--rounds", "-r", help="Max consensus rounds"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show full responses and analyses"),
    config: str = typer.Option(DEFAULT_CONFIG, "--config", "-c", help="Path to agents YAML config"),
    save: bool = typer.Option(False, "--save", "-s", help="Save result to tests/results/"),
):
    async def _run():
        agents = _make_agents(config)
        display = Display(verbose=verbose)
        from collabia.consensus.loop import run_consensus

        result = await run_consensus(
            question=question,
            agents=agents,
            max_rounds=rounds,
            display=display,
            verbose=verbose,
        )
        if result.first_response:
            display.show_before_after(result.first_response, result.winner, agents)
        else:
            display.show_final_answer(result.winner, agents)

        display.show_cost_breakdown(result.metrics)

        if save:
            path = _save_result(question, config, result, agents)
            console.print(f"\n[dim]Saved → {path}[/]")

    asyncio.run(_run())


@app.command(name="benchmark", help="Run the same question on multiple configs and compare responses.")
def benchmark(
    question: str = typer.Argument(..., help="The question to ask"),
    rounds: int = typer.Option(settings.max_rounds, "--rounds", "-r", help="Max consensus rounds"),
    configs: list[str] = typer.Option(
        [DEFAULT_CONFIG, "agents/3xlite.yaml"],
        "--config",
        "-c",
        help="Agent YAML configs to compare (repeat for multiple)",
    ),
    save: bool = typer.Option(False, "--save", "-s", help="Save each result to tests/results/"),
):
    async def _run():
        display = Display()
        from collabia.consensus.loop import run_consensus

        results = []
        for config_path in configs:
            console.rule(f"[bold cyan]Running: {config_path}[/]")
            agents = _make_agents(config_path)
            result = await run_consensus(
                question=question,
                agents=agents,
                max_rounds=rounds,
                display=display,
                verbose=False,
            )
            results.append((config_path, result.first_response, result.winner, result.metrics, agents))

            if save:
                path = _save_result(question, config_path, result, agents)
                console.print(f"[dim]Saved → {path}[/]")

        display.show_benchmark([(c, f, w) for c, f, w, _, _ in results])

        # Cost comparison across configs
        console.rule("[bold cyan]Cost comparison[/]")
        for config_path, _, _, metrics, _ in results:
            console.print(f"\n[bold]{config_path}[/]")
            display.show_cost_breakdown(metrics)

    asyncio.run(_run())


@app.command(name="check-auth", help="Verify GCP credentials and model access.")
def check_auth(
    config: str = typer.Option(DEFAULT_CONFIG, "--config", "-c", help="Path to agents YAML config"),
):
    async def _check():
        display = Display()
        console.print("[bold]Checking GCP credentials and model access…[/]\n")

        agents = _make_agents(config)
        for agent in agents:
            try:
                resp = await agent.respond("Say 'OK' in one word.", context="", round_num=0)
                if resp.text:
                    display.check_auth_ok(f"{agent.display_name} (Vertex AI)")
                else:
                    display.check_auth_fail(agent.display_name, "Empty response")
            except Exception as e:
                display.check_auth_fail(agent.display_name, str(e))

    asyncio.run(_check())


def main():
    """Entry point: if first arg looks like a question (not a subcommand), route to `ask`."""
    subcommands = {"ask", "check-auth", "benchmark"}
    if len(sys.argv) > 1 and sys.argv[1] not in subcommands and not sys.argv[1].startswith("-"):
        sys.argv.insert(1, "ask")
    app()
