"""gate-twin: digital twin of the Armstrong Gate (U.S. Patent 12,409,695 B2)."""

from .bench import BenchRig, raised_cosine, sine, still
from .generator import ClawPoleAlternator, NullGenerator, PMGenerator
from .model import QuarterCarGate, SimResult
from .params import DEFAULT_PARAMS_PATH, Params, load_params
from .roads import ISO8608_GD0, RoadProfile, iso8608_profile

__version__ = "0.1.0.dev0"

__all__ = [
    "BenchRig",
    "raised_cosine",
    "sine",
    "still",
    "ClawPoleAlternator",
    "NullGenerator",
    "PMGenerator",
    "QuarterCarGate",
    "SimResult",
    "Params",
    "load_params",
    "DEFAULT_PARAMS_PATH",
    "RoadProfile",
    "iso8608_profile",
    "ISO8608_GD0",
]
