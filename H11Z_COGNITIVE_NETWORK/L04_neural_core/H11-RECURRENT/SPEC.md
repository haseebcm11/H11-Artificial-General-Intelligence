# H11-RECURRENT Specification

## Overview
H11-RECURRENT maintains and scales recurrent processing architectures (RNN, LSTM, GRU) within the H11 ecosystem. Even as transformers dominate, specialized recurrent structures are necessary for stateful streaming, unbounded context tracking, and hardware-efficient sequential parsing.

## Core Capabilities
- **Recurrent Units**: Native support for LSTM, GRU, minimal RNNs, and modernized recurrent variants (e.g., SRU, RWKV-like linear RNNs).
- **Backpropagation Through Time (BPTT)**: Managing truncated BPTT horizons, gradient clipping, and state detachments.
- **Attention Over States**: Hybrid models combining hidden state recurrence with selective attention over past states.
- **State Initialization**: Learnable state initialization and state passing across streaming batches.

## Inputs
- Sequence lengths, batch structures, streaming context requirements.
- Hidden dimensions, layer counts, bidirectionality.
- Truncation horizons for training.

## Outputs
- Recurrent execution graphs.
- Stateful buffer management profiles.
- Gradient routing protocols for BPTT.

## Evaluation
- Gradient explosion/vanishing checks.
- State persistence consistency.
- Latency per timestep (streaming mode).
