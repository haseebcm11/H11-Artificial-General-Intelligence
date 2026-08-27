"""
Layer 10 - Memory Architecture
H11 Cognitive Substrate
"""

from .working.agent import H11WorkingAgent
from .shortterm.agent import H11ShorttermAgent
from .longterm.agent import H11LongtermAgent
from .episodic.agent import H11EpisodicAgent
from .semantic.agent import H11SemanticAgent
from .procedural.agent import H11ProceduralAgent
from .retrieval.agent import H11RetrievalAgent
from .consolidate.agent import H11ConsolidateAgent
from .forget.agent import H11ForgetAgent
from .recall.agent import H11RecallAgent
from .association.agent import H11AssociationAgent
from .context_mem.agent import H11ContextMemAgent
from .state.agent import H11StateAgent
from .session.agent import H11SessionAgent
from .memorybank.agent import H11MemorybankAgent
from .scratchpad.agent import H11ScratchpadAgent
from .compression_mem.agent import H11CompressionMemAgent
from .reflection_mem.agent import H11ReflectionMemAgent
from .skill.agent import H11SkillAgent
from .temporal_mem.agent import H11TemporalMemAgent

__all__ = [
    "H11WorkingAgent",
    "H11ShorttermAgent",
    "H11LongtermAgent",
    "H11EpisodicAgent",
    "H11SemanticAgent",
    "H11ProceduralAgent",
    "H11RetrievalAgent",
    "H11ConsolidateAgent",
    "H11ForgetAgent",
    "H11RecallAgent",
    "H11AssociationAgent",
    "H11ContextMemAgent",
    "H11StateAgent",
    "H11SessionAgent",
    "H11MemorybankAgent",
    "H11ScratchpadAgent",
    "H11CompressionMemAgent",
    "H11ReflectionMemAgent",
    "H11SkillAgent",
    "H11TemporalMemAgent"
]
