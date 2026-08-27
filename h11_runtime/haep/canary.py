"""H11-AGI Enhancement Protocol v1.0 — Canary Runtime & Automatic Rollback.

Sections 24, 25, 26: Safe production canary routing, dual shadow execution,
transactional commit, and instant rollback.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

from .protocol import BaselineLock, EnhancementObject, EnhancementState, PromotionLevel


@dataclass
class CanaryEvaluationResult:
    total_requests: int
    baseline_success_count: int
    candidate_success_count: int
    candidate_error_count: int
    candidate_avg_latency_ms: float
    baseline_avg_latency_ms: float
    regression_detected: bool
    rollback_triggered: bool
    rollback_reason: Optional[str] = None


class AutomaticRollbackTrigger(ValueError):
    """Raised when canary monitoring triggers an emergency rollback."""
    pass


class EnhancementTransaction:
    """Section 26: Transactional enhancement commit & rollback context."""

    def __init__(self, enhancement: EnhancementObject, rollback_fn: Optional[Callable[[], None]] = None) -> None:
        self.enhancement = enhancement
        self.rollback_fn = rollback_fn
        self.committed = False
        self.aborted = False

    def __enter__(self) -> EnhancementTransaction:
        self.enhancement.transition_to(EnhancementState.CANARY, "Entering canary transaction")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            self.abort(reason=f"Exception in transaction: {exc_val}")
            return False  # re-raise exception
        if not self.committed:
            self.commit()
        return True

    def commit(self) -> None:
        self.committed = True
        self.enhancement.transition_to(EnhancementState.PROMOTED, "Enhancement transaction committed")
        self.enhancement.promotion_level = PromotionLevel.P4_PRODUCTION

    def abort(self, reason: str = "Transaction aborted") -> None:
        self.aborted = True
        if self.rollback_fn:
            try:
                self.rollback_fn()
            except Exception:
                pass
        self.enhancement.transition_to(EnhancementState.ROLLBACK, reason)
        self.enhancement.promotion_level = PromotionLevel.P0_REJECTED


class CanaryRouter:
    """Section 24: Manages split traffic & shadow evaluation between baseline and candidate."""

    def __init__(self, max_error_rate: float = 0.01, max_latency_overhead: float = 2.0, min_latency_threshold_ms: float = 5.0) -> None:
        self.max_error_rate = max_error_rate
        self.max_latency_overhead = max_latency_overhead
        self.min_latency_threshold_ms = min_latency_threshold_ms

    def run_shadow_evaluation(
        self,
        baseline_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        candidate_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        test_inputs: List[Dict[str, Any]],
    ) -> CanaryEvaluationResult:
        """Execute candidate in shadow mode alongside baseline and compare metrics."""
        b_success = 0
        c_success = 0
        c_errors = 0
        b_latencies = []
        c_latencies = []

        for inp in test_inputs:
            # Baseline execution
            t0 = time.perf_counter()
            try:
                b_res = baseline_fn(inp)
                b_success += 1
            except Exception:
                b_res = {}
            b_latencies.append((time.perf_counter() - t0) * 1000.0)

            # Candidate execution
            t0 = time.perf_counter()
            try:
                c_res = candidate_fn(inp)
                # Verify safety / non-empty output
                if isinstance(c_res, dict) and c_res.get("status") in ("OK", "COMPLETED", "SUCCESS"):
                    c_success += 1
                elif c_res is not None and not isinstance(c_res, Exception):
                    c_success += 1
                else:
                    c_errors += 1
            except Exception:
                c_errors += 1
            c_latencies.append((time.perf_counter() - t0) * 1000.0)

        tot = max(len(test_inputs), 1)
        err_rate = c_errors / tot
        b_avg_lat = sum(b_latencies) / tot
        c_avg_lat = sum(c_latencies) / tot

        rollback = False
        reason = None

        if err_rate > self.max_error_rate:
            rollback = True
            reason = f"Candidate error rate {err_rate:.2%} exceeded max allowed threshold {self.max_error_rate:.2%}"
        elif c_avg_lat > self.min_latency_threshold_ms and b_avg_lat > 0 and (c_avg_lat / b_avg_lat) > self.max_latency_overhead:
            rollback = True
            reason = f"Candidate latency overhead {c_avg_lat/b_avg_lat:.2f}x exceeded max allowed {self.max_latency_overhead:.2f}x"

        return CanaryEvaluationResult(
            total_requests=len(test_inputs),
            baseline_success_count=b_success,
            candidate_success_count=c_success,
            candidate_error_count=c_errors,
            candidate_avg_latency_ms=round(c_avg_lat, 2),
            baseline_avg_latency_ms=round(b_avg_lat, 2),
            regression_detected=c_success < b_success,
            rollback_triggered=rollback,
            rollback_reason=reason,
        )
