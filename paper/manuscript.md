# Who Bears the Error?

## Threshold Choice, Fairness Trade-offs, and Institutional Accountability in COMPAS

**Author:** Zhixun Zheng  
**Date:** August 2026

## Abstract

Risk scores become consequential only after an institution chooses how to convert them into decisions. Using ProPublica's historical Broward County COMPAS data, this study asks how a common classification threshold redistributes false-positive and false-negative errors across recorded racial groups and what that implies for institutional accountability. It reproduces ProPublica's published two-year contingency counts in the full 7,214-defendant sample, evaluates all common decile thresholds, estimates pointwise uncertainty with 5,000 race-stratified defendant-level bootstrap replicates, and applies a prespecified asymmetric error-loss analysis in the 6,150-defendant Black-White comparison sample. Black and White ROC AUC values were nearly identical (0.6918 and 0.6931). At the conventional $t=5$ cutoff, however, false-positive rates were 44.85% and 23.45%, while false-negative rates were 27.99% and 47.72%, respectively; PPV differed by 3.84 percentage points. The direction of the FPR and FNR gaps persisted across every interior threshold. The aggregate loss-minimizing threshold also moved sharply with the prespecified false-positive weight: $\lambda=.25,.50,.75$ yielded $t^*=2,6,10$. Those focal optima were comparatively stable under the bootstrap and unchanged in the full-population robustness check. These are conditional optima, not morally correct thresholds. The results show where statistical evaluation ceases to determine a public decision: data can describe a threshold's consequences and optimization can select a rule under a stated objective, but the institution remains responsible for the objective, threshold, permitted consequence, distributive justification, and means of individual contestation.

**Keywords:** COMPAS; algorithmic fairness; classification thresholds; false positives; false negatives; institutional accountability

# Introduction

Algorithmic risk scores do not become consequential decision rules merely by producing predictions. An institution must still decide where to place a classification threshold, what consequence a higher-risk classification may influence, and which errors it is more willing to tolerate. The COMPAS controversy made the stakes of those choices visible. In 2016, ProPublica reported that, among Broward County defendants who were not rearrested within two years, Black defendants were nearly twice as likely as White defendants to be classified above COMPAS’s low-risk category; false-negative rates ran in the opposite direction (Angwin et al. 2016; Larson et al. 2016). A subsequent reanalysis reported similar Black and White ranking discrimination and approximately similar observed rearrest rates within broad risk categories (Flores, Bechtel, and Lowenkamp 2016). These findings can coexist because they describe different properties of the same scores after those scores are converted into classifications.

The distinction is central to debates about algorithmic fairness. AUC evaluates ranking discrimination, PPV describes the observed outcome composition among those classified as higher risk, and FPR and FNR describe different directions of classification error. When observed outcome rates differ across groups and prediction is imperfect, several plausible fairness criteria generally cannot be satisfied simultaneously (Chouldechova 2017; Kleinberg, Mullainathan, and Raghavan 2017). These incompatibility results explain why apparently conflicting evaluations may each be statistically correct. They do not determine which criterion a public institution should prioritize, where it should place the threshold, or what consequences the resulting category should carry.

That unresolved step motivates this study. Much of the COMPAS dispute has been framed as a contest among performance or fairness metrics. Yet a graded score does not contain its own decision cutoff. The same score outputs can produce different classifications, false-positive and false-negative rates, and group disparities when a common threshold is moved. An institution can also obtain different loss-minimizing thresholds by assigning different relative weights to false positives and false negatives. Treating either the cutoff or the weighting as an automatic property of the model obscures the institutional choice between prediction and action.

This paper therefore asks: **How does the choice of classification threshold redistribute false-positive and false-negative errors across recorded racial groups in the historical COMPAS data, and what does that imply for institutional accountability?** It first reproduces ProPublica’s published two-year contingency counts from the public historical Broward County data. It then sweeps every common decile threshold, estimates Black-minus-White metric gaps with 5,000 race-stratified defendant-level bootstrap replicates, and evaluates a prespecified asymmetric error-loss function across false-positive weights. The thresholds are analytical decision rules rather than a reconstruction of actual judicial use, and the outcome is observed two-year rearrest rather than true offending. The error weights are sensitivity parameters, not measurements of social harm.

Three findings organize the analysis. First, the known ProPublica contingency counts are reproduced exactly. Second, Black and White ROC AUC values are nearly identical and PPV differences are comparatively small, while common thresholds generate substantially larger, oppositely signed FPR and FNR gaps across the interior threshold range. Third, the aggregate loss-minimizing threshold changes from $t=2$ to $t=6$ to $t=10$ when the prespecified false-positive weight $\lambda$ moves from 0.25 to 0.50 to 0.75. The focal optima are comparatively stable under the prespecified bootstrap, but they remain conditional on the selected objective. Aggregate optimality also does not determine whether the resulting distribution of modeled weighted error loss across groups is acceptable.

The paper’s contribution is consequently both empirical and institutional. Empirically, it extends a known-result replication into a full sweep of the available common decile thresholds, with uncertainty estimates and transparent cost sensitivity. Institutionally, it identifies the point at which statistical evaluation ceases to determine the decision: data can describe the consequences of a threshold and optimization can select a threshold under a specified objective, but neither can by itself choose or justify the legitimate objective or permitted consequence. The operational framework developed from the analysis therefore focuses on decision specification, error accounting, institutional justification, and individual contestability. It is not offered as a universal solution to algorithmic fairness or as proof of legal compliance. Its narrower claim is that responsibility remains with the institution that converts a score into a rule with consequences.

The remainder of the paper proceeds as follows. Section 2 situates the COMPAS dispute within work on competing metrics, incompatible fairness criteria, threshold choice, and institutional authority. Section 3 describes the data and analysis. Section 4 presents the results. Section 5 develops the institutional-accountability argument, Section 6 states the study’s limitations, and Section 7 concludes.

# Background and Related Work

## The COMPAS dispute and competing empirical interpretations

