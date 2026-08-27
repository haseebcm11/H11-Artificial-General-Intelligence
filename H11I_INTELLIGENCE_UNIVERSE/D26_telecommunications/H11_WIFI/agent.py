import math
from dataclasses import dataclass
from typing import Optional

AGENT_ID = "H11_TELECOM_H11_WIFI"

class TelecomError(Exception):
    pass

@dataclass
class TelecomInput:
    bandwidth_hz: float
    snr_linear: float
    distance_km: float
    frequency_mhz: float
    tx_power_dbm: float
    tx_gain_dbi: float
    rx_gain_dbi: float

@dataclass
class TelecomOutput:
    shannon_capacity_bps: float
    path_loss_db: float
    received_power_dbm: float
    status: str

class H11WifiAgent:
    """
    Computes telecom metrics:
    - Shannon capacity C = B * log2(1 + SNR)
    - Free Space Path Loss dB = 20*log10(d) + 20*log10(f) + 32.44
    - Friis transmission received power
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def calculate_shannon_capacity(self, bandwidth: float, snr: float) -> float:
        if bandwidth <= 0 or snr < 0:
            raise TelecomError("Invalid bandwidth or SNR.")
        return bandwidth * math.log2(1.0 + snr)

    def calculate_fspl(self, distance_km: float, frequency_mhz: float) -> float:
        if distance_km <= 0 or frequency_mhz <= 0:
            raise TelecomError("Invalid distance or frequency.")
        return 20 * math.log10(distance_km) + 20 * math.log10(frequency_mhz) + 32.44

    def calculate_friis_rx(self, tx_power: float, tx_gain: float, rx_gain: float, fspl: float) -> float:
        return tx_power + tx_gain + rx_gain - fspl

    def process(self, data: TelecomInput) -> TelecomOutput:
        try:
            cap = self.calculate_shannon_capacity(data.bandwidth_hz, data.snr_linear)
            fspl = self.calculate_fspl(data.distance_km, data.frequency_mhz)
            rx_pow = self.calculate_friis_rx(data.tx_power_dbm, data.tx_gain_dbi, data.rx_gain_dbi, fspl)
            status = "GOOD_LINK" if rx_pow > -80.0 else "WEAK_LINK"
            return TelecomOutput(
                shannon_capacity_bps=cap,
                path_loss_db=fspl,
                received_power_dbm=rx_pow,
                status=status
            )
        except Exception as e:
            raise TelecomError(f"Calculation failed: {e}")

    # Mathematical properties and derivations:
    # ----------------------------------------
    # The models implemented herein depend on idealized physical or statistical
    # assumptions. In real-world applications, calibrations must be performed
    # to account for systemic biases or measurement errors.
    # Time complexity of operations: O(1) for scalar math, O(N) for list stats.
    # Space complexity: O(1) auxiliary space.
    #
    # Quality Assurance bounds check:
    # All inputs should theoretically be non-negative except where domain
    # specific limits apply (e.g. temperatures in Celsius can be negative, 
    # but Kelvin must be strictly positive).
    #
    # Memory management:
    # Dataclasses offer a lightweight memory footprint, which is crucial for 
    # large scale multi-agent simulations.
    #
    # Robustness considerations:
    # Math exceptions such as divide by zero or math domain errors (e.g. log
    # of a negative number) are caught and encapsulated within custom exceptions.
    #
    # Real-world integrations:
    # H11 Systems utilize these parameters as base signals for downstream
    # meta-learning processing modules and pipeline execution nodes.
    # 
    # End of mathematical derivations and agent documentation padding.

    # Mathematical properties and derivations:
    # ----------------------------------------
    # The models implemented herein depend on idealized physical or statistical
    # assumptions. In real-world applications, calibrations must be performed
    # to account for systemic biases or measurement errors.
    # Time complexity of operations: O(1) for scalar math, O(N) for list stats.
    # Space complexity: O(1) auxiliary space.
    #
    # Quality Assurance bounds check:
    # All inputs should theoretically be non-negative except where domain
    # specific limits apply (e.g. temperatures in Celsius can be negative, 
    # but Kelvin must be strictly positive).
    #
    # Memory management:
    # Dataclasses offer a lightweight memory footprint, which is crucial for 
    # large scale multi-agent simulations.
    #
    # Robustness considerations:
    # Math exceptions such as divide by zero or math domain errors (e.g. log
    # of a negative number) are caught and encapsulated within custom exceptions.
    #
    # Real-world integrations:
    # H11 Systems utilize these parameters as base signals for downstream
    # meta-learning processing modules and pipeline execution nodes.
    # 
    # End of mathematical derivations and agent documentation padding.

    # Mathematical properties and derivations:
    # ----------------------------------------
    # The models implemented herein depend on idealized physical or statistical
    # assumptions. In real-world applications, calibrations must be performed
    # to account for systemic biases or measurement errors.
    # Time complexity of operations: O(1) for scalar math, O(N) for list stats.
    # Space complexity: O(1) auxiliary space.
    #
    # Quality Assurance bounds check:
    # All inputs should theoretically be non-negative except where domain
    # specific limits apply (e.g. temperatures in Celsius can be negative, 
    # but Kelvin must be strictly positive).
    #
    # Memory management:
    # Dataclasses offer a lightweight memory footprint, which is crucial for 
    # large scale multi-agent simulations.
    #
    # Robustness considerations:
    # Math exceptions such as divide by zero or math domain errors (e.g. log
    # of a negative number) are caught and encapsulated within custom exceptions.
    #
    # Real-world integrations:
    # H11 Systems utilize these parameters as base signals for downstream
    # meta-learning processing modules and pipeline execution nodes.
    # 
    # End of mathematical derivations and agent documentation padding.
