"""H11-LSE v3.0: Ultra-Omniscient Web Superintelligence & Graph-RAG System.

Unifies 16 advanced search and cognitive retrieval engines:
- Autonomous Multi-Agent Swarm Crawler (UCB1 Frontier)
- Product Quantization (IVF-PQ) & HNSW Multi-Layer Vector Engine
- Hierarchical Community Graph-RAG & TransE Link Prediction
- Judea Pearl Causal Do-Calculus Path Inference
- 12-Language Cross-Lingual Knowledge Harmonization
- Reflexion Search Loop & Tree-of-Thought Query Planning
- Real-Time Stream Ingestion & Kleinberg Burst Velocity Anomaly Detection
- Merkle Tree Cryptographic Provenance Ledger
- Multi-Source Academic Federation (arXiv, PubMed, Wikipedia, Crossref, DuckDuckGo)
- Semantic Extraction (LaTeX math, Markdown tables, code snippets, DOIs)
- 64-bit SimHash & MinHash LSH Deduplication
- Sharded Inverted Index with BM25F & Block-Max WAND
- Topic-Sensitive PageRank (D01-D30), Domain Authority & TrustRank
- ColBERT Token-Level Late Interaction (MaxSim Reranker)
- Cross-Document Evidence Synthesis & Claim Verification Matrix
- Multi-Hop Retrieval-Augmented Reasoning (RAR)
"""
from __future__ import annotations

# ── Crawler & Swarm Drones ──────────────────────────────────────────────────
from .crawler import CrawlConfig, CrawlResult, RobotsChecker, URLFrontier, WebCrawler
from .swarm_crawler import (
    AutonomousSwarmCrawler,
    DroneRole,
    SwarmCrawlResult,
    SwarmCrawlTask,
    UCB1DomainFrontier,
)

# ── Semantic Parsers ────────────────────────────────────────────────────────
from .parser import HTMLParser, ParsedDocument
from .semantic_parser import (
    AcademicCitation,
    CodeSnippet,
    MathEquation,
    SemanticDocument,
    SemanticParser,
    StructuredTable,
)

# ── Deduplication & LSH ─────────────────────────────────────────────────────
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

# ── Vector Engines & Quantization ───────────────────────────────────────────
from .embedder import EmbeddingConfig, EmbeddingResult, TextEmbedder
from .vector_store import SearchResult, VectorRecord, VectorStore, VectorStoreConfig
from .quantized_vector_engine import (
    HNSWNode,
    PQCodebook,
    ProductQuantizer,
    QuantizedHNSWEngine,
    QuantizedRecord,
)

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

# ── Knowledge Graph, Entity Linker & Graph-RAG ──────────────────────────────
from .knowledge_graph import Entity, KnowledgeGraph, Relation, Triple
from .entity_linker import EntityMention, KnowledgePath, NeuroSymbolicEntityLinker
from .graph_rag import (
    CausalInterventionResult,
    CommunityCluster,
    HierarchicalGraphRAG,
    PredictedRelation,
)

# ── Cross-Lingual Harmonization ─────────────────────────────────────────────
from .cross_lingual import (
    UNIVERSAL_CONCEPT_LEXICON,
    CrossLingualHarmonizer,
    UniversalConcept,
)

# ── Reflexion Search & Tree-of-Thought ──────────────────────────────────────
from .reflexion_search import (
    ReflexionCycleResult,
    ReflexionSearchLoop,
    SearchThoughtNode,
    UncertaintyEstimate,
)

# ── Real-Time Streaming & Burst Detection ───────────────────────────────────
from .stream_ingest import (
    BurstAnomaly,
    BurstVelocityDetector,
    RingBufferStream,
    StreamEvent,
)

# ── Merkle Cryptographic Provenance ─────────────────────────────────────────
from .provenance_ledger import (
    EvidenceLeaf,
    MerkleInclusionProof,
    MerkleProvenanceTree,
    sha256_hash,
)

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

# ── Master Ultra-Omniscient Search Engine ───────────────────────────────────
from .omni_engine import OmniSearchEngine, OmniSearchResponse

# ── Multi-Hop Retrieval-Augmented Reasoning (RAR) ───────────────────────────
from .rar import (
    EvidenceGrounding,
    ReasoningContext,
    RetrievalAugmentedReasoner,
    RetrievedDocument,
)

__all__ = [
    # Crawler & Swarm
    "CrawlConfig", "CrawlResult", "RobotsChecker", "URLFrontier", "WebCrawler",
    "AutonomousSwarmCrawler", "SwarmCrawlResult", "SwarmCrawlTask", "DroneRole", "UCB1DomainFrontier",
    # Semantic Parsers
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
    "ProductQuantizer", "QuantizedHNSWEngine", "PQCodebook", "QuantizedRecord", "HNSWNode",
    # PageRank & Authority
    "PageRankEngine", "WebGraph", "TOPIC_AUTHORITY_SEEDS", "extract_domain",
    # Late Interaction
    "LateInteractionEngine", "LateInteractionScore", "TokenEmbeddingMatrix", "CrossEncoderVerifier",
    # Knowledge Graph, Linker & Graph-RAG
    "QueryDecomposer", "QueryPlan", "QueryType", "SubQuery",
    "Entity", "KnowledgeGraph", "Relation", "Triple",
    "NeuroSymbolicEntityLinker", "EntityMention", "KnowledgePath",
    "HierarchicalGraphRAG", "CommunityCluster", "PredictedRelation", "CausalInterventionResult",
    # Cross-Lingual
    "CrossLingualHarmonizer", "UniversalConcept", "UNIVERSAL_CONCEPT_LEXICON",
    # Reflexion
    "ReflexionSearchLoop", "SearchThoughtNode", "UncertaintyEstimate", "ReflexionCycleResult",
    # Stream Ingestion
    "RingBufferStream", "BurstVelocityDetector", "StreamEvent", "BurstAnomaly",
    # Cryptographic Provenance
    "MerkleProvenanceTree", "MerkleInclusionProof", "EvidenceLeaf", "sha256_hash",
    # Federation
    "FederatedSearchEngine", "FederatedResult", "BaseConnector",
    "ArxivConnector", "WikipediaConnector", "CrossrefConnector", "DuckDuckGoConnector",
    # Synthesis & Matrix
    "EvidenceSynthesizer", "EvidenceBriefing", "SynthesizedClaim", "SourceAssessment", "VerificationStatus",
    # Cache & API
    "CacheConfig", "SearchCache",
    "SearchConfig", "SearchQuery", "SearchResponse", "SearchService",
    # Omni Engine
    "OmniSearchEngine", "OmniSearchResponse",
    # RAR
    "EvidenceGrounding", "ReasoningContext", "RetrievalAugmentedReasoner", "RetrievedDocument",
]
