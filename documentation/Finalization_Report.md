# COMPAS Working Paper v1.0 Release Audit

**Date:** 2026-08-21  
**Paper:** *Who Bears the Error? Threshold Choice, Fairness Trade-offs, and Institutional Accountability in COMPAS*

Core empirical analyses were substantially completed on August 7–8, 2026. The subsequent release period focused on manuscript integration, citation verification, reproducibility checks, repository cleanup, and final audit.

## Outcome

The empirical phase remains closed. The missing Sample R population robustness output is present, the Methods section matches the implemented pipeline, the Related Work section has been audited against primary or authoritative sources, and the manuscript has been integrated with the frozen tables and figures. No frozen headline result changed.

## Verification record

- The pinned ProPublica file downloaded successfully from commit `bafff5da3f2e45eca6c2d5055faad269defd135a`; SHA-256 verification passed.
- All five repository tests passed in a clean isolated environment.
- Deterministic diagnostics reproduced AUC values 0.7022, 0.6918, 0.6931, and the -0.0013 Black-minus-White gap.
- Canonical output dimensions passed: 55 threshold rows, 10 calibration rows, 364 bootstrap interval rows, 1,111 cost-grid rows, 101 population-robustness rows, and 33 bootstrap optimal-membership rows.
- The t=5 and t=8 FPR/FNR/PPV estimates and all Table 2 confidence intervals passed an automated check against the canonical CSVs.
- FPR-gap intervals were above zero and FNR-gap intervals below zero for every interior threshold t=2,...,10.
- Focal primary and Sample R optima were both 2, 6, and 10 at lambda=.25, .50, and .75. Sample R and Sample C minimizing sets differed at exactly five grid weights: .31, .38, .56, .69, and .70.
- The manuscript compiled without undefined citations, undefined references, overfull boxes, or clipping warnings.
- The 15-page PDF, including two supplemental figures, was rendered to page images and visually inspected. Tables, formulas, captions, references, and figures were within page bounds and legible.

## Changelog

### Substantive completion

- Completed the protocol-required Sample R aggregate-cost robustness output and incorporated the result into Methods and Results.
- Added Section 2 Background and Related Work with a narrowly defined gap: prior work identifies competing metrics, incompatibilities, threshold sensitivity, and legal cautions, while this paper contributes the full common-threshold sweep, uncertainty, and transparent error-cost sensitivity.
- Added a final abstract that reports the design and main results without expanding the paper's claim beyond historical COMPAS threshold choice.

### Citation changes

- Rechecked ProPublica's investigation and technical methods separately.
- Narrowed the Flores et al. characterization to similar AUC and approximately similar rearrest rates within broad risk categories.
- Distinguished Chouldechova's threshold-specific predictive-parity result from Kleinberg et al.'s score-level calibration and balance conditions.
- Framed the empirical findings as consistent with and illustrative of the incompatibility literature, not as a new proof.
- Replaced broad references to *State v. Loomis* with the official Wisconsin Supreme Court opinion and stated its limitations, warnings, independent-reasons requirement, and jurisdiction-specific scope.

### Wording changes

- Standardized the primary contrasts as signed Black-minus-White differences rather than "absolute differences."
- Standardized the variable and table language as "group-specific weighted error loss" while reserving "modeled error burdens" for interpretive prose.
- Preserved the distinction between an optimum conditional on a chosen objective and an objectively correct threshold.
- Removed wording that could imply variance decomposition, economic efficiency, realized social harm, causal race effects, current-system performance, or legal compliance.
- Clarified in `AMENDMENTS.md` that the frozen protocol's phrase "signed absolute differences" was a label error; the formulas and implementation have always used signed differences.

### Code and repository changes

