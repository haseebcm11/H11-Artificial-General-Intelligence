import random
import logging
from typing import List, Dict, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum, auto

logger = logging.getLogger("H11-AUGMENTER")

class ModalityType(Enum):
    TEXT = auto()
    TENSOR_IMAGE = auto()
    AUDIO = auto()

@dataclass
class DataPayload:
    id: str
    content: Any  # str for text, List/Array for tensors
    labels: Any
    lineage: List[str] = field(default_factory=list)

@dataclass
class AugmentationPolicy:
    n_ops: int = 2
    magnitude: int = 5  # Scale 0 to 10
    include_original: bool = True

class TextAugmenter:
    """Implements Easy Data Augmentation (EDA) and Paraphrasing stubs."""
    def __init__(self):
        self.synonyms = {"good": ["excellent", "great"], "bad": ["terrible", "poor"]}

    def random_synonym_replace(self, text: str, magnitude: int) -> str:
        words = text.split()
        num_replace = max(1, int(len(words) * (magnitude / 10.0) * 0.3))
        
        for _ in range(num_replace):
            idx = random.randint(0, len(words) - 1)
            word = words[idx]
            if word in self.synonyms:
                words[idx] = random.choice(self.synonyms[word])
        return " ".join(words)

    def random_deletion(self, text: str, magnitude: int) -> str:
        words = text.split()
        if len(words) <= 1: return text
        
        prob = (magnitude / 10.0) * 0.2
        kept_words = [w for w in words if random.random() > prob]
        return " ".join(kept_words) if kept_words else words[0]

class TensorAugmenter:
    """Implements MixUp and Manifold mutations for numeric arrays."""
    
    def mixup(self, t1: List[float], t2: List[float], alpha: float = 0.2) -> List[float]:
        # Beta distribution stub for lambda
        lam = max(0.1, min(0.9, random.betavariate(alpha, alpha)))
        
        # Mix features
        mixed = []
        for v1, v2 in zip(t1, t2):
            mixed.append(v1 * lam + v2 * (1 - lam))
        return mixed

class RandAugmentOrchestrator:
    """Core Agent for H11-AUGMENTER implementing RandAugment policy."""
    
    def __init__(self):
        self.text_aug = TextAugmenter()
        self.tensor_aug = TensorAugmenter()
        
        # Define available operations per modality
        self.text_ops: List[Callable] = [
            self.text_aug.random_synonym_replace,
            self.text_aug.random_deletion
        ]
        logger.info("Initialized H11-AUGMENTER Agent")

    def augment_batch(self, batch: List[DataPayload], modality: ModalityType, policy: AugmentationPolicy) -> List[DataPayload]:
        output_batch = []
        
        for item in batch:
            if policy.include_original:
                output_batch.append(item)
                
            mutated_content = item.content
            lineage = item.lineage.copy()
            
            # Apply N operations sequentially
            for _ in range(policy.n_ops):
                if modality == ModalityType.TEXT:
                    op = random.choice(self.text_ops)
                    mutated_content = op(mutated_content, policy.magnitude)
                    lineage.append(op.__name__)
                elif modality == ModalityType.TENSOR_IMAGE:
                    # Specialized flow for mixup requiring pairs
                    target = random.choice(batch)
                    mutated_content = self.tensor_aug.mixup(mutated_content, target.content)
                    lineage.append(f"mixup_with_{target.id}")
                    break # MixUp is usually terminal in a chain
                    
            output_batch.append(DataPayload(
                id=f"{item.id}_aug",
                content=mutated_content,
                labels=item.labels, # Note: Mixup requires label blending in full impl
                lineage=lineage
            ))
            
        logger.info(f"Augmented batch of {len(batch)} -> {len(output_batch)} items")
        return output_batch
