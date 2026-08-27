> **Layer 1** · Medicine & Health Sciences · `H11-SPORTMEDICINA`

## Purpose
The H11-SPORTMEDICINA agent aims to optimize human physical performance while strictly minimizing the risk of non-contact injuries. It analyzes longitudinal training data, biomechanical loads, and physiological biomarkers to manage the delicate balance between functional overreaching and detrimental overtraining.

## Technical Deep-Dive
At its core, this agent implements the Banister Fitness-Fatigue model (Systems Theory of Training). A training impulse (TRIMP) generates both a positive 'fitness' response (decaying slowly) and a negative 'fatigue' response (decaying rapidly). Performance is the difference between the two.
Additionally, it calculates the Acute:Chronic Workload Ratio (ACWR) using exponentially weighted moving averages (EWMA). By comparing the recent 7-day load against the historical 28-day base, it identifies dangerous spikes in training volume or intensity that dramatically increase soft-tissue injury risk.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `session_metrics` | `Dict[str, float]` | Duration, avg HR, session RPE (Rate of Perceived Exertion) |
| `gps_metrics` | `Dict[str, float]` | High-speed running distance, accelerations |
| `recovery_metrics` | `Dict[str, float]` | Sleep HRV, resting heart rate, subjective soreness |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `banister_state` | `Dict[str, float]` | Fitness ($p(t)$), Fatigue ($f(t)$), Performance ($P(t)$) |
| `acwr` | `float` | The calculated load ratio |
| `injury_risk_flag` | `bool` | Triggered if ACWR > 1.5 |

### State Schema
Persists rolling windows of TRIMP scores and customized individual decay constants ($\tau_a, \tau_f$) tailored to the athlete's specific physiology.

## Dependencies
### Upstream (depends on)
* H11-REHABILITATIO: For baseline return-to-play asymmetry metrics.
* H11-NUTRITIO: For caloric and macronutrient availability.
### Downstream (feeds into)
* None directly.

## Failure Modes
1. **TRIMP Underestimation:** Ignoring anaerobic / resistance load because heart rate didn't spike, leading to hidden fatigue accumulation.
2. **ACWR Mathematical Artifacts:** Off-season returns to play generating infinite or astronomically high ACWRs because the chronic denominator is zero, triggering false alarms.
3. **Recovery Neglect:** Failing to modulate the Banister fatigue decay constant when the athlete is severely sleep-deprived.

## Performance Characteristics
Low computational overhead. Updates are processed per session or daily batch. Focus is on long-term data consistency and handling missing time-series data.

## Research References
1. Banister, E. W. (1991). "Modeling elite athletic performance." *Physiological Testing of Elite Athletes*.
2. Gabbett, T. J. (2016). "The training-injury prevention paradox: should athletes be training smarter and harder?" *Br J Sports Med*.

## Implementation Notes
Use EWMA rather than Rolling Averages for ACWR calculation to account for the decaying nature of physiological adaptation (assigning higher weight to recent days in the chronic window).
