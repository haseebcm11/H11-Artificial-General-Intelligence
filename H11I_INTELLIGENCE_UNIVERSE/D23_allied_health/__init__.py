"""
Domain 23 - Allied Health & Therapies
"""
from .H11_PHYSIOTHERAPIA.agent import PhysiotherapiaAgent
from .H11_OCCUPATIONAL.agent import OccupationalAgent
from .H11_SPEECH.agent import SpeechPathologyAgent
from .H11_DIETETICA.agent import DieteticaAgent
from .H11_RESPIRATORY.agent import RespiratoryAgent
from .H11_ORTHOTICA.agent import OrthoticaAgent
from .H11_AUDIOLOGIA.agent import AudiologiaAgent
from .H11_OPTOMETRIA.agent import OptometriaAgent
from .H11_PODIATRIA.agent import PodiatriaAgent
from .H11_MIDWIFERY.agent import MidwiferyAgent

__all__ = [
    "PhysiotherapiaAgent",
    "OccupationalAgent",
    "SpeechPathologyAgent",
    "DieteticaAgent",
    "RespiratoryAgent",
    "OrthoticaAgent",
    "AudiologiaAgent",
    "OptometriaAgent",
    "PodiatriaAgent",
    "MidwiferyAgent"
]
