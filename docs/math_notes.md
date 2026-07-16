# Math notes

## Definitions

- **Representation of N**: an integer pair (a, b) with a ≤ b and a³ + b³ = N.
  The a ≤ b canonicalization deduplicates (a, b) ↔ (b, a).
- **Taxicab number Ta(k)**: the smallest positive N expressible as a sum of two
  *positive* cubes in k distinct ways.
- **Cabtaxi number Cab(k)**: the smallest positive N expressible as a sum of
  two integer cubes (any sign) in k distinct ways.

## Sign regimes

- **positive**: a, b ≥ 1.
- **mixed**: a, b ∈ ℤ.

## Trivial family in mixed regime

The identity (k+1)³ + (−k)³ = 3k² + 3k + 1 gives every integer of the form
3k² + 3k + 1 a "free" representation in the mixed regime. When counting
non-trivial multi-representation numbers, this family is usually excluded.

## References

- OEIS A001235 — Taxicab numbers.
- OEIS A011541 — Ta(n) sequence.
- OEIS A047696 — Cabtaxi numbers.