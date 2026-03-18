import asyncio
from dataclasses import dataclass

from collabia.agents.base import AgentAnalysis, AgentCritique, AgentResponse, BaseAgent
from collabia.consensus.voting import compute_elimination_votes, find_best
from collabia.display.terminal import Display


@dataclass
class ConsensusResult:
    winner: AgentResponse
    first_response: AgentResponse | None  # winner's round 1 response, None if only 1 round


async def run_consensus(
    question: str,
    agents: list[BaseAgent],
    max_rounds: int,
    display: Display,
    verbose: bool = False,
) -> ConsensusResult:
    context = ""
    last_responses: dict[str, AgentResponse] = {}
    first_responses: dict[str, AgentResponse] = {}  # round 1 responses

    for round_num in range(1, max_rounds + 1):
        active_agents = [a for a in agents if not a.is_eliminated]

        # Only 1 active agent left — they win
        if len(active_agents) == 1:
            winner = active_agents[0]
            display.winner(winner.display_name, round_num - 1)
            final = last_responses[winner.agent_id]
            first = first_responses.get(winner.agent_id)
            return ConsensusResult(winner=final, first_response=first if first != final else None)

        display.start_round(round_num, max_rounds, [a.display_name for a in active_agents])

        # --- Phase 1: parallel responses from active agents ---
        response_tasks = [
            agent.respond(question, context, round_num) for agent in active_agents
        ]
        raw_responses = await asyncio.gather(*response_tasks, return_exceptions=True)

        responses: dict[str, AgentResponse] = {}
        for agent, result in zip(active_agents, raw_responses):
            if isinstance(result, Exception):
                display.agent_error(agent.display_name, str(result))
            else:
                responses[agent.agent_id] = result

        if not responses:
            display.error("All agents failed this round.")
            break

        last_responses.update(responses)
        if round_num == 1:
            first_responses = dict(responses)
        display.show_responses(responses, verbose)

        # --- Phase 2: parallel critiques from ALL agents ---
        critique_tasks = [
            agent.critique(question, responses, round_num) for agent in agents
        ]
        raw_critiques = await asyncio.gather(*critique_tasks, return_exceptions=True)

        critiques: list[AgentCritique] = []
        for agent, result in zip(agents, raw_critiques):
            if isinstance(result, Exception):
                display.agent_error(agent.display_name, f"critique error: {result}")
            else:
                critiques.append(result)

        display.show_critiques(critiques, verbose)

        # --- Phase 3: parallel elimination votes from ALL agents ---
        analysis_tasks = [
            agent.analyze(question, responses, critiques, round_num) for agent in agents
        ]
        raw_analyses = await asyncio.gather(*analysis_tasks, return_exceptions=True)

        analyses: list[AgentAnalysis] = []
        for agent, result in zip(agents, raw_analyses):
            if isinstance(result, Exception):
                display.agent_error(agent.display_name, f"vote error: {result}")
            else:
                analyses.append(result)

        if not analyses:
            display.error("All votes failed.")
            break

        worst_id, votes = compute_elimination_votes(analyses)
        display.show_elimination_votes(votes, analyses, verbose)

        # Eliminate the agent with the most votes against them
        for agent in agents:
            if agent.agent_id == worst_id:
                agent.is_eliminated = True
                display.agent_eliminated(agent.display_name)
                break

        # Update context with the best remaining response
        active_ids = [a.agent_id for a in agents if not a.is_eliminated]
        if active_ids:
            best_id = find_best(votes, active_ids)
            if best_id in responses:
                context = responses[best_id].text

    # Max rounds reached — return the last best response among active agents
    display.no_consensus(max_rounds)
    active_agents = [a for a in agents if not a.is_eliminated]
    if active_agents and last_responses:
        for aid in [a.agent_id for a in active_agents]:
            if aid in last_responses:
                final = last_responses[aid]
                first = first_responses.get(aid)
                return ConsensusResult(winner=final, first_response=first if first != final else None)

    raise RuntimeError("No responses were generated.")
