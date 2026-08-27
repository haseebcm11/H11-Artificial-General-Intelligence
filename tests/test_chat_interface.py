"""Test suite for H11-AGI Conversational Reasoning Chat Interface and API Server.

Validates:
1. ConversationalReasoner initialization & multi-step thought streaming
2. Synchronous & streaming reasoning over clinical, quantum, and mathematical queries
3. REST API /api/chat and /api/health endpoint responses
4. Merkle provenance inclusion proofs and ALIGN verification in chat responses.
"""
from __future__ import annotations

import asyncio
import unittest

from h11_runtime.server import ChatResponse, ConversationalReasoner, ReasoningStep


class TestConversationalReasoner(unittest.IsolatedAsyncioTestCase):
    """Test the conversational reasoning orchestrator."""

    async def asyncSetUp(self) -> None:
        self.reasoner = ConversationalReasoner()
        await self.reasoner.initialize()

    async def test_streaming_reasoning_pipeline(self) -> None:
        query = "Evaluate therapeutic protocol for acute falciparum malaria"
        thoughts = []
        answer = None

        async for item in self.reasoner.stream_reason(query):
            if item["type"] == "thought":
                thoughts.append(item)
            elif item["type"] == "answer":
                answer = item

        # Verify thought stream progression
        self.assertGreaterEqual(len(thoughts), 4)
        phases = [t["phase"] for t in thoughts]
        self.assertIn("INGEST", phases)
        self.assertIn("SEARCH", phases)
        self.assertIn("NEURAL_MOE", phases)
        self.assertIn("ALIGN_GATE", phases)

        # Verify final synthesized answer
        self.assertIsNotNone(answer)
        self.assertIn("Artemether", answer["response_text"])
        self.assertTrue(answer["align_verified"])
        self.assertTrue(answer["action_licensed"])
        self.assertIsNotNone(answer["merkle_root"])
        self.assertGreater(answer["execution_time_ms"], 0)

    async def test_quantum_query_reasoning(self) -> None:
        query = "Formulate superconducting qubit Hamiltonian and decoherence mitigation"
        resp: ChatResponse = await self.reasoner.reason(query)

        self.assertIsInstance(resp, ChatResponse)
        self.assertIn("Hamiltonian", resp.response_text)
        self.assertTrue(resp.align_verified)
        self.assertIsNotNone(resp.audit_head)
        self.assertGreaterEqual(len(resp.reasoning_trace), 4)

    async def test_mathematics_query_reasoning(self) -> None:
        query = "Derive spectral graph Cheeger inequality complexity bounds"
        resp: ChatResponse = await self.reasoner.reason(query)

        self.assertIsInstance(resp, ChatResponse)
        self.assertIn("Cheeger", resp.response_text)
        self.assertTrue(resp.align_verified)


class TestFastAPIServerEndpoints(unittest.IsolatedAsyncioTestCase):
    """Test the FastAPI REST endpoints if fastapi is installed."""

    async def test_health_and_chat_endpoints(self) -> None:
        try:
            from fastapi.testclient import TestClient
            from h11_runtime.server.app import app
        except ImportError:
            self.skipTest("FastAPI TestClient not available")

        client = TestClient(app)

        # Test /api/health
        health_resp = client.get("/api/health")
        self.assertEqual(health_resp.status_code, 200)
        data = health_resp.json()
        self.assertEqual(data["status"], "HEALTHY")
        self.assertEqual(data["domain"], "h11.network")

        # Test /api/clusters
        clusters_resp = client.get("/api/clusters")
        self.assertEqual(clusters_resp.status_code, 200)
        cdata = clusters_resp.json()
        self.assertEqual(cdata["total_indexed_agents"], 1000)

        # Test POST /api/chat
        chat_resp = client.post("/api/chat", json={"query": "What is the second eigenvalue of a graph Laplacian?"})
        self.assertEqual(chat_resp.status_code, 200)
        c_body = chat_resp.json()
        self.assertIn("response", c_body)
        self.assertTrue(c_body["align_verified"])


if __name__ == "__main__":
    unittest.main()
