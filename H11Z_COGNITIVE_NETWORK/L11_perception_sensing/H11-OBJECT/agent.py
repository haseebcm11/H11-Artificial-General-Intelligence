"""H11-OBJECT: Object bounding box calculation.

Implements Intersection over Union (IoU) and Non-Maximum Suppression (NMS).
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

AGENT_ID = "H11-OBJECT"

class ObjectError(ValueError): pass

@dataclass
class BBox:
    x1: float
    y1: float
    x2: float
    y2: float
    score: float

@dataclass
class ObjectInput:
    boxes: List[BBox]
    iou_threshold: float = 0.5

@dataclass
class ObjectOutput:
    agent_id: str
    filtered_boxes: List[BBox]
    suppressed_count: int
    execution_time_ms: float

class ObjectAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    def _iou(self, a: BBox, b: BBox) -> float:
        x1 = max(a.x1, b.x1)
        y1 = max(a.y1, b.y1)
        x2 = min(a.x2, b.x2)
        y2 = min(a.y2, b.y2)
        
        inter_area = max(0, x2 - x1) * max(0, y2 - y1)
        
        a_area = (a.x2 - a.x1) * (a.y2 - a.y1)
        b_area = (b.x2 - b.x1) * (b.y2 - b.y1)
        
        union_area = a_area + b_area - inter_area
        return inter_area / max(1e-5, union_area)

    def process(self, input_data: ObjectInput) -> ObjectOutput:
        start_time = time.perf_counter()
        
        # Sort by confidence
        sorted_boxes = sorted(input_data.boxes, key=lambda b: b.score, reverse=True)
        keep = []
        
        for i, box in enumerate(sorted_boxes):
            discard = False
            for kept_box in keep:
                if self._iou(box, kept_box) >= input_data.iou_threshold:
                    discard = True
                    break
            if not discard:
                keep.append(box)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ObjectOutput(
            agent_id=AGENT_ID,
            filtered_boxes=keep,
            suppressed_count=len(input_data.boxes) - len(keep),
            execution_time_ms=elapsed_ms
        )
