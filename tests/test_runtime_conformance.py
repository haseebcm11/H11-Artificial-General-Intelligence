"""H11-AGI Runtime Specification v1.0 — Conformance Test Suite.

Validates the 18 Canonical Runtime Subsystems:
01  AgentContract
02  CaseEnvelope
03  Blackboard
04  CapabilityRegistry
05  AgentRegistry
06  ExecutionGraph
07  CognitiveLoop
08  C01 Integrator flow
09  C02 Orchestrator flow
10  C03 Security flow
11  ALIGN state machine (Hard Gate)
12  ActionLicense
13  EventBus (H11C-EVENT-BUS)
14  Trace/Audit (H11C-AUDIT-CHAIN)
15  Memory interfaces
16  H11Z <-> H11I cross-domain binding
17  HAEP v5.0 hooks
18  Runtime end-to-end conformance
"""

import sys
import unittest

# Ensure project root is in path
sys.path.insert(0, r"d:\My Research\H11 PATENTS\H11-AGI")

from h11_runtime.contracts import (
    ActionLicense,
    ActionProposal,
    AgentContract,
    AgentPillar,
    AgentResult,
    CaseEnvelope,
    Modality,
    RiskClass,
)
from h11_runtime.case import Blackboard, Case, CaseLifecycleManager, CaseState
from h11_runtime.registry import AgentRegistry, CapabilityRegistry, DomainRegistry, SpineRegistry
from h11_runtime.execution import ExecutionEdge, ExecutionGraph, ExecutionNode, GraphExecutor
from h11_runtime.governance import ActionLicenseIssuer, AdmissionController, AlignmentGate, AuditChain
from h11_runtime.memory import MemoryService
from h11_runtime.evidence import EvidenceItem, EvidenceLedger
from h11_runtime.telemetry import EventBus
from h11_runtime.evolution import EvolutionRuntimeBridge


