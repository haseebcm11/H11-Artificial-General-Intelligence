from __future__ import annotations
import logging
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional, Any

logger = logging.getLogger(__name__)

class EmbedderException(Exception):
    """Custom exception for embedder errors."""
    pass

@dataclass
class EmbeddingConfig:
    model_name: str = 'all-MiniLM-L6-v2'
    batch_size: int = 32
    max_seq_length: int = 512
    normalize: bool = True
    device: str = 'cpu'
    cache_dir: Optional[str] = None

@dataclass
class EmbeddingResult:
    doc_id: str
    vector: List[float]
    model_name: str
    dimension: int
    computed_at: datetime

class TextEmbedder:
    def __init__(self, config: Optional[EmbeddingConfig] = None):
        self.config = config or EmbeddingConfig()
        self._model: Any = None
        self._fallback_mode: bool = False
        self._fallback_dim: int = 384

    def _load_model(self) -> None:
        """Lazy loads the sentence transformers model on first use."""
        if self._model is not None or self._fallback_mode:
            return
            
        if self.config.model_name in ("tfidf-fallback", "mock", "fallback", "none", "tfidf"):
            self._fallback_mode = True
            return

        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(
                self.config.model_name,
                device=self.config.device,
                cache_folder=self.config.cache_dir
            )
            # Apply seq length max if supported
            if hasattr(self._model, "max_seq_length"):
                self._model.max_seq_length = self.config.max_seq_length
        except ImportError:
            logger.warning("sentence-transformers not installed. Falling back to TF-IDF hashing.")
            self._fallback_mode = True
        except Exception as e:
            logger.error(f"Failed to load sentence-transformers model: {e}")
            self._fallback_mode = True

    def _fallback_embed(self, text: str) -> List[float]:
        """A simple TF-IDF inspired hashing embedding for dependency-free fallback."""
        tokens = re.findall(r'\w+', text.lower())
        vec = [0.0] * self._fallback_dim
        if not tokens:
            return vec
        
        for t in tokens:
            idx = hash(t) % self._fallback_dim
            vec[idx] += 1.0

        # Term frequency log smoothing
        for i in range(self._fallback_dim):
            if vec[i] > 0:
                vec[i] = math.log(vec[i] + 1)
                
        if self.config.normalize:
            norm = math.sqrt(sum(v * v for v in vec))
            if norm > 0:
                vec = [v / norm for v in vec]
        return vec

    def embed_text(self, text: str) -> List[float]:
        self._load_model()

        if self._fallback_mode:
            return self._fallback_embed(text)
        
        vecs = self._model.encode(
            [text],
            batch_size=1,
            normalize_embeddings=self.config.normalize,
            show_progress_bar=False
        )
        return vecs[0].tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        self._load_model()

        if self._fallback_mode:
            return [self._fallback_embed(t) for t in texts]
        
        vecs = self._model.encode(
            texts,
            batch_size=self.config.batch_size,
            normalize_embeddings=self.config.normalize,
            show_progress_bar=False
        )
        return [v.tolist() for v in vecs]

    def embed_document(self, doc_id: str, text: str) -> EmbeddingResult:
        vector = self.embed_text(text)
        
        model_name = "fallback-tfidf-hash" if self._fallback_mode else self.config.model_name
        
        return EmbeddingResult(
            doc_id=doc_id,
            vector=vector,
            model_name=model_name,
            dimension=len(vector),
            computed_at=datetime.now(timezone.utc)
        )

    def similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        if len(vec_a) != len(vec_b):
            raise EmbedderException(f"Vector dimensions mismatch: {len(vec_a)} != {len(vec_b)}")
        
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return dot_product / (norm_a * norm_b)

    @property
    def dimension(self) -> int:
        if self._fallback_mode:
            return self._fallback_dim
        if self._model is not None:
            return self._model.get_sentence_embedding_dimension()
        
        # Default assumption before loading if sentence_transformers handles dimension retrieval
        # Alternatively, we could just load the model.
        self._load_model()
        if self._fallback_mode:
            return self._fallback_dim
        return self._model.get_sentence_embedding_dimension()
