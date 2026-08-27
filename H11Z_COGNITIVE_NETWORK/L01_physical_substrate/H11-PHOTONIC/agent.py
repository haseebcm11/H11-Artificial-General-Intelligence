import math
from dataclasses import dataclass

AGENT_ID = "H11-PHOTONIC"

@dataclass
class PhotonicInput:
    waveguide_length_cm: float
    propagation_loss_db_cm: float
    num_modulators: int
    modulator_insertion_loss_db: float
    num_couplers: int
    coupler_loss_db: float
    laser_power_mw: float
    detector_sensitivity_dbm: float

@dataclass
class PhotonicOutput:
    total_link_loss_db: float
    received_power_dbm: float
    link_margin_db: float
    is_link_viable: bool

class PhotonicException(Exception):
    pass

class PhotonicAgent:
    """
    Computes optical waveguide insertion loss and power budget for silicon photonics links.
    Converts laser power to dBm, calculates losses, checks against receiver sensitivity.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: PhotonicInput) -> PhotonicOutput:
        if input_data.laser_power_mw <= 0:
            raise PhotonicException("Laser power must be strictly positive.")
            
        # Convert laser power from mW to dBm
        # P(dBm) = 10 * log10(P(mW))
        tx_power_dbm = 10.0 * math.log10(input_data.laser_power_mw)
        
        # Calculate individual losses
        propagation_loss = input_data.waveguide_length_cm * input_data.propagation_loss_db_cm
        modulator_loss = input_data.num_modulators * input_data.modulator_insertion_loss_db
        coupler_loss = input_data.num_couplers * input_data.coupler_loss_db
        
        total_loss_db = propagation_loss + modulator_loss + coupler_loss
        
        received_power_dbm = tx_power_dbm - total_loss_db
        
        # Link margin is how far we are above the detector sensitivity
        link_margin_db = received_power_dbm - input_data.detector_sensitivity_dbm
        is_viable = link_margin_db >= 0.0
        
        return PhotonicOutput(
            total_link_loss_db=total_loss_db,
            received_power_dbm=received_power_dbm,
            link_margin_db=link_margin_db,
            is_link_viable=is_viable
        )
