"""Comprehensive test suite for H11-LSE v3.0: Ultra-Omniscient Search Engine.

Validates:
1. Autonomous Swarm Crawler & UCB1 Multi-Armed Bandit Scheduling
2. Product Quantization (IVF-PQ) & HNSW Multi-Layer Vector Engine
3. Hierarchical Graph-RAG, TransE Link Prediction & Causal Do-Calculus
4. 12-Language Cross-Lingual Concept Harmonization
5. Reflexion Search Loop, Tree-of-Thought & Uncertainty Quantification
6. Real-Time Stream Ingestion & Burst Velocity Anomaly Detector
7. Merkle Tree Content Provenance Ledger & Inclusion Proofs
8. End-to-End OmniSearchEngine Unified Pipeline
"""
from __future__ import annotations

import asyncio
import time
import unittest

from h11_runtime.search import (
    AutonomousSwarmCrawler,
    BurstAnomaly,
    BurstVelocityDetector,
    CrossLingualHarmonizer,
    DroneRole,
    Entity,
    HierarchicalGraphRAG,
    KnowledgeGraph,
    MerkleInclusionProof,
    MerkleProvenanceTree,
    OmniSearchEngine,
    ProductQuantizer,
    QuantizedHNSWEngine,
    ReflexionSearchLoop,
    Relation,
    RingBufferStream,
    StreamEvent,
    SwarmCrawlTask,
    UCB1DomainFrontier,
    UniversalConcept,
    sha256_hash,
)


class TestSwarmCrawler(unittest.TestCase):
    """Test Autonomous Swarm Crawler & UCB1 Bandit Frontier."""

    def test_ucb1_frontier_prioritization(self) -> None:
        frontier = UCB1DomainFrontier()
        frontier.add_task(SwarmCrawlTask(url="https://nature.com/paper1"))
        frontier.add_task(SwarmCrawlTask(url="https://arxiv.org/abs/2401"))
        frontier.add_task(SwarmCrawlTask(url="https://randomblog.com/p1"))

        # First visit: unvisited domains explored first
        task1 = frontier.select_next_task()
        self.assertIsNotNone(task1)
        frontier.record_feedback(task1.domain, reward=0.95)

        task2 = frontier.select_next_task()
        self.assertIsNotNone(task2)
        frontier.record_feedback(task2.domain, reward=0.90)

        task3 = frontier.select_next_task()
        self.assertIsNotNone(task3)
        frontier.record_feedback(task3.domain, reward=0.10)

        # Add more tasks to each domain
        frontier.add_task(SwarmCrawlTask(url="https://nature.com/paper2"))
        frontier.add_task(SwarmCrawlTask(url="https://randomblog.com/p2"))

        # Nature has much higher mean reward -> should be selected over randomblog
        next_task = frontier.select_next_task()
        self.assertEqual(next_task.domain, "nature.com")


class TestQuantizedVectorEngine(unittest.TestCase):
    """Test Product Quantization (IVF-PQ), ADC distance tables, and HNSW graph."""

    def setUp(self) -> None:
        self.dim = 32
        self.pq = ProductQuantizer(vector_dim=self.dim, num_subvectors=4)
        self.engine = QuantizedHNSWEngine(vector_dim=self.dim, M=4)

    def test_pq_encode_and_adc_table(self) -> None:
        vec = [0.1 * i for i in range(self.dim)]
        codes = self.pq.encode(vec)
        self.assertEqual(len(codes), 4)  # 4 bytes for 4 subvectors

        adc_table = self.pq.compute_adc_table(vec)
        self.assertEqual(len(adc_table), 4)
        self.assertEqual(len(adc_table[0]), 256)

        sim = self.pq.adc_similarity(adc_table, codes)
        self.assertIsInstance(sim, float)

    def test_hnsw_quantized_graph_search(self) -> None:
        for i in range(20):
            vec = [0.05 * (i + j) for j in range(self.dim)]
            self.engine.add(f"doc_{i}", vec, metadata={"idx": i})

        self.assertEqual(self.engine.size, 20)

        query = [0.05 * j for j in range(self.dim)]
        hits_adc = self.engine.search_quantized(query, top_k=3)
        hits_hnsw = self.engine.search_hnsw(query, top_k=3)

        self.assertEqual(len(hits_adc), 3)
        self.assertEqual(len(hits_hnsw), 3)
        self.assertEqual(hits_adc[0][0], "doc_0")


