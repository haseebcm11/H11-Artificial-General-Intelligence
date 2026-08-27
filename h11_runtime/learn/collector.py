from __future__ import annotations
import json
import logging
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

logger = logging.getLogger(__name__)

@dataclass
class TrainingExample:
    example_id: str
    agent_id: str
    query: str
    retrieved_docs: List[Dict]
    agent_output: Dict[str, Any]
    feedback_score: Optional[float]
    domain: str
    created_at: datetime
    case_id: str

@dataclass
class CollectionConfig:
    storage_dir: str = './h11_training_data'
    max_examples: int = 1_000_000
    min_feedback_score: float = 0.5
    domains: Optional[List[str]] = None

class DataCollector:
    def __init__(self, config: Optional[CollectionConfig] = None):
        self.config = config or CollectionConfig()
        self._examples: List[TrainingExample] = []
        os.makedirs(self.config.storage_dir, exist_ok=True)
        self._load()

    def record(
        self,
        agent_id: str,
        case_id: str,
        query: str,
        retrieved_docs: List[Dict],
        output: Dict,
        domain: str,
        feedback_score: Optional[float] = None
    ) -> str:
        if self.config.domains and domain not in self.config.domains:
            logger.debug(f"Domain {domain} not in configured domains. Skipping.")
            return ""

        example = TrainingExample(
            example_id=str(uuid.uuid4()),
            agent_id=agent_id,
            query=query,
            retrieved_docs=retrieved_docs,
            agent_output=output,
            feedback_score=feedback_score,
            domain=domain,
            created_at=datetime.utcnow(),
            case_id=case_id
        )

        self._examples.append(example)
        if len(self._examples) > self.config.max_examples:
            self._examples.pop(0)

        logger.info(f"Recorded training example {example.example_id} for agent {agent_id}")
        self._save()
        return example.example_id

    def get_examples(self, domain: Optional[str] = None, min_score: float = 0.0, limit: int = 1000) -> List[TrainingExample]:
        filtered = [
            ex for ex in self._examples
            if (domain is None or ex.domain == domain) and
               (ex.feedback_score is None or ex.feedback_score >= min_score)
        ]
        return filtered[-limit:]

    def export_for_training(self, format: str = 'jsonl', output_path: Optional[str] = None) -> str:
        if format != 'jsonl':
            raise ValueError(f"Unsupported format: {format}")

        path = output_path or os.path.join(self.config.storage_dir, f"export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl")
        
        with open(path, 'w', encoding='utf-8') as f:
            for ex in self._examples:
                if ex.feedback_score is None or ex.feedback_score >= self.config.min_feedback_score:
                    data = asdict(ex)
                    data['created_at'] = ex.created_at.isoformat()
                    f.write(json.dumps(data) + '\n')
        
        logger.info(f"Exported {len(self._examples)} examples to {path}")
        return path

    def _save(self) -> None:
        path = os.path.join(self.config.storage_dir, 'current_collection.jsonl')
        with open(path, 'w', encoding='utf-8') as f:
            for ex in self._examples:
                data = asdict(ex)
                data['created_at'] = ex.created_at.isoformat()
                f.write(json.dumps(data) + '\n')

    def _load(self) -> None:
        path = os.path.join(self.config.storage_dir, 'current_collection.jsonl')
        if not os.path.exists(path):
            return
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self._examples.clear()
                for line in f:
                    data = json.loads(line)
                    data['created_at'] = datetime.fromisoformat(data['created_at'])
                    self._examples.append(TrainingExample(**data))
        except Exception as e:
            logger.error(f"Failed to load examples from {path}: {e}")

    @property
    def stats(self) -> Dict[str, Any]:
        total = len(self._examples)
        by_domain: Dict[str, int] = {}
        total_score = 0.0
        scored_count = 0

        for ex in self._examples:
            by_domain[ex.domain] = by_domain.get(ex.domain, 0) + 1
            if ex.feedback_score is not None:
                total_score += ex.feedback_score
                scored_count += 1

        avg_score = total_score / scored_count if scored_count > 0 else 0.0

        return {
            "total_examples": total,
            "by_domain": by_domain,
            "avg_feedback_score": avg_score
        }
