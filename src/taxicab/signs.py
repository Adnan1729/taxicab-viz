"""Sign regime definitions for sums-of-two-cubes representations."""

from __future__ import annotations

from enum import StrEnum


class SignRegime(StrEnum):
    """Which (a, b) pairs count as valid representations.

    - POSITIVE: a >= 1 and b >= 1.
    - MIXED:    a, b in Z (any signs).

    Inherits from str so that regime.value serializes cleanly to parquet
    and is human-readable in dataframes.
    """

    POSITIVE = "positive"
    MIXED = "mixed"


def is_trivial_mixed(a: int, b: int) -> bool:
    """Detect the trivial family (k+1)^3 + (-k)^3 = 3k^2 + 3k + 1.

    Under canonicalization a <= b, this family has the form a = -k, b = k+1
    for some k >= 0, i.e. b == 1 - a with a <= 0 < b.

    Only meaningful in the MIXED regime; in POSITIVE the family doesn't appear.
    """
    return b == 1 - a and a <= 0 < b
