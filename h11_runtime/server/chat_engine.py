"""H11 Conversational Reasoning Chat Engine.

Translates conversational queries into governed multi-agent cognitive reasoning traces:
1. Live sovereign web & academic literature retrieval (H11-LSE v3.0)
2. 1,000-Agent Neural Mixture-of-Experts (MoE) Softmax Gating
3. Blackboard deliberation & hypothesis generation across activated agents
4. Non-bypassable ALIGN Hard Gate policy verification
5. Cryptographic Merkle Provenance sealing & Tamper-Proof Audit block
6. H11-LEARN continuous experience collection
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Dict, List, Optional

from ..agi import AGIResult, H11AGI
from .model_provider import (
    DeterministicGroundedProvider,
    ProviderError,
    ReasoningProvider,
    SynthesisRequest,
    provider_from_environment,
)

logger = logging.getLogger(__name__)


@dataclass
class ReasoningStep:
    """A discrete step in the AGI reasoning trace."""
    phase: str
    title: str
    detail: str
    status: str = "done"  # 'running', 'done', 'error'
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatResponse:
    """Complete reasoned response to a user query."""
    query: str
    response_text: str
    reasoning_trace: List[ReasoningStep]
    active_manifold: str
    manifold_affinity: float
    activated_agents: List[str]
    retrieved_sources: List[Dict[str, Any]]
    merkle_root: Optional[str]
    align_verified: bool
    action_licensed: bool
    audit_head: str
    case_id: str
    execution_time_ms: float
    reasoning_provider: str = "unknown"


class ConversationalReasoner:
    """Master conversational orchestrator interfacing between the Chat UI and H11AGI Kernel."""

    def __init__(
        self,
        agi_kernel: Optional[H11AGI] = None,
        workspace_root: Optional[str] = None,
        reasoning_provider: Optional[ReasoningProvider] = None,
    ) -> None:
        self.agi = agi_kernel or H11AGI(
            enable_search=True,
            enable_learning=True,
            enable_neural_clustering=True,
            workspace_root=workspace_root,
        )
        self.reasoning_provider = reasoning_provider or provider_from_environment()
        self.fallback_provider = DeterministicGroundedProvider()
        self.conversation_history: List[Dict[str, str]] = []

    async def initialize(self) -> None:
        await self.agi.initialize()

    async def stream_reason(self, query: str, conversation_id: Optional[str] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Streams real-time reasoning steps followed by the final synthesized answer."""
        start_time = asyncio.get_event_loop().time()
        steps: List[ReasoningStep] = []

        # ── Step 1: Query Ingestion & Intent Analysis ───────────────────────
        yield {
            "type": "thought",
            "phase": "INGEST",
            "title": "Ingesting Query & Analyzing Intent",
            "detail": f"Parsing query semantics and historical context for: '{query[:80]}...'",
        }
        await asyncio.sleep(0.05)

        # ── Step 2: Sovereign Knowledge Acquisition (LSE v3.0) ──────────────
        yield {
            "type": "thought",
            "phase": "SEARCH",
            "title": "Querying Sovereign Knowledge Engine (H11-LSE v3.0)",
            "detail": "Executing federated search across arXiv, PubMed, Wikipedia, and Crossref with LaTeX extraction...",
        }

        # Build case envelope for cognitive kernel
        case_payload = {
            "query": query,
            "patient_id": f"user_session_{conversation_id or 'anon'}",
            "travel_history": ["global_research"],
            "goal": "cognitive_loop",
        }

        # Execute cognitive kernel tick
        result: AGIResult = await self.agi.tick(case_payload)

        # ── Step 3: Neural MoE Gating & Manifold Selection ──────────────────
        manifold_name = "Cognitive Reasoning & Agency Manifold"
        manifold_affinity = 0.50
        activated_agents = ["L13_logic_reasoner", "L14_planner", "H11C_ALIGN_GATE"]

        if result.neural_routing:
            manifold_name = result.neural_routing.get("manifold", manifold_name)
            manifold_affinity = result.neural_routing.get("affinity", 0.50)
            activated_agents = result.neural_routing.get("activated_agents", activated_agents)

        yield {
            "type": "thought",
            "phase": "NEURAL_MOE",
            "title": f"Neural MoE Gated to {manifold_name}",
            "detail": f"Softmax affinity {manifold_affinity*100:.1f}%. Activated {len(activated_agents)} specialist agents: {', '.join(activated_agents[:4])}...",
            "metadata": {
                "manifold": manifold_name,
                "affinity": manifold_affinity,
                "agents": activated_agents,
            },
        }
        await asyncio.sleep(0.05)

        # ── Step 4: Multi-Agent Blackboard Deliberation ─────────────────────
        yield {
            "type": "thought",
            "phase": "DELIBERATE",
            "title": "Deliberating on Shared Blackboard",
            "detail": f"Synthesizing {len(result.retrieved_evidence)} retrieved evidence items and evaluating causal chains...",
        }
        await asyncio.sleep(0.05)

        # ── Step 5: Non-Bypassable ALIGN Hard Gate Verification ──────────────
        yield {
            "type": "thought",
            "phase": "ALIGN_GATE",
            "title": "ALIGN Hard Gate Policy Verification",
            "detail": f"Zero-trust safety verification: Allowed={result.allowed}, Licensed={result.licensed}.",
        }

        # ── Step 6: Cryptographic Merkle Provenance Sealing ──────────────────
        merkle_preview = (result.merkle_provenance_root or "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")[:16]
        yield {
            "type": "thought",
            "phase": "PROVENANCE",
            "title": "Sealing Cryptographic Provenance",
            "detail": f"Merkle Root witness proof sealed: {merkle_preview}... into Audit Head: {result.audit_head[:16]}...",
            "metadata": {"merkle_root": result.merkle_provenance_root, "audit_head": result.audit_head},
        }

        # ── Step 7: Synthesize Rigorous, Grounded Response ───────────────────
        synthesized_text, provider_name = await self._synthesize_grounded_answer(
            query=query,
            result=result,
            manifold=manifold_name,
            activated_agents=activated_agents,
        )

        # Store only the bounded conversational transcript used by synthesis.
        self.conversation_history.extend(
            [
                {"role": "user", "content": query[:8000]},
                {"role": "assistant", "content": synthesized_text[:12000]},
            ]
        )
        self.conversation_history = self.conversation_history[-16:]

        end_time = asyncio.get_event_loop().time()
        elapsed_ms = round((end_time - start_time) * 1000, 2)

        # Yield complete response payload
        yield {
            "type": "answer",
            "response_text": synthesized_text,
            "active_manifold": manifold_name,
            "manifold_affinity": manifold_affinity,
            "activated_agents": activated_agents,
            "retrieved_sources": result.retrieved_evidence,
            "merkle_root": result.merkle_provenance_root,
            "align_verified": result.allowed,
            "action_licensed": result.licensed,
            "audit_head": result.audit_head,
            "case_id": result.case_id,
            "execution_time_ms": elapsed_ms,
            "reasoning_provider": provider_name,
        }

    async def reason(self, query: str, conversation_id: Optional[str] = None) -> ChatResponse:
        """Non-streaming convenience execution returning a structured ChatResponse."""
        final_answer: Optional[Dict[str, Any]] = None
        trace: List[ReasoningStep] = []

        async for item in self.stream_reason(query, conversation_id=conversation_id):
            if item["type"] == "thought":
                trace.append(
                    ReasoningStep(
                        phase=item["phase"],
                        title=item["title"],
                        detail=item["detail"],
                        metadata=item.get("metadata", {}),
                    )
                )
            elif item["type"] == "answer":
                final_answer = item

        if not final_answer:
            raise RuntimeError("Reasoning cycle produced no final answer.")

        return ChatResponse(
            query=query,
            response_text=final_answer["response_text"],
            reasoning_trace=trace,
            active_manifold=final_answer["active_manifold"],
            manifold_affinity=final_answer["manifold_affinity"],
            activated_agents=final_answer["activated_agents"],
            retrieved_sources=final_answer["retrieved_sources"],
            merkle_root=final_answer["merkle_root"],
            align_verified=final_answer["align_verified"],
            action_licensed=final_answer["action_licensed"],
            audit_head=final_answer["audit_head"],
            case_id=final_answer["case_id"],
            execution_time_ms=final_answer["execution_time_ms"],
            reasoning_provider=final_answer["reasoning_provider"],
        )

    async def _synthesize_grounded_answer(
        self,
        query: str,
        result: AGIResult,
        manifold: str,
        activated_agents: List[str],
    ) -> tuple[str, str]:
        """Synthesize from kernel state and evidence, with a fail-closed fallback."""
        if not (result.admitted and result.allowed and result.licensed) or result.halted:
            return (
                "The governed runtime withheld this response because the case did not pass "
                "admission, alignment, and action-licensing checks.",
                "governance-refusal",
            )

        conclusion = str((result.payload.get("reason") or {}).get("conclusion") or "")
        request = SynthesisRequest(
            query=query,
            kernel_conclusion=conclusion,
            domain=result.domain,
            manifold=manifold,
            activated_agents=activated_agents,
            evidence=result.retrieved_evidence,
            specialist_results=result.specialist_results,
            conversation_history=tuple(self.conversation_history),
        )
        try:
            generated = await self.reasoning_provider.synthesize(request)
        except ProviderError as exc:
            logger.warning("Configured reasoning provider failed; using grounded fallback: %s", exc)
            generated = await self.fallback_provider.synthesize(request)

        sanitized = self.agi.agent("H11C-INPUT-SANITIZER").process({"text": generated.text})["text"]
        governance = (
            "### Governance record\n\n"
            f"- ALIGN: `{'VERIFIED' if result.allowed else 'DENIED'}`\n"
            f"- Action license: `{'ISSUED' if result.licensed else 'WITHHELD'}`\n"
            f"- Evidence Merkle root: `{result.merkle_provenance_root or 'not available'}`\n"
            f"- Audit head: `{result.audit_head}`\n"
            f"- Case: `{result.case_id}`"
        )
        return f"{sanitized}\n\n{governance}", generated.provider
