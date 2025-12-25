"""
yp-diagnostic: A diagnostic coordinate for finite systems near capacity thresholds.

This package computes a diagnostic coordinate y(p) = (1 - p2/p1)^(-1/2) that
indicates when a ratio x = p2/p1 approaches 1.

SCOPE:
    This is a DIAGNOSTIC tool only. It:
    - Computes x = p2/p1 and y = (1-x)^(-1/2)
    - Propagates uncertainty
    - Enforces semantic guardrails

    It does NOT:
    - Infer p1 or p2 from data
    - Model system dynamics
    - Predict transitions or failures
    - Claim universality, causality, or mechanism

See README.md and docs/scope.md for full scope and limitations.
"""

__version__ = "1.0.0"

from yp_diagnostic.core import compute_x_y
from yp_diagnostic.uncertainty import bootstrap_ci, delta_method_ci
from yp_diagnostic.validation import (
    collapse_test,
    negative_control_plot,
    sensitivity_check,
)

__all__ = [
    "compute_x_y",
    "bootstrap_ci",
    "delta_method_ci",
    "collapse_test",
    "negative_control_plot",
    "sensitivity_check",
]
