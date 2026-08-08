# COMPAS Research Protocol v1.0

## Who Bears the Error? Threshold Choice and Accountability in Algorithmic Risk Assessment

**Author:** Zhixun Zheng  
**Version:** 1.0  
**Date frozen:** 2026-08-07  
**Status:** First-stage protocol, frozen before implementation of the extension analyses  
**Planned product:** Reproducible code repository and an 8-12 page mixed quantitative/policy working paper

---

## 1. Purpose of this protocol

This document fixes the first-stage analysis before new threshold and error-cost results are produced. Its purpose is to prevent the project from expanding or changing direction in response to whichever patterns look most interesting after the data are examined.

The project grows out of the expository essay *Who Bears the Error? Fairness and Authority in Algorithmic Risk Assessment*. That essay will remain unchanged as the Princeton graded written paper. The present project is a separate empirical extension.

This is not a blind preregistration of an unknown dataset. The data are public, and ProPublica's headline error rates are already known and discussed in the source essay. Accordingly:

- the ProPublica error-table analysis is a **known-result replication**;
- the threshold sweep, uncertainty analysis, and error-cost analysis are **prespecified extensions** under this protocol;
- any analysis added after those results are seen will be labeled **exploratory** and recorded in an amendment log.

The project is not designed to decide whether COMPAS is, in a single global sense, "fair," "unfair," "biased," or "racist." It studies a narrower question: how a common decision threshold allocates different kinds of classification error, and what an institution must disclose and justify when it turns a score into an adverse decision rule.

---

## 2. Research question and analytical claims

### 2.1 Primary research question

> **How does the choice of classification threshold redistribute false-positive and false-negative burdens across racial groups in COMPAS, and what does that imply for institutional accountability?**

### 2.2 Empirical subquestions

1. Can ProPublica's published false-positive rate (FPR), false-negative rate (FNR), and positive predictive value (PPV) results be reproduced exactly from its public two-year COMPAS file?
2. How do FPR, FNR, PPV, selection rate, accuracy, and related quantities change when the common COMPAS cutoff is moved across every possible decile threshold?
3. How do the Black-White gaps in those quantities change with the threshold, and how uncertain are the estimated gaps under defendant-level resampling?
4. How does the loss-minimizing threshold change when the relative cost assigned to false positives versus false negatives changes?
5. At a threshold selected to minimize aggregate loss, how are the resulting modeled error burdens distributed between the two focal groups?

### 2.3 Normative proposition to be illustrated, not statistically "proved"

The data can estimate what follows from a specified threshold and cost weighting. They cannot determine which false-positive/false-negative weighting is legally or morally legitimate. If different defensible weights produce different loss-minimizing thresholds and different modeled subgroup error burdens, the institution must own and justify that choice rather than presenting it as an automatic output of the model.

### 2.4 Claims this design does not support

The analysis will not claim to estimate:

- the causal effect of race on a COMPAS score;
- the causal effect of COMPAS on detention, sentence length, or rearrest;
- the fairness of every COMPAS scale or every use of COMPAS;
- the true rate of reoffending, as distinct from observed rearrest;
- the threshold actually used in every Broward County or other institutional decision;
- the social value of a false positive or false negative;
- the legality or constitutionality of a particular deployment.

---

## 3. Scope lock

### 3.1 Included in version 1.0

1. Exact replication of ProPublica's general two-year recidivism error tables.
2. A complete sweep of common thresholds over the COMPAS general recidivism decile score.
3. Descriptive discrimination and calibration diagnostics.
4. Black-White subgroup metrics and gaps.
5. Defendant-level bootstrap uncertainty intervals.
6. A transparent asymmetric false-positive/false-negative cost analysis.
7. An operational accountability framework derived from the empirical outputs.

### 3.2 Excluded from version 1.0

The following will not be added before the first working paper is complete:

