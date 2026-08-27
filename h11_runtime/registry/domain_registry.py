"""Domain Registry."""
from __future__ import annotations

from typing import Dict, List, Set


class DomainRegistry:
    """Taxonomy of the 30 H11I intelligence domains."""

    def __init__(self) -> None:
        self.domains: Dict[str, Set[str]] = {}

    def register_domain_agent(self, domain_code: str, agent_id: str) -> None:
        if domain_code not in self.domains:
            self.domains[domain_code] = set()
        self.domains[domain_code].add(agent_id)

    def list_domain_agents(self, domain_code: str) -> List[str]:
        return sorted(list(self.domains.get(domain_code, set())))
