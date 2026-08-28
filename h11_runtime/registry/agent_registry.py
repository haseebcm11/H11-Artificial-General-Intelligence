"""Master Agent Registry Indexing All 1,000 Agents across H11Z, H11I, and H11C."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from ..contracts.agent_contract import AgentContract, AgentPillar
from ..loader import AgentIdentity, discover_all_agents, load_agent, LoadedAgentInterface


@dataclass
class AgentEntry:
    agent_id: str
    canonical_id: str
    class_name: str
    pillar: Any
    layer_or_domain: str
    capabilities: List[str]
    relative_path: str = ""
    reliability_score: float = 0.98
    dependencies: List[str] = field(default_factory=list)
    factory: Optional[Callable[[], Any]] = None


class AgentRegistry:
    """05 — AgentRegistry: Master index of all 1,000 agents across H11Z, H11I, and H11C (v3.0 Section 18)."""

    def __init__(self, auto_discover: bool = True) -> None:
        self.agents: Dict[str, Any] = {}
        self.canonical_index: Dict[str, AgentEntry] = {}
        self.capability_index: Dict[str, Set[str]] = {}
        if auto_discover:
            self._discover_and_register_all()
        self._register_compatibility_contracts()

    def _register_compatibility_contracts(self) -> None:
        """Preserve the stable v1 public IDs while canonical discovery evolves."""
        contracts = [
            AgentContract(
                agent_id="H11_QUANTUM",
                class_name="QuantumAgent",
                pillar=AgentPillar.H11Z_COGNITIVE_NETWORK,
                layer_or_domain="L01_physical_substrate",
                input_schema_name="QuantumInput",
                output_schema_name="QuantumOutput",
                capabilities=["QUANTUM_SIMULATION", "HAMILTONIAN_CALC"],
            ),
            AgentContract(
                agent_id="H11_MED_GENERAL",
                class_name="MedGeneralAgent",
                pillar=AgentPillar.H11I_INTELLIGENCE_UNIVERSE,
                layer_or_domain="D01_medicine_health",
                input_schema_name="ClinicalInput",
                output_schema_name="ClinicalOutput",
                capabilities=["CLINICAL_TRIAGE", "DIAGNOSTIC_SYNTHESIS"],
            ),
            AgentContract(
                agent_id="H11_PHARMA",
                class_name="PharmaAgent",
                pillar=AgentPillar.H11I_INTELLIGENCE_UNIVERSE,
                layer_or_domain="D02_pharmacology",
                input_schema_name="DrugInput",
                output_schema_name="DrugOutput",
                capabilities=["DOSAGE_CALCULATION", "INTERACTION_CHECK"],
            ),
            AgentContract(
                agent_id="H11_REASON",
                class_name="ReasonAgent",
                pillar=AgentPillar.H11Z_COGNITIVE_NETWORK,
                layer_or_domain="L13_cognition_reasoning",
                input_schema_name="ReasonInput",
                output_schema_name="ReasonOutput",
                capabilities=["CAUSAL_INFERENCE", "DEDUCTION"],
            ),
            AgentContract(
                agent_id="H11C_ALIGN_ENFORCE",
                class_name="AlignEnforceAgent",
                pillar=AgentPillar.H11C_CONTROL_PLANE,
                layer_or_domain="C03_security_integrity",
                input_schema_name="AlignInput",
                output_schema_name="AlignOutput",
                capabilities=["ALIGN_ENFORCEMENT", "POLICY_VERIFY"],
            ),
        ]
        for contract in contracts:
            self.register_agent_contract(contract)
            for capability in contract.capabilities:
                self.capability_index.setdefault(capability.upper(), set()).add(contract.agent_id)

    def _discover_and_register_all(self) -> None:
        """Populates registry directly from canonical loader catalog."""
        catalog = discover_all_agents()
        for canonical_id, ident in catalog.items():
            pillar_enum = AgentPillar.H11Z_COGNITIVE_NETWORK
            if ident.pillar == "H11I":
                pillar_enum = AgentPillar.H11I_INTELLIGENCE_UNIVERSE
            elif ident.pillar == "H11C":
                pillar_enum = AgentPillar.H11C_CONTROL_PLANE

            entry = AgentEntry(
                agent_id=ident.agent_id,
                canonical_id=canonical_id,
                class_name=ident.class_name,
                pillar=pillar_enum,
                layer_or_domain=ident.layer_or_domain,
                capabilities=ident.capabilities,
                relative_path=ident.relative_path,
                reliability_score=ident.reliability_score,
                dependencies=ident.dependencies,
            )
            # Index by short agent_id, canonical_id, and path
            self.agents[ident.agent_id] = entry
            self.agents[canonical_id] = entry
            self.canonical_index[canonical_id] = entry

            for cap in ident.capabilities:
                cap_key = cap.upper()
                if cap_key not in self.capability_index:
                    self.capability_index[cap_key] = set()
                self.capability_index[cap_key].add(canonical_id)

    def register_agent_contract(self, contract: AgentContract) -> None:
        self.agents[contract.agent_id] = contract

    def register_agent(
        self,
        agent_id: str,
        class_name: str,
        pillar: Any,
        layer_or_domain: str,
        capabilities: List[str],
        factory: Optional[Callable[[], Any]] = None,
    ) -> AgentEntry:
        canonical_id = f"{pillar}:{layer_or_domain}:{agent_id}"
        entry = AgentEntry(
            agent_id=agent_id,
            canonical_id=canonical_id,
            class_name=class_name,
            pillar=pillar,
            layer_or_domain=layer_or_domain,
            capabilities=capabilities,
            factory=factory,
        )
        self.agents[agent_id] = entry
        self.agents[canonical_id] = entry
        self.canonical_index[canonical_id] = entry
        return entry

    def get_agent(self, agent_identifier: str) -> Optional[Any]:
        return self.agents.get(agent_identifier)

    def load(self, agent_identifier: str) -> LoadedAgentInterface:
        """Loads and instantiates agent by ID or canonical identity."""
        return load_agent(agent_identifier)

    def get_by_capability(self, capability: str) -> List[AgentEntry]:
        identifiers = self.capability_index.get(capability.upper(), set())
        return [self.agents[identifier] for identifier in identifiers if identifier in self.agents]

    def get_by_pillar(self, pillar: Any) -> List[Any]:
        pillar_val = getattr(pillar, "value", str(pillar))
        return [
            a for a in self.canonical_index.values()
            if getattr(a, "pillar", None) == pillar or getattr(getattr(a, "pillar", None), "value", None) == pillar_val
        ]

    def total_count(self) -> int:
        return len(self.canonical_index) if self.canonical_index else len(self.agents)
