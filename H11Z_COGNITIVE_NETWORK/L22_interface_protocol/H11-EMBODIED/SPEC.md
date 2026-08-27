# H11-EMBODIED Specification

## Overview
The H11-EMBODIED agent bridges the gap between semantic understanding (language, high-level reasoning) and physical environments. It implements Embodied AI methodologies to ground symbols in physical reality, enabling robots to reason about their surroundings, understand affordances, and translate natural language instructions into actionable physical skills.

## Core Responsibilities
1.  **Grounded Language Understanding**: Translating abstract concepts and linguistic commands into specific spatial, temporal, and physical contexts.
2.  **Affordance Learning**: Recognizing actionable properties of objects within the environment (e.g., a mug is graspable, a button is pressable).
3.  **Physical Common Sense**: Applying intuitive physics (gravity, collision, containment) to predict outcomes of actions and validate planned trajectories.
4.  **Semantic Scene Graphs**: Maintaining a dynamic, relational graph of the environment, integrating visual perception with semantic labels and object states.

## Technical Mechanisms
-   **SayCan & Inner Monologue Frameworks**: Utilizing Large Language Models (LLMs) to score the probability of a language command matching a set of pre-trained, feasible skills (value functions).
-   **Visual Language Models (VLMs)**: Employing models like CLIP, ViLD, or Open-Vocab detectors to ground bounding boxes and point clouds to language embeddings.
-   **Skill Sequences & Code-as-Policies**: Translating high-level reasoning into executable Python code or skill primitives that parameterize lower-level control loops.
-   **Spatial Memory**: Maintaining an egocentric to allocentric mapping of the world for long-horizon planning and navigation.
