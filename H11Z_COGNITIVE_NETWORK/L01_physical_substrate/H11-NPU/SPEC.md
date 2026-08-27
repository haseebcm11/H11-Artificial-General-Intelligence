# H11-NPU Specification

## Overview
The H11-NPU (Neural Processing Unit) sub-agent models a dedicated neural accelerator architecture, optimizing for matrix multiplications, convolutions, and non-linear activations common in deep learning workloads. The core computational paradigm revolves around large 2D arrays of MAC (Multiply-Accumulate) units, tightly coupled with on-chip SRAM to minimize data movement energy.

## Architecture
At a hardware level, the NPU assumes a dataflow architecture, potentially utilizing systolic array techniques to propagate weights and activations efficiently. It heavily emphasizes reduced precision arithmetic—such as INT8, INT4, or specialized floating-point formats like BF16 and FP8—to maximize throughput and energy efficiency. The memory hierarchy avoids deep caches in favor of explicitly managed scratchpads, reflecting the predictable memory access patterns of tensor operations.

## Execution Model
The agent schedules tensor operations by mapping them onto the spatial array. The scheduler must solve a complex bin-packing and tiling problem to ensure that the SRAM is utilized maximally without thrashing. Power gating and clock gating are dynamically applied at the granularity of individual MAC blocks to stay within strict thermal and power budgets typical of mobile and edge deployment environments.
