import re
import math
import random
import hashlib
from typing import List, Dict, Any, Union, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger("H11_PRIVACY_DATA")

class PrivacyLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    STRICT = "strict"

@dataclass
class PrivacyConfig:
    level: PrivacyLevel = PrivacyLevel.MEDIUM
    k_target: int = 5
    epsilon_budget: float = 2.0
    masking_char: str = "*"
    salt: str = "H11_SECURE_SALT_991"

@dataclass
class PrivacyState:
    epsilon_consumed: float = 0.0
    redacted_counts: Dict[str, int] = field(default_factory=dict)
    
@dataclass
class PrivacyInput:
    data: Union[str, List[Dict[str, Any]]]
    quasi_identifiers: Optional[List[str]] = None
    sensitive_numerical_fields: Optional[List[str]] = None

@dataclass
class PrivacyOutput:
    sanitized_data: Union[str, List[Dict[str, Any]]]
    metrics: Dict[str, Any]

class H11PrivacyAgent:
    """
    H11-PRIVACY-DATA: Handles deterministic scrubbing and differential privacy.
    """
    
    # Common PII Regexes
    REGEX_EMAIL = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    REGEX_SSN = r'\b\d{3}-\d{2}-\d{4}\b'
    REGEX_CC = r'\b(?:\d[ -]*?){13,16}\b'
    
    def __init__(self, config: PrivacyConfig):
        self.config = config
        self.state = PrivacyState()
        logger.info(f"Initialized H11-PRIVACY-DATA with level {self.config.level.value}")

    def process(self, payload: PrivacyInput) -> PrivacyOutput:
        if isinstance(payload.data, str):
            return self._scrub_unstructured(payload.data)
        elif isinstance(payload.data, list):
            return self._anonymize_structured(payload)
        else:
            raise ValueError("Unsupported data type for privacy processing.")

    def _scrub_unstructured(self, text: str) -> PrivacyOutput:
        """
        Regex and pseudo-NER text masking.
        """
        metrics = {"emails": 0, "ssns": 0, "ccs": 0}
        
        def replacer_email(match):
            metrics["emails"] += 1
            return "[EMAIL_REDACTED]"
            
        def replacer_ssn(match):
            metrics["ssns"] += 1
            return "[SSN_REDACTED]"
            
        def replacer_cc(match):
            metrics["ccs"] += 1
            return "[CC_REDACTED]"

        sanitized = re.sub(self.REGEX_EMAIL, replacer_email, text)
        sanitized = re.sub(self.REGEX_SSN, replacer_ssn, sanitized)
        sanitized = re.sub(self.REGEX_CC, replacer_cc, sanitized)
        
        # Update global state
        for k, v in metrics.items():
            self.state.redacted_counts[k] = self.state.redacted_counts.get(k, 0) + v
            
        return PrivacyOutput(
            sanitized_data=sanitized,
            metrics={"redactions": metrics}
        )

    def _anonymize_structured(self, payload: PrivacyInput) -> PrivacyOutput:
        """
        Applies k-anonymity (generalization) and Differential Privacy (Laplace noise).
        """
        data = [dict(row) for row in payload.data] # Deep copy dicts
        metrics = {}
        
        # 1. Differential Privacy on numerical fields
        if payload.sensitive_numerical_fields and self.config.level in [PrivacyLevel.MEDIUM, PrivacyLevel.STRICT]:
            eps_per_query = 0.1
            if self.state.epsilon_consumed + eps_per_query > self.config.epsilon_budget:
                logger.warning("Privacy budget exhausted! Cannot add safe DP noise. Redacting completely.")
                for row in data:
                    for field in payload.sensitive_numerical_fields:
                        if field in row:
                            row[field] = None
            else:
                self.state.epsilon_consumed += eps_per_query
                metrics["dp_applied"] = True
                metrics["epsilon_consumed"] = eps_per_query
                
                # Assume global sensitivity Δf = 100 for demonstration
                sensitivity = 100.0
                scale = sensitivity / eps_per_query
                
                for row in data:
                    for field in payload.sensitive_numerical_fields:
                        if field in row and isinstance(row[field], (int, float)):
                            noise = self._laplace_mechanism(scale)
                            row[field] += noise
                            
        # 2. Pseudonymization of explicit identifiers
        for row in data:
            if "user_id" in row:
                row["user_id"] = self._hash_id(str(row["user_id"]))
                
        # 3. Simple k-anonymity generalization on QIs
        # A real implementation uses Mondrian multidimensional partitioning.
        # This is a stub generalizing 'age' and 'zipcode'
        if payload.quasi_identifiers:
            for row in data:
                if "age" in payload.quasi_identifiers and "age" in row:
                    # Bin ages to decades
                    age = int(row["age"])
                    row["age"] = f"{age//10 * 10}-{(age//10 * 10) + 9}"
                if "zipcode" in payload.quasi_identifiers and "zipcode" in row:
                    # Strip last 2 digits
                    row["zipcode"] = str(row["zipcode"])[:3] + "**"
                    
            metrics["k_anonymity_attempted"] = True
            metrics["qis"] = payload.quasi_identifiers
            
        return PrivacyOutput(
            sanitized_data=data,
            metrics=metrics
        )

    def _laplace_mechanism(self, scale: float) -> float:
        """Draws noise from a Laplace distribution (0, scale)."""
        u = random.uniform(-0.5, 0.5)
        return -scale * math.copysign(1.0, u) * math.log(1 - 2 * abs(u))

    def _hash_id(self, identifier: str) -> str:
        """Securely pseudo-anonymize an identifier."""
        salted = self.config.salt + identifier
        return hashlib.sha256(salted.encode('utf-8')).hexdigest()[:12]

if __name__ == "__main__":
    agent = H11PrivacyAgent(PrivacyConfig(level=PrivacyLevel.STRICT))
    
    # Test unstructured
    text = "Contact john.doe@example.com or call, SSN is 123-45-6789."
    out_text = agent.process(PrivacyInput(data=text))
    print(f"Scrubbed Text: {out_text.sanitized_data}")
    print(f"Metrics: {out_text.metrics}")
    
    # Test structured
    rows = [
        {"user_id": "U1", "age": 34, "zipcode": "90210", "salary": 55000},
        {"user_id": "U2", "age": 36, "zipcode": "90212", "salary": 60000}
    ]
    out_struct = agent.process(PrivacyInput(
        data=rows, 
        quasi_identifiers=["age", "zipcode"], 
        sensitive_numerical_fields=["salary"]
    ))
    print(f"Sanitized Data:")
    for r in out_struct.sanitized_data:
        print(" ", r)
