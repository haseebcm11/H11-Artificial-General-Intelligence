"""H11-LSE v2.0: Superintelligent Large Search Engine System.

Provides an enterprise-grade, distributed web intelligence and retrieval engine:
- Multi-Source Academic & Deep Web Federation (arXiv, PubMed, Wikipedia, Crossref, DuckDuckGo)
- Semantic Extraction for LaTeX Math, Tables, Code Snippets, DOIs/PMIDs, and Freshness
- 64-bit SimHash Hamming Distance & MinHash LSH Deduplication Filter
- Sharded Inverted Index with BM25F Field Weighting & Block-Max WAND Pruning
- Topic-Sensitive PageRank (D01-D30), Domain Authority & TrustRank Spam Suppression
- ColBERT Token-Level Late Interaction (MaxSim Reranking) & Cross-Encoder Verification
- Neuro-Symbolic Knowledge Graph Entity Linking & Multi-Hop Path Reasoning
- Multi-Document Evidence Synthesis & Claim Verification Matrix
"""
from __future__ import annotations

# ── Crawler & Parsers ───────────────────────────────────────────────────────
from .crawler import CrawlConfig, CrawlResult, RobotsChecker, URLFrontier, WebCrawler
from .parser import HTMLParser, ParsedDocument
from .semantic_parser import (
    AcademicCitation,
    CodeSnippet,
    MathEquation,
    SemanticDocument,
    SemanticParser,
    StructuredTable,
)

# ── Deduplication & LSH ────────────────────────────────────────────────────
from .dedup import MinHash, SimHash, SimHashIndex, canonicalize_url

# ── Sharded & BM25F Indexing ────────────────────────────────────────────────
from .indexer import DocumentEntry, IndexConfig, InvertedIndex, SearchHit
from .sharded_index import (
    DocumentFields,
    FieldWeights,
    Posting,
    PostingBlock,
    ShardedIndex,
    varbyte_decode,
    varbyte_encode,
)

# ── Embedder & Vector Store ─────────────────────────────────────────────────
from .embedder import EmbeddingConfig, EmbeddingResult, TextEmbedder
from .vector_store import SearchResult, VectorRecord, VectorStore, VectorStoreConfig

# ── PageRank & Authority Graph ──────────────────────────────────────────────
from .pagerank import (
    TOPIC_AUTHORITY_SEEDS,
    PageRankEngine,
    WebGraph,
    extract_domain,
)

# ── Late Interaction & Cross-Encoder ────────────────────────────────────────
from .late_interaction import (
    CrossEncoderVerifier,
    LateInteractionEngine,
    LateInteractionScore,
    TokenEmbeddingMatrix,
)

# ── Query Engine & Knowledge Graph ──────────────────────────────────────────
from .query_engine import QueryDecomposer, QueryPlan, QueryType, SubQuery
from .knowledge_graph import Entity, KnowledgeGraph, Relation, Triple
from .entity_linker import EntityMention, KnowledgePath, NeuroSymbolicEntityLinker

# ── Federation & Multi-Source Connectors ────────────────────────────────────
from .federation import (
    ArxivConnector,
    BaseConnector,
    CrossrefConnector,
    DuckDuckGoConnector,
    FederatedResult,
    FederatedSearchEngine,
    WikipediaConnector,
)

# ── Evidence Synthesis & Verification Matrix ────────────────────────────────
from .synthesizer import (
    EvidenceBriefing,
    EvidenceSynthesizer,
    SourceAssessment,
    SynthesizedClaim,
    VerificationStatus,
)

# ── Multi-Tier Cache & Service Facade ───────────────────────────────────────
from .cache import CacheConfig, SearchCache
from .api import SearchConfig, SearchQuery, SearchResponse, SearchService

# ── Multi-Hop Retrieval-Augmented Reasoning (RAR) ───────────────────────────
from .rar import (
    EvidenceGrounding,
    ReasoningContext,
    RetrievalAugmentedReasoner,
    RetrievedDocument,
)

__all__ = [
    # Crawler & Semantic Parsers
    "CrawlConfig", "CrawlResult", "RobotsChecker", "URLFrontier", "WebCrawler",
    "HTMLParser", "ParsedDocument", "SemanticParser", "SemanticDocument",
    "MathEquation", "StructuredTable", "CodeSnippet", "AcademicCitation",
    # Deduplication
    "SimHash", "SimHashIndex", "MinHash", "canonicalize_url",
    # Sharded Index & BM25F
    "IndexConfig", "InvertedIndex", "SearchHit", "DocumentEntry",
    "ShardedIndex", "DocumentFields", "FieldWeights", "Posting", "PostingBlock",
    "varbyte_encode", "varbyte_decode",
    # Embeddings & Vectors
    "EmbeddingConfig", "EmbeddingResult", "TextEmbedder",
    "VectorStore", "VectorStoreConfig", "VectorRecord", "SearchResult",
    # PageRank & Authority
    "PageRankEngine", "WebGraph", "TOPIC_AUTHORITY_SEEDS", "extract_domain",
    # Late Interaction
    "LateInteractionEngine", "LateInteractionScore", "TokenEmbeddingMatrix", "CrossEncoderVerifier",
    # Query Engine & KG
    "QueryDecomposer", "QueryPlan", "QueryType", "SubQuery",
    "Entity", "KnowledgeGraph", "Relation", "Triple",
    "NeuroSymbolicEntityLinker", "EntityMention", "KnowledgePath",
    # Federation
    "FederatedSearchEngine", "FederatedResult", "BaseConnector",
    "ArxivConnector", "WikipediaConnector", "CrossrefConnector", "DuckDuckGoConnector",
    # Synthesis & Matrix
    "EvidenceSynthesizer", "EvidenceBriefing", "SynthesizedClaim", "SourceAssessment", "VerificationStatus",
    # Cache & API
    "CacheConfig", "SearchCache",
    "SearchConfig", "SearchQuery", "SearchResponse", "SearchService",
    # RAR
    "EvidenceGrounding", "ReasoningContext", "RetrievalAugmentedReasoner", "RetrievedDocument",
]
