"""Tests for H11-SEARCH: Sovereign Internet Knowledge Acquisition Engine.

Validates: crawler, parser, indexer, embedder, vector_store, ranker,
query_engine, knowledge_graph, cache, api, rar.
"""
from __future__ import annotations

import asyncio
import unittest
from datetime import datetime


class TestHTMLParser(unittest.TestCase):
    """Test HTML → clean text extraction."""

    def setUp(self) -> None:
        from h11_runtime.search.parser import HTMLParser
        self.parser = HTMLParser()

    def test_parse_basic_html(self) -> None:
        html = """<html><head><title>Test Page</title></head>
        <body><h1>Hello World</h1><p>This is a test paragraph.</p></body></html>"""
        doc = self.parser.parse(html, "https://example.com/test")
        self.assertEqual(doc.title, "Test Page")
        self.assertIn("Hello World", doc.text)
        self.assertIn("test paragraph", doc.text)
        self.assertEqual(doc.url, "https://example.com/test")
        self.assertGreater(doc.word_count, 0)

    def test_parse_strips_scripts_and_styles(self) -> None:
        html = """<html><body>
        <script>alert('evil');</script>
        <style>.hidden { display: none; }</style>
        <p>Clean content here.</p>
        </body></html>"""
        doc = self.parser.parse(html, "https://example.com")
        self.assertNotIn("alert", doc.text)
        self.assertNotIn("display", doc.text)
        self.assertIn("Clean content", doc.text)

    def test_parse_extracts_headings(self) -> None:
        html = """<html><body>
        <h1>Main Title</h1><h2>Subtitle</h2><h3>Section</h3>
        </body></html>"""
        doc = self.parser.parse(html, "https://example.com")
        heading_texts = [h[1] for h in doc.headings]
        self.assertIn("Main Title", heading_texts)

    def test_parse_empty_html(self) -> None:
        doc = self.parser.parse("", "https://example.com")
        self.assertEqual(doc.url, "https://example.com")


class TestIndexer(unittest.TestCase):
    """Test BM25 inverted index engine."""

    def setUp(self) -> None:
        from h11_runtime.search.indexer import InvertedIndex
        self.index = InvertedIndex()

    def test_add_and_search(self) -> None:
        self.index.add_document("doc1", "https://example.com/1", "Quantum Computing",
                                "Quantum computing uses qubits and superposition for parallel computation.")
        self.index.add_document("doc2", "https://example.com/2", "Classical Computing",
                                "Classical computers use transistors and binary logic gates.")
        results = self.index.search("quantum qubits", top_k=5)
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].doc_id, "doc1")

    def test_empty_search(self) -> None:
        results = self.index.search("nonexistent term xyz123")
        self.assertEqual(len(results), 0)

    def test_remove_document(self) -> None:
        self.index.add_document("doc1", "https://example.com", "Test", "hello world test")
        self.index.remove_document("doc1")
        results = self.index.search("hello world")
        self.assertEqual(len(results), 0)

    def test_index_stats(self) -> None:
        self.index.add_document("doc1", "https://example.com", "Test", "the quick brown fox")
        stats = self.index.stats
        self.assertEqual(stats["num_docs"], 1)


class TestEmbedder(unittest.TestCase):
    """Test vector embedding pipeline (uses TF-IDF fallback)."""

    def setUp(self) -> None:
        from h11_runtime.search.embedder import TextEmbedder, EmbeddingConfig
        self.embedder = TextEmbedder(EmbeddingConfig(model_name="tfidf-fallback"))

    def test_embed_text_returns_vector(self) -> None:
        vec = self.embedder.embed_text("quantum computing is fascinating")
        self.assertIsInstance(vec, list)
        self.assertGreater(len(vec), 0)

    def test_embed_batch(self) -> None:
        vecs = self.embedder.embed_batch(["hello world", "quantum physics", "deep learning"])
        self.assertEqual(len(vecs), 3)

    def test_similarity(self) -> None:
        vec_a = self.embedder.embed_text("quantum computing")
        vec_b = self.embedder.embed_text("quantum computing")
        sim = self.embedder.similarity(vec_a, vec_b)
        self.assertGreaterEqual(sim, 0.99)  # Same text → near-perfect similarity


class TestVectorStore(unittest.TestCase):
    """Test approximate nearest neighbor search."""

    def setUp(self) -> None:
        from h11_runtime.search.vector_store import VectorStore, VectorStoreConfig
        self.store = VectorStore(VectorStoreConfig(dimension=4))

    def test_add_and_search(self) -> None:
        self.store.add("doc1", [1.0, 0.0, 0.0, 0.0])
        self.store.add("doc2", [0.0, 1.0, 0.0, 0.0])
        self.store.add("doc3", [0.9, 0.1, 0.0, 0.0])
        results = self.store.search([1.0, 0.0, 0.0, 0.0], top_k=2)
        self.assertGreater(len(results), 0)
        # doc1 should be most similar
        self.assertEqual(results[0].doc_id, "doc1")

    def test_delete(self) -> None:
        self.store.add("doc1", [1.0, 0.0, 0.0, 0.0])
        deleted = self.store.delete("doc1")
        self.assertTrue(deleted)
        self.assertEqual(self.store.size, 0)

    def test_size(self) -> None:
        self.store.add("a", [1.0, 0.0, 0.0, 0.0])
        self.store.add("b", [0.0, 1.0, 0.0, 0.0])
        self.assertEqual(self.store.size, 2)


