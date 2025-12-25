"""
Validation utilities for yp-diagnostic.

This module provides diagnostic utilities for examining the behavior of
the y(p) coordinate. These functions report diagnostics only; they do
NOT determine correctness or validate any claims about system behavior.

INTERPRETATION WARNING:
    These utilities are for exploratory analysis and reproducibility checking.
    They do NOT validate that y(p) is appropriate for your system.
    They do NOT determine whether thresholds are meaningful.
    They do NOT test hypotheses about system behavior.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np


def collapse_test(
    p1_arrays: List[np.ndarray],
    p2_arrays: List[np.ndarray],
    labels: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Compute x and y for multiple datasets to examine collapse behavior.

    This function computes the diagnostic coordinates for multiple datasets
    and returns them for comparison. It does NOT determine whether collapse
    is meaningful or significant.

    WHAT THIS DOES:
        - Computes x = p2/p1 and y = (1-x)^(-1/2) for each dataset.
        - Returns arrays suitable for plotting on common axes.
        - Reports basic statistics (min, max, mean) for each dataset.

    WHAT THIS DOES NOT DO:
        - Does NOT test for statistical significance of collapse.
        - Does NOT determine if collapse is meaningful for your system.
        - Does NOT validate any theoretical claims.

    Parameters
    ----------
    p1_arrays : list of np.ndarray
        List of p1 arrays, one per dataset.
    p2_arrays : list of np.ndarray
        List of p2 arrays, one per dataset. Must match p1_arrays in length.
    labels : list of str, optional
        Labels for each dataset. If None, datasets are numbered.

    Returns
    -------
    dict
        Dictionary containing:
        - 'datasets': List of dicts, each with 'label', 'x', 'y', 'stats'.
        - 'n_datasets': Number of datasets processed.

    Raises
    ------
    ValueError
        If p1_arrays and p2_arrays have different lengths.
        If any p1 array contains non-positive values.
        If any p2 array contains negative values.

    Examples
    --------
    >>> p1_a = np.array([100, 100, 100])
    >>> p2_a = np.array([50, 75, 90])
    >>> p1_b = np.array([200, 200, 200])
    >>> p2_b = np.array([100, 150, 180])
    >>> result = collapse_test([p1_a, p1_b], [p2_a, p2_b], ['A', 'B'])
    """
    if len(p1_arrays) != len(p2_arrays):
        raise ValueError(
            f"p1_arrays and p2_arrays must have the same length. "
            f"Got {len(p1_arrays)} and {len(p2_arrays)}."
        )

    if labels is None:
        labels = [f"dataset_{i}" for i in range(len(p1_arrays))]

    if len(labels) != len(p1_arrays):
        raise ValueError(
            f"labels must have the same length as p1_arrays. "
            f"Got {len(labels)} labels and {len(p1_arrays)} arrays."
        )

    datasets = []

    for i, (p1, p2, label) in enumerate(zip(p1_arrays, p2_arrays, labels)):
        p1 = np.asarray(p1)
        p2 = np.asarray(p2)

        # Validate constraints
        if np.any(p1 <= 0):
            raise ValueError(
                f"Dataset '{label}': p1 must be positive. Found non-positive values."
            )
        if np.any(p2 < 0):
            raise ValueError(
                f"Dataset '{label}': p2 must be non-negative. Found negative values."
            )

        # Compute x and y
        x = p2 / p1
        x_clipped = np.clip(x, None, 0.999999)
        y = np.power(1.0 - x_clipped, -0.5)

        # Compute basic statistics for reporting
        stats = {
            "x_min": float(np.min(x)),
            "x_max": float(np.max(x)),
            "x_mean": float(np.mean(x)),
            "y_min": float(np.min(y)),
            "y_max": float(np.max(y)),
            "y_mean": float(np.mean(y)),
            "n_points": int(x.size),
        }

        datasets.append(
            {
                "label": label,
                "x": x,
                "y": y,
                "stats": stats,
            }
        )

    return {
        "datasets": datasets,
        "n_datasets": len(datasets),
    }


def negative_control_plot(
    p1: np.ndarray,
    p2_real: np.ndarray,
    n_shuffles: int = 100,
    random_state: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate shuffled negative controls for comparison.

    This function generates shuffled versions of p2 to serve as negative
    controls. Comparing real data against shuffled data can help identify
    whether observed patterns differ from random baseline.

    WHAT THIS DOES:
        - Shuffles p2 values n_shuffles times.
        - Computes x and y for each shuffle.
        - Returns arrays suitable for comparison plotting.

    WHAT THIS DOES NOT DO:
        - Does NOT perform statistical hypothesis testing.
        - Does NOT determine significance or p-values.
        - Does NOT validate any claims about the real data.

    Parameters
    ----------
    p1 : np.ndarray
        The reference values.
    p2_real : np.ndarray
        The real comparison values.
    n_shuffles : int, default=100
        Number of shuffled negative controls to generate.
    random_state : int, optional
        Random seed for reproducibility.

    Returns
    -------
    dict
        Dictionary containing:
        - 'real': Dict with 'x' and 'y' for real data.
        - 'shuffled': List of dicts, each with 'x' and 'y' for shuffled data.
        - 'n_shuffles': Number of shuffles performed.

    Raises
    ------
    ValueError
        If p1 contains non-positive values.
        If p2_real contains negative values.
        If p1 and p2_real have different shapes.

    Examples
    --------
    >>> p1 = np.array([100, 100, 100, 100])
    >>> p2 = np.array([50, 75, 85, 95])
    >>> result = negative_control_plot(p1, p2, n_shuffles=50, random_state=42)
    """
    rng = np.random.default_rng(random_state)

    p1 = np.asarray(p1)
    p2_real = np.asarray(p2_real)

    if p1.shape != p2_real.shape:
        raise ValueError(
            f"p1 and p2_real must have the same shape. "
            f"Got p1.shape={p1.shape}, p2_real.shape={p2_real.shape}"
        )

    if np.any(p1 <= 0):
        raise ValueError("p1 must be positive. Found non-positive values.")
    if np.any(p2_real < 0):
        raise ValueError("p2_real must be non-negative. Found negative values.")

    # Compute real data coordinates
    x_real = p2_real / p1
    x_real_clipped = np.clip(x_real, None, 0.999999)
    y_real = np.power(1.0 - x_real_clipped, -0.5)

    # Generate shuffled controls
    shuffled_results = []
    for _ in range(n_shuffles):
        p2_shuffled = rng.permutation(p2_real)
        x_shuf = p2_shuffled / p1
        x_shuf_clipped = np.clip(x_shuf, None, 0.999999)
        y_shuf = np.power(1.0 - x_shuf_clipped, -0.5)
        shuffled_results.append({"x": x_shuf, "y": y_shuf})

    return {
        "real": {"x": x_real, "y": y_real},
        "shuffled": shuffled_results,
        "n_shuffles": n_shuffles,
    }


def sensitivity_check(
    p1: Union[float, np.ndarray],
    p2: Union[float, np.ndarray],
    perturbation_fractions: Optional[List[float]] = None,
) -> Dict[str, Any]:
    """
    Check sensitivity of y to perturbations in p1 and p2.

    This function applies small perturbations to p1 and p2 and reports
    how y changes. This helps understand the local sensitivity of the
    diagnostic coordinate.

    WHAT THIS DOES:
        - Applies fractional perturbations to p1 and p2.
        - Reports the resulting change in x and y.
        - Computes local sensitivity (dy/y)/(dp/p).

    WHAT THIS DOES NOT DO:
        - Does NOT determine if sensitivity is acceptable.
        - Does NOT validate measurement precision requirements.
        - Does NOT account for correlated errors.

    Parameters
    ----------
    p1 : float or np.ndarray
        The reference value(s).
    p2 : float or np.ndarray
        The comparison value(s).
    perturbation_fractions : list of float, optional
        Fractional perturbations to apply (e.g., [0.01, 0.05, 0.10] for
        1%, 5%, 10% perturbations). Default is [0.01, 0.05, 0.10].

    Returns
    -------
    dict
        Dictionary containing:
        - 'baseline': Dict with 'x' and 'y' at nominal values.
        - 'p1_sensitivity': List of dicts showing y response to p1 perturbations.
        - 'p2_sensitivity': List of dicts showing y response to p2 perturbations.

    Raises
    ------
    ValueError
        If p1 <= 0 or p2 < 0.

    Examples
    --------
    >>> result = sensitivity_check(p1=100.0, p2=85.0)
    >>> for entry in result['p1_sensitivity']:
    ...     print(f"p1 +{entry['perturbation']*100:.0f}%: y changes by {entry['y_change_pct']:.1f}%")
    """
    if perturbation_fractions is None:
        perturbation_fractions = [0.01, 0.05, 0.10]

    p1_arr = np.asarray(p1)
    p2_arr = np.asarray(p2)

    if np.any(p1_arr <= 0):
        raise ValueError("p1 must be positive.")
    if np.any(p2_arr < 0):
        raise ValueError("p2 must be non-negative.")

    # Compute baseline
    x_base = p2_arr / p1_arr
    x_base_clipped = np.clip(x_base, None, 0.999999)
    y_base = np.power(1.0 - x_base_clipped, -0.5)

    # For scalar inputs, convert to float for output
    if p1_arr.ndim == 0:
        x_base = float(x_base)
        y_base = float(y_base)

    baseline = {"x": x_base, "y": y_base}

    # Compute p1 sensitivity (increasing p1 decreases x, decreases y)
    p1_sensitivity = []
    for frac in perturbation_fractions:
        p1_perturbed = p1_arr * (1 + frac)
        x_pert = p2_arr / p1_perturbed
        x_pert_clipped = np.clip(x_pert, None, 0.999999)
        y_pert = np.power(1.0 - x_pert_clipped, -0.5)

        if p1_arr.ndim == 0:
            y_change_pct = (float(y_pert) - float(y_base)) / float(y_base) * 100
            p1_sensitivity.append(
                {
                    "perturbation": frac,
                    "p1_perturbed": float(p1_perturbed),
                    "x_new": float(x_pert),
                    "y_new": float(y_pert),
                    "y_change_pct": y_change_pct,
                }
            )
        else:
            y_change_pct = (y_pert - y_base) / y_base * 100
            p1_sensitivity.append(
                {
                    "perturbation": frac,
                    "x_new": x_pert,
                    "y_new": y_pert,
                    "y_change_pct_mean": float(np.mean(y_change_pct)),
                }
            )

    # Compute p2 sensitivity (increasing p2 increases x, increases y)
    p2_sensitivity = []
    for frac in perturbation_fractions:
        p2_perturbed = p2_arr * (1 + frac)
        x_pert = p2_perturbed / p1_arr
        x_pert_clipped = np.clip(x_pert, None, 0.999999)
        y_pert = np.power(1.0 - x_pert_clipped, -0.5)

        if p2_arr.ndim == 0:
            y_change_pct = (float(y_pert) - float(y_base)) / float(y_base) * 100
            p2_sensitivity.append(
                {
                    "perturbation": frac,
                    "p2_perturbed": float(p2_perturbed),
                    "x_new": float(x_pert),
                    "y_new": float(y_pert),
                    "y_change_pct": y_change_pct,
                }
            )
        else:
            y_change_pct = (y_pert - y_base) / y_base * 100
            p2_sensitivity.append(
                {
                    "perturbation": frac,
                    "x_new": x_pert,
                    "y_new": y_pert,
                    "y_change_pct_mean": float(np.mean(y_change_pct)),
                }
            )

    return {
        "baseline": baseline,
        "p1_sensitivity": p1_sensitivity,
        "p2_sensitivity": p2_sensitivity,
    }
