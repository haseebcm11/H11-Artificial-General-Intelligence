"""
H11-BPE: Byte-Pair Encoding algorithm implementation.
Computes pair frequencies and merges iteratively to build a subword vocabulary.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Set
import collections
import re

AGENT_ID = "H11-BPE"

@dataclass
class BPEInput:
    corpus: List[str]
    num_merges: int

@dataclass
class BPEOutput:
    vocabulary: Dict[str, int]
    merges: List[Tuple[str, str]]
    final_tokens: List[List[str]]

class H11BPEAgent:
    def __init__(self):
        self.vocab = {}
        
    def _get_stats(self, vocab: Dict[str, int]) -> Dict[Tuple[str, str], int]:
        pairs = collections.defaultdict(int)
        for word, freq in vocab.items():
            symbols = word.split()
            for i in range(len(symbols)-1):
                pairs[symbols[i], symbols[i+1]] += freq
        return pairs

    def _merge_vocab(self, pair: Tuple[str, str], v_in: Dict[str, int]) -> Dict[str, int]:
        v_out = {}
        bigram = re.escape(' '.join(pair))
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
        for word in v_in:
            w_out = p.sub(''.join(pair), word)
            v_out[w_out] = v_in[word]
        return v_out

    def process(self, data: BPEInput) -> BPEOutput:
        vocab_counts = collections.Counter()
        for text in data.corpus:
            words = text.strip().split()
            for w in words:
                vocab_counts[' '.join(list(w)) + ' </w>'] += 1
                
        vocab = dict(vocab_counts)
        merges = []
        
        for i in range(data.num_merges):
            pairs = self._get_stats(vocab)
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            vocab = self._merge_vocab(best, vocab)
            merges.append(best)
            
        final_vocab = collections.defaultdict(int)
        for word, freq in vocab.items():
            for token in word.split():
                final_vocab[token] += freq
                
        final_tokens = []
        for text in data.corpus:
            tokens = []
            for w in text.strip().split():
                w_with_end = ' '.join(list(w)) + ' </w>'
                # Apply merges
                for merge_pair in merges:
                    bigram = ' '.join(merge_pair)
                    w_with_end = w_with_end.replace(bigram, ''.join(merge_pair))
                tokens.append(w_with_end.split())
            final_tokens.append([t for sub in tokens for t in sub])
            
        return BPEOutput(
            vocabulary=dict(final_vocab),
            merges=merges,
            final_tokens=final_tokens
        )


# Backwards compatibility aliases
BpeAgent = H11BPEAgent
BpeInput = BPEInput
BpeOutput = BPEOutput
