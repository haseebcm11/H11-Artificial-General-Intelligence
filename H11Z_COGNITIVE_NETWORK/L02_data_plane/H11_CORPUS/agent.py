import re
import hashlib
import random
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field

@dataclass
class ExtractionRule:
    min_length: int = 50
    remove_html: bool = True
    target_languages: List[str] = field(default_factory=lambda: ["en"])

@dataclass
class CorpusStats:
    total_docs: int = 0
    total_words: int = 0
    exact_dups: int = 0
    fuzzy_dups: int = 0
    filtered_out: int = 0

@dataclass
class Document:
    doc_id: str
    content: str
    metadata: Dict[str, str]

class CorpusManagerAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.num_perm = config.get("minhash_num_permutations", 128)
        self.bands = config.get("lsh_bands", 16)
        self.rows_per_band = self.num_perm // self.bands
        self.hash_seeds = [random.randint(1, 2**32 - 1) for _ in range(self.num_perm)]
        
        self.exact_seen: Set[str] = set()
        self.lsh_buckets: Dict[str, List[str]] = {}
        self.stats = CorpusStats()

    def clean_text(self, raw_text: str, rules: ExtractionRule) -> Optional[str]:
        """Applies basic extraction and cleaning heuristics."""
        if rules.remove_html:
            # Very naive HTML strip for demonstration
            clean = re.sub(r'<[^>]+>', ' ', raw_text)
        else:
            clean = raw_text
            
        clean = re.sub(r'\s+', ' ', clean).strip()
        
        if len(clean.split()) < rules.min_length:
            self.stats.filtered_out += 1
            return None
            
        return clean

    def _compute_minhash(self, text: str) -> List[int]:
        """Computes a MinHash signature for the document."""
        tokens = set(text.lower().split())
        signature = [float('inf')] * self.num_perm
        
        for token in tokens:
            token_hash = int(hashlib.md5(token.encode('utf-8')).hexdigest()[:8], 16)
            for i in range(self.num_perm):
                # Simulated universal hashing
                h = (token_hash ^ self.hash_seeds[i]) % (2**32)
                if h < signature[i]:
                    signature[i] = h
                    
        return signature

    def is_duplicate(self, doc_id: str, text: str) -> bool:
        """Runs exact and fuzzy deduplication logic."""
        # 1. Exact Dedup
        sha = hashlib.sha256(text.encode('utf-8')).hexdigest()
        if sha in self.exact_seen:
            self.stats.exact_dups += 1
            return True
        self.exact_seen.add(sha)
        
        # 2. Fuzzy Dedup via LSH
        sig = self._compute_minhash(text)
        is_fuzzy_dup = False
        
        for b in range(self.bands):
            start = b * self.rows_per_band
            band_tuple = tuple(sig[start:start + self.rows_per_band])
            bucket_key = f"b{b}_{hash(band_tuple)}"
            
            if bucket_key in self.lsh_buckets:
                # In a real system, we'd fetch the docs in the bucket and compute exact Jaccard.
                # Here, falling into the same bucket is treated as a duplicate.
                is_fuzzy_dup = True
                break
                
            if bucket_key not in self.lsh_buckets:
                self.lsh_buckets[bucket_key] = []
            self.lsh_buckets[bucket_key].append(doc_id)
            
        if is_fuzzy_dup:
            self.stats.fuzzy_dups += 1
            return True
            
        return False

    def ingest_corpus(self, docs: List[Document], rules: ExtractionRule) -> List[Document]:
        """Main pipeline for ingesting, cleaning, and deduplicating a corpus."""
        processed_corpus = []
        
        for doc in docs:
            self.stats.total_docs += 1
            
            clean_content = self.clean_text(doc.content, rules)
            if not clean_content:
                continue
                
            self.stats.total_words += len(clean_content.split())
            
            if not self.is_duplicate(doc.doc_id, clean_content):
                processed_corpus.append(Document(
                    doc_id=doc.doc_id,
                    content=clean_content,
                    metadata=doc.metadata
                ))
                
        return processed_corpus

    def get_statistics(self) -> CorpusStats:
        return self.stats
