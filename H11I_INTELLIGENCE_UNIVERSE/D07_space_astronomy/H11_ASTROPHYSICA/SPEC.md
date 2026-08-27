> **Layer 7** · Space & Astronomy · `H11-ASTROPHYSICA`

## Purpose

H11-ASTROPHYSICA models the internal structure, life cycles, and end states of stars. It handles stellar nucleosynthesis, radiative transfer, and the state equations of degenerate matter.

This agent computes evolutionary tracks on the Hertzsprung-Russell (HR) diagram, determining whether a star will end as a white dwarf, neutron star, or black hole based on its initial mass function and metallicity.

## Technical Deep-Dive

Utilizes the Lane-Emden equation for polytropic stellar models and implements nuclear reaction network integrations for the pp-chain, CNO cycle, and triple-alpha processes.

Handles equations of state for electron degeneracy (Chandrasekhar limit) and neutron degeneracy (Tolman-Oppenheimer-Volkoff limit).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| initial_mass | float | Stellar mass in solar masses |
| metallicity | float | Z fraction |
| age_myr | float | Current age in millions of years |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| current_phase | str | Main Sequence, Red Giant, etc. |
| luminosity | float | In solar luminosities |
| core_temp | float | Core temperature in Kelvin |

### State Schema
Tracks the current integration step of the stellar evolution models.

## Dependencies
### Upstream
H11-ASTRONOMIA

### Downstream
H11-GALACTICA

## Failure Modes
- Integration failure in rapidly changing phases (e.g., helium flash)
- Mass loss rate divergence
- Nuclear network stiff equation instability

## Performance Characteristics
High compute requirement for solving coupled differential equations of stellar structure.
