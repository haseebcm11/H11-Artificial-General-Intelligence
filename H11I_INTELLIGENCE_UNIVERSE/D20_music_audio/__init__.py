"""
Domain 20 - Music & Audio

This module exposes the agents responsible for musical and auditory intelligence.
"""

from .H11_COMPOSITIO.agent import CompositioAgent
from .H11_HARMONIA.agent import HarmoniaAgent
from .H11_RHYTHMUS.agent import RhythmusAgent
from .H11_ORCHESTRATIO.agent import OrchestratioAgent
from .H11_MUSICPROD.agent import MusicprodAgent
from .H11_AUDIOENG.agent import AudioengAgent
from .H11_CLASSICA_MUS.agent import ClassicaMusAgent
from .H11_JAZZ.agent import JazzAgent
from .H11_ELECTRONICA_MUS.agent import ElectronicaMusAgent
from .H11_WORLDMUS.agent import WorldmusAgent
from .H11_FILMSCORE.agent import FilmscoreAgent
from .H11_SOUNDDESIGN.agent import SounddesignAgent

__all__ = [
    "CompositioAgent",
    "HarmoniaAgent",
    "RhythmusAgent",
    "OrchestratioAgent",
    "MusicprodAgent",
    "AudioengAgent",
    "ClassicaMusAgent",
    "JazzAgent",
    "ElectronicaMusAgent",
    "WorldmusAgent",
    "FilmscoreAgent",
    "SounddesignAgent",
]
