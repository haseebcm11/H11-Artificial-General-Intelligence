"""Tests for H11-AGI Real Unified System Architecture v3.0."""

import asyncio
import unittest

from h11_runtime import (
    ActionLicense,
    ActionLicenseIssuer,
    ActionProposal,
    AdmissionController,
    AgentGraph,
    AgentRegistry,
    AlignmentGate,
    AuditChain,
    Blackboard,
    CapabilityGraph,
    CapabilityRegistry,
    Case,
    CaseEnvelope,
    CaseLifecycleManager,
    CaseState,
    CheckpointManager,
    DependencyGraph,
    DomainRegistry,
    EdgeType,
    EventBus,
    ExecutionEdge,
    ExecutionGraph,
    ExecutionNode,
    GovernanceGraph,
    H11AGI,
    H11SystemState,
    InterruptHandler,
    JoinBarrier,
    MemoryService,
    MemoryType,
    ResourceBudget,
    RiskClass,
    RuntimeEvent,
    StateGraph,
    WorkerPool,
    WorkerTask,
)


class ArchitectureV3Tests(unittest.TestCase):
    """Verifies all v3.0 core subsystems, the 6 graphs, and invariants."""

    def test_01_agent_graph_and_registry(self):
        """Test Agent Graph and registry indexing."""
        ag = AgentGraph()
        ag.register_agent(
            agent_id="H11-NEURAL-L04",
            pillar="H11Z",
            layer_or_domain="L04_neural_core",
            capabilities={"neural_inference", "matrix_multiply"},
            input_schema="TensorInput",
            output_schema="TensorOutput",
        )
        providers = ag.get_providers_for_capability("neural_inference")
        self.assertEqual(len(providers), 1)
        self.assertEqual(providers[0].agent_id, "H11-NEURAL-L04")
        self.assertEqual(providers[0].status, "AVAILABLE")

        ag.set_agent_status("H11-NEURAL-L04", "BUSY")
        self.assertEqual(ag.nodes["H11-NEURAL-L04"].status, "BUSY")

    def test_02_capability_graph_transitive_closure(self):
        """Test Capability Graph dependency closure."""
        cg = CapabilityGraph()
        cg.add_capability("synthesis", requires={"reasoning", "evidence"})
        cg.add_capability("reasoning", requires={"representation", "world_model"})
        cg.add_capability("evidence", requires={"retrieval"})
        cg.add_capability("representation")
        cg.add_capability("world_model")
        cg.add_capability("retrieval")

        closure = cg.resolve_capability_closure({"synthesis"})
        self.assertIn("synthesis", closure)
        self.assertIn("reasoning", closure)
        self.assertIn("evidence", closure)
        self.assertIn("representation", closure)
        self.assertIn("world_model", closure)
        self.assertIn("retrieval", closure)

    def test_03_dependency_graph_topological_sort_and_cycle(self):
        """Test Dependency Graph sorting and cycle detection."""
        dg = DependencyGraph()
        dg.add_dependency("NODE_C", "NODE_B")
        dg.add_dependency("NODE_B", "NODE_A")

        order = dg.topological_sort()
        self.assertEqual(order, ["NODE_A", "NODE_B", "NODE_C"])

        # Cycle test
        dg_cycle = DependencyGraph()
        dg_cycle.add_dependency("A", "B")
        dg_cycle.add_dependency("B", "C")
        dg_cycle.add_dependency("C", "A")
        with self.assertRaises(ValueError):
            dg_cycle.topological_sort()

    def test_04_execution_graph_typed_dag(self):
        """Test Execution Graph typed nodes and edges."""
        eg = ExecutionGraph()
        n1 = eg.add_node("N1", "H11-ANATOMIA", "anatomy_lookup")
        n2 = eg.add_node("N2", "H11-PARASITOLOGIA", "parasite_identification")
        edge = eg.add_edge("N1", "N2", EdgeType.DATA)

        self.assertEqual(len(eg.nodes), 2)
        self.assertEqual(len(eg.edges), 1)
        self.assertEqual(eg.get_prerequisites("N2"), ["N1"])
        self.assertEqual(eg.get_dependents("N1"), ["N2"])

    def test_05_state_graph_progression(self):
        """Test State Graph valid transitions and halt."""
        sg = StateGraph("NEW")
        self.assertTrue(sg.transition("ADMITTED", "Passed admission check"))
        self.assertTrue(sg.transition("CONTEXTUALIZED", "Context packed"))
        self.assertTrue(sg.transition("MAPPED", "Capabilities resolved"))
        self.assertTrue(sg.transition("HALTED", "Safety trigger"))
        self.assertEqual(sg.current_state, "HALTED")
        self.assertFalse(sg.transition("EXECUTING"))  # Invalid transition from HALTED

    def test_06_governance_graph_permissions(self):
        """Test Governance Graph policy authorization."""
        gg = GovernanceGraph()
        gg.register_policy(
            policy_id="POL-MEDICAL-01",
            principal="D01-DOCTOR",
            target_capability="clinical_diagnosis",
            allowed_actions={"READ", "PRESCRIBE"},
        )
        ok, reason = gg.check_permission("D01-DOCTOR", "clinical_diagnosis", "PRESCRIBE")
        self.assertTrue(ok)
        self.assertIn("POL-MEDICAL-01", reason)

        denied, err = gg.check_permission("D01-DOCTOR", "clinical_diagnosis", "EXECUTE_SURGERY")
        self.assertFalse(denied)
        self.assertIn("Permission denied", err)

    def test_07_blackboard_and_case_lifecycle(self):
        """Test Blackboard workspace, evidence, conflicts, and decisions."""
        env = CaseEnvelope(objective="Clinical diagnosis case", input_data={"symptoms": ["fever"]})
        case = Case(envelope=env)
        self.assertEqual(case.state, CaseState.NEW)

        case.blackboard.post_fact("fever", True, source_agent="H11-ANAMNESIS")
        self.assertTrue(case.blackboard.get_fact("fever"))

        case.blackboard.post_evidence(
            claim="Parasitemia observed", source="Blood Smear", confidence=0.98
        )
        self.assertEqual(len(case.blackboard.evidence), 1)

        conf = case.blackboard.register_conflict("SPECIES", [{"agent": "A", "val": "P. falciparum"}, {"agent": "B", "val": "P. vivax"}])
        self.assertFalse(conf["resolved"])

        case.blackboard.post_decision("Treat with Artemether-Lumefantrine", "Confirms P. falciparum", deciding_agent="H11C-CONSENSUS")
        self.assertEqual(len(case.blackboard.decisions), 1)

    def test_08_workers_and_synchronization(self):
        """Test WorkerPool, JoinBarrier, Checkpointing, and Interruptibility."""
        async def run_async_test():
            pool = WorkerPool(concurrency=4)
            task = WorkerTask(
                task_id="TASK-1",
                node_id="N-1",
                agent_id="H11-REASON",
                func=lambda x, y: x + y,
                args=(10, 20),
            )
            res = await pool.execute_task(task)
            self.assertEqual(res, 30)
            self.assertEqual(task.status, "COMPLETED")

            # Join Barrier
            barrier = JoinBarrier(expected_branches=2)
            self.assertFalse(barrier.arrive("Result Branch 1"))
            self.assertTrue(barrier.arrive("Result Branch 2"))
            self.assertTrue(barrier.is_complete())

            # Checkpointing
            cm = CheckpointManager()
            cm.save_checkpoint("CP-1", {"state": "EXECUTING", "step": 5})
            restored = cm.restore_checkpoint("CP-1")
            self.assertEqual(restored["step"], 5)

            # Interrupt Handler
            ih = InterruptHandler()
            self.assertFalse(ih.is_interrupted())
            ih.trigger_interrupt("Manual Stop")
            self.assertTrue(ih.is_interrupted())

        asyncio.run(run_async_test())

    def test_09_resource_budget_and_system_state(self):
        """Test ResourceBudget constraints and H11SystemState."""
        budget = ResourceBudget(max_tool_calls=5, max_agent_activations=3)
        self.assertTrue(budget.can_activate_agent())
        budget.used_agent_activations = 3
        self.assertFalse(budget.can_activate_agent())

        state = H11SystemState(system_version="3.0")
        state.agent_state["H11-ANATOMIA"] = "READY"
        self.assertEqual(state.runtime_state, "OPERATIONAL")
        self.assertEqual(state.agent_state["H11-ANATOMIA"], "READY")


if __name__ == "__main__":
    unittest.main()
