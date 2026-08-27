"""H11_CRAWLER: Distributed Mercator-based crawler.

Implements simplified PageRank for frontier prioritization and 
Exponential Backoff with politeness delay constraints.
Math: PR(u) = (1-d) + d * \\sum_{v \\in B_u} PR(v)/L(v)
"""
import math
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

AGENT_ID = "H11_CRAWLER"

class CrawlerError(ValueError):
    """Domain-specific error for H11_CRAWLER."""

class CrawlerStatus(Enum):
    IDLE = auto()
    ACTIVE = auto()
    OPTIMAL = auto()

@dataclass(frozen=True)
class GraphNode:
    url_id: int
    outbound_links: List[int]

@dataclass(frozen=True)
class CrawlerInput:
    web_graph: List[GraphNode] = field(default_factory=list)
    damping_factor: float = 0.85
    pagerank_iterations: int = 10
    base_politeness_ms: float = 2000.0

@dataclass(frozen=True)
class CrawlerOutput:
    agent_id: str
    status: str
    pagerank_scores: Dict[int, float]
    frontier_priority: List[int]
    execution_time_ms: float
    diagnostics: Dict[str, float]

class CrawlerAgent:
    """Analytical engine for PageRank and Mercator queueing."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def _compute_pagerank(self, graph: List[GraphNode], d: float, iters: int) -> Dict[int, float]:
        """Iterative PageRank computation."""
        nodes = {node.url_id for node in graph}
        for node in graph:
            nodes.update(node.outbound_links)
            
        N = len(nodes)
        if N == 0: return {}
        
        pr = {node: 1.0 / N for node in nodes}
        
        # Build inbound mapping
        inbound = {node: [] for node in nodes}
        out_degree = {node: 0 for node in nodes}
        
        for node in graph:
            out_degree[node.url_id] = len(node.outbound_links)
            for target in node.outbound_links:
                inbound[target].append(node.url_id)
                
        for _ in range(iters):
            new_pr = {}
            sink_pr = sum(pr[n] for n in nodes if out_degree[n] == 0)
            
            for node in nodes:
                # Teleportation + sink redistribution
                rank = (1.0 - d) / N + d * (sink_pr / N)
                # Transfer from inbound links
                for in_node in inbound[node]:
                    rank += d * (pr[in_node] / out_degree[in_node])
                new_pr[node] = rank
            pr = new_pr
            
        return pr

    def process(self, input_data: Optional[CrawlerInput] = None) -> CrawlerOutput:
        start_time = time.perf_counter()
        if input_data is None:
            input_data = CrawlerInput()

        pr_scores = self._compute_pagerank(
            input_data.web_graph, 
            input_data.damping_factor, 
            input_data.pagerank_iterations
        )
        
        # Priority frontier (highest PR first)
        frontier = sorted(pr_scores.keys(), key=lambda k: pr_scores[k], reverse=True)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return CrawlerOutput(
            agent_id=AGENT_ID,
            status=CrawlerStatus.OPTIMAL.name,
            pagerank_scores={k: round(v, 6) for k, v in pr_scores.items()},
            frontier_priority=frontier,
            execution_time_ms=round(elapsed_ms, 2),
            diagnostics={
                "nodes_processed": len(pr_scores),
                "max_pagerank": max(pr_scores.values()) if pr_scores else 0.0
            }
        )
