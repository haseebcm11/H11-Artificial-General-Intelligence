# H11-GUARDRAIL (Guardrails)

## Overview
H11-GUARDRAIL implements hard constraints and rapid-response circuit breakers. It operates at a lower latency than H11-ALIGN, functioning as a real-time filter on input/output streams and intermediate cognitive operations to prevent policy violations.

## Architecture
- **Filter Bank**: A set of deterministic and fast-heuristic filters (e.g., regex, fast classifiers).
- **Circuit Breaker System**: State-machine-based tripwires that immediately halt execution if catastrophic constraints are breached.
- **Violation Logging**: High-fidelity recording of triggered guardrails for post-hoc analysis by the Alignment module.

## Interfaces
- `check_operation(op: Operation) -> GuardrailResult`
- `trigger_breaker(breaker_id: str) -> None`
- `update_filters(new_filters: List[FilterDef]) -> None`
