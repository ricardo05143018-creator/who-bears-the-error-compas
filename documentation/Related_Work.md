# 2. Background and Related Work

## 2.1 The COMPAS dispute and competing empirical interpretations

The public COMPAS debate began from a disagreement about what property of a risk instrument should count as evidence of fair performance. ProPublica examined Broward County defendants with two years of follow-up and reported sharply different directions of error at the Low versus Medium/High cutoff: Black defendants who were not rearrested were classified above Low more often than White defendants, while White defendants who were rearrested were classified Low more often than Black defendants (Angwin et al., 2016; Larson et al., 2016). Northpointe's response disputed ProPublica's interpretation and organized its defense around accuracy equity and predictive parity, while also objecting to aspects of the cutoff and error analysis (Dieterich, Mendoza, and Brennan, 2016).

Flores, Bechtel, and Lowenkamp (2016) offered a related but distinct reanalysis. Using the decile score and a more restricted analytical sample, they reported AUC values of 0.69 for White defendants and 0.70 for Black defendants, with no statistically significant difference, and observed rearrest rates that were close across the two groups within the broad Low, Medium, and High categories. They also emphasized that converting a three-category instrument into a binary classifier requires a binning decision. The two binning rules they examined changed false-positive and false-negative rates in opposite directions.

These analyses use different samples in places and answer different statistical questions. Similar ranking discrimination or outcome rates within broad score categories can coexist with unequal classification-error rates after a cutoff is imposed. This study reports AUC, PPV, FPR, and FNR separately, reproduces the published contingency table, and treats the threshold as an explicit analytical input.

## 2.2 Different metrics answer different questions

The relevant measures condition on different events. ROC AUC describes how often a randomly selected rearrested defendant receives a higher score than a randomly selected non-rearrested defendant, counting a score tie as one-half. It is a ranking measure and does not require a particular threshold. Positive predictive value instead conditions on the higher-risk classification and asks what share of those classified higher risk were observed to be rearrested. False-positive and false-negative rates condition on the observed outcome and distinguish the two directions of error.

Because the denominators differ, parity on one measure does not imply parity on another. AUC concerns the ordering produced by the score; PPV concerns the composition of a selected category; FPR and FNR concern the two directions of classification error. Each measure can inform a different part of an institutional decision.

## 2.3 Calibration, predictive parity, and incompatibility

Chouldechova (2017) formalized the relationship among prevalence, predictive parity, and classification-error rates. When observed outcome prevalence differs across groups, equal PPV at a threshold is generally incompatible with equal FPR and FNR unless prediction is perfect. Her COMPAS illustration also showed that approximate calibration or predictive parity can coexist with error-rate imbalance. The result explains why ProPublica and its critics could emphasize different, statistically defensible properties of the same data.

Kleinberg, Mullainathan, and Raghavan (2017) established a related score-level result. They considered calibration within groups, balance for the negative class, and balance for the positive class, and showed that all three can be satisfied together only in constrained cases: perfect prediction or equal base rates. Their balance conditions are score-level conditions, not identical to threshold-specific FPR and FNR parity, although they generalize the same concern about differential treatment of positive and negative classes.

Kleinberg and colleagues expressly declined to recommend how conflicts among fairness definitions should be resolved, while Chouldechova distinguished statistical criteria from the social and ethical judgment of fairness. The incompatibility results provide context for this study's threshold comparisons; choosing an institutional objective remains a separate judgment.

## 2.4 From a score to a decision rule

The distinction between a score and a rule is already visible in the early COMPAS exchange. Flores, Bechtel, and Lowenkamp (2016) observed that a multicategory score must be binned before contingency-table measures can be calculated. They showed that placing Medium with High lowers one type of error and raises another relative to placing Medium with Low, and noted that different users could prefer different trade-offs. ProPublica likewise reported its main Low-versus-Medium/High table and a High-only sensitivity check (Larson et al., 2016).

Those comparisons show that the threshold matters. This study extends them by evaluating every common decile threshold, reporting uncertainty across the resulting metric curves, and showing how the loss-minimizing threshold changes with the relative error weight. It audits the choices required to turn an existing score into a common binary rule.

## 2.5 Institutional use and contestability

The legal controversy surrounding COMPAS also illustrates why predictive evaluation does not settle legitimate use. In *State v. Loomis*, the Wisconsin Supreme Court held that a sentencing court's consideration of COMPAS did not violate due process when the assessment was used with the limitations and cautions specified in the opinion (2016 WI 68, paras. 98-100, 120). The holding was narrow. The court said that a risk score could not determine incarceration or sentence severity, could not be the determinative factor in deciding whether community supervision was safe and effective, and had to be accompanied by a written advisement addressing the proprietary model, group-based inference, possible racial disparity, the absence of Wisconsin cross-validation at the time, and the need for continuing monitoring. The court also stressed that the sentencing judge had relied on independent factors and stated that the sentence would have been the same without COMPAS (paras. 104-109).

Within that jurisdiction and procedural setting, *Loomis* shows that the authority given to a score depends on its permitted consequence, the reasons independently supporting the decision, the warnings supplied to the decision-maker, and the opportunity to review and challenge relevant information. These concerns inform the accountability framework proposed here.

Prior work explains competing metrics, demonstrates incompatibilities, and identifies legal cautions around institutional use. The analysis below adds a full common-threshold sweep, uncertainty estimates, and prespecified error-weight comparisons to show how the choice of a decision rule redistributes observed errors.
