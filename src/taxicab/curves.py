"""Sample the continuous curve x^3 + y^3 = N for plotting overlays."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def sample_curve_positive(n: int, n_points: int = 400) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Sample x^3 + y^3 = N in the first quadrant (x, y >= 0).

    Returns (xs, ys) arrays of length n_points. The curve is a compact arc from
    (0, N^(1/3)) to (N^(1/3), 0), symmetric across y = x.

    Parametrized by x in [0, N^(1/3)] for numerical stability — y is then
    the real cube root of N - x^3.
    """
    if n <= 0:
        raise ValueError(f"n must be positive for positive-regime curve, got {n}")
    cbrt_n = n ** (1 / 3)
    xs = np.linspace(0.0, cbrt_n, n_points)
    # y = (N - x^3)^(1/3), guaranteed non-negative for x in [0, N^(1/3)].
    ys = np.cbrt(n - xs**3)
    return xs, ys


def sample_curve_full(n: int, x_range: tuple[float, float], n_points: int = 800) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Sample x^3 + y^3 = N over all of R, given an explicit x_range.

    For the mixed regime: the curve extends unboundedly with asymptote y = -x.
    Caller must supply x_range to bound the plot window.
    """
    x_min, x_max = x_range
    if x_min >= x_max:
        raise ValueError(f"x_range must have x_min < x_max, got {x_range}")
    xs = np.linspace(x_min, x_max, n_points)
    ys = np.cbrt(n - xs**3)  # np.cbrt handles negatives correctly
    return xs, ys