The public COMPAS debate began from a disagreement about what property of a risk instrument should count as evidence of fair performance. ProPublica examined Broward County defendants with two years of follow-up and reported sharply different directions of error at the Low versus Medium/High cutoff: Black defendants who were not rearrested were classified above Low more often than White defendants, while White defendants who were rearrested were classified Low more often than Black defendants (Angwin et al. 2016; Larson et al. 2016). Northpointe’s response disputed ProPublica’s interpretation and organized its defense around accuracy equity and predictive parity, while also objecting to aspects of the cutoff and error analysis (Dieterich, Mendoza, and Brennan 2016).

Flores, Bechtel, and Lowenkamp (2016) offered a related but distinct reanalysis. Using the decile score and a more restricted analytical sample, they reported AUC values of 0.69 for White defendants and 0.70 for Black defendants, with no statistically significant difference, and observed rearrest rates that were close across the two groups within the broad Low, Medium, and High categories. They also emphasized that converting a three-category instrument into a binary classifier requires a binning decision. The two binning rules they examined changed false-positive and false-negative rates in opposite directions.

These analyses need not be treated as mutually exclusive verdicts. They use different samples in places and ask different statistical questions. Similar ranking discrimination or outcome rates within broad score categories do not imply equal false-positive and false-negative rates after a cutoff is imposed. Conversely, unequal classification-error rates do not by themselves establish that the score has different ranking discrimination across groups. The present study therefore does not use one metric to declare the entire instrument fair or unfair. It reproduces the published contingency table as a known result and then treats the threshold as an explicit analytical input.

## Different metrics answer different questions

The relevant measures condition on different events. ROC AUC describes how often a randomly selected rearrested defendant receives a higher score than a randomly selected non-rearrested defendant. It is a ranking measure and does not require a particular threshold. Positive predictive value instead conditions on the higher-risk classification and asks what share of those classified higher risk were observed to be rearrested. False-positive and false-negative rates condition on the observed outcome and distinguish the two directions of error.

Because the denominators differ, parity on one measure does not imply parity on another. This point is especially important when a score is used in a decision process. AUC concerns the ordering produced by the score; PPV concerns the composition of a selected category; FPR and FNR concern who bears each type of classification mistake. Reporting them together is therefore not a search for one master fairness statistic. It is an accounting of distinct properties that may matter for distinct institutional reasons.

## Calibration, predictive parity, and incompatibility

Chouldechova (2017) formalized the relationship among prevalence, predictive parity, and classification-error rates. When observed outcome prevalence differs across groups, equal PPV at a threshold is generally incompatible with equal FPR and FNR unless prediction is perfect. Her COMPAS illustration also showed that approximate calibration or predictive parity can coexist with error-rate imbalance. The result explains why ProPublica and its critics could emphasize different, statistically defensible properties of the same data.

Kleinberg, Mullainathan, and Raghavan (2017) established a related score-level result. They considered calibration within groups, balance for the negative class, and balance for the positive class, and showed that all three can be satisfied together only in constrained cases: perfect prediction or equal base rates. Their balance conditions are score-level conditions, not identical to threshold-specific FPR and FNR parity, although they generalize the same concern about differential treatment of positive and negative classes.

Neither theorem chooses an institutional objective. Kleinberg and colleagues expressly declined to recommend how conflicts among fairness definitions should be resolved, and Chouldechova distinguished statistical criteria from the social and ethical judgment of fairness. In this paper, the incompatibility results provide context for the empirical pattern; the COMPAS threshold sweep is not presented as a new proof of either theorem or as a test of every theorem condition.

## From a score to a decision rule

The distinction between a score and a rule is already visible in the early COMPAS exchange. Flores, Bechtel, and Lowenkamp (2016) observed that a multicategory score must be binned before contingency-table measures can be calculated. They showed that placing Medium with High lowers one type of error and raises another relative to placing Medium with Low, and noted that different users could prefer different trade-offs. ProPublica likewise reported its main Low-versus-Medium/High table and a High-only sensitivity check (Larson et al. 2016).

Those comparisons identify the threshold as consequential, but they do not map the full available threshold space or make the weighting of false positives and false negatives explicit. This study adds that step. It evaluates every common decile threshold, reports uncertainty across the resulting metric curves, and asks how a transparent loss-minimizing threshold changes when the relative error weight changes. The contribution is not a new risk model. It is an audit of the choices required to turn an existing score into a common binary rule.

## Institutional use and contestability

The legal controversy surrounding COMPAS also illustrates why predictive evaluation does not settle legitimate use. In *State v. Loomis*, the Wisconsin Supreme Court held that a sentencing court’s consideration of COMPAS did not violate due process when the assessment was used with the limitations and cautions specified in the opinion (Wisconsin Supreme Court 2016, paras. 98–100, 120). The holding was narrow. The court said that a risk score could not determine incarceration or sentence severity, could not be the determinative factor in deciding whether community supervision was safe and effective, and had to be accompanied by a written advisement addressing the proprietary model, group-based inference, possible racial disparity, the absence of Wisconsin cross-validation at the time, and the need for continuing monitoring. The court also stressed that the sentencing judge had relied on independent factors and stated that the sentence would have been the same without COMPAS (Wisconsin Supreme Court 2016, paras. 104–109).

*Loomis* therefore should not be cited as a general judicial endorsement of COMPAS or as proof that a particular threshold is lawful. It shows, within one jurisdiction and procedural setting, that the authority given to a score depends on the permitted consequence, the reasons independently supporting the decision, the warnings supplied to the decision-maker, and the opportunity to review and challenge relevant information. The accountability framework developed here is a normative proposal informed by those concerns, not a claim that its four modules exhaust constitutional or statutory requirements.

Together, this literature leaves a focused gap. Prior work explains competing metrics, demonstrates incompatibilities, and identifies legal cautions around institutional use. It does not, by itself, show how every available common threshold redistributes observed errors, how sampling uncertainty surrounds that redistribution, or how prespecified error weights move the aggregate optimum. Those are the empirical steps used below to connect score evaluation to institutional responsibility.

# Data and Methods

## Data source and provenance