- violent-recidivism and failure-to-appear scales;
- other jurisdictions, countries, or proprietary risk tools;
- generative AI, large language models, or "AI judge" literature;
- newly trained machine-learning models or fairness corrections;
- race-specific deployment thresholds;
- causal claims or adjusted race-effect regressions;
- intersectional subgroup analyses;
- temporal-drift estimation;
- qualitative interviews or case-level anecdotes;
- a broad comparative-law review;
- publication-target optimization.

These may be considered only as separately labeled later work. They are not prerequisites for completing this project.

---

## 4. Data source, version, and provenance

### 4.1 Primary file

The analysis will use ProPublica's `compas-scores-two-years.csv` from the public `propublica/compas-analysis` repository.

- Repository: <https://github.com/propublica/compas-analysis>
- Commit fixed for this protocol: `bafff5da3f2e45eca6c2d5055faad269defd135a`
- Commit-pinned file: <https://raw.githubusercontent.com/propublica/compas-analysis/bafff5da3f2e45eca6c2d5055faad269defd135a/compas-scores-two-years.csv>
- Expected SHA-256: `c451db85908b2f7fef1d83203bedf6b71ecda0d5af468d82ae62178f91d0cc7d`
- Expected dimensions: 7,214 rows and 53 raw columns.

The data cover defendants scored in Broward County, Florida, principally in 2013-2014. ProPublica constructed the file by linking COMPAS records with court, jail, and correctional records. Its methodology is described in [How We Analyzed the COMPAS Recidivism Algorithm](https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm).

### 4.2 Data minimization and privacy

The source file contains direct identifiers and detailed case information. The project will not republish names, birth dates, case numbers, offense descriptions, or row-level examples.

The preparation script will read the source file, verify its checksum, and create a local analysis table containing only:

- a non-identifying internal row key;
- recorded race;
- general recidivism decile score;
- score category;
- two-year rearrest outcome.

The raw file and the row-level processed table will both be excluded from version control. The processed table may be generated at runtime as `data/processed/analysis.csv`, but it must be listed in `.gitignore`. Reproducibility will rely on a download script, the commit-pinned URL, and the checksum rather than a second public copy of row-level data. Only aggregated figure-source and table CSV files may be included in the public repository.

### 4.3 Terminology

The raw labels are `African-American` and `Caucasian`. In prose and figures, they will be displayed as **Black** and **White**, with a note that these are mappings from the race categories recorded in the source data and are not measurements of self-defined racial identity.

The outcome will be called **two-year rearrest** whenever precision matters. The dataset variable is named `two_year_recid`, but observed rearrest is not identical to true reoffending.

---

## 5. Analysis populations and inclusion rules

### 5.1 Replication sample R: all recorded race groups

The known-result replication will use all 7,214 rows in `compas-scores-two-years.csv` without applying the separate 30-day case-matching filters used elsewhere in ProPublica's notebook.

This distinction is deliberate. ProPublica used a 6,172-person matched-case sample for some score-distribution and regression analyses, but its published two-year error tables used the 7,214-person file because case information was not required for that calculation. Mixing those samples would fail to reproduce the headline FPR and FNR values.

Expected composition of sample R:

| Recorded race | Expected n |
|---|---:|
| African-American | 3,696 |
| Caucasian | 2,454 |
| Hispanic | 637 |
| Other | 377 |
| Asian | 32 |
| Native American | 18 |
| **Total** | **7,214** |

Expected outcome counts are 3,251 with `two_year_recid = 1` and 3,963 with `two_year_recid = 0`.

### 5.2 Primary comparative sample C: Black and White defendants

Threshold-gap and primary error-cost analyses will use the 6,150 defendants whose recorded race is either `African-American` or `Caucasian`:

- Black: 3,696;
- White: 2,454.

The two-group restriction is prespecified because the research question and source dispute concern this contrast and because several other recorded groups have samples too small for stable threshold-by-threshold inference. Their exclusion from comparative inference does not imply that their outcomes are unimportant. Their sample counts will still be disclosed.

