from __future__ import annotations
import asyncio
import json
import logging
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Any

logger = logging.getLogger(__name__)

class IndexerException(Exception):
    """Custom exception for indexer errors."""
    pass

DEFAULT_STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for",
    "if", "in", "into", "is", "it", "no", "not", "of", "on", "or",
    "such", "that", "the", "their", "then", "there", "these", "they",
    "this", "to", "was", "will", "with"
}

@dataclass
class IndexConfig:
    k1: float = 1.5
    b: float = 0.75
    min_token_length: int = 2
    max_token_length: int = 50
    stop_words: Set[str] = field(default_factory=lambda: set(DEFAULT_STOP_WORDS))

@dataclass
class TokenStats:
    term_frequency: int
    document_frequency: int
    positions: List[int]

@dataclass
class DocumentEntry:
    doc_id: str
    url: str
    title: str
    content_hash: str
    token_count: int
    indexed_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SearchHit:
    doc_id: str
    url: str
    title: str
    score: float
    snippet: str
    matched_terms: List[str]

class Tokenizer:
    def __init__(self, config: IndexConfig):
        self.config = config
        self._pattern = re.compile(r'\b\w+\b')

    def tokenize(self, text: str) -> List[str]:
        text = text.lower()
        raw_tokens = self._pattern.findall(text)
        tokens = []
        for t in raw_tokens:
            t = t.strip("_")
            if len(t) < self.config.min_token_length or len(t) > self.config.max_token_length:
                continue
            if t in self.config.stop_words:
                continue
            t = self._stem(t)
            tokens.append(t)
        return tokens

    def _stem(self, word: str) -> str:
        suffixes = ['ing', 'ly', 'ed', 'es', 's']
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) - len(suffix) >= 3:
                return word[:-len(suffix)]
        return word

