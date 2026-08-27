"""H11 Intelligent Neural Agent Clustering & MoE Routing Subsystem.

Provides neural graph embeddings, functional cognitive manifold clustering,
and Mixture-of-Experts (MoE) softmax gating across all 1,000 agents in H11-AGI.
"""
from __future__ import annotations

from .neural_cluster_engine import (
    AgentMetadata,
    CognitiveManifoldCluster,
    NeuralAgentClusterEngine,
    NeuralRoutingDecision,
)

__all__ = [
    "AgentMetadata",
    "CognitiveManifoldCluster",
    "NeuralAgentClusterEngine",
    "NeuralRoutingDecision",
]
