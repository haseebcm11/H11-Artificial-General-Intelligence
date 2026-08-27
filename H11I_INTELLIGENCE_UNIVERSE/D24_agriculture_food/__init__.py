"""
Domain 24: Agriculture & Food Sciences
"""

from .H11_CROP.agent import CropAgent
from .H11_HORTICULTURA.agent import HorticulturaAgent
from .H11_IRRIGATIO.agent import IrrigatioAgent
from .H11_LIVESTOCK.agent import LivestockAgent
from .H11_AQUACULTURA.agent import AquaculturaAgent
from .H11_FOODSCI.agent import FoodsciAgent
from .H11_FERMENTATIO.agent import FermentatioAgent
from .H11_GASTRONOMIA.agent import GastronomiaAgent
from .H11_VITICULTURA.agent import ViticulturaAgent
from .H11_FOODTECH.agent import FoodtechAgent
from .H11_PRECISIONAG.agent import PrecisionagAgent
from .H11_SOILSCI.agent import SoilsciAgent

__all__ = [
    "CropAgent",
    "HorticulturaAgent",
    "IrrigatioAgent",
    "LivestockAgent",
    "AquaculturaAgent",
    "FoodsciAgent",
    "FermentatioAgent",
    "GastronomiaAgent",
    "ViticulturaAgent",
    "FoodtechAgent",
    "PrecisionagAgent",
    "SoilsciAgent"
]
