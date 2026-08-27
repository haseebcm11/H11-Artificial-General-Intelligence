import time
import math
import asyncio
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto

class MessageType(Enum):
    # Blackboard
    POST_BLACKBOARD = auto()
    READ_BLACKBOARD = auto()
    # Contract Net Protocol
    CFP = auto()
    BID = auto()
    AWARD = auto()
    # Paxos
    PREPARE = auto()
    PROMISE = auto()
    ACCEPT = auto()
    ACCEPTED = auto()

@dataclass
class KnowledgeEntry:
    id: str
    topic: str
    content: Any
    author_id: str
    base_confidence: float
    timestamp: float = field(default_factory=time.time)
    decay_rate: float = 0.05 # exponential decay factor

    def current_confidence(self) -> float:
        elapsed = time.time() - self.timestamp
        return self.base_confidence * math.exp(-self.decay_rate * elapsed)

class StochasticBlackboard:
    def __init__(self):
        self._store: Dict[str, List[KnowledgeEntry]] = {}

    def post(self, entry: KnowledgeEntry) -> None:
        if entry.topic not in self._store:
            self._store[entry.topic] = []
        self._store[entry.topic].append(entry)

    def read(self, topic: str, min_confidence: float = 0.5) -> List[KnowledgeEntry]:
        if topic not in self._store:
            return []
        
        # Filter and sort by current confidence
        valid_entries = [
            e for e in self._store[topic] 
            if e.current_confidence() >= min_confidence
        ]
        return sorted(valid_entries, key=lambda x: x.current_confidence(), reverse=True)

@dataclass
class Bid:
    bidder_id: str
    task_id: str
    estimated_cost: float
    estimated_time: float
    quality_score: float

    def utility(self, cost_weight: float = 0.4, time_weight: float = 0.4, quality_weight: float = 0.2) -> float:
        # Lower cost/time is better, higher quality is better
        # Normalization assumed done prior to utility calculation for simplicity
        return (quality_weight * self.quality_score) - (cost_weight * self.estimated_cost) - (time_weight * self.estimated_time)

class ContractNetManager:
    def __init__(self):
        self.active_cfps: Dict[str, Dict[str, Any]] = {}
        self.bids: Dict[str, List[Bid]] = {}

    def issue_cfp(self, task_id: str, requirements: Dict[str, Any]) -> None:
        self.active_cfps[task_id] = requirements
        self.bids[task_id] = []

    def receive_bid(self, bid: Bid) -> None:
        if bid.task_id in self.bids:
            self.bids[bid.task_id].append(bid)

    def evaluate_and_award(self, task_id: str) -> Optional[str]:
        if task_id not in self.bids or not self.bids[task_id]:
            return None
        
        task_bids = self.bids[task_id]
        best_bid = max(task_bids, key=lambda b: b.utility())
        
        # Cleanup
        del self.active_cfps[task_id]
        del self.bids[task_id]
        
        return best_bid.bidder_id

class PaxosNode:
    def __init__(self, node_id: str, cluster_size: int):
        self.node_id = node_id
        self.cluster_size = cluster_size
        self.quorum = (cluster_size // 2) + 1
        
        # Acceptor state
        self.min_proposal_id = 0
        self.accepted_proposal_id = 0
        self.accepted_value = None
        
        # Proposer state
        self.promises_received = 0
        self.accepts_received = 0

    def receive_prepare(self, proposal_id: int) -> Tuple[bool, int, Any]:
        if proposal_id > self.min_proposal_id:
            self.min_proposal_id = proposal_id
            return (True, self.accepted_proposal_id, self.accepted_value)
        return (False, 0, None)

    def receive_accept(self, proposal_id: int, value: Any) -> bool:
        if proposal_id >= self.min_proposal_id:
            self.min_proposal_id = proposal_id
            self.accepted_proposal_id = proposal_id
            self.accepted_value = value
            return True
        return False

class CollaborationAgent:
    """
    H11-COLLABORATION Agent implementation.
    Integrates Blackboard, Contract Net, and Paxos consensus for robust multi-agent coordination.
    """
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.blackboard = StochasticBlackboard()
        self.cnp_manager = ContractNetManager()
        self.paxos_node = PaxosNode(agent_id, cluster_size=5) # Example cluster size

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        action_type = request.get("action_type")
        payload = request.get("payload", {})
        sender_id = request.get("agent_id", "unknown")

        try:
            if action_type == "POST_BLACKBOARD":
                entry = KnowledgeEntry(
                    id=payload.get("id"),
                    topic=payload.get("topic"),
                    content=payload.get("content"),
                    author_id=sender_id,
                    base_confidence=payload.get("confidence", 1.0)
                )
                self.blackboard.post(entry)
                return {"status": "success", "message": "Knowledge posted."}
                
            elif action_type == "READ_BLACKBOARD":
                entries = self.blackboard.read(
                    topic=payload.get("topic"), 
                    min_confidence=payload.get("min_confidence", 0.1)
                )
                return {
                    "status": "success", 
                    "data": [{"content": e.content, "confidence": e.current_confidence()} for e in entries]
                }
                
            elif action_type == "INITIATE_CNP":
                task_id = payload.get("task_id")
                self.cnp_manager.issue_cfp(task_id, payload.get("requirements", {}))
                return {"status": "success", "message": f"CFP issued for {task_id}"}
                
            elif action_type == "SUBMIT_BID":
                bid = Bid(
                    bidder_id=sender_id,
                    task_id=payload.get("task_id"),
                    estimated_cost=payload.get("cost", 0.0),
                    estimated_time=payload.get("time", 0.0),
                    quality_score=payload.get("quality", 0.0)
                )
                self.cnp_manager.receive_bid(bid)
                return {"status": "success", "message": "Bid received."}
                
            elif action_type == "AWARD_CNP":
                task_id = payload.get("task_id")
                winner = self.cnp_manager.evaluate_and_award(task_id)
                return {"status": "success", "winner": winner}
                
            elif action_type == "PROPOSE_CONSENSUS":
                # Simulated local paxos proposal initiation
                proposal_id = payload.get("proposal_id", 1)
                value = payload.get("value")
                ack, last_pid, last_val = self.paxos_node.receive_prepare(proposal_id)
                if ack:
                    accepted = self.paxos_node.receive_accept(proposal_id, value)
                    if accepted:
                        return {"status": "success", "message": "Value accepted locally."}
                return {"status": "failure", "message": "Proposal rejected."}
                
            else:
                return {"status": "error", "message": f"Unknown action type: {action_type}"}
                
        except Exception as e:
            return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    agent = CollaborationAgent("collab-primary")
    agent.process_request({
        "action_type": "POST_BLACKBOARD",
        "agent_id": "sensor-1",
        "payload": {
            "id": "k1",
            "topic": "environment.temperature",
            "content": 22.5,
            "confidence": 0.95
        }
    })
    result = agent.process_request({
        "action_type": "READ_BLACKBOARD",
        "agent_id": "planner-1",
        "payload": {"topic": "environment.temperature"}
    })
    print("Blackboard Result:", result)
