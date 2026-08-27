# H11-FUNCTION-CALL Specification

## Overview
The Function Calling agent is responsible for extracting structured arguments from natural language and mapping them into strict JSON schemas formatted as OpenAI function definitions. It supports parallel function execution, nested/dependent function invocation (e.g., passing the output of one tool into another), and dynamic schema validation with automated retry loops for malformed LLM outputs.

## Mathematical Foundation
Let $\mathcal{F} = \{f_1, f_2, \dots, f_n\}$ be a set of available functions, where each function $f_i$ is associated with a JSON schema $S_i$. Let $U$ be a natural language utterance.
The goal is to find a set of function calls $C = \{(f_{k_1}, A_1), \dots, (f_{k_m}, A_m)\}$ such that each argument set $A_j$ satisfies the schema $S_{k_j}$.

For nested calls, we represent $C$ as a directed acyclic graph $G = (V, E)$ where each vertex $v \in V$ is a function call and an edge $(v_a, v_b)$ indicates that the output of $v_a$ is an argument to $v_b$.

Validation relies on finding a morphism from the extracted JSON to the expected schema tree.

## Architecture
- **Schema Registry**: Holds Pydantic-based schemas or raw JSON schemas.
- **Extraction Engine**: Uses few-shot or structured LLM requests to generate JSON blocks.
- **Dependency Resolver**: Topologically sorts nested function calls to execute them in parallel where possible.
- **Validator**: Ensures arguments conform strictly to schemas.
- **Recovery Manager**: Retries failed validations by appending error messages to the prompt.
