from dataclasses import dataclass

AGENT_ID = "H11_AUDIOLOGIA"

@dataclass
class HealthMetricsInput:
    weight_kg: float
    height_cm: float
    age_years: float
    is_male: bool
    max_heart_rate: float
    resting_heart_rate: float
    goniometry_max_angle: float
    goniometry_min_angle: float
    fev1_liters: float
    fvc_liters: float

@dataclass
class HealthMetricsOutput:
    bmr_kcal: float
    vo2_max: float
    range_of_motion_deg: float
    fev1_fvc_ratio: float

class DomainException(Exception):
    pass

class H11AudiologiaAgent:
    """
    Allied Health sciences computational agent.
    Implements BMR Harris-Benedict, VO2max estimation (Uth-Sorensen-Overgaard-Pedersen),
    Goniometry ROM, and Spirometry FEV1/FVC ratio.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: HealthMetricsInput) -> HealthMetricsOutput:
        if input_data.weight_kg <= 0 or input_data.height_cm <= 0 or input_data.age_years <= 0:
            raise DomainException("Anthropometrics must be positive")
            
        # 1. BMR Harris-Benedict (Original)
        if input_data.is_male:
            bmr = 66.5 + (13.75 * input_data.weight_kg) + (5.003 * input_data.height_cm) - (6.75 * input_data.age_years)
        else:
            bmr = 655.1 + (9.563 * input_data.weight_kg) + (1.850 * input_data.height_cm) - (4.676 * input_data.age_years)
            
        # 2. VO2max estimation: VO2max = 15.3 x (MHR / RHR)
        if input_data.resting_heart_rate <= 0:
            raise DomainException("RHR must be positive")
        vo2 = 15.3 * (input_data.max_heart_rate / input_data.resting_heart_rate)
        
        # 3. Goniometry ROM
        rom = abs(input_data.goniometry_max_angle - input_data.goniometry_min_angle)
        
        # 4. Spirometry FEV1/FVC
        if input_data.fvc_liters <= 0:
            raise DomainException("FVC must be positive")
        ratio = input_data.fev1_liters / input_data.fvc_liters
        
        return HealthMetricsOutput(
            bmr_kcal=bmr,
            vo2_max=vo2,
            range_of_motion_deg=rom,
            fev1_fvc_ratio=ratio
        )
