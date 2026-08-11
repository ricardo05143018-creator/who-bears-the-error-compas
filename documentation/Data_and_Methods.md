# COMPAS Data and Methods FINAL v1.0

**Project:** *Who Bears the Error? Threshold Choice, Fairness Trade-offs, and Institutional Accountability in COMPAS*  
**Finalized:** 2026-08-11  
**Status:** Final Data and Methods section, derived from COMPAS Research Protocol v1.0 and the completed frozen implementation

## 3. Data and Methods

### 3.1 Data source and provenance

The analysis used ProPublica's public `compas-scores-two-years.csv` file from the `propublica/compas-analysis` repository. The source was fixed at commit `bafff5da3f2e45eca6c2d5055faad269defd135a`; the downloaded file had SHA-256 digest `c451db85908b2f7fef1d83203bedf6b71ecda0d5af468d82ae62178f91d0cc7d` and dimensions 7,214 rows by 53 columns. The data concern defendants scored in Broward County, Florida, principally during 2013-2014. The pipeline downloaded the commit-pinned file and halted before analysis if its checksum or dimensions differed from these frozen values.

Additional integrity checks required the outcome to be binary, the general recidivism score to lie from 1 through 10, the defendant identifier to be unique and complete, and the analysis variables to contain no missing values. The raw CSV contains two columns headed `decile_score`; after import, the second is named `decile_score.1`. The preparation step required these columns to agree in all rows before retaining one as the canonical general recidivism score. The violent-risk variable `v_decile_score` was not used. Any failed check halted the pipeline rather than triggering silent row deletion or imputation.

The source file contains direct identifiers and detailed case fields that were unnecessary for the analysis. Neither the raw file nor any row-level processed table was retained in the public repository. If generated at runtime, the minimized table contained only a nonidentifying row key, recorded race, general recidivism decile score and category, and the two-year outcome, and was excluded through `.gitignore`. Public machine-readable outputs were limited to aggregated figure-source and result tables. The pinned download, checksum, and preparation code therefore provide reproducibility without republishing a second person-level dataset.

### 3.2 Analysis populations and variables

The known-result replication used sample R, all 7,214 rows in the source file: 3,696 recorded as `African-American`, 2,454 as `Caucasian`, 637 as Hispanic, 377 as Other, 32 as Asian, and 18 as Native American. It did not apply the separate 30-day case-matching filters used in some other parts of ProPublica's analysis because the published two-year error tables were calculated from the full file. The primary comparative sample C contained the 6,150 defendants recorded as `African-American` or `Caucasian`. These categories are displayed as Black and White for readability, but they are administrative labels in the source data rather than measures of self-identified racial identity. The smaller recorded groups were included in the replication audit and pooled estimates but excluded from the prespecified two-group comparisons.

For defendant \(i\), \(Y_i=1\) denoted `two_year_recid = 1`, and \(Y_i=0\) otherwise. This variable measures observed rearrest within two years, not true offending. The general recidivism decile score was denoted \(S_i\in\{1,\ldots,10\}\), and the focal recorded group was \(G_i\in\{B,W\}\). No values of the score, outcome, or race variables were imputed.

### 3.3 Threshold rules and performance measures

For each common threshold \(t\), the analytical binary rule was

\[
\widehat{Y}_{i,t}=\mathbf{1}(S_i\ge t),
\qquad t\in\{1,2,\ldots,11\}.
\]

Thus, \(t=1\) classified every defendant as higher risk, whereas \(t=11\) classified none. The \(t=5\) rule reproduced COMPAS `Low` versus `Medium/High`, and \(t=8\) reproduced `Low/Medium` versus `High`. Every primary comparison applied the same threshold to all groups. The endpoint rules were retained to display the full available decision space; a metric with an empty denominator was stored as undefined rather than set to zero.

At each threshold, true-negative, false-positive, false-negative, and true-positive counts were computed before the corresponding rates. The primary metrics were

\[
FPR=\frac{FP}{FP+TN},\qquad
FNR=\frac{FN}{FN+TP},\qquad
PPV=\frac{TP}{TP+FP}.
\]

The primary group contrasts were signed Black-minus-White differences in these rates. Differences rather than ratios were used as the primary contrasts because ratios become unstable when the White reference rate approaches zero; Black/White FPR and FNR ratios were retained only for the two prespecified reference cutoffs, \(t=5\) and \(t=8\). The threshold sweep also calculated TPR, TNR, NPV, selection rate, accuracy, balanced accuracy, and overall error rate, with the underlying numerators and denominators retained in the canonical outputs.

