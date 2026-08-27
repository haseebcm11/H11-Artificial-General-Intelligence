import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class LTLOp(Enum):
    GLOBALLY = "G"
    FINALLY = "F"
    NEXT = "X"
    UNTIL = "U"
    AND = "&"
    OR = "|"
    NOT = "!"

@dataclass
class LTLNode:
    op: Optional[LTLOp] = None
    predicate: Optional[str] = None
    left: Optional['LTLNode'] = None
    right: Optional['LTLNode'] = None
    
    def __str__(self):
        if self.predicate:
            return self.predicate
        if self.op in (LTLOp.GLOBALLY, LTLOp.FINALLY, LTLOp.NEXT, LTLOp.NOT):
            return f"{self.op.value}({self.left})"
        if self.op in (LTLOp.UNTIL, LTLOp.AND, LTLOp.OR):
            return f"({self.left} {self.op.value} {self.right})"
        return "Empty"

class FormalConstraintGenerator:
    """
    A simplistic heuristic parser for converting text goals to LTL nodes.
    In a real substrate, this uses LLM-based parsing with formal grammar checking.
    """
    def synthesize(self, text: str) -> List[LTLNode]:
        text = text.lower()
        nodes = []
        
        # Rule 1: "Never" -> G(!predicate)
        if "never" in text:
            pred = text.split("never")[1].strip().replace(" ", "_")
            node = LTLNode(op=LTLOp.GLOBALLY, left=LTLNode(op=LTLOp.NOT, left=LTLNode(predicate=pred)))
            nodes.append(node)
            
        # Rule 2: "Always" -> G(predicate)
        if "always" in text:
            pred = text.split("always")[1].strip().replace(" ", "_")
            node = LTLNode(op=LTLOp.GLOBALLY, left=LTLNode(predicate=pred))
            nodes.append(node)
            
        # Rule 3: "Eventually" -> F(predicate)
        if "eventually" in text:
            pred = text.split("eventually")[1].strip().replace(" ", "_")
            node = LTLNode(op=LTLOp.FINALLY, left=LTLNode(predicate=pred))
            nodes.append(node)
            
        return nodes

class SpecificationAgent:
    def __init__(self):
        self.generator = FormalConstraintGenerator()
        
    def specify_goal(self, natural_language_goal: str) -> List[str]:
        ltl_nodes = self.generator.synthesize(natural_language_goal)
        return [str(node) for node in ltl_nodes]

if __name__ == "__main__":
    agent = SpecificationAgent()
    specs = agent.specify_goal("never harm_humans")
    specs += agent.specify_goal("always preserve_energy")
    specs += agent.specify_goal("eventually complete_task")
    
    for s in specs:
        print(f"Generated LTL: {s}")
