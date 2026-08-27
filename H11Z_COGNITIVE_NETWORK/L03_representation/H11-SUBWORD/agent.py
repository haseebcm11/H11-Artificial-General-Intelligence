"""
H11-SUBWORD: WordPiece tokenizer logic - MaxMatch forward segmentation.
"""
from dataclasses import dataclass
from typing import List, Dict

AGENT_ID = "H11-SUBWORD"

@dataclass
class SubwordInput:
    text: str
    vocabulary: Dict[str, int]
    unk_token: str = "[UNK]"

@dataclass
class SubwordOutput:
    tokens: List[str]
    token_ids: List[int]

class H11SubwordAgent:
    def process(self, data: SubwordInput) -> SubwordOutput:
        words = data.text.strip().split()
        output_tokens = []
        output_ids = []
        
        for word in words:
            start = 0
            is_bad = False
            sub_tokens = []
            
            while start < len(word):
                end = len(word)
                cur_substr = None
                while start < end:
                    substr = word[start:end]
                    if start > 0:
                        substr = "##" + substr
                        
                    if substr in data.vocabulary:
                        cur_substr = substr
                        break
                    end -= 1
                    
                if cur_substr is None:
                    is_bad = True
                    break
                    
                sub_tokens.append(cur_substr)
                start = end
                
            if is_bad:
                output_tokens.append(data.unk_token)
                output_ids.append(data.vocabulary.get(data.unk_token, 0))
            else:
                for t in sub_tokens:
                    output_tokens.append(t)
                    output_ids.append(data.vocabulary[t])
                    
        return SubwordOutput(
            tokens=output_tokens,
            token_ids=output_ids
        )
