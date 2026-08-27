"""General cognitive spine: recall → reason → align → encode.

Used when the case is a query (or goal) rather than a host-infection workup.
Shares LONGTERM with the medical spine so a follow-up can retrieve a prior case.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from .adapters import AlignAdapter, LongtermAdapter, ReasonAdapter
from .envelope import Envelope, SchemaError, hash_embed, new_id
from .spine import SpineResult

COG_SCHEMA_ID = "h11.spine.cognitive_query.v1"


def premises_from_nodes(nodes: List[Dict[str, Any]]) -> List[str]:
    out: List[str] = []
    for node in nodes:
        payload = node.get("payload") or node
        parasite = payload.get("parasite")
        drug = payload.get("drug")
        if parasite:
            out.append(f"Identified parasite is {parasite}.")
        if drug:
            out.append(f"Recommended antiparasitic is {drug}.")
        if payload.get("confidence") is not None:
            out.append(f"Diagnostic confidence is {payload['confidence']}.")
        if payload.get("map_mmhg") is not None:
            out.append(f"Mean arterial pressure is {payload['map_mmhg']} mmHg.")
        text = payload.get("text")
        if text and not parasite:
            out.append(str(text)[:400])
    return out


class CognitiveSpine:
    def __init__(
        self,
        longterm: Optional[LongtermAdapter] = None,
        reason: Optional[ReasonAdapter] = None,
        align: Optional[AlignAdapter] = None,
    ) -> None:
        self.longterm = longterm or LongtermAdapter()
        self.reason = reason or ReasonAdapter()
        self.align = align or AlignAdapter()
        self._ready = False

    async def initialize(self) -> None:
        if self._ready:
            return
        await self.longterm.initialize()
        await self.reason.initialize()
        await self.align.initialize()
        self._ready = True

    async def run(self, case: Dict[str, Any]) -> SpineResult:
        if not self._ready:
            await self.initialize()
        query = str(case.get("query") or case.get("goal") or "").strip()
        if not query:
            raise SchemaError("cognitive spine requires query or goal")
        payload = dict(case)
        payload.setdefault("case_id", new_id("case"))
        patient_id = payload.get("patient_id")

        recalled: List[Dict[str, Any]] = []
        recall_scores: List[float] = []
        if patient_id:
            cue = hash_embed(f"patient:{patient_id}", dim=32)
            hit = self.longterm.retrieve(cue, top_k=3)
            recalled = list(hit.retrieved_nodes)
            recall_scores = list(hit.confidence_scores)
        if not recalled:
            cue = hash_embed(query, dim=32)
            hit = self.longterm.retrieve(cue, top_k=3)
            recalled = list(hit.retrieved_nodes)
            recall_scores = list(hit.confidence_scores)

        premises = list(payload.get("premises") or [])
        premises.extend(premises_from_nodes(recalled))
        for fact in payload.get("blackboard_facts") or []:
            if fact not in premises:
                premises.append(str(fact))
        if not premises:
            premises = [query]

        reasoned = self.reason.infer(query, premises)
        payload["premises"] = premises
        payload["reason"] = reasoned
        payload["recalled"] = recalled
        payload["recall_scores"] = recall_scores

        trace_id = new_id("trace")
        env = Envelope(
            trace_id=trace_id,
            schema_id=COG_SCHEMA_ID,
            from_agent="H11-REASON",
            to_agent="H11-ALIGN",
            payload=payload,
            events=["InferenceComplete"],
        )
        env = await self.align.hop(env)

        answer_text = str((env.payload.get("reason") or {}).get("conclusion") or "")
        embed_src = json.dumps(
            {
                "case_id": env.payload["case_id"],
                "query": query,
                "conclusion": answer_text,
            },
            sort_keys=True,
        )
        self.longterm.encode(
            [
                {
                    "case_id": env.payload["case_id"],
                    "patient_id": patient_id,
                    "text": embed_src,
                    "embedding": hash_embed(embed_src, dim=32),
                    "kind": "qa",
                    "answer": answer_text,
                }
            ]
        )
        if patient_id:
            self.longterm.encode(
                [
                    {
                        "case_id": env.payload["case_id"],
                        "patient_id": patient_id,
                        "text": embed_src,
                        "embedding": hash_embed(f"patient:{patient_id}", dim=32),
                        "kind": "patient_index",
                        "answer": answer_text,
                    }
                ]
            )

        hops = ["H11-LONGTERM", "H11-REASON", "H11-ALIGN"]
        events = list(env.events)
        events.append("memory_consolidated")
        allowed = bool(env.payload.get("alignment", {}).get("allowed"))
        return SpineResult(
            trace_id=trace_id,
            hops=hops,
            envelopes=[env],
            payload=env.payload,
            allowed=allowed,
            events=events,
        )
