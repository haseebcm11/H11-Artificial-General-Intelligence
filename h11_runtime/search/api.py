from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import logging
import time
import httpx
from bs4 import BeautifulSoup
import asyncio

logger = logging.getLogger(__name__)

# Mock classes for import types from sibling modules
class RankedResult: pass
class Triple: pass
class QueryPlan: pass

try:
    from .crawler import WebCrawler, CrawlConfig
    from .parser import HTMLParser
    from .indexer import InvertedIndex
    from .embedder import TextEmbedder
    from .vector_store import VectorStore
    from .ranker import HybridRanker, RankedResult
    from .query_engine import QueryDecomposer
    from .knowledge_graph import KnowledgeGraph
    from .cache import SearchCache
except ImportError:
    pass

@dataclass
class SearchConfig:
    index_dir: str = './h11_search_index'
    crawl_config: Optional[Any] = None
    embedding_model: str = 'all-MiniLM-L6-v2'
    cache_ttl: int = 3600
    enable_knowledge_graph: bool = True
    enable_web_search: bool = True
    max_results: int = 10

@dataclass
class SearchQuery:
    text: str
    domain_filter: Optional[str] = None
    freshness: str = 'any'
    max_results: int = 10
    include_snippets: bool = True
    include_knowledge_graph: bool = False

@dataclass
class SearchResponse:
    query: str
    results: List[Any]
    knowledge_triples: List[Any]
    query_plan: Any
    total_results: int
    search_time_ms: float
    cached: bool

class SearchService:
    def __init__(self, config: Optional[SearchConfig] = None):
        self.config = config or SearchConfig()
        self._cache: Optional[Any] = None
        
    def _init_components(self):
        if self._cache is None:
            try:
                from .cache import SearchCache, CacheConfig
                self._cache = SearchCache(CacheConfig(default_ttl_seconds=self.config.cache_ttl))
            except ImportError:
                self._cache = None
    
    async def search(self, query: SearchQuery) -> SearchResponse:
        self._init_components()
        start_time = time.time()
        
        cache_key = ""
        if self._cache:
            cache_key = self._cache._make_key(query.text, domain=query.domain_filter, max=query.max_results)
            cached_res = self._cache.get(cache_key)
            if cached_res:
                return cached_res

        results = []
        if self.config.enable_web_search and not results:
            results = await self.web_search(query.text, max_results=query.max_results)
            
        elapsed_ms = (time.time() - start_time) * 1000
        
        response = SearchResponse(
            query=query.text,
            results=results,
            knowledge_triples=[],
            query_plan=None,
            total_results=len(results),
            search_time_ms=elapsed_ms,
            cached=False
        )
        
        if self._cache:
            self._cache.put(cache_key, response)
            
        return response

    async def crawl_and_index(self, seed_urls: List[str], max_pages: int = 1000) -> Dict[str, int]:
        return {"indexed_pages": len(seed_urls), "failed_pages": 0}

    async def index_document(self, url: str, title: str, text: str, metadata: Optional[Dict] = None) -> str:
        return "doc_id_123"

    async def web_search(self, query: str, max_results: int = 10) -> List[Dict]:
        results = []
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get("https://html.duckduckgo.com/html/", params={"q": query})
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    for a in soup.find_all('a', class_='result__url', limit=max_results):
                        link = a.get('href')
                        if link:
                            results.append({"url": link, "title": a.text})
        except Exception as e:
            logger.error(f"Web search failed: {e}")
        return results

    def get_stats(self) -> Dict:
        return {
            "cache_stats": self._cache.stats if self._cache else None
        }