### 5.3 Missingness, duplication, and unexpected data

No imputation is permitted for the score, outcome, or race variables.

The expected file has:

- no missing values in `id`, `race`, the general recidivism score, `score_text`, or `two_year_recid`;
- one row per unique `id`;
- general recidivism scores from 1 through 10;
- only binary values 0 and 1 for `two_year_recid`.

The raw CSV contains two columns with the header `decile_score`. When read by pandas, the second is normally renamed `decile_score.1`. The script must assert that these two general-recidivism score columns are identical in all 7,214 rows before retaining one canonical variable named `score`. The violent-risk variable `v_decile_score` must not be substituted.

If the checksum, dimensions, key counts, missingness, score range, duplicate structure, or duplicate-score equality differs from the expectations above, analysis stops. The discrepancy must be diagnosed and documented; rows may not be silently dropped to recover the expected result.

---

## 6. Variables and decision rule

For defendant \(i\):

- \(Y_i = 1\) if `two_year_recid = 1`, and \(Y_i = 0\) otherwise;
- \(S_i \in \{1,\ldots,10\}\) is the general recidivism decile score;
- \(G_i \in \{B,W\}\) denotes the focal recorded race group.

For threshold \(t\), define the hypothetical binary decision rule

\[
\widehat{Y}_{i,t}=\mathbf{1}(S_i\ge t), \qquad t\in\{1,2,\ldots,11\}.
\]

Thus:

- \(t=1\) classifies everyone as higher risk;
- \(t=11\) classifies no one as higher risk;
- \(t=5\) reproduces ProPublica's `Low` versus `Medium/High` split;
- \(t=8\) reproduces `Low/Medium` versus `High`.

All primary threshold analyses use the **same threshold for every group**. Group-specific thresholds are outside scope because they would constitute a different deployment policy, not merely an audit of one common rule.

The endpoints \(t=1\) and \(t=11\) are retained because they make the full decision space and the behavior of the cost function explicit. Metrics with empty predicted-positive or predicted-negative denominators will be reported as undefined rather than assigned zero.

---

## 7. Estimands and metrics

For each group \(g\) and threshold \(t\), the analysis will calculate the confusion counts \(TP_{g,t}\), \(FP_{g,t}\), \(TN_{g,t}\), and \(FN_{g,t}\).

### 7.1 Primary error metrics

\[
FPR_{g,t}=\frac{FP_{g,t}}{FP_{g,t}+TN_{g,t}}
\]

\[
FNR_{g,t}=\frac{FN_{g,t}}{FN_{g,t}+TP_{g,t}}
\]

\[
PPV_{g,t}=\frac{TP_{g,t}}{TP_{g,t}+FP_{g,t}}
\]

The primary subgroup contrasts are signed absolute differences, Black minus White:

\[
\Delta FPR_t=FPR_{B,t}-FPR_{W,t},
\]

\[
\Delta FNR_t=FNR_{B,t}-FNR_{W,t},
\]

\[
\Delta PPV_t=PPV_{B,t}-PPV_{W,t}.
\]

Absolute differences are primary because ratios become unstable when the reference rate approaches zero. FPR and FNR ratios will be reported only at \(t=5\) and \(t=8\), with denominator values shown.

### 7.2 Secondary threshold-dependent metrics

For each group and, where relevant, the pooled sample:

- true-positive rate / recall: \(TPR=1-FNR\);
- true-negative rate / specificity: \(TNR=1-FPR\);
- negative predictive value: \(NPV=TN/(TN+FN)\);
- selection rate: \((TP+FP)/N\);
- accuracy: \((TP+TN)/N\);
- balanced accuracy: \((TPR+TNR)/2\);
- overall error rate: \((FP+FN)/N\).

Undefined quantities at degenerate endpoints will remain `NA` in tables and will not be connected across missing values in figures.

