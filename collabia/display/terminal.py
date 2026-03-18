from collections import Counter

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from collabia.agents.base import AgentAnalysis, AgentCritique, AgentResponse, BaseAgent

console = Console()


class Display:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def start_round(self, round_num: int, max_rounds: int, agent_names: list[str]) -> None:
        agents_str = ", ".join(agent_names)
        console.rule(f"[bold cyan]Round {round_num}/{max_rounds}[/] — Active: {agents_str}")

    def show_responses(self, responses: dict[str, AgentResponse], verbose: bool) -> None:
        for agent_id, resp in responses.items():
            if verbose:
                console.print(
                    Panel(
                        resp.text,
                        title=f"[bold green]{agent_id}[/] response",
                        border_style="green",
                    )
                )
            else:
                preview = resp.text[:200].replace("\n", " ")
                if len(resp.text) > 200:
                    preview += "…"
                console.print(f"  [green]{agent_id}[/]: {preview}")

    def show_critiques(self, critiques: list[AgentCritique], verbose: bool) -> None:
        if not verbose:
            console.print(f"  [yellow]✎ {len(critiques)} critique(s) collected[/]")
            return
        for critique in critiques:
            lines = "\n".join(
                f"[bold]{agent_id}:[/] {text}"
                for agent_id, text in critique.critiques.items()
            )
            console.print(
                Panel(
                    lines,
                    title=f"[yellow]{critique.agent_id}[/] critiques",
                    border_style="yellow",
                )
            )

    def show_elimination_votes(
        self, votes: Counter, analyses: list[AgentAnalysis], verbose: bool
    ) -> None:
        table = Table(title="Elimination votes", show_header=True, header_style="bold red")
        table.add_column("Agent", style="cyan")
        table.add_column("Votes to eliminate", justify="right")
        for agent_id, count in votes.most_common():
            table.add_row(agent_id, str(count))
        console.print(table)

        if verbose:
            for analysis in analyses:
                console.print(
                    Panel(
                        f"[bold]Eliminate:[/] {analysis.eliminate_agent_id}\n"
                        f"[bold]Reasoning:[/] {analysis.reasoning}",
                        title=f"[magenta]{analysis.agent_id}[/] vote",
                        border_style="magenta",
                    )
                )

    def winner(self, display_name: str, rounds: int) -> None:
        console.print(
            f"\n[bold green]✓ Winner after {rounds} round(s): [bold]{display_name}[/][/]\n"
        )

    def agent_eliminated(self, display_name: str) -> None:
        console.print(f"  [yellow]⚠ {display_name} eliminated (fewest votes)[/]")

    def agent_error(self, display_name: str, message: str) -> None:
        console.print(f"  [red]✗ {display_name} error: {message}[/]")

    def error(self, message: str) -> None:
        console.print(f"[bold red]Error: {message}[/]")

    def no_consensus(self, max_rounds: int) -> None:
        console.print(
            f"\n[yellow]No consensus reached after {max_rounds} rounds.[/] "
            "Returning last preferred response.\n"
        )

    def show_final_answer(self, response: AgentResponse, agents: list[BaseAgent]) -> None:
        agent = next((a for a in agents if a.agent_id == response.agent_id), None)
        name = agent.display_name if agent else response.agent_id
        console.print(
            Panel(
                response.text,
                title=f"[bold blue]Final Answer[/] — {name}",
                border_style="blue",
            )
        )

    def check_auth_ok(self, name: str) -> None:
        console.print(f"  [green]✓[/] {name} OK")

    def check_auth_fail(self, name: str, error: str) -> None:
        console.print(f"  [red]✗[/] {name} FAILED: {error}")
