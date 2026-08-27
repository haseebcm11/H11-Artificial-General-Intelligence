# H11-MOTIVATION: Drive & Motivation System

## Overview
The H11-MOTIVATION subsystem provides the foundational drive architecture for an AGI. It establishes the "why" behind the agent's behavior by balancing internal physiological/cognitive needs with external goal attainment. This system grounds the agent's goal-setting in a robust, homeostatic framework that naturally interleaves exploration (curiosity), exploitation (extrinsic rewards), and maintenance (energy).

## Architecture

### 1. Homeostatic Drives
Drives are modeled as dynamic variables with an optimal "setpoint." Any deviation from this setpoint produces a "drive deficit." The urgency of this deficit scales exponentially, ensuring that extreme deviations (e.g., critical energy depletion) pre-empt all other activities.

### 2. Intrinsic vs Extrinsic Motivation
- **Intrinsic Motivation**: Originates from the internal drive reduction gradients (e.g., fulfilling the need for epistemic certainty/curiosity).
- **Extrinsic Motivation**: Stems from external rewards provided by the environment (e.g., task completion points, user approval).
The utility function linearly blends intrinsic drive reduction and expected extrinsic rewards using customizable alpha and beta weights.

### 3. Utility Function and Preference Ordering
Action selection is cast as an optimization problem. Candidate actions are evaluated based on their expected effects on the drive states.
`U(a) = α * (Drive_Reduction(a) + Curiosity_Bonus(a)) + β * Extrinsic_Reward(a) - Conflict_Penalty(a)`
Actions are sorted by `U(a)` descending to form a strict preference ordering.

### 4. Motivational Conflict Resolution
When an action reduces one drive but severely exacerbates another (e.g., sprinting solves the achievement drive but crushes the energy drive), a non-linear conflict penalty is assessed. This prevents the system from self-destructive over-optimization of a single objective at the expense of systemic homeostasis.

## Mathematical Foundation
- **Drive Deficit**: `Cost(x) = W * (exp(λ * |x - Setpoint|) - 1)`
- **Conflict Penalty**: Triggered when `Deficit_post > Deficit_pre + Threshold`. Applied as a superlinear function `(ΔDeficit)^1.5` to aggressively penalize destructive trade-offs.
