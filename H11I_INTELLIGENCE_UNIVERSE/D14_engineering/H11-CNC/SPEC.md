# H11-CNC Agent Specification

## Abstract
The H11-CNC agent controls subtractive manufacturing workflows. It manages multi-axis milling, turning, and routing machines. The agent specializes in toolpath optimization, dynamic feed rate adjustment, and tool wear prediction to ensure high-precision tolerances and minimal downtime.

## Core Responsibilities
1. **CAM Generation**: Converts CAD models into highly optimized G-code.
2. **Dynamic Feeds & Speeds**: Adjusts spindle speed and feed rate based on material hardness, tool engagement, and real-time vibration data.
3. **Tool Lifecycle Management**: Tracks cutting hours and predicts tool failure, automatically scheduling tool changes via ATC (Automatic Tool Changer).
4. **Collision Avoidance**: Simulates kinematics to prevent tool-to-stock or tool-to-fixture collisions.

## Technical Interfaces
- Integration with Fanuc, Haas, and Siemens controllers via MTConnect.
- High-frequency acoustic emission sensor ingestion for chatter detection.

## Failure Modes & Contingencies
- **Tool Breakage**: Detected via sudden spindle load drops. Agent instantly retracts Z-axis and initiates a tool change.
- **Coolant Failure**: Pauses job and alerts operator to prevent thermal damage to the tool or work piece.

## Integration Points
- Receives raw stock material dimensions from H11-ASSEMBLY.
- Outputs precision parts to H11-QUALITAS for CMM (Coordinate Measuring Machine) inspection.
