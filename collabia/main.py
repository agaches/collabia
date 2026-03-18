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


def _make_agents():
    from collabia.agents.gemini import GeminiAgent
    from collabia.agents.gemini_flash import GeminiFlashAgent
    from collabia.agents.gemini_lite import GeminiLiteAgent

    return [GeminiAgent(), GeminiFlashAgent(), GeminiLiteAgent()]


@app.command(name="ask", help="Ask a question and run the consensus loop.")
def ask(
    question: str = typer.Argument(..., help="The question to ask"),
    rounds: int = typer.Option(settings.max_rounds, "--rounds", "-r", help="Max consensus rounds"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show full responses and analyses"),
):
    async def _run():
        agents = _make_agents()
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


@app.command(name="check-auth", help="Verify GCP credentials and model access.")
def check_auth():
    async def _check():
        display = Display()
        console.print("[bold]Checking GCP credentials and model access…[/]\n")

        # Check Gemini 2.5 Pro
        try:
            from collabia.agents.gemini import GeminiAgent

            agent = GeminiAgent()
            resp = await agent.respond("Say 'OK' in one word.", context="", round_num=0)
            if resp.text:
                display.check_auth_ok("Gemini 2.5 Pro (Vertex AI)")
            else:
                display.check_auth_fail("Gemini 2.5 Pro", "Empty response")
        except Exception as e:
            display.check_auth_fail("Gemini 2.5 Pro", str(e))

        # Check Gemini 2.5 Flash
        try:
            from collabia.agents.gemini_flash import GeminiFlashAgent

            agent = GeminiFlashAgent()
            resp = await agent.respond("Say 'OK' in one word.", context="", round_num=0)
            if resp.text:
                display.check_auth_ok("Gemini 2.5 Flash (Vertex AI)")
            else:
                display.check_auth_fail("Gemini 2.5 Flash", "Empty response")
        except Exception as e:
            display.check_auth_fail("Gemini 2.5 Flash", str(e))

        # Check Gemini 3.1 Flash Lite
        try:
            from collabia.agents.gemini_lite import GeminiLiteAgent

            agent = GeminiLiteAgent()
            resp = await agent.respond("Say 'OK' in one word.", context="", round_num=0)
            if resp.text:
                display.check_auth_ok("Gemini 3.1 Flash Lite (Vertex AI)")
            else:
                display.check_auth_fail("Gemini 3.1 Flash Lite", "Empty response")
        except Exception as e:
            display.check_auth_fail("Gemini 3.1 Flash Lite", str(e))

    asyncio.run(_check())


def main():
    """Entry point: if first arg looks like a question (not a subcommand), route to `ask`."""
    subcommands = {"ask", "check-auth"}
    if len(sys.argv) > 1 and sys.argv[1] not in subcommands and not sys.argv[1].startswith("-"):
        sys.argv.insert(1, "ask")
    app()
