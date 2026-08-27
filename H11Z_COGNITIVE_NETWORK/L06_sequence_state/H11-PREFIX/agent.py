from dataclasses import dataclass
from typing import List, Dict

AGENT_ID = "H11-PREFIX"

class PrefixTreeError(Exception):
    """Raised for malformed prefix tree structures."""
    pass

@dataclass
class PrefixInput:
    prompt_tokens: List[int]
    cache_tree: Dict[int, List[int]]

@dataclass
class PrefixOutput:
    matched_prefix_length: int
    optimal_node_id: int
    cache_hit_rate: float

class PrefixAgent:
    """
    Prefix/Radix tree exact matching for KV cache reuse (Prompt Caching).
    """
    def process(self, req: PrefixInput) -> PrefixOutput:
        if not req.prompt_tokens:
            return PrefixOutput(0, -1, 0.0)
            
        best_match = 0
        best_node = -1
        
        for node_id, tokens in req.cache_tree.items():
            match_len = 0
            for pt, ct in zip(req.prompt_tokens, tokens):
                if pt == ct:
                    match_len += 1
                else:
                    break
            
            if match_len > best_match:
                best_match = match_len
                best_node = node_id
                
        hit_rate = best_match / len(req.prompt_tokens)
        
        return PrefixOutput(
            matched_prefix_length=best_match,
            optimal_node_id=best_node,
            cache_hit_rate=hit_rate
        )
