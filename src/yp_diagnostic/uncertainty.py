"""
Uncertainty propagation module for yp-diagnostic.

This module provides functions for propagating uncertainty from p1 and p2
measurements into the diagnostic coordinate y. Two methods are provided:
bootstrap resampling and the delta method.

INTERPRETATION WARNING:
    These uncertainty estimates apply to the computed diagnostic coordinate only.
    They do NOT represent prediction intervals for system behavior.
    They do NOT account for model misspecification or systematic errors.
"""

import warnings
from typing import Dict, Optional, Tuple, Union

import numpy as np
from scipy import stats


def bootstrap_ci(
    p1: Union[float, np.ndarray],
    p2: Union[float, np.ndarray],
    p1_std: Optional[float] = None,
    p2_std: Optional[float] = None,
    n_boot: int = 2000,
    confidence_level: float = 0.95,
    random_state: Optional[int] = None,
) -> Dict[str, Union[float, Tuple[float, float]]]:
    """
    Compute bootstrap confidence intervals for x and y.

    This function propagates uncertainty from p1 and p2 into the diagnostic
    coordinates x and y using bootstrap resampling.

    ASSUMPTIONS:
        - If p1 and p2 are scalars with standard deviations provided,
          samples are drawn from normal distributions centered at p1, p2.
        - If p1 and p2 are arrays, bootstrap resampling is performed on
          paired observations.
        - Independence between bootstrap samples is assumed.
        - The bootstrap distribution approximates the sampling distribution.

    LIMITATIONS:
        - Does not account for systematic errors or biases.
        - Normal distribution assumption may not hold for all data.
        - Confidence intervals are for the diagnostic coordinate only,
          not for any system behavior or outcome.

    Parameters
    ----------
    p1 : float or np.ndarray
        The reference value(s). If scalar, p1_std should be provided.
        If array, represents multiple observations.
    p2 : float or np.ndarray
        The comparison value(s). If scalar, p2_std should be provided.
        If array, represents multiple observations.
    p1_std : float, optional
        Standard deviation of p1 (required if p1 is scalar).
    p2_std : float, optional
        Standard deviation of p2 (required if p2 is scalar).
    n_boot : int, default=2000
        Number of bootstrap resamples.
    confidence_level : float, default=0.95
        Confidence level for intervals (e.g., 0.95 for 95% CI).
    random_state : int, optional
        Random seed for reproducibility.

    Returns
    -------
    dict
        Dictionary containing:
        - 'x_mean': Mean of x across bootstrap samples.
        - 'x_ci': Tuple of (lower, upper) confidence interval for x.
        - 'y_mean': Mean of y across bootstrap samples.
        - 'y_ci': Tuple of (lower, upper) confidence interval for y.
        - 'n_boot': Number of bootstrap samples used.

    Raises
    ------
    ValueError
        If scalar inputs are provided without standard deviations.
        If array inputs have mismatched lengths.

    Examples
    --------
    >>> result = bootstrap_ci(p1=100.0, p2=85.0, p1_std=5.0, p2_std=3.0)
    >>> print(f"y = {result['y_mean']:.3f}, 95% CI: {result['y_ci']}")
    """
    rng = np.random.default_rng(random_state)

    # Warn if bootstrap sample count may be insufficient
    # Why: Too few samples can lead to unstable confidence intervals
    if n_boot < 1000:
        warnings.warn(
            f"n_boot={n_boot} may be insufficient for stable confidence intervals. "
            f"Consider n_boot >= 1000 (default is 2000) for reliable estimates.",
            UserWarning,
            stacklevel=2,
        )

    p1_arr = np.asarray(p1)
    p2_arr = np.asarray(p2)

    # Handle scalar inputs with standard deviations
    if p1_arr.ndim == 0 and p2_arr.ndim == 0:
        if p1_std is None or p2_std is None:
            raise ValueError(
                "When p1 and p2 are scalars, p1_std and p2_std must be provided "
                "to generate bootstrap samples."
            )

        # Generate samples assuming normal distribution
        # Why: Without raw data, we assume measurement uncertainty is normally distributed
        p1_samples = rng.normal(float(p1), p1_std, size=n_boot)
        p2_samples = rng.normal(float(p2), p2_std, size=n_boot)

        # Ensure physical constraints: p1 > 0, p2 >= 0
        # Why: Invalid samples would produce undefined x or y values
        p1_samples = np.maximum(p1_samples, 1e-10)
        p2_samples = np.maximum(p2_samples, 0.0)

    else:
        # Handle array inputs via paired bootstrap resampling
        if p1_arr.shape != p2_arr.shape:
            raise ValueError(
                f"p1 and p2 arrays must have the same shape. "
                f"Got p1.shape={p1_arr.shape}, p2.shape={p2_arr.shape}"
            )

        n_obs = p1_arr.size
        # Generate bootstrap indices and resample
        # Why: Paired resampling preserves correlation structure between p1 and p2
        indices = rng.integers(0, n_obs, size=(n_boot, n_obs))
        p1_samples = p1_arr.flat[indices].mean(axis=1)
        p2_samples = p2_arr.flat[indices].mean(axis=1)

    # Compute x and y for each bootstrap sample
    x_samples = p2_samples / p1_samples

    # Clip x to prevent divergence
    # Why: (1-x)^(-1/2) diverges as x -> 1
    x_clipped = np.clip(x_samples, None, 0.999999)
    y_samples = np.power(1.0 - x_clipped, -0.5)

    # Compute confidence intervals using percentile method
    # Why: Percentile method is robust and does not assume normality of bootstrap distribution
    alpha = 1.0 - confidence_level
    lower_pct = 100 * (alpha / 2)
    upper_pct = 100 * (1 - alpha / 2)

    x_ci = (
        float(np.percentile(x_samples, lower_pct)),
        float(np.percentile(x_samples, upper_pct)),
    )
    y_ci = (
        float(np.percentile(y_samples, lower_pct)),
        float(np.percentile(y_samples, upper_pct)),
    )

    return {
        "x_mean": float(np.mean(x_samples)),
        "x_ci": x_ci,
        "y_mean": float(np.mean(y_samples)),
        "y_ci": y_ci,
        "n_boot": n_boot,
    }


