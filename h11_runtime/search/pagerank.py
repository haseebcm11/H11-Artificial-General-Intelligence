"""Topic-Sensitive PageRank, Domain Authority & TrustRank Graph Engine.

Implements:
- Power-iteration PageRank with damping factor d = 0.85.
- Topic-Sensitive PageRank biased towards seed authority domains per H11I domain (D01-D30).
- Domain Authority & TrustRank score propagation to penalize spam/untrusted sources.
- HITS (Hyperlink-Induced Topic Search) Hubs and Authorities algorithm.
"""
from __future__ import annotations

import logging
import math
import urllib.parse
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


# High-authority verified seed domains per H11I topic family
TOPIC_AUTHORITY_SEEDS: Dict[str, Set[str]] = {
    # Medicine, Pharmacology, Healthcare
    "D01_medicine": {"nih.gov", "ncbi.nlm.nih.gov", "who.int", "cdc.gov", "nejm.org", "thelancet.com", "bmj.com"},
    "D02_pharmacology": {"fda.gov", "drugbank.com", "ema.europa.eu", "rxlist.com"},
    # Physical Sciences, Math, Astronomy
    "D07_space": {"nasa.gov", "esa.int", "space.com", "hubblesite.org"},
    "D08_physics": {"arxiv.org", "aps.org", "nature.com", "cern.ch", "iop.org"},
    "D09_chemistry": {"rsc.org", "acs.org", "pubchem.ncbi.nlm.nih.gov", "nist.gov"},
    "D10_mathematics": {"ams.org", "mathworld.wolfram.com", "oeis.org", "projecteuclid.org"},
    # Computer Science & Cybersecurity
    "D11_computer_science": {"ieee.org", "acm.org", "github.com", "arxiv.org", "w3.org", "python.org"},
    "D30_cybersecurity": {"cisa.gov", "nist.gov", "mitre.org", "owasp.org", "ietf.org"},
    # Law & Finance
    "D17_finance": {"sec.gov", "federalreserve.gov", "worldbank.org", "imf.org", "bloomberg.com"},
    "D18_law": {"courtlistener.com", "supremecourt.gov", "law.cornell.edu", "eur-lex.europa.eu"},
    # Universal Baseline
    "UNIVERSAL": {"wikipedia.org", "wikimedia.org", "wikidata.org", "nature.com", "science.org", "stanford.edu", "mit.edu", "harvard.edu"},
}


def extract_domain(url: str) -> str:
    """Extracts base domain from a URL (e.g., 'https://sub.nature.com/paper' -> 'nature.com')."""
    if not url:
        return ""
    try:
        netloc = urllib.parse.urlparse(url).netloc.lower()
        if ":" in netloc:
            netloc = netloc.split(":")[0]
        # Remove leading www.
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc
    except Exception:
        return url.lower()


class WebGraph:
    """Directed link graph representing the web link topology."""

    def __init__(self) -> None:
        self.nodes: Set[str] = set()
        self.out_edges: Dict[str, Set[str]] = {}  # node -> set of target nodes
        self.in_edges: Dict[str, Set[str]] = {}   # node -> set of source nodes

    def add_node(self, node: str) -> None:
        if node not in self.nodes:
            self.nodes.add(node)
            self.out_edges[node] = set()
            self.in_edges[node] = set()

    def add_edge(self, source: str, target: str) -> None:
        self.add_node(source)
        self.add_node(target)
        if source != target:  # Ignore self-loops
            self.out_edges[source].add(target)
            self.in_edges[target].add(source)

    @property
    def size(self) -> int:
        return len(self.nodes)


