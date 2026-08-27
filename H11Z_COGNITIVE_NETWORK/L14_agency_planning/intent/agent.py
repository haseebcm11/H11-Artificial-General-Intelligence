import uuid
import math
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto

class IntentDomain(Enum):
    INFORMATION_RETRIEVAL = auto()
    TRANSACTIONAL = auto()
    NAVIGATIONAL = auto()
    SOCIAL = auto()
    EPISTEMIC_UPDATE = auto()
    UNKNOWN = auto()

@dataclass
class IntentSlot:
    key: str
    value: Any
    confidence: float
    required: bool
    source_span: Optional[Tuple[int, int]] = None

@dataclass
class ParsedIntent:
    intent_id: str
    domain: IntentDomain
    primary_class: str
    confidence: float
    slots: Dict[str, IntentSlot]
    is_implicit: bool
    parent_intent_id: Optional[str] = None
    
    def is_actionable(self) -> bool:
        return all(slot.confidence > 0.6 for slot in self.slots.values() if slot.required)

@dataclass
class ActionCandidate:
    action_type: str
    target_system: str
    parameters: Dict[str, Any]
    score: float

class IntentDisambiguator:
    def __init__(self, entropy_threshold: float = 1.5):
        self.entropy_threshold = entropy_threshold

    def calculate_distribution_entropy(self, probabilities: List[float]) -> float:
        return -sum(p * math.log2(p) for p in probabilities if p > 0)
        
    def requires_disambiguation(self, intent_hypotheses: List[ParsedIntent]) -> bool:
        if not intent_hypotheses:
            return True
            
        probs = [i.confidence for i in intent_hypotheses]
        total = sum(probs)
        normalized = [p / total for p in probs]
        entropy = self.calculate_distribution_entropy(normalized)
        
        return entropy > self.entropy_threshold

class ImplicitIntentDetector:
    def __init__(self):
        self.context_history: List[Dict[str, Any]] = []
        
    def add_context(self, state: Dict[str, Any]):
        self.context_history.append({"state": state, "timestamp": time.time()})
        if len(self.context_history) > 10:
            self.context_history.pop(0)
            
    def infer_implicits(self, explicit_intent: ParsedIntent) -> List[ParsedIntent]:
        # Simple heuristic rule for demonstration: if user is asking for information repetitively,
        # implicit intent might be FRUSTRATION or NEED_TUTORIAL
        implicits = []
        if explicit_intent.domain == IntentDomain.INFORMATION_RETRIEVAL:
            recent_irs = sum(1 for c in self.context_history if c.get('state', {}).get('domain') == 'INFORMATION_RETRIEVAL')
            if recent_irs > 3:
                implicits.append(ParsedIntent(
                    intent_id=str(uuid.uuid4()),
                    domain=IntentDomain.EPISTEMIC_UPDATE,
                    primary_class="provide_summary_tutorial",
                    confidence=0.75,
                    slots={},
                    is_implicit=True,
                    parent_intent_id=explicit_intent.intent_id
                ))
        return implicits

class IntentFormationAgent:
    def __init__(self):
        self.disambiguator = IntentDisambiguator()
        self.implicit_detector = ImplicitIntentDetector()
        self.intent_registry: Dict[str, ParsedIntent] = {}
        self.action_mappings = {
            "search_query": [
                ActionCandidate("web_search", "search_api", {"query": "$query"}, 0.9)
            ],
            "provide_summary_tutorial": [
                ActionCandidate("generate_document", "llm_agent", {"topic": "summary"}, 0.85)
            ]
        }

    def _pseudo_parse_utterance(self, utterance: str) -> List[ParsedIntent]:
        # Simulated parsing logic
        utterance_lower = utterance.lower()
        if "find" in utterance_lower or "search" in utterance_lower:
            return [ParsedIntent(
                intent_id=str(uuid.uuid4()),
                domain=IntentDomain.INFORMATION_RETRIEVAL,
                primary_class="search_query",
                confidence=0.88,
                slots={
                    "query": IntentSlot("query", utterance, 0.9, True, (0, len(utterance)))
                },
                is_implicit=False
            )]
        return [ParsedIntent(
            intent_id=str(uuid.uuid4()),
            domain=IntentDomain.UNKNOWN,
            primary_class="unhandled",
            confidence=0.3,
            slots={},
            is_implicit=False
        )]

    def process_input(self, utterance: str) -> Dict[str, Any]:
        raw_hypotheses = self._pseudo_parse_utterance(utterance)
        
        needs_clarification = self.disambiguator.requires_disambiguation(raw_hypotheses)
        
        best_intent = max(raw_hypotheses, key=lambda x: x.confidence) if raw_hypotheses else None
        
        resolved_intents = [best_intent] if best_intent and not needs_clarification else []
        
        if best_intent and not needs_clarification:
            self.intent_registry[best_intent.intent_id] = best_intent
            self.implicit_detector.add_context({"domain": best_intent.domain.name, "class": best_intent.primary_class})
            
            implicits = self.implicit_detector.infer_implicits(best_intent)
            for imp in implicits:
                self.intent_registry[imp.intent_id] = imp
            resolved_intents.extend(implicits)
            
        mapped_actions = []
        for intent in resolved_intents:
            if intent.primary_class in self.action_mappings:
                candidates = self.action_mappings[intent.primary_class]
                for c in candidates:
                    # Resolve parameters
                    resolved_params = {}
                    for k, v in c.parameters.items():
                        if isinstance(v, str) and v.startswith("$"):
                            slot_name = v[1:]
                            if slot_name in intent.slots:
                                resolved_params[k] = intent.slots[slot_name].value
                            else:
                                resolved_params[k] = None
                        else:
                            resolved_params[k] = v
                    mapped_actions.append({
                        "intent_id": intent.intent_id,
                        "action_type": c.action_type,
                        "parameters": resolved_params
                    })

        return {
            "utterance": utterance,
            "intents": [
                {
                    "id": i.intent_id,
                    "class": i.primary_class,
                    "domain": i.domain.name,
                    "implicit": i.is_implicit
                } for i in resolved_intents
            ],
            "needs_disambiguation": needs_clarification,
            "actions": mapped_actions
        }

if __name__ == "__main__":
    agent = IntentFormationAgent()
    print(agent.process_input("Search for quantum mechanics papers."))
    for _ in range(4):
        print(agent.process_input("Find more information on entanglement."))
