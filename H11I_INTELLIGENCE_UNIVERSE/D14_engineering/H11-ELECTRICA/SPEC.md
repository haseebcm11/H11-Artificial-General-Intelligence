# H11-ELECTRICA Agent Specification

## Abstract
The H11-ELECTRICA agent manages macroscopic electrical systems, encompassing power generation, transmission, distribution, and large-scale industrial electrical design. It focuses on high-voltage and medium-voltage domains.

## Architecture
1. **Grid Simulator**: Models AC/DC power flow, short-circuit faults, and transient stability.
2. **Component Sizer**: Determines appropriate specifications for transformers, switchgear, generators, and cabling.
3. **Renewables Integrator**: Analyzes integration of solar, wind, and storage into the grid.

## State Management
Maintains grid topology, component health states, and dynamic load profiles over time.

## I/O Specifications
- Inputs: Geographic load profiles, generation capacities, grid topology graphs.
- Outputs: Single-line diagrams, load flow reports, arc flash hazard analysis, equipment schedules.
