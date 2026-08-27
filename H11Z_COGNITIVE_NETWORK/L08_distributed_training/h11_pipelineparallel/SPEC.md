# <H11-PIPELINEPARALLEL — Pipeline Scheduler>
> **Layer 8** · Distributed Training Infrastructure · `H11-PIPELINEPARALLEL`

## Purpose
Distributes sequential model layers across multiple nodes to form a processing pipeline, enabling models larger than a single node to be trained efficiently.

## Technical Deep-Dive
Implements the 1F1B (One Forward, One Backward) scheduling algorithm to minimize pipeline bubbles.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `num_microbatches` | `int` | Number of microbatches per step |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `schedule` | `List[str]` | The execution schedule for the pipeline stage |
