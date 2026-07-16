# taxicab-viz

Research and visualization of taxicab numbers — integers expressible as sums of
two cubes in multiple ways — across three sign regimes: positive, mixed, and
their interaction.

## Status

Early scaffolding. See `docs/math_notes.md` for definitions and conventions.

## Development

```bash
conda env create -f environment.yml
conda activate taxicab-viz
pip install -e ".[dev]"
pytest
```

## Layout

- `src/taxicab/` — library code
- `scripts/` — CLI entry points producing artifacts in `data/` and `figures/`
- `tests/` — pytest suite
- `docs/` — research notes and references