"""aks-lab: computational home of Armstrong Kinetic Solutions.

Models ONLY the mechanism of US 12,409,695 B2.  Every number this package
produces is reproducible from a command and tagged measured / modeled / target.
"""

from .bench.harness import BenchRig, raised_cosine, sine_stroke, still
from .elements.gate import Gate, GateParams, linear_gate
from .elements.generator import ClawPoleAlternator, LinearGenerator, NullGenerator, PMGenerator
from .params import gate_from_yaml, load_gate_raw
from .roads import iso8608_profile, white_velocity_level
from .vehicles import CornerParams, PassiveQuarterCar, QuarterCarGate, SimResult, corner

__all__ = [
    "BenchRig", "raised_cosine", "sine_stroke", "still",
    "Gate", "GateParams", "linear_gate",
    "ClawPoleAlternator", "LinearGenerator", "NullGenerator", "PMGenerator",
    "gate_from_yaml", "load_gate_raw",
    "iso8608_profile", "white_velocity_level",
    "CornerParams", "PassiveQuarterCar", "QuarterCarGate", "SimResult", "corner",
]
__version__ = "0.2.0.dev0"
