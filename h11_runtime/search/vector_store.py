from __future__ import annotations
import math
import logging
import json
import os
import pickle
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

@dataclass
class VectorStoreConfig:
    """Configuration for the VectorStore."""
    dimension: int
    distance_metric: str = 'cosine'  # Options: 'cosine', 'l2', 'ip'
    ef_construction: int = 200
    M: int = 16
    ef_search: int = 50
    max_elements: int = 1_000_000

@dataclass
class VectorRecord:
    """A single vector record to be stored."""
    doc_id: str
    vector: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SearchResult:
    """Result from a vector search."""
    doc_id: str
    distance: float
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)

class VectorStore:
    """
    An approximate nearest neighbor vector store.
    Gracefully falls back across:
    faiss -> hnswlib -> brute-force numpy -> brute-force pure Python.
    """
    def __init__(self, config: VectorStoreConfig):
        self.config = config
        self.index = None
        self.index_type = "pure_python"
        self.doc_ids: List[str] = []
        self.vectors: List[List[float]] = []
        self.metadatas: List[Dict[str, Any]] = []
        
        self._init_index()
        
    def _init_index(self) -> None:
        """Initialize the best available backend index."""
        try:
            import faiss
            import numpy as np
            self.index_type = "faiss"
            if self.config.distance_metric == 'l2':
                self.index = faiss.IndexFlatL2(self.config.dimension)
            else:
                self.index = faiss.IndexFlatIP(self.config.dimension)
            logger.info("Initialized FAISS vector index.")
            return
        except ImportError:
            pass
            
        try:
            import hnswlib
            import numpy as np
            self.index_type = "hnswlib"
            space = 'l2' if self.config.distance_metric == 'l2' else 'cosine'
            if self.config.distance_metric == 'ip':
                space = 'ip'
            self.index = hnswlib.Index(space=space, dim=self.config.dimension)
            self.index.init_index(
                max_elements=self.config.max_elements,
                ef_construction=self.config.ef_construction,
                M=self.config.M
            )
            self.index.set_ef(self.config.ef_search)
            logger.info("Initialized hnswlib vector index.")
            return
        except ImportError:
            pass
            
        try:
            import numpy as np
            self.index_type = "numpy"
            logger.info("Initialized numpy brute-force vector index.")
            return
        except ImportError:
            pass
            
        self.index_type = "pure_python"
        logger.info("Initialized pure-python brute-force vector index.")
        
    def _normalize(self, vec: List[float]) -> List[float]:
        """Normalize a vector to unit length for cosine similarity."""
        norm = math.sqrt(sum(v * v for v in vec))
        if norm == 0:
            return vec
        return [v / norm for v in vec]
        
    def add(self, doc_id: str, vector: List[float], metadata: Optional[Dict] = None) -> None:
        """Add a single vector to the store."""
        if len(vector) != self.config.dimension:
            raise ValueError(f"Vector dimension {len(vector)} does not match config {self.config.dimension}")
            
        if self.config.distance_metric == 'cosine':
            vector = self._normalize(vector)
            
        idx = len(self.doc_ids)
        
        if self.index_type == "faiss":
            import numpy as np
            self.index.add(np.array([vector], dtype=np.float32))
        elif self.index_type == "hnswlib":
            import numpy as np
            self.index.add_items(np.array([vector], dtype=np.float32), np.array([idx]))
            
        self.doc_ids.append(doc_id)
        self.vectors.append(vector)
        self.metadatas.append(metadata or {})
        
    def add_batch(self, records: List[VectorRecord]) -> int:
        """Add a batch of records to the store."""
        for rec in records:
            self.add(rec.doc_id, rec.vector, rec.metadata)
        return len(records)
        
    def search(self, query_vector: List[float], top_k: int = 10) -> List[SearchResult]:
        """Search the store for nearest neighbors to the query vector."""
        if not self.doc_ids:
            return []
            
        if len(query_vector) != self.config.dimension:
            raise ValueError("Query vector dimension mismatch.")
            
        if self.config.distance_metric == 'cosine':
            query_vector = self._normalize(query_vector)
            
        results: List[SearchResult] = []
        
        if self.index_type == "faiss":
            import numpy as np
            q = np.array([query_vector], dtype=np.float32)
            distances, indices = self.index.search(q, min(top_k, len(self.doc_ids)))
            for d, i in zip(distances[0], indices[0]):
                if i != -1 and i < len(self.doc_ids):
                    score = float(d) if self.config.distance_metric != 'l2' else 1.0 / (1.0 + float(d))
                    results.append(SearchResult(self.doc_ids[i], float(d), score, self.metadatas[i]))
                    
        elif self.index_type == "hnswlib":
            import numpy as np
            q = np.array([query_vector], dtype=np.float32)
            labels, distances = self.index.knn_query(q, k=min(top_k, len(self.doc_ids)))
            for i, d in zip(labels[0], distances[0]):
                score = 1.0 - float(d) if self.config.distance_metric != 'l2' else 1.0 / (1.0 + float(d))
                results.append(SearchResult(self.doc_ids[i], float(d), score, self.metadatas[i]))
                
        elif self.index_type == "numpy":
            import numpy as np
            q = np.array(query_vector, dtype=np.float32)
            mat = np.array(self.vectors, dtype=np.float32)
            if self.config.distance_metric in ('cosine', 'ip'):
                scores = np.dot(mat, q)
                indices = np.argsort(scores)[::-1][:top_k]
                for i in indices:
                    results.append(SearchResult(self.doc_ids[i], -float(scores[i]), float(scores[i]), self.metadatas[i]))
            else:
                diff = mat - q
                distances = np.sum(diff * diff, axis=1)
                indices = np.argsort(distances)[:top_k]
                for i in indices:
                    results.append(SearchResult(self.doc_ids[i], float(distances[i]), 1.0 / (1.0 + float(distances[i])), self.metadatas[i]))
                    
        else:
            # Pure python fallback
            scored = []
            for i, vec in enumerate(self.vectors):
                if self.config.distance_metric in ('cosine', 'ip'):
                    score = sum(v * q for v, q in zip(vec, query_vector))
                    scored.append((i, -score, score))
                else:
                    dist = sum((v - q) ** 2 for v, q in zip(vec, query_vector))
                    scored.append((i, dist, 1.0 / (1.0 + dist)))
            
            scored.sort(key=lambda x: (x[1] if self.config.distance_metric == 'l2' else -x[2]))
            for i, d, s in scored[:top_k]:
                results.append(SearchResult(self.doc_ids[i], d, s, self.metadatas[i]))
                
        return results
        
    def delete(self, doc_id: str) -> bool:
        """Delete a document by id. May trigger an index rebuild for external backends."""
        try:
            idx = self.doc_ids.index(doc_id)
            self.doc_ids.pop(idx)
            self.vectors.pop(idx)
            self.metadatas.pop(idx)
            
            # Rebuild index if using faiss or hnswlib since deletion is non-trivial there
            if self.index_type in ("faiss", "hnswlib"):
                self._init_index()
                vectors_copy = list(self.vectors)
                ids_copy = list(self.doc_ids)
                metas_copy = list(self.metadatas)
                self.doc_ids.clear()
                self.vectors.clear()
                self.metadatas.clear()
                for i in range(len(vectors_copy)):
                    self.add(ids_copy[i], vectors_copy[i], metas_copy[i])
            return True
        except ValueError:
            return False

    def save(self, directory: str) -> None:
        """Save the vector store to disk."""
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, "config.json"), "w") as f:
            json.dump({
                "dimension": self.config.dimension,
                "distance_metric": self.config.distance_metric,
                "ef_construction": self.config.ef_construction,
                "M": self.config.M,
                "ef_search": self.config.ef_search,
                "max_elements": self.config.max_elements
            }, f)
            
        with open(os.path.join(directory, "data.pkl"), "wb") as f:
            pickle.dump({
                "doc_ids": self.doc_ids,
                "vectors": self.vectors,
                "metadatas": self.metadatas
            }, f)

    @classmethod
    def load(cls, directory: str) -> VectorStore:
        """Load the vector store from disk."""
        with open(os.path.join(directory, "config.json"), "r") as f:
            data = json.load(f)
            config = VectorStoreConfig(**data)
        
        store = cls(config)
        with open(os.path.join(directory, "data.pkl"), "rb") as f:
            d = pickle.load(f)
            doc_ids = d["doc_ids"]
            vectors = d["vectors"]
            metadatas = d["metadatas"]
            
            for i in range(len(doc_ids)):
                store.add(doc_ids[i], vectors[i], metadatas[i])
        return store

    @property
    def size(self) -> int:
        """Get the number of stored vectors."""
        return len(self.doc_ids)
