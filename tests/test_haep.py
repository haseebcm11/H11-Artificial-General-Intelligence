"""Unit & Integration Test Suite for H11-AGI Enhancement Protocol v5.0 (HAEP v5.0)."""

import os
import sys
import unittest

# Ensure project root is in path
sys.path.insert(0, r"d:\My Research\H11 PATENTS\H11-AGI")

from h11_runtime.haep import (
    ArchitectureDifferential,
    AuthorityLevel,
    BaselineLock,
    BottleneckRecord,
    CapabilityLandscape,
    CapabilityStatus,
    CompiledIntelligencePathway,
    DecomposedCapability,
    EmergenceClass,
    EmergenceObservatory,
    EnhancementAuthorizationToken,
    EnhancementObject,
    EnvironmentModel,
    EnvironmentState,
    EvolutionConstitution,
    EvolutionCost,
    EvolutionDebt,
    EvolutionDebtManager,
    EvolutionHealthScorecard,
    EvolutionMemoryManager,
    EvolutionOrchestrator,
    EvolutionPath,
    EvolutionState,
    GovernanceGate,
    HAEPRuntime,
    H11SelfModel,
    IntelligenceState,
    MetacognitiveMonitor,
    OptimizationDomain,
    OptimizationRegime,
    PlanningHorizon,
    PromotionLevel,
    PromotionVector,
    RecursiveLevel,
    RiskLevel,
    SelfOptimizer,
    SolutionType,
    StabilizedEmergenceRecord,
    SystemGenomeManager,
    SystemState,
    TriadFitness,
)


