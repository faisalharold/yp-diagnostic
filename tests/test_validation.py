"""
Tests for yp_diagnostic.validation module.

These tests verify:
- Correct output structure from validation functions
- Input validation and error handling
- Reproducibility with random seeds
- No side effects from function calls
"""

import numpy as np
import pytest

from yp_diagnostic.validation import (
    collapse_test,
    negative_control_plot,
    sensitivity_check,
)
from yp_diagnostic.uncertainty import bootstrap_ci, delta_method_ci


class TestCollapseTest:
    """Tests for the collapse_test function."""

    def test_basic_collapse_test(self):
        """Test basic collapse_test with two datasets."""
        p1_a = np.array([100.0, 100.0, 100.0])
        p2_a = np.array([50.0, 75.0, 90.0])
        p1_b = np.array([200.0, 200.0, 200.0])
        p2_b = np.array([100.0, 150.0, 180.0])

        result = collapse_test([p1_a, p1_b], [p2_a, p2_b], ["A", "B"])

        assert result["n_datasets"] == 2
        assert len(result["datasets"]) == 2
        assert result["datasets"][0]["label"] == "A"
        assert result["datasets"][1]["label"] == "B"

    def test_collapse_test_output_structure(self):
        """Verify output structure contains expected keys."""
        p1 = np.array([100.0, 100.0])
        p2 = np.array([50.0, 75.0])

        result = collapse_test([p1], [p2], ["test"])

        dataset = result["datasets"][0]
        assert "label" in dataset
        assert "x" in dataset
        assert "y" in dataset
        assert "stats" in dataset

        stats = dataset["stats"]
        assert "x_min" in stats
        assert "x_max" in stats
        assert "x_mean" in stats
        assert "y_min" in stats
        assert "y_max" in stats
        assert "y_mean" in stats
        assert "n_points" in stats

    def test_collapse_test_computes_correct_x_y(self):
        """Verify x and y are computed correctly."""
        p1 = np.array([100.0])
        p2 = np.array([50.0])

        result = collapse_test([p1], [p2])

        x = result["datasets"][0]["x"]
        y = result["datasets"][0]["y"]

        assert x[0] == pytest.approx(0.5)
        assert y[0] == pytest.approx(np.sqrt(2))

    def test_collapse_test_mismatched_lengths_raises_error(self):
        """Verify error when p1_arrays and p2_arrays have different lengths."""
        p1 = np.array([100.0])
        p2 = np.array([50.0])

        with pytest.raises(ValueError, match="same length"):
            collapse_test([p1, p1], [p2])

    def test_collapse_test_invalid_p1_raises_error(self):
        """Verify error when p1 contains non-positive values."""
        p1 = np.array([0.0, 100.0])
        p2 = np.array([50.0, 50.0])

        with pytest.raises(ValueError, match="p1 must be positive"):
            collapse_test([p1], [p2])

    def test_collapse_test_invalid_p2_raises_error(self):
        """Verify error when p2 contains negative values."""
        p1 = np.array([100.0, 100.0])
        p2 = np.array([-10.0, 50.0])

        with pytest.raises(ValueError, match="p2 must be non-negative"):
            collapse_test([p1], [p2])

    def test_collapse_test_default_labels(self):
        """Verify default labels are generated when not provided."""
        p1 = np.array([100.0])
        p2 = np.array([50.0])

        result = collapse_test([p1, p1], [p2, p2])

        assert result["datasets"][0]["label"] == "dataset_0"
        assert result["datasets"][1]["label"] == "dataset_1"


class TestNegativeControlPlot:
    """Tests for the negative_control_plot function."""

    def test_basic_negative_control(self):
        """Test basic negative control generation."""
        p1 = np.array([100.0, 100.0, 100.0, 100.0])
        p2 = np.array([50.0, 75.0, 85.0, 95.0])

        result = negative_control_plot(p1, p2, n_shuffles=10, random_state=42)

        assert "real" in result
        assert "shuffled" in result
        assert result["n_shuffles"] == 10
        assert len(result["shuffled"]) == 10

    def test_negative_control_real_data_structure(self):
        """Verify real data has expected structure."""
        p1 = np.array([100.0, 100.0])
        p2 = np.array([50.0, 75.0])

        result = negative_control_plot(p1, p2, n_shuffles=5, random_state=42)

        assert "x" in result["real"]
        assert "y" in result["real"]
        assert len(result["real"]["x"]) == 2
        assert len(result["real"]["y"]) == 2

    def test_negative_control_shuffled_structure(self):
        """Verify shuffled data has expected structure."""
        p1 = np.array([100.0, 100.0])
        p2 = np.array([50.0, 75.0])

        result = negative_control_plot(p1, p2, n_shuffles=5, random_state=42)

        for shuffled in result["shuffled"]:
            assert "x" in shuffled
            assert "y" in shuffled
            assert len(shuffled["x"]) == 2
            assert len(shuffled["y"]) == 2

    def test_negative_control_reproducibility(self):
        """Verify reproducibility with random_state."""
        p1 = np.array([100.0, 100.0, 100.0])
        p2 = np.array([50.0, 75.0, 90.0])

        result1 = negative_control_plot(p1, p2, n_shuffles=10, random_state=42)
        result2 = negative_control_plot(p1, p2, n_shuffles=10, random_state=42)

        # Real data should be identical
        np.testing.assert_array_equal(result1["real"]["x"], result2["real"]["x"])

        # Shuffled data should also be identical with same seed
        for s1, s2 in zip(result1["shuffled"], result2["shuffled"]):
            np.testing.assert_array_equal(s1["x"], s2["x"])

    def test_negative_control_mismatched_shapes_raises_error(self):
        """Verify error when p1 and p2 have different shapes."""
        p1 = np.array([100.0, 100.0])
        p2 = np.array([50.0])

        with pytest.raises(ValueError, match="same shape"):
            negative_control_plot(p1, p2)

    def test_negative_control_invalid_p1_raises_error(self):
        """Verify error when p1 contains non-positive values."""
        p1 = np.array([0.0, 100.0])
        p2 = np.array([50.0, 50.0])

        with pytest.raises(ValueError, match="p1 must be positive"):
            negative_control_plot(p1, p2)

    def test_negative_control_invalid_p2_raises_error(self):
        """Verify error when p2 contains negative values."""
        p1 = np.array([100.0, 100.0])
        p2 = np.array([-10.0, 50.0])

        with pytest.raises(ValueError, match="p2_real must be non-negative"):
            negative_control_plot(p1, p2)


