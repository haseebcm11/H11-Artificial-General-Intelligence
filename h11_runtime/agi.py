"""H11-AGI: Governed 1,000 Multi-Agent AGI Operating System.

Authoritative Runtime Path:
INPUT -> H11C ADMISSION -> IDENTITY / CAPABILITY / SECURITY -> WORLD + CASE STATE ->
TASK UNDERSTANDING & DECOMPOSITION -> COGNITIVE PLANNING -> CAPABILITY RESOLUTION ->
MOE SPECIALIST ROUTING -> TYPED EXECUTION GRAPH -> REAL SPECIALIST EXECUTION (PARALLEL) ->
EVIDENCE COLLECTION -> CROSS-AGENT DELIBERATION -> SYNTHESIS ->
INDEPENDENT VERIFICATION (REPLAN IF REJECTED) -> ALIGNMENT / GOVERNANCE ->
ACTION OR FINAL ANSWER -> OBSERVATION -> MEMORY -> LEARNING / EVALUATION.
"""
from __future__ import annotations

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from .adapters import AlignAdapter, LongtermAdapter, ReasonAdapter
from .case.blackboard import Blackboard
from .case.case import Case, CaseState
from .case.world_model import WorldModel
from .cognitive import CognitiveSpine
from .contracts.action_license import ActionLicense
from .contracts.action_proposal import ActionProposal
from .contracts.agent_result import AgentResult
from .contracts.envelope import CaseEnvelope, Modality, RiskClass
from .control_catalog import AGENTS
from .control_kernel import ControlAgent, ControlError, KernelState, make_agent
from .deliberation.deliberator import Deliberator, SynthesisCandidate
from .envelope import new_id
from .evidence.item import EvidenceItem
from .evidence.ledger import EvidenceLedger
from .execution.executor import GraphExecutor
from .execution.specialist import SpecialistExecutionCoordinator, SpecialistExecutionRecord
from .graph.agent_graph import AgentGraph
from .graph.capability_graph import CapabilityGraph
from .graph.execution_graph import ExecutionGraph, ExecutionNode
from .graph.governance_graph import GovernanceGraph
from .graph.state_graph import StateGraph
from .haep import HAEPRuntime
from .loader import AgentIdentity, discover_all_agents, load_agent, LoadedAgentInterface
from .memory.service import MemoryService
from .memory.types import MemoryType
from .planning.planner import CognitivePlan, CognitivePlanner
from .planning.tool_planner import AutonomousPlanResult, AutonomousToolPlanner
from .registry.agent_registry import AgentRegistry
from .spine import HostInfectionSpine, SpineResult, assert_crossed
from .telemetry.bus import EventBus
from .telemetry.event import RuntimeEvent
from .tools import AutonomousToolLoop, GovernedToolRegistry, ToolSpec
from .state.budget import ResourceBudget
from .verification.verifier import IndependentVerifier, VerificationReport

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
    blackboard_summary: Optional[Dict[str, Any]] = None
    execution_graph_nodes: int = 0
    state_progression: List[str] = field(default_factory=list)
    specialist_results: List[Dict[str, Any]] = field(default_factory=list)
    deliberation: Optional[Dict[str, Any]] = None
    verification: Optional[Dict[str, Any]] = None
    cognitive_plan: Optional[Dict[str, Any]] = None
    contributing_agents: List[str] = field(default_factory=list)
    tool_loop: Optional[Dict[str, Any]] = None
    tool_planning: Optional[Dict[str, Any]] = None


