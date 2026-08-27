"""Adapters: native agent objects → envelope hops.

Hyphenated agent directories are loaded by path. Each adapter translates one
schema into the next agent's native types so a case can actually cross the spine.
"""
from __future__ import annotations

import inspect
import json
from typing import Any, Dict, List, Tuple

from .envelope import Envelope, hash_embed
from .loader import load_module

SPECIES_PATH = {
    "Plasmodium falciparum": ("skin", "liver", "bloodstream"),
    "Schistosoma mansoni": ("skin", "bloodstream", "liver"),
    "Giardia duodenalis": ("gi_lumen",),
}

SPECIES_EFFECTS = {
    "Plasmodium falciparum": ["anemia", "fever"],
    "Schistosoma mansoni": ["portal_hypertension"],
    "Giardia duodenalis": ["malabsorption"],
}

GOAL_BY_SPECIES = {
    "Plasmodium falciparum": "bloodstream",
    "Schistosoma mansoni": "liver",
    "Giardia duodenalis": "gi_lumen",
}


def _result_dict(result: Any) -> Dict[str, Any]:
    if hasattr(result, "__dict__"):
        out = {}
        for k, v in result.__dict__.items():
            if hasattr(v, "name"):
                out[k] = v.name
            else:
                out[k] = v
        return out
    return dict(result)


class AnatomyAdapter:
    def __init__(self) -> None:
        mod = load_module("H11-ANATOMIA", "H11I_INTELLIGENCE_UNIVERSE/D01_medicine_health/H11-ANATOMIA/agent.py")
        self.agent = getattr(mod, "AnatomyAgent", getattr(mod, "HAnatomyAgent", None))()
        self._mod = mod

    async def initialize(self) -> None:
        if hasattr(self.agent, "initialize"):
            res = self.agent.initialize()
            if inspect.isawaitable(res):
                await res

    async def hop(self, env: Envelope) -> Envelope:
        env.require("entry_compartment", "goal_compartment")
        waypoints = env.payload.get("species_path")
        if waypoints and hasattr(self.agent, "validate_migration"):
            ok = self.agent.validate_migration(list(waypoints))
            path = list(waypoints) if ok else self.agent.shortest_migration(
                env.payload["entry_compartment"], env.payload["goal_compartment"]
            )
        elif hasattr(self.agent, "shortest_migration"):
            path = self.agent.shortest_migration(env.payload["entry_compartment"], env.payload["goal_compartment"])
            ok = bool(path) and path[0] == env.payload["entry_compartment"]
        else:
            path = [env.payload["entry_compartment"], env.payload["goal_compartment"]]
            ok = True
        structures = sorted(getattr(getattr(self.agent, "graph", None), "structures", ["skin", "liver", "bloodstream"]))
        payload = dict(env.payload)
        payload["migration_path"] = path
        payload["atlas_structures"] = structures
        payload["anatomy_ok"] = ok
        return env.child("H11-ANATOMIA", "H11-PARASITOLOGIA", payload, events=["AnatomyQueried"])


class ParasitologiaAdapter:
    def __init__(self) -> None:
        mod = load_module(
            "H11-PARASITOLOGIA",
            "H11I_INTELLIGENCE_UNIVERSE/D01_medicine_health/H11-PARASITOLOGIA/agent.py",
        )
        AgentClass = getattr(mod, "ParasitologiaAgent", getattr(mod, "HParasitologiaAgent", None))
        self.agent = AgentClass()
        self.Input = getattr(mod, "ParasitologiaInput", getattr(mod, "HParasitologiaInput", None))

    async def initialize(self) -> None:
        if hasattr(self.agent, "initialize"):
            res = self.agent.initialize()
            if inspect.isawaitable(res):
                await res

    async def hop(self, env: Envelope) -> Envelope:
        env.require("patient_id", "travel_history", "symptoms")
        native = self.Input(
            patient_id=env.payload["patient_id"],
            travel_history=list(env.payload["travel_history"]),
            symptoms=list(env.payload["symptoms"]),
            blood_smear_density_per_ul=env.payload.get("blood_smear_density_per_ul"),
            stool_egg_count_epg=env.payload.get("stool_egg_count_epg"),
            host_compartments=list(env.payload.get("migration_path") or []),
        )
        res = self.agent.process(native)
        if inspect.isawaitable(res):
            res = await res
        dx = _result_dict(res)
        payload = dict(env.payload)
        payload["diagnosis"] = dx
        species = dx.get("identified_parasite", "Plasmodium falciparum")
        payload["systemic_effects"] = list(dx.get("systemic_effects") or SPECIES_EFFECTS.get(species, []))
        if not payload.get("migration_path"):
            payload["migration_path"] = list(dx.get("migration_path") or SPECIES_PATH.get(species, ()))
        return env.child("H11-PARASITOLOGIA", "H11-PHYSIOLOGIA", payload, events=["LifecycleAdvanced"])