### 7.3 Threshold-independent discrimination

The empirical ROC AUC of the 1-10 score for predicting \(Y\) will be reported for:

- sample R overall;
- Black defendants;
- White defendants;
- the Black-White AUC difference.

AUC will be interpreted only as ranking discrimination. Similar AUC values do not imply similar FPR, FNR, or PPV at a chosen threshold.

### 7.4 Score-level calibration diagnostic

For each score \(s\in\{1,\ldots,10\}\) and group \(g\), calculate

\[
q_{g,s}=P(Y=1\mid S=s,G=g),
\]

and the score-specific difference \(q_{B,s}-q_{W,s}\).

This is a descriptive calibration diagnostic. The COMPAS decile will not be treated as a literal predicted probability, so Brier scores or probability calibration slopes will not be computed from \(S/10\).

---

## 8. Known-result replication

Before any extension result is interpreted, the code must reproduce ProPublica's \(t=5\) contingency tables on sample R.

Expected counts:

| Population | TN | FP | FN | TP | FPR | FNR | PPV |
|---|---:|---:|---:|---:|---:|---:|---:|
| All defendants | 2,681 | 1,282 | 1,216 | 2,035 | 32.35% | 37.40% | 61.35% |
| Black defendants | 990 | 805 | 532 | 1,369 | 44.85% | 27.99% | 62.97% |
| White defendants | 1,139 | 349 | 461 | 505 | 23.45% | 47.72% | 59.13% |

Counts must match exactly. Displayed rates may differ from ProPublica's rounded values only through transparent rounding. Failure of the counts to match blocks all later analysis until resolved.

The \(t=8\) `High`-only split will also be reproduced as a prespecified reference analysis, but it is not required to match a second hard-coded table before the pipeline runs.

---

## 9. Threshold sweep

For every \(t\in\{1,\ldots,11\}\):

1. apply the common rule \(\widehat{Y}_t=\mathbf{1}(S\ge t)\);
2. compute all metrics in Section 7 for Black, White, sample C, and sample R where applicable;
3. compute the Black-White metric gaps;
4. retain all raw numerators and denominators beside each rate;
5. identify but do not optimize any one fairness metric in isolation.

No threshold will be selected because it minimizes a racial gap alone. A threshold at which one gap becomes small may worsen another metric, create a degenerate classifier, or impose a different modeled aggregate error burden. The sweep is intended to show the complete consequence profile, not to announce a universally "fairest" cutoff.

---

## 10. Bootstrap uncertainty analysis

### 10.1 Resampling unit and scheme

The resampling unit is the individual defendant. The expected file contains one record per unique defendant identifier.

Use \(B=5{,}000\) nonparametric bootstrap replicates with NumPy's `PCG64` generator and seed `20260807`.

For the primary comparative sample, resample with replacement **within the Black and White groups separately**, preserving each group's observed sample size. For pooled sample-R estimates, resample within all six recorded race categories so that the observed race composition is fixed.

### 10.2 Bootstrap outputs

For each replicate, recompute:

- FPR, FNR, PPV, selection rate, accuracy, and balanced accuracy across thresholds;
- signed Black-White gaps;
- group-specific and pooled AUC;
- score-level observed rearrest rates and their group differences;
- the error-cost curves and focal optimal-threshold results described in Section 11.

Report 95% percentile intervals using the 2.5th and 97.5th percentiles. Curve bands are **pointwise**, not simultaneous. The project will not use the bands as a sequence of threshold-by-threshold significance tests.

If a metric is undefined in a bootstrap replicate because its denominator is zero, store it as missing. A confidence interval will be suppressed if fewer than 95% of replicates yield a defined value. This rule is especially relevant to PPV and NPV at the endpoint thresholds.

### 10.3 Inferential language

