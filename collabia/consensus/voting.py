from collections import Counter

from collabia.agents.base import AgentAnalysis


def compute_elimination_votes(analyses: list[AgentAnalysis]) -> tuple[str, Counter]:
    """Return (agent_id_to_eliminate, vote_counts) based on majority vote."""
    votes = Counter(a.eliminate_agent_id for a in analyses)
    worst = votes.most_common(1)[0][0]
    return worst, votes


def find_best(votes: Counter, active_agent_ids: list[str]) -> str:
    """Return the active agent_id with the fewest elimination votes (least targeted)."""
    scored = {agent_id: votes.get(agent_id, 0) for agent_id in active_agent_ids}
    return min(scored, key=lambda aid: scored[aid])
