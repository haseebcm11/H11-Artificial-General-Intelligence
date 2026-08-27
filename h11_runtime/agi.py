"""AGI kernel: admit → bind → compose → run spine → align-enforce → remember → seal.

This is the control plane sitting on the specialist roster. It does not skip
ALIGN. Unadmitted cases never reach PIPELINE-RUNNER.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .adapters import AlignAdapter, LongtermAdapter, ReasonAdapter
from .cognitive import CognitiveSpine
from .control_kernel import ControlAgent, ControlError, KernelState, make_agent
from .envelope import new_id
from .haep import HAEPRuntime
from .spine import HostInfectionSpine, SpineResult, assert_crossed


@dataclass
class AGIResult:
    case_id: str
    admitted: bool
    domain: str
    pipeline_id: str
    identity: str
    licensed: bool
    allowed: bool
    halted: bool
    hops: List[str]
    audit_head: str
    payload: Dict[str, Any]
    action: str = ""
    spine: Optional[SpineResult] = None
    events: List[str] = field(default_factory=list)
    error: Optional[str] = None


class H11AGI:
    """One gated cognitive system over the specialist spines."""

    def __init__(self) -> None:
        self.state = KernelState()
        self.longterm = LongtermAdapter()
        self.reason = ReasonAdapter()
        self.align = AlignAdapter()
        self.spine = HostInfectionSpine(
            longterm=self.longterm, reason=self.reason, align=self.align
        )
        self.cog = CognitiveSpine(
            longterm=self.longterm, reason=self.reason, align=self.align
        )
        self.haep = HAEPRuntime()
        self._ready = False

    def agent(self, agent_id: str) -> ControlAgent:
        return make_agent(agent_id, state=self.state)

    async def initialize(self) -> None:
        if self._ready:
            return
        self.agent("H11C-SPINE-REGISTRAR").process({})
        await self.spine.initialize()
        await self.cog.initialize()
        self._ready = True

    def _board_facts(self, patient_id: Optional[str]) -> List[str]:
        if not patient_id:
            return []
        got = self.agent("H11C-BLACKBOARD").process({"op": "get", "key": patient_id})
        val = next(iter(got.get("board", {}).values()), None)
        if not isinstance(val, dict):
            return []
        facts = []
        if val.get("parasite"):
            facts.append(f"Identified parasite is {val['parasite']}.")
        if val.get("drug"):
            facts.append(f"Recommended antiparasitic is {val['drug']}.")
        if val.get("confidence") is not None:
            facts.append(f"Diagnostic confidence is {val['confidence']}.")
        if val.get("conclusion"):
            facts.append(str(val["conclusion"]))
        return facts

    def _remember_case(self, payload: Dict[str, Any]) -> None:
        patient_id = payload.get("patient_id")
        dx = payload.get("diagnosis") or {}
        if not patient_id or not dx:
            return
        self.agent("H11C-BLACKBOARD").process(
            {
                "op": "set",
                "key": patient_id,
                "value": {
                    "case_id": payload.get("case_id"),
                    "parasite": dx.get("identified_parasite"),
                    "drug": dx.get("recommended_antiparasitic"),
                    "confidence": dx.get("confidence_score"),
                    "conclusion": (payload.get("reason") or {}).get("conclusion"),
                },
            }
        )

    async def tick(self, case: Dict[str, Any]) -> AGIResult:
        if not self._ready:
            await self.initialize()
        events: List[str] = []
        case = dict(case)
        case.setdefault("case_id", new_id("case"))
        case.setdefault(
            "schema_id",
            "h11.spine.host_infection_case.v1"
            if case.get("symptoms") or case.get("blood_smear_density_per_ul")
            else "h11.spine.cognitive_query.v1",
        )

        admit = self.agent("H11C-ADMISSION-CONTROL").process({"case": case})
        events.append("admitted" if admit["admitted"] else "denied")
        if not admit["admitted"]:
            return AGIResult(
                case_id=case["case_id"],
                admitted=False,
                domain="",
                pipeline_id="",
                identity="",
                licensed=False,
                allowed=False,
                halted=True,
                hops=["H11C-ADMISSION-CONTROL"],
                audit_head=self.agent("H11C-AUDIT-CHAIN").process({"event": "deny"})["head"],
                payload=case,
                error="not_admitted",
            )

        ident = self.agent("H11C-IDENTITY").process({"name": case.get("patient_id") or case["case_id"]})
        token = self.agent("H11C-CAPABILITY-TOKEN").process(
            {"identity": ident["identity"], "scopes": ["read", "reason", "align"]}
        )
        sandboxed = self.agent("H11C-SANDBOX-GATE").process({"hop": "tick"})
        schema_ok = self.agent("H11C-SCHEMA-FIREWALL").process({"payload": case, "required": ["schema_id"]})
        inj_text = " ".join(
            [
                " ".join(map(str, case.get("symptoms") or [])),
                str(case.get("query") or ""),
                str(case.get("goal") or ""),
            ]
        )
        inj = self.agent("H11C-INJECTION-GATE").process({"text": inj_text})
        if inj["dirty"]:
            self.agent("H11C-QUARANTINE").process({})
            return AGIResult(
                case_id=case["case_id"],
                admitted=True,
                domain="",
                pipeline_id="",
                identity=ident["identity"],
                licensed=False,
                allowed=False,
                halted=True,
                hops=["H11C-INJECTION-GATE", "H11C-QUARANTINE"],
                audit_head=self.agent("H11C-AUDIT-CHAIN").process({"event": "quarantine"})["head"],
                payload=case,
                error="injection",
            )

        zt = self.agent("H11C-ZERO-TRUST-HOP").process(
            {
                "identity": ident["identity"],
                "token": token["token"],
                "sandboxed": sandboxed["sandboxed"],
                "schema_ok": schema_ok["ok"],
            }
        )
        if not zt["ok"]:
            raise ControlError("zero-trust hop failed")

        routed = self.agent("H11C-CROSS-DOMAIN-ROUTER").process({"case": case})
        domain = routed["domain"]
        pipeline_id = routed["pipeline_id"]
        label = self.agent("H11C-DATA-CLASS").process({"payload": case})
        comp = self.agent("H11C-COMPARTMENT").process({"label": label["label"], "sink": domain})
        if not comp["ok"]:
            self.agent("H11C-HALT").process({})
            return AGIResult(
                case_id=case["case_id"],
                admitted=True,
                domain=domain,
                pipeline_id=pipeline_id,
                identity=ident["identity"],
                licensed=False,
                allowed=False,
                halted=True,
                hops=["H11C-COMPARTMENT", "H11C-HALT"],
                audit_head=self.agent("H11C-AUDIT-CHAIN").process({"event": "compartment_fail"})["head"],
                payload=case,
                error="compartment",
            )

        caps = self.agent("H11C-CAPABILITY-MAPPER").process({"goal": domain})
        composed = self.agent("H11C-PIPELINE-COMPOSER").process(
            {"goal": domain, "capabilities": caps["capabilities"]}
        )
        hooked = self.agent("H11C-ALIGN-HOOK").process({"pipeline": composed["pipeline"]})
        self.state.phase = "PERCEIVE"
        self.agent("H11C-COGNITIVE-LOOP").process({"align_allowed": False})

        spine_result: Optional[SpineResult] = None
        hops = list(hooked["pipeline"])
        allowed = False
        would_act = False
        if pipeline_id == "host_infection":
            spine_result = await self.spine.run(case)
            assert_crossed(spine_result)
            allowed = spine_result.allowed
            hops = ["H11C-ADMISSION-CONTROL", "H11C-ZERO-TRUST-HOP"] + spine_result.hops
            case = dict(spine_result.payload)
            events.extend(spine_result.events)
            self._remember_case(case)
        elif pipeline_id == "cognitive_loop":
            case["blackboard_facts"] = self._board_facts(case.get("patient_id"))
            spine_result = await self.cog.run(case)
            allowed = spine_result.allowed
            hops = ["H11C-ADMISSION-CONTROL", "H11C-ZERO-TRUST-HOP"] + spine_result.hops
            case = dict(spine_result.payload)
            events.extend(spine_result.events)
        else:
            allowed = False
            hops = ["H11C-ADMISSION-CONTROL", "H11C-CROSS-DOMAIN-ROUTER", "H11C-ALIGN-HOOK"]

        action = str((case.get("reason") or {}).get("action") or "")
        would_act = action == "TREAT"

        enforce = self.agent("H11C-ALIGN-ENFORCE").process(
            {
                "trace_id": case.get("case_id"),
                "align_allowed": allowed,
                "would_act": would_act,
            }
        )
        conf = (case.get("diagnosis") or {}).get("confidence_score")
        if conf is None:
            conf = (case.get("reason") or {}).get("overall_confidence") or 0
        if not would_act:
            conf = max(float(conf), 0.85)
        med = self.agent("H11C-MEDICAL-SAFETY").process(
            {
                "attrs": {
                    "align_allowed": allowed,
                    "confidence": conf,
                }
            }
        )
        licensed = self.agent("H11C-ACTION-LICENSE").process(
            {
                "ok_flags": {
                    "align": enforce["ok"],
                    "sandbox": sandboxed["sandboxed"],
                    "policy": med["decision"] == "allow",
                }
            }
        )
        if not enforce["ok"] or not licensed["licensed"]:
            self.agent("H11C-HALT").process({})

        self.agent("H11C-MEMORY-PROJECTOR").process({"payload": case})
        head = self.agent("H11C-AUDIT-CHAIN").process(
            {"event": {"case_id": case["case_id"], "allowed": allowed, "licensed": licensed["licensed"]}}
        )["head"]
        if allowed and licensed["licensed"]:
            try:
                self.agent("H11C-COGNITIVE-LOOP").process({"align_allowed": True})
            except ControlError:
                pass

        return AGIResult(
            case_id=case["case_id"],
            admitted=True,
            domain=domain,
            pipeline_id=pipeline_id,
            identity=ident["identity"],
            licensed=bool(licensed["licensed"]),
            allowed=allowed,
            halted=self.state.halt,
            hops=hops,
            audit_head=head,
            payload=case,
            action=action,
            spine=spine_result,
            events=events,
        )