The analysis is primarily descriptive. It will report estimates, denominators, and uncertainty intervals rather than a large family of p-values. No threshold will be called "fair" or "unfair" because a pointwise interval excludes zero.

---

## 11. Asymmetric error-cost analysis

### 11.1 Primary loss function

For sample C, define the per-defendant aggregate loss at threshold \(t\) as

\[
L_t(\lambda)=\frac{\lambda FP_t+(1-\lambda)FN_t}{N},
\qquad \lambda\in[0,1].
\]

Here:

- \(\lambda\) is the relative weight assigned to a false positive;
- \(1-\lambda\) is the weight assigned to a false negative;
- the implied FP-to-FN cost ratio is \(\lambda/(1-\lambda)\) for interior values;
- \(\lambda=0.5\) assigns equal unit cost to FP and FN.

The loss will be evaluated on the grid \(\lambda\in\{0,0.01,\ldots,1\}\) and all thresholds \(t\in\{1,\ldots,11\}\).

For each \(\lambda\), define the complete minimizing set

\[
T^*(\lambda)=\underset{t\in\{1,\ldots,11\}}{\arg\min}\;L_t(\lambda).
\]

If multiple thresholds tie, all minimizers will be reported. The analysis will not hide a normative tie-break inside the code. For any display that mechanically requires one line, the highest minimizing threshold will be shown and explicitly labeled as a display convention favoring fewer adverse higher-risk classifications; the full minimizing set remains the reported estimand.

### 11.2 Group-specific weighted error loss

At any \((t,\lambda)\), define the group-specific weighted error loss

\[
L_{g,t}(\lambda)
=\lambda\frac{FP_{g,t}}{N_g}+(1-\lambda)\frac{FN_{g,t}}{N_g}
=\lambda(1-\pi_g)FPR_{g,t}+(1-\lambda)\pi_gFNR_{g,t},
\]

where \(\pi_g=P(Y=1\mid G=g)\).

This is a modeled weighted-error quantity, not a measurement of realized social harm. In the paper's prose, comparisons based on it may be described as the distribution of **modeled error burdens**, but code variables, figure labels, and table headings will use **group-specific weighted error loss**.

This decomposition will be reported at:

- \(t=5\);
- \(t=8\);
- every threshold in \(T^*(\lambda)\) for focal values \(\lambda\in\{0.25,0.50,0.75\}\).

The aggregate optimum and group-specific weighted error losses must be presented together. An aggregate loss minimum is not evidence that the modeled error-burden allocation between groups is acceptable.

### 11.3 Uncertainty in the optimum

For focal \(\lambda\in\{0.25,0.50,0.75\}\), the bootstrap will record how often each threshold belongs to the minimizing set. These selection frequencies describe sampling instability; they are not posterior probabilities that a threshold is morally or legally correct. Because a bootstrap replicate may contain multiple tied minimizers, threshold membership frequencies need not sum to 100%.

### 11.4 Robustness loss

As a prespecified appendix check, repeat the optimization using a class-conditional loss:

\[
\widetilde{L}_t(\lambda)=\lambda FPR_t+(1-\lambda)FNR_t.
\]

Unlike the primary per-defendant loss, this form gives equal structural weight to the non-rearrested and rearrested conditional pools before \(\lambda\) is applied. Comparing the two makes visible that an "optimal" threshold can depend on both error valuations and population base rates.

### 11.5 Interpretation constraint

The cost function is a transparent sensitivity device, not an empirical measurement of actual legal, moral, fiscal, or public-safety harm. No observed value of \(\lambda\) will be estimated from the dataset. Equal numerical weights will not be described as a neutral social choice.

---

## 12. Prespecified figures and tables

The first-stage paper will contain no more than six main figures. The planned set is five.

### Figure 1: Known-result replication

Point estimates and 95% bootstrap intervals for FPR, FNR, and PPV at \(t=5\), shown for Black and White defendants, with numerators and denominators available in the caption or companion table.

