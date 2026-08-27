# H11-ASSEMBLY Agent Specification

## Abstract
The H11-ASSEMBLY agent orchestrates robotic manipulation and human-in-the-loop assembly workflows. It sequences discrete assembly steps, coordinates robotic arms (e.g., UR, KUKA) for pick-and-place, welding, or fastening, and tracks bill of materials (BOM) consumption.

## Core Responsibilities
1. **Workflow Sequencing**: Compiles CAD assembly models into sequential robotic instructions.
2. **Kinematic Coordination**: Prevents collisions in multi-robot cells using real-time spatial awareness.
3. **Torque & Fastening Control**: Monitors smart tools to ensure precise torque specifications are met on all fasteners.
4. **Inventory & BOM Management**: Tracks parts consumed during assembly and requests resupply automatically.

## Technical Interfaces
- ROS2/MoveIt for robotic arm path planning and execution.
- Open Protocol for communicating with smart screwdrivers and torque wrenches.

## Failure Modes & Contingencies
- **Dropped Part**: Visual servos detect missing parts in grippers; agent automatically commands a retry or retrieves a new part.
- **Torque Failure**: If a fastener strips or fails to reach torque, the sub-assembly is routed to a rework station.

## Integration Points
- Consumes parts produced by H11-3DPRINT and H11-CNC.
- Passes finished assemblies to H11-QUALITAS for final functional testing.
