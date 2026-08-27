# H11-CHAIN Specification

## Overview
The `H11-CHAIN` agent implements Chain-of-Thought (CoT) prompting and self-consistency protocols. It encourages language models and sub-symbolic systems to emit intermediate computation steps ("thinking step-by-step") before yielding a final answer, vastly improving performance on logic, math, and common-sense reasoning.

## Core Capabilities
- **CoT Prompting**: Automatically structures zero-shot and few-shot CoT sequences.
- **Faithfulness Tracking**: Assesses whether the model's actual reasoning aligns with its generated textual chain.
- **Self-Consistency**: Samples multiple reasoning paths and marginalizes over them to find the most consistent final answer (majority voting or expected value).
- **Intermediate Computation Extraction**: Parses CoT traces to extract intermediate variable states or math derivations.

## Theoretical Foundations
- **Chain of Thought**: Wei et al., 2022 ("Chain-of-Thought Prompting Elicits Reasoning in Large Language Models").
- **Self-Consistency**: Wang et al., 2022 ("Self-Consistency Improves Chain of Thought Reasoning in Language Models").

## Data Structures
- `PromptTemplate`: Manages the few-shot exemplars and instructions.
- `ThoughtStep`: A discrete textual or symbolic chunk representing one reasoning operation.
- `ConsistencyEnsemble`: A collection of parallel CoT outputs used for voting.