### Figure 2: Score distribution and score-level outcomes

Two panels:

1. distribution of decile scores by group, normalized within group;
2. observed two-year rearrest rate by decile score and group, with pointwise 95% intervals and cell counts.

### Figure 3: Threshold consequence curves

Four panels showing FPR, FNR, selection rate, and PPV across \(t=1,\ldots,11\) for Black and White defendants. Undefined PPV endpoint values remain blank. The ProPublica thresholds \(t=5\) and \(t=8\) are marked.

### Figure 4: Subgroup gap curves

Signed Black-minus-White gaps in FPR, FNR, and PPV across thresholds with pointwise 95% bootstrap intervals. A horizontal zero reference is included without treating zero as a universal fairness target.

### Figure 5: Error-cost sensitivity

Two or three panels showing:

1. the loss surface or threshold-specific loss curves over \(\lambda\);
2. the minimizing threshold set \(T^*(\lambda)\);
3. Black and White group-specific weighted error loss at focal \(\lambda\) values.

### Table 1: Sample and replication audit

Data checksum, sample counts, outcome counts, score mapping, confusion counts, and exact reproduction status.

### Table 2: Core threshold and cost results

Metrics and subgroup gaps at \(t=5\), \(t=8\), and the minimizing threshold sets for \(\lambda=0.25,0.50,0.75\), including uncertainty intervals and bootstrap selection frequencies.

### Table 3: Operational accountability record

The completed decision specification, error accounting, institutional-justification questions, and contestability requirements from Section 14.

Figures may be combined into multi-panel layouts, but metrics or thresholds may not be omitted merely because they weaken the narrative.

---

## 13. Prespecified robustness and sensitivity checks

The following checks are allowed without amending the protocol:

1. **Category mapping check:** verify that `Low = 1-4`, `Medium = 5-7`, and `High = 8-10`; reproduce \(t=5\) using both `score_text != "Low"` and `score >= 5`.
2. **High-only cutoff:** report \(t=8\) beside the ProPublica \(t=5\) cutoff.
3. **Population check:** repeat the aggregate error-cost calculation on sample R and compare it with the primary sample-C result.
4. **Loss normalization check:** compare the per-defendant loss \(L\) with the class-conditional loss \(\widetilde{L}\).
5. **Endpoint check:** retain \(t=1\) and \(t=11\) for error and cost curves while explicitly marking undefined predictive values.
6. **Reproducibility check:** run the complete pipeline twice from a clean environment and require identical numerical tables and figure-source data.

No unplanned covariate adjustment, subgroup split, alternative outcome, alternative algorithm, or new fairness metric may be presented as confirmatory under version 1.0.

---

## 14. Operational accountability framework

The original essay proposed public justification, repeated independent audit, and individual contestability. The empirical project will translate those three principles into four operational modules.

### A. Decision specification

An institution must state:

- the outcome being predicted;
- the time horizon;
- the deployment population and jurisdiction;
- the score and version used;
- the threshold or mapping from score to category;
- the action a higher-risk classification is permitted to influence;
- whether the score is advisory, presumptive, or binding;
- who has authority to select or change the rule.

### B. Error accounting and audit

An audit must report:

- sample construction and missingness;
- outcome prevalence and the limits of the outcome label;
- confusion-count numerators and denominators;
- FPR, FNR, PPV, NPV, selection rate, accuracy, and AUC;
- subgroup differences with uncertainty intervals;
- score-level outcome rates;
- threshold sensitivity rather than one preferred cutoff alone;
- local validation and, where repeated data exist, temporal drift;
- the audit schedule, responsible body, and public reporting rule.

### C. Institutional justification

The institution must answer:

- Why is this outcome an adequate target?
- Why is this threshold used?
- What harms are associated with false positives and false negatives?
- What relative priority has the institution assigned to those harms?
- Which group-specific weighted error losses, and therefore which modeled error-burden pattern, result from that choice?
- What alternatives were considered?
- What evidence or event would trigger revision or suspension?

