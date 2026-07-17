"""Sign regime definitions and family classification for sums-of-two-cubes."""

from __future__ import annotations

from enum import Enum


class SignRegime(str, Enum):
    """Which (a, b) pairs count as valid representations.

    - POSITIVE: a >= 1 and b >= 1.
    - MIXED:    a, b in Z (any signs).

    Inherits from str so the value serializes cleanly to parquet.
    """

    POSITIVE = "positive"
    MIXED = "mixed"


class Family(str, Enum):
    """Classification of a canonicalized (a, b) representation by parametric family.

    - TRIVIAL:  b = 1 - a with a <= 0, giving N = 3a^2 - 3a + 1. This family
                covers every N of the form 3k^2 + 3k + 1. Mixed regime only.
    - SPORADIC: everything else.

    This binary classification is deliberately coarse. Other parametric families
    exist (see e.g. Pletser 2022 for consecutive-cube families) and can be
    identified in a downstream module without changing the sweep schema.
    """

    TRIVIAL = "trivial"
    SPORADIC = "sporadic"


def is_trivial_mixed(a: int, b: int) -> bool:
    """True iff (a, b) is in the trivial family b = 1 - a with a <= 0.

    Assumes a <= b canonicalization.
    """
    return b == 1 - a and a <= 0


def classify(a: int, b: int) -> Family:
    """Classify a canonicalized representation by parametric family."""
    if is_trivial_mixed(a, b):
        return Family.TRIVIAL
    return Family.SPORADIC
