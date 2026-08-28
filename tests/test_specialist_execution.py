from __future__ import annotations

import unittest
from dataclasses import dataclass

from h11_runtime.case.blackboard import Blackboard
from h11_runtime.execution.specialist import SpecialistExecutionCoordinator
from h11_runtime.graph.execution_graph import ExecutionGraph


@dataclass
class Metadata:
    agent_id: str
    relative_path: str


class SpecialistExecutionTests(unittest.IsolatedAsyncioTestCase):
    async def test_structured_quantum_agent_really_executes(self) -> None:
        routed_id = "L01_physical_substrate/H11-QUANTUM"
        metadata = {
            routed_id: Metadata(
                agent_id="H11-QUANTUM",
                relative_path="H11Z_COGNITIVE_NETWORK/L01_physical_substrate/H11-QUANTUM/agent.py",
            )
        }
        case = {
            "query": "Calculate circuit fidelity",
            "t1_time_us": 100.0,
            "t2_time_us": 80.0,
            "gate_time_ns": 20.0,
            "num_gates": 10,
            "base_gate_fidelity": 0.999,
        }
        graph = ExecutionGraph("CASE-QUANTUM")
        node = graph.add_node(routed_id)
        board = Blackboard("CASE-QUANTUM")

        records = await SpecialistExecutionCoordinator().execute(
            [routed_id], metadata, case, graph, board
        )

        self.assertEqual(records[0].status, "COMPLETED")
        self.assertGreater(records[0].output["total_circuit_fidelity"], 0.98)
        self.assertEqual(node.status, "COMPLETED")
        self.assertIn(routed_id, board.agent_results)

    async def test_missing_inputs_are_skipped_without_fabricated_output(self) -> None:
        routed_id = "L01_physical_substrate/H11-QUANTUM"
        metadata = {
            routed_id: Metadata(
                agent_id="H11-QUANTUM",
                relative_path="H11Z_COGNITIVE_NETWORK/L01_physical_substrate/H11-QUANTUM/agent.py",
            )
        }
        graph = ExecutionGraph("CASE-MISSING")
        graph.add_node(routed_id)
        records = await SpecialistExecutionCoordinator().execute(
            [routed_id], metadata, {"query": "Explain quantum systems"}, graph, Blackboard("CASE-MISSING")
        )

        self.assertEqual(records[0].status, "SKIPPED")
        self.assertIsNone(records[0].output)
        self.assertIn("t1_time_us", records[0].missing_inputs)

    async def test_nested_case_fields_are_compiled_with_provenance(self) -> None:
        routed_id = "L01_physical_substrate/H11-QUANTUM"
        metadata = {
            routed_id: Metadata(
                agent_id="H11-QUANTUM",
                relative_path="H11Z_COGNITIVE_NETWORK/L01_physical_substrate/H11-QUANTUM/agent.py",
            )
        }
        graph = ExecutionGraph("CASE-NESTED-QUANTUM")
        graph.add_node(routed_id)
        records = await SpecialistExecutionCoordinator().execute(
            [routed_id],
            metadata,
            {
                "query": "Calculate circuit fidelity from nested coherence measurements",
                "coherence_times": {"t1_us": 100.0, "t2_us": 80.0},
                "gate_time_ns": 20.0,
                "num_gates": 10,
                "base_gate_fidelity": 0.999,
            },
            graph,
            Blackboard("CASE-NESTED-QUANTUM"),
        )

        record = records[0]
        self.assertEqual(record.status, "COMPLETED")
        self.assertGreater(record.output["total_circuit_fidelity"], 0.98)
        provenance = record.contract_diagnostics["field_provenance"]
        self.assertEqual(provenance["t1_time_us"], "case.coherence_times.t1_us")
        self.assertIn("qubit_topology", record.contract_diagnostics["schema_only_fields"])

    async def test_cross_domain_alias_executes_softmax_agent(self) -> None:
        routed_id = "L05_attention_context/H11-SOFTMAX"
        metadata = {
            routed_id: Metadata(
                agent_id="H11-SOFTMAX",
                relative_path="H11Z_COGNITIVE_NETWORK/L05_attention_context/H11-SOFTMAX/agent.py",
            )
        }
        graph = ExecutionGraph("CASE-SOFTMAX")
        graph.add_node(routed_id)
        records = await SpecialistExecutionCoordinator().execute(
            [routed_id], metadata, {"scores": [1.0, 2.0, 3.0]}, graph, Blackboard("CASE-SOFTMAX")
        )

        record = records[0]
        self.assertEqual(record.status, "COMPLETED")
        self.assertAlmostEqual(sum(record.output["probabilities"]), 1.0)
        self.assertEqual(record.contract_diagnostics["field_provenance"]["logits"], "case.scores")

    async def test_invalid_contract_type_is_skipped_with_diagnostics(self) -> None:
        routed_id = "L05_attention_context/H11-SOFTMAX"
        metadata = {
            routed_id: Metadata(
                agent_id="H11-SOFTMAX",
                relative_path="H11Z_COGNITIVE_NETWORK/L05_attention_context/H11-SOFTMAX/agent.py",
            )
        }
        graph = ExecutionGraph("CASE-BAD-SOFTMAX")
        graph.add_node(routed_id)
        records = await SpecialistExecutionCoordinator().execute(
            [routed_id], metadata, {"scores": "not-a-vector"}, graph, Blackboard("CASE-BAD-SOFTMAX")
        )

        self.assertEqual(records[0].status, "SKIPPED")
        self.assertIsNone(records[0].output)
        self.assertTrue(records[0].contract_diagnostics["validation_errors"])


if __name__ == "__main__":
    unittest.main()
