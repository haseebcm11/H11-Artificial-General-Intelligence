# H11-API-USE (External API Integration Agent)

## 1. Overview
The H11-API-USE agent provides a unified cognitive substrate for planning, composing, and executing calls across disparate external APIs (REST, GraphQL, gRPC). It is responsible for handling the complex non-functional requirements of API interaction, including rate limiting, cursor-based pagination, resilient error handling, and cross-API data composition.

## 2. Core Architecture
- **Protocol Adapters**: Specialized drivers for REST (HTTP/1.1 and HTTP/2), GraphQL (query extraction and mutation synthesis), and gRPC (protobuf serialization/deserialization).
- **Dynamic Rate Limiter**: Implements an advanced Token Bucket algorithm with predictive refill rates based on heuristic analysis of `Retry-After` headers and endpoint SLA tiers.
- **Universal Paginator**: An abstract iterator over API endpoints supporting multiple strategies:
  - Offset/Limit based
  - Keyset/Cursor based
  - Link Header (RFC 5988) based
- **Error Interpretation Engine**: Classifies errors into transient (network issues, 503s), semi-transient (429s, requiring backoff), and terminal (400s, 401s, requiring structural payload adjustments).

## 3. Advanced Capabilities
- **API Composition**: The agent can chain responses from one API directly into requests for another, building an execution DAG (Directed Acyclic Graph) of operations.
- **Schema Induction**: Attempts to infer the schema of undocumented JSON responses to provide typed downstream objects.
- **Key Management Security**: Integrates with secure vaults and automatically rotates compromised or expired tokens during execution.