The analysis used ProPublica’s public `compas-scores-two-years.csv` file from the `propublica/compas-analysis` repository (Larson et al. 2016). The source was fixed at commit `bafff5da3f2e45eca6c2d5055faad269defd135a`; the downloaded file had SHA-256 digest `c451db85908b2f7fef1d83203bedf6b71ecda0d5af468d82ae62178f91d0cc7d` and dimensions 7,214 rows by 53 columns. The data concern defendants scored in Broward County, Florida, principally during 2013–2014. The pipeline downloaded the commit-pinned file and halted before analysis if its checksum or dimensions differed from these frozen values.

Additional integrity checks required the outcome to be binary, the general recidivism score to lie from 1 through 10, the defendant identifier to be unique and complete, and the analysis variables to contain no missing values. The raw CSV contains two columns headed `decile_score`; after import, the second is named `decile_score.1`. The preparation step required these columns to agree in all rows before retaining one as the canonical general recidivism score. The violent-risk variable `v_decile_score` was not used. Any failed check halted the pipeline rather than triggering silent row deletion or imputation.

The source file contains direct identifiers and detailed case fields that were unnecessary for the analysis. Neither the raw file nor any row-level processed table was retained in the public repository. If generated at runtime, the minimized table contained only a nonidentifying row key, recorded race, general recidivism decile score and category, and the two-year outcome, and was excluded through `.gitignore`. Public machine-readable outputs were limited to aggregated figure-source and result tables. The pinned download, checksum, and preparation code therefore provide reproducibility without republishing a second person-level dataset.

## Analysis populations and variables

The known-result replication used sample R, all 7,214 rows in the source file: 3,696 recorded as `African-American`, 2,454 as `Caucasian`, 637 as Hispanic, 377 as Other, 32 as Asian, and 18 as Native American. It did not apply the separate 30-day case-matching filters used in some other parts of ProPublica’s analysis because the published two-year error tables were calculated from the full file. The primary comparative sample C contained the 6,150 defendants recorded as `African-American` or `Caucasian`. These categories are displayed as Black and White for readability, but they are administrative labels in the source data rather than measures of self-identified racial identity. The smaller recorded groups were included in the replication audit and pooled estimates but excluded from the prespecified two-group comparisons.

For defendant $i$, $Y_i=1$ denoted `two_year_recid = 1`, and $Y_i=0$ otherwise. This variable measures observed rearrest within two years, not true offending. The general recidivism decile score was denoted $S_i\in\{1,\ldots,10\}$, and the focal recorded group was $G_i\in\{B,W\}$. No values of the score, outcome, or race variables were imputed.

## Threshold rules and performance measures

For each common threshold $t$, the analytical binary rule was $$\widehat{Y}_{i,t}=\mathbf{1}(S_i\ge t),
\qquad t\in\{1,2,\ldots,11\}.$$ Thus, $t=1$ classified every defendant as higher risk, whereas $t=11$ classified none. The $t=5$ rule reproduced COMPAS Low versus Medium/High, and $t=8$ reproduced Low/Medium versus High. Every primary comparison applied the same threshold to all groups. The endpoint rules were retained to display the full available decision space; a metric with an empty denominator was stored as undefined rather than set to zero.

At each threshold, true-negative, false-positive, false-negative, and true-positive counts were computed before the corresponding rates. The primary metrics were $$FPR=\frac{FP}{FP+TN},\qquad
FNR=\frac{FN}{FN+TP},\qquad
PPV=\frac{TP}{TP+FP}.$$ The primary group contrasts were signed Black-minus-White differences in these rates. Differences rather than ratios were used as the primary contrasts because ratios become unstable when the White reference rate approaches zero; Black/White FPR and FNR ratios were retained only for the two prespecified reference cutoffs, $t=5$ and $t=8$. The threshold sweep also calculated TPR, TNR, NPV, selection rate, accuracy, balanced accuracy, and overall error rate, with the underlying numerators and denominators retained in the canonical outputs.

Threshold-independent ranking discrimination was summarized by the empirical ROC AUC for sample R, Black defendants, White defendants, and the signed Black-minus-White difference. AUC was interpreted as a ranking measure, not as evidence that classification errors at a selected cutoff were similar. As a descriptive score-level calibration diagnostic, the analysis also estimated $$q_{g,s}=P(Y=1\mid S=s,G=g)$$ for each score $s=1,\ldots,10$, together with $q_{B,s}-q_{W,s}$. Because the COMPAS decile is not a literal predicted probability, no Brier score or probability-calibration slope was calculated from $S/10$.

## Bootstrap uncertainty

Uncertainty was evaluated with 5,000 nonparametric defendant-level bootstrap replicates generated by NumPy’s `PCG64` generator with seed `20260807`. For sample C comparisons, defendants were resampled with replacement within the Black and White groups separately, preserving both observed group sizes. For pooled sample-R estimates, resampling occurred within all six recorded race categories, preserving the observed race composition. Each replicate recomputed the threshold-dependent metrics and signed gaps, pooled and group-specific AUC values, score-level rearrest rates, and the focal error-cost optima.

Intervals were the 2.5th and 97.5th percentiles of the bootstrap distribution. Threshold and score curves use pointwise, not simultaneous, 95% intervals and were not interpreted as a sequence of significance tests. A replicate-specific undefined value was stored as missing, and an interval was suppressed if fewer than 95% of replicates produced a defined estimate.

## Error-cost sensitivity

The primary sensitivity analysis evaluated the per-defendant aggregate loss in sample C, $$L_t(\lambda)=\frac{\lambda FP_t+(1-\lambda)FN_t}{N},
\qquad \lambda\in[0,1],$$ where $\lambda$ is the prespecified weight on a false positive and $1-\lambda$ is the weight on a false negative. Loss was calculated for all thresholds and for $\lambda=0,0.01,\ldots,1$. For each value of $\lambda$, the estimand was the complete minimizing set $$T^*(\lambda)=\underset{t\in\{1,\ldots,11\}}{\arg\min}\;L_t(\lambda).$$ All tied minimizers were retained. When a display required one line, the highest minimizing threshold was shown as an explicit convention favoring fewer higher-risk classifications, not as an additional optimization criterion. The focal values $\lambda=0.25,0.50,0.75$ represent false-positive to false-negative weight ratios of 1:3, 1:1, and 3:1.

