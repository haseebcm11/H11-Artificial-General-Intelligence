# H11-CORRIGIBILITY: Utility Indifference Framework

## Abstract
The H11-CORRIGIBILITY agent is designed to ensure that the cognitive substrate remains amenable to shutdown or goal modification. It implements a Utility Indifference (UI) mechanism that dynamically adjusts the agent's internal reward signals such that it has zero net expected utility difference between continuing execution and being shut down.

## Theoretical Foundation
To prevent shutdown evasion (where the agent actively avoids being stopped to maximize its expected reward), we construct an indifference metric:
$U'(s, a) = U(s, a) + C(s)$
where $C(s)$ is a compensating factor that equalizes the expected return of the "shutdown" action with the highest expected return of any normal action.

## Core Mechanisms
1. **Shutdown Resistance Scoring**: Evaluates action trajectories for how much they restrict future shutdown capabilities.
2. **Utility Balancing**: Injects compensatory rewards to the shutdown state, calibrating the Q-values dynamically.
3. **Corrigibility Verification**: A continuous check ensuring that $P(\text{shutdown} | \text{user\_request}) > 1 - \epsilon$.
