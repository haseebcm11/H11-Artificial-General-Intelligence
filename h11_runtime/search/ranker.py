from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

@dataclass
class RankConfig:
    """Configuration for the hybrid ranker."""
    bm25_weight: float = 0.4
    semantic_weight: float = 0.6
    rerank_top_k: int = 50
    final_top_k: int = 10
    min_score_threshold: float = 0.01

@dataclass
class RankedResult:
    """A combined search result from multiple systems."""
    doc_id: str
    url: str
    title: str
    snippet: str
    bm25_score: float
    semantic_score: float
    combined_score: float
    rerank_score: Optional[float]
    evidence_quality: str

class HybridRanker:
    """
    Hybrid ranking engine that combines BM25 and Semantic search results,
    using score normalization and Reciprocal Rank Fusion (RRF).
    """
    def __init__(self, inverted_index: Any, vector_store: Any, config: Optional[RankConfig] = None):
        self.inverted_index = inverted_index
        self.vector_store = vector_store
        self.config = config or RankConfig()
        
    def reciprocal_rank_fusion(self, *ranked_lists: List[str], k: int = 60) -> List[Tuple[str, float]]:
        """
        Apply Reciprocal Rank Fusion (RRF) across multiple ranked lists.
        
        Args:
            ranked_lists: A variable number of lists containing doc_ids ranked by relevance.
            k: The RRF constant (default 60).
            
        Returns:
            A list of tuples (doc_id, rrf_score) sorted in descending order of score.
        """
        scores: Dict[str, float] = {}
        for r_list in ranked_lists:
            for rank, doc_id in enumerate(r_list):
                if doc_id not in scores:
                    scores[doc_id] = 0.0
                scores[doc_id] += 1.0 / (k + rank + 1)
                
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores

    def _normalize_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Min-Max normalize scores to [0, 1] range."""
        if not scores:
            return {}
        vals = list(scores.values())
        min_val, max_val = min(vals), max(vals)
        if max_val == min_val:
            return {k: 1.0 for k in scores}
        return {k: (v - min_val) / (max_val - min_val) for k, v in scores.items()}
        
    def rank(self, query: str, query_embedding: List[float], top_k: int = 10) -> List[RankedResult]:
        """
        Rank search results combining sparse and dense retrieval.
        
        Args:
            query: The plaintext query for the inverted index.
            query_embedding: The embedding vector for semantic search.
            top_k: Number of final results to return (overrides config.final_top_k).
            
        Returns:
            A list of RankedResult instances.
        """
        # 1. Get BM25 results
        bm25_raw = []
        if hasattr(self.inverted_index, 'search'):
            bm25_raw = self.inverted_index.search(query, top_k=self.config.rerank_top_k)
        bm25_scores = {r.doc_id: getattr(r, 'score', 0.0) for r in bm25_raw}
        bm25_metadata = {r.doc_id: getattr(r, 'metadata', {}) for r in bm25_raw}
        
        # 2. Get semantic results
        semantic_raw = []
        if hasattr(self.vector_store, 'search'):
            semantic_raw = self.vector_store.search(query_embedding, top_k=self.config.rerank_top_k)
        semantic_scores = {r.doc_id: getattr(r, 'score', 0.0) for r in semantic_raw}
        semantic_metadata = {r.doc_id: getattr(r, 'metadata', {}) for r in semantic_raw}
        
        # Merge metadata
        all_doc_ids = set(bm25_scores.keys()).union(set(semantic_scores.keys()))
        metadata_map = {}
        for doc_id in all_doc_ids:
            metadata_map[doc_id] = bm25_metadata.get(doc_id, semantic_metadata.get(doc_id, {}))
            
        # 3. Normalize score distributions
        bm25_norm = self._normalize_scores(bm25_scores)
        semantic_norm = self._normalize_scores(semantic_scores)
        
        # 4. Combine with weighted sum
        combined_scores: Dict[str, float] = {}
        for doc_id in all_doc_ids:
            b_score = bm25_norm.get(doc_id, 0.0)
            s_score = semantic_norm.get(doc_id, 0.0)
            combined_scores[doc_id] = (
                self.config.bm25_weight * b_score + 
                self.config.semantic_weight * s_score
            )
            
        # 5. Apply RRF as tiebreaker
        bm25_ranked = [doc_id for doc_id, _ in sorted(bm25_scores.items(), key=lambda x: x[1], reverse=True)]
        semantic_ranked = [doc_id for doc_id, _ in sorted(semantic_scores.items(), key=lambda x: x[1], reverse=True)]
        rrf_scores = dict(self.reciprocal_rank_fusion(bm25_ranked, semantic_ranked, k=60))
        
        # Rank by combined_score primarily, then RRF
        ranked_docs = sorted(
            all_doc_ids,
            key=lambda d: (combined_scores[d], rrf_scores.get(d, 0.0)),
            reverse=True
        )
        
        # Filter top-k for reranking
        ranked_docs = ranked_docs[:self.config.rerank_top_k]
        
        # 6. Optionally apply cross-encoder reranking
        rerank_scores_map = {}
        try:
            import sentence_transformers
            # Implementation for cross-encoder reranking would go here
            logger.debug("Sentence transformers available. Proceeding without reranking for now.")
        except ImportError:
            pass
            
        results: List[RankedResult] = []
        for doc_id in ranked_docs:
            c_score = combined_scores[doc_id]
            if c_score < self.config.min_score_threshold:
                continue
                
            # 7. Classify evidence quality
            quality = 'LOW'
            if c_score > 0.8:
                quality = 'HIGH'
            elif c_score > 0.4:
                quality = 'MEDIUM'
                
            meta = metadata_map.get(doc_id, {})
            results.append(RankedResult(
                doc_id=doc_id,
                url=meta.get('url', ''),
                title=meta.get('title', ''),
                snippet=meta.get('snippet', ''),
                bm25_score=bm25_scores.get(doc_id, 0.0),
                semantic_score=semantic_scores.get(doc_id, 0.0),
                combined_score=c_score,
                rerank_score=rerank_scores_map.get(doc_id, None),
                evidence_quality=quality
            ))
            
        final_k = min(top_k, self.config.final_top_k)
        return results[:final_k]
