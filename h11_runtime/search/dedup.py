"""64-bit SimHash & MinHash LSH Near-Duplicate Deduplication Engine.

Provides:
- 64-bit SimHash calculation over word and character n-gram features.
- Inverted Hamming table for sub-millisecond near-duplicate lookup (k <= 3).
- MinHash LSH for Jaccard similarity estimation across large web document sets.
- URL normalization & canonicalization (strips query tracking, hash fragments, port normalization).
"""
from __future__ import annotations

import hashlib
import re
import urllib.parse
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


def canonicalize_url(url: str) -> str:
    """Normalizes and canonicalizes a URL to eliminate duplicates."""
    if not url:
        return ""
    try:
        parsed = urllib.parse.urlparse(url.strip())
        scheme = parsed.scheme.lower() or "http"
        netloc = parsed.netloc.lower()

        # Remove default ports
        if (scheme == "http" and netloc.endswith(":80")) or (scheme == "https" and netloc.endswith(":443")):
            netloc = netloc.rsplit(":", 1)[0]

        # Strip www. prefix for canonical grouping (keep domain consistent)
        if netloc.startswith("www."):
            netloc = netloc[4:]

        path = parsed.path or "/"
        # Collapse multiple consecutive slashes
        path = re.sub(r"/+", "/", path)
        if len(path) > 1 and path.endswith("/"):
            path = path[:-1]

        # Filter out tracking query parameters
        ignored_params = {
            "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
            "fbclid", "gclid", "msclkid", "ref", "source", "ref_src", "spm"
        }
        query_pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=False)
        clean_pairs = sorted([(k, v) for k, v in query_pairs if k.lower() not in ignored_params])
        clean_query = urllib.parse.urlencode(clean_pairs)

        # No fragment hash
        return urllib.parse.urlunparse((scheme, netloc, path, "", clean_query, ""))
    except Exception:
        return url.strip().lower()


class SimHash:
    """64-bit SimHash algorithm for near-duplicate text detection."""

    def __init__(self, text: str, f: int = 64) -> None:
        self.f = f
        self.value = self._compute(text)

    def _compute(self, text: str) -> int:
        """Computes 64-bit fingerprint from text tokens."""
        tokens = re.findall(r"\w+", text.lower())
        if not tokens:
            return 0

        # Character 3-grams for richer sub-word coverage if text is short
        features: List[str] = tokens
        if len(tokens) < 10:
            features = [text[i : i + 3] for i in range(len(text) - 2)] or tokens

        v = [0] * self.f
        for token in features:
            # 64-bit MD5 prefix hash
            h = int(hashlib.md5(token.encode("utf-8")).hexdigest()[:16], 16)
            for i in range(self.f):
                bit = (h >> i) & 1
                v[i] += 1 if bit == 1 else -1

        fingerprint = 0
        for i in range(self.f):
            if v[i] > 0:
                fingerprint |= 1 << i
        return fingerprint

    def distance(self, other: SimHash) -> int:
        """Calculates bitwise Hamming distance between two SimHashes."""
        x = (self.value ^ other.value) & ((1 << self.f) - 1)
        # Brian Kernighan bit-count algorithm
        dist = 0
        while x:
            dist += 1
            x &= x - 1
        return dist

    def similarity(self, other: SimHash) -> float:
        """Calculates normalized similarity [0.0, 1.0] based on Hamming distance."""
        dist = self.distance(other)
        return max(0.0, 1.0 - (dist / float(self.f)))


class SimHashIndex:
    """Fast in-memory index for finding near-duplicate SimHashes within threshold k."""

    def __init__(self, k: int = 3, f: int = 64) -> None:
        self.k = k  # Max Hamming distance threshold (default 3)
        self.f = f
        self.num_blocks = k + 1
        self.block_size = f // self.num_blocks
        # Tables for sub-blocks: table_idx -> {block_val -> set(doc_id)}
        self._tables: List[Dict[int, Set[str]]] = [{} for _ in range(self.num_blocks)]
        self._hashes: Dict[str, SimHash] = {}

    def _get_block_keys(self, simhash: SimHash) -> List[int]:
        keys = []
        for i in range(self.num_blocks):
            mask = (1 << self.block_size) - 1
            shift = i * self.block_size
            key = (simhash.value >> shift) & mask
            keys.append(key)
        return keys

    def add(self, doc_id: str, simhash: SimHash) -> None:
        """Adds a document SimHash to the index."""
        self._hashes[doc_id] = simhash
        keys = self._get_block_keys(simhash)
        for i, key in enumerate(keys):
            if key not in self._tables[i]:
                self._tables[i][key] = set()
            self._tables[i][key].add(doc_id)

    def find_near_duplicates(self, simhash: SimHash) -> List[Tuple[str, int]]:
        """Returns list of (doc_id, distance) for docs within Hamming distance k."""
        candidates: Set[str] = set()
        keys = self._get_block_keys(simhash)
        for i, key in enumerate(keys):
            if key in self._tables[i]:
                candidates.update(self._tables[i][key])

        matches = []
        for doc_id in candidates:
            other = self._hashes.get(doc_id)
            if other is not None:
                dist = simhash.distance(other)
                if dist <= self.k:
                    matches.append((doc_id, dist))
        return sorted(matches, key=lambda x: x[1])

    def is_duplicate(self, text: str) -> bool:
        """Checks if given text is a near-duplicate of an already indexed document."""
        sh = SimHash(text, self.f)
        matches = self.find_near_duplicates(sh)
        return len(matches) > 0


class MinHash:
    """128-permutation MinHash for estimating Jaccard set similarity."""

    def __init__(self, num_perm: int = 128) -> None:
        self.num_perm = num_perm
        # Deterministic universal hash parameters: (a * x + b) % prime
        self._prime = 4294967311
        self._a = [((i * 10007 + 3) % self._prime) or 1 for i in range(num_perm)]
        self._b = [(i * 20011 + 7) % self._prime for i in range(num_perm)]

    def compute(self, text: str) -> List[int]:
        """Computes MinHash signature from shingle tokens."""
        tokens = set(re.findall(r"\w+", text.lower()))
        if not tokens:
            return [0] * self.num_perm

        sig = [0xFFFFFFFF] * self.num_perm
        for token in tokens:
            token_hash = int(hashlib.sha256(token.encode("utf-8")).hexdigest()[:8], 16)
            for i in range(self.num_perm):
                val = (self._a[i] * token_hash + self._b[i]) % self._prime
                if val < sig[i]:
                    sig[i] = val
        return sig

    @staticmethod
    def jaccard_similarity(sig_a: List[int], sig_b: List[int]) -> float:
        """Estimates Jaccard similarity between two MinHash signatures."""
        if not sig_a or not sig_b or len(sig_a) != len(sig_b):
            return 0.0
        matches = sum(1 for a, b in zip(sig_a, sig_b) if a == b)
        return float(matches) / float(len(sig_a))
