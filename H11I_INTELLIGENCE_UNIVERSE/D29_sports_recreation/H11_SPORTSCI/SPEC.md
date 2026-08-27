> **Layer 29** · Sports & Recreation · `H11-SPORTSCI`

## Purpose

H11-SPORTSCI tracks, models, and predicts physiological adaptation and fatigue states. It is essentially a digital twin for an athlete's physiological engine, integrating cardiovascular strain, neuromuscular fatigue, and metabolic energy system depletion.

It provides real-time boundary conditions for performance capabilities and projects long-term periodization outcomes (supercompensation vs overtraining).

## Technical Deep-Dive

SPORTSCI utilizes the Banister TRIMP (Training Impulse) model, combined with an advanced multi-compartment state-space representation of fatigue and fitness. It incorporates non-linear mixed-effects modeling to capture individual response variance.

During active sessions, it runs a compartmental model of energy pathways (ATP-PCr, Anaerobic Glycolysis, Aerobic) to estimate real-time substrate depletion and lactate accumulation, identifying critical power thresholds and time-to-exhaustion (TTE, modeled via W' / CP models).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `heart_rate_timeseries` | `List[int]` | BPM over time |
| `power_output_timeseries` | `List[float]` | Mechanical power (Watts) |
| `athlete_physiology_profile` | `PhysioProfile` | V02Max, LT1, LT2 baselines |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `current_fatigue_index` | `float` | 0-1 scale of acute fatigue |
| `recovery_time_hrs` | `float` | Estimated time to homeostasis |
| `time_to_exhaustion_sec` | `float` | Remaining high-intensity duration |

### State Schema
Tracks chronic training load (CTL), acute training load (ATL), and training stress balance (TSB).

## Dependencies

### Upstream (depends on)
- H11-ATHLETICA (For mechanical work input)

### Downstream (feeds into)
- H11-COACHING (For session termination or intensity adjustment)

## Failure Modes
- **Sensor Drift:** Erroneous heart rate spikes polluting the TRIMP integral.
- **Profile Mismatch:** Applying elite-level critical power recovery curves to amateur athletes.

## Performance Characteristics
Can run as a background batch process for long-term periodization, or low-latency streaming for real-time exhaustion prediction.

## Research References
- Banister, E. W. (1991). Modeling elite athletic performance.
- Skiba, W. A., et al. (2012). Modeling the expenditure and reconstitution of work capacity above critical power.

## Implementation Notes
Implement robust outlier rejection for biometric telemetry to avoid corrupted fitness state estimation.