class TestSensitivityCheck:
    """Tests for the sensitivity_check function."""

    def test_basic_sensitivity_check(self):
        """Test basic sensitivity check with scalar inputs."""
        result = sensitivity_check(p1=100.0, p2=85.0)

        assert "baseline" in result
        assert "p1_sensitivity" in result
        assert "p2_sensitivity" in result

    def test_sensitivity_check_baseline(self):
        """Verify baseline values are correct."""
        result = sensitivity_check(p1=100.0, p2=50.0)

        assert result["baseline"]["x"] == pytest.approx(0.5)
        assert result["baseline"]["y"] == pytest.approx(np.sqrt(2))

    def test_sensitivity_check_default_perturbations(self):
        """Verify default perturbation fractions are used."""
        result = sensitivity_check(p1=100.0, p2=85.0)

        # Default is [0.01, 0.05, 0.10]
        assert len(result["p1_sensitivity"]) == 3
        assert len(result["p2_sensitivity"]) == 3

        fractions = [entry["perturbation"] for entry in result["p1_sensitivity"]]
        assert fractions == [0.01, 0.05, 0.10]

    def test_sensitivity_check_custom_perturbations(self):
        """Verify custom perturbation fractions work."""
        result = sensitivity_check(
            p1=100.0, p2=85.0, perturbation_fractions=[0.02, 0.04]
        )

        assert len(result["p1_sensitivity"]) == 2
        assert len(result["p2_sensitivity"]) == 2

    def test_sensitivity_p1_increase_decreases_y(self):
        """Verify increasing p1 decreases y."""
        result = sensitivity_check(p1=100.0, p2=85.0)

        for entry in result["p1_sensitivity"]:
            # Increasing p1 should decrease y (negative change)
            assert entry["y_change_pct"] < 0

    def test_sensitivity_p2_increase_increases_y(self):
        """Verify increasing p2 increases y."""
        result = sensitivity_check(p1=100.0, p2=85.0)

        for entry in result["p2_sensitivity"]:
            # Increasing p2 should increase y (positive change)
            assert entry["y_change_pct"] > 0

    def test_sensitivity_check_with_arrays(self):
        """Test sensitivity check with array inputs."""
        p1 = np.array([100.0, 100.0])
        p2 = np.array([50.0, 75.0])

        result = sensitivity_check(p1=p1, p2=p2)

        assert isinstance(result["baseline"]["x"], np.ndarray)
        assert isinstance(result["baseline"]["y"], np.ndarray)

    def test_sensitivity_check_invalid_p1_raises_error(self):
        """Verify error when p1 <= 0."""
        with pytest.raises(ValueError, match="p1 must be positive"):
            sensitivity_check(p1=0.0, p2=50.0)

    def test_sensitivity_check_invalid_p2_raises_error(self):
        """Verify error when p2 < 0."""
        with pytest.raises(ValueError, match="p2 must be non-negative"):
            sensitivity_check(p1=100.0, p2=-10.0)


