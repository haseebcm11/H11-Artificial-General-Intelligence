# H11-ANALOGY: Analogical Reasoning Agent

## Overview
The H11-ANALOGY agent handles structural mapping between a source domain and a target domain. It leverages Gentner's Structure-Mapping Theory to identify parallel relational structures across domains.

## Theoretical Foundations
- **Structure-Mapping Theory (SMT)**: Analogy is defined as a mapping of knowledge from a base domain to a target domain, guided by structural similarities rather than surface attributes.
- **Systematicity Principle**: A preference for mappings that belong to higher-order relational structures (e.g., causal chains).
- **Structure Mapping Engine (SME)**: The algorithmic formulation that constructs local matches and merges them into globally consistent mappings.

## Architecture
1. **Local Matcher**: Identifies potential pairings between relations and attributes in the source and target.
2. **Structural Consistency Filter**: Enforces 1-to-1 mapping and parallel connectivity (if relations map, their arguments must map).
3. **Global Evaluator**: Computes a structural evaluation score based on depth and systematicity.
