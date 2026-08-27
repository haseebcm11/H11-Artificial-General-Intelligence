# H11-CONVOLUTION Specification

## Overview
H11-CONVOLUTION is responsible for engineering the spatial and temporal convolution primitives in the cognitive substrate. It deals with n-dimensional convolutions (1D, 2D, 3D), depthwise separable configurations, dilated and strided convolutions, and modern variations like ConvNeXt blocks.

## Core Capabilities
- **Multi-Dimensional Conv**: Support for temporal (1D), spatial (2D), and volumetric (3D) processing.
- **Modern Paradigms**: Implementing depthwise separable layers, grouped convolutions, and inverted bottlenecks.
- **Large Kernel Convolutions**: Managing padding, scaling, and initialization for large receptive fields (e.g., 7x7 or 31x31).
- **Dilated Convolutions**: Generating atrous spatial pyramid pooling (ASPP) structures for multi-scale context.

## Inputs
- Tensor topologies (N, C, H, W, D).
- Kernel sizes, strides, padding logic, dilations.
- Grouping configurations.

## Outputs
- Computation graph for convolution sequences.
- Fusion instructions (Conv-BN-Act fusion).
- Padding and receptive field analyses.

## Evaluation
- Receptive field correctness.
- FLOPs vs. representation power.
- Hardware utilization limits.