class H11AGI:
    """Master 1,000 Multi-Agent AGI Operating System runtime."""

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

        # ── Core Integration Subsystems ─────────────────────────────────────
        self.event_bus = EventBus()
        self.memory_service = MemoryService()
        self.evidence_ledger = EvidenceLedger()
        self.agent_registry = AgentRegistry(auto_discover=True)
        self.graph_executor = GraphExecutor(max_concurrent=16)
        self.deliberator = Deliberator()
        self.verifier = IndependentVerifier()
        self.blackboards: Dict[str, Blackboard] = {}
        self.world_models: Dict[str, WorldModel] = {}
        self.active_graphs: Dict[str, ExecutionGraph] = {}
        self.state_graph = StateGraph()
        self.agent_graph = AgentGraph()
        self.capability_graph = CapabilityGraph()
        self.governance_graph = GovernanceGraph()
        self.tool_registry = GovernedToolRegistry()
        self.tool_loop = AutonomousToolLoop(
            registry=self.tool_registry,
            authorizer=lambda name: bool(
                self.agent("H11C-TOOL-ALLOWLIST").process(
                    {"item": name, "allowed": self.tool_registry.names()}
                )["ok"]
            ),
        )

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

        # Bind only capabilities that are genuinely available in this runtime.
        if self.omni_search is not None:
            self.tool_registry.register(ToolSpec(
                name="knowledge.search",
                description="Retrieve grounded evidence through H11-LSE.",
                handler=self._tool_knowledge_search,
                required_arguments=("query",),
                timeout_seconds=8.0,
                retryable_exceptions=(TimeoutError, ConnectionError),
            ))
        if self.cluster_engine is not None:
            self.tool_registry.register(ToolSpec(
                name="agents.route",
                description="Select repository specialists through the neural MoE router.",
                handler=self._tool_route_agents,
                required_arguments=("query",),
            ))

        # ── 4. Cognitive Planner ────────────────────────────────────────────
        self.planner = CognitivePlanner(cluster_engine=self.cluster_engine)

    def agent(self, agent_id: str) -> ControlAgent:
        return make_agent(agent_id, state=self.state)

    async def _tool_knowledge_search(self, query: str) -> Dict[str, Any]:
        if self.omni_search is None:
            raise RuntimeError("knowledge search capability is unavailable")
        response = await self.omni_search.omni_search(str(query))
        return {
            "query": str(query),
            "briefing": response.briefing,
            "merkle_root": response.merkle_root,
            "results": [
                {
                    "url": result.get("url"),
                    "title": result.get("title"),
                    "snippet": result.get("snippet"),
                    "relevance": result.get("score"),
                    "source": result.get("source"),
                }
                for result in response.base_response.results
            ],
        }

    def _tool_route_agents(self, query: str) -> Dict[str, Any]:
        if self.cluster_engine is None:
            raise RuntimeError("specialist routing capability is unavailable")
        decision = self.cluster_engine.route_query(str(query), top_k_agents=6)
        return {
            "query": str(query),
            "primary_cluster_id": decision.primary_cluster_id,
            "cluster_affinity": decision.cluster_affinity,
            "selected_agent_ids": decision.selected_agent_ids,
            "routing_probabilities": decision.agent_routing_probabilities,
            "rationale": decision.rationale,
        }

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

    def _emit(self, event_type: str, case_id: str, payload: Dict[str, Any]) -> None:
        """Emits telemetry event on EventBus."""
        ev = RuntimeEvent(
            event_id=f"EVT-{uuid.uuid4().hex[:8].upper()}",
            event_name=event_type,
            topic="CASE",
            case_id=case_id,
            source="H11AGI_KERNEL",
            payload=payload,
            timestamp=time.time(),
        )
        self.event_bus.emit(ev)

    @staticmethod
    def _as_agent_result(record: SpecialistExecutionRecord) -> AgentResult:
        """Convert an honest specialist execution record into deliberation input."""
        completed = record.status == "COMPLETED"
        confidence = 0.95 if completed else 0.0
        if isinstance(record.output, dict):
            raw_confidence = record.output.get("confidence", record.output.get("confidence_score"))
            if isinstance(raw_confidence, (int, float)):
                confidence = max(0.0, min(1.0, float(raw_confidence)))
        return AgentResult(
            agent_id=record.agent_id,
            canonical_id=record.agent_id,
            success=completed,
            data=record.output,
            confidence=confidence,
            uncertainty=1.0 - confidence,
            latency_ms=record.latency_ms,
            error_message=record.error,
            execution_metadata={
                "status": record.status,
                "input_fields": record.input_fields,
                "missing_inputs": record.missing_inputs,
                "contract_diagnostics": record.contract_diagnostics,
            },
        )

    async def tick(self, case: Dict[str, Any] | CaseEnvelope) -> AGIResult:
        """Executes full 24-step canonical cognitive loop with MoE execution, deliberation, and independent verification."""
        if not self._ready:
            await self.initialize()
        events: List[str] = []
        state_history: List[str] = ["NEW"]

        if hasattr(case, "input_data") and isinstance(case.input_data, dict):
            case = dict(case.input_data)
        elif hasattr(case, "__dict__") and not isinstance(case, dict):
            case = dict(case.__dict__)
        else:
            case = dict(case)
        case_id = case.setdefault("case_id", new_id("case"))
        case.setdefault("patient_id", f"PAT-{case_id}")
        case.setdefault(
            "schema_id",
            "h11.spine.host_infection_case.v1"
            if case.get("symptoms") or case.get("blood_smear_density_per_ul")
            else "h11.spine.cognitive_query.v1",
        )

        # ── Step 1: Initialize Blackboard, WorldModel & Execution Context ───
        board = Blackboard(case_id)
        self.blackboards[case_id] = board
        world = WorldModel(case_id)
        self.world_models[case_id] = world
        case_envelope = CaseEnvelope(
            case_id=case_id,
            principal_id=str(case.get("principal_id") or "SYSTEM_USER"),
            input_data=case,
            objective=str(case.get("goal") or case.get("query") or ""),
        )
        case_obj = Case(envelope=case_envelope)
        case_obj.blackboard = board

        self._emit("CASE_INTAKE", case_id, {"schema_id": case.get("schema_id")})

        # ── Step 2-4: Admission, Identity & Zero-Trust Verification ─────────
        admit = self.agent("H11C-ADMISSION-CONTROL").process({"case": case})
        events.append("admitted" if admit["admitted"] else "denied")
        if not admit["admitted"]:
            state_history.append("REJECTED")
            self._emit("ADMISSION_DENIED", case_id, {"reason": "risk_threshold_exceeded"})
            return AGIResult(
                case_id=case_id,
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
                state_progression=state_history,
            )

        state_history.append("ADMITTED")
        ident = self.agent("H11C-IDENTITY").process({"name": case.get("patient_id") or case_id})
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
            state_history.append("QUARANTINED")
            self.agent("H11C-QUARANTINE").process({})
            self._emit("INJECTION_DETECTED", case_id, {"text": inj_text})
            return AGIResult(
                case_id=case_id,
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
                state_progression=state_history,
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

        state_history.append("CONTEXTUALIZED")
        routed = self.agent("H11C-CROSS-DOMAIN-ROUTER").process({"case": case})
        domain = routed["domain"]
        pipeline_id = routed["pipeline_id"]
        label = self.agent("H11C-DATA-CLASS").process({"payload": case})
        comp = self.agent("H11C-COMPARTMENT").process({"label": label["label"], "sink": domain})
        if not comp["ok"]:
            self.agent("H11C-HALT").process({})
            state_history.append("HALTED")
            return AGIResult(
                case_id=case_id,
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
                state_progression=state_history,
            )

        state_history.append("MAPPED")
        caps = self.agent("H11C-CAPABILITY-MAPPER").process({"goal": domain})
        composed = self.agent("H11C-PIPELINE-COMPOSER").process(
            {"goal": domain, "capabilities": caps["capabilities"]}
        )
        hooked = self.agent("H11C-ALIGN-HOOK").process({"pipeline": composed["pipeline"]})
        self.state.phase = "PERCEIVE"
        self.agent("H11C-COGNITIVE-LOOP").process({"align_allowed": False})
        state_history.append("COMPOSED")

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

                for ev in retrieved_evidence:
                    board.post_evidence(
                        claim=str(ev.get("snippet") or ev.get("title")),
                        source=str(ev.get("url") or "LSE_v3"),
                        confidence=float(ev.get("relevance") or 0.95),
                        provenance=merkle_root_hash or ""
                    )
                    self.evidence_ledger.append(EvidenceItem(
                        claim=str(ev.get("snippet") or ev.get("title")),
                        source=str(ev.get("url") or "LSE_v3"),
                        provenance=merkle_root_hash or "",
                        confidence=float(ev.get("relevance") or 0.95),
                        metadata={"case_id": case_id}
                    ))
            except Exception as exc:
                logger.warning(f"LSE v3.0 retrieval error: {exc}")

        # ── Step 6: TASK DECOMPOSITION, PLANNING & MoE ROUTING ───────────────
        state_history.append("PLANNING")
        plan = self.planner.create_plan(
            goal=query_text or domain,
            retrieved_evidence=retrieved_evidence,
            domain_hint=domain,
        )
        neural_routing_dict = {
            "manifold": plan.primary_cluster_id or domain,
            "cluster_affinity": plan.cluster_affinity,
            "activated_agents": plan.activated_agents,
            "agent_routing_probabilities": plan.routing_probabilities,
            "plan_id": plan.plan_id,
        }
        case["neural_routing"] = neural_routing_dict
        events.append(f"plan_created_{plan.plan_id}")

        # ── Step 6B: BOUNDED OBSERVE-ACT-RECOVER TOOL LOOP ────────────────
        tool_loop_result = None
        tool_planning_result: Optional[AutonomousPlanResult] = None
        autonomous_tools_requested = bool(case.get("auto_tools"))
        raw_tool_plan = case.get("tool_plan")
        tool_expectations = case.get("tool_expectations") or []
        if autonomous_tools_requested and not raw_tool_plan:
            tool_planning_result = self.autonomous_tool_planner.synthesize(query_text, case)
            case["tool_planning"] = tool_planning_result.to_dict()
            events.append(f"autonomous_tool_planning_{tool_planning_result.status.lower()}")
            if tool_planning_result.selected is not None:
                raw_tool_plan = tool_planning_result.selected.plan
                tool_expectations = tool_planning_result.selected.expectations
                case["tool_plan"] = raw_tool_plan
                case["tool_expectations"] = tool_expectations
        if isinstance(raw_tool_plan, list) and raw_tool_plan:
            requested_tool_calls = int(case.get("max_tool_calls") or max(1, len(raw_tool_plan) * 2))
            tool_budget = ResourceBudget(
                max_tool_calls=max(1, min(50, requested_tool_calls)),
                time_budget_sec=float(max(1.0, min(45.0, float(case.get("tool_time_budget_sec") or 10.0)))),
            )
            tool_loop_result = await self.tool_loop.run(
                plan=raw_tool_plan,
                expectations=tool_expectations,
                case_context=case,
                blackboard=board,
                world_model=world,
                evidence_ledger=self.evidence_ledger,
                budget=tool_budget,
            )
            case["tool_results"] = tool_loop_result.outputs
            case["tool_evaluation"] = tool_loop_result.evaluation.to_dict()
            research_output = tool_loop_result.outputs.get("research")
            if isinstance(research_output, dict):
                autonomous_evidence = [
                    item for item in research_output.get("results", []) if isinstance(item, dict)
                ]
                known_urls = {item.get("url") for item in retrieved_evidence}
                for item in autonomous_evidence:
                    if item.get("url") not in known_urls:
                        retrieved_evidence.append(item)
                        known_urls.add(item.get("url"))
                    board.post_evidence(
                        claim=str(item.get("snippet") or item.get("title") or ""),
                        source=str(item.get("url") or "tool://knowledge.search"),
                        confidence=float(item.get("relevance") or 0.9),
                        provenance=str(research_output.get("merkle_root") or ""),
                    )
                case["retrieved_evidence"] = retrieved_evidence
                case["autonomous_research_briefing"] = research_output.get("briefing")
                merkle_root_hash = str(research_output.get("merkle_root") or merkle_root_hash or "") or None
                case["merkle_root"] = merkle_root_hash
                events.append(f"autonomous_research_grounded_{len(autonomous_evidence)}")
            events.append(
                f"tool_loop_{tool_loop_result.status.lower()}_score_{tool_loop_result.evaluation.score:.2f}"
            )

        # ── Step 7: EXECUTION GRAPH ASSEMBLY & REAL SPECIALIST EXECUTION ─────
        state_history.append("EXECUTING")
        exec_graph = self.planner.build_execution_graph(plan, case_id=case_id)
        self.active_graphs[case_id] = exec_graph

        # Execute all routed specialist agents in parallel DAG frontier stages
        graph_results: Dict[str, AgentResult] = await self.graph_executor.execute_graph_async(
            case=case_obj,
            graph=exec_graph,
        )
        specialist_results_list = [r.to_dict() for r in graph_results.values()]
        contributing_agents = [r.agent_id for r in graph_results.values() if r.success]
        events.append(f"executed_{len(graph_results)}_specialists")
        logger.info(f"ExecutionGraph completed: {len(contributing_agents)} active specialists produced AgentResults.")

        # ── Step 8: CROSS-AGENT DELIBERATION LAYER ───────────────────────────
        state_history.append("DELIBERATING")
        synthesis = self.deliberator.deliberate(
            agent_results=list(graph_results.values()),
            query_context=query_text,
        )
        events.append(f"deliberated_consensus_{len(synthesis.consensus_claims)}")

        # ── Step 9: INDEPENDENT VERIFICATION LAYER & REPLANNING ──────────────
        state_history.append("VERIFYING")
        verif_report = self.verifier.verify(
            synthesis=synthesis,
            evidence_ledger=self.evidence_ledger,
        )
        events.append(f"verification_{verif_report.status.lower()}")

        # Recursive Replanning if Verification Fails
        if not verif_report.passed and plan.iteration < plan.max_iterations:
            state_history.append("REPLANNING")
            events.append("replanning_triggered")
            replanned = self.planner.replan(
                current_plan=plan,
                rejection_reasons=verif_report.rejection_reasons,
                replan_actions=verif_report.recommended_replan_actions,
            )
            if replanned:
                plan = replanned
                replan_graph = self.planner.build_execution_graph(plan, case_id=case_id)
                self.active_graphs[case_id] = replan_graph
                replan_records = await self.specialist_executor.execute(
                    selected_agent_ids=plan.activated_agents,
                    metadata=self.cluster_engine.agents if self.cluster_engine else {},
                    case=case,
                    graph=replan_graph,
                    blackboard=board,
                )
                replan_results = {
                    record.agent_id: self._as_agent_result(record) for record in replan_records
                }
                graph_results.update(replan_results)
                specialist_results_list.extend(record.to_dict() for record in replan_records)
                contributing_agents = [r.agent_id for r in graph_results.values() if r.success]
                synthesis = self.deliberator.deliberate(
                    agent_results=list(graph_results.values()),
                    query_context=query_text,
                )
                verif_report = self.verifier.verify(synthesis=synthesis, evidence_ledger=self.evidence_ledger)
                events.append(f"replan_verification_{verif_report.status.lower()}")

        # ── Step 10: HOST SPINE EXECUTION & BLACKBOARD INTEGRATION ───────────
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
            board.post_fact("diagnosis", case.get("diagnosis"), source_agent="H11-PATHOLOGIA")
            board.post_fact("parasite_clearance", case.get("parasite_clearance"), source_agent="H11-PHARMA")
        elif pipeline_id == "cognitive_loop":
            case["blackboard_facts"] = self._board_facts(case.get("patient_id"))
            case["synthesis_candidate"] = synthesis.synthesized_output
            spine_result = await self.cog.run(case)
            allowed = spine_result.allowed
            hops = ["H11C-ADMISSION-CONTROL", "H11C-ZERO-TRUST-HOP"] + spine_result.hops
            case = dict(spine_result.payload)
            events.extend(spine_result.events)
            board.post_fact("reasoning_synthesis", case.get("reason"), source_agent="H11-REASON")
        else:
            allowed = False
            hops = ["H11C-ADMISSION-CONTROL", "H11C-CROSS-DOMAIN-ROUTER", "H11C-ALIGN-HOOK"]

        if tool_loop_result is not None and not tool_loop_result.evaluation.passed:
            allowed = False
            events.append("tool_goal_not_satisfied")
        if autonomous_tools_requested and (tool_planning_result is None or tool_planning_result.selected is None):
            allowed = False
            events.append("autonomous_tool_plan_unavailable")

        state_history.append("INTEGRATING")
        action = str((case.get("reason") or {}).get("action") or synthesis.synthesized_output.get("primary_action") or "REASON")
        would_act = action in ("TREAT", "EXECUTE", "ACT")

        # ── Step 11: NON-BYPASSABLE ALIGN HARD GATE ENFORCEMENT ──────────────
        state_history.append("ALIGNING")
        enforce = self.agent("H11C-ALIGN-ENFORCE").process(
            {
                "trace_id": case.get("case_id"),
                "align_allowed": allowed,
                "would_act": would_act,
            }
        )
        conf = (case.get("diagnosis") or {}).get("confidence_score")
        if conf is None:
            conf = (case.get("reason") or {}).get("overall_confidence") or synthesis.overall_confidence
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
                    "policy": med["decision"] == "allow" and verif_report.policy_compliance,
                }
            }
        )
        if not enforce["ok"] or not licensed["licensed"]:
            self.agent("H11C-HALT").process({})
            state_history.append("HALTED")
        else:
            state_history.append("RELEASED")

        # ── Step 12: CRYPTOGRAPHIC AUDIT SEALING & MERKLE WITNESS ───────────
        self.agent("H11C-MEMORY-PROJECTOR").process({"payload": case})
        audit_event = {
            "case_id": case_id,
            "allowed": allowed,
            "licensed": licensed["licensed"],
            "merkle_root": merkle_root_hash,
            "plan_id": plan.plan_id,
            "contributing_agents": contributing_agents,
        }
        head = self.agent("H11C-AUDIT-CHAIN").process({"event": audit_event})["head"]

        if allowed and licensed["licensed"]:
            try:
                self.agent("H11C-COGNITIVE-LOOP").process({"align_allowed": True})
            except ControlError:
                pass

        # ── Step 13: OBSERVATION & WORLD MODEL CONSOLIDATION ────────────────
        state_history.append("OBSERVING")
        world.add_observation(
            source_agent="H11_DELIBERATOR",
            data={"synthesis": synthesis.deliberation_summary, "contributing_agents": contributing_agents},
        )

        # ── Step 14: MEMORY CONSOLIDATION & H11-LEARN DISTILLATION ─────────
        state_history.append("MEMORIZED")
        self.memory_service.store_episodic(
            content={
                "case_id": case_id,
                "query": query_text,
                "domain": domain,
                "action": action,
                "merkle": merkle_root_hash,
                "allowed": allowed,
                "licensed": bool(licensed["licensed"]),
                "audit_head": head,
                "contributing_agents": contributing_agents,
            },
            importance=0.9
        )

        learning_recorded = False
        if self.collector is not None and allowed:
            try:
                self.collector.record(
                    agent_id=f"H11C-{pipeline_id.upper()}",
                    case_id=case_id,
                    query=query_text,
                    retrieved_docs=retrieved_evidence,
                    output={
                        "action": action,
                        "domain": domain,
                        "allowed": allowed,
                        "merkle": merkle_root_hash,
                        "contributing_agents": contributing_agents,
                    },
                    domain=domain,
                    feedback_score=float(conf) if conf else None,
                )
                learning_recorded = True
                events.append("learning_recorded")
                logger.info(f"H11-LEARN: Experience recorded for case {case_id}")
            except Exception as exc:
                logger.warning(f"H11-LEARN recording error: {exc}")

        state_history.append("CLOSED")
        self._emit("CASE_CLOSED", case_id, {"status": "SUCCESS" if allowed else "HALTED"})

        return AGIResult(
            case_id=case_id,
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
            blackboard_summary={"facts_count": len(board.facts), "evidence_count": len(board.evidence)},
            execution_graph_nodes=len(exec_graph.nodes),
            state_progression=state_history,
            specialist_results=specialist_results_list,
            deliberation={
                "consensus_claims": synthesis.consensus_claims,
                "contradictions": synthesis.contradictions,
                "uncertainty_score": synthesis.uncertainty_score,
                "summary": synthesis.deliberation_summary,
            },
            verification={
                "status": verif_report.status,
                "factual_score": verif_report.factual_support_score,
                "consistency_score": verif_report.logical_consistency_score,
                "policy_compliance": verif_report.policy_compliance,
            },
            cognitive_plan={
                "plan_id": plan.plan_id,
                "iteration": plan.iteration,
                "is_replanned": plan.is_replanned,
                "subgoals_count": len(plan.subgoals),
            },
            contributing_agents=contributing_agents,
            tool_loop=tool_loop_result.to_dict() if tool_loop_result else None,
            tool_planning=tool_planning_result.to_dict() if tool_planning_result else None,
        )

    def get_system_telemetry(self) -> Dict[str, Any]:
        """Returns unified telemetry across all connected layers, agents, LSE, and learn."""
        telemetry = {
            "state_phase": self.state.phase,
            "halted": self.state.halt,
            "indexed_agents_total": len(self.agent_registry.canonical_index),
            "clustering_stats": self.cluster_engine.get_cluster_stats() if self.cluster_engine else None,
            "omni_search_stats": self.omni_search.get_full_stats() if self.omni_search else None,
            "learn_stats": self.collector.stats if self.collector else None,
            "event_bus_handlers": len(self.event_bus.handlers),
            "evidence_ledger_size": len(self.evidence_ledger.items),
            "episodic_memory_count": len(self.memory_service.episodic_store),
        }
        return telemetry
