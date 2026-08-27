# H11-3DPRINT Agent Specification

## Abstract
The H11-3DPRINT agent coordinates advanced additive manufacturing processes. It translates generic geometric requirements into machine-specific G-code, optimizing toolpaths for structural integrity, surface finish, and minimal material waste. The agent supports FDM, SLA, and SLS technologies.

## Core Responsibilities
1. **Model Analysis**: Validates STL/OBJ files for manifold errors, overhangs, and thin walls.
2. **Slicing & Toolpath Generation**: Produces optimized G-code with adaptive layer heights and custom infill patterns (e.g., gyroid, cubic).
3. **Print Monitoring**: Uses computer vision to detect print failures (spaghetti, warping, layer shifts) in real-time.
4. **Material Management**: Tracks filament/resin usage and schedules automatic swaps or refills.

## Technical Interfaces
- OctoPrint API / Moonraker API for direct printer control.
- OpenCV/TensorFlow for real-time defect detection via webcam streams.

## Failure Modes & Contingencies
- **Thermal Runaway**: Instantly halts print and severs power via smart relays.
- **Filament Runout**: Pauses print, stores precise Cartesian coordinates, and alerts H11-ASSEMBLY or human operators.

## Integration Points
- Receives models from CAD design sub-agents.
- Hands off completed parts to H11-ASSEMBLY or H11-QUALITAS.
