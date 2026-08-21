# COMPAS Working Paper Citation Audit

**Audit date:** 2026-08-21  
**Scope:** Introduction, Background/Related Work, Data and Methods, Discussion, Limitations, Conclusion, table notes, and bibliography.  
**Rule:** Empirical claims from this study are checked against canonical outputs; historical, literature, and legal claims are checked against primary or authoritative sources. Normative claims are identified as the paper's argument rather than attributed to a source.

| Claim | Location | Source checked | Support status | Action |
|---|---|---|---|---|
| ProPublica reported a 45% versus 23% FPR pattern and a 28% versus 48% FNR pattern at Low versus Medium/High. | Introduction; Related Work 2.1 | Larson et al. (2016), methodology, contingency tables; Angwin et al. (2016) | SUPPORTED | Retained and described as ProPublica's historical finding. |
| The published two-year error table used 7,214 defendants and the displayed counts 2681/1282/1216/2035, 990/805/532/1369, and 1139/349/461/505. | Methods; Results; Table 1 | Larson et al. (2016), contingency tables | SUPPORTED | Retained; independently reproduced by the pipeline. |
| Scores 1-4 were Low, 5-7 Medium, and 8-10 High. | Methods 3.3; table notes | Larson et al. (2016), data-acquisition description | SUPPORTED | Retained; mapping is also a tested pipeline invariant. |
| The records concern Broward County defendants scored principally in 2013-2014. | Methods 3.1 | Larson et al. (2016), data-acquisition description | SUPPORTED | Retained with "principally" because the file is a historical administrative extract. |
| Recorded race came from Broward County administrative records, not self-identification. | Methods 3.1-3.2; Limitations | Larson et al. (2016), race-data description | SUPPORTED WITH NARROWING | Manuscript calls the categories administrative labels and makes no identity or causal claim. |
| The outcome is observed arrest/rearrest within two years, not true offending. | Introduction; Methods; Limitations | Larson et al. (2016), outcome construction and matching process | SUPPORTED WITH NARROWING | Retained as a measurement limitation; "true offending" is explicitly described as unobserved. |
| Flores et al. found similar Black and White ranking discrimination. | Introduction; Related Work 2.1 | Flores, Bechtel, and Lowenkamp (2016), Table 1: AUC 0.69 White, 0.70 Black, no significant difference | SUPPORTED | Retained with the metric named as AUC/ranking discrimination. |
| Flores et al. found similar observed rearrest rates within broad risk categories. | Introduction; Related Work 2.1 | Flores et al. (2016), Table 1: Low 29/35, Medium 53/56, High 73/75 | SUPPORTED WITH NARROWING | "Calibration" was not used as a blanket label; prose says "approximately similar" and "broad categories." |
| Flores et al. showed that binning Medium with Low rather than High decreases FPR and increases FNR. | Related Work 2.4 | Flores et al. (2016), discussion of Tables 3-4 | SUPPORTED | Retained as evidence that threshold/binning choice changes error allocation. |
| Northpointe's response emphasized accuracy equity and predictive parity and disputed ProPublica's cutoff/error interpretation. | Related Work 2.1 | Dieterich, Mendoza, and Brennan (2016), original report; ProPublica technical response links the report and reproduces the disputed cutoff claims | SUPPORTED WITH NARROWING | Described as Northpointe's framing, not as proof that COMPAS is fair. |
| Predictive parity and equal FPR/FNR are generally incompatible when prevalence differs and prediction is imperfect. | Introduction; Related Work 2.3; Discussion 5.2 | Chouldechova (2017), equation and incompatibility argument | SUPPORTED | Retained; no claim that this paper reproves the result. |
| Calibration within groups, balance for the negative class, and balance for the positive class cannot all hold except in constrained cases. | Introduction; Related Work 2.3; Discussion 5.2 | Kleinberg, Mullainathan, and Raghavan (2017), Theorem 1 | SUPPORTED | Retained with the two exceptions named: perfect prediction or equal base rates. |
| Kleinberg's balance conditions are identical to threshold-specific FPR/FNR parity. | — | Kleinberg et al. (2017), definitions | UNSUPPORTED | Excluded. The manuscript says the score-level conditions are related but not identical. |
| The incompatibility theorems determine which fairness criterion an institution should choose. | — | Chouldechova (2017); Kleinberg et al. (2017) | UNSUPPORTED | Excluded. The manuscript states that the theorems do not choose an institutional objective. |
| *Loomis* approved COMPAS without qualification. | — | *State v. Loomis*, 2016 WI 68 | UNSUPPORTED | Excluded. The holding is described as jurisdiction- and use-specific and subject to limitations and cautions. |
| *Loomis* permitted COMPAS as one relevant factor but barred using it to determine incarceration or sentence severity or as the determinative community-supervision factor. | Related Work 2.5 | *State v. Loomis*, paras. 88-100 | SUPPORTED | Retained with the limited procedural context stated. |
| *Loomis* required a written advisement about proprietary operation, group data, disparity concerns, local validation, and monitoring. | Related Work 2.5 | *State v. Loomis*, paras. 65-66, 100-101 | SUPPORTED | Retained in compressed form without converting it into a general national rule. |
| The sentencing court in *Loomis* relied on independent factors and said the sentence would have been the same without COMPAS. | Related Work 2.5 | *State v. Loomis*, paras. 103-109 | SUPPORTED | Retained to explain why the case outcome does not establish broad approval. |
| AUC = 0.7022/0.6918/0.6931 and Black-minus-White AUC gap = -0.0013 with the reported bootstrap interval. | Results; Table 1 | `calibration_diagnostics.csv`; `bootstrap_intervals.csv`; frozen Table 1 | SUPPORTED | Retained; values match canonical outputs. |
| At t=5 and t=8, the stated FPR/FNR/PPV levels, gaps, confidence intervals, and ratios are correct. | Results; Table 2; Figures 1, 3, 4 | `threshold_sweep_results.csv`; `bootstrap_intervals.csv`; frozen Table 2 | SUPPORTED | Retained; no threshold is described as historically mandated. |
| FPR and FNR gap pointwise intervals exclude zero for all interior thresholds t=2,...,10. | Results 4.3 | `bootstrap_intervals.csv`; Figure 4 | SUPPORTED | Retained as a pointwise descriptive statement; no multiple-testing or simultaneous-CI claim. |
| The focal aggregate optima are t=2, 6, and 10 at lambda=.25, .50, and .75. | Introduction; Results; Discussion; Conclusion; Table 2; Figure 5 | `deterministic_cost_grid.csv` | SUPPORTED | Retained as conditional optima under the stated per-defendant loss. |
| Bootstrap optimal-set membership is 99.62%, 90.92%, and 87.70%. | Results; Table 2 | `bootstrap_optimal_threshold_frequencies.csv` | SUPPORTED | Retained; note states that tied membership frequencies need not sum to 100%. |
| Sample R and Sample C share the three focal optima and differ at 5 of 101 grid weights, each by one adjacent threshold. | Results 4.4; Methods robustness description | `population_robustness.csv`; `deterministic_cost_grid.csv` | SUPPORTED | Retained as the prespecified population robustness result, not as a new estimand. |
| Group-specific weighted error loss is realized social harm or welfare. | — | Protocol and loss definition | UNSUPPORTED | Excluded. It is consistently labeled a modeled sensitivity quantity. |
| The four accountability modules establish legal compliance. | Table 3 note; Discussion; Conclusion | Paper's normative argument; *Loomis* used only as a bounded illustration | UNSUPPORTED | Excluded. The framework is labeled a normative minimum and not a legal-compliance test. |

## Source disposition

- **Primary/authoritative sources retained:** ProPublica's investigation and methods; Northpointe's response; Flores et al.; Chouldechova; Kleinberg et al.; the official Wisconsin Supreme Court opinion in *State v. Loomis*.
- **Secondary summaries:** not used to support surviving historical, statistical-theorem, or legal claims.
- **Original Princeton-paper sources:** all six substantive sources were rechecked. No unsupported claim from the earlier essay was carried forward.

## Audit result

Every surviving externally verifiable claim is supported at the level stated or was narrowed to the source's actual scope. The paper's empirical claims match the canonical machine-readable outputs, and its institutional claims are presented as normative arguments rather than empirical or legal findings.