def delta_method_ci(
    p1: float,
    p2: float,
    p1_std: float,
    p2_std: float,
    cov_p1_p2: float = 0.0,
    confidence_level: float = 0.95,
) -> Dict[str, Union[float, Tuple[float, float]]]:
    """
    Compute confidence intervals for x and y using the delta method.

    The delta method provides approximate confidence intervals by
    linearizing the transformation around the point estimate.

    ASSUMPTIONS:
        - p1 and p2 are approximately normally distributed.
        - The transformation is approximately linear in the region
          of uncertainty (valid when standard errors are small relative
          to the point estimates).
        - First-order Taylor expansion is adequate.

    LIMITATIONS:
        - Accuracy degrades as x approaches 1 (nonlinearity increases).
        - Accuracy degrades when standard errors are large relative to means.
        - Does not account for non-normal distributions.
        - Confidence intervals are for the diagnostic coordinate only.

    Parameters
    ----------
    p1 : float
        The reference value. Must be positive.
    p2 : float
        The comparison value. Must be non-negative.
    p1_std : float
        Standard deviation of p1.
    p2_std : float
        Standard deviation of p2.
    cov_p1_p2 : float, default=0.0
        Covariance between p1 and p2. Default assumes independence.
    confidence_level : float, default=0.95
        Confidence level for intervals.

    Returns
    -------
    dict
        Dictionary containing:
        - 'x': Point estimate of x.
        - 'x_std': Standard error of x.
        - 'x_ci': Tuple of (lower, upper) confidence interval for x.
        - 'y': Point estimate of y.
        - 'y_std': Standard error of y.
        - 'y_ci': Tuple of (lower, upper) confidence interval for y.

    Raises
    ------
    ValueError
        If p1 <= 0 or p2 < 0.
        If standard deviations are negative.

    Examples
    --------
    >>> result = delta_method_ci(p1=100.0, p2=85.0, p1_std=5.0, p2_std=3.0)
    >>> print(f"y = {result['y']:.3f} +/- {result['y_std']:.3f}")
    """
    # Validate inputs
    if p1 <= 0:
        raise ValueError(f"p1 must be positive. Got p1={p1}")
    if p2 < 0:
        raise ValueError(f"p2 must be non-negative. Got p2={p2}")
    if p1_std < 0 or p2_std < 0:
        raise ValueError(
            f"Standard deviations must be non-negative. "
            f"Got p1_std={p1_std}, p2_std={p2_std}"
        )

    # Compute x = p2 / p1
    x = p2 / p1

    # Warn about accuracy degradation in high-x regime
    # Why: The nonlinearity of (1-x)^(-1/2) increases as x approaches 1,
    # making the first-order Taylor approximation less accurate
    if x > 0.9:
        warnings.warn(
            f"x = {x:.3f} > 0.9: Delta method accuracy degrades as x approaches 1. "
            f"The first-order Taylor approximation becomes less reliable in the "
            f"high-x regime. Consider using bootstrap_ci for more robust uncertainty "
            f"estimates when x > 0.9.",
            UserWarning,
            stacklevel=2,
        )

    # Compute variance of x using delta method
    # For x = p2/p1:
    #   dx/dp1 = -p2/p1^2
    #   dx/dp2 = 1/p1
    # Var(x) = (dx/dp1)^2 * Var(p1) + (dx/dp2)^2 * Var(p2) + 2*(dx/dp1)*(dx/dp2)*Cov(p1,p2)
    dx_dp1 = -p2 / (p1**2)
    dx_dp2 = 1.0 / p1

    var_x = (
        (dx_dp1**2) * (p1_std**2)
        + (dx_dp2**2) * (p2_std**2)
        + 2 * dx_dp1 * dx_dp2 * cov_p1_p2
    )
    x_std = np.sqrt(max(var_x, 0.0))  # Ensure non-negative due to numerical issues

    # Compute y = (1 - x)^(-1/2)
    # Clip x to prevent divergence
    x_clipped = min(x, 0.999999)
    y = (1.0 - x_clipped) ** (-0.5)

    # Compute variance of y using delta method
    # For y = (1-x)^(-1/2):
    #   dy/dx = (1/2) * (1-x)^(-3/2)
    # Var(y) = (dy/dx)^2 * Var(x)
    dy_dx = 0.5 * ((1.0 - x_clipped) ** (-1.5))
    var_y = (dy_dx**2) * var_x
    y_std = np.sqrt(max(var_y, 0.0))

    # Compute confidence intervals assuming normal distribution
    # Why: Delta method assumes asymptotic normality
    z = stats.norm.ppf(1 - (1 - confidence_level) / 2)

    x_ci = (x - z * x_std, x + z * x_std)
    y_ci = (y - z * y_std, y + z * y_std)

    return {
        "x": x,
        "x_std": x_std,
        "x_ci": x_ci,
        "y": y,
        "y_std": y_std,
        "y_ci": y_ci,
    }
