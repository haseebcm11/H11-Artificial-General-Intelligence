# H11-GNN: Graph Neural Network

## Overview
The H11-GNN agent constructs Graph Neural Networks for non-Euclidean data modalities. It enables message passing over dynamic or static topologies, and provides mechanisms for attention, convolutions, and equivariance.

## Capabilities
- **Message Passing Neural Networks (MPNN)**: Core framework for node, edge, and global state updates.
- **GCN & GAT Layers**: Graph Convolutional Networks and Graph Attention Networks for feature aggregation.
- **Equivariant GNNs**: E(n) equivariant networks for physics and spatial reasoning.
- **Over-smoothing Mitigation**: Implementing jumping knowledge, residual connections, and PairNorm to allow deeper GNNs.
