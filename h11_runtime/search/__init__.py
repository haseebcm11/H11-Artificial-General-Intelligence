"""H11-SEARCH: Sovereign Internet Knowledge Acquisition Engine.

Provides live internet crawling, indexing, semantic search, hybrid ranking,
knowledge graph construction, and retrieval-augmented reasoning for the
H11-AGI 1,000-agent cognitive architecture.

Subsystems
----------
- **Crawler**        : Async web spider with robots.txt compliance
- **Parser**         : HTML → clean text extraction
- **Indexer**        : BM25 inverted index engine
- **Embedder**       : Dense vector embedding pipeline
- **VectorStore**    : HNSW approximate nearest-neighbour search
- **Ranker**         : Hybrid BM25 + semantic reranking
- **QueryEngine**    : Natural-language query decomposition
- **KnowledgeGraph** : Entity / relation triple store
- **Cache**          : Result caching & freshness management
- **SearchService**  : Unified API surface for all agents
- **RAR**            : Retrieval-Augmented Reasoning connector
"""
from __future__ import annotations

# ── Crawler ─────────────────────────────────────────────────────────────────
from .crawler import CrawlConfig, CrawlResult, RobotsChecker, URLFrontier, WebCrawler

# ── Parser ──────────────────────────────────────────────────────────────────
from .parser import HTMLParser, ParsedDocument

# ── Indexer ─────────────────────────────────────────────────────────────────
from .indexer import IndexConfig, InvertedIndex, SearchHit, DocumentEntry

# ── Embedder ────────────────────────────────────────────────────────────────
from .embedder import EmbeddingConfig, EmbeddingResult, TextEmbedder

# ── Vector Store ────────────────────────────────────────────────────────────
from .vector_store import VectorStore, VectorStoreConfig, VectorRecord, SearchResult

# ── Ranker ──────────────────────────────────────────────────────────────────
from .ranker import HybridRanker, RankConfig, RankedResult

# ── Query Engine ────────────────────────────────────────────────────────────
from .query_engine import QueryDecomposer, QueryPlan, QueryType, SubQuery

# ── Knowledge Graph ─────────────────────────────────────────────────────────
from .knowledge_graph import Entity, KnowledgeGraph, Relation, Triple

# ── Cache ───────────────────────────────────────────────────────────────────
from .cache import CacheConfig, SearchCache

# ── Unified API ─────────────────────────────────────────────────────────────
from .api import SearchConfig, SearchQuery, SearchResponse, SearchService

# ── Retrieval-Augmented Reasoning ───────────────────────────────────────────
from .rar import (
    EvidenceGrounding,
    ReasoningContext,
    RetrievalAugmentedReasoner,
    RetrievedDocument,
)

__all__ = [
    # Crawler
    "CrawlConfig", "CrawlResult", "RobotsChecker", "URLFrontier", "WebCrawler",
    # Parser
    "HTMLParser", "ParsedDocument",
    # Indexer
    "IndexConfig", "InvertedIndex", "SearchHit", "DocumentEntry",
    # Embedder
    "EmbeddingConfig", "EmbeddingResult", "TextEmbedder",
    # Vector Store
    "VectorStore", "VectorStoreConfig", "VectorRecord", "SearchResult",
    # Ranker
    "HybridRanker", "RankConfig", "RankedResult",
    # Query Engine
    "QueryDecomposer", "QueryPlan", "QueryType", "SubQuery",
    # Knowledge Graph
    "Entity", "KnowledgeGraph", "Relation", "Triple",
    # Cache
    "CacheConfig", "SearchCache",
    # API
    "SearchConfig", "SearchQuery", "SearchResponse", "SearchService",
    # RAR
    "EvidenceGrounding", "ReasoningContext", "RetrievalAugmentedReasoner",
    "RetrievedDocument",
]