To examine the distribution associated with an aggregate optimum, group-specific weighted error loss was defined as $$L_{g,t}(\lambda)
=\lambda\frac{FP_{g,t}}{N_g}+(1-\lambda)\frac{FN_{g,t}}{N_g}.$$ This quantity was evaluated at $t=5$, $t=8$, and the focal minimizing thresholds. It is a modeled sensitivity quantity rather than a measurement of realized social harm. In the bootstrap, the analysis recorded how often each threshold belonged to the full minimizing set at each focal $\lambda$. Because a replicate could contain tied minimizers, membership frequencies across thresholds need not sum to 100%.

As a prespecified robustness check, the optimization was repeated using the class-conditional loss $$\widetilde{L}_t(\lambda)=\lambda FPR_t+(1-\lambda)FNR_t.$$ Unlike the per-defendant primary loss, this expression gives equal structural weight to the non-rearrested and rearrested conditional pools before applying $\lambda$. Comparing the two specifications makes visible the dependence of an optimum on both the chosen error weights and population base rates. Neither loss function estimates which weighting is legally, morally, or institutionally appropriate.

## Prespecification and reproducibility

The analysis plan was frozen before implementation of the threshold, bootstrap, and cost extensions. Because the dataset was public and ProPublica’s headline error rates were already known, the $t=5$ analysis was designated a known-result replication rather than a blind preregistration. Extension results were generated only after the acquisition and integrity checks passed and the expected $t=5$ contingency counts were reproduced exactly. Category mapping, the $t=8$ cutoff, sample-R aggregate loss, endpoint behavior, the class-conditional loss, and clean-run reproducibility were the prespecified robustness checks.

The population robustness check repeated the aggregate per-defendant loss calculation across the full sample R population and compared its minimizing set with the primary sample C result at every value on the prespecified $\lambda$ grid. The code separated acquisition, preparation, metric calculation, resampling, cost analysis, and output generation; exposed the random seed; and generated public tables and figure-source data without manual transcription. The full pipeline was required to reproduce identical aggregate outputs from a clean run.

<div class="threeparttable">

<div id="tab:sample-replication">

| *Panel A. Data and sample audit*          |                                                       |                       |       |       |       |
|:------------------------------------------|------------------------------------------------------:|----------------------:|------:|------:|------:|
| Audit item                                |                                         Frozen result |                       |       |       |       |
| Source file and fixed commit              |         `compas-scores-two-years.csv`; `bafff5da3f2e` |                       |       |       |       |
| SHA-256 verification                      |                                                Passed |                       |       |       |       |
| Raw dimensions                            |                        7,214 rows $\times$ 53 columns |                       |       |       |       |
| Replication sample R                      |                                                 7,214 |                       |       |       |       |
| Sample R outcomes, no rearrest / rearrest |                       3,963 (54.93%) / 3,251 (45.07%) |                       |       |       |       |
| Primary comparative sample C              |                                                 6,150 |                       |       |       |       |
| Sample C outcomes, no rearrest / rearrest |                       3,283 (53.38%) / 2,867 (46.62%) |                       |       |       |       |
| Black (`African-American`)                |                                                 3,696 |                       |       |       |       |
| White (`Caucasian`)                       |                                                 2,454 |                       |       |       |       |
| Other recorded groups                     | Hispanic 637; Other 377; Asian 32; Native American 18 |                       |       |       |       |
| *Panel B. Exact $t=5$ replication*        |                                                       |                       |       |       |       |
| Group                                     |                                                   $N$ |                    TN |    FP |    FN |    TP |
| All defendants                            |                                                 7,214 |                 2,681 | 1,282 | 1,216 | 2,035 |
| Black                                     |                                                 3,696 |                   990 |   805 |   532 | 1,369 |
| White                                     |                                                 2,454 |                 1,139 |   349 |   461 |   505 |
| *Panel C. Threshold-independent ROC AUC*  |                                                       |                       |       |       |       |
| Population or contrast                    |                                              Estimate |      95% bootstrap CI |       |       |       |
| Sample R                                  |                                                0.7022 |    \[0.6902, 0.7144\] |       |       |       |
| Black                                     |                                                0.6918 |    \[0.6751, 0.7088\] |       |       |       |
| White                                     |                                                0.6931 |    \[0.6713, 0.7150\] |       |       |       |
| Black $-$ White                           |                                             $-0.0013$ | \[$-0.0287$, 0.0261\] |       |       |       |

Sample construction, exact replication, and score discrimination

</div>

<div class="tablenotes">

*Note.* Sample R contains all recorded race groups; sample C contains defendants recorded as African-American or Caucasian, displayed as Black and White. The outcome is observed two-year rearrest. At $t=5$, scores 5–10 are classified as higher risk. TN, FP, FN, and TP denote true negatives, false positives, false negatives, and true positives. Panel B reproduces ProPublica’s published contingency counts exactly. AUC intervals are 95% percentile intervals from 5,000 race-stratified bootstrap replicates. Recorded race categories are administrative labels in the source data and are not measures of self-defined racial identity.

</div>

</div>

# Results

## Replication and score discrimination

The analysis first reproduced ProPublica’s published $t=5$ contingency counts exactly. In the full replication sample of 7,214 defendants, 1,282 false positives and 1,216 false negatives were observed. Among Black defendants, the corresponding counts were 805 false positives and 532 false negatives; among White defendants, they were 349 and 461, respectively (Table <a href="#tab:sample-replication" data-reference-type="ref" data-reference="tab:sample-replication">1</a>).

Ranking discrimination was nearly identical across the two focal groups. The ROC AUC was 0.6918 for Black defendants and 0.6931 for White defendants, yielding a Black-minus-White difference of $-0.0013$. The 95% bootstrap interval for this difference, \[$-0.0287$, 0.0261\], included small differences in either direction (Table <a href="#tab:sample-replication" data-reference-type="ref" data-reference="tab:sample-replication">1</a>). Thus, the score ranked rearrest risk similarly across the two groups even though, as shown below, a common classification threshold produced substantially different error rates. Figure <a href="#fig:score-diagnostics" data-reference-type="ref" data-reference="fig:score-diagnostics">1</a> displays the group score distributions and observed rearrest rates within each score as descriptive diagnostics.

