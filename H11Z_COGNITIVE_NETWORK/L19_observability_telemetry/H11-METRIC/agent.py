import math
import re
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

AGENT_ID = "H11-METRIC"

@dataclass
class MetricInput:
    raw_logs: List[str]
    ema_alpha: float
    percentiles: List[float]

@dataclass
class MetricOutput:
    ema_values: List[float]
    percentile_results: Dict[float, float]
    cardinality: int
    parsed_logs: List[Dict[str, Any]]

class MetricProcessingException(Exception):
    pass

class MetricAgent:
    """
    Computes EMA smoothing, percentiles, metric cardinality, and structured log parsing.
    """
    def process(self, input_data: MetricInput) -> MetricOutput:
        parsed_logs = []
        values = []
        log_pattern = re.compile(r"\[(?P<timestamp>[^\]]+)\] (?P<level>\w+) (?P<message>.*) value=(?P<value>\d+\.?\d*)")
        
        unique_labels = set()
        
        for log in input_data.raw_logs:
            match = log_pattern.search(log)
            if match:
                parsed = match.groupdict()
                parsed["value"] = float(parsed["value"])
                parsed_logs.append(parsed)
                values.append(parsed["value"])
                unique_labels.add(parsed["message"])
                
        if not values:
            raise MetricProcessingException("No valid metrics found in logs")
            
        ema_values = [values[0]]
        for val in values[1:]:
            ema_values.append(input_data.ema_alpha * val + (1 - input_data.ema_alpha) * ema_values[-1])
            
        sorted_vals = sorted(values)
        percentile_results = {}
        for p in input_data.percentiles:
            k = (len(sorted_vals) - 1) * p
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                percentile_results[p] = sorted_vals[int(k)]
            else:
                d0 = sorted_vals[int(f)] * (c - k)
                d1 = sorted_vals[int(c)] * (k - f)
                percentile_results[p] = d0 + d1
                
        return MetricOutput(
            ema_values=ema_values,
            percentile_results=percentile_results,
            cardinality=len(unique_labels),
            parsed_logs=parsed_logs
        )
