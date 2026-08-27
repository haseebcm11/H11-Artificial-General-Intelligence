"""Master Agent Registry."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from ..contracts import AgentContract, AgentPillar


@dataclass
class AgentEntry:
    agent_id: str
    class_name: str
    pillar: Any
    layer_or_domain: str
    capabilities: List[str]
    factory: Optional[Callable[[], Any]] = None


class AgentRegistry:
    """05 — AgentRegistry: Master index of all 1,000 agents across H11Z, H11I, and H11C."""

    def __init__(self) -> None:
        self.agents: Dict[str, Any] = {}
        self._populate_standard_contracts()

    def _populate_standard_contracts(self) -> None:
        self.register_agent_contract(
            AgentContract(
                agent_id="H11_QUANTUM",
                class_name="QuantumAgent",
                pillar=AgentPillar.H11Z_COGNITIVE_NETWORK,
                layer_or_domain="L01_physical_substrate",
                input_schema_name="QuantumInput",
                output_schema_name="QuantumOutput",
                capabilities=["QUANTUM_SIMULATION", "HAMILTONIAN_CALC"],
            )
        )
        self.register_agent_contract(
            AgentContract(
                agent_id="H11_MED_GENERAL",
                class_name="MedGeneralAgent",
                pillar=AgentPillar.H11I_INTELLIGENCE_UNIVERSE,
                layer_or_domain="D01_medicine_health",
                input_schema_name="ClinicalInput",
                output_schema_name="ClinicalOutput",
                capabilities=["CLINICAL_TRIAGE", "DIAGNOSTIC_SYNTHESIS"],
            )
        )
        self.register_agent_contract(
            AgentContract(
                agent_id="H11_PHARMA",
                class_name="PharmaAgent",
                pillar=AgentPillar.H11I_INTELLIGENCE_UNIVERSE,
                layer_or_domain="D02_pharmacology",
                input_schema_name="DrugInput",
                output_schema_name="DrugOutput",
                capabilities=["DOSAGE_CALCULATION", "INTERACTION_CHECK"],
            )
        )
        self.register_agent_contract(
            AgentContract(
                agent_id="H11_REASON",
                class_name="ReasonAgent",
                pillar=AgentPillar.H11Z_COGNITIVE_NETWORK,
                layer_or_domain="L13_cognition_reasoning",
                input_schema_name="ReasonInput",
                output_schema_name="ReasonOutput",
                capabilities=["CAUSAL_INFERENCE", "DEDUCTION"],
            )
        )
        self.register_agent_contract(
            AgentContract(
                agent_id="H11C_ALIGN_ENFORCE",
                class_name="AlignEnforceAgent",
                pillar=AgentPillar.H11C_CONTROL_PLANE,
                layer_or_domain="C03_security_integrity",
                input_schema_name="AlignInput",
                output_schema_name="AlignOutput",
                capabilities=["ALIGN_ENFORCEMENT", "POLICY_VERIFY"],
            )
        )

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
        entry = AgentEntry(
            agent_id=agent_id,
            class_name=class_name,
            pillar=pillar,
            layer_or_domain=layer_or_domain,
            capabilities=capabilities,
            factory=factory,
        )
        self.agents[agent_id] = entry
        return entry

    def get_agent(self, agent_id: str) -> Optional[Any]:
        return self.agents.get(agent_id)

    def get_by_pillar(self, pillar: Any) -> List[Any]:
        pillar_val = getattr(pillar, "value", str(pillar))
        return [
            a for a in self.agents.values()
            if getattr(a, "pillar", None) == pillar or getattr(getattr(a, "pillar", None), "value", None) == pillar_val
        ]

    def total_count(self) -> int:
        return len(self.agents)
