from __future__ import annotations
import json
import logging
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Set
from .collector import TrainingExample

logger = logging.getLogger(__name__)

@dataclass
class DistilledRule:
    rule_id: str
    agent_id: str
    domain: str
    condition: str
    action: str
    confidence: float
    source_examples: List[str]
    created_at: datetime
    validated: bool = False

class KnowledgeDistiller:
    def distill_from_examples(self, examples: List[TrainingExample], min_confidence: float = 0.7) -> List[DistilledRule]:
        logger.info(f"Distilling rules from {len(examples)} examples.")
        rules: List[DistilledRule] = []
        
        # Simulated distillation logic mapping patterns to rules
        for ex in examples:
            if ex.feedback_score is not None and ex.feedback_score >= min_confidence:
                rule_id = str(uuid.uuid4())
                condition = f"Condition derived from query: {ex.query[:50]}"
                action = f"Action derived from output: {str(ex.agent_output)[:50]}"
                
                rule = DistilledRule(
                    rule_id=rule_id,
                    agent_id=ex.agent_id,
                    domain=ex.domain,
                    condition=condition,
                    action=action,
                    confidence=ex.feedback_score,
                    source_examples=[ex.example_id],
                    created_at=datetime.utcnow(),
                    validated=False
                )
                rules.append(rule)
        
        logger.info(f"Distilled {len(rules)} potential rules.")
        return rules

    def merge_rules(self, existing: List[DistilledRule], new: List[DistilledRule]) -> List[DistilledRule]:
        merged_dict: Dict[str, DistilledRule] = {}
        
        for rule in existing:
            # Simple unique key based on condition and action for deduplication
            key = f"{rule.condition}::{rule.action}"
            merged_dict[key] = rule
            
        for rule in new:
            key = f"{rule.condition}::{rule.action}"
            if key in merged_dict:
                existing_rule = merged_dict[key]
                # Increase confidence slightly, merge sources
                existing_rule.confidence = min(1.0, existing_rule.confidence + 0.05)
                existing_rule.source_examples.extend(rule.source_examples)
                existing_rule.source_examples = list(set(existing_rule.source_examples))
            else:
                merged_dict[key] = rule
                
        return list(merged_dict.values())

    def validate_rule(self, rule: DistilledRule, test_examples: List[TrainingExample]) -> float:
        # Simulated validation logic
        if not test_examples:
            return 0.0
            
        applicable = [ex for ex in test_examples if ex.domain == rule.domain]
        if not applicable:
            return 0.0
            
        # Pretend we evaluated the rule against the test examples
        match_count = min(len(applicable), max(1, int(len(applicable) * rule.confidence)))
        accuracy = match_count / len(applicable)
        
        rule.validated = accuracy >= 0.8
        logger.info(f"Rule {rule.rule_id} validated with accuracy {accuracy:.2f}")
        return accuracy

    def export_rules(self, rules: List[DistilledRule], path: str) -> None:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                data = []
                for rule in rules:
                    r_dict = asdict(rule)
                    r_dict['created_at'] = rule.created_at.isoformat()
                    data.append(r_dict)
                json.dump(data, f, indent=2)
            logger.info(f"Exported {len(rules)} rules to {path}")
        except Exception as e:
            logger.error(f"Failed to export rules to {path}: {e}")
