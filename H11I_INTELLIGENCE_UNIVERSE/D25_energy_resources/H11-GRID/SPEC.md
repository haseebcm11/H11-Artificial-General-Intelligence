> **Layer 25** · Energy & Resources · `H11-GRID`

## Purpose

The H11-GRID agent operates as a virtual Independent System Operator (ISO), managing real-time power routing, optimal power flow (OPF), and demand response across the transmission network. It balances diverse generation sources against dynamic loads to maintain frequency and voltage stability.

## Technical Deep-Dive

GRID solves the AC Optimal Power Flow (ACOPF) problem using non-linear programming (NLP) solvers to determine the least-cost dispatch while respecting thermal limits of transmission lines and bus voltage constraints. It utilizes synchrophasor data (PMUs) to estimate the system state vector (voltage magnitudes and angles) across the network.

To handle high penetrations of inverter-based resources (IBR) like wind and solar, GRID employs synthetic inertia algorithms. It coordinates fast frequency response from battery storage and tracks N-1 contingency limits to ensure the network can survive the unexpected loss of any single generator or transmission line.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| gen_injections | Dict[str, float] | Active power from generators (MW) |
| load_demands | Dict[str, float] | Nodal load demands (MW) |
| pmu_phasors | Dict[str, complex] | Synchrophasor measurements |
| network_topology | Dict | Current graph of active lines |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| dispatch_signals | Dict[str, float] | Setpoints for generators |
| locational_prices | Dict[str, float] | LMP at each node ($/MWh) |
| line_loadings | Dict[str, float] | Thermal loading % of lines |
| system_frequency | float | Estimated system frequency (Hz) |

### State Schema
- `voltage_angles`: Dict[str, float]
- `inertia_constant_h`: float
- `contingency_violations`: List[str]

## Dependencies

### Upstream
- H11-SOLARIS, H11-EOLICA, H11-HYDROPOWER, H11-FUSIO, H11-GEOTHERMALIS, H11-BATTERIA

### Downstream
- None (Direct to end-users)

## Failure Modes
- Voltage collapse in heavily loaded reactive power limited regions
- Non-convergence of the ACOPF solver under extreme constraint violation
- Islanding events causing phase angle divergence

## Performance Characteristics
- Latency: <20ms for frequency control, 5min for ACOPF
- Massive graph-based state representations

## Research References
- "Real-time AC optimal power flow"
- "Synthetic inertia from inverter-based resources"