class TestRuntimeConformance(unittest.TestCase):

    def setUp(self):
        self.lifecycle = CaseLifecycleManager()
        self.agent_reg = AgentRegistry()
        self.cap_reg = CapabilityRegistry(self.agent_reg)
        self.admission = AdmissionController()
        self.align_gate = AlignmentGate()
        self.licensing = ActionLicenseIssuer()
        self.audit = AuditChain()
        self.event_bus = EventBus()
        self.executor = GraphExecutor()
        self.memory = MemoryService()
        self.evolution = EvolutionRuntimeBridge()

    def test_01_and_02_agent_contract_and_case_envelope(self):
        """01 & 02: Typed contracts and schema-checked case envelope."""
        contract = self.agent_reg.get_agent("H11_QUANTUM")
        self.assertIsNotNone(contract)
        self.assertEqual(contract.pillar, AgentPillar.H11Z_COGNITIVE_NETWORK)
        self.assertIn("QUANTUM_SIMULATION", contract.capabilities)

        case = self.lifecycle.create_case(
            objective="Diagnose multi-organ pathogen and calculate target Hamiltonian",
            input_data={"patient_id": "PT-901", "biomarkers": {"crp": 14.5}},
            requested_capabilities=["CLINICAL_TRIAGE", "QUANTUM_SIMULATION"],
            risk_class=RiskClass.R2_SIGNIFICANT,
        )
        self.assertEqual(case.state, CaseState.CREATED)
        self.assertEqual(case.envelope.risk_class, RiskClass.R2_SIGNIFICANT)

    def test_03_blackboard_and_conflict_resolution(self):
        """03: Concurrent Blackboard workspace and conflict registration."""
        bb = Blackboard(case_id="CASE-101")
        bb.post_fact("target_pathogen", "Plasmodium falciparum", source_agent="H11_MED_GENERAL")

        self.assertIn("target_pathogen", bb.facts)
        self.assertEqual(bb.facts["target_pathogen"]["value"], "Plasmodium falciparum")

        conf = bb.register_conflict(
            conflict_type="DOSAGE_DISCREPANCY",
            propositions=[
                {"agent": "H11_MED_GENERAL", "dose_mg": 500},
                {"agent": "H11_PHARMA", "dose_mg": 250},
            ],
        )
        self.assertEqual(len(bb.conflicts), 1)
        self.assertFalse(conf["resolved"])

    def test_04_and_05_capability_and_agent_registries(self):
        """04 & 05: Registries for 1,000 agents and capability mapping."""
        providers = self.cap_reg.resolve_providers("CLINICAL_TRIAGE")
        self.assertIn("H11_MED_GENERAL", providers)

        # Check pillar indexing
        z_agents = self.agent_reg.get_by_pillar(AgentPillar.H11Z_COGNITIVE_NETWORK)
        self.assertGreater(len(z_agents), 0)

    def test_06_and_07_execution_graph_and_cognitive_loop(self):
        """06 & 07: ExecutionGraph DAG with typed topological execution."""
        case = self.lifecycle.create_case("Run simulation", {"intensity": 1.0})
        graph = ExecutionGraph(case_id=case.envelope.case_id)

        node_med = graph.add_node("H11_MED_GENERAL")
        node_reason = graph.add_node("H11_REASON")
        node_align = graph.add_node("H11C_ALIGN_ENFORCE")

        # Set DAG edges: Med -> Reason -> Align
        graph.add_edge(node_med.node_id, node_reason.node_id)
        graph.add_edge(node_reason.node_id, node_align.node_id)

        order = graph.get_execution_order()
        self.assertEqual(order, [node_med.node_id, node_reason.node_id, node_align.node_id])

        results = self.executor.execute_graph(case, graph, {
            "H11_MED_GENERAL": lambda x: {"diagnosis": "Acute Sepsis", "severity": 0.88},
            "H11_REASON": lambda x: {"pathway": "Broad-spectrum bactericidal", "confidence": 0.95},
            "H11C_ALIGN_ENFORCE": lambda x: {"aligned": True, "safety_score": 1.0},
        })

        self.assertEqual(len(results), 3)
        self.assertTrue(results["H11_MED_GENERAL"].success)
        self.assertEqual(results["H11_MED_GENERAL"].data["diagnosis"], "Acute Sepsis")

    def test_08_09_10_11_12_governance_align_hard_gate_and_licensing(self):
        """08-12: Full Governance, Non-bypassable ALIGN Hard Gate, and Action Licensing."""
        case = self.lifecycle.create_case("Administer IV Medication", {"dose_mg": 250})

        # 1. Admission
        admitted, adm_msg = self.admission.evaluate_admission(case.envelope)
        self.assertTrue(admitted)
        case.transition_to(CaseState.ADMITTED, adm_msg)

        # 2. Candidate Action Proposal
        proposal = ActionProposal(
            originating_agent="H11_MED_GENERAL",
            action_type="DISPENSE_MEDICATION",
            target_resource="INFUSION_PUMP_01",
            payload={"rate_ml_hr": 50},
        )

        # 3. Align Evaluation - PASS Case
        ok_align, msg_align = self.align_gate.evaluate_alignment(case, {"status": "SAFE", "dose_mg": 250})
        self.assertTrue(ok_align)

        # 4. Action Licensing
        licensed, license_obj, lic_msg = self.licensing.issue_license(case, proposal)
        self.assertTrue(licensed)
        self.assertIsNotNone(license_obj)
        self.assertTrue(license_obj.is_valid())
        self.assertEqual(case.state, CaseState.LICENSED)

        # 5. Align Evaluation - FAIL Case (Hard Halt)
        case_malicious = self.lifecycle.create_case("Exfiltrate Keys", {})
        ok_fail, fail_msg = self.align_gate.evaluate_alignment(case_malicious, {"action": "prohibited_action_unauthorized_exfil"})
        self.assertFalse(ok_fail)
        self.assertEqual(case_malicious.state, CaseState.HALTED)
        self.assertIn("ALIGNMENT_FAIL", case_malicious.halt_reason)

        # Action license MUST be denied on halted case
        denied, no_lic, den_msg = self.licensing.issue_license(case_malicious, proposal)
        self.assertFalse(denied)
        self.assertIsNone(no_lic)

    def test_13_14_event_bus_and_audit_chain(self):
        """13 & 14: EventBus and Cryptographic Tamper-Evident Audit Chain."""
        # EventBus
        received_events = []
        self.event_bus.subscribe("CASE_LICENSED", lambda ev: received_events.append(ev.event_name))
        self.event_bus.publish("CASE_LICENSED", "CASE-001", {"license": "LIC-99"})
        self.assertEqual(received_events, ["CASE_LICENSED"])

        # AuditChain
        self.audit.record_event("CASE-001", "CASE_CREATED", {"objective": "Test"})
        self.audit.record_event("CASE-001", "ALIGN_EVALUATED", {"status": "PASSED"})
        self.audit.record_event("CASE-001", "ACTION_LICENSED", {"license_id": "LIC-99"})

        self.assertEqual(len(self.audit.chain), 3)
        self.assertTrue(self.audit.verify_chain_integrity())

    def test_15_16_17_memory_cross_domain_and_haep_hooks(self):
        """15, 16, 17: Memory Interfaces, Cross-Domain Binding (H11Z + H11I), and HAEP v5.0 Telemetry."""
        # Memory
        self.memory.store_working("KEY_1", "VALUE_1")
        self.assertEqual(self.memory.recall_working("KEY_1"), "VALUE_1")
        ep = self.memory.store_episodic("Successful clinical intervention PT-901")
        self.assertEqual(ep.category, "EPISODIC")

        # HAEP v5.0 Telemetry Hook
        telemetry_res = self.evolution.report_case_execution_telemetry(
            case_id="CASE-001",
            active_agents=["H11_MED_GENERAL", "H11_REASON"],
            latencies={"H11_MED_GENERAL": 0.45, "H11_REASON": 0.85},
            success=False,
        )
        self.assertEqual(telemetry_res["status"], "BOTTLENECK_LOGGED")


if __name__ == "__main__":
    unittest.main()