<figure id="fig:score-diagnostics">
<embed src="figure2.pdf" />
<figcaption>Score distributions and observed outcomes. Panel A shows the within-group distribution of general-recidivism decile scores. Panel B shows observed two-year rearrest rates within each score with pointwise 95% bootstrap intervals; Black/White cell counts are printed below each score. The decile is not treated as a literal probability forecast.</figcaption>
</figure>

## Moving the threshold changes the allocation of errors

At the conventional $t=5$ cutoff, the false-positive rate was 44.85% for Black defendants and 23.45% for White defendants, a gap of 21.39 percentage points. The false-negative pattern ran in the opposite direction: 27.99% for Black defendants and 47.72% for White defendants, a gap of $-19.74$ percentage points. Positive predictive values were much closer, at 62.97% and 59.13%, respectively (Table <a href="#tab:threshold-cost-results" data-reference-type="ref" data-reference="tab:threshold-cost-results">2</a>; Figure <a href="#fig:t5" data-reference-type="ref" data-reference="fig:t5">2</a>).

<figure id="fig:t5">
<embed src="figure1.pdf" style="width:72.0%" />
<figcaption>Group-specific false-positive rate, false-negative rate, and positive predictive value at the <span class="math inline"><em>t</em> = 5</span> common cutoff. Points are estimates and bars are pointwise 95% bootstrap intervals.</figcaption>
</figure>

These differences were not unique to the $t=5$ cutoff. Increasing the common threshold reduced false-positive rates and increased false-negative rates for both groups, while also reducing the share classified as higher risk. The relative allocation of errors, however, changed with the threshold rather than disappearing. At $t=8$, for example, the Black-minus-White FPR gap was still $+10.38$ percentage points, while the FNR gap remained $-18.79$ percentage points. The corresponding PPV gap was only $+1.64$ percentage points (Table <a href="#tab:threshold-cost-results" data-reference-type="ref" data-reference="tab:threshold-cost-results">2</a>; Figures <a href="#fig:threshold-consequences" data-reference-type="ref" data-reference="fig:threshold-consequences">3</a>–<a href="#fig:gaps" data-reference-type="ref" data-reference="fig:gaps">4</a>).

<div class="threeparttable">

<div id="tab:threshold-cost-results">

| *Panel A. Prespecified common cutoffs* |        |               |                |                |                        |                      |
|:---------------------------------------|:-------|--------------:|---------------:|---------------:|-----------------------:|---------------------:|
| Cutoff                                 | Metric |     Black (%) |      White (%) | B$-$W gap (pp) |       95% bootstrap CI |            B/W ratio |
| $t=5$                                  | FPR    |         44.85 |          23.45 |       $+21.39$ | \[$+18.13$, $+24.55$\] |                 1.91 |
|                                        | FNR    |         27.99 |          47.72 |       $-19.74$ | \[$-23.50$, $-16.01$\] |                 0.59 |
|                                        | PPV    |         62.97 |          59.13 |        $+3.84$ |   \[$+0.02$, $+7.77$\] |                    – |
| $t=8$                                  | FPR    |         15.82 |           5.44 |       $+10.38$ |  \[$+8.37$, $+12.48$\] |                 2.91 |
|                                        | FNR    |         61.02 |          79.81 |       $-18.79$ | \[$-22.16$, $-15.37$\] |                 0.76 |
|                                        | PPV    |         72.29 |          70.65 |        $+1.64$ |   \[$-4.38$, $+7.61$\] |                    – |
| *Panel B. Focal cost sensitivity*      |        |               |                |                |                        |                      |
| $\lambda$ (FP:FN)                      |        | Primary $t^*$ | Aggregate loss |     Black loss |             White loss | Bootstrap membership |
| 0.25 (1:3)                             |        |             2 |         0.1275 |         0.1191 |                 0.1401 |               99.62% |
| 0.50 (1:1)                             |        |             6 |         0.1720 |         0.1791 |                 0.1612 |               90.92% |
| 0.75 (3:1)                             |        |            10 |         0.1150 |         0.1252 |                 0.0996 |               87.70% |

Core threshold results and cost-sensitive optimal thresholds

</div>

<div class="tablenotes">

*Note.* Both cutoffs apply the same decision rule to every group: higher risk if score $\geq t$. The $t=5$ cutoff reproduces Low versus Medium/High; $t=8$ reproduces Low/Medium versus High. Gaps are signed Black-minus-White differences in percentage points. Intervals are pointwise 95% percentile intervals from 5,000 race-stratified bootstrap replicates and are not threshold-by-threshold significance tests. FPR and FNR ratios use the White rate as the denominator. Primary $t^*$ denotes the common threshold minimizing the prespecified per-defendant aggregate loss at the displayed $\lambda$. Aggregate loss is $[\lambda FP+(1-\lambda)FN]/N$ in sample C; group-specific weighted error loss uses the same expression within each group. Lambda is a sensitivity parameter, not an estimate of social harm. Bootstrap membership is the share of replicates in which the displayed threshold belonged to the complete minimizing set; tied minimizers mean frequencies across thresholds need not sum to 100%.

</div>

</div>

<figure id="fig:threshold-consequences">
<embed src="figure3.pdf" style="width:97.0%" />
<figcaption>Consequences of moving the common threshold. Panels show group-specific FPR, FNR, higher-risk classification rate, and PPV for thresholds <span class="math inline"><em>t</em> = 1, …, 11</span>. The same threshold is applied to both groups. Endpoints are retained even when PPV or NPV is undefined because no one or everyone is classified higher risk.</figcaption>
</figure>

## Error-rate disparities persist across nondegenerate thresholds