Threshold-independent ranking discrimination was summarized by the empirical ROC AUC for sample R, Black defendants, White defendants, and the signed Black-minus-White difference. AUC was interpreted as a ranking measure, not as evidence that classification errors at a selected cutoff were similar. As a descriptive score-level calibration diagnostic, the analysis also estimated

\[
q_{g,s}=P(Y=1\mid S=s,G=g)
\]

for each score \(s=1,\ldots,10\), together with \(q_{B,s}-q_{W,s}\). Because the COMPAS decile is not a literal predicted probability, no Brier score or probability-calibration slope was calculated from \(S/10\).

### 3.4 Bootstrap uncertainty

Uncertainty was evaluated with 5,000 nonparametric defendant-level bootstrap replicates generated by NumPy's `PCG64` generator with seed `20260807`. For sample C comparisons, defendants were resampled with replacement within the Black and White groups separately, preserving both observed group sizes. For pooled sample-R estimates, resampling occurred within all six recorded race categories, preserving the observed race composition. Each replicate recomputed the threshold-dependent metrics and signed gaps, pooled and group-specific AUC values, score-level rearrest rates, and the focal error-cost optima.

Intervals were the 2.5th and 97.5th percentiles of the bootstrap distribution. Threshold and score curves use pointwise, not simultaneous, 95% intervals and were not interpreted as a sequence of significance tests. A replicate-specific undefined value was stored as missing, and an interval was suppressed if fewer than 95% of replicates produced a defined estimate.

### 3.5 Error-cost sensitivity

The primary sensitivity analysis evaluated the per-defendant aggregate loss in sample C,

\[
L_t(\lambda)=\frac{\lambda FP_t+(1-\lambda)FN_t}{N},
\qquad \lambda\in[0,1],
\]

where \(\lambda\) is the prespecified weight on a false positive and \(1-\lambda\) is the weight on a false negative. Loss was calculated for all thresholds and for \(\lambda=0,0.01,\ldots,1\). For each value of \(\lambda\), the estimand was the complete minimizing set

\[
T^*(\lambda)=\underset{t\in\{1,\ldots,11\}}{\arg\min}\;L_t(\lambda).
\]

All tied minimizers were retained. When a display required one line, the highest minimizing threshold was shown as an explicit convention favoring fewer higher-risk classifications, not as an additional optimization criterion. The focal values \(\lambda=0.25,0.50,0.75\) represent false-positive to false-negative weight ratios of 1:3, 1:1, and 3:1.

To examine the distribution associated with an aggregate optimum, group-specific weighted error loss was defined as

\[
L_{g,t}(\lambda)
=\lambda\frac{FP_{g,t}}{N_g}+(1-\lambda)\frac{FN_{g,t}}{N_g}.
\]

This quantity was evaluated at \(t=5\), \(t=8\), and the focal minimizing thresholds. It is a modeled sensitivity quantity rather than a measurement of realized social harm. In the bootstrap, the analysis recorded how often each threshold belonged to the full minimizing set at each focal \(\lambda\). Because a replicate could contain tied minimizers, membership frequencies across thresholds need not sum to 100%.

As a prespecified robustness check, the optimization was repeated using the class-conditional loss

\[
\widetilde{L}_t(\lambda)=\lambda FPR_t+(1-\lambda)FNR_t.
\]

Unlike the per-defendant primary loss, this expression gives equal structural weight to the non-rearrested and rearrested conditional pools before applying \(\lambda\). Comparing the two specifications makes visible the dependence of an optimum on both the chosen error weights and population base rates. Neither loss function estimates which weighting is legally, morally, or institutionally appropriate.

### 3.6 Prespecification and reproducibility

The analysis plan was frozen before implementation of the threshold, bootstrap, and cost extensions. Because the dataset was public and ProPublica's headline error rates were already known, the \(t=5\) analysis was designated a known-result replication rather than a blind preregistration. Extension results were generated only after the acquisition and integrity checks passed and the expected \(t=5\) contingency counts were reproduced exactly. Category mapping, the \(t=8\) cutoff, sample-R aggregate loss, endpoint behavior, the class-conditional loss, and clean-run reproducibility were the prespecified robustness checks.

The population robustness check repeated the aggregate per-defendant loss calculation across the full Sample R population and compared its minimizing set with the primary Sample C result at every value on the prespecified \(\lambda\) grid.

The code separated acquisition, preparation, metric calculation, resampling, cost analysis, and output generation; exposed the random seed; and generated public tables and figure-source data without manual transcription. The full pipeline was required to reproduce identical aggregate outputs from a clean run. These design choices distinguish the frozen confirmatory extension from any later exploratory analysis and preserve a complete audit trail for the results reported below.
