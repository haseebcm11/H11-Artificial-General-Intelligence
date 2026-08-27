"""
Agent Module: L11_SCENE
Agent Class: SceneAgent

Scene graph parsing with entity-relationship triplets, spatial relation vectors (above/below/inside), and centroid distance geometry.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L11_SCENE"


class SceneError(ValueError):
    """Raised when SceneAgent domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class SceneAgentInput:
    objects: list[dict] = field(default_factory=lambda: [{'id': 'o1', 'box': [0, 0, 10, 10], 'label': 'table'}, {'id': 'o2', 'box': [2, 12, 6, 16], 'label': 'cup'}])


@dataclass(frozen=True)
class SceneAgentOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    relations: list[dict] = field(default_factory=list)


class SceneAgent:
    """
    Scene graph parsing with entity-relationship triplets, spatial relation vectors (above/below/inside), and centroid distance geometry.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: SceneAgentInput) -> SceneAgentOutput:
        """Execute domain-specific analytical mathematics and logic."""
        objs = inputs.objects if inputs.objects else []
        relations = []
        for i in range(len(objs)):
            for j in range(i + 1, len(objs)):
                b1, b2 = objs[i]["box"], objs[j]["box"]
                c1 = ((b1[0]+b1[2])/2.0, (b1[1]+b1[3])/2.0)
                c2 = ((b2[0]+b2[2])/2.0, (b2[1]+b2[3])/2.0)
                dist = math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)
                rel = "above" if c2[1] > c1[1] else "below"
                relations.append({"src": str(objs[i].get("id")), "dst": str(objs[j].get("id")), "relation": rel, "distance": round(dist, 3)})
        density = len(relations) / max(len(objs)*(len(objs)-1)/2.0, 1.0) if len(objs) > 1 else 1.0
        metrics = {"object_count": float(len(objs)), "relation_count": float(len(relations)), "graph_density": round(density, 4)}
        return SceneAgentOutput(status="COMPLETED", score=round(density, 4), metrics=metrics, relations=relations)
