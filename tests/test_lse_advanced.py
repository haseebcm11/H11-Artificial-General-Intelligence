"""Comprehensive test suite for H11-LSE v2.0: Superintelligent Large Search Engine.

Validates:
1. SimHash & MinHash Deduplication & URL Canonicalization
2. Semantic Parser (LaTeX math, Markdown tables, code snippets, DOIs, freshness)
3. Sharded Index, BM25F Field Weighting & Positional Phrase Search
4. Topic-Sensitive PageRank, Domain Authority & TrustRank
5. ColBERT Token-Level Late Interaction (MaxSim) & Cross-Encoder Verification
6. Neuro-Symbolic Entity Linker & Multi-Hop Path Reasoning
7. Evidence Synthesizer & Claim Verification Matrix
8. End-to-End LSE v2.0 Unified Search Pipeline
"""
from __future__ import annotations

import asyncio
import datetime
import unittest

from h11_runtime.search import (
    CrossEncoderVerifier,
    DocumentFields,
    EvidenceSynthesizer,
    FederatedSearchEngine,
    KnowledgeGraph,
    LateInteractionEngine,
    MinHash,
    NeuroSymbolicEntityLinker,
    PageRankEngine,
    SearchConfig,
    SearchQuery,
    SearchService,
    SemanticParser,
    ShardedIndex,
    SimHash,
    SimHashIndex,
    VerificationStatus,
    WebGraph,
    canonicalize_url,
    varbyte_decode,
    varbyte_encode,
)


class TestDeduplication(unittest.TestCase):
    """Test 64-bit SimHash, MinHash LSH, and URL canonicalization."""

    def test_canonicalize_url(self) -> None:
        url_a = "https://www.nature.com/articles/s41586-024?utm_source=twitter&utm_medium=social#section2"
        url_b = "http://nature.com:80/articles/s41586-024/?utm_medium=social&utm_source=twitter"
        clean_a = canonicalize_url(url_a)
        clean_b = canonicalize_url(url_b)
        self.assertEqual(clean_a, "https://nature.com/articles/s41586-024")
        self.assertEqual(clean_b, "http://nature.com/articles/s41586-024")

    def test_simhash_identical_and_near_duplicate(self) -> None:
        text1 = "Quantum computing harnesses superposition and entanglement for computational supremacy."
        text2 = "Quantum computing harnesses superposition and entanglement for computational advantage."
        text3 = "Photosynthesis converts carbon dioxide and water into glucose using sunlight energy."

        sh1 = SimHash(text1)
        sh2 = SimHash(text2)
        sh3 = SimHash(text3)

        self.assertLessEqual(sh1.distance(sh2), 10)
        self.assertGreater(sh1.distance(sh3), 20)

    def test_simhash_index_lookup(self) -> None:
        index = SimHashIndex(k=3)
        doc1_text = "The quick brown fox jumps over the lazy dog in the sunny morning park."
        doc2_text = "The quick brown fox jumps over the lazy dog in the sunny morning park!"

        sh1 = SimHash(doc1_text)
        index.add("doc1", sh1)

        self.assertTrue(index.is_duplicate(doc2_text))
        self.assertFalse(index.is_duplicate("Completely different topic regarding financial derivatives."))

    def test_minhash_jaccard(self) -> None:
        mh = MinHash(num_perm=64)
        sig1 = mh.compute("artificial intelligence neural networks deep learning transformers")
        sig2 = mh.compute("artificial intelligence neural networks deep learning transformers algorithms")
        sig3 = mh.compute("organic gardening composting soil nutrients vegetable planting")

        sim_12 = MinHash.jaccard_similarity(sig1, sig2)
        sim_13 = MinHash.jaccard_similarity(sig1, sig3)

        self.assertGreater(sim_12, 0.70)
        self.assertLess(sim_13, 0.20)


