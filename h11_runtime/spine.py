"""Host-infection composition spine.

This is the enabling embodiment: a typed case crosses six agents that do not
share a package, via a common envelope and per-hop schema checks.

ANATOMIA → PARASITOLOGIA → PHYSIOLOGIA → LONGTERM → REASON → ALIGN
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .adapters import (
    GOAL_BY_SPECIES,
    SPECIES_PATH,
    AlignAdapter,
    AnatomyAdapter,
    LongtermAdapter,
    ParasitologiaAdapter,
    PhysiologiaAdapter,
    ReasonAdapter,
)
from .envelope import (
    SPINE_SCHEMA_ID,
    Envelope,
    SchemaError,
    new_id,
    validate_case,
)

HOPS = (
    "H11-ANATOMIA",
    "H11-PARASITOLOGIA",
    "H11-PHYSIOLOGIA",
    "H11-LONGTERM",
    "H11-REASON",
    "H11-ALIGN",
)


@dataclass
class SpineResult:
    trace_id: str
    hops: List[str]
    envelopes: List[Envelope]
    payload: Dict[str, Any]
    allowed: bool
    events: List[str] = field(default_factory=list)


class HostInfectionSpine:
    def __init__(self, longterm=None, reason=None, align=None) -> None:
        self.anatomy = AnatomyAdapter()
        self.parasitologia = ParasitologiaAdapter()
        self.physiologia = PhysiologiaAdapter()
        self.longterm = longterm or LongtermAdapter()
        self.reason = reason or ReasonAdapter()
        self.align = align or AlignAdapter()
        self._ready = False

    async def initialize(self) -> None:
        await self.anatomy.initialize()
        await self.parasitologia.initialize()
        await self.physiologia.initialize()
        await self.longterm.initialize()
        await self.reason.initialize()
        await self.align.initialize()
        self._ready = True

    async def run(self, case: Dict[str, Any]) -> SpineResult:
        if not self._ready:
            await self.initialize()
        payload = dict(case)
        payload.setdefault("case_id", new_id("case"))
        payload.setdefault("entry_compartment", "skin")
        payload.setdefault("blood_smear_density_per_ul", None)
        payload.setdefault("stool_egg_count_epg", None)
        validate_case(payload)

        # Provisional goal from lab pattern so anatomy can pathfind *before* diagnosis.
        # Parasitologia then confirms species; path is recomputed if the goal changes.
        if (payload.get("blood_smear_density_per_ul") or 0) > 1000 and any(
            "fever" in s.lower() for s in payload["symptoms"]
        ):
            payload["goal_compartment"] = "bloodstream"
            payload["species_path"] = list(SPECIES_PATH["Plasmodium falciparum"])
        elif payload.get("stool_egg_count_epg"):
            payload["goal_compartment"] = "liver"
            payload["species_path"] = list(SPECIES_PATH["Schistosoma mansoni"])
        else:
            payload["goal_compartment"] = "gi_lumen"
            payload["species_path"] = list(SPECIES_PATH["Giardia duodenalis"])

        trace_id = new_id("trace")
        env = Envelope(
            trace_id=trace_id,
            schema_id=SPINE_SCHEMA_ID,
            from_agent="CASE",
            to_agent="H11-ANATOMIA",
            payload=payload,
        )
        envelopes = [env]
        env = await self.anatomy.hop(env)
        envelopes.append(env)
        env = await self.parasitologia.hop(env)
        envelopes.append(env)

        species = env.payload["diagnosis"]["identified_parasite"]
        confirmed = list(SPECIES_PATH.get(species, ()))
        if confirmed and env.payload.get("migration_path") != confirmed:
            env.payload["species_path"] = confirmed
            env.payload["entry_compartment"] = confirmed[0]
            env.payload["goal_compartment"] = GOAL_BY_SPECIES.get(species, confirmed[-1])
            env = await self.anatomy.hop(env)
            envelopes.append(env)

        env = await self.physiologia.hop(env)
        envelopes.append(env)
        env = await self.longterm.hop(env)
        envelopes.append(env)
        env = await self.reason.hop(env)
        envelopes.append(env)
        env = await self.align.hop(env)
        envelopes.append(env)

        events: List[str] = []
        for hop in envelopes:
            events.extend(hop.events)

        allowed = bool(env.payload.get("alignment", {}).get("allowed"))
        hops = [e.from_agent for e in envelopes if e.from_agent != "CASE"]
        return SpineResult(
            trace_id=trace_id,
            hops=hops,
            envelopes=envelopes,
            payload=env.payload,
            allowed=allowed,
            events=events,
        )


def assert_crossed(result: SpineResult) -> None:
    """Fail loudly if the case did not actually compose."""
    payload = result.payload
    for key in ("migration_path", "diagnosis", "vitals", "recalled", "reason", "alignment"):
        if key not in payload:
            raise SchemaError(f"spine did not produce {key}")
    if not payload["recalled"]:
        raise SchemaError("LONGTERM encode/retrieve did not round-trip")
    recalled_case = payload["recalled"][0]["payload"]["case_id"]
    if recalled_case != payload["case_id"]:
        raise SchemaError("recalled memory is a different case")
    conclusion = payload["reason"].get("conclusion", "")
    parasite = payload["diagnosis"]["identified_parasite"]
    if parasite not in conclusion and parasite not in " ".join(payload.get("premises") or []):
        raise SchemaError("REASON did not consume diagnosis premises")
    if "H11-ALIGN" not in result.hops:
        raise SchemaError("ALIGN hop missing")
