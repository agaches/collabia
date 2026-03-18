import asyncio

from collabia.agents.base import AgentAnalysis, AgentCritique, AgentResponse, BaseAgent
from collabia.consensus.voting import compute_majority, find_worst, is_majority
from collabia.display.terminal import Display


async def run_consensus(
    question: str,
    agents: list[BaseAgent],
    max_rounds: int,
    display: Display,
    verbose: bool = False,
) -> AgentResponse:
    context = ""
    last_responses: dict[str, AgentResponse] = {}

    for round_num in range(1, max_rounds + 1):
        active_agents = [a for a in agents if not a.is_eliminated]

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

        last_responses = responses
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

        # --- Phase 3: parallel votes from ALL agents (informed by critiques) ---
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

        preferred_id, votes = compute_majority(analyses)
        display.show_votes(votes, analyses, verbose)

        # --- Consensus check ---
        if is_majority(votes, len(agents)):
            display.consensus_reached(round_num, preferred_id, agents)
            return responses[preferred_id]

        # --- Eliminate worst agent (only if more than 1 active) ---
        if len(active_agents) > 1:
            active_ids = [a.agent_id for a in active_agents]
            worst_id = find_worst(votes, active_ids)
            for agent in agents:
                if agent.agent_id == worst_id:
                    agent.is_eliminated = True
                    display.agent_eliminated(agent.display_name)
                    break

        # Update context with preferred response
        if preferred_id in responses:
            context = responses[preferred_id].text

    # No consensus reached — return the last preferred response
    display.no_consensus(max_rounds)
    if last_responses:
        preferred_id = next(iter(last_responses))
        return last_responses[preferred_id]

    raise RuntimeError("No responses were generated.")