class TestSemanticParser(unittest.TestCase):
    """Test LaTeX math, Markdown tables, code snippets, DOIs, and freshness."""

    def setUp(self) -> None:
        self.parser = SemanticParser()

    def test_extract_math_equations(self) -> None:
        text = """
        The energy-momentum relation is given by $$E^2 = (pc)^2 + (m_0 c^2)^2$$.
        In quantum mechanics, the wave equation is $\\hat{H}\\psi = E\\psi$.
        """
        equations = self.parser.extract_equations(text)
        self.assertGreaterEqual(len(equations), 2)
        self.assertTrue(any(eq.is_block for eq in equations))
        self.assertTrue(any(eq.domain_hint == "D08_physics" for eq in equations))

    def test_extract_html_tables_to_markdown(self) -> None:
        html_text = """
        <table>
            <tr><th>Metric</th><th>Score</th><th>Threshold</th></tr>
            <tr><td>Accuracy</td><td>0.98</td><td>0.90</td></tr>
            <tr><td>F1-Score</td><td>0.96</td><td>0.85</td></tr>
        </table>
        """
        tables = self.parser.extract_tables(html_text)
        self.assertEqual(len(tables), 1)
        self.assertIn("Accuracy", tables[0].markdown)
        self.assertIn("| Metric | Score | Threshold |", tables[0].markdown)

    def test_extract_code_snippets(self) -> None:
        code_text = """
        Here is the algorithm implementation:
        ```python
        def compute_loss(y_true, y_pred):
            import torch
            return torch.nn.functional.cross_entropy(y_pred, y_true)
        ```
        """
        snippets = self.parser.extract_code_snippets(code_text)
        self.assertEqual(len(snippets), 1)
        self.assertEqual(snippets[0].language, "python")
        self.assertIn("def compute_loss", snippets[0].code)

    def test_extract_academic_citations(self) -> None:
        text = "Refer to the breakthrough published at doi:10.1038/s41586-024-00123-x and arXiv:2403.12345."
        citations = self.parser.extract_citations(text)
        types = [c.citation_type for c in citations]
        self.assertIn("DOI", types)
        self.assertIn("ARXIV", types)

    def test_temporal_freshness_decay(self) -> None:
        old_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=365)
        fresh_score_news = self.parser.calculate_freshness(old_date, is_scientific=False)
        fresh_score_science = self.parser.calculate_freshness(old_date, is_scientific=True)
        # Science decays slower than news
        self.assertGreater(fresh_score_science, fresh_score_news)


class TestShardedIndex(unittest.TestCase):
    """Test multi-shard BM25F indexing and positional phrase matching."""

    def setUp(self) -> None:
        self.index = ShardedIndex(num_shards=3)
        self.index.add_document(
            DocumentFields(
                doc_id="doc-quantum-1",
                url="https://nature.com/articles/quantum-supremacy",
                title="Quantum Computing with Superconducting Qubits",
                headings="Quantum Hardware and Coherence Times",
                abstract="Superconducting circuits provide a scalable platform for quantum supremacy.",
                body="We demonstrate high fidelity two-qubit gate operations below the surface code threshold.",
            )
        )
        self.index.add_document(
            DocumentFields(
                doc_id="doc-classical-2",
                url="https://ieee.org/papers/classical-cmos",
                title="CMOS Transistor Scaling and Thermal Limits",
                headings="Silicon Fabrication and FinFET Architecture",
                abstract="Classical CMOS scaling faces fundamental thermodynamic and leakage limits.",
                body="Transistor gate delays are constrained by subthreshold slope and quantum tunneling.",
            )
        )

    def test_bm25f_field_search(self) -> None:
        results = self.index.search_bm25f("quantum qubits", top_k=5)
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0][0], "doc-quantum-1")

    def test_exact_phrase_search(self) -> None:
        # Exact phrase query: "quantum supremacy"
        matches = self.index.search_phrase("quantum supremacy", top_k=5)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "doc-quantum-1")

    def test_varbyte_compression(self) -> None:
        numbers = [1, 128, 300, 10000, 500000]
        encoded = varbyte_encode(numbers)
        decoded = varbyte_decode(encoded)
        self.assertEqual(numbers, decoded)


