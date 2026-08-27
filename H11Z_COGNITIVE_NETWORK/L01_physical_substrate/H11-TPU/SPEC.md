# H11-TPU: Systolic Matrix Multiply

## Abstract
The H11-TPU layer models the architecture and operational semantics of Tensor Processing Units (TPUs), specialized ASIC accelerators developed for massive-scale deep learning. Unlike the general-purpose SIMT execution model of GPUs, this layer focuses on the deterministic, instruction-driven systolic array architecture. It models the flow of data through two-dimensional matrices of processing elements (PEs), specifically optimized for bfloat16 and int8 matrix multiplication workloads.

## Systolic Array and Data Flow
The core simulation handles the synchronous data pipelining inherent to systolic arrays. It calculates the setup time, weight loading latency, and activation wave propagation across the array (e.g., 128x128 or 256x256 dimensions). The layer computes strict algorithmic throughput bounds, demonstrating the efficiency of specialized matrix multiply units (MXUs) over traditional vector ALUs. High Bandwidth Memory (HBM) integration and SRAM buffer allocation are modeled to ensure continuous data feeding, preventing array starvation.

## Pod Topology and XLA Compilation
Beyond a single chip, the H11-TPU layer captures the macro-architecture of TPU pods (v4/v5 topologies). It models the Inter-Core Interconnect (ICI) optical links, simulating 3D torus network latency and bandwidth for synchronous all-reduce operations. Additionally, the layer incorporates abstractions for the XLA (Accelerated Linear Algebra) compiler, demonstrating how high-level computational graphs are lowered into optimized HLO (High Level Optimizer) instructions, fused, and scheduled directly onto the systolic arrays.
