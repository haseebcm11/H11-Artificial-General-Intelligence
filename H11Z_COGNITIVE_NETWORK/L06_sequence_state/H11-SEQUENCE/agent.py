from dataclasses import dataclass
from typing import Tuple

AGENT_ID = "H11-SEQUENCE"

class AlignmentError(Exception):
    """Raised when sequences are too large to align."""
    pass

@dataclass
class SequenceInput:
    seq1: str
    seq2: str
    match_score: float = 1.0
    gap_penalty: float = -1.0
    mismatch_penalty: float = -1.0

@dataclass
class SequenceOutput:
    alignment_score: float
    aligned_seq1: str
    aligned_seq2: str

class SequenceAgent:
    """
    Needleman-Wunsch Dynamic Programming for global sequence alignment.
    DP(i,j) = max( DP(i-1,j-1)+S, DP(i-1,j)+gap, DP(i,j-1)+gap )
    """
    def process(self, req: SequenceInput) -> SequenceOutput:
        n, m = len(req.seq1), len(req.seq2)
        if n * m > 1e6:
            raise AlignmentError("Sequences too large for exact DP alignment")
            
        dp = [[0.0] * (m + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            dp[i][0] = i * req.gap_penalty
        for j in range(1, m + 1):
            dp[0][j] = j * req.gap_penalty
            
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                match = dp[i-1][j-1] + (req.match_score if req.seq1[i-1] == req.seq2[j-1] else req.mismatch_penalty)
                delete = dp[i-1][j] + req.gap_penalty
                insert = dp[i][j-1] + req.gap_penalty
                dp[i][j] = max(match, delete, insert)
                
        align1, align2 = "", ""
        i, j = n, m
        while i > 0 or j > 0:
            if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + (req.match_score if req.seq1[i-1] == req.seq2[j-1] else req.mismatch_penalty):
                align1 = req.seq1[i-1] + align1
                align2 = req.seq2[j-1] + align2
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i-1][j] + req.gap_penalty:
                align1 = req.seq1[i-1] + align1
                align2 = "-" + align2
                i -= 1
            else:
                align1 = "-" + align1
                align2 = req.seq2[j-1] + align2
                j -= 1
                
        return SequenceOutput(
            alignment_score=dp[n][m],
            aligned_seq1=align1,
            aligned_seq2=align2
        )