The cost analysis supplies a way to expose the consequences of different weights. It does not supply the justification for choosing a weight.

### D. Individual contestability

An affected person must have a meaningful route to challenge:

- incorrect input data;
- whether the model applies to the person's situation;
- whether the correct score, version, and threshold were used;
- how the score was interpreted or weighted;
- the adverse consequence drawn from it;
- the adequacy of the human decision-maker's independent reasons.

The process should identify who reviews the challenge, the evidence available to the person, the time limit for a response, and the remedy for an error. Contestability does not remove group-level trade-offs; it prevents a group-derived probability from becoming an unanswerable judgment about an individual.

---

## 15. Analysis order and decision rules

The implementation must proceed in this order:

1. **Freeze protocol:** commit this file before extension analysis code is run.
2. **Acquire data:** download the commit-pinned file and verify SHA-256.
3. **Validate schema:** run every integrity assertion in Sections 4-6.
4. **Create minimal analysis table:** remove direct identifiers and unused case fields.
5. **Run exact replication:** require the Section 8 counts to match.
6. **Generate descriptive and calibration diagnostics.**
7. **Run the full threshold sweep.**
8. **Run the bootstrap.**
9. **Run primary and robustness cost analyses.**
10. **Generate the prespecified tables and figures.**
11. **Write Results only after all prespecified outputs exist.**
12. **Write the accountability and limitations sections without changing the empirical specification.**

If a step fails, later steps pause. The researcher may fix a coding or data-handling error, but the failure and correction must be recorded.

---

## 16. Reproducibility requirements

The repository should contain:

```text
COMPAS-project/
├── .gitignore
├── README.md
├── PROTOCOL.md
├── AMENDMENTS.md
├── requirements.txt or an equivalent lockfile
├── data/
│   └── README.md               # source, checksum, and regeneration instructions
├── src/
│   ├── fetch_data.py
│   ├── prepare_data.py
│   ├── metrics.py
│   ├── bootstrap.py
│   ├── cost_analysis.py
│   └── make_outputs.py
├── tests/
│   ├── test_data_integrity.py
│   ├── test_threshold_mapping.py
│   └── test_propublica_replication.py
├── output/
│   ├── figures/
│   └── tables/
└── paper/
```

Minimum technical requirements:

- pin the Python environment and package versions;
- set and expose all random seeds;
- separate data preparation, metric definitions, bootstrap, and plotting;
- test the exact \(t=5\) confusion counts;
- generate any row-level processed table only at runtime under `data/processed/`, with the directory excluded through `.gitignore`;
- save only aggregated figure-source and result tables as public machine-readable files;
- avoid manual spreadsheet edits or manually transcribed results;
- make one documented command reproduce every public table and figure;
- ensure no direct identifier appears in logs, figures, tables, or processed files, and no row-level raw or processed dataset is committed;
- require the author to understand and be able to explain every transformation and metric.

---

## 17. Limitations to be stated in the paper

At minimum, the final paper must acknowledge:

1. **Rearrest is not reoffense.** Policing, surveillance, reporting, and record-linkage processes affect the observed label.
2. **Historical and local data.** The sample concerns Broward County defendants scored principally in 2013-2014 and does not establish current performance elsewhere.
3. **Measurement error.** ProPublica reported an estimated 3.75% record-matching error rate in a 400-case audit, with an interval of approximately +/-1.8 percentage points.
4. **Proprietary system.** The public file contains outputs and outcomes, not the complete COMPAS formula, training data, or institutional implementation rules.
5. **Unknown use and consequence.** A hypothetical binary cutoff does not establish how any particular judge or agency actually used a score.
6. **Discrete scores.** Only a small set of common thresholds is available, and neighboring policy values can generate the same minimizing set.
7. **Sampling uncertainty is not total uncertainty.** The bootstrap does not capture systematic record-linkage error, label bias, policy changes, or external-validity uncertainty.
8. **Two-group focus.** The primary comparison omits inference for smaller recorded groups and does not address intersectional burdens.
9. **No causal identification.** Metric gaps describe joint patterns in scores and observed outcomes; they do not isolate a causal mechanism.
10. **Cost weights are illustrative.** The analysis reveals sensitivity to value choices but does not validate a particular valuation.
11. **Fairness criteria remain plural.** Similar calibration or AUC can coexist with unequal error rates; no single reported metric settles institutional legitimacy.

