import math
from dataclasses import dataclass
from typing import List

AGENT_ID = "H11-CULTURAL"

@dataclass
class SocialMetricsInput:
    incomes: List[float]
    observed_freqs: List[float]
    expected_freqs: List[float]
    baseline_measure: float
    population_mean: float
    correlation: float
    utility_x: float
    utility_alpha: float

@dataclass
class SocialMetricsOutput:
    gini_coefficient: float
    chi_squared_stat: float
    regression_to_mean_estimate: float
    utility_value: float

class DomainException(Exception):
    pass

class H11CulturalAgent:
    """
    Humanities & Social Sciences quantitative agent.
    Computes Gini coefficient, Chi-squared independence, Regression to the mean,
    and Utility function U(x) = x^a.
    """
    def __init__(self):
        self.agent_id = AGENT_ID

    def process(self, input_data: SocialMetricsInput) -> SocialMetricsOutput:
        # 1. Gini coefficient
        incomes = sorted(input_data.incomes)
        n = len(incomes)
        if n == 0 or sum(incomes) == 0:
            gini = 0.0
        else:
            coef = 2.0 / n
            const = (n + 1.0) / n
            weighted_sum = sum((i + 1) * yi for i, yi in enumerate(incomes))
            gini = coef * (weighted_sum / sum(incomes)) - const
            
        # 2. Chi-squared independence
        if len(input_data.observed_freqs) != len(input_data.expected_freqs):
            raise DomainException("Observed and expected frequencies must match in length")
            
        chi2 = 0.0
        for obs, exp in zip(input_data.observed_freqs, input_data.expected_freqs):
            if exp <= 0:
                continue
            chi2 += ((obs - exp) ** 2) / exp
            
        # 3. Regression to the mean
        # E[Y|X] = mean_Y + r * (X - mean_X) * (std_Y/std_X). Assuming standardized vars.
        rtm_est = input_data.population_mean + input_data.correlation * (input_data.baseline_measure - input_data.population_mean)
        
        # 4. Utility function U(x) = x^a
        if input_data.utility_x < 0:
            raise DomainException("Utility x must be non-negative")
        utility = math.pow(input_data.utility_x, input_data.utility_alpha)
        
        return SocialMetricsOutput(
            gini_coefficient=gini,
            chi_squared_stat=chi2,
            regression_to_mean_estimate=rtm_est,
            utility_value=utility
        )
