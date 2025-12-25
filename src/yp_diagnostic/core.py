"""
Core computation module for yp-diagnostic.

This module provides the compute_x_y function for calculating diagnostic
coordinates. It is strictly a diagnostic tool and does not infer, predict,
or model system behavior.
"""

import warnings
from typing import Tuple, Union

import numpy as np


# Numerical constant: maximum x value before clipping to prevent divergence
# This corresponds to y = 1000 approximately
_X_CLIP_MAX = 0.999999


def compute_x_y(
    p1: Union[float, np.ndarray],
    p2: Union[float, np.ndarray],
    p1_name: str,
    p2_name: str,
    failure_definition: str,
) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Compute the diagnostic coordinate (x, y) from p1 and p2.

    This function computes:
        x = p2 / p1
        y = (1 - x)^(-1/2)

    INTERPRETATION WARNING:
        This is a DIAGNOSTIC coordinate only. It:
        - Does NOT predict system failure
        - Does NOT model system dynamics
        - Does NOT imply causation or mechanism
        - Does NOT claim universality

        The coordinate y indicates when the ratio x = p2/p1 approaches 1.
        As x -> 1, y diverges. This flags a regime where small changes
        in x produce large changes in y. No further interpretation is
        warranted without domain-specific validation.

    Parameters
    ----------
    p1 : float or np.ndarray
        The reference value (e.g., capacity). Must be positive.
    p2 : float or np.ndarray
        The comparison value (e.g., load). Must be non-negative.
    p1_name : str
        Semantic description of p1 (e.g., "server_capacity_requests_per_sec").
        Required for interpretability. Cannot be empty.
    p2_name : str
        Semantic description of p2 (e.g., "current_load_requests_per_sec").
        Required for interpretability. Cannot be empty.
    failure_definition : str
        Definition of what constitutes failure in this context
        (e.g., "response_time_exceeds_500ms"). Required for interpretability.
        Cannot be empty.

    Returns
    -------
    x : float or np.ndarray
        The ratio p2 / p1.
    y : float or np.ndarray
        The diagnostic coordinate (1 - x)^(-1/2).

    Raises
    ------
    ValueError
        If p1_name, p2_name, or failure_definition is missing or empty.
        If p1 <= 0 or p2 < 0.

    Warns
    -----
    UserWarning
        If x >= 0.9 (approaching capacity threshold).
        If x >= 1.0 (at or exceeding capacity).

    Examples
    --------
    >>> x, y = compute_x_y(
    ...     p1=100.0,
    ...     p2=85.0,
    ...     p1_name="capacity",
    ...     p2_name="load",
    ...     failure_definition="timeout"
    ... )
    >>> print(f"x={x:.3f}, y={y:.3f}")
    x=0.850, y=2.582
    """
    # Validate semantic metadata is provided
    # Why: Enforce interpretability by requiring explicit context
    if not p1_name or not isinstance(p1_name, str) or p1_name.strip() == "":
        raise ValueError(
            "p1_name is required and must be a non-empty string. "
            "This ensures the diagnostic coordinate has explicit semantic context."
        )

    if not p2_name or not isinstance(p2_name, str) or p2_name.strip() == "":
        raise ValueError(
            "p2_name is required and must be a non-empty string. "
            "This ensures the diagnostic coordinate has explicit semantic context."
        )

    if (
        not failure_definition
        or not isinstance(failure_definition, str)
        or failure_definition.strip() == ""
    ):
        raise ValueError(
            "failure_definition is required and must be a non-empty string. "
            "This ensures the diagnostic coordinate has explicit semantic context."
        )

    # Convert to numpy arrays for uniform handling
    p1_arr = np.asarray(p1)
    p2_arr = np.asarray(p2)

    # Validate numerical constraints
    # Why: p1 must be positive to avoid division by zero or negative ratios
    if np.any(p1_arr <= 0):
        raise ValueError(
            f"p1 must be positive. Received values <= 0. "
            f"p1 represents '{p1_name}' which must be a positive reference value."
        )

    # Why: p2 must be non-negative as it represents a quantity being compared
    if np.any(p2_arr < 0):
        raise ValueError(
            f"p2 must be non-negative. Received values < 0. "
            f"p2 represents '{p2_name}' which cannot be negative."
        )

    # Compute x = p2 / p1
    x = p2_arr / p1_arr

    # Check for warning conditions and issue appropriate warnings
    # Why: Alert user when approaching or exceeding capacity threshold
    if np.any(x >= 1.0):
        warnings.warn(
            f"x >= 1.0 detected (p2 >= p1). The diagnostic coordinate y will be "
            f"clipped to prevent numerical divergence. This indicates '{p2_name}' "
            f"meets or exceeds '{p1_name}'. Interpretation: the system may be at "
            f"or beyond the threshold defined by '{failure_definition}'. "
            f"This is a diagnostic flag, not a prediction.",
            UserWarning,
            stacklevel=2,
        )
    elif np.any(x >= 0.9):
        warnings.warn(
            f"x >= 0.9 detected (p2/p1 >= 0.9). The system is approaching the "
            f"capacity threshold. '{p2_name}' is within 10% of '{p1_name}'. "
            f"This is a diagnostic flag indicating proximity to threshold, "
            f"not a prediction of failure.",
            UserWarning,
            stacklevel=2,
        )

    # Clip x to prevent numerical divergence as x -> 1
    # Why: (1-x)^(-1/2) diverges as x -> 1, so we clip to maintain numerical stability
    x_clipped = np.clip(x, None, _X_CLIP_MAX)

    # Compute y = (1 - x)^(-1/2)
    y = np.power(1.0 - x_clipped, -0.5)

    # Return scalar if input was scalar
    if p1_arr.ndim == 0 and p2_arr.ndim == 0:
        return float(x), float(y)

    return x, y