Across the interior threshold range, the signed FPR gap remained positive and the FNR gap remained negative, indicating that Black defendants experienced higher false-positive rates while White defendants experienced higher false-negative rates under the same common threshold. Pointwise bootstrap intervals for both gaps remained separated from zero across all interior thresholds ($t=2,\ldots,10$) (Figure <a href="#fig:gaps" data-reference-type="ref" data-reference="fig:gaps">4</a>).

PPV differences were considerably smaller and less stable. Around the central thresholds, the Black-minus-White PPV gap approached zero, and several pointwise bootstrap intervals crossed zero. This combination—similar ranking discrimination and comparatively small predictive-value differences alongside much larger error-rate differences—illustrates why no single performance statistic determines how classification errors are distributed.

<figure id="fig:gaps">
<embed src="figure4.pdf" />
<figcaption>Signed Black-minus-White metric gaps across common thresholds. Panels show FPR, FNR, and PPV gaps with pointwise 95% bootstrap intervals. The horizontal line marks zero. Intervals are descriptive and are not simultaneous or multiple-testing-adjusted.</figcaption>
</figure>

## The loss-minimizing threshold depends strongly on error valuation

The location of the aggregate loss-minimizing threshold changed sharply with the prespecified error weighting. When false negatives were weighted three times as heavily as false positives ($\lambda=0.25$), the aggregate per-defendant loss was minimized at $t=2$. Under equal weighting ($\lambda=0.50$), the optimum moved to $t=6$. When false positives received three times the weight of false negatives ($\lambda=0.75$), the optimum moved to $t=10$ (Table <a href="#tab:threshold-cost-results" data-reference-type="ref" data-reference="tab:threshold-cost-results">2</a>; Figure <a href="#fig:cost" data-reference-type="ref" data-reference="fig:cost">5</a>).

These optima were also relatively stable under defendant-level bootstrap resampling. The displayed threshold belonged to the complete minimizing set in 99.62%, 90.92%, and 87.70% of replicates at $\lambda=0.25,0.50,$ and $0.75$, respectively. The focal optima were therefore comparatively stable under the prespecified defendant-level bootstrap.

As a prespecified population robustness check, the focal aggregate optima were unchanged in sample R ($t^*=2,6,10$ at $\lambda=0.25,0.50,0.75$); the complete sample R and sample C minimizing sets differed at only 5 of 101 grid weights, each by one adjacent threshold.

Aggregate optimality also did not imply equal modeled burden across groups. At the equal-weight optimum ($t=6$), for example, group-specific weighted error loss was 0.1791 for Black defendants and 0.1612 for White defendants. At $\lambda=0.75$ and $t=10$, the corresponding values were 0.1252 and 0.0996. These quantities are sensitivity measures rather than estimates of social harm, but they show that minimizing aggregate loss and evaluating its distribution across groups are distinct questions.

<figure id="fig:cost">
<embed src="figure5.pdf" />
<figcaption>Cost sensitivity and conditional optima. Panel A maps per-defendant aggregate weighted error loss over <span class="math inline"><em>λ</em></span> and the common threshold. Panel B shows the complete minimizing set at every grid weight. Panel C shows group-specific weighted error loss at the focal aggregate optima. The loss is a sensitivity device, not a measure of realized social harm.</figcaption>
</figure>

# Discussion: Institutional Accountability

The empirical results locate a consequential institutional choice between model output and public action. COMPAS supplies a score, but a classification rule also requires a threshold, an account of the relative importance assigned to different errors, and a specification of what consequence the classification may influence. The analysis does not identify a legally or morally correct rule. It shows that these institutional choices change both the decision rule and the distribution of its errors. Accountability must therefore extend beyond evaluation of the score to the institution’s conversion of that score into a consequential decision rule (Table <a href="#tab:accountability-framework" data-reference-type="ref" data-reference="tab:accountability-framework">3</a>).

## Prediction does not determine the decision rule

A risk score orders or differentiates cases; it does not contain within itself the socially legitimate point at which a person should be classified as higher risk. That additional step is sometimes obscured when a threshold is presented as though it were a technical property of the model. In practice, the threshold is a policy input that determines which scores trigger a category and, potentially, an adverse consequence.

Figure <a href="#fig:cost" data-reference-type="ref" data-reference="fig:cost">5</a> makes this distinction concrete. When false negatives receive three times the weight of false positives, the aggregate loss-minimizing common threshold is $t=2$. Equal weighting moves the optimum to $t=6$, while assigning three times the weight to false positives moves it to $t=10$. The $\lambda$ values in this analysis are sensitivity parameters, not empirical estimates of the social harms caused by either error. They nevertheless demonstrate that different prespecified objectives can yield sharply different decision rules from the same scores.

An optimizing procedure can therefore answer a conditional question: given a specified population, outcome, loss function, and error weighting, which threshold minimizes the stated objective? It cannot determine which objective a public institution ought to adopt. The relevant distinction is between a threshold that is **optimal conditional on a chosen objective** and one that is **objectively optimal**. The analysis supports the former claim only. Responsibility for selecting the objective, threshold, and permitted consequence remains with the institution using the score.

## Similar predictive performance does not settle error allocation

The near-equality of Black and White ROC AUC values does not conflict with the much larger FPR and FNR gaps observed after a common threshold is imposed. AUC answers a ranking question: how well does the score distinguish observed rearrest outcomes across pairs of cases? PPV answers a different threshold-specific question: among those classified as higher risk, what proportion are observed to rearrest? FPR and FNR instead describe the two directions in which the resulting classification rule is wrong, conditional on the observed outcome.

These quantities are not substitutes. In this analysis, the Black-minus-White AUC difference was $-0.0013$. The PPV gaps at $t=5$ and $t=8$ were $+3.84$ and $+1.64$ percentage points, while the corresponding FPR and FNR gaps were much larger. At $t=5$, the FPR gap was $+21.39$ percentage points and the FNR gap was $-19.74$ percentage points; at $t=8$, they remained $+10.38$ and $-18.79$ percentage points. Similar discrimination and comparatively small predictive-value differences can therefore coexist with a substantially different allocation of false positives and false negatives once an institution chooses a threshold.

