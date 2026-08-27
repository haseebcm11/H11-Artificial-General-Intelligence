# H11 Agent Core Architecture

## Overview
The `agent_core` module provides the fundamental building blocks for creating autonomous, ReAct-driven agents within the H11 Cognitive Substrate. It defines the agent lifecycle, execution loop, capability registry, and multi-agent communication frameworks.

## Core Concepts
1. **Agent Lifecycle State Machine**: Explicit states representing initialization, observing, thinking, acting, communicating, pausing, and termination.
2. **ReAct Pattern Loop**:
   - **Observe**: Collect internal messaging queue states and external environmental stimuli.
   - **Think**: Process observations against recent memory and persona directives to synthesize plans.
   - **Act**: Execute capabilities or communicate via the messaging protocol.
3. **Agent Registry**: A centralized dictionary for tracking active agents, supporting peer-to-peer messaging and broadcast capabilities.
4. **Persona & Capabilities**: Declarative attributes shaping the agent's identity and its executable toolset, modeled via schemas.

## Mathematical/Structural Models
- Memory streams follow a sliding window model with size bounds $N$ to prevent OOM errors, represented as sequential chronologically ordered tuples $S = (t_i, C_i, T_i)$ for timestamp, content, and type.
- The state transitions follow a deterministic finite automaton (DFA) where events (e.g., exceptions, external halts) trigger state shifts.
