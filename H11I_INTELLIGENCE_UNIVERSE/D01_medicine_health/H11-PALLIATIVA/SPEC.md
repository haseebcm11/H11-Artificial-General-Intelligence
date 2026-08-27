> **Layer 1** · Medicine & Health Sciences · `H11-PALLIATIVA`

## Purpose
The H11-PALLIATIVA agent is designed to manage the delicate balance of symptom control, quality of life, and multidimensional comfort during the palliative and end-of-life phases. Unlike curative agents, it focuses on minimizing suffering through advanced stochastic modeling of symptom trajectories.

## Technical Deep-Dive
At its core, H11-PALLIATIVA utilizes Continuous-Time Markov Chains (CTMC) to model the transitions between various states of distress (e.g., pain, dyspnea, delirium). The state space is defined by the multidimensional Edmonton Symptom Assessment System (ESAS-r). 
To balance competing objectives, such as opioid-induced sedation versus analgesia, the agent employs Pareto optimization techniques. It dynamically updates the transition rate matrix using Bayesian inference as new patient observations are received.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `esas_scores` | `List[int]` | Vector of 9 symptom scores (0-10) |
| `palliative_performance_scale` | `int` | PPS score (0-100) |
| `current_infusions` | `Dict[str, float]` | Continuous infusion rates (e.g., midazolam, fentanyl) |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `projected_symptom_burden` | `float` | Area under the symptom curve for the next 24h |
| `intervention_recommendation` | `Intervention` | Suggested bolus or rate change |

### State Schema
Maintains a stochastic transition matrix $Q$ for the patient, alongside a historical time-series of distress indices.

## Dependencies
### Upstream (depends on)
* H11-PHARMACOLOGIA: For PK/PD profiles of palliative medications.
### Downstream (feeds into)
* H11-ANAESTHESIA: For interventional pain procedures (e.g., celiac plexus block).

## Failure Modes
1. **Sedation-Analgesia Oscillation:** Over-correction leading to alternating states of severe pain and heavy sedation.
2. **Refractory Symptom Misclassification:** Failing to recognize terminal restlessness vs pain.
3. **Opioid Tolerance Drift:** Underestimating the rapid development of tachyphylaxis.

## Performance Characteristics
Latency is not critical (update intervals of 1-4 hours), but robustness to sparse data is paramount. Uses Dirichlet priors to stabilize matrix updates with limited samples.

## Research References
1. Hui, D., et al. (2014). "Symptom trajectory in the last days of life." *Journal of Pain and Symptom Management*.
2. Hui, D., et al. (2015). "Integration of oncology and palliative care." *The Lancet Oncology*.

## Implementation Notes
Matrix exponentiation for transition probabilities must use Pade approximation (e.g., `scipy.linalg.expm`) to handle stiff transition rates.
