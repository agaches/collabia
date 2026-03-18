import asyncio
import sys

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


@app.command(name="ask", help="Ask a question and run the consensus loop.")
def ask(
    question: str = typer.Argument(..., help="The question to ask"),
    rounds: int = typer.Option(settings.max_rounds, "--rounds", "-r", help="Max consensus rounds"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show full responses and analyses"),
    config: str = typer.Option(DEFAULT_CONFIG, "--config", "-c", help="Path to agents YAML config"),
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
            results.append((config_path, result.first_response, result.winner))

        display.show_benchmark(results)

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
