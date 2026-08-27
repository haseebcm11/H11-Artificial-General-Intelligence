# H11-ELECTRONICA Agent Specification

## Abstract
The H11-ELECTRONICA agent specializes in micro-electronics, PCB design, VLSI, and embedded hardware systems. It focuses on low-voltage, high-frequency, and highly integrated analog/digital circuits.

## Architecture
1. **Schematic Analyzer**: Parses netlists and semantic schematic representations.
2. **PCB Router Heuristics**: Evaluates track widths, impedance matching, and layer stack-ups.
3. **Signal Integrity Engine**: Analyzes crosstalk, reflections, and EMI/EMC compliance issues.

## State Management
Maintains circuit netlists, BOM (Bill of Materials) data, component libraries, and PCB layout geometric constraints.

## I/O Specifications
- Inputs: SPICE netlists, logical schematics, target constraints (size, power, cost).
- Outputs: PCB gerber heuristics, BOM optimization reports, thermal dissipation maps for ICs.
