from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Any
import logging

logger = logging.getLogger(__name__)

@dataclass
class RetrievedDocument:
    doc_id: str
    url: str
    title: str
    content: str
    snippet: str
    relevance_score: float
    source_type: str  # 'web', 'index', 'knowledge_graph'
    retrieved_at: datetime
    domain: Optional[str] = None

@dataclass
class ReasoningContext:
    agent_id: str
    case_id: str
    query: str
    retrieved_docs: List[RetrievedDocument]
    knowledge_triples: List[Any]
    grounding_chain: List[str]
    total_evidence_score: float

@dataclass
class EvidenceGrounding:
    claim: str
    supporting_docs: List[str]
    confidence: float
    provenance: str

class RetrievalAugmentedReasoner:
    def __init__(self, search_service: Any):
        self.search_service = search_service

    async def retrieve_for_agent(self, agent_id: str, query: str, domain_filter: Optional[str] = None, max_results: int = 10, freshness: str = 'any') -> List[RetrievedDocument]:
        search_query_cls = getattr(self.search_service, 'SearchQuery', None)
        if search_query_cls is None:
            # Fallback import if passed instance dynamically
            try:
                from .api import SearchQuery
                search_query_cls = SearchQuery
            except ImportError:
                return []
                
        if search_query_cls:
            sq = search_query_cls(
                text=query,
                domain_filter=domain_filter,
                freshness=freshness,
                max_results=max_results
            )
            response = await self.search_service.search(sq)
            docs = []
            for i, r in enumerate(response.results):
                docs.append(RetrievedDocument(
                    doc_id=f"doc_{i}",
                    url=r.get('url', ''),
                    title=r.get('title', ''),
                    content=r.get('content', ''),
                    snippet=r.get('snippet', ''),
                    relevance_score=r.get('score', 0.5),
                    source_type='web',
                    retrieved_at=datetime.utcnow(),
                    domain=domain_filter
                ))
            return docs
        return []

    async def build_reasoning_context(self, agent_id: str, case_id: str, query: str, domain_filter: Optional[str] = None) -> ReasoningContext:
        docs = await self.retrieve_for_agent(agent_id, query, domain_filter)
        score = self.compute_evidence_score(docs)
        
        return ReasoningContext(
            agent_id=agent_id,
            case_id=case_id,
            query=query,
            retrieved_docs=docs,
            knowledge_triples=[],
            grounding_chain=[],
            total_evidence_score=score
        )

    def ground_evidence(self, claim: str, context: ReasoningContext) -> EvidenceGrounding:
        supporting = []
        claim_words = set(claim.lower().split())
        for doc in context.retrieved_docs:
            doc_words = set((doc.title + " " + doc.content).lower().split())
            if len(claim_words.intersection(doc_words)) > 0:
                supporting.append(doc.doc_id)
                
        confidence = len(supporting) / len(context.retrieved_docs) if context.retrieved_docs else 0.0
        
        return EvidenceGrounding(
            claim=claim,
            supporting_docs=supporting,
            confidence=min(1.0, confidence * 2.0),
            provenance="Keyword overlap with retrieved context."
        )

    def summarize_evidence(self, context: ReasoningContext, max_length: int = 2000) -> str:
        summary = f"Evidence Summary for Query: '{context.query}'\n\n"
        for doc in context.retrieved_docs:
            part = f"- [{doc.source_type}] {doc.title} ({doc.url}): {doc.snippet}\n"
            if len(summary) + len(part) > max_length:
                summary += "...\n[Truncated]"
                break
            summary += part
        return summary

    def compute_evidence_score(self, docs: List[RetrievedDocument]) -> float:
        if not docs:
            return 0.0
        
        total_score = sum(doc.relevance_score for doc in docs)
        avg_score = total_score / len(docs)
        
        sources = {doc.source_type for doc in docs}
        diversity_bonus = 0.1 * (len(sources) - 1)
        
        return min(1.0, avg_score + diversity_bonus)