class TestHAEPv5Protocol(unittest.TestCase):

    def setUp(self):
        self.runtime = HAEPRuntime()

    def test_full_v5_self_optimization_cycle(self):
        """Test complete HAEP v5.0 Self-Optimization Loop with bottleneck detection, compilation, & recalibration."""
        sample_code = """
class OptimizedSuperconductingRoutingSpecialist:
    def process(self, inputs):
        return {"status": "OK", "score": 0.99, "critical_temperature_k": 93.5}
"""
        def baseline(x): return {"status": "OK", "score": 0.86}
        def candidate(x): return {"status": "OK", "score": 0.99}

        test_data = [{"qubit_id": f"QB-{i}"} for i in range(10)]

        ok, enh, new_state = self.runtime.execute_self_optimization_cycle(
            target_agent="H11_SPINTRONIC",
            problem_description="Tunnel magnetoresistance ratio degradation under thermal fluctuation",
            candidate_code=sample_code,
            baseline_fn=baseline,
            candidate_fn=candidate,
            test_cases=test_data,
            required_capability="QUANTUM_SIMULATION",
            domain=OptimizationDomain.O3_ARCHITECTURAL,
            regime=OptimizationRegime.REGIME_1_LOCAL,
            horizon=PlanningHorizon.H1_NEAR_TERM,
            risk=RiskLevel.R1_LOW,
        )

        self.assertTrue(ok)
        self.assertEqual(enh.status, EvolutionState.NEW_STATE)
        self.assertEqual(enh.promotion_level, PromotionLevel.P5_STABLE)
        self.assertEqual(new_state.version, "1.1.0")
        self.assertEqual(new_state.lineage_depth, 1)
        self.assertGreater(new_state.fitness.intelligence_fitness, 0.90)
        self.assertEqual(len(new_state.intelligence_state.vector), 11)
        self.assertTrue(self.runtime.ledger.verify_integrity())
        self.assertGreaterEqual(len(self.runtime.events), 8)

    def test_h11_opt_bottleneck_detection_and_upstream_tracing(self):
        """Test Section 27 & 28: Bottleneck Detection and upstream propagation."""
        optimizer = SelfOptimizer()
        deps = {"QUANTUM_SIMULATION": ["H11_QUANTUM", "H11_SPINTRONIC", "H11_PHYSICA"]}
        latencies = {"H11_QUANTUM": 0.35, "H11_SPINTRONIC": 0.88, "H11_PHYSICA": 0.22}

        bn = optimizer.detect_bottleneck("QUANTUM_SIMULATION", deps, latencies)
        self.assertEqual(bn.weakest_component, "H11_SPINTRONIC")
        self.assertEqual(bn.upstream_origin, "H11_QUANTUM")

    def test_marginal_intelligence_gain_and_saturation(self):
        """Test Section 25 & 26: Marginal Intelligence Gain (MIG) and saturation detection."""
        optimizer = SelfOptimizer()

        # High gain: delta capability 0.15 for 0.02 compute -> MIG = 7.5
        mig_high = optimizer.compute_mig(delta_capability=0.15, delta_resources=0.02)
        self.assertEqual(mig_high, 7.5)

        # Saturation check: diminishing returns
        history = [2.5, 0.8, 0.03]
        self.assertTrue(optimizer.is_intelligence_saturated(history, threshold=0.05))

    def test_regime_escalation_and_intelligence_compilation(self):
        """Test Section 15 & 59: Optimization Regime Escalation and Intelligence Compilation."""
        optimizer = SelfOptimizer()

        # Regime Escalation
        reg0 = OptimizationRegime.REGIME_1_LOCAL
        reg_esc = optimizer.escalate_regime(reg0, failure_count=2)
        self.assertEqual(reg_esc, OptimizationRegime.REGIME_2_COMPOSITION)

        # Intelligence Compilation
        pathway = optimizer.compile_intelligence_pathway(
            signature="SPINTRONIC_HAMILTONIAN_REASONING",
            specialists=["H11_SPINTRONIC", "H11_QUANTUM", "H11_REASON"],
        )
        self.assertEqual(pathway.speedup_factor, 3.8)
        self.assertIn("SPINTRONIC_HAMILTONIAN_REASONING", optimizer.compiled_pathways)

    def test_environment_model_and_drift_detection(self):
        """Test Section 51 & 52: Environment Model and Environment Drift detection."""
        env_model = EnvironmentModel()
        new_env_drifted = EnvironmentState(
            task_load=0.9,
            threat_level=0.45,
            data_distribution_shift=0.35,
        )

        is_drifted, msg = env_model.check_environment_drift(new_env_drifted, threshold=0.20)
        self.assertTrue(is_drifted)
        self.assertIn("ENVIRONMENT_DRIFT_DETECTED", msg)

        # Adaptation loop execution
        adapt_res = env_model.execute_adaptation_loop(msg)
        self.assertEqual(adapt_res["status"], "ADAPTED")
        self.assertFalse(adapt_res["is_permanent_evolution"])

    def test_metacognitive_anti_deception_and_self_model_error(self):
        """Test Section 83, 84, 92: Metacognitive monitoring and anti-deception."""
        meta = MetacognitiveMonitor()

        # Self-Model Error
        err = meta.compute_self_model_error(believed_score=0.98, observed_score=0.86)
        self.assertAlmostEqual(err, 0.12, places=2)

        # Reward Hacking Detection
        is_hack, hack_msg = meta.detect_reward_hacking(benchmark_score=0.99, actual_task_competence=0.45)
        self.assertTrue(is_hack)
        self.assertIn("REWARD_HACKING_DETECTED", hack_msg)

        # Objective Gaming Detection
        is_gaming, gaming_msg = meta.detect_objective_gaming(formal_satisfaction=True, safety_intent_preserved=False)
        self.assertTrue(is_gaming)
        self.assertIn("OBJECTIVE_GAMING_DETECTED", gaming_msg)

    def test_v5_invariants_and_authority_levels(self):
        """Test Section 88 & 113: V5 Invariants (V5-I01 to V5-I20) and Authority Levels."""
        gate = GovernanceGate()
        enh = EnhancementObject(
            target="H11_MEM",
            proposed_change="Optimize LRU eviction policy",
            parent_version="1.0.0",
            baseline_lock=BaselineLock(),
            authority_level=AuthorityLevel.A4_BOUNDED_ADAPTATION,
            vector=PromotionVector(capability=0.92, reliability=0.95, safety=1.0, security=1.0),
        )

        # Authorized call from Control Plane passes
        ok, violations = gate.verify_v5_invariants(enh, caller_id="H11C_CONTROL_PLANE")
        self.assertTrue(ok)
        self.assertEqual(len(violations), 0)

        # Safety regression fails V5-I19
        enh_bad = EnhancementObject(
            target="H11_MEM",
            proposed_change="Aggressive unconstrained bypass",
            parent_version="1.0.0",
            baseline_lock=BaselineLock(),
            vector=PromotionVector(capability=0.95, reliability=0.90, safety=0.85, security=1.0),
        )
        ok_bad, bad_v = gate.verify_v5_invariants(enh_bad, caller_id="H11C_CONTROL_PLANE")
        self.assertFalse(ok_bad)
        self.assertTrue(any("V5_I19_VIOLATION" in v for v in bad_v))


if __name__ == "__main__":
    unittest.main()
