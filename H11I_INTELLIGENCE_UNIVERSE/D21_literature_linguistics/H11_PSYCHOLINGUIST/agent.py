import math
from dataclasses import dataclass
from typing import List, Dict

AGENT_ID = "H11_PSYCHOLINGUIST"

@dataclass
class TextMetricsInput:
    words: int
    sentences: int
    syllables: int
    documents: List[List[str]]
    target_doc_index: int
    term: str
    string_a: str
    string_b: str

@dataclass
class TextMetricsOutput:
    flesch_reading_ease: float
    tf_idf_score: float
    levenshtein_distance: int

class DomainException(Exception):
    pass

class H11PsycholinguistAgent:
    """
    Linguistics and Literature processing agent.
    Implements Flesch readability formula, TF-IDF calculation, and Levenshtein distance.
    """
    def __init__(self):
        self.agent_id = AGENT_ID
        
    def _levenshtein(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self._levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    def process(self, input_data: TextMetricsInput) -> TextMetricsOutput:
        if input_data.sentences <= 0 or input_data.words <= 0:
            raise DomainException("Sentences and words must be > 0 for Flesch score")
            
        # 1. Flesch Readability: 206.835 - 1.015(words/sentences) - 84.6(syllables/words)
        flesch = 206.835 - 1.015 * (input_data.words / input_data.sentences) - 84.6 * (input_data.syllables / input_data.words)
        
        # 2. TF-IDF Calculation
        N = len(input_data.documents)
        if N == 0 or input_data.target_doc_index >= N:
            raise DomainException("Invalid document configuration")
            
        target_doc = input_data.documents[input_data.target_doc_index]
        tf = target_doc.count(input_data.term) / len(target_doc) if target_doc else 0.0
        
        docs_with_term = sum(1 for doc in input_data.documents if input_data.term in doc)
        idf = math.log(N / (1 + docs_with_term))
        tfidf = tf * idf
        
        # 3. Levenshtein distance
        lev_dist = self._levenshtein(input_data.string_a, input_data.string_b)
        
        return TextMetricsOutput(
            flesch_reading_ease=flesch,
            tf_idf_score=tfidf,
            levenshtein_distance=lev_dist
        )