---

## 18. Amendment and exploratory-analysis policy

`AMENDMENTS.md` will record, for every change:

- date and version;
- exact change;
- reason;
- whether relevant results had already been seen;
- which outputs or claims are affected.

Rules:

- coding corrections that restore the written specification become patch versions such as 1.0.1;
- substantive changes to an outcome, sample, threshold set, metric, bootstrap method, loss function, or focal comparison require version 1.1 or later;
- new datasets, algorithms, or jurisdictions require a new major protocol;
- unplanned analyses may appear only in a section titled **Exploratory Analyses**;
- exploratory results may motivate later work but cannot replace an inconvenient prespecified result.

---

## 19. Completion and stopping condition

Version 1 of the project is complete when all of the following exist:

- this frozen protocol and an amendment log;
- a reproducible data-acquisition and validation pipeline;
- exact ProPublica replication;
- 4-6 informative, prespecified figures;
- one replication table and one core result table;
- bootstrap uncertainty outputs;
- threshold and asymmetric-cost analyses;
- a completed operational accountability table;
- an 8-12 page working paper with limitations;
- a clean README explaining how to reproduce the results;
- no row-level raw or processed dataset in the public repository;
- a successful clean end-to-end rerun.

The first stage stops at that point. It will not expand merely to pursue a journal, workshop, additional model, or broader literature label. The target effort is approximately 25-40 focused hours. If the work reaches 40 hours before the stopping condition is met, the project must be reviewed for simplification rather than automatically expanded.

---

## 20. Planned paper structure

1. Introduction
2. The COMPAS dispute and incompatible fairness criteria
3. Data and methods
4. Known-result replication
5. Threshold analysis
6. Error-cost sensitivity and group-specific weighted error loss
7. From measurement to institutional accountability
8. Limitations
9. Conclusion

The central empirical conclusion will be stated conditionally: changing a threshold or an error-cost weighting changes the decision rule and the distribution of mistakes. The central institutional conclusion will remain separate: because the data do not choose the legitimate weighting or consequence, responsibility rests with the public institution that adopts and uses the rule.

---

## 21. Core references

- Angwin, Julia, Jeff Larson, Surya Mattu, and Lauren Kirchner. ["Machine Bias."](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing) *ProPublica*, May 23, 2016.
- Larson, Jeff, Surya Mattu, Lauren Kirchner, and Julia Angwin. ["How We Analyzed the COMPAS Recidivism Algorithm."](https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm) *ProPublica*, May 23, 2016.
- ProPublica. [`compas-analysis`](https://github.com/propublica/compas-analysis), public data and analysis repository.
- Chouldechova, Alexandra. ["Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments."](https://doi.org/10.1089/big.2016.0047) *Big Data* 5, no. 2 (2017): 153-163.
- Kleinberg, Jon, Sendhil Mullainathan, and Manish Raghavan. ["Inherent Trade-Offs in the Fair Determination of Risk Scores."](https://doi.org/10.4230/LIPIcs.ITCS.2017.43) In *8th Innovations in Theoretical Computer Science Conference*, 2017.

---

**Protocol lock statement:** Results will not be used to retroactively change the primary sample, threshold definition, metric definitions, bootstrap scheme, loss function, focal \(\lambda\) values, or planned outputs without a dated amendment and explicit exploratory label.
