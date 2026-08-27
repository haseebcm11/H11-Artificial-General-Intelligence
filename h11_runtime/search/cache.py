from __future__ import annotations
import threading
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Optional, Dict
import hashlib
import json
import logging
import re
import fnmatch
import sys

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    key: str
    value: Any
    created_at: datetime
    expires_at: datetime
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.utcnow)
    size_bytes: int = 0

@dataclass
class CacheConfig:
    max_entries: int = 10000
    max_memory_bytes: int = 500_000_000
    default_ttl_seconds: int = 3600
    eviction_policy: str = 'lru'  # 'lru', 'lfu', 'ttl'

class SearchCache:
    """
    Search result caching and freshness management system.
    """
    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.Lock()
        self._hit_count = 0
        self._miss_count = 0

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._cache.get(key)
            if not entry:
                self._miss_count += 1
                return None
            
            if datetime.utcnow() > entry.expires_at:
                del self._cache[key]
                self._miss_count += 1
                return None

            entry.access_count += 1
            entry.last_accessed = datetime.utcnow()
            self._hit_count += 1
            return entry.value

    def put(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        with self._lock:
            now = datetime.utcnow()
            ttl = ttl_seconds if ttl_seconds is not None else self.config.default_ttl_seconds
            expires_at = now + timedelta(seconds=ttl)
            
            try:
                size_bytes = sys.getsizeof(value)
            except Exception:
                size_bytes = 0

            entry = CacheEntry(
                key=key,
                value=value,
                created_at=now,
                expires_at=expires_at,
                size_bytes=size_bytes
            )
            
            self._cache[key] = entry
            self._evict()

    def invalidate(self, key: str) -> bool:
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def invalidate_pattern(self, pattern: str) -> int:
        with self._lock:
            regex = fnmatch.translate(pattern)
            prog = re.compile(regex)
            keys_to_delete = [k for k in self._cache.keys() if prog.match(k)]
            for k in keys_to_delete:
                del self._cache[k]
            return len(keys_to_delete)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
            self._hit_count = 0
            self._miss_count = 0

    def _evict(self) -> None:
        if len(self._cache) <= self.config.max_entries and \
           sum(e.size_bytes for e in self._cache.values()) <= self.config.max_memory_bytes:
            return

        now = datetime.utcnow()
        expired = [k for k, v in self._cache.items() if now > v.expires_at]
        for k in expired:
            del self._cache[k]

        while len(self._cache) > self.config.max_entries or \
              sum(e.size_bytes for e in self._cache.values()) > self.config.max_memory_bytes:
            
            if self.config.eviction_policy == 'lru':
                key_to_evict = min(self._cache.keys(), key=lambda k: self._cache[k].last_accessed)
            elif self.config.eviction_policy == 'lfu':
                key_to_evict = min(self._cache.keys(), key=lambda k: self._cache[k].access_count)
            elif self.config.eviction_policy == 'ttl':
                key_to_evict = min(self._cache.keys(), key=lambda k: self._cache[k].expires_at)
            else:
                key_to_evict = min(self._cache.keys(), key=lambda k: self._cache[k].last_accessed)
            
            del self._cache[key_to_evict]

    def _make_key(self, query: str, **params) -> str:
        data = {"query": query, "params": params}
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    @property
    def stats(self) -> Dict[str, Any]:
        with self._lock:
            total = self._hit_count + self._miss_count
            hit_rate = self._hit_count / total if total > 0 else 0.0
            size = sum(e.size_bytes for e in self._cache.values())
            return {
                "hit_count": self._hit_count,
                "miss_count": self._miss_count,
                "hit_rate": hit_rate,
                "size": size,
                "entry_count": len(self._cache)
            }
