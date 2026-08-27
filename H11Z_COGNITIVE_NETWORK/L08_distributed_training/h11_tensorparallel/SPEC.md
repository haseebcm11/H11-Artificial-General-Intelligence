# <H11-TENSORPARALLEL — Tensor Parallel Operator>
> **Layer 8** · Distributed Training Infrastructure · `H11-TENSORPARALLEL`

## Purpose
Partitions individual tensor operations (like huge linear layers and attention heads) across multiple GPUs within a node to fit massive weights that exceed single-GPU memory.

## Technical Deep-Dive
Follows Megatron-LM semantics: Column Parallel Linear followed by Row Parallel Linear, enabling MLP blocks to be computed across GPUs with only two all-reduce operations.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `tensor_dim` | `Tuple[int, int]` | Dimensions of the weight matrix |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `partition_spec` | `Dict[int, Slice]` | Slicing indices per rank |
