"""
Agent Module: L04_AGENT_NEURON
Agent Class: AgentNeuron

Leaky Integrate-and-Fire (LIF) biological neuron dynamics with membrane potential ODE integration, spike generation thresholding, and refractory period resetting.
"""

from dataclasses import dataclass, field
import math
import sys

AGENT_ID = "L04_AGENT_NEURON"


class AgentNeuronError(ValueError):
    """Raised when AgentNeuron domain parameters or inputs violate operational bounds."""
    pass


@dataclass(frozen=True)
class AgentNeuronInput:
    data: list[float] = field(default_factory=lambda: [1.2, 0.8, 1.5, 0.5, 2.0, 0.2])
    parameters: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentNeuronOutput:
    status: str = 'OK'
    score: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    membrane_trace: list[float] = field(default_factory=list)
    spikes: list[int] = field(default_factory=list)


class AgentNeuron:
    """
    Leaky Integrate-and-Fire (LIF) biological neuron dynamics with membrane potential ODE integration, spike generation thresholding, and refractory period resetting.
    """
    def __init__(self, agent_id: str = AGENT_ID):
        self.agent_id = agent_id

    def process(self, inputs: AgentNeuronInput) -> AgentNeuronOutput:
        """Execute domain-specific analytical mathematics and logic."""
        v_thresh = float(inputs.parameters.get("v_threshold", 1.0))
        v_reset = float(inputs.parameters.get("v_reset", 0.0))
        tau_m = float(inputs.parameters.get("tau_m", 10.0))
        dt = float(inputs.parameters.get("dt", 1.0))
        decay = math.exp(-dt / max(tau_m, 1e-6))

        currents = inputs.data if inputs.data else [1.0, 0.5, 1.2, 0.3]
        v_mem = v_reset
        spikes, v_trace = [], []
        refractory_steps = 0
        refractory_period = int(inputs.parameters.get("refractory_steps", 2))

        for I in currents:
            if refractory_steps > 0:
                v_mem = v_reset
                refractory_steps -= 1
                spikes.append(0)
            else:
                v_mem = v_mem * decay + I * (1.0 - decay)
                if v_mem >= v_thresh:
                    spikes.append(1)
                    v_mem = v_reset
                    refractory_steps = refractory_period
                else:
                    spikes.append(0)
            v_trace.append(round(v_mem, 4))

        spike_rate = sum(spikes) / max(len(spikes), 1)
        mean_v = sum(v_trace) / max(len(v_trace), 1)
        score = min(1.0, spike_rate * 2.0 + mean_v * 0.2)
        metrics = {"spike_count": float(sum(spikes)), "firing_rate": round(spike_rate, 4), "mean_membrane_potential": round(mean_v, 4), "decay_factor": round(decay, 4)}
        return AgentNeuronOutput(status="COMPLETED", score=round(score, 4), metrics=metrics, membrane_trace=v_trace, spikes=spikes)
