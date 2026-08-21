# Who Bears the Error?

This repository accompanies *Who Bears the Error? Threshold Choice, Fairness
Trade-offs, and Institutional Accountability in COMPAS*. It reproduces the
published ProPublica contingency counts, evaluates every common decile
threshold, estimates pointwise bootstrap uncertainty, and implements the
prespecified error-cost and population-robustness analyses.

## Reproduce the analysis

Create a Python environment, install `requirements.txt`, and run from the
repository root:

```bash
python src/fetch_data.py
pytest -q
python src/diagnostics.py
python src/threshold_sweep.py
python src/bootstrap_and_cost.py
python src/make_figures.py
```

`bootstrap_and_cost.py` runs 5,000 bootstrap replicates and may take several
minutes. It uses NumPy `PCG64` with seed `20260807`.

The acquisition script downloads the data from ProPublica commit
`bafff5da3f2e45eca6c2d5055faad269defd135a` and requires SHA-256 digest
`c451db85908b2f7fef1d83203bedf6b71ecda0d5af468d82ae62178f91d0cc7d`.
The raw file and any processed row-level file are ignored. Canonical public
outputs are the six aggregated CSV files in `output/tables/`, five main figures,
and two supplemental figures in `output/figures/`.

## Repository map

- `documentation/`: frozen protocol, amendments record, citation audit, and finalization report
- `src/`: acquisition, validation, metrics, diagnostics, threshold, bootstrap/cost, and figure scripts
- `tests/`: data-integrity, threshold-mapping, replication, and endpoint tests
- `output/tables/`: canonical aggregated machine-readable results
- `output/figures/`: frozen main and supplemental figures
- `paper/`: integrated manuscript source, bibliography, and final PDF

The loss parameter `lambda` is a prespecified sensitivity device, not a measure
of realized social harm. The paper does not claim that any displayed threshold
is legally or morally correct.
