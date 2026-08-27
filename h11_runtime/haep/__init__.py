"""H11-AGI Enhancement Protocol v5.0 (HAEP v5.0) Runtime Package.

Governed Autonomous Intelligence Evolution & Self-Optimization Architecture.
"""

from .api import EnhancementEvent, HAEPRuntime
from .canary import CanaryEvaluationResult, CanaryRouter, EnhancementTransaction
from .constitution import ConstitutionViolationError, EvolutionConstitution
from .debt import EvolutionDebtManager
from .engine import ChangeBuilderSubsystem, ValidationSubsystem
from .environment import EnvironmentModel, EnvironmentState
from .genome import ArchitectureDifferential, SystemGenomeManager, TrajectoryPoint
from .governance import EvolutionFreezeActiveError, GovernanceGate
from .guard import EvolutionGuard
from .landscape import CapabilityLandscape, DecomposedCapability, LandscapeCapability
from .ledger import EnhancementLedger, EvolutionaryMemoryGraph, LedgerRecord
from .memory import EvolutionMemoryManager, LineageNode
from .metacognition import MetacognitiveMonitor, MetacognitiveReport
from .observatory import EmergenceObservatory, StabilizedEmergenceRecord
from .optimizer import BottleneckRecord, CompiledIntelligencePathway, SelfOptimizer
from .orchestrator import EvolutionCheckpoint, EvolutionOrchestrator, EvolutionPath
from .protocol import (
    AuthorityLevel,
    AutonomyTier,
    BaselineLock,
    CapabilityStatus,
    DeficiencyType,
    EmergenceClass,
    EmergentCapabilityRecord,
    EnhancementAuthorizationToken,
    EnhancementClass,
    EnhancementObject,
    EnhancementOperation,
    EnhancementState,
    EvolutionCost,
    EvolutionDebt,
    EvolutionHealthScorecard,
    EvolutionPlan,
    EvolutionPrimitive,
    EvolutionState,
    IntelligenceLevel,
    IntelligenceState,
    MemoryClass,
    OptimizationDomain,
    OptimizationRegime,
    PlanningHorizon,
    PortfolioCategory,
    PromotionLevel,
    PromotionVector,
    RecursiveLevel,
    RiskLevel,
    SolutionType,
    SystemState,
    SystemStateVector,
    TriadFitness,
)
from .search import (
    EvolutionPlanner,
    EvolutionSpaceSearch,
    FutureStateCandidate,
    SaturationDetector,
    SynergyAntagonismEvaluator,
)
from .self_model import (
    CapabilityAttributionEngine,
    CapabilityGapEngine,
    CapabilityNode,
    EmergentCapabilityDetector,
    H11SelfModel,
    KnowledgeVsArchitectureDecider,
)
from .society import AgentTelemetry, MinimumSufficientIntelligence, SocietyEcologyTracker

__all__ = [
    "HAEPRuntime",
    "SelfOptimizer",
    "BottleneckRecord",
    "CompiledIntelligencePathway",
    "EnvironmentModel",
    "EnvironmentState",
    "MetacognitiveMonitor",
    "MetacognitiveReport",
    "TriadFitness",
    "IntelligenceState",
    "OptimizationDomain",
    "OptimizationRegime",
    "AuthorityLevel",
    "AutonomyTier",
    "PlanningHorizon",
    "CapabilityStatus",
    "EmergenceClass",
    "MemoryClass",
    "EvolutionState",
    "PromotionLevel",
    "PromotionVector",
    "RiskLevel",
    "RecursiveLevel",
    "SystemState",
    "SystemStateVector",
    "EvolutionCost",
    "EvolutionDebt",
    "EvolutionHealthScorecard",
    "EvolutionPlan",
    "EmergentCapabilityRecord",
    "EvolutionPrimitive",
    "EnhancementAuthorizationToken",
    "BaselineLock",
    "TrajectoryPoint",
    "ArchitectureDifferential",
    "SystemGenomeManager",
    "GovernanceGate",
    "EvolutionFreezeActiveError",
    "EvolutionConstitution",
    "ConstitutionViolationError",
    "EvolutionDebtManager",
    "CapabilityLandscape",
    "LandscapeCapability",
    "DecomposedCapability",
    "EmergenceObservatory",
    "StabilizedEmergenceRecord",
    "EvolutionOrchestrator",
    "EvolutionPath",
    "EvolutionCheckpoint",
    "CanaryRouter",
    "CanaryEvaluationResult",
    "EnhancementTransaction",
    "EnhancementLedger",
    "LedgerRecord",
    "EvolutionaryMemoryGraph",
    "EvolutionMemoryManager",
    "LineageNode",
    "SocietyEcologyTracker",
    "AgentTelemetry",
    "MinimumSufficientIntelligence",
    "H11SelfModel",
    "CapabilityNode",
    "CapabilityGapEngine",
    "KnowledgeVsArchitectureDecider",
    "EmergentCapabilityDetector",
    "CapabilityAttributionEngine",
    "EvolutionSpaceSearch",
    "FutureStateCandidate",
    "EvolutionPlanner",
    "SynergyAntagonismEvaluator",
    "SaturationDetector",
    "EvolutionGuard",
    "ChangeBuilderSubsystem",
    "ValidationSubsystem",
    "EnhancementEvent",
    "EnhancementObject",
    "EnhancementClass",
    "EnhancementOperation",
    "EnhancementState",
    "IntelligenceLevel",
    "SolutionType",
    "DeficiencyType",
    "PortfolioCategory",
]