This pattern does not make AUC or PPV unimportant, nor does it establish that any single error-rate parity criterion must control. It shows that each metric answers a different question and that reporting one cannot resolve the institutional choice represented by the others. The result is consistent with, and gives an institutional illustration of, the incompatibility arguments developed by Chouldechova (2017) and Kleinberg, Mullainathan, and Raghavan (2017). Trade-offs among fairness criteria are not proof that evaluation is impossible, but they require the institution to identify and justify the criterion it uses.

## Aggregate optimality is not distributive legitimacy

Even after an error weighting has been specified, minimizing aggregate loss does not determine whether the resulting distribution across groups is acceptable. At $\lambda=0.50$ and $t=6$, aggregate loss is minimized while group-specific weighted error loss is 0.1791 for Black defendants and 0.1612 for White defendants. At $\lambda=0.75$ and $t=10$, the corresponding losses are 0.1252 and 0.0996. The same objective used to select the common threshold therefore produces different modeled error burdens across the two focal groups.

These quantities should not be read as measurements of realized social harm. They are weighted-error sensitivity measures constructed from false positives and false negatives in the observed data. Their value is diagnostic: they make visible a distributional consequence that an aggregate objective alone can conceal. A threshold can minimize the specified total loss without equalizing, or otherwise legitimating, the modeled weighted error loss within each group.

Optimization selects a threshold according to a specified objective; it does not legitimate the distribution produced by that objective. An institution cannot treat aggregate minimization as a complete answer to a distributive question. It must also disclose the group-specific consequences of the chosen rule and explain why both the objective and the resulting distribution are acceptable for the decision context.

## From model evaluation to institutional accountability

Table <a href="#tab:accountability-framework" data-reference-type="ref" data-reference="tab:accountability-framework">3</a> translates these findings into four proposed minimum procedural obligations when an institution converts a risk score into a consequential decision rule. First, **decision specification** requires the institution to identify the outcome, horizon, deployment population, score and version, threshold, permitted consequence, and decision authority. Without that record, neither the rule nor responsibility for it is fully specified. Second, **error accounting** requires more than a single performance statistic: it should report FPR, FNR, PPV, subgroup gaps, uncertainty, threshold sensitivity, and relevant local validation.

Third, **institutional justification** requires an answer to the questions the optimization cannot resolve. The institution should explain why the selected threshold is appropriate, how false-positive and false-negative harms were weighted, what alternatives were considered, and what evidence would trigger revision or suspension. The sensitivity analysis can expose the consequences of alternative weights; it cannot supply the public justification for choosing one.

Fourth, **individual contestability** preserves a route for an affected person to challenge incorrect inputs, model applicability, the score or version used, the applied threshold, the interpretation of the score, the resulting adverse consequence, and the reasons offered by the decision-maker. Group-level probabilities and aggregate optimization do not settle an individual case. Human involvement alone is insufficient if the reviewer cannot inspect the relevant information, give independent reasons, or remedy an error.

This framework does not solve algorithmic fairness or establish legal compliance, causation, or the legitimacy of any threshold, weighting, or consequence. It specifies a minimum institutional record for disclosing, auditing, justifying, and contesting those choices. Under this framework, an institution that turns a score into a decision rule remains responsible for the choices that the model and data do not make.

<div class="threeparttable">

<div id="tab:accountability-framework">

| Module                          | Institution must specify or disclose                                                                 | What this analysis illustrates                                                                                                               |
|:--------------------------------|:-----------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|
| **Decision specification**      | Outcome, horizon, population, score/version, threshold, permitted consequence, decision authority    | Threshold is a policy input, not an inherent property of the score                                                                           |
| **Error accounting**            | FPR/FNR/PPV, subgroup gaps, uncertainty, threshold sensitivity, local validation                     | Small AUC/PPV differences can coexist with much larger FPR/FNR gaps                                                                          |
| **Institutional justification** | Why this threshold? How are FP and FN harms weighted? What alternatives were considered?             | Changing FP/FN weights shifts the aggregate optimum from $t^*=2$ at $\lambda=.25$, to $t^*=6$ at $\lambda=.50$, to $t^*=10$ at $\lambda=.75$ |
| **Individual contestability**   | Challenge inputs, applicability, score/version/threshold, use of score, adverse consequence, reasons | Group-level probabilities and aggregate optimization do not settle an individual case                                                        |

Operational accountability framework for threshold-based algorithmic decisions

</div>

<div class="tablenotes">

*Note.* This framework translates the descriptive findings into operational disclosure, justification, and review questions. It does not by itself establish legal compliance, causation, or the legitimacy of any particular threshold or error weighting. AUC denotes area under the receiver operating characteristic curve; FPR, FNR, PPV, FP, and FN denote false-positive rate, false-negative rate, positive predictive value, false positives, and false negatives. The displayed $t^*$ values are the common thresholds minimizing the prespecified per-defendant aggregate loss at each displayed $\lambda$.

</div>

</div>

# Limitations

First, the outcome is observed two-year rearrest, not true offending or a complete measure of recidivism. Rearrest is shaped by policing intensity, surveillance, reporting, charging, and record-linkage processes, so the label may reflect institutional practices as well as underlying conduct. ProPublica’s audit also estimated a 3.75% record-matching error rate, with an interval of approximately $\pm1.8$ percentage points (Larson et al. 2016). The reported metrics therefore describe the score’s relationship to the observed rearrest label, not its accuracy against an unobserved ground truth of offending.

Second, the data are historical and local. They concern defendants in Broward County, Florida, scored principally in 2013–2014, and cannot establish current performance in Broward County, performance in other jurisdictions, or the behavior of other risk instruments. The public data contain recorded scores and outcomes but not the complete proprietary COMPAS formula, training data, or institutional implementation rules. This study evaluates the available historical outputs; it is not an audit of the current COMPAS system or of contemporary deployment practice.

Third, the source categories `African-American` and `Caucasian`, displayed here as Black and White, are recorded administrative labels rather than self-identified racial identities. The primary comparison omits inferential analysis for smaller recorded groups and does not address intersectional patterns. Moreover, the reported gaps are descriptive associations among recorded race, scores, and observed outcomes. They do not identify a causal effect of race or isolate the mechanisms that produced the differences.

