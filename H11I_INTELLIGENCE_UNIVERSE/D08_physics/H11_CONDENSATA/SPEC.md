> **Layer 8** · Physics · `H11-CONDENSATA`

## Purpose

The H11-CONDENSATA agent simulates interacting quantum many-body systems on discrete lattices, solving for emergent phenomena such as superconductivity, Mott insulators, and topological phases.

## Technical Deep-Dive

It evaluates Hubbard and Heisenberg models using exact diagonalization for small clusters and Density Matrix Renormalization Group (DMRG) for 1D systems. It solves the BCS gap equation iteratively to find superconducting critical temperatures and order parameters.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| temperature | float | Thermodynamic T |
| lattice | LatticeType | Bravais lattice |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| phase | PhaseState | Resulting ground state phase |

### State Schema
Tracks `susceptibility` and `current_temperature`.

## Dependencies
### Upstream (depends on)
- H11-THERMODYNAMICA
- H11-CRYOGENICA

### Downstream (feeds into)
- H11-QUANTUMINFO

## Failure Modes
- DMRG truncation error divergence
- Fermionic sign problem in QMC

## Performance Characteristics
Memory-bound due to exponentially growing Hilbert spaces.

## Research References
- Bardeen, Cooper, Schrieffer (1957). Theory of Superconductivity.
- White, S. R. (1992). Density matrix formulation for quantum renormalization groups.

## Implementation Notes
Use sparse matrix libraries (e.g., SciPy, PETSc) for large eigenvalue problems.
