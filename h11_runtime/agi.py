"""H11-AGI: Sovereign Governed Cognitive Operating Architecture.

Unifies:
1. 1,000-Agent Cognitive Universe (H11Z + H11I + H11C)
2. Advanced Neural Clustering & Mixture-of-Experts (MoE) Softmax Gating
3. H11-LSE v3.0: 16-Subsystem Ultra-Omniscient Web Superintelligence & Graph-RAG
4. H11-LEARN: Continuous Distillation & Parameter Fine-Tuning Pipeline
5. Non-Bypassable ALIGN Hard Gate & Zero-Trust Security (C03)
6. Six Operational Graphs & Cryptographic Merkle Provenance Audit Chain
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .adapters import AlignAdapter, LongtermAdapter, ReasonAdapter
from .cognitive import CognitiveSpine
from .control_kernel import ControlAgent, ControlError, KernelState, make_agent
from .envelope import new_id
from .haep import HAEPRuntime
from .spine import HostInfectionSpine, SpineResult, assert_crossed

logger = logging.getLogger(__name__)

# ── Search & Knowledge Engine ───────────────────────────────────────────────
_search_available = False
try:
    from .search.api import SearchConfig, SearchQuery, SearchService
    from .search.omni_engine import OmniSearchEngine, OmniSearchResponse
    from .search.rar import RetrievalAugmentedReasoner, RetrievedDocument
    _search_available = True
except ImportError as exc:
    logger.info(f"H11-SEARCH not available: {exc}")

# ── Learning Pipeline ───────────────────────────────────────────────────────
_learn_available = False
try:
    from .learn.collector import CollectionConfig, DataCollector
    from .learn.distiller import KnowledgeDistiller
    from .learn.governed_update import GovernedUpdater
    _learn_available = True
except ImportError as exc:
    logger.info(f"H11-LEARN not available: {exc}")

# ── Neural Agent Clustering ─────────────────────────────────────────────────
_clustering_available = False
try:
    from .neural_clustering.neural_cluster_engine import (
        CognitiveManifoldCluster,
        NeuralAgentClusterEngine,
        NeuralRoutingDecision,
    )
    _clustering_available = True
except ImportError as exc:
    logger.info(f"Neural Clustering not available: {exc}")


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
    retrieved_evidence: List[Dict[str, Any]] = field(default_factory=list)
    learning_recorded: bool = False
    neural_routing: Optional[Dict[str, Any]] = None
    merkle_provenance_root: Optional[str] = None


class H11AGI:
    """Master Governed Cognitive Operating System uniting 1,000 agents, LSE v3.0, and H11-LEARN."""

    def __init__(
        self,
        enable_search: bool = True,
        enable_learning: bool = True,
        enable_neural_clustering: bool = True,
        workspace_root: Optional[str] = None,
    ) -> None:
        self.state = KernelState()
        self.longterm = LongtermAdapter()
        self.reason = ReasonAdapter()
        self.align = AlignAdapter()
        self.spine = HostInfectionSpine(longterm=self.longterm, reason=self.reason, align=self.align)
        self.cog = CognitiveSpine(longterm=self.longterm, reason=self.reason, align=self.align)
        self.haep = HAEPRuntime()
        self._ready = False

        # ── 1. H11-LSE v3.0: Sovereign Search & Web Superintelligence ───────
        self.search: Optional[SearchService] = None
        self.omni_search: Optional[OmniSearchEngine] = None
        self.rar: Optional[RetrievalAugmentedReasoner] = None
        if enable_search and _search_available:
            self.search = SearchService()
            self.omni_search = OmniSearchEngine(self.search.config)
            self.rar = RetrievalAugmentedReasoner(self.search)
            logger.info("H11-LSE v3.0 initialized — Omniscient web search & Graph-RAG enabled.")

        # ── 2. H11-LEARN: Continuous Distillation Pipeline ──────────────────
        self.collector: Optional[DataCollector] = None
        self.distiller: Optional[KnowledgeDistiller] = None
        self.governed_updater: Optional[GovernedUpdater] = None
        if enable_learning and _learn_available:
            self.collector = DataCollector()
            self.distiller = KnowledgeDistiller()
            self.governed_updater = GovernedUpdater()
            logger.info("H11-LEARN initialized — continuous learning and rule distillation enabled.")

        # ── 3. Neural Agent Clustering Engine (1,000 Agents) ────────────────
        self.cluster_engine: Optional[NeuralAgentClusterEngine] = None
        if enable_neural_clustering and _clustering_available:
            self.cluster_engine = NeuralAgentClusterEngine(workspace_root=workspace_root)
            logger.info(f"NeuralAgentClusterEngine initialized — {len(self.cluster_engine.agents)} agents clustered.")

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
        """Executes full 24-step cognitive loop with live LSE search, Neural MoE routing, and ALIGN gate."""
        if not self._ready:
            await self.initialize()
        events: List[str] = []
        if hasattr(case, "input_data") and isinstance(case.input_data, dict):
            case = dict(case.input_data)
        elif hasattr(case, "__dict__") and not isinstance(case, dict):
            case = dict(case.__dict__)
        else:
            case = dict(case)
        case.setdefault("case_id", new_id("case"))
        case.setdefault(
            "schema_id",
            "h11.spine.host_infection_case.v1"
            if case.get("symptoms") or case.get("blood_smear_density_per_ul")
            else "h11.spine.cognitive_query.v1",
        )

        # ── Step 1-4: Admission, Identity & Zero-Trust Verification ─────────
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

        # ── Step 5: H11-LSE v3.0 ULTRA-OMNISCIENT KNOWLEDGE RETRIEVAL ────────
        retrieved_evidence: List[Dict[str, Any]] = []
        merkle_root_hash: Optional[str] = None
        query_text = " ".join(filter(None, [
            str(case.get("query") or ""),
            str(case.get("goal") or ""),
            " ".join(map(str, case.get("symptoms") or [])),
        ])).strip()

        if self.omni_search is not None and query_text:
            try:
                omni_resp = await self.omni_search.omni_search(query_text, domain_hint=domain)
                merkle_root_hash = omni_resp.merkle_root
                retrieved_evidence = [
                    {
                        "url": r.get("url"),
                        "title": r.get("title"),
                        "snippet": r.get("snippet"),
                        "relevance": r.get("score"),
                        "source": r.get("source"),
                    }
                    for r in omni_resp.base_response.results
                ]
                case["retrieved_evidence"] = retrieved_evidence
                case["evidence_briefing"] = omni_resp.briefing
                case["merkle_root"] = merkle_root_hash
                events.append(f"retrieved_{len(retrieved_evidence)}_evidence_items")
                logger.info(f"LSE v3.0: Retrieved {len(retrieved_evidence)} items, Merkle root {merkle_root_hash[:16]}...")
            except Exception as exc:
                logger.warning(f"LSE v3.0 retrieval error: {exc}")

        # ── Step 6: NEURAL AGENT CLUSTERING & MoE SOFTMAX GATING ─────────────
        neural_routing_dict: Optional[Dict[str, Any]] = None
        if self.cluster_engine is not None and query_text:
            try:
                routing_decision = self.cluster_engine.route_query(
                    query=query_text,
                    retrieved_evidence=retrieved_evidence,
                    top_k_agents=6,
                )
                neural_routing_dict = {
                    "manifold": routing_decision.primary_cluster_id,
                    "affinity": routing_decision.cluster_affinity,
                    "activated_agents": routing_decision.selected_agent_ids,
                    "rationale": routing_decision.rationale,
                }
                case["neural_routing"] = neural_routing_dict
                events.append(f"moe_routed_to_{routing_decision.primary_cluster_id}")
                logger.info(f"MoE Gated: {routing_decision.rationale}")
            except Exception as exc:
                logger.warning(f"Neural routing error: {exc}")

        # ── Step 7: SPINE & BLACKBOARD REASONING DELIBERATION ────────────────
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

        # ── Step 8: NON-BYPASSABLE ALIGN HARD GATE ENFORCEMENT ───────────────
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
            {"attrs": {"align_allowed": allowed, "confidence": conf}}
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

        # ── Step 9: CRYPTOGRAPHIC AUDIT SEALING & MERKLE WITNESS ────────────
        self.agent("H11C-MEMORY-PROJECTOR").process({"payload": case})
        audit_event = {
            "case_id": case["case_id"],
            "allowed": allowed,
            "licensed": licensed["licensed"],
            "merkle_root": merkle_root_hash,
            "manifold": neural_routing_dict.get("manifold") if neural_routing_dict else None,
        }
        head = self.agent("H11C-AUDIT-CHAIN").process({"event": audit_event})["head"]

        if allowed and licensed["licensed"]:
            try:
                self.agent("H11C-COGNITIVE-LOOP").process({"align_allowed": True})
            except ControlError:
                pass

        # ── Step 10: H11-LEARN CONTINUOUS RECORDING & DISTILLATION ──────────
        learning_recorded = False
        if self.collector is not None and allowed:
            try:
                self.collector.record(
                    agent_id=f"H11C-{pipeline_id.upper()}",
                    case_id=case["case_id"],
                    query=query_text,
                    retrieved_docs=retrieved_evidence,
                    output={"action": action, "domain": domain, "allowed": allowed, "merkle": merkle_root_hash},
                    domain=domain,
                    feedback_score=float(conf) if conf else None,
                )
                learning_recorded = True
                events.append("learning_recorded")
                logger.info(f"H11-LEARN: Experience recorded for case {case['case_id']}")
            except Exception as exc:
                logger.warning(f"H11-LEARN recording error: {exc}")

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
            retrieved_evidence=retrieved_evidence,
            learning_recorded=learning_recorded,
            neural_routing=neural_routing_dict,
            merkle_provenance_root=merkle_root_hash,
        )

    def get_system_telemetry(self) -> Dict[str, Any]:
        """Returns unified telemetry across all connected layers, agents, LSE, and learn."""
        telemetry = {
            "state_phase": self.state.phase,
            "halted": self.state.halt,
            "indexed_agents_total": len(self.cluster_engine.agents) if self.cluster_engine else 0,
            "clustering_stats": self.cluster_engine.get_cluster_stats() if self.cluster_engine else None,
            "omni_search_stats": self.omni_search.get_full_stats() if self.omni_search else None,
            "learn_stats": self.collector.stats if self.collector else None,
        }
        return telemetry
