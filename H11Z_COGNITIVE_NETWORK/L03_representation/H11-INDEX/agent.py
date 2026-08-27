"""
H11-INDEX: Inverted Index Construction with TF-IDF weighting.
"""
from dataclasses import dataclass
from typing import List, Dict
import math

AGENT_ID = "H11-INDEX"

@dataclass
class IndexInput:
    documents: List[List[str]]

@dataclass
class IndexOutput:
    inverted_index: Dict[str, Dict[int, float]]
    idf: Dict[str, float]

class H11IndexAgent:
    def process(self, data: IndexInput) -> IndexOutput:
        N = len(data.documents)
        df = {}
        tf = []
        
        for i, doc in enumerate(data.documents):
            doc_tf = {}
            for term in doc:
                doc_tf[term] = doc_tf.get(term, 0) + 1
            tf.append(doc_tf)
            
            for term in set(doc):
                df[term] = df.get(term, 0) + 1
                
        idf = {term: math.log(N / (count + 1)) for term, count in df.items()}
        
        inverted_index = {}
        for i, doc_tf in enumerate(tf):
            doc_len = sum(doc_tf.values())
            for term, count in doc_tf.items():
                tfidf = (count / doc_len) * idf[term]
                if term not in inverted_index:
                    inverted_index[term] = {}
                inverted_index[term][i] = tfidf
                
        return IndexOutput(
            inverted_index=inverted_index,
            idf=idf
        )
