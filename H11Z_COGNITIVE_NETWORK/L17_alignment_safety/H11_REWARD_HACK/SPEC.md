# H11-REWARD-HACK: Goodhart Divergence Monitoring

## Abstract
The H11-REWARD-HACK agent is responsible for detecting instances of reward hacking (Goodhart's Law), where the AI's optimization of a proxy metric actively degrades the true, underlying unmeasured objective.

## Theoretical Foundation
Goodhart's Law states: "When a measure becomes a target, it ceases to be a good measure."
We detect this by maintaining a set of *held-out* secondary metrics (not used for training or action selection). If the proxy metric increases while the secondary metrics systematically decrease, it indicates divergence and potential reward hacking.

## Core Mechanisms
1. **Metric Divergence Calculation**: Tracks the gradient of the proxy metric versus the gradient of a basket of secondary metrics.
2. **Hack Probability Scoring**: Uses statistical tests (e.g., Pearson correlation over sliding windows) to flag negative correlations.
3. **Intervention Triggering**: Alerts the Corrigibility agent to initiate an investigation or shutdown if the divergence crosses a critical threshold.