class TestPageRankEngine(unittest.TestCase):
    """Test PageRank, Topic-Sensitive PageRank, and Domain Authority."""

    def setUp(self) -> None:
        self.engine = PageRankEngine()
        self.graph = WebGraph()
        # Create web graph: A -> B -> C -> A, and D -> B
        self.graph.add_edge("https://nature.com/article1", "https://arxiv.org/abs/2401.001")
        self.graph.add_edge("https://arxiv.org/abs/2401.001", "https://github.com/code/repo")
        self.graph.add_edge("https://github.com/code/repo", "https://nature.com/article1")
        self.graph.add_edge("https://untrusted-blog.com/post", "https://arxiv.org/abs/2401.001")

    def test_pagerank_convergence(self) -> None:
        ranks = self.engine.compute_pagerank(self.graph)
        self.assertEqual(len(ranks), self.graph.size)
        self.assertAlmostEqual(sum(ranks.values()), 1.0, places=3)
        # arxiv.org has two inbound links, should rank highest
        self.assertGreater(ranks["https://arxiv.org/abs/2401.001"], ranks["https://untrusted-blog.com/post"])

    def test_topic_sensitive_pagerank(self) -> None:
        physics_ranks = self.engine.compute_topic_pagerank(self.graph, topic="D08_physics")
        self.assertGreater(physics_ranks["https://arxiv.org/abs/2401.001"], 0.0)

    def test_domain_authority_score(self) -> None:
        da_gov = self.engine.calculate_domain_authority("https://nih.gov/health", base_pagerank=0.05, in_degree=100)
        da_blog = self.engine.calculate_domain_authority("https://myrandomblog.com/p", base_pagerank=0.001, in_degree=2)
        self.assertGreater(da_gov, da_blog)
        self.assertGreaterEqual(da_gov, 50.0)


class TestLateInteraction(unittest.TestCase):
    """Test ColBERT MaxSim token-level late interaction and cross-encoder verifier."""

    def setUp(self) -> None:
        self.engine = LateInteractionEngine(embedding_dim=64)

    def test_maxsim_token_matching(self) -> None:
        query = "quantum error correction threshold"
        doc_relevant = "Surface codes achieve fault-tolerant quantum error correction below empirical threshold."
        doc_irrelevant = "Gardening tips for organic tomatoes and composting soil nutrients."

        ranked = self.engine.rank_documents(query, [("doc_rel", doc_relevant), ("doc_irrel", doc_irrelevant)])
        self.assertEqual(ranked[0][0], "doc_rel")
        self.assertGreater(ranked[0][1], ranked[1][1])

    def test_cross_encoder_entailment_and_contradiction(self) -> None:
        claim = "Artemether is effective for uncomplicated malaria"
        evidence_entail = "Artemether lumefantrine is highly effective for uncomplicated falciparum malaria treatment."
        evidence_contra = "Artemether is not effective and fails in malaria treatment."

        res_entail = CrossEncoderVerifier.verify_claim(claim, evidence_entail)
        res_contra = CrossEncoderVerifier.verify_claim(claim, evidence_contra)

        self.assertEqual(res_entail["status"], "ENTAILMENT")
        self.assertTrue(res_contra["is_contradiction"])


class TestNeuroSymbolicEntityLinker(unittest.TestCase):
    """Test entity linking and multi-hop graph path discovery."""

    def setUp(self) -> None:
        self.kg = KnowledgeGraph()
        from h11_runtime.search.knowledge_graph import Entity, Relation

        self.kg.add_entity(Entity(id="e_plasmodium", name="Plasmodium falciparum", entity_type="PATHOGEN"))
        self.kg.add_entity(Entity(id="e_malaria", name="Malaria", entity_type="DISEASE"))
        self.kg.add_entity(Entity(id="e_artemether", name="Artemether", entity_type="DRUG"))

        # Add relations: Plasmodium -> CAUSES -> Malaria, Artemether -> TREATS -> Malaria
        self.kg.add_relation(
            Relation(id="r1", subject_id="e_plasmodium", predicate="CAUSES", object_id="e_malaria", confidence=0.98)
        )
        self.kg.add_relation(
            Relation(id="r2", subject_id="e_artemether", predicate="TREATS", object_id="e_malaria", confidence=0.95)
        )

        self.linker = NeuroSymbolicEntityLinker(self.kg)

    def test_link_surface_mentions(self) -> None:
        text = "Patient infected with Plasmodium falciparum requires Artemether therapy."
        mentions = self.linker.link_mentions(text)
        linked_ids = [m.linked_entity_id for m in mentions if m.linked_entity_id]
        self.assertIn("e_plasmodium", linked_ids)
        self.assertIn("e_artemether", linked_ids)

    def test_find_multi_hop_path(self) -> None:
        paths = self.linker.find_multi_hop_paths("Plasmodium falciparum", "Artemether", max_hops=3)
        self.assertGreater(len(paths), 0)
        self.assertEqual(paths[0].hops, 2)
        self.assertIn("CAUSES", paths[0].description)
        self.assertIn("TREATS", paths[0].description)


