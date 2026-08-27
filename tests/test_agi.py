from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from h11_runtime.agi import H11AGI
from h11_runtime.control_catalog import AGENTS, BY_ID, family_counts
from h11_runtime.control_kernel import ControlError, KernelState, make_agent


class ControlPlaneCatalogTests(unittest.TestCase):
    def test_exactly_125_agents_split_40_45_40(self):
        counts = family_counts()
        self.assertEqual(sum(counts.values()), 125)
        self.assertEqual(len(AGENTS), 125)
        self.assertEqual(len(BY_ID), 125)
        self.assertEqual(counts["integrator"], 40)
        self.assertEqual(counts["orchestrator"], 45)
        self.assertEqual(counts["security"], 40)

    def test_every_agent_has_triple_on_disk(self):
        base = ROOT / "H11C_CONTROL_PLANE"
        missing = []
        for a in AGENTS:
            fam = {
                "integrator": "C01_integrators",
                "orchestrator": "C02_orchestrators",
                "security": "C03_securities",
            }[a.family]
            d = base / fam / a.agent_id
            for name in ("SPEC.md", "schema.json", "agent.py"):
                if not (d / name).is_file():
                    missing.append(f"{a.agent_id}/{name}")
        self.assertEqual(missing, [])

    def test_every_handler_runs_without_skipping_identity(self):
        state = KernelState()
        failures = []
        for a in AGENTS:
            agent = make_agent(a.agent_id, state=state)
            payload = {
                "payload": {"case_id": "c1", "schema_id": "h11.spine.host_infection_case.v1", "patient_id": "P"},
                "case": {"case_id": "c1", "patient_id": "P", "symptoms": ["fever"]},
                "events": ["e1"],
                "traces": [{"ts": "1"}, {"ts": "2"}],
                "required": ["schema_id"],
                "goal": "medical treat",
                "capabilities": ["H11-REASON"],
                "nodes": ["a", "b"],
                "edges": [["a", "b"]],
                "candidates": [{"confidence": 0.9, "id": "x"}],
                "op": "push",
                "key": "k",
                "value": 1,
                "queue": [],
                "item": {"priority": 1, "safety": True},
                "pipeline": ["H11-REASON", "H11-ALIGN"],
                "index": 0,
                "state": "aligned",
                "event": "act",
                "budget": 8,
                "cost": 1,
                "elapsed": 0.1,
                "deadline": 1.0,
                "attempts": 0,
                "max_attempts": 3,
                "halted": False,
                "primary_ok": True,
                "n": 2,
                "branches": ["b0", "b1"],
                "expected": 2,
                "running": 1,
                "incoming_priority": 2,
                "name": "P",
                "identity": "id-1",
                "scopes": ["read"],
                "hop": "x",
                "text": "fever and chills",
                "item": "H11-ALIGN",
                "allowed": ["H11-ALIGN"],
                "label": "medical",
                "sink": "medical",
                "tokens": 3,
                "drop": [],
                "keys": ["secret"],
                "rules": [],
                "attrs": {"align_allowed": True, "confidence": 0.96},
                "consent": True,
                "approvals": ["a", "b"],
                "need": 2,
                "nonce": f"n-{a.agent_id}",
                "op": "has",
                "sandboxed": True,
                "schema_ok": True,
                "token": {"sig": "x"},
                "align_allowed": True,
                "would_act": False,
                "ok_flags": {"align": True, "sandbox": True, "policy": True},
                "admitted": True,
                "checkpoint": {"phase": "PERCEIVE"},
            }
            try:
                out = agent.process(payload)
            except ControlError as exc:
                failures.append(f"{a.agent_id}: {exc}")
                continue
            if out.get("agent_id") != a.agent_id:
                failures.append(f"{a.agent_id}: missing agent_id on output")
        self.assertEqual(failures, [])


class AGITickTests(unittest.IsolatedAsyncioTestCase):
    async def test_falciparum_tick_is_licensed_and_aligned(self):
        agi = H11AGI()
        result = await agi.tick(
            {
                "patient_id": "P-1001",
                "travel_history": ["Kenya"],
                "symptoms": ["fever", "chills"],
                "blood_smear_density_per_ul": 5200.0,
            }
        )
        self.assertTrue(result.admitted)
        self.assertEqual(result.domain, "medical")
        self.assertEqual(result.pipeline_id, "host_infection")
        self.assertTrue(result.allowed)
        self.assertTrue(result.licensed)
        self.assertFalse(result.halted)
        self.assertIn("H11-ALIGN", result.hops)
        self.assertIn("H11C-ADMISSION-CONTROL", result.hops)
        self.assertEqual(result.payload["diagnosis"]["identified_parasite"], "Plasmodium falciparum")
        self.assertEqual(result.action, "TREAT")
        self.assertTrue(result.audit_head)

    async def test_align_enforce_halts_when_act_without_allow(self):
        agi = H11AGI()
        await agi.initialize()
        out = agi.agent("H11C-ALIGN-ENFORCE").process(
            {"trace_id": "t1", "align_allowed": False, "would_act": True}
        )
        self.assertFalse(out["ok"])
        self.assertTrue(agi.state.halt)

    async def test_cognitive_loop_refuses_act_before_align(self):
        agi = H11AGI()
        await agi.initialize()
        loop = agi.agent("H11C-COGNITIVE-LOOP")
        loop.state.phase = "ACT"
        with self.assertRaises(ControlError):
            loop.process({"align_allowed": False})


if __name__ == "__main__":
    unittest.main()