class TestHierarchicalGraphRAG(unittest.TestCase):
    """Test community clustering, TransE link prediction, and Causal Do-Calculus."""

    def setUp(self) -> None:
        self.kg = KnowledgeGraph()
        self.kg.add_entity(Entity(id="e1", name="Artemisinin", entity_type="DRUG"))
        self.kg.add_entity(Entity(id="e2", name="Plasmodium", entity_type="PARASITE"))
        self.kg.add_entity(Entity(id="e3", name="Malaria", entity_type="DISEASE"))
        self.kg.add_entity(Entity(id="e4", name="Hemoglobin", entity_type="PROTEIN"))

        self.kg.add_relation(Relation(id="r1", subject_id="e1", predicate="TREATS", object_id="e3", confidence=0.98))
        self.kg.add_relation(Relation(id="r2", subject_id="e2", predicate="CAUSES", object_id="e3", confidence=0.95))
        self.kg.add_relation(Relation(id="r3", subject_id="e2", predicate="DESTROYS", object_id="e4", confidence=0.90))

        self.graph_rag = HierarchicalGraphRAG(self.kg, embedding_dim=16)

    def test_community_detection(self) -> None:
        clusters = self.graph_rag.detect_communities()
        self.assertGreater(len(clusters), 0)
        self.assertIn("Community Cluster", clusters[0].summary)

    def test_transe_hypothesis_generation(self) -> None:
        hypotheses = self.graph_rag.predict_novel_hypotheses(top_k=3)
        self.assertIsInstance(hypotheses, list)

    def test_causal_do_calculus(self) -> None:
        causal = self.graph_rag.evaluate_causal_intervention(treatment="Artemisinin", outcome="Malaria")
        self.assertIsNotNone(causal)
        self.assertGreater(causal.causal_effect_score, 0.5)
        self.assertIn("P(Malaria | do(Artemisinin))", causal.governing_chain)


class TestCrossLingualHarmonizer(unittest.TestCase):
    """Test 12-language detection and universal concept harmonization."""

    def setUp(self) -> None:
        self.harmonizer = CrossLingualHarmonizer()

    def test_language_detection(self) -> None:
        self.assertEqual(self.harmonizer.detect_language("Quantum computing algorithms"), "en")
        self.assertEqual(self.harmonizer.detect_language("量子计算神经网络"), "zh")
        self.assertEqual(self.harmonizer.detect_language("Квантовые вычисления и малярия"), "ru")
        self.assertEqual(self.harmonizer.detect_language("क्वांटम कंप्यूटिंग"), "hi")

    def test_universal_concept_linking(self) -> None:
        concepts_en = self.harmonizer.link_concepts("New treatments for malaria infection.")
        concepts_zh = self.harmonizer.link_concepts("关于疟疾和青蒿素的研究")

        ids_en = [c.concept_id for c in concepts_en]
        ids_zh = [c.concept_id for c in concepts_zh]

        self.assertIn("CUI_MALARIA", ids_en)
        self.assertIn("CUI_MALARIA", ids_zh)
        self.assertIn("CUI_ARTEMISININ", ids_zh)

    def test_multilingual_query_expansion(self) -> None:
        expansions = self.harmonizer.expand_query_multilingual("malaria artemisinin", target_languages=["zh", "de", "fr"])
        self.assertIn("zh", expansions)
        self.assertIn("青蒿素", expansions["zh"])


class TestReflexionSearchLoop(unittest.TestCase):
    """Test Tree-of-Thought planning and uncertainty estimation."""

    def setUp(self) -> None:
        self.loop = ReflexionSearchLoop()

    def test_tree_of_thought_planning(self) -> None:
        root = self.loop.plan_tree_of_thoughts("Superconducting qubit coherence times")
        self.assertEqual(root.thought_id, "T0")
        self.assertEqual(len(root.children), 3)

    def test_uncertainty_estimation(self) -> None:
        # Full coverage docs
        docs_full = [
            {"title": "Quantum qubit coherence times", "snippet": "Detailed superconducting analysis", "source": "arxiv", "score": 0.9},
            {"title": "Superconducting qubit coherence limits", "snippet": "Empirical data", "source": "nature", "score": 0.85},
            {"title": "Superconducting quantum coherence", "snippet": "Overview", "source": "ieee", "score": 0.88},
        ]
        unc_low = self.loop.estimate_uncertainty("quantum qubit coherence", docs_full)
        self.assertFalse(unc_low.has_information_gap)
        self.assertLess(unc_low.epistemic_uncertainty, 0.40)

        # Incomplete docs
        unc_high = self.loop.estimate_uncertainty("quantum qubit coherence", [])
        self.assertTrue(unc_high.has_information_gap)
        self.assertEqual(unc_high.epistemic_uncertainty, 1.0)


