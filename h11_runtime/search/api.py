"""Unified Large Search Engine (LSE v2.0) Service Facade.

Orchestrates:
- Query Decomposition & Domain Classification (QueryEngine)
- Federated Academic & Web Fan-out (ArXiv, PubMed, Wikipedia, Crossref, DuckDuckGo)
- Sharded Inverted Index with BM25F & Block-Max WAND
- ColBERT Token-Level Late Interaction (MaxSim Reranking)
- 64-bit SimHash Deduplication
- Neuro-Symbolic Knowledge Graph Entity Linking
- Cross-Document Evidence Synthesis & Verification Matrix
- Multi-tier Cache
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .cache import CacheConfig, SearchCache
from .dedup import SimHash, SimHashIndex, canonicalize_url
from .entity_linker import NeuroSymbolicEntityLinker
from .federation import FederatedResult, FederatedSearchEngine
from .indexer import InvertedIndex
from .knowledge_graph import Entity, KnowledgeGraph, Relation, Triple
from .late_interaction import LateInteractionEngine
from .pagerank import PageRankEngine, WebGraph
from .query_engine import QueryDecomposer, QueryPlan
from .ranker import HybridRanker, RankedResult
from .semantic_parser import SemanticDocument, SemanticParser
from .sharded_index import DocumentFields, ShardedIndex
from .synthesizer import EvidenceBriefing, EvidenceSynthesizer

logger = logging.getLogger(__name__)


@dataclass
class SearchConfig:
    index_dir: str = "./h11_search_index"
    crawl_config: Optional[Any] = None
    embedding_model: str = "all-MiniLM-L6-v2"
    cache_ttl: int = 3600
    enable_knowledge_graph: bool = True
    enable_web_search: bool = True
    enable_academic_federation: bool = True
    enable_late_interaction: bool = True
    max_results: int = 10


@dataclass
class SearchQuery:
    text: str
    domain_filter: Optional[str] = None
    freshness: str = "any"
    max_results: int = 10
    include_snippets: bool = True
    include_knowledge_graph: bool = True
    enable_synthesis: bool = True


@dataclass
class SearchResponse:
    query: str
    results: List[Dict[str, Any]]
    knowledge_triples: List[Any]
    query_plan: Optional[QueryPlan]
    evidence_briefing: Optional[EvidenceBriefing]
    total_results: int
    search_time_ms: float
    cached: bool
    domain_classified: List[str] = field(default_factory=list)


class SearchService:
    """Enterprise Large Search Engine (LSE v2.0) coordinator."""

    def __init__(self, config: Optional[SearchConfig] = None) -> None:
        self.config = config or SearchConfig()
        self.cache = SearchCache(CacheConfig(default_ttl_seconds=self.config.cache_ttl))
        self.query_decomposer = QueryDecomposer()
        self.semantic_parser = SemanticParser()
        self.sharded_index = ShardedIndex(num_shards=4)
        self.dedup_index = SimHashIndex(k=3)
        self.federation = FederatedSearchEngine(enable_academic=self.config.enable_academic_federation)
        self.late_interaction = LateInteractionEngine(embedding_dim=128)
        self.knowledge_graph = KnowledgeGraph()
        self.entity_linker = NeuroSymbolicEntityLinker(self.knowledge_graph)
        self.synthesizer = EvidenceSynthesizer()
        self.pagerank_engine = PageRankEngine()
        self.web_graph = WebGraph()

    async def search(self, query: SearchQuery) -> SearchResponse:
        """Executes full multi-stage LSE v2.0 search and reasoning pipeline."""
        start_time = time.time()

        # 1. Cache Check
        cache_key = self.cache._make_key(query.text, domain=query.domain_filter, max=query.max_results)
        cached_res = self.cache.get(cache_key)
        if cached_res:
            cached_res.cached = True
            return cached_res

        # 2. Query Decomposition & Classification
        query_plan = self.query_decomposer.decompose(query.text)
        domain = query.domain_filter or (query_plan.domains[0] if query_plan.domains else "D11_cs")

        # 3. Federated Knowledge Fan-Out (arXiv, PubMed, Wikipedia, Crossref, DuckDuckGo)
        federated_hits: List[FederatedResult] = []
        if self.config.enable_web_search or self.config.enable_academic_federation:
            federated_hits = await self.federation.federated_search(
                query=query.text,
                domain_hint=domain,
                max_results_per_source=max(2, query.max_results // 2),
            )

        # 4. Local Sharded Index Retrieval
        local_hits = self.sharded_index.search_bm25f(query.text, top_k=query.max_results)

        # 5. Merge, Deduplicate & Canonicalize
        candidate_docs: List[Dict[str, Any]] = []
        seen_urls = set()

        for fed in federated_hits:
            c_url = canonicalize_url(fed.url)
            if c_url not in seen_urls:
                seen_urls.add(c_url)
                candidate_docs.append(
                    {
                        "doc_id": fed.doi_or_id or c_url,
                        "title": fed.title,
                        "url": fed.url,
                        "snippet": fed.snippet,
                        "score": fed.score,
                        "source": fed.source_name,
                        "authors": fed.authors,
                        "publish_date": fed.publish_date,
                    }
                )

        for doc_id, score in local_hits:
            doc_fields = self.sharded_index.get_document(doc_id)
            if doc_fields:
                c_url = canonicalize_url(doc_fields.url)
                if c_url not in seen_urls:
                    seen_urls.add(c_url)
                    candidate_docs.append(
                        {
                            "doc_id": doc_id,
                            "title": doc_fields.title,
                            "url": doc_fields.url,
                            "snippet": (doc_fields.abstract or doc_fields.body)[:300],
                            "score": min(1.0, score / 10.0),
                            "source": "local_sharded_index",
                        }
                    )

        # 6. ColBERT Token-Level MaxSim Reranking
        if self.config.enable_late_interaction and candidate_docs:
            doc_tuples = [(d["doc_id"], d["title"] + " " + d["snippet"]) for d in candidate_docs]
            reranked = self.late_interaction.rank_documents(query.text, doc_tuples)
            reranked_dict = {r[0]: (r[1], r[2]) for r in reranked}

            for doc in candidate_docs:
                if doc["doc_id"] in reranked_dict:
                    maxsim_score, details = reranked_dict[doc["doc_id"]]
                    # Combine source trust with MaxSim neural alignment
                    doc["maxsim_score"] = round(maxsim_score, 4)
                    doc["score"] = round((doc["score"] * 0.4) + (maxsim_score * 0.6), 4)

            candidate_docs.sort(key=lambda x: x["score"], reverse=True)

        final_results = candidate_docs[: query.max_results]

        # 7. Knowledge Graph Entity Linking
        knowledge_triples: List[Any] = []
        if self.config.enable_knowledge_graph and final_results:
            combined_text = " ".join([d["title"] + ". " + d["snippet"] for d in final_results])
            mentions = self.entity_linker.link_mentions(combined_text)
            for m in mentions[:5]:
                if m.linked_entity_id:
                    triples = self.knowledge_graph.query(subject=m.surface_text)
                    knowledge_triples.extend(triples)

        # 8. Cross-Document Evidence Synthesis & Verification Matrix
        briefing: Optional[EvidenceBriefing] = None
        if query.enable_synthesis and final_results:
            briefing = self.synthesizer.synthesize(query=query.text, domain=domain, raw_documents=final_results)

        elapsed_ms = (time.time() - start_time) * 1000

        response = SearchResponse(
            query=query.text,
            results=final_results,
            knowledge_triples=knowledge_triples,
            query_plan=query_plan,
            evidence_briefing=briefing,
            total_results=len(final_results),
            search_time_ms=elapsed_ms,
            cached=False,
            domain_classified=query_plan.domains,
        )

        # Cache response
        self.cache.put(cache_key, response)
        return response

    async def index_document(self, url: str, title: str, text: str, metadata: Optional[Dict] = None) -> str:
        """Indexes document with semantic extraction, deduplication, and sharding."""
        c_url = canonicalize_url(url)
        # Check SimHash duplicate
        if self.dedup_index.is_duplicate(text):
            logger.info(f"Duplicate content detected for {url} - skipping index.")
            return "duplicate_skipped"

        # Semantic parsing
        sem_doc = self.semantic_parser.parse(text, url=c_url, title=title)

        # Build sharded document
        doc_id = hashlib.sha256(c_url.encode("utf-8")).hexdigest()[:16]
        sharded_doc = DocumentFields(
            doc_id=doc_id,
            url=c_url,
            title=title,
            headings=" ".join([h[1] for h in sem_doc.metadata.get("headings", [])]),
            abstract=text[:300],
            body=sem_doc.clean_text,
            metadata=metadata or {},
        )
        self.sharded_index.add_document(sharded_doc)
        self.dedup_index.add(doc_id, SimHash(text))

        # Add citations to KG
        for cit in sem_doc.citations:
            self.knowledge_graph.add_entity(
                Entity(id=f"CIT-{cit.identifier}", name=cit.identifier, entity_type=cit.citation_type, source_url=c_url)
            )

        return doc_id

    def get_stats(self) -> Dict[str, Any]:
        """Returns comprehensive telemetry across all LSE v2.0 engines."""
        return {
            "cache_stats": self.cache.stats,
            "sharded_index_docs": self.sharded_index.total_documents,
            "knowledge_graph": self.knowledge_graph.stats,
            "federated_connectors": [c.source_name for c in self.federation.connectors],
        }
