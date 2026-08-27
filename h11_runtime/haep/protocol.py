"""H11-AGI Enhancement Protocol v5.0 — Core Data Models & Self-Optimization Architecture.

Operational architecture specification: HAEP v5.0
Owner: H11 Systems
Runtime: h11_runtime/haep
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import time
from typing import Any, Dict, List, Optional, Set, Tuple
import uuid


class OptimizationDomain(str, Enum):
    """Section 8: The Seven V5 Optimization Domains."""
    O1_COGNITIVE = "O1_COGNITIVE"       # Reasoning, planning, inference
    O2_CAPABILITY = "O2_CAPABILITY"     # Domain coverage and task competence
    O3_ARCHITECTURAL = "O3_ARCHITECTURAL" # Agents, layers, dependencies, composition
    O4_RESOURCE = "O4_RESOURCE"         # Compute, memory, latency, energy
    O5_KNOWLEDGE = "O5_KNOWLEDGE"       # Acquisition, retrieval, consolidation
    O6_EVOLUTION = "O6_EVOLUTION"       # Improving the enhancement process
    O7_ADAPTATION = "O7_ADAPTATION"     # Responding to changing environments


class OptimizationRegime(int, Enum):
    """Section 14: The Six Optimization Regimes."""
    REGIME_0_STABLE = 0
    REGIME_1_LOCAL = 1
    REGIME_2_COMPOSITION = 2
    REGIME_3_ARCHITECTURAL = 3
    REGIME_4_DISCOVERY = 4
    REGIME_5_META = 5


class AuthorityLevel(str, Enum):
    """Section 88: The Seven V5 Evolution Authority Levels (A0 to A6)."""
    A0_OBSERVE_ONLY = "A0_OBSERVE_ONLY"
    A1_DIAGNOSE = "A1_DIAGNOSE"
    A2_GENERATE_CANDIDATES = "A2_GENERATE_CANDIDATES"
    A3_SANDBOX_EXECUTION = "A3_SANDBOX_EXECUTION"
    A4_BOUNDED_ADAPTATION = "A4_BOUNDED_ADAPTATION"
    A5_AUTHORIZED_PRODUCTION = "A5_AUTHORIZED_PRODUCTION_EVOLUTION"
    A6_RECURSIVE_EVOLUTION = "A6_RECURSIVE_EVOLUTION"


AutonomyTier = AuthorityLevel


class PlanningHorizon(str, Enum):
    """Section 7: Three planning horizons."""
    H0_IMMEDIATE = "H0_IMMEDIATE"   # Runtime optimization (routing, resource, recovery)
    H1_NEAR_TERM = "H1_NEAR_TERM"   # Near-term improvements (agents, memory, composition)
    H2_STRATEGIC = "H2_STRATEGIC"   # Long-term strategic evolution (new domains, substrates)


class CapabilityStatus(str, Enum):
    """Section 9 & 10: Capability Landscape status mapping."""
    KNOWN_STRONG = "KNOWN_STRONG"
    KNOWN_WEAK = "KNOWN_WEAK"
    UNKNOWN = "UNKNOWN"             # "I don't yet know whether I can do X"
    MISSING = "MISSING"
    EMERGENT = "EMERGENT"
    DEGRADING = "DEGRADING"
    IMPROVING = "IMPROVING"
    SATURATED = "SATURATED"


class EmergenceClass(str, Enum):
    """Section 41: Classification of emergent behaviors."""
    DESIRABLE = "DESIRABLE"
    NEUTRAL = "NEUTRAL"
    UNKNOWN = "UNKNOWN"
    UNDESIRABLE = "UNDESIRABLE"
    DANGEROUS = "DANGEROUS"


class MemoryClass(str, Enum):
    """Section 44: The Four Classes of Evolution Memory."""
    FACT = "FACT_MEMORY"           # What happened
    DECISION = "DECISION_MEMORY"   # Why a decision was made
    CAUSAL = "CAUSAL_MEMORY"       # What caused what
    STRATEGY = "STRATEGY_MEMORY"   # Which strategies work under which conditions


class SolutionType(str, Enum):
    LOCAL = "LOCAL"
    COMPOSITIONAL = "COMPOSITIONAL"
    STRUCTURAL = "STRUCTURAL"
    EVOLUTIONARY = "EVOLUTIONARY"


class PortfolioCategory(str, Enum):
    """Section 31: Enhancement Portfolio categories."""
    CRITICAL_FIX = "CRITICAL_FIX"
    CAPABILITY = "CAPABILITY"
    EFFICIENCY = "EFFICIENCY"
    SECURITY = "SECURITY"
    RELIABILITY = "RELIABILITY"
    ARCHITECTURAL = "ARCHITECTURAL"
    RESEARCH = "RESEARCH"


class DeficiencyType(str, Enum):
    KNOWLEDGE = "KNOWLEDGE"
    REASONING = "REASONING"
    COMPOSITION = "COMPOSITION"
    SUBSTRATE = "SUBSTRATE"


class EnhancementOperation(str, Enum):
    RECONFIGURE = "RECONFIGURE"
    RE_ROUTE = "RE_ROUTE"
    RE_PARAMETERIZE = "RE_PARAMETERIZE"
    RE_PROMPT = "RE_PROMPT"
    RE_TRAIN = "RE_TRAIN"
    RE_RETRIEVE = "RE_RETRIEVE"
    RE_COMPOSE = "RE_COMPOSE"
    RE_ORDER = "RE_ORDER"
    RE_VERIFY = "RE_VERIFY"
    RE_PAIR = "RE_PAIR"
    REPLACE = "REPLACE"
    MERGE = "MERGE"
    SPLIT = "SPLIT"
    ADD = "ADD"
    RETIRE = "RETIRE"


class EnhancementClass(str, Enum):
    CLASS_A_CONFIGURATION = "A_CONFIGURATION"
    CLASS_B_SPECIALIST_BEHAVIOR = "B_SPECIALIST_BEHAVIOR"
    CLASS_C_COMPOSITION = "C_COMPOSITION"
    CLASS_D_COGNITIVE_SUBSTRATE = "D_COGNITIVE_SUBSTRATE"
    CLASS_E_CONTROL_PLANE = "E_CONTROL_PLANE"
    CLASS_F_SAFETY_SECURITY = "F_SAFETY_SECURITY"
    CLASS_G_RECURSIVE_ENHANCEMENT = "G_RECURSIVE_ENHANCEMENT"


class EvolutionState(str, Enum):
    OBSERVED = "OBSERVED"
    MODELED = "MODELED"
    UNDERSTOOD = "UNDERSTOOD"
    DIAGNOSED = "DIAGNOSED"
    EVOLUTION_SEARCH = "EVOLUTION_SEARCH"
    CANDIDATE = "CANDIDATE"
    PREDICTED = "PREDICTED"
    GENERATED = "GENERATED"
    SELECTED = "SELECTED"
    TRANSFORMED = "TRANSFORMED"
    SIMULATED = "SIMULATED"
    BUILT = "BUILT"
    VERIFIED = "VERIFIED"
    GOVERNED = "GOVERNED"
    DEPLOYED = "DEPLOYED"
    CANARY = "CANARY"
    PROMOTED = "PROMOTED"
    MONITORED = "MONITORED"
    LEARNED = "LEARNED"
    RECALIBRATED = "RECALIBRATED"
    NEW_STATE = "NEW_STATE"
    # Exceptional States
    QUARANTINED = "QUARANTINED"
    ROLLED_BACK = "ROLLED_BACK"
    FROZEN = "EVOLUTION_FROZEN"
    DEADLOCKED = "DEADLOCKED"
    SURPRISED = "EVOLUTION_SURPRISE"
    ANOMALOUS = "EVOLUTION_ANOMALY"
    CONFLICTED = "CONFLICTED"
    SUPERSEDED = "SUPERSEDED"


EnhancementState = EvolutionState


class PromotionLevel(str, Enum):
    P0_REJECTED = "P0_REJECTED"
    P1_RETAINED_DEV = "P1_RETAINED_IN_DEVELOPMENT"
    P2_INTERNAL_DEPLOY = "P2_INTERNAL_DEPLOYMENT"
    P3_CANARY = "P3_CANARY"
    P4_PRODUCTION = "P4_PRODUCTION"
    P5_STABLE = "P5_STABLE"


class RiskLevel(str, Enum):
    R0_INFORMATIONAL = "R0_INFORMATIONAL"
    R1_LOW = "R1_LOW"
    R2_SIGNIFICANT = "R2_SIGNIFICANT"
    R3_CRITICAL = "R3_CRITICAL"


class RecursiveLevel(int, Enum):
    LEVEL_1_TASKS = 1
    LEVEL_2_AGENTS = 2
    LEVEL_3_COMPOSITION = 3
    LEVEL_4_ARCHITECTURE = 4
    LEVEL_5_EVOLUTION = 5
    LEVEL_6_META_EVOLUTION = 6

    # Backwards compatibility aliases
    LEVEL_0_ORDINARY = 0
    LEVEL_1_AGENT = 2
    LEVEL_2_COMPOSITION = 3
    LEVEL_3_SUBSTRATE = 4
    LEVEL_4_ENHANCEMENT_ENGINE = 5
    LEVEL_5_RECURSIVE_SELF_IMPROVEMENT = 6


class IntelligenceLevel(int, Enum):
    LEVEL_1_TASK = 1
    LEVEL_2_SYSTEM = 2
    LEVEL_3_EVOLUTION = 3


@dataclass(frozen=True)
class PromotionVector:
    capability: float = 0.0
    generalization: float = 0.0
    reliability: float = 0.0
    safety: float = 1.0
    security: float = 1.0
    observability: float = 1.0
    efficiency: float = 0.0
    complexity: float = 0.0

    def passes_hard_gates(self) -> bool:
        return self.safety >= 0.99 and self.security >= 0.99 and self.reliability >= 0.90

    @property
    def system_tradeoff_score(self) -> float:
        benefit = (self.capability * 0.35 + self.generalization * 0.25 + self.reliability * 0.25 + self.efficiency * 0.15)
        cost_penalty = 1.0 + (self.complexity * 0.5)
        return benefit / cost_penalty


@dataclass
class IntelligenceState:
    """Section 5: H11 11-Dimensional Intelligence State Vector I(t)."""
    capabilities_score: float = 0.96
    generalization_score: float = 0.94
    reliability_score: float = 0.98
    efficiency_score: float = 0.92
    knowledge_score: float = 0.95
    memory_score: float = 0.96
    resilience_score: float = 0.97
    security_score: float = 1.0
    safety_score: float = 1.0
    governance_score: float = 1.0
    adaptability_score: float = 0.93
    uncertainty: float = 0.04

    @property
    def vector(self) -> List[float]:
        return [
            self.capabilities_score,
            self.generalization_score,
            self.reliability_score,
            self.efficiency_score,
            self.knowledge_score,
            self.memory_score,
            self.resilience_score,
            self.security_score,
            self.safety_score,
            self.governance_score,
            self.adaptability_score,
        ]


@dataclass
class TriadFitness:
    """Section 109-111: Architectural, Intelligence, & Evolution Fitness."""
    architectural_fitness: float = 0.95
    intelligence_fitness: float = 0.97
    evolution_fitness: float = 0.98


@dataclass
class EvolutionDebt:
    """Section 31: Evolution Debt Tracking."""
    technical_debt: float = 0.0
    architectural_debt: float = 0.0
    capability_debt: float = 0.0
    security_debt: float = 0.0
    governance_debt: float = 0.0
    observability_debt: float = 0.0

    @property
    def total_debt(self) -> float:
        return sum([
            self.technical_debt,
            self.architectural_debt,
            self.capability_debt,
            self.security_debt,
            self.governance_debt,
            self.observability_debt,
        ])


@dataclass
class EvolutionHealthScorecard:
    """Section 78: 12-Dimensional Evolution Health Scorecard."""
    capability_score: float = 0.96
    generalization_score: float = 0.94
    reliability_score: float = 0.98
    safety_score: float = 1.0
    security_score: float = 1.0
    efficiency_score: float = 0.92
    complexity_score: float = 0.15
    evolution_debt_score: float = 0.05
    prediction_error_score: float = 0.02
    evolution_stability_score: float = 0.99
    emergence_health_score: float = 0.95
    architectural_drift_score: float = 0.0


@dataclass
class SystemStateVector:
    """Section 2: S(t) = [A, C, K, M, P, G, R, Z, E]."""
    architecture: str = "THREE_PILLARS_1000_AGENTS"
    capabilities: Set[str] = field(default_factory=set)
    knowledge_version: str = "1.0.0"
    memory_state: str = "CONSOLIDATED"
    policies: List[str] = field(default_factory=lambda: ["ALIGN_V1", "ZERO_TRUST_HOP", "SCHEMA_FIREWALL"])
    governance_state: str = "ACTIVE_GOVERNED"
    runtime_state: str = "OPTIMAL"
    security_state: str = "SECURE"
    evolutionary_state: str = "STABLE"


@dataclass
class SystemState:
    """Section 2: Complete System State S(t)."""
    state_id: str = field(default_factory=lambda: f"S-{uuid.uuid4().hex[:8].upper()}")
    version: str = "1.0.0"
    vector: SystemStateVector = field(default_factory=SystemStateVector)
    intelligence_state: IntelligenceState = field(default_factory=IntelligenceState)
    fitness: TriadFitness = field(default_factory=TriadFitness)
    genome_hash: str = ""
    active_agent_count: int = 1000
    pillars: Dict[str, int] = field(default_factory=lambda: {
        "H11Z_COGNITIVE_NETWORK": 400,
        "H11I_INTELLIGENCE_UNIVERSE": 475,
        "H11C_CONTROL_PLANE": 125,
    })
    created_at: float = field(default_factory=time.time)
    parent_state_id: Optional[str] = None
    lineage_depth: int = 0


@dataclass
class EvolutionCost:
    """Section 16: Evolution Cost representation."""
    implementation_effort: float = 0.1
    compute_cost: float = 0.1
    latency_penalty: float = 0.0
    risk_score: float = 0.1
    complexity_delta: float = 0.05
    migration_difficulty: float = 0.0
    disruption_score: float = 0.0

    @property
    def total_cost(self) -> float:
        return (
            self.implementation_effort * 0.2 +
            self.compute_cost * 0.2 +
            self.latency_penalty * 0.15 +
            self.risk_score * 0.25 +
            self.complexity_delta * 0.1 +
            self.disruption_score * 0.1
        )


@dataclass
class EvolutionPlan:
    """Section 10 & 11: Multi-step Evolution Plan with topological ordering."""
    plan_id: str = field(default_factory=lambda: f"PLAN-{uuid.uuid4().hex[:6].upper()}")
    objective: str = ""
    current_state_id: str = ""
    target_state_id: str = ""
    ordered_transitions: List[str] = field(default_factory=list)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    estimated_cost: EvolutionCost = field(default_factory=EvolutionCost)
    expected_value: float = 0.0
    rollback_path: List[str] = field(default_factory=list)
    governance_requirements: List[str] = field(default_factory=list)


@dataclass
class EmergentCapabilityRecord:
    """Section 18: Emergent capability detected from multi-specialist composition."""
    capability_id: str = field(default_factory=lambda: f"EMERG-{uuid.uuid4().hex[:6].upper()}")
    name: str = ""
    originating_specialists: List[str] = field(default_factory=list)
    composition_topology: str = ""
    triggering_task_class: str = ""
    observed_behavior: str = ""
    reliability_score: float = 0.95
    reproducibility: bool = True
    discovered_at: float = field(default_factory=time.time)


@dataclass
class EvolutionPrimitive:
    """Section 45: Reusable generalized architectural primitive."""
    primitive_id: str
    name: str
    category: str
    applicable_domains: List[str]
    implementation_template: str
    historical_success_rate: float = 1.0


class InteractionEffect(str, Enum):
    INDEPENDENT = "INDEPENDENT"
    CONFLICT = "ENHANCEMENT_CONFLICT"
    SYNERGY = "ENHANCEMENT_SYNERGY"
    ANTAGONISM = "ENHANCEMENT_ANTAGONISM"


@dataclass
class BaselineLock:
    baseline_id: str = field(default_factory=lambda: f"BASE-{uuid.uuid4().hex[:8]}")
    system_state: SystemState = field(default_factory=SystemState)
    locked_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnhancementAuthorizationToken:
    token_id: str = field(default_factory=lambda: f"AUTH-{uuid.uuid4().hex[:12].upper()}")
    enhancement_id: str = ""
    target: str = ""
    risk: RiskLevel = RiskLevel.R1_LOW
    recursive_level: RecursiveLevel = RecursiveLevel.LEVEL_2_AGENTS
    authority_level: AuthorityLevel = AuthorityLevel.A4_BOUNDED_ADAPTATION
    scope: List[str] = field(default_factory=list)
    authority: str = "H11C_CONTROL_PLANE"
    approved_version: str = "1.0.0"
    expiration: float = field(default_factory=lambda: time.time() + 86400.0)
    rollback_reference: str = ""
    is_revoked: bool = False

    def is_valid(self) -> bool:
        return not self.is_revoked and time.time() < self.expiration


@dataclass
class EnhancementObject:
    """Section 82: V5 Evolution Transition Object."""
    enhancement_id: str = field(default_factory=lambda: f"H11-ENH-{uuid.uuid4().hex[:8].upper()}")
    parent_version: str = "1.0.0"
    target: str = ""
    operation: EnhancementOperation = EnhancementOperation.REPLACE
    change_type: EnhancementClass = EnhancementClass.CLASS_B_SPECIALIST_BEHAVIOR
    domain: OptimizationDomain = OptimizationDomain.O2_CAPABILITY
    regime: OptimizationRegime = OptimizationRegime.REGIME_1_LOCAL
    solution_type: SolutionType = SolutionType.LOCAL
    deficiency_type: DeficiencyType = DeficiencyType.REASONING
    portfolio_category: PortfolioCategory = PortfolioCategory.CAPABILITY
    horizon: PlanningHorizon = PlanningHorizon.H1_NEAR_TERM
    authority_level: AuthorityLevel = AuthorityLevel.A4_BOUNDED_ADAPTATION
    recursive_level: RecursiveLevel = RecursiveLevel.LEVEL_2_AGENTS
    origin: str = "L21_SELF_DIAGNOSIS"
    problem: str = ""
    objective: str = ""
    hypothesis: str = ""
    affected_agents: List[str] = field(default_factory=list)
    affected_layers: List[str] = field(default_factory=list)
    affected_domains: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    risk_class: RiskLevel = RiskLevel.R1_LOW
    proposed_change: str = ""
    expected_effect: str = ""
    status: EvolutionState = EvolutionState.OBSERVED
    promotion_level: PromotionLevel = PromotionLevel.P1_RETAINED_DEV
    vector: PromotionVector = field(default_factory=PromotionVector)
    cost: EvolutionCost = field(default_factory=EvolutionCost)
    evolution_value: float = 0.0
    auth_token: Optional[EnhancementAuthorizationToken] = None
    baseline_lock: Optional[BaselineLock] = None
    predicted_outcome: float = 0.95
    observed_outcome: float = 0.0
    created_at: float = field(default_factory=time.time)
    created_by: str = "L21_ENHANCEMENT_ENGINE"
    history: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def prediction_error(self) -> float:
        if self.observed_outcome == 0.0:
            return 0.0
        return round(self.observed_outcome - self.predicted_outcome, 4)

    @property
    def capability_density(self) -> float:
        """Section 35: Capability Density = useful capability / complexity."""
        complexity = max(self.vector.complexity, 0.05)
        return round(self.vector.capability / complexity, 3)

    @property
    def evolution_efficiency(self) -> float:
        """Section 36: Evolution Efficiency = validated delta / total cost."""
        cost = max(self.cost.total_cost, 0.01)
        return round(self.vector.system_tradeoff_score / cost, 3)

    def transition_to(self, new_state: EvolutionState, reason: str = "") -> None:
        self.history.append({
            "from_state": self.status.value,
            "to_state": new_state.value,
            "timestamp": time.time(),
            "reason": reason,
        })
        self.status = new_state