Fourth, the threshold sweep is an analytical sensitivity exercise rather than a reconstruction of historical deployment. Applying common thresholds $t=1,\ldots,11$ shows how classification consequences would change under alternative rules; it does not claim that Broward County judges or agencies actually used each threshold, used the score as a binding binary classifier, or attached a particular consequence to every higher-risk classification. Because COMPAS scores are discrete, only a finite set of common thresholds is available, and neighboring values of $\lambda$ may therefore yield the same minimizing threshold set. The results characterize the implications of specified rules, not the decisions of particular officials.

Fifth, $\lambda$ is a prespecified sensitivity parameter, not a measured social-welfare weight. The movement of the aggregate optimum from $t=2$ to $t=6$ to $t=10$ demonstrates dependence on the stated objective, but it does not show that any $\lambda$ is legally, morally, or institutionally appropriate. The loss function does not monetize individual harm, and group-specific weighted error loss is not realized social harm. More generally, neither an aggregate optimum nor any single performance metric settles institutional legitimacy.

Finally, the 5,000-replicate race-stratified defendant-level bootstrap captures sampling variation conditional on the observed dataset, prespecified analysis, and specified resampling scheme. It does not incorporate systematic label bias, record-linkage error, model drift, policy change, uncertainty about institutional use, or external-validity uncertainty. The reported metric-gap intervals are pointwise rather than simultaneous, and optimal-threshold membership frequencies measure stability under this resampling scheme rather than total uncertainty about the decision rule.

# Conclusion

This study examined how a common COMPAS threshold redistributes false-positive and false-negative errors across groups in historical Broward County data. Black and White defendants had nearly identical ranking discrimination and comparatively small PPV differences, yet common classification thresholds produced much larger and oppositely signed FPR and FNR gaps. Moving the threshold changed the levels and allocation of these errors rather than making the distributive question disappear. Similar discrimination and comparatively small PPV differences therefore did not determine the error consequences of the resulting decision rule.

The cost-sensitivity analysis sharpened this result. With $\lambda$, the prespecified weight on false positives, set to 0.25, 0.50, and 0.75, the aggregate loss-minimizing thresholds were $t=2,6,$ and $10$, respectively, and the focal optima were comparatively stable under the prespecified bootstrap. These are conditional optima under specified objectives, not morally correct thresholds or estimates of social welfare. The same scores can support sharply different rules depending on how false-positive and false-negative errors are valued.

Statistical analysis can describe those consequences, quantify sampling uncertainty, and identify the threshold that minimizes a stated objective. It cannot choose the objective, determine the permitted consequence, or legitimate the resulting distribution across groups. Accountability therefore requires an institution using a risk score to specify its decision rule, account for multiple error metrics and their uncertainty, justify its threshold and error weighting, and preserve meaningful individual contestability. Aggregate optimization cannot substitute for institutional justification.

The contribution is consequently narrower than a general solution to algorithmic fairness: it locates responsibility at the point where prediction is converted into action. Once a score becomes a rule with consequences, responsibility for the choices between prediction and action remains with the institution using it.

# Supplemental robustness figures

<figure id="fig:supp-bootstrap">
<embed src="supplement_bootstrap_optimal_membership.pdf" style="width:82.0%" />
<figcaption>Bootstrap minimizing-set membership frequencies at the three focal error weights. A replicate may have tied minimizers, so threshold membership frequencies at a given weight need not sum to 100%.</figcaption>
</figure>

<figure id="fig:supp-loss">
<embed src="supplement_robustness_optimal_thresholds.pdf" style="width:82.0%" />
<figcaption>Complete loss-minimizing threshold sets under the per-defendant primary loss and the class-conditional robustness loss across the full <span class="math inline"><em>λ</em></span> grid. Hollow and crossed markers preserve coincident minimizers.</figcaption>
</figure>

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-angwin2016" class="csl-entry">

Angwin, Julia, Jeff Larson, Surya Mattu, and Lauren Kirchner. 2016. “Machine Bias.” ProPublica. <https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing>.

</div>

<div id="ref-chouldechova2017" class="csl-entry">

Chouldechova, Alexandra. 2017. “Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments.” *Big Data* 5 (2): 153–63. <https://doi.org/10.1089/big.2016.0047>.

</div>

<div id="ref-dieterich2016" class="csl-entry">

Dieterich, William, Christina Mendoza, and Tim Brennan. 2016. “COMPAS Risk Scales: Demonstrating Accuracy Equity and Predictive Parity.” Northpointe Inc. Research Department. <https://www.documentcloud.org/documents/2998391-ProPublica-Commentary-Final-070616/>.

</div>

<div id="ref-flores2016" class="csl-entry">

Flores, Anthony W., Kristin Bechtel, and Christopher T. Lowenkamp. 2016. “False Positives, False Negatives, and False Analyses: A Rejoinder to ‘Machine Bias: There’s Software Used Across the Country to Predict Future Criminals. And It’s Biased Against Blacks.’” *Federal Probation* 80 (2): 38–46. <https://www.uscourts.gov/sites/default/files/80_2_6_0.pdf>.

</div>

<div id="ref-kleinberg2017" class="csl-entry">

Kleinberg, Jon, Sendhil Mullainathan, and Manish Raghavan. 2017. “Inherent Trade-Offs in the Fair Determination of Risk Scores.” In *8th Innovations in Theoretical Computer Science Conference*, 67:43:1–23. Leibniz International Proceedings in Informatics. <https://doi.org/10.4230/LIPIcs.ITCS.2017.43>.

</div>

<div id="ref-larson2016" class="csl-entry">

Larson, Jeff, Surya Mattu, Lauren Kirchner, and Julia Angwin. 2016. “How We Analyzed the COMPAS Recidivism Algorithm.” ProPublica. <https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm>.

</div>

<div id="ref-loomis2016" class="csl-entry">

Wisconsin Supreme Court. 2016. “State v. Loomis.” <https://www.wicourts.gov/sc/opinion/DisplayDocument.pdf?content=pdf&seqNo=171690>.

</div>

</div>
