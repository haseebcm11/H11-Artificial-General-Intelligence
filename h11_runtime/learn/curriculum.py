from __future__ import annotations
import uuid
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

@dataclass
class CurriculumStage:
    stage_id: str
    name: str
    domain: str
    difficulty: int
    topics: List[str]
    seed_queries: List[str]
    prerequisite_stages: List[str]

@dataclass
class Curriculum:
    curriculum_id: str
    stages: List[CurriculumStage]
    target_domain: str
    created_at: datetime

class CurriculumGenerator:
    def __init__(self):
        self.templates = {
            "financial": ["Basic Accounting", "Market Mechanics", "Derivatives", "Algorithmic Trading"],
            "medical": ["Anatomy", "Diagnostics", "Pharmacology", "Surgical Procedures"],
            "legal": ["Contracts", "Torts", "Corporate Law", "Intellectual Property"]
        }

    def generate_curriculum(self, domain: str, num_stages: int = 10) -> Curriculum:
        logger.info(f"Generating curriculum for domain: {domain} with {num_stages} stages")
        stages: List[CurriculumStage] = []
        topics = self.templates.get(domain, [f"Topic {i}" for i in range(1, num_stages + 1)])
        
        prev_stage_id = None
        for i in range(num_stages):
            stage_id = str(uuid.uuid4())
            topic_idx = min(i, len(topics) - 1)
            
            stage = CurriculumStage(
                stage_id=stage_id,
                name=f"Stage {i+1}: {topics[topic_idx]}",
                domain=domain,
                difficulty=(i % 10) + 1,
                topics=[topics[topic_idx]],
                seed_queries=[f"Explain {topics[topic_idx]} basics.", f"Advanced {topics[topic_idx]} problems."],
                prerequisite_stages=[prev_stage_id] if prev_stage_id else []
            )
            stages.append(stage)
            prev_stage_id = stage_id

        return Curriculum(
            curriculum_id=str(uuid.uuid4()),
            stages=stages,
            target_domain=domain,
            created_at=datetime.utcnow()
        )

    def generate_queries(self, stage: CurriculumStage, count: int = 50) -> List[str]:
        logger.info(f"Generating {count} queries for stage {stage.name}")
        queries = []
        for i in range(count):
            base = stage.seed_queries[i % len(stage.seed_queries)]
            queries.append(f"{base} (Variation {i+1})")
        return queries
