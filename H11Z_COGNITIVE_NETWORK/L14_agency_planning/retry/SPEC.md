# H11-RETRY: Retry & Recovery Agent

## Overview
The H11-RETRY agent is responsible for resilient task execution and error recovery within the H11 Cognitive Substrate. It implements industry-standard fault-tolerance patterns such as exponential backoff, circuit breaking, fallback strategies, dead-letter queues (DLQ), and compensation actions to ensure robust system operation even under transient failures or rate limits.

## Core Capabilities
1. **Error Classification**: Differentiates between transient (e.g., network timeouts, rate limits) and permanent (e.g., validation failures, unauthorized) errors to determine if a retry is viable.
2. **Retry Policies**: Configurable retry strategies, including exponential backoff with configurable jitter to prevent thundering herd problems.
3. **Circuit Breaker Pattern**: Protects downstream services by tripping (opening) when failure thresholds are exceeded, preventing cascading failures and allowing services to recover.
4. **Fallback Strategies & Graceful Degradation**: Provides alternative execution paths or default values when primary operations fail consistently or circuit breakers are open.
5. **Dead Letter Queue (DLQ)**: Captures permanently failed tasks or tasks that exhaust their retry budgets for manual inspection or later reprocessing.
6. **Compensation Actions (Sagas)**: Orchestrates compensating transactions to undo partial state changes when a multi-step workflow fails.

## Mathematical Foundations
- **Exponential Backoff**: Given attempt $k$, the wait time is $w(k) = \min(w_{max}, w_{base} \cdot 2^k) + \text{jitter}$
- **Circuit Breaker Transition Probability**: Moving from Half-Open to Closed requires $N$ consecutive successful probes.

## Integration
H11-RETRY acts as a middleware or decorator for inter-agent communication and external API calls. Agents can submit tasks to H11-RETRY or query it for the next scheduled execution time and policy evaluation.