class TestBootstrapCI:
    """Tests for the bootstrap_ci function."""

    def test_basic_bootstrap_ci(self):
        """Test basic bootstrap CI with scalar inputs."""
        result = bootstrap_ci(
            p1=100.0, p2=85.0, p1_std=5.0, p2_std=3.0, n_boot=1000, random_state=42
        )

        assert "x_mean" in result
        assert "x_ci" in result
        assert "y_mean" in result
        assert "y_ci" in result
        assert result["n_boot"] == 1000

    def test_bootstrap_ci_output_structure(self):
        """Verify CI output has proper structure."""
        result = bootstrap_ci(
            p1=100.0, p2=85.0, p1_std=5.0, p2_std=3.0, random_state=42
        )

        # CI should be tuple of (lower, upper)
        assert len(result["x_ci"]) == 2
        assert result["x_ci"][0] < result["x_ci"][1]
        assert len(result["y_ci"]) == 2
        assert result["y_ci"][0] < result["y_ci"][1]

    def test_bootstrap_ci_x_mean_within_ci(self):
        """Verify x mean is within confidence interval."""
        # Use moderate x value where distribution is less skewed
        result = bootstrap_ci(
            p1=100.0, p2=50.0, p1_std=5.0, p2_std=3.0, random_state=42
        )

        # For x, the distribution is approximately symmetric
        assert result["x_ci"][0] <= result["x_mean"] <= result["x_ci"][1]

    def test_bootstrap_ci_y_values_positive(self):
        """Verify y values are positive and CI is ordered."""
        result = bootstrap_ci(
            p1=100.0, p2=85.0, p1_std=5.0, p2_std=3.0, random_state=42
        )

        # y should always be positive
        assert result["y_mean"] > 0
        assert result["y_ci"][0] > 0
        assert result["y_ci"][1] > 0
        # CI should be ordered (lower < upper)
        assert result["y_ci"][0] < result["y_ci"][1]

    def test_bootstrap_ci_reproducibility(self):
        """Verify reproducibility with random_state."""
        result1 = bootstrap_ci(
            p1=100.0, p2=85.0, p1_std=5.0, p2_std=3.0, random_state=42
        )
        result2 = bootstrap_ci(
            p1=100.0, p2=85.0, p1_std=5.0, p2_std=3.0, random_state=42
        )

        assert result1["x_mean"] == result2["x_mean"]
        assert result1["y_mean"] == result2["y_mean"]

    def test_bootstrap_ci_missing_std_raises_error(self):
        """Verify error when scalar inputs lack standard deviations."""
        with pytest.raises(ValueError, match="p1_std and p2_std must be provided"):
            bootstrap_ci(p1=100.0, p2=85.0)

    def test_bootstrap_ci_with_arrays(self):
        """Test bootstrap CI with array inputs."""
        p1 = np.array([100.0, 100.0, 100.0, 100.0, 100.0])
        p2 = np.array([50.0, 60.0, 70.0, 80.0, 90.0])

        result = bootstrap_ci(p1=p1, p2=p2, n_boot=500, random_state=42)

        assert "x_mean" in result
        assert "y_mean" in result


class TestDeltaMethodCI:
    """Tests for the delta_method_ci function."""

    def test_basic_delta_method_ci(self):
        """Test basic delta method CI."""
        result = delta_method_ci(p1=100.0, p2=85.0, p1_std=5.0, p2_std=3.0)

        assert "x" in result
        assert "x_std" in result
        assert "x_ci" in result
        assert "y" in result
        assert "y_std" in result
        assert "y_ci" in result

    def test_delta_method_point_estimates(self):
        """Verify point estimates are correct."""
        result = delta_method_ci(p1=100.0, p2=50.0, p1_std=5.0, p2_std=3.0)

        assert result["x"] == pytest.approx(0.5)
        assert result["y"] == pytest.approx(np.sqrt(2))

    def test_delta_method_ci_structure(self):
        """Verify CI output has proper structure."""
        result = delta_method_ci(p1=100.0, p2=85.0, p1_std=5.0, p2_std=3.0)

        assert len(result["x_ci"]) == 2
        assert result["x_ci"][0] < result["x_ci"][1]
        assert len(result["y_ci"]) == 2
        assert result["y_ci"][0] < result["y_ci"][1]

    def test_delta_method_std_positive(self):
        """Verify standard errors are non-negative."""
        result = delta_method_ci(p1=100.0, p2=85.0, p1_std=5.0, p2_std=3.0)

        assert result["x_std"] >= 0
        assert result["y_std"] >= 0

    def test_delta_method_invalid_p1_raises_error(self):
        """Verify error when p1 <= 0."""
        with pytest.raises(ValueError, match="p1 must be positive"):
            delta_method_ci(p1=0.0, p2=50.0, p1_std=5.0, p2_std=3.0)

    def test_delta_method_invalid_p2_raises_error(self):
        """Verify error when p2 < 0."""
        with pytest.raises(ValueError, match="p2 must be non-negative"):
            delta_method_ci(p1=100.0, p2=-10.0, p1_std=5.0, p2_std=3.0)

    def test_delta_method_invalid_std_raises_error(self):
        """Verify error when standard deviations are negative."""
        with pytest.raises(ValueError, match="non-negative"):
            delta_method_ci(p1=100.0, p2=50.0, p1_std=-5.0, p2_std=3.0)

    def test_delta_method_with_covariance(self):
        """Test delta method with non-zero covariance."""
        result = delta_method_ci(
            p1=100.0, p2=85.0, p1_std=5.0, p2_std=3.0, cov_p1_p2=2.0
        )

        # Should still produce valid output
        assert result["x_std"] >= 0
        assert result["y_std"] >= 0
