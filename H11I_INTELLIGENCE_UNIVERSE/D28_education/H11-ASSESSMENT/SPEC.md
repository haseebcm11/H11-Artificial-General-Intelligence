> **Layer 6** · Educational Systems · `H11-ASSESSMENT`

## Purpose
The Assessment Agent acts as the evaluator and diagnostic engine of the educational substrate. It generates, administers, and grades formative and summative assessments. Beyond mere grading, its primary purpose is latent trait estimation—accurately determining a learner's true capability level regarding specific Knowledge Components based on their observed responses.

H11-ASSESSMENT ensures that testing is not merely evaluative but actively diagnostic, identifying specific misconceptions and calibrating the difficulty of future questions dynamically.

## Technical Deep-Dive
H11-ASSESSMENT is built around Item Response Theory (IRT), specifically the 3-Parameter Logistic (3PL) model, which accounts for item difficulty, discrimination, and guessing probability. As a learner answers questions, the agent uses Bayesian inference to update the posterior distribution of their latent ability parameter ($\theta$).

For testing administration, it employs Computerized Adaptive Testing (CAT) algorithms. Instead of a fixed test, CAT selects the next item that provides maximum Fisher information at the learner's current estimated ability level, drastically reducing the number of questions needed to reach a confident assessment.

For constructed responses (e.g., essays, code), the agent integrates advanced NLP techniques, utilizing fine-tuned LLMs for automated rubric-based grading, extracting not just a score, but specific sub-component diagnostics.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `test_spec` | `AssessmentBlueprint` | KC targets and standard error requirements. |
| `learner_id` | `str` | Identifier for fetching prior IRT priors. |
| `responses` | `List[Response]` | User answers to administered items. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `ability_estimate` | `LatentTrait` | Updated proficiency scores per KC. |
| `next_item` | `TestItem` | The next optimally selected question. |
| `diagnostic_report` | `Diagnostic` | Identified misconceptions and gaps. |

### State Schema
Maintains the `ItemBank` (calibrated IRT parameters for all questions) and `ActiveAssessments` tracking the running Bayesian state for in-progress tests.

## Dependencies
### Upstream (depends on)
- `H11-CURRICULUM`: Defines the KCs that need assessment.
- `H11-LLM_CORE`: Provides inference for grading constructed responses.

### Downstream (feeds into)
- `H11-CURRICULUM`: Feeds back proficiency data to update the curriculum DAG.
- `H11-STUDENT_MODEL`: Updates the global learner profile.

## Failure Modes
1. **Item Exposure**: Overusing highly discriminative items, leading to compromised test security.
2. **Prior Collapse**: Over-relying on historical ability priors, preventing the system from recognizing sudden learning leaps.
3. **Misconception Misclassification**: Incorrectly diagnosing a systemic misunderstanding as a simple careless error due to poor item design.

## Performance Characteristics
- **CAT Selection**: Must compute maximum information and select the next item in < 100ms to maintain testing flow.
- **Grading Latency**: Constructed response grading via LLMs operates asynchronously, typically completing in 2-5 seconds.

## Research References
1. "Computerized Adaptive Testing: A Primer" (Wainer)
2. "Bayesian Networks in Educational Assessment"
3. "Automated Essay Scoring using Deep Learning"

## Implementation Notes
Implement the IRT math using vectorized NumPy operations for speed. The item bank should track exposure rates and employ a Sympson-Hetter control mechanism to prevent item overexposure.