- Replaced the development-style script name and dated build marker with canonical `src/bootstrap_and_cost.py` and neutral runtime labeling.
- Confirmed that no substantive result such as 2/6/10 is hard-coded as a pipeline pass/fail criterion.
- Confirmed that no superseded-output cleanup logic remains in the canonical analysis script.
- Kept only six canonical aggregated CSV result tables; raw and processed row-level data are excluded by `.gitignore`.
- Added a reproducible README, requirements file, four test modules containing five tests, data-minimization notice, amendments record, citation audit, manuscript source, and bibliography.
- Retained five concise, task-specific comments in `make_figures.py`; no section-by-section explanatory commentary was added to the code.

### Format and integration changes

- Adopted the final title throughout the integrated manuscript and repository front matter.
- Inserted the three frozen tables, five frozen main figures, and two supplemental figures with final captions.
- Added cross-references and a seven-item audited bibliography.
- Removed draft-status and section-boundary notes from the paper body.

## Adversarial review summary

### Quantitative reviewer

No mismatch was found between the manuscript, tables, figures, and canonical outputs. Endpoints remain explicitly degenerate, confidence intervals are labeled pointwise, tied minimizers are preserved, the displayed-threshold convention is disclosed, and the loss parameter is not presented as estimated welfare.

### Reproducibility reviewer

The data URL is commit-pinned, checksum and dimensions are frozen, deterministic scripts and tests execute from the documented repository layout, random generation is specified, the bootstrap outputs are public, and no row-level public data are required. The cosmetic build-label change did not justify rerunning 5,000 replicates.

### Citation and legal-scope reviewer

Every surviving literature or legal claim has a primary or authoritative source. The manuscript does not describe *Loomis* as a general approval of COMPAS, does not turn a Wisconsin sentencing holding into a national legal rule, and does not present the accountability framework as proof of compliance.

### Privacy reviewer

The repository does not contain the downloaded raw CSV, a processed individual-level table, direct identifiers, or a second copy of race/score/outcome rows. Only aggregated result tables and rendered figures are public.

### Style reviewer

The integrated prose follows one argument from score to threshold to errors to objective to consequence to institutional responsibility. Repetitive meta-commentary, draft labels, exaggerated transitions, and generic AI-governance digressions were excluded. Code comments are limited to cases where tie handling, input provenance, or rendering behavior would otherwise be unclear.

## Remaining risks

The paper retains the inherent limitations stated in Section 6: observed rearrest is not true offending; the data are historical and local; race categories are administrative labels; the threshold sweep is analytical rather than a deployment reconstruction; lambda is not measured welfare; and bootstrap uncertainty is not total uncertainty. These are disclosed scope limits, not unresolved defects.

**NO MATERIAL OPEN ITEMS.**

## Final freeze verdict

| Component | Verdict | Note |
|---|---|---|
| Protocol v1.0 | FINAL / FROZEN | Preserved; one non-substantive terminology clarification recorded in `AMENDMENTS.md`. |
| Code and pipeline | FINAL / FROZEN | Canonical names, no hard-coded empirical answer, no obsolete cleanup logic. |
| Tables 1-3 | FINAL / FROZEN | Numbers and rendered layout verified. |
| Figures 1-5 | FINAL / FROZEN | Regenerated successfully and visually verified. |
| Supplemental figures | FINAL / FROZEN | Bootstrap membership and loss-normalization robustness included. |
| Introduction | FINAL / FROZEN | Only citation integration and final title applied. |
| Background / Related Work | FINAL / FROZEN | Primary-source audit completed. |
| Data and Methods | FINAL / FROZEN | Sample R robustness implementation and terminology aligned. |
| Results | FINAL / FROZEN | Canonical values and population-robustness result verified. |
| Discussion | FINAL / FROZEN | Normative claims remain bounded by the empirical record. |
| Limitations | FINAL / FROZEN | Six prespecified limitations retained. |
| Conclusion | FINAL / FROZEN | No expansion beyond the institutional-choice thesis. |
| Abstract | FINAL / FROZEN | Written last and checked against the final manuscript. |
| Bibliography | FINAL / FROZEN | Seven cited sources, all audited. |
| Repository | FINAL / FROZEN | README path tested; privacy and output inventory checked. |
| Entire paper | FINAL / FROZEN | Ready for submission-stage copyediting or venue formatting only. |