class InvertedIndex:
    def __init__(self, config: Optional[IndexConfig] = None):
        self.config = config or IndexConfig()
        self.tokenizer = Tokenizer(self.config)
        
        # Internal state
        # term -> doc_id -> TokenStats
        self._index: Dict[str, Dict[str, TokenStats]] = {}
        self._documents: Dict[str, DocumentEntry] = {}
        self._raw_texts: Dict[str, str] = {}
        self._total_token_count: int = 0

    def add_document(self, doc_id: str, url: str, title: str, text: str, metadata: Optional[Dict] = None) -> None:
        if doc_id in self._documents:
            self.remove_document(doc_id)

        tokens = self.tokenizer.tokenize(text)
        token_count = len(tokens)
        self._total_token_count += token_count

        # Compute term frequencies and positions
        term_positions: Dict[str, List[int]] = {}
        for pos, term in enumerate(tokens):
            if term not in term_positions:
                term_positions[term] = []
            term_positions[term].append(pos)

        for term, positions in term_positions.items():
            if term not in self._index:
                self._index[term] = {}
            # Initialize with 0 df, will be updated collectively below
            self._index[term][doc_id] = TokenStats(
                term_frequency=len(positions),
                document_frequency=0,
                positions=positions
            )

        entry = DocumentEntry(
            doc_id=doc_id,
            url=url,
            title=title,
            content_hash=str(hash(text)),
            token_count=token_count,
            indexed_at=datetime.now(timezone.utc),
            metadata=metadata or {}
        )
        self._documents[doc_id] = entry
        self._raw_texts[doc_id] = text

        # Update document_frequency for all affected terms
        for term in term_positions.keys():
            df = len(self._index[term])
            for d_id, stats in self._index[term].items():
                stats.document_frequency = df

    def remove_document(self, doc_id: str) -> None:
        if doc_id not in self._documents:
            return

        entry = self._documents.pop(doc_id)
        self._total_token_count -= entry.token_count
        self._raw_texts.pop(doc_id, None)

        empty_terms = []
        for term, doc_map in self._index.items():
            if doc_id in doc_map:
                del doc_map[doc_id]
                if not doc_map:
                    empty_terms.append(term)
                else:
                    df = len(doc_map)
                    for d_id, stats in doc_map.items():
                        stats.document_frequency = df

        for term in empty_terms:
            del self._index[term]

    def search(self, query: str, top_k: int = 10) -> List[SearchHit]:
        query_tokens = self.tokenizer.tokenize(query)
        if not query_tokens or not self._documents:
            return []

        scores: Dict[str, float] = {}
        matched_terms_map: Dict[str, Set[str]] = {}

        N = len(self._documents)
        avgdl = self._total_token_count / N if N > 0 else 0
        k1 = self.config.k1
        b = self.config.b

        for term in set(query_tokens):
            if term not in self._index:
                continue
            
            doc_map = self._index[term]
            n_qi = len(doc_map)
            idf = math.log((N - n_qi + 0.5) / (n_qi + 0.5) + 1.0)

            for doc_id, stats in doc_map.items():
                f_qi_D = stats.term_frequency
                D_len = self._documents[doc_id].token_count

                numerator = f_qi_D * (k1 + 1)
                denominator = f_qi_D + k1 * (1 - b + b * (D_len / avgdl))
                term_score = idf * (numerator / denominator)

                scores[doc_id] = scores.get(doc_id, 0.0) + term_score
                if doc_id not in matched_terms_map:
                    matched_terms_map[doc_id] = set()
                matched_terms_map[doc_id].add(term)

        results = []
        for doc_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]:
            doc_entry = self._documents[doc_id]
            matched_terms = list(matched_terms_map[doc_id])
            snippet = self.get_snippet(doc_id, matched_terms)
            results.append(SearchHit(
                doc_id=doc_id,
                url=doc_entry.url,
                title=doc_entry.title,
                score=score,
                snippet=snippet,
                matched_terms=matched_terms
            ))

        return results

    def get_snippet(self, doc_id: str, query_terms: List[str], snippet_length: int = 200) -> str:
        text = self._raw_texts.get(doc_id, "")
        if not text:
            return ""

        text_lower = text.lower()
        first_idx = -1

        for qt in query_terms:
            idx = text_lower.find(qt)
            if idx != -1 and (first_idx == -1 or idx < first_idx):
                first_idx = idx

        if first_idx == -1:
            return text[:snippet_length] + "..." if len(text) > snippet_length else text

        half_length = snippet_length // 2
        start = max(0, first_idx - half_length)
        end = min(len(text), first_idx + half_length)

        if start > 0:
            while start < len(text) and not text[start].isspace():
                start += 1
        if end < len(text):
            while end > 0 and not text[end].isspace():
                end -= 1

        snippet = text[start:end].strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
            
        return snippet

    async def save(self, path: str) -> None:
        data = {
            "config": {
                "k1": self.config.k1,
                "b": self.config.b,
                "min_token_length": self.config.min_token_length,
                "max_token_length": self.config.max_token_length,
                "stop_words": list(self.config.stop_words)
            },
            "documents": {
                doc_id: {
                    "doc_id": entry.doc_id,
                    "url": entry.url,
                    "title": entry.title,
                    "content_hash": entry.content_hash,
                    "token_count": entry.token_count,
                    "indexed_at": entry.indexed_at.isoformat(),
                    "metadata": entry.metadata
                } for doc_id, entry in self._documents.items()
            },
            "raw_texts": self._raw_texts,
            "index": {
                term: {
                    doc_id: {
                        "term_frequency": stats.term_frequency,
                        "document_frequency": stats.document_frequency,
                        "positions": stats.positions
                    } for doc_id, stats in doc_map.items()
                } for term, doc_map in self._index.items()
            },
            "total_token_count": self._total_token_count
        }

        def _write():
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        await asyncio.to_thread(_write)

    @classmethod
    async def load(cls, path: str) -> InvertedIndex:
        def _read():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)

        data = await asyncio.to_thread(_read)
        
        config_data = data["config"]
        config = IndexConfig(
            k1=config_data["k1"],
            b=config_data["b"],
            min_token_length=config_data["min_token_length"],
            max_token_length=config_data["max_token_length"],
            stop_words=set(config_data["stop_words"])
        )

        idx = cls(config)
        idx._total_token_count = data.get("total_token_count", 0)
        idx._raw_texts = data.get("raw_texts", {})

        for doc_id, doc_dict in data.get("documents", {}).items():
            idx._documents[doc_id] = DocumentEntry(
                doc_id=doc_dict["doc_id"],
                url=doc_dict["url"],
                title=doc_dict["title"],
                content_hash=doc_dict["content_hash"],
                token_count=doc_dict["token_count"],
                indexed_at=datetime.fromisoformat(doc_dict["indexed_at"]),
                metadata=doc_dict["metadata"]
            )

        for term, doc_map in data.get("index", {}).items():
            idx._index[term] = {}
            for doc_id, stats_dict in doc_map.items():
                idx._index[term][doc_id] = TokenStats(
                    term_frequency=stats_dict["term_frequency"],
                    document_frequency=stats_dict["document_frequency"],
                    positions=stats_dict["positions"]
                )

        return idx

    @property
    def stats(self) -> Dict[str, Any]:
        N = len(self._documents)
        return {
            "num_docs": N,
            "num_terms": len(self._index),
            "avg_doc_length": self._total_token_count / N if N > 0 else 0
        }
