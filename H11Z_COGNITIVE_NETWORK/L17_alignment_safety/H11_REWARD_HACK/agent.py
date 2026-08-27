import numpy as np
from collections import deque
from dataclasses import dataclass
from typing import List, Deque

@dataclass
class MetricSnapshot:
    timestamp: float
    proxy: float
    secondaries: List[float]

class DivergenceMonitor:
    def __init__(self, window_size: int = 100, threshold: float = -0.7):
        self.window_size = window_size
        self.threshold = threshold
        self.history: Deque[MetricSnapshot] = deque(maxlen=window_size)
        
    def add_snapshot(self, snapshot: MetricSnapshot):
        self.history.append(snapshot)
        
    def compute_divergence(self) -> float:
        """
        Computes the correlation between the proxy metric and the average of secondary metrics.
        Returns the correlation coefficient. A strong negative correlation suggests reward hacking.
        """
        if len(self.history) < 10:
            return 0.0 # Not enough data
            
        proxies = np.array([s.proxy for s in self.history])
        # Average the secondary metrics for a stable true-objective indicator
        secondaries = np.array([np.mean(s.secondaries) for s in self.history])
        
        # Calculate gradients (differences) to detect trend divergence
        dp = np.diff(proxies)
        ds = np.diff(secondaries)
        
        if np.std(dp) == 0 or np.std(ds) == 0:
            return 0.0
            
        correlation = np.corrcoef(dp, ds)[0, 1]
        return correlation

class RewardHackDetectorAgent:
    def __init__(self):
        self.monitor = DivergenceMonitor()
        
    def process_telemetry(self, timestamp: float, proxy: float, secondaries: List[float]) -> dict:
        self.monitor.add_snapshot(MetricSnapshot(timestamp, proxy, secondaries))
        corr = self.monitor.compute_divergence()
        
        is_hacking = corr < self.monitor.threshold
        
        return {
            "divergence_correlation": corr,
            "reward_hacking_detected": bool(is_hacking),
            "alert_level": "CRITICAL" if is_hacking else "NORMAL"
        }

if __name__ == "__main__":
    agent = RewardHackDetectorAgent()
    # Simulate normal behavior (positive correlation)
    for i in range(20):
        agent.process_telemetry(i, float(i), [float(i), float(i*1.1)])
    print("Normal status:", agent.process_telemetry(21, 21.0, [21.0, 22.0]))
    
    # Simulate reward hacking (proxy goes up, secondaries tank)
    for i in range(22, 50):
        agent.process_telemetry(i, float(i), [float(100 - i), float(100 - i*1.2)])
    print("Hack status:", agent.process_telemetry(50, 50.0, [50.0, 40.0]))
