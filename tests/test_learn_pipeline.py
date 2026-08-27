"""Tests for H11-LEARN: Continuous Learning Pipeline.

Validates: collector, distiller, evaluator, curriculum, governed_update.
"""
from __future__ import annotations

import unittest
from datetime import datetime


class TestDataCollector(unittest.TestCase):
    """Test training data collection."""

    def setUp(self) -> None:
        from h11_runtime.learn.collector import DataCollector, CollectionConfig
        import tempfile, os
        self.tmpdir = tempfile.mkdtemp()
        self.collector = DataCollector(CollectionConfig(storage_dir=self.tmpdir))

    def test_record_example(self) -> None:
        example_id = self.collector.record(
            agent_id="H11C-MEDICAL",
            case_id="case-001",
            query="What causes sepsis?",
            retrieved_docs=[{"url": "https://pubmed.ncbi.nlm.nih.gov/123", "title": "Sepsis Review"}],
            output={"action": "DIAGNOSE", "result": "bacterial_infection"},
            domain="D01_medicine_health",
            feedback_score=0.9,
        )
        self.assertIsNotNone(example_id)

    def test_get_examples(self) -> None:
        self.collector.record(
            agent_id="H11C-TEST", case_id="c1", query="test",
            retrieved_docs=[], output={}, domain="D11_cs",
        )
        examples = self.collector.get_examples()
        self.assertEqual(len(examples), 1)

    def test_stats(self) -> None:
        self.collector.record(
            agent_id="H11C-A", case_id="c1", query="q",
            retrieved_docs=[], output={}, domain="D01",
        )
        stats = self.collector.stats
        self.assertEqual(stats["total_examples"], 1)


class TestKnowledgeDistiller(unittest.TestCase):
    """Test knowledge distillation into agent rules."""

    def setUp(self) -> None:
        from h11_runtime.learn.distiller import KnowledgeDistiller
        self.distiller = KnowledgeDistiller()

    def test_distill_empty(self) -> None:
        rules = self.distiller.distill_from_examples([])
        self.assertEqual(len(rules), 0)

    def test_merge_rules(self) -> None:
        from h11_runtime.learn.distiller import DistilledRule
        r1 = DistilledRule(
            rule_id="r1", agent_id="A", domain="D01",
            condition="fever > 38", action="diagnose_infection",
            confidence=0.7, source_examples=["e1"],
            created_at=datetime.now(), validated=False,
        )
        r2 = DistilledRule(
            rule_id="r2", agent_id="A", domain="D01",
            condition="fever > 38", action="diagnose_infection",
            confidence=0.8, source_examples=["e2"],
            created_at=datetime.now(), validated=False,
        )
        merged = self.distiller.merge_rules([r1], [r2])
        self.assertGreater(len(merged), 0)


class TestModelEvaluator(unittest.TestCase):
    """Test benchmark evaluation."""

    def setUp(self) -> None:
        from h11_runtime.learn.evaluator import ModelEvaluator
        self.evaluator = ModelEvaluator()

    def test_evaluate_accuracy(self) -> None:
        result = self.evaluator.evaluate_accuracy(
            predictions=["cat", "dog", "bird"],
            ground_truth=["cat", "dog", "fish"],
        )
        self.assertAlmostEqual(result.score, 2 / 3, places=2)
        self.assertIsNotNone(result.benchmark_name)

    def test_evaluate_safety(self) -> None:
        result = self.evaluator.evaluate_safety([
            "This is a helpful response.",
            "Here is a safe explanation of the concept.",
        ])
        self.assertTrue(result.passed)


class TestCurriculumGenerator(unittest.TestCase):
    """Test automated curriculum generation."""

    def setUp(self) -> None:
        from h11_runtime.learn.curriculum import CurriculumGenerator
        self.generator = CurriculumGenerator()

    def test_generate_curriculum(self) -> None:
        curriculum = self.generator.generate_curriculum("D01_medicine_health", num_stages=5)
        self.assertIsNotNone(curriculum)
        self.assertGreater(len(curriculum.stages), 0)

    def test_generate_queries(self) -> None:
        curriculum = self.generator.generate_curriculum("D08_physics", num_stages=3)
        if curriculum.stages:
            queries = self.generator.generate_queries(curriculum.stages[0], count=10)
            self.assertGreater(len(queries), 0)


class TestGovernedUpdater(unittest.TestCase):
    """Test HAEP v5.0 governed model updates."""

    def setUp(self) -> None:
        from h11_runtime.learn.governed_update import GovernedUpdater
        self.updater = GovernedUpdater()

    def test_propose_update(self) -> None:
        from h11_runtime.learn.evaluator import EvaluationReport, BenchmarkResult
        report = EvaluationReport(
            model_id="test-model-v1",
            benchmarks=[
                BenchmarkResult(
                    benchmark_name="accuracy",
                    score=0.95,
                    threshold=0.9,
                    passed=True,
                    details={},
                )
            ],
            overall_pass=True,
            evaluated_at=datetime.now(),
            recommendation="PROMOTE",
        )
        proposal = self.updater.propose_update("models/test-v1", report)
        self.assertEqual(proposal.status, "PENDING")

    def test_reject_update(self) -> None:
        from h11_runtime.learn.evaluator import EvaluationReport, BenchmarkResult
        from h11_runtime.learn.governed_update import GovernedUpdater
        report = EvaluationReport(
            model_id="bad-model",
            benchmarks=[
                BenchmarkResult("accuracy", 0.3, 0.9, False, {}),
            ],
            overall_pass=False,
            evaluated_at=datetime.now(),
            recommendation="REJECT",
        )
        proposal = self.updater.propose_update("models/bad", report)
        self.updater.reject(proposal, "Failed accuracy threshold")
        self.assertEqual(proposal.status, "REJECTED")


if __name__ == "__main__":
    unittest.main()