class TestStreamIngestAndBurstDetector(unittest.TestCase):
    """Test streaming ring buffer and burst anomaly detection."""

    def test_ring_buffer_operations(self) -> None:
        buffer = RingBufferStream(capacity=5)
        for i in range(8):
            buffer.push(StreamEvent(event_id=f"e{i}", source_feed="test", title=f"Event {i}", content="", url=""))

        self.assertEqual(buffer.size, 5)
        recent = buffer.get_recent(3)
        self.assertEqual(len(recent), 3)
        self.assertEqual(recent[0].event_id, "e7")

    def test_burst_velocity_anomaly_detection(self) -> None:
        detector = BurstVelocityDetector(window_seconds=60.0, z_threshold=2.0)
        # Establish baseline
        now = time.time()
        for i in range(10):
            ev = StreamEvent(event_id=f"b_{i}", source_feed="news", title="standard background market news", content="", url="", timestamp=now + i * 2)
            detector.ingest_event(ev)

        # Sudden surge of "superconductor"
        anomalies: List[BurstAnomaly] = []
        for i in range(5):
            ev = StreamEvent(event_id=f"surge_{i}", source_feed="news", title="breakthrough room temperature superconductor discovery announced", content="", url="", timestamp=now + 30 + i * 0.1)
            anom = detector.ingest_event(ev)
            anomalies.extend(anom)

        terms = [a.term for a in anomalies]
        self.assertTrue(any("superconductor" in t for t in terms))


class TestMerkleProvenanceLedger(unittest.TestCase):
    """Test Merkle Tree proof generation and cryptographic verification."""

    def test_merkle_tree_and_proof_verification(self) -> None:
        tree = MerkleProvenanceTree()
        tree.add_leaf("Artemether-Lumefantrine achieves 98% cure rate.", "https://who.int/malaria")
        tree.add_leaf("Plasmodium falciparum genome contains 5,300 genes.", "https://nature.com/genomics")
        tree.add_leaf("Quantum phase estimation error scales as O(1/2^t).", "https://arxiv.org/abs/2401")
        tree.add_leaf("Superconductivity observed at ambient pressures.", "https://science.org/physics")

        root = tree.build_tree()
        self.assertIsNotNone(root)
        self.assertEqual(len(root), 64)  # 64-char SHA-256 hex string

        # Generate and verify proof for leaf 1
        proof_1 = tree.generate_proof(1)
        self.assertIsNotNone(proof_1)
        self.assertTrue(MerkleProvenanceTree.verify_proof(proof_1))

        # Tampered proof must fail verification
        tampered_proof = MerkleInclusionProof(
            leaf_hash=sha256_hash("TAMPERED_CONTENT"),
            leaf_index=proof_1.leaf_index,
            merkle_root=proof_1.merkle_root,
            audit_path=proof_1.audit_path,
            timestamp=proof_1.timestamp,
        )
        self.assertFalse(MerkleProvenanceTree.verify_proof(tampered_proof))


class TestOmniSearchEngine(unittest.IsolatedAsyncioTestCase):
    """End-to-end test of the Master OmniSearchEngine."""

    async def test_omni_search_full_pipeline(self) -> None:
        engine = OmniSearchEngine()

        # Seed local index with a document
        await engine.base_service.index_document(
            url="https://nature.com/articles/malaria-treatment",
            title="Artemisinin Combination Therapies for Falciparum Malaria",
            text="Artemisinin combination therapies represent the global gold standard for malaria treatment.",
        )

        response = await engine.omni_search("malaria artemisinin treatment", domain_hint="D01_medicine")

        # Verify unified omniscient output components
        self.assertEqual(response.query, "malaria artemisinin treatment")
        self.assertIsNotNone(response.thought_tree)
        self.assertIsNotNone(response.uncertainty)
        self.assertIn("zh", response.multilingual_expansions)
        self.assertIsNotNone(response.merkle_root)
        self.assertGreater(len(response.merkle_root), 0)
        self.assertGreaterEqual(response.total_latency_ms, 0.0)

        # Telemetry stats
        stats = engine.get_full_stats()
        self.assertIn("merkle_leaves_sealed", stats)
        self.assertIn("supported_languages", stats)


if __name__ == "__main__":
    unittest.main()
