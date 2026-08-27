from __future__ import annotations

import enum
import re
import logging
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any

logger = logging.getLogger(__name__)

class QueryType(enum.Enum):
    """Enumeration of possible query types."""
    FACTUAL = "FACTUAL"
    ANALYTICAL = "ANALYTICAL"
    COMPARATIVE = "COMPARATIVE"
    PROCEDURAL = "PROCEDURAL"
    EXPLORATORY = "EXPLORATORY"
    DEFINITION = "DEFINITION"

@dataclass
class SubQuery:
    """Represents a component of a larger compound query."""
    text: str
    query_type: QueryType
    domain_hint: Optional[str]
    priority: int
    parent_query_id: Optional[str] = None

@dataclass
class QueryPlan:
    """Represents a structured plan for executing a search query."""
    original_query: str
    sub_queries: List[SubQuery]
    query_type: QueryType
    estimated_complexity: int
    requires_temporal: bool
    requires_comparison: bool
    domains: List[str]

class QueryDecomposer:
    """Natural language query decomposition and routing engine."""

    # Domain keyword mappings covering the 30 H11I domains
    DOMAIN_MAPPINGS = {
        "D01": ["medicine", "health", "doctor", "disease", "treatment", "symptom", "medical", "patient", "clinical", "diabetes", "cancer", "infection", "syndrome", "pathology", "diagnosis", "therapy", "physician", "hospital", "illness", "surgery"],
        "D02": ["pharmacology", "drugs", "pharmacy", "medication", "pill", "prescription", "antibiotic", "dosage"],
        "D03": ["psychology", "mental", "behavior", "cognitive", "therapy", "emotion", "psychiatric"],
        "D04": ["neuroscience", "brain", "neuron", "synapse", "nervous system", "cortex"],
        "D05": ["biology", "genetics", "dna", "rna", "gene", "evolution", "organism", "cell", "protein"],
        "D06": ["earth", "environment", "climate", "geology", "weather", "ocean", "atmosphere", "ecology"],
        "D07": ["agriculture", "farming", "crop", "soil", "harvest", "livestock", "agronomy"],
        "D08": ["physics", "quantum", "gravity", "force", "energy", "mechanics", "thermodynamics", "relativity", "particle"],
        "D09": ["chemistry", "molecule", "reaction", "acid", "base", "element", "compound", "catalyst"],
        "D10": ["mathematics", "algebra", "calculus", "geometry", "theorem", "equation", "topology", "matrix"],
        "D11": ["computer science", "programming", "algorithm", "algorithms", "software", "hardware", "coding", "python", "java", "machine learning", "ai"],
        "D12": ["engineering", "civil", "mechanical", "electrical", "structural", "design", "bridge"],
        "D13": ["materials", "polymers", "ceramics", "metals", "composites", "nanotechnology"],
        "D14": ["energy", "solar", "wind", "nuclear", "fossil", "power", "grid", "electricity"],
        "D15": ["aerospace", "space", "satellite", "rocket", "aviation", "aircraft", "orbit"],
        "D16": ["robotics", "robot", "automation", "cybernetics", "drone", "actuator"],
        "D17": ["finance", "economics", "market", "stock", "trade", "investment", "currency", "inflation"],
        "D18": ["law", "legal", "court", "judge", "attorney", "justice", "legislation", "contract"],
        "D19": ["education", "school", "learning", "teaching", "student", "curriculum", "pedagogy"],
        "D20": ["linguistics", "nlp", "language", "grammar", "syntax", "semantics", "phonetics"],
        "D21": ["philosophy", "ethics", "epistemology", "metaphysics", "logic", "existentialism"],
        "D22": ["sociology", "society", "culture", "community", "demographics", "social"],
        "D23": ["political science", "government", "policy", "election", "democracy", "state", "diplomacy"],
        "D24": ["history", "past", "ancient", "century", "war", "empire", "revolution"],
        "D25": ["art", "painting", "sculpture", "aesthetics", "gallery", "canvas"],
        "D26": ["music", "melody", "rhythm", "instrument", "composer", "harmony", "symphony"],
        "D27": ["architecture", "building", "design", "urban", "construction", "blueprint"],
        "D28": ["sports", "athletics", "game", "match", "team", "player", "championship", "fitness", "exercise"],
        "D29": ["communication", "media", "journalism", "broadcast", "news", "press", "television"],
        "D30": ["cybersecurity", "security", "hacker", "encryption", "firewall", "malware", "vulnerability", "cryptography"]
    }

    def __init__(self) -> None:
        pass

    def _detect_query_type(self, query: str) -> QueryType:
        """Heuristically detects the query type from keywords and patterns."""
        query_lower = query.lower()
        if re.search(r'\b(compare|vs|versus|compared to|difference between)\b', query_lower):
            return QueryType.COMPARATIVE
        elif re.search(r'\b(how to|guide|steps|procedure|tutorial)\b', query_lower):
            return QueryType.PROCEDURAL
        elif re.search(r'\b(what is|define|definition of|meaning of)\b', query_lower):
            return QueryType.DEFINITION
        elif re.search(r'\b(analyze|why|reasons for|impact of|effect of)\b', query_lower):
            return QueryType.ANALYTICAL
        elif re.search(r'\b(explore|overview|summary|tell me about)\b', query_lower):
            return QueryType.EXPLORATORY
        else:
            return QueryType.FACTUAL

    def decompose(self, query: str) -> QueryPlan:
        """Analyzes a query and produces an execution plan with sub-queries."""
        logger.info(f"Decomposing query: {query}")
        query_lower = query.lower()
        
        # Determine temporal and comparative flags
        requires_temporal = bool(re.search(r'\b(latest|recent|last year|20\d{2}|current)\b', query_lower))
        requires_comparison = bool(re.search(r'\b(vs|versus|compared to|difference between)\b', query_lower))
        
        main_query_type = self._detect_query_type(query)
        domains = self.classify_domain(query)
        
        # Split on conjunctions
        split_pattern = r'\b(and|but|also|moreover)\b'
        parts = re.split(split_pattern, query, flags=re.IGNORECASE)
        
        sub_queries: List[SubQuery] = []
        # Reconstruct parts, ignoring just the conjunction words themselves as queries
        current_text = ""
        for part in parts:
            if part.lower() in ["and", "but", "also", "moreover"]:
                continue
            
            clean_part = part.strip()
            if clean_part:
                sq_type = self._detect_query_type(clean_part)
                sq_domains = self.classify_domain(clean_part)
                domain_hint = sq_domains[0] if sq_domains else (domains[0] if domains else None)
                sub_queries.append(
                    SubQuery(
                        text=clean_part,
                        query_type=sq_type,
                        domain_hint=domain_hint,
                        priority=1,
                        parent_query_id=None
                    )
                )

        if not sub_queries:
            sub_queries.append(
                SubQuery(
                    text=query,
                    query_type=main_query_type,
                    domain_hint=domains[0] if domains else None,
                    priority=1,
                    parent_query_id=None
                )
            )
            
        estimated_complexity = min(10, len(sub_queries) * 2 + (3 if requires_comparison else 0) + (2 if requires_temporal else 0))
        if estimated_complexity < 1:
            estimated_complexity = 1

        plan = QueryPlan(
            original_query=query,
            sub_queries=sub_queries,
            query_type=main_query_type,
            estimated_complexity=estimated_complexity,
            requires_temporal=requires_temporal,
            requires_comparison=requires_comparison,
            domains=domains
        )
        return plan

    def expand_query(self, query: str) -> List[str]:
        """Generates query variations/synonyms for recall improvement."""
        logger.debug(f"Expanding query: {query}")
        variations = [query]
        synonyms = {
            "fast": ["quick", "rapid", "speedy"],
            "best": ["top", "optimal", "leading"],
            "cheap": ["affordable", "inexpensive", "budget"],
            "algorithm": ["method", "procedure", "technique"],
            "algorithms": ["methods", "procedures", "techniques"],
            "machine": ["computational", "automated"],
            "learning": ["training", "adaptation"],
        }
        words = query.split()
        for i, word in enumerate(words):
            word_lower = word.lower()
            if word_lower in synonyms:
                for syn in synonyms[word_lower]:
                    new_words = list(words)
                    new_words[i] = syn
                    variations.append(" ".join(new_words))
        return list(set(variations))

    def extract_entities(self, query: str) -> List[Tuple[str, str]]:
        """
        Extracts entities using basic regex patterns.
        Returns a list of (entity, type) tuples.
        """
        entities = []
        
        # Simple heuristics for demonstration
        # PERSON: Capitalized names (2+ words)
        for match in re.finditer(r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b', query):
            entities.append((match.group(1), "PERSON"))
            
        # DRUG / CHEMICAL: Ends with -ine, -mab, -nib, -ol
        for match in re.finditer(r'\b([a-zA-Z]+(?:ine|mab|nib|ol|cillin))\b', query, re.IGNORECASE):
            # Ignore some common non-drug words
            if match.group(1).lower() not in ["machine", "imagine", "school"]:
                entities.append((match.group(1), "DRUG/CHEMICAL"))

        # DISEASE: Words followed by syndrome, disease, disorder
        for match in re.finditer(r'\b([A-Za-z]+ (?:syndrome|disease|disorder))\b', query, re.IGNORECASE):
            entities.append((match.group(1), "DISEASE"))
            
        return entities

    def classify_domain(self, query: str) -> List[str]:
        """Maps query to H11I domain codes (D01-D30) using keyword matching."""
        domains_found = set()
        query_lower = query.lower()
        
        for domain_code, keywords in self.DOMAIN_MAPPINGS.items():
            for kw in keywords:
                if re.search(rf'\b{kw}\b', query_lower):
                    domains_found.add(domain_code)
                    
        return sorted(list(domains_found))