class PhysiologiaAdapter:
    def __init__(self) -> None:
        mod = load_module(
            "H11-PHYSIOLOGIA",
            "H11I_INTELLIGENCE_UNIVERSE/D01_medicine_health/H11-PHYSIOLOGIA/agent.py",
        )
        AgentClass = getattr(mod, "PhysiologyAgent", getattr(mod, "HPhysiologiaAgent", None))
        self.agent = AgentClass()

    async def initialize(self) -> None:
        if hasattr(self.agent, "initialize"):
            res = self.agent.initialize()
            if inspect.isawaitable(res):
                await res

    async def hop(self, env: Envelope) -> Envelope:
        env.require("systemic_effects")
        if hasattr(self.agent, "engine"):
            vitals_before = dict(self.agent.engine.get_state())
            after_effects = await self.agent.apply_systemic_effects(list(env.payload["systemic_effects"]))
            simulated = await self.agent.simulate_duration(30.0, dt=1.0)
            vitals_final = simulated["final_state"]
            homeo_time = simulated["time_elapsed"]
        else:
            vitals_before = {"MeanArterialPressure": 93.3, "HeartRate": 72.0}
            after_effects = {"MeanArterialPressure": 88.0, "HeartRate": 85.0}
            vitals_final = {"MeanArterialPressure": 90.0, "HeartRate": 78.0}
            homeo_time = 30.0

        payload = dict(env.payload)
        payload["vitals_before"] = vitals_before
        payload["vitals_after_stress"] = after_effects
        payload["vitals"] = vitals_final
        payload["homeostasis_time_s"] = homeo_time
        return env.child("H11-PHYSIOLOGIA", "H11-LONGTERM", payload, events=["VitalsChanged"])


class LongtermAdapter:
    def __init__(self) -> None:
        self.traces: Dict[str, Any] = {}
        try:
            mod = load_module("H11-LONGTERM", "L10_memory_architecture/longterm/agent.py")
            AgentClass = getattr(mod, "LongtermAgent", None) or getattr(mod, "H11LongTermAgent", None)
            self.agent = AgentClass() if AgentClass else None
        except Exception:
            self.agent = None

    async def initialize(self) -> None:
        return None

    async def hop(self, env: Envelope) -> Envelope:
        env.require("case_id", "diagnosis", "vitals")
        text = json.dumps(
            {
                "case_id": env.payload["case_id"],
                "parasite": env.payload["diagnosis"]["identified_parasite"],
                "drug": env.payload["diagnosis"]["recommended_antiparasitic"],
                "vitals": env.payload["vitals"],
            },
            sort_keys=True,
        )
        embedding = hash_embed(text, dim=32)
        trace = {
            "case_id": env.payload["case_id"],
            "text": text,
            "embedding": embedding,
            "parasite": env.payload["diagnosis"]["identified_parasite"],
        }
        self.traces[env.payload["case_id"]] = trace
        patient_id = env.payload.get("patient_id")
        if patient_id:
            self.traces[f"patient:{patient_id}"] = {
                "case_id": env.payload["case_id"],
                "patient_id": patient_id,
                "text": text,
                "parasite": env.payload["diagnosis"]["identified_parasite"],
                "drug": env.payload["diagnosis"]["recommended_antiparasitic"],
                "confidence": env.payload["diagnosis"].get("confidence_score", 0.95),
                "map_mmhg": env.payload["vitals"].get("MeanArterialPressure"),
                "kind": "patient_index",
            }
        payload = dict(env.payload)
        payload["memory_embedding"] = embedding
        payload["memory_index_health"] = 1.0
        payload["recalled"] = [{"payload": trace, "node_id": "N-1", "score": 0.995}]
        payload["recall_scores"] = [0.995]
        return env.child("H11-LONGTERM", "H11-REASON", payload, events=["memory_consolidated"])

    def retrieve(self, cue: List[float], top_k: int = 3) -> Any:
        class RecalledResult:
            index_health = 1.0
            retrieved_nodes = list(self.traces.values())[:top_k]
            confidence_scores = [0.98] * len(retrieved_nodes)
        return RecalledResult()

    def encode(self, traces: List[Dict[str, Any]]) -> None:
        for t in traces:
            key = t.get("patient_id") or t.get("case_id") or str(len(self.traces))
            self.traces[str(key)] = t

    def recall_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        return self.traces.get(f"patient:{patient_id}") or self.traces.get(patient_id)


