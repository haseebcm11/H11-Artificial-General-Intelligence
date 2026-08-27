import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
import time

logger = logging.getLogger(__name__)

class Modality(Enum):
    SPEECH = auto()
    GESTURE = auto()
    GAZE = auto()
    PROXEMICS = auto()

class CognitiveLoadLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

@dataclass
class MultimodalInput:
    modality: Modality
    timestamp: float
    data: Any
    confidence: float

@dataclass
class UserState:
    id: str
    cognitive_load: CognitiveLoadLevel = CognitiveLoadLevel.LOW
    trust_score: float = 1.0
    recent_inputs: List[MultimodalInput] = field(default_factory=list)

@dataclass
class Intent:
    action: str
    target: Optional[str] = None
    confidence: float = 0.0

class FusionEngine:
    def __init__(self, config: Dict[str, Any]):
        self.weights = {
            Modality.SPEECH: config.get("modalities", {}).get("speech", {}).get("weight", 0.6),
            Modality.GESTURE: config.get("modalities", {}).get("gesture", {}).get("weight", 0.3),
            Modality.GAZE: config.get("modalities", {}).get("gaze", {}).get("weight", 0.1),
        }
        self.time_window = 1.0  # seconds
        
    def fuse(self, inputs: List[MultimodalInput]) -> Optional[Intent]:
        # Filter stale inputs
        current_time = time.time()
        valid_inputs = [i for i in inputs if current_time - i.timestamp <= self.time_window]
        
        if not valid_inputs:
            return None
            
        # Example Late Fusion logic
        speech_intent = None
        gesture_target = None
        
        for idx in valid_inputs:
            if idx.modality == Modality.SPEECH and idx.confidence > 0.5:
                speech_intent = idx.data  # e.g., "point" or "fetch"
            elif idx.modality == Modality.GESTURE and idx.confidence > 0.6:
                gesture_target = idx.data # e.g., "object_123"
            elif idx.modality == Modality.GAZE and idx.confidence > 0.8:
                if not gesture_target:
                    gesture_target = idx.data
                    
        # Combine
        if speech_intent and gesture_target:
            return Intent(action=speech_intent, target=gesture_target, confidence=0.85)
        elif speech_intent:
            return Intent(action=speech_intent, confidence=0.6)
            
        return None

class DialogManager:
    def __init__(self, config: Dict[str, Any]):
        self.history = []
        self.max_history = config.get("dialog_management", {}).get("max_turns_history", 5)
        
    def add_turn(self, user_intent: Intent, system_response: str):
        self.history.append({"user": user_intent, "system": system_response})
        if len(self.history) > self.max_history:
            self.history.pop(0)

class HCIAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.fusion_engine = FusionEngine(config)
        self.dialog_manager = DialogManager(config)
        self.user_state = UserState(id="user_1")
        
    def process_input(self, m_input: MultimodalInput):
        self.user_state.recent_inputs.append(m_input)
        
        # Keep window clean
        current_time = time.time()
        self.user_state.recent_inputs = [
            i for i in self.user_state.recent_inputs 
            if current_time - i.timestamp <= self.fusion_engine.time_window
        ]
        
        intent = self.fusion_engine.fuse(self.user_state.recent_inputs)
        if intent:
            self._handle_intent(intent)
            
    def _handle_intent(self, intent: Intent):
        response = ""
        
        # Adapt response based on cognitive load
        if self.user_state.cognitive_load == CognitiveLoadLevel.HIGH:
            response = f"Acknowledged. Executing {intent.action}." # Concise
        else:
            if intent.target:
                response = f"I understand. I will {intent.action} the {intent.target}." # Detailed
            else:
                response = f"I am preparing to {intent.action}. Please specify a target if needed."
                
        logger.info(f"System Response: {response}")
        self.dialog_manager.add_turn(intent, response)
        
        # Clear used inputs
        self.user_state.recent_inputs = []

if __name__ == "__main__":
    config = {
        "modalities": {
            "speech": {"weight": 0.7, "timeout_ms": 1000},
            "gesture": {"weight": 0.3, "confidence_threshold": 0.5}
        },
        "user_modeling": {
            "track_cognitive_load": True,
            "adaptation_rate": 0.1
        }
    }
    
    agent = HCIAgent(config)
    
    t = time.time()
    agent.process_input(MultimodalInput(Modality.GAZE, t, "apple", 0.9))
    agent.process_input(MultimodalInput(Modality.SPEECH, t+0.2, "fetch", 0.8))
    
    # Simulate high cognitive load user
    agent.user_state.cognitive_load = CognitiveLoadLevel.HIGH
    t = time.time()
    agent.process_input(MultimodalInput(Modality.GESTURE, t, "bottle", 0.85))
    agent.process_input(MultimodalInput(Modality.SPEECH, t+0.1, "grab", 0.9))