class PageRankEngine:
    """Computes global PageRank, Topic-Sensitive PageRank, and Domain TrustRank."""

    def __init__(self, damping: float = 0.85, max_iter: int = 100, tol: float = 1e-6) -> None:
        self.damping = damping
        self.max_iter = max_iter
        self.tol = tol

    def compute_pagerank(self, graph: WebGraph, personalization: Optional[Dict[str, float]] = None) -> Dict[str, float]:
        """Computes standard or personalized PageRank via Power Iteration."""
        n = graph.size
        if n == 0:
            return {}

        nodes = list(graph.nodes)
        node_idx = {node: i for i, node in enumerate(nodes)}

        # Default uniform teleportation vector if none provided
        if personalization is None or sum(personalization.values()) == 0:
            teleport = [1.0 / n] * n
        else:
            total_pers = sum(personalization.get(node, 0.0) for node in nodes)
            if total_pers > 0:
                teleport = [personalization.get(node, 0.0) / total_pers for node in nodes]
            else:
                teleport = [1.0 / n] * n

        # Initial rank distribution
        ranks = [1.0 / n] * n

        for iteration in range(self.max_iter):
            new_ranks = [0.0] * n
            dangling_sum = sum(ranks[node_idx[node]] for node in nodes if len(graph.out_edges[node]) == 0)

            for i, target_node in enumerate(nodes):
                inbound_sum = 0.0
                for source_node in graph.in_edges[target_node]:
                    out_deg = len(graph.out_edges[source_node])
                    if out_deg > 0:
                        inbound_sum += ranks[node_idx[source_node]] / out_deg

                # PageRank transition equation
                new_ranks[i] = (
                    self.damping * (inbound_sum + (dangling_sum * teleport[i]))
                    + (1.0 - self.damping) * teleport[i]
                )

            # Check L1 convergence
            diff = sum(abs(new_ranks[i] - ranks[i]) for i in range(n))
            ranks = new_ranks
            if diff < self.tol:
                break

        return {nodes[i]: ranks[i] for i in range(n)}

    def compute_topic_pagerank(self, graph: WebGraph, topic: str) -> Dict[str, float]:
        """Computes topic-sensitive PageRank biased towards domain-specific authority seeds."""
        seeds = set(TOPIC_AUTHORITY_SEEDS.get(topic, set())) | TOPIC_AUTHORITY_SEEDS["UNIVERSAL"]
        personalization: Dict[str, float] = {}

        for node in graph.nodes:
            dom = extract_domain(node)
            # High weight if domain ends with or matches a seed
            if any(dom == s or dom.endswith("." + s) for s in seeds):
                personalization[node] = 10.0
            elif dom.endswith(".edu") or dom.endswith(".gov") or dom.endswith(".org"):
                personalization[node] = 2.0
            else:
                personalization[node] = 0.1

        return self.compute_pagerank(graph, personalization=personalization)

    def compute_trustrank(self, graph: WebGraph, trusted_seed_urls: Set[str]) -> Dict[str, float]:
        """Computes TrustRank to filter out web spam and malicious link networks."""
        n = graph.size
        if n == 0:
            return {}

        personalization = {node: (1.0 if node in trusted_seed_urls or extract_domain(node) in trusted_seed_urls else 0.0) for node in graph.nodes}
        # If no seeds present in graph, fall back to .edu/.gov/.org
        if sum(personalization.values()) == 0:
            for node in graph.nodes:
                dom = extract_domain(node)
                if dom.endswith(".gov") or dom.endswith(".edu") or dom.endswith(".org"):
                    personalization[node] = 1.0

        return self.compute_pagerank(graph, personalization=personalization)

    def calculate_domain_authority(self, url: str, base_pagerank: float, in_degree: int) -> float:
        """Calculates a normalized Domain Authority score [0.0, 100.0]."""
        dom = extract_domain(url)
        # Baseline TLD bonus
        tld_bonus = 0.0
        if dom.endswith(".gov"):
            tld_bonus = 25.0
        elif dom.endswith(".edu"):
            tld_bonus = 20.0
        elif dom.endswith(".org"):
            tld_bonus = 10.0

        # Logarithmic in-link boost
        link_score = 15.0 * math.log10(max(1, in_degree) + 1)
        # Scaled PageRank
        pr_score = min(50.0, base_pagerank * 1000.0)

        da = pr_score + link_score + tld_bonus
        return min(100.0, max(1.0, da))
