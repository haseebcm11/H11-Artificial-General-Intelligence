# H11-INTENT (Intent Formation & Recognition)

## Overview
H11-INTENT is responsible for parsing, disambiguating, and forming intents from both user inputs and internal agent state. It maps ambiguous inputs into structured intent slots, handles multi-intent scenarios, and performs intent-to-action mapping using probabilistic semantic slot filling and implicit intent detection via contextual anomaly analysis.

## Core Mechanisms
1. **Probabilistic Intent Classification:** Utilizes a generative hierarchical model to map utterances into primary and secondary intents.
2. **Semantic Slot Filling:** Extracts entities and aligns them with intent frames (intent slots).
3. **Implicit Intent Detection:** Detects unspoken intents by comparing explicit utterances with historical behavior trajectories and context graphs.
4. **Disambiguation Engine:** Generates clarification requests or multi-hypothesis action maps when intent confidence is below a threshold.

## Architecture
- `IntentParser`: The main entrypoint for text-to-intent.
- `ContextGraph`: Tracks conversational state to infer implicit intents.
- `ActionMapper`: Translates intent frames into actionable primitives.