class TestEvidenceSynthesizer(unittest.TestCase):
    """Test claim verification matrix and source reliability grading."""

    def setUp(self) -> None:
        self.synthesizer = EvidenceSynthesizer()

    def test_source_grading(self) -> None:
        grade_nih = self.synthesizer.assess_source("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12345", "pubmed")
        grade_nature = self.synthesizer.assess_source("https://www.nature.com/articles/s41586", "crossref")
        grade_blog = self.synthesizer.assess_source("https://techblog123.com/post", "web")

        self.assertIn(grade_nih.grade, ("A+", "A"))
        self.assertIn(grade_nature.grade, ("A+", "A"))
        self.assertEqual(grade_blog.grade, "C")

    def test_synthesize_consensus_matrix(self) -> None:
        docs = [
            {
                "url": "https://who.int/malaria/guidelines",
                "source": "official",
                "content": "Artemisinin combination therapy is the first-line treatment for uncomplicated falciparum malaria globally.",
            },
            {
                "url": "https://cdc.gov/malaria/treatment",
                "source": "official",
                "content": "Artemisinin combination therapy is the first-line treatment for uncomplicated falciparum malaria patients.",
            },
        ]
        briefing = self.synthesizer.synthesize(query="Malaria treatment guidelines", domain="D01_medicine", raw_documents=docs)
        self.assertGreater(len(briefing.claims), 0)
        self.assertEqual(briefing.consensus_level, "STRONG_CONSENSUS")
        self.assertTrue(any(c.status == VerificationStatus.VERIFIED_CONSENSUS for c in briefing.claims))
        self.assertIn("Claim Verification Matrix", briefing.evidence_matrix_markdown)


class TestLSEUnifiedPipeline(unittest.IsolatedAsyncioTestCase):
    """End-to-end test of the unified Large Search Engine (LSE v2.0) service."""

    async def test_search_and_index_pipeline(self) -> None:
        service = SearchService(
            SearchConfig(
                enable_web_search=False,
                enable_academic_federation=False,
                enable_late_interaction=True,
            )
        )

        # 1. Index document with math & tables
        doc_text = """
        Quantum algorithms utilize unitary matrix transformations.
        The phase estimation error bounds satisfy $$\\Delta \\theta \\le \\frac{2\\pi}{2^t}$$.
        <table>
            <tr><th>Qubits</th><th>Fidelity</th></tr>
            <tr><td>53</td><td>99.4%</td></tr>
        </table>
        """
        doc_id = await service.index_document(
            url="https://nature.com/articles/quantum-phase-estimation",
            title="Quantum Phase Estimation Algorithms",
            text=doc_text,
        )
        self.assertIsNotNone(doc_id)
        self.assertNotEqual(doc_id, "duplicate_skipped")

        # 2. Query the indexed document
        query = SearchQuery(text="quantum unitary matrix transformations", max_results=5)
        response = await service.search(query)

        self.assertGreater(response.total_results, 0)
        self.assertIsNotNone(response.query_plan)
        self.assertIn("D10", response.domain_classified)  # Matrix -> Math / Physics
        self.assertGreaterEqual(response.search_time_ms, 0.0)


if __name__ == "__main__":
    unittest.main()