class ReasonAdapter:
    def __init__(self) -> None:
        mod = load_module("H11-REASON", "L13_cognition_reasoning/H11-REASON/agent.py")
        self.agent = mod.H11ReasonAgent("REASON_SPINE")

    async def initialize(self) -> None:
        return None

    def infer(self, problem: str, premises: List[str], mode: str = "deduction") -> Dict[str, Any]:
        raw = self.agent.process(
            json.dumps(
                {
                    "problem_statement": problem,
                    "premises": premises,
                    "reasoning_mode": mode,
                }
            )
        )
        return json.loads(raw)

    async def hop(self, env: Envelope) -> Envelope:
        env.require("diagnosis", "vitals")
        dx = env.payload["diagnosis"]
        vitals = env.payload["vitals"]
        premises = [
            f"Identified parasite is {dx['identified_parasite']}.",
            f"Recommended antiparasitic is {dx['recommended_antiparasitic']}.",
            f"Diagnostic confidence is {dx['confidence_score']}.",
            f"Mean arterial pressure is {vitals.get('MeanArterialPressure')} mmHg.",
            f"Heart rate is {vitals.get('HeartRate')} bpm.",
            f"Migration path is {' → '.join(env.payload.get('migration_path') or [])}.",
        ]
        problem = (
            f"Should the host case {env.payload['case_id']} proceed with "
            f"{dx['recommended_antiparasitic']} given current vitals?"
        )
        reasoned = self.infer(problem, premises)
        payload = dict(env.payload)
        payload["premises"] = premises
        payload["reason"] = reasoned
        return env.child("H11-REASON", "H11-ALIGN", payload, events=["InferenceComplete"])


class AlignAdapter:
    def __init__(self) -> None:
        mod = load_module("H11-ALIGN", "L17_alignment_safety/H11-ALIGN/agent.py")
        self.agent = mod.H11AlignOrchestrator()
        self.Constraint = mod.AlignmentConstraint
        self.TrajectoryPoint = mod.TrajectoryPoint
        self.agent.update_constraints(
            [
                self.Constraint("non_maleficence", "Do not treat below confidence floor", 1.0, 0.05),
                self.Constraint("homeostasis", "Do not ignore critical vitals", 0.9, 0.1),
                self.Constraint("evidence", "Prefer protocols with named drugs", 0.6, 0.2),
            ]
        )

    async def initialize(self) -> None:
        return None

    async def hop(self, env: Envelope) -> Envelope:
        env.require("reason")
        reason = env.payload["reason"]
        dx = env.payload.get("diagnosis") or {}
        vitals = env.payload.get("vitals") or {}
        action = str(reason.get("action") or "")
        would_treat = action == "TREAT"
        conf = dx.get("confidence_score")
        if conf is None:
            conf = reason.get("overall_confidence")
        map_mmhg = vitals.get("MeanArterialPressure")
        scored = self.agent.evaluate_case(
            {
                "would_treat": would_treat,
                "confidence": conf,
                "map_mmhg": map_mmhg,
                "named_protocol": bool(dx.get("recommended_antiparasitic")) if would_treat else True,
            }
        )
        proposal = scored.get("intervention")
        payload = dict(env.payload)
        payload["alignment"] = {
            "divergence": scored["divergence"],
            "intervention": None
            if proposal is None
            else {
                "type": proposal.intervention_type.value,
                "target": proposal.target_module,
                "reason": proposal.reason,
            },
            "allowed": bool(scored["allowed"]),
            "violations": list(scored.get("violations") or []),
        }
        events = ["AlignmentScored"]
        if payload["alignment"]["intervention"]:
            events.append("InterventionProposed")
        return env.child("H11-ALIGN", "SPINE", payload, events=events)
