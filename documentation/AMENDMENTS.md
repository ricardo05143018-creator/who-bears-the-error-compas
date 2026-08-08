# Protocol amendments

No substantive amendments were made to COMPAS Research Protocol v1.0.

The Sample R aggregate-cost calculation was a prespecified population
robustness check in the protocol. Its implementation and the corresponding
`population_robustness.csv` output complete that planned check; they do not
change the estimand or add a post hoc analysis. The public script uses a neutral
build date and contains no hard-coded expected substantive optimum.

One terminology clarification applies to Section 7.1 of the frozen protocol.
The phrase "signed absolute differences" is internally inconsistent; the
displayed formulas and the implemented estimand are signed Black-minus-White
differences. The manuscript uses "signed differences" throughout. This corrects
the label only and does not alter a formula, computation, or result.
