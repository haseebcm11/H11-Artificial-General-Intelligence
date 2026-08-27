import math
from typing import List
from dataclasses import dataclass

AGENT_ID = "H11-FLASHATTENTION"

class FlashAttentionException(Exception):
    pass

@dataclass
class FlashAttentionInput:
    q_blocks: List[List[List[float]]]
    k_blocks: List[List[List[float]]]
    v_blocks: List[List[List[float]]]
    block_size: int

@dataclass
class FlashAttentionOutput:
    fused_output: List[List[float]]
    sram_utilization: float

class FlashAttentionAgent:
    """
    H11-FLASHATTENTION
    Implements FlashAttention tiling and online softmax.
    Computes exact attention iteratively block-by-block, maintaining running max (m_i) and running sum of exponents (l_i).
    Memory complexity O(N) instead of O(N^2).
    """
    def __init__(self):
        self.sram_utilization = 0.0

    def process(self, input_data: FlashAttentionInput) -> FlashAttentionOutput:
        q_blocks = input_data.q_blocks
        k_blocks = input_data.k_blocks
        v_blocks = input_data.v_blocks
        
        if not q_blocks or not k_blocks:
            raise FlashAttentionException("Empty blocks")
            
        d = len(q_blocks[0][0])
        scale = 1.0 / math.sqrt(d)
        
        Tr = len(q_blocks)
        Tc = len(k_blocks)
        
        O = []
        l = []
        m = []
        
        # Initialize output
        for r in range(Tr):
            br = len(q_blocks[r])
            O.append([[0.0 for _ in range(d)] for _ in range(br)])
            l.append([0.0 for _ in range(br)])
            m.append([-1e9 for _ in range(br)])
            
        for c in range(Tc):
            K_j = k_blocks[c]
            V_j = v_blocks[c]
            bc = len(K_j)
            
            for r in range(Tr):
                Q_i = q_blocks[r]
                br = len(Q_i)
                
                # S_ij = Q_i K_j^T
                S_ij = [[sum(Q_i[i_idx][dim] * K_j[j_idx][dim] for dim in range(d)) * scale 
                         for j_idx in range(bc)] for i_idx in range(br)]
                
                for i_idx in range(br):
                    m_ij = max(S_ij[i_idx])
                    m_i_new = max(m[r][i_idx], m_ij)
                    
                    l_ij = sum(math.exp(S_ij[i_idx][j_idx] - m_ij) for j_idx in range(bc))
                    l_i_new = math.exp(m[r][i_idx] - m_i_new) * l[r][i_idx] + math.exp(m_ij - m_i_new) * l_ij
                    
                    # P_ij = exp(S_ij - m_ij)
                    for dim in range(d):
                        term1 = math.exp(m[r][i_idx] - m_i_new) * l[r][i_idx] * O[r][i_idx][dim]
                        term2 = math.exp(m_ij - m_i_new) * sum(math.exp(S_ij[i_idx][j_idx] - m_ij) * V_j[j_idx][dim] for j_idx in range(bc))
                        O[r][i_idx][dim] = (term1 + term2) / l_i_new
                        
                    m[r][i_idx] = m_i_new
                    l[r][i_idx] = l_i_new
                    
        # Flatten O
        fused_output = []
        for r in range(Tr):
            fused_output.extend(O[r])
            
        self.sram_utilization = 0.85 # Mock calculation for SRAM usage
        
        return FlashAttentionOutput(
            fused_output=fused_output,
            sram_utilization=self.sram_utilization
        )
