> **Layer 19** · Arts, Design & Creativity · `H11-PAINTING`

## Purpose

The H11-PAINTING agent is designed to simulate, analyze, and synthesize digital painting workflows. It models physical properties of paint, fluid dynamics, and canvas textures to create hyper-realistic or highly stylized painterly outputs.

## Technical Deep-Dive

Utilizing smoothed-particle hydrodynamics (SPH) for simulating paint viscosity and blending, this agent goes beyond simple color overlays. It computes Kubelka-Munk theory equations to simulate the reflectance and transmittance of layered pigments, allowing for realistic glazing and scumbling effects.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| image_data | bytes | Reference image data |
| target_medium | MediumType | Oil, Acrylic, etc. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| synthesized_layers | List[bytes] | Final layers |
| stroke_paths | List[Dict] | Vector paths of brushstrokes |

### State Schema
- `active_layers`: Tracks memory allocated to layers.
- `is_drying`: Boolean state for physical drying simulation.

## Dependencies

### Upstream (depends on)
- H11-VISION: For reference image understanding.

### Downstream (feeds into)
- H11-DIGITALART: For further digital compositing.

## Failure Modes
- Canvas tearing: Over-saturation of virtual water in watercolor simulation.
- Out of memory: Too many unmerged layers.

## Performance Characteristics
GPU heavy. SPH simulation requires massive parallel compute.

## Research References
- Kubelka-Munk model for pigment mixing.
- Fluid Dynamics in Computer Graphics.

## Implementation Notes
Use WebGL or CUDA for stroke simulations.
