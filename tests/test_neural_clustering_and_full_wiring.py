"""Comprehensive test suite for Advanced Neural Clustering & Full System Wiring.

Validates:
1. 1,000-Agent Discovery, Neural Feature Embeddings & 8 Cognitive Manifolds
2. Dynamic Mixture-of-Experts (MoE) Softmax Gating across diverse problem domains
3. Full System Interconnection in H11AGI:
   Case -> LSE v3.0 Knowledge -> Neural MoE Routing -> 1,000 Agents -> Blackboard
   -> ALIGN Hard Gate -> Merkle Provenance Witness -> Audit Sealing -> H11-LEARN.
"""
from __future__ import annotations

import asyncio
import os
import unittest

from h11_runtime import AGIResult, H11AGI
from h11_runtime.neural_clustering import (
    CognitiveManifoldCluster,
    NeuralAgentClusterEngine,
    NeuralRoutingDecision,
)


class TestNeuralAgentClustering(unittest.TestCase):
    """Test 1,000-agent discovery and cognitive manifold clustering."""

    def setUp(self) -> None:
        self.engine = NeuralAgentClusterEngine()

    def test_indexed_agent_count(self) -> None:
        # Verify 1,000 agents are discovered and indexed across repo
        self.assertEqual(len(self.engine.agents), 1000)
        self.assertTrue(any(meta.agent_id == "H11-ANATOMIA" for meta in self.engine.agents.values()))

    def test_cognitive_manifolds_initialized(self) -> None:
        self.assertEqual(len(self.engine.clusters), 8)
        self.assertIn("CLUST_BIOMEDICAL_HEALTH", self.engine.clusters)
        self.assertIn("CLUST_PHYSICS_QUANTUM", self.engine.clusters)
        self.assertIn("CLUST_CYBER_GOVERNANCE", self.engine.clusters)

        # Check all clusters have assigned agents and valid centroid vectors
        for cid, clust in self.engine.clusters.items():
            self.assertGreater(len(clust.agent_ids), 0, f"Cluster {cid} should not be empty")
            self.assertEqual(len(clust.centroid_vector), 128)

    def test_agent_embedding_properties(self) -> None:
        agent_meta = next(iter(self.engine.agents.values()))
        self.assertEqual(len(agent_meta.embedding), 128)
        self.assertIsNotNone(agent_meta.assigned_cluster)


class TestMoESoftmaxRouting(unittest.TestCase):
    """Test dynamic Mixture-of-Experts softmax routing across domain queries."""

    def setUp(self) -> None:
        self.engine = NeuralAgentClusterEngine()

    def test_medical_query_routing(self) -> None:
        decision = self.engine.route_query(
            query="Severe Plasmodium falciparum malaria with acute hemolytic anemia",
            retrieved_evidence=[
                {"title": "Artemether therapy guidelines", "snippet": "First-line ACT treatment for falciparum malaria."}
            ],
            top_k_agents=6,
        )
        self.assertEqual(decision.primary_cluster_id, "CLUST_BIOMEDICAL_HEALTH")
        self.assertGreater(decision.cluster_affinity, 0.20)
        self.assertEqual(len(decision.selected_agent_ids), 6)
        self.assertIn("MoE Gated", decision.rationale)

    def test_quantum_physics_routing(self) -> None:
        decision = self.engine.route_query(
            query="Superconducting qubit Hamiltonian phase estimation and coherence times",
            top_k_agents=5,
        )
        self.assertIn(decision.primary_cluster_id, ("CLUST_PHYSICS_QUANTUM", "CLUST_FORMAL_MATHEMATICS"))
        self.assertEqual(len(decision.selected_agent_ids), 5)

    def test_security_governance_routing(self) -> None:
        decision = self.engine.route_query(
            query="Zero-trust cryptographic audit chain verification and action licensing",
            top_k_agents=4,
        )
        self.assertEqual(decision.primary_cluster_id, "CLUST_CYBER_GOVERNANCE")
        self.assertEqual(len(decision.selected_agent_ids), 4)

    def test_mathematics_algorithm_routing(self) -> None:
        decision = self.engine.route_query(
            query="Graph isomorphism polynomial time complexity and spectral eigenvectors",
            top_k_agents=5,
        )
        self.assertIn(decision.primary_cluster_id, ("CLUST_FORMAL_MATHEMATICS", "CLUST_PHYSICS_QUANTUM"))


class TestFullSystemWiring(unittest.IsolatedAsyncioTestCase):
    """End-to-end test validating full-system interconnection in H11AGI."""

    async def test_full_system_cognitive_tick(self) -> None:
        # Instantiate fully connected AGI Kernel
        agi = H11AGI(
            enable_search=True,
            enable_learning=True,
            enable_neural_clustering=True,
        )
        await agi.initialize()

        # Construct a real clinical case envelope
        case_payload = {
            "patient_id": "patient-malaria-001",
            "travel_history": ["sub-saharan_africa"],
            "symptoms": ["fever", "chills", "anemia"],
            "suspected_pathogen": "Plasmodium falciparum",
            "patient_vitals": {"temp_c": 39.4, "heart_rate": 115},
            "query": "Evaluate optimal therapeutic intervention for acute falciparum malaria",
            "goal": "host_infection",
        }

        # Execute the unified 24-step cognitive loop
        result = await agi.tick(case_payload)

        # 1. Verify Admission & Identity
        self.assertTrue(result.admitted)
        self.assertIsNotNone(result.identity)

        # 2. Verify LSE v3.0 Live Knowledge Retrieval & Merkle Root
        self.assertIsNotNone(result.merkle_provenance_root)
        self.assertEqual(len(result.merkle_provenance_root), 64)

        # 3. Verify Neural MoE Agent Routing
        self.assertIsNotNone(result.neural_routing)
        self.assertEqual(result.neural_routing["manifold"], "CLUST_BIOMEDICAL_HEALTH")
        self.assertGreater(len(result.neural_routing["activated_agents"]), 0)

        # 4. Verify ALIGN Hard Gate & Action Licensing
        self.assertTrue(result.allowed)
        self.assertTrue(result.licensed)
        self.assertFalse(result.halted)

        # 5. Verify Cryptographic Audit Chain Sealing
        self.assertIsNotNone(result.audit_head)

        # 6. Verify H11-LEARN Experience Recording
        self.assertTrue(result.learning_recorded)

        # 7. Verify Unified System Telemetry
        telemetry = agi.get_system_telemetry()
        self.assertGreaterEqual(telemetry["indexed_agents_total"], 1000)
        self.assertIsNotNone(telemetry["clustering_stats"])
        self.assertIsNotNone(telemetry["omni_search_stats"])
        self.assertIsNotNone(telemetry["learn_stats"])


if __name__ == "__main__":
    unittest.main()
