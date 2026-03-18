from collections import Counter

from collabia.agents.base import AgentAnalysis


def compute_majority(analyses: list[AgentAnalysis]) -> tuple[str, Counter]:
    """Return (preferred_agent_id_with_most_votes, vote_counts)."""
    votes = Counter(a.preferred_agent_id for a in analyses)
    winner = votes.most_common(1)[0][0]
    return winner, votes


def is_majority(votes: Counter, total_agents: int) -> bool:
    """True if the leading candidate has strictly more than half of all agents' votes."""
    if not votes:
        return False
    leader_votes = votes.most_common(1)[0][1]
    return leader_votes > total_agents / 2


def find_worst(votes: Counter, active_agent_ids: list[str]) -> str:
    """Return the active agent_id with the fewest votes (least preferred)."""
    # Give zero votes to agents not mentioned in the tally
    scored = {agent_id: votes.get(agent_id, 0) for agent_id in active_agent_ids}
    return min(scored, key=lambda aid: scored[aid])
