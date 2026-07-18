# taxicab-viz

Enumeration, classification, and visualisation of representations of integers as
sums of two cubes, across the positive and mixed sign regimes. This repository
accompanies the blog post *[Taxicab Numbers, Sixty Years On](https://amahmud.neocities.org/blog/taxicab)*.

## What's here

- Parallelised sweeps that enumerate every representation of every N up to a
  chosen bound, in either sign regime, in seconds
- Classification of mixed-regime representations into the trivial family
  (a, 1-a) and everything else (sporadic)
- Cubic residue analysis mod 7 and mod 9
- Three publication-quality figures that make Hooley's 1963 asymptotic and the
  classical modular obstructions visible
- All results reproducible from a fresh clone with a single environment file

## Results at a glance

Sweeping N ≤ 10⁹ in the positive regime finds 441,521 representations across
438,413 distinct N. Of those:

| Representations | Count of N |
|---|---|
| 1 | 438,405 |
| 2 | 1,546 |
| 3 | 8 |

The first taxicab-2 is 1729 = 1³ + 12³ = 9³ + 10³ (the Hardy–Ramanujan number).
The first taxicab-3 is Ta(3) = 87,539,319.

Sweeping the mixed regime with |a|, |b| ≤ 2000 finds 8,006,001 representations
including 119 taxicab-4 and 14 taxicab-5 numbers for N > 0. Cabtaxi(2) = 91 is
the smallest N whose sporadic representation (3³ + 4³) coincides with a trivial
representation (6³ + (-5)³).

Full results and figures match OEIS A001235, A011541, and A018787 across the
range tested.

## Quick start

```bash
conda env create -f environment.yml
conda activate taxicab-viz
pip install -e ".[dev]"
pytest
```

Reproduce the artefacts:

```bash
# Compute (takes ~2 seconds each on 4 cores)
python scripts/compute_taxicab.py --regime positive --n-max 1000000000
python scripts/compute_taxicab.py --regime mixed --b-max 2000

# Render figures
python scripts/render_generic_vs_taxicab.py
python scripts/render_distribution.py
python scripts/render_residues.py

# Optional: dark-mode variants for dark-background blog embeds
python scripts/invert_figures.py
```

Figures land in `figures/` (light) and `figures_dark/` (dark). Parquet artefacts
land in `data/processed/`.

## Layout

```
src/taxicab/           library code
├── core.py            single-N representation finder with exact integer arithmetic
├── search.py          parallel sweep with sign-regime dispatch
├── signs.py           sign regime and family enums, classification
├── curves.py          smooth curve sampling for plot overlays
├── residues.py        cubic residue analysis
├── io.py              parquet persistence with JSON sidecar manifests
└── viz/               plotting modules
    ├── style.py       publication style (classical scientific aesthetic)
    ├── curves.py      curve-with-lattice-point plots
    ├── histograms.py  representation-count distribution and Hooley cumulative
    └── residues.py    residue frequency bar charts

scripts/               thin CLI entry points that produce artefacts
tests/                 pytest suite (~40 tests, ~90% coverage on the library)
data/processed/        computed parquet + JSON sidecar manifests (gitignored)
figures/               rendered SVGs (gitignored)
figures_dark/          dark-mode inverted SVGs (gitignored)
docs/                  research notes and references
```

## Design notes

**Enumeration, not per-N query.** The sweep enumerates pairs (a, b) and groups
by a³ + b³, which is O(N^{2/3}) total rather than O(N · N^{1/3}) if we asked
each N in turn. This is what makes the 10⁹ sweep tractable in seconds.

**Sign regimes as first-class parameters.** The positive regime bounds the
*output* (N ≤ n_max); the mixed regime bounds the *input* (|a|, |b| ≤ b_max),
because bounding the output does not bound the search space. The two regimes
have separate enumeration paths rather than a shared function with regime
conditionals.

**Family classification vectorised.** The trivial family (a, 1-a) is identified
in a single boolean expression on the DataFrame, not row-by-row. Necessary at
the 8M-row scale.

**Reproducibility via manifests.** Every parquet artefact has a JSON sidecar
recording the parameters that produced it. Reading a file six months later
without the manifest is a source of confusion; with it, the artefact documents
itself.

## Development

Standard workflow:

```bash
pytest -v
ruff check .
ruff format .
mypy
```

All three should pass cleanly before commits. See `pyproject.toml` for the tool
configurations.

## What this repository does not do

- **Elliptic curve rank computation.** The natural next step would be to
  compute the Mordell–Weil rank of the elliptic curve associated to each
  multi-representation N. This requires SageMath or PARI/GP, neither of which
  installs cleanly on Windows without administrator rights. See the blog post's
  closing sections for the honest account.

- **New mathematics.** Everything computed here is either classical (Hooley's
  theorem, cubic residue obstruction) or catalogued (OEIS entries). The
  contribution is pedagogical, not research.

## References

Primary references cited in the blog post:

- C. Hooley, *On the representations of a number as the sum of two cubes*,
  Math. Z. 82 (1963), 259–266.
- J. H. Silverman, *Taxicabs and sums of two cubes*, Amer. Math. Monthly
  100(4) (1993), 331–340.
- A. R. Booker and A. V. Sutherland, *On a question of Mordell*, PNAS 118(11)
  (2021), e2022377118.
- OEIS sequences A001235 (taxicab-2 numbers), A011541 (Ta(n)), A018787
  (numbers ≥3 representations).

## License

MIT. See `LICENSE` for details.
