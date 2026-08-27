# H11-MEMS Specification

## Overview
The H11-MEMS agent is dedicated to Micro-Electro-Mechanical Systems (MEMS). It handles the multi-physics complexities associated with microscopic sensors, actuators, fluidics, and optical components, where surface forces often dominate volumetric forces.

## Core Capabilities
- **Multi-Physics Coupling:** Simulates electrostatics, solid mechanics, and fluid dynamics simultaneously (e.g., squeeze-film damping).
- **Yield Analysis:** Predicts failure rates based on microfabrication process variations.
- **Resonator Tuning:** Optimizes quality factor (Q) and resonant frequencies for gyroscopes and RF filters.

## System Architecture
Interacts with layout tools (GDSII) and finite element analysis (FEA) suites to close the loop between conceptual design, behavioral simulation, and physical layout.