class TestQueryEngine(unittest.TestCase):
    """Test query decomposition and domain classification."""

    def setUp(self) -> None:
        from h11_runtime.search.query_engine import QueryDecomposer
        self.decomposer = QueryDecomposer()

    def test_decompose_simple_query(self) -> None:
        plan = self.decomposer.decompose("What is quantum entanglement?")
        self.assertIsNotNone(plan)
        self.assertEqual(plan.original_query, "What is quantum entanglement?")
        self.assertGreater(len(plan.sub_queries), 0)

    def test_classify_medical_domain(self) -> None:
        domains = self.decomposer.classify_domain("What causes diabetes mellitus?")
        self.assertTrue(any("D01" in d for d in domains))

    def test_classify_physics_domain(self) -> None:
        domains = self.decomposer.classify_domain("Explain quantum superposition in physics")
        self.assertTrue(any("D08" in d for d in domains))

    def test_expand_query(self) -> None:
        variations = self.decomposer.expand_query("machine learning algorithms")
        self.assertGreater(len(variations), 1)


class TestKnowledgeGraph(unittest.TestCase):
    """Test entity and relation extraction."""

    def setUp(self) -> None:
        from h11_runtime.search.knowledge_graph import KnowledgeGraph, Entity
        self.kg = KnowledgeGraph()

    def test_add_entity(self) -> None:
        from h11_runtime.search.knowledge_graph import Entity
        e = Entity(id="e1", name="Aspirin", entity_type="DRUG",
                   aliases=["ASA"], properties={}, confidence=0.95)
        self.kg.add_entity(e)
        found = self.kg.get_entity("e1")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Aspirin")

    def test_extract_entities_from_text(self) -> None:
        entities = self.kg.extract_entities(
            "Dr. John Smith at Harvard University discovered a new treatment for cancer."
        )
        self.assertGreater(len(entities), 0)

    def test_stats(self) -> None:
        from h11_runtime.search.knowledge_graph import Entity
        self.kg.add_entity(Entity(id="e1", name="Test", entity_type="MISC",
                                  aliases=[], properties={}, confidence=1.0))
        stats = self.kg.stats
        self.assertEqual(stats["num_entities"], 1)


class TestCache(unittest.TestCase):
    """Test search result caching."""

    def setUp(self) -> None:
        from h11_runtime.search.cache import SearchCache
        self.cache = SearchCache()

    def test_put_and_get(self) -> None:
        self.cache.put("key1", {"result": "test"})
        val = self.cache.get("key1")
        self.assertIsNotNone(val)
        self.assertEqual(val["result"], "test")

    def test_get_missing(self) -> None:
        val = self.cache.get("nonexistent")
        self.assertIsNone(val)

    def test_invalidate(self) -> None:
        self.cache.put("key1", "value1")
        removed = self.cache.invalidate("key1")
        self.assertTrue(removed)
        self.assertIsNone(self.cache.get("key1"))

    def test_stats(self) -> None:
        self.cache.put("k", "v")
        self.cache.get("k")  # hit
        self.cache.get("missing")  # miss
        stats = self.cache.stats
        self.assertEqual(stats["hit_count"], 1)
        self.assertEqual(stats["miss_count"], 1)


class TestHybridRanker(unittest.TestCase):
    """Test hybrid BM25 + semantic ranking."""

    def test_reciprocal_rank_fusion(self) -> None:
        from h11_runtime.search.ranker import HybridRanker
        rrf = HybridRanker.reciprocal_rank_fusion
        # Two ranked lists
        fused = rrf(["a", "b", "c"], ["b", "c", "a"], k=60)
        self.assertGreater(len(fused), 0)
        # 'b' appears in position 2 and 1, should rank highly
        ids = [doc_id for doc_id, _ in fused]
        self.assertIn("b", ids)


class TestSearchIntegration(unittest.TestCase):
    """Test SearchService initialization."""

    def test_search_service_creates(self) -> None:
        from h11_runtime.search.api import SearchService
        svc = SearchService()
        self.assertIsNotNone(svc)

    def test_search_service_stats(self) -> None:
        from h11_runtime.search.api import SearchService
        svc = SearchService()
        stats = svc.get_stats()
        self.assertIsInstance(stats, dict)


class TestRAR(unittest.TestCase):
    """Test Retrieval-Augmented Reasoning connector."""

    def test_rar_creates(self) -> None:
        from h11_runtime.search.api import SearchService
        from h11_runtime.search.rar import RetrievalAugmentedReasoner
        svc = SearchService()
        rar = RetrievalAugmentedReasoner(svc)
        self.assertIsNotNone(rar)

    def test_compute_evidence_score_empty(self) -> None:
        from h11_runtime.search.api import SearchService
        from h11_runtime.search.rar import RetrievalAugmentedReasoner
        rar = RetrievalAugmentedReasoner(SearchService())
        score = rar.compute_evidence_score([])
        self.assertEqual(score, 0.0)


if __name__ == "__main__":
    unittest.main()
