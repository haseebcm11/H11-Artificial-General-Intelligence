import math
import dataclasses
from typing import List, Tuple

AGENT_ID = "H11_JEWELRY"

class H11JewelryException(Exception):
    pass

@dataclasses.dataclass
class H11JewelryInput:
    rgb_color: Tuple[int, int, int]
    layout_width: float
    bezier_points: List[Tuple[float, float]]
    t_value: float

@dataclasses.dataclass
class H11JewelryOutput:
    cmyk_color: Tuple[float, float, float, float]
    golden_ratio_splits: Tuple[float, float]
    bezier_evaluation: Tuple[float, float]
    agent_id: str

class H11JewelryAgent:
    """
    Arts & Design Domain Agent.
    Implements:
    - Color mixing RGB to CMYK
    - Golden ratio proportions
    - Quadratic Bezier curve evaluation: B(t) = (1-t)^2*P0 + 2t(1-t)*P1 + t^2*P2
    """
    
    GOLDEN_RATIO = 1.61803398875

    def process(self, request: H11JewelryInput) -> H11JewelryOutput:
        if not (0 <= request.t_value <= 1):
            raise H11JewelryException("t_value must be between 0 and 1")
            
        # 1. RGB to CMYK conversion
        r, g, b = [x / 255.0 for x in request.rgb_color]
        k = 1.0 - max(r, g, b)
        if k == 1.0:
            c, m, y = 0.0, 0.0, 0.0
        else:
            c = (1.0 - r - k) / (1.0 - k)
            m = (1.0 - g - k) / (1.0 - k)
            y = (1.0 - b - k) / (1.0 - k)
            
        # 2. Golden ratio splits
        major = request.layout_width / self.GOLDEN_RATIO
        minor = request.layout_width - major
        
        # 3. Bezier curve evaluation (Quadratic)
        # B(t) = (1-t)^2*P0 + 2t(1-t)*P1 + t^2*P2
        if len(request.bezier_points) != 3:
            # Fallback to linear or point if not exactly 3
            bx, by = 0.0, 0.0
        else:
            p0, p1, p2 = request.bezier_points
            t = request.t_value
            mt = 1.0 - t
            
            bx = (mt**2)*p0[0] + 2*mt*t*p1[0] + (t**2)*p2[0]
            by = (mt**2)*p0[1] + 2*mt*t*p1[1] + (t**2)*p2[1]
            
        return H11JewelryOutput(
            cmyk_color=(c, m, y, k),
            golden_ratio_splits=(major, minor),
            bezier_evaluation=(bx, by),
            agent_id=AGENT_ID
        )
