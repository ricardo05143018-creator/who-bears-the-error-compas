# Data

The repository does not redistribute raw or processed row-level defendant data.

Run `python src/fetch_data.py` to download ProPublica's public
`compas-scores-two-years.csv` from the pinned commit. The script verifies the
frozen SHA-256 checksum before storing the file locally. `prepare_data.py` then
checks the frozen dimensions and schema in memory. Any runtime-generated
row-level file is excluded by `.gitignore`.

Public outputs under `output/tables/` contain only aggregated result tables and
figure-source tables.