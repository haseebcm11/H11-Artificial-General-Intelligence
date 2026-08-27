> **Layer 20** · Security, Integrity & Resilience · `H11-PROMPTGUARD`

## Purpose

The H11-PROMPTGUARD agent is responsible for prompt-injection defense within the H11 Cognitive Substrate. Prompt security: direct/indirect prompt injection, instruction hierarchy, input/output sanitization, prompt injection detection classifiers, delimiter strategies, system prompt protection.

This agent ensures robust operational security by continuously monitoring and enforcing policies relevant to its domain. It acts as a foundational pillar, preventing malicious exploitation and ensuring that cognitive processes run within safe, intended boundaries.

## Technical Deep-Dive

Enforces an Instruction Hierarchy where system directives strictly override user inputs. Uses an LLM-based zero-shot classifier and robust delimiting (e.g., `<|user_input|>`) to sanitize external text, detecting indirect injections.

It leverages advanced algorithms optimized for low-latency operations, ensuring security checks do not bottleneck cognitive processing. The architecture is modular, allowing plug-and-play integrations with external hardware security modules (HSMs) or external threat intelligence feeds where applicable.

State management is tightly controlled to prevent cross-contamination or state-based attacks. Cryptographic boundaries are maintained using memory-safe operations, and sensitive state is aggressively zeroed out when no longer required.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `user_prompt` | `PromptInput` | Raw user text |
| `context` | `SecurityContext` | Metadata including timestamp, source, and tracing ID |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `safe_prompt` | `SafePrompt` | Sanitized and structured prompt |
| `audit_log` | `AuditRecord` | Cryptographically signed log of the decision/action |

### State Schema
- **`classifier_weights`**: Weights for lightweight injection classifier
- **`attack_history`**: Logged injection attempts

## Dependencies

### Upstream (depends on)
- H11-ZEROTRUST: For baseline identity and context verification.

### Downstream (feeds into)
- H11-THREAT: Feeds telemetry and anomaly data for broader correlation.

## Failure Modes
- Policy engine latency exceeding timeout thresholds.
- Exhaustion of secure memory or key handle limits.
- Desynchronization with global state ledgers or threat feeds.

## Performance Characteristics
- Latency: < 5ms per synchronous check.
- Throughput: 10,000+ operations/sec per core.
- Memory: Bounded, with aggressive eviction policies for cached state.

## Research References
- NIST SP 800-207 (Zero Trust Architecture)
- MITRE ATT&CK and ATLAS Frameworks

## Implementation Notes
Focus on avoiding side-channel leaks (e.g., constant-time string comparisons where applicable). Fail closed unless explicit configuration dictates a fail-open posture for availability.
