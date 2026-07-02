"""Provenance and parameter-integrity tests (honesty norms, CLAUDE.md)."""

import math

from gatetwin import Params, load_params
from gatetwin.params import missing_provenance


def test_every_parameter_has_provenance():
    _, raw = load_params()
    assert missing_provenance(raw) == []


def test_yaml_matches_dataclass_defaults():
    p, _ = load_params()
    d = Params()
    assert p == d, "params.yaml and Params defaults have drifted apart"


def test_patent_constraint_soft_first():
    """Claims 2/11: biasing spring rate strictly lower than main spring rate."""
    p, _ = load_params()
    assert p.k_b < p.k_s


def test_derived_ratios():
    p, _ = load_params()
    assert math.isclose(p.Gt, 2 * math.pi * p.n_step / p.lead)
    body_hz = math.sqrt(p.k_s / p.m_s) / (2 * math.pi)
    hop_hz = math.sqrt((p.k_s + p.k_t) / p.m_u) / (2 * math.pi)
    assert 1.0 <= body_hz <= 1.5, body_hz
    assert 9.0 <= hop_hz <= 15.0, hop_hz
