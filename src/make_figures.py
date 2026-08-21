"""
Generate the figures used in the COMPAS paper
Date: August 2026
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.prepare_data import load_and_prepare


TABLE_DIR = os.path.join(PROJECT_ROOT, "output", "tables")
FIGURE_DIR = os.path.join(PROJECT_ROOT, "output", "figures")
PANEL_DIR = os.path.join(FIGURE_DIR, "panels")
GROUPS = ("Black", "White")
FOCAL_LAMBDAS = (0.25, 0.50, 0.75)
THRESHOLDS = tuple(range(1, 12))

EXPECTED_PANELS = (
    "figure1_t5_error_rates",
    "figure2a_score_distribution",
    "figure2b_rearrest_by_score",
    "figure3a_fpr_by_threshold",
    "figure3b_fnr_by_threshold",
    "figure3c_selection_by_threshold",
    "figure3d_ppv_by_threshold",
    "figure4a_fpr_gap",
    "figure4b_fnr_gap",
    "figure4c_ppv_gap",
    "figure5a_primary_loss_surface",
    "figure5b_primary_optimal_threshold_map",
    "figure5c_group_loss_at_focal_optima",
    "supplement_bootstrap_optimal_membership",
    "supplement_robustness_optimal_thresholds",
)
EXPECTED_PAPER_FIGURES = (
    "figure1",
    "figure2",
    "figure3",
    "figure4",
    "figure5",
    "supplement_bootstrap_optimal_membership",
    "supplement_robustness_optimal_thresholds",
)


def require_columns(table, table_name, columns):
    missing = sorted(set(columns) - set(table.columns))
    if missing:
        raise RuntimeError(f"{table_name} is missing columns: {missing}")


def one_row(table, table_name, **filters):
    mask = pd.Series(True, index=table.index)
    for column, value in filters.items():
        mask &= table[column] == value
    rows = table.loc[mask]
    if len(rows) != 1:
        raise RuntimeError(
            f"Expected one row in {table_name} for {filters}; found {len(rows)}."
        )
    return rows.iloc[0]


def bootstrap_interval(intervals, threshold, metric):
    rows = intervals[
        (intervals["threshold"].astype(str) == str(threshold))
        & (intervals["metric"] == metric)
    ]
    if len(rows) != 1:
        raise RuntimeError(
            f"Expected one bootstrap row for threshold={threshold}, "
            f"metric={metric}; found {len(rows)}."
        )
    row = rows.iloc[0]
    return float(row["ci_lower"]), float(row["ci_upper"])


def save_figure(fig, *targets):
    fig.tight_layout()
    for directory, stem in targets:
        os.makedirs(directory, exist_ok=True)
        fig.savefig(os.path.join(directory, f"{stem}.pdf"), bbox_inches="tight")
        fig.savefig(
            os.path.join(directory, f"{stem}.png"),
            dpi=300,
            bbox_inches="tight",
        )
    plt.close(fig)


def mark_reference_ticks(ax):
    labels = [str(x) for x in THRESHOLDS]
    labels[4] = "5\nLow vs.\nMed/High"
    labels[7] = "8\nHigh\nonly"
    ax.set_xticks(THRESHOLDS)
    ax.set_xticklabels(labels)


def mark_panel(ax, label):
    ax.text(
        -0.10,
        1.06,
        label,
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold",
        va="top",
    )


def validate_tables(sweep, calibration, intervals, optfreq, cost):
    require_columns(
        sweep,
        "threshold_sweep_results.csv",
        {"group", "threshold", "fpr", "fnr", "ppv", "selection_rate"},
    )
    for group in (*GROUPS, "Gap (Black - White)"):
        rows = sweep[sweep["group"] == group]
        if len(rows) != 11 or rows["threshold"].duplicated().any():
            raise RuntimeError(f"Threshold sweep is incomplete for group={group}.")
        if set(rows["threshold"].astype(int)) != set(THRESHOLDS):
            raise RuntimeError(
                f"Threshold sweep has unexpected thresholds for group={group}."
            )

    require_columns(
        calibration,
        "calibration_diagnostics.csv",
        {"score", "q_black", "q_white", "n_black", "n_white"},
    )
    if len(calibration) != 10 or calibration["score"].duplicated().any():
        raise RuntimeError("calibration_diagnostics.csv must contain one row per score.")
    if set(calibration["score"].astype(int)) != set(range(1, 11)):
        raise RuntimeError("calibration_diagnostics.csv must contain scores 1 through 10.")

    require_columns(
        intervals,
        "bootstrap_intervals.csv",
        {"threshold", "metric", "ci_lower", "ci_upper"},
    )
    if len(intervals) != 364:
        raise RuntimeError(
            f"bootstrap_intervals.csv must have 364 rows; found {len(intervals)}."
        )
    required_auc = {
        "AUC (Black)",
        "AUC (White)",
        "AUC (Sample R)",
        "AUC Gap (B-W)",
    }
    for metric in required_auc:
        if (intervals["metric"] == metric).sum() != 1:
            raise RuntimeError(f"Expected one bootstrap interval for {metric}.")

    require_columns(
        optfreq,
        "bootstrap_optimal_threshold_frequencies.csv",
        {"lambda", "threshold", "membership_frequency"},
    )
    if len(optfreq) != 33 or optfreq.duplicated(["lambda", "threshold"]).any():
        raise RuntimeError(
            "bootstrap_optimal_threshold_frequencies.csv must have 33 unique rows."
        )
    for lmbda in FOCAL_LAMBDAS:
        rows = optfreq[np.isclose(optfreq["lambda"], lmbda)]
        if len(rows) != 11 or set(rows["threshold"].astype(int)) != set(THRESHOLDS):
            raise RuntimeError(
                f"Optimal-threshold frequencies are incomplete for lambda={lmbda}."
            )

    require_columns(
        cost,
        "deterministic_cost_grid.csv",
        {
            "lambda",
            "threshold",
            "L_t_Sample_C",
            "L_g_Black",
            "L_g_White",
            "is_primary_minimizer",
            "is_robustness_minimizer",
        },
    )
    if len(cost) != 1111 or cost.duplicated(["lambda", "threshold"]).any():
        raise RuntimeError(
            f"deterministic_cost_grid.csv must have 1111 unique rows; found {len(cost)}."
        )
    if cost["lambda"].nunique() != 101 or set(
        cost["threshold"].astype(int)
    ) != set(THRESHOLDS):
        raise RuntimeError("deterministic_cost_grid.csv has an incomplete grid.")
    for flag in ("is_primary_minimizer", "is_robustness_minimizer"):
        if not cost.groupby("lambda")[flag].any().all():
            raise RuntimeError(f"At least one lambda has no {flag}.")


def check_figure_outputs():
    missing = []
    for directory, stems in (
        (PANEL_DIR, EXPECTED_PANELS),
        (FIGURE_DIR, EXPECTED_PAPER_FIGURES),
    ):
        for stem in stems:
            for extension in ("pdf", "png"):
                path = os.path.join(directory, f"{stem}.{extension}")
                if not os.path.isfile(path):
                    missing.append(path)
    if missing:
        raise RuntimeError(f"Figure generation is incomplete: {missing}")


def plot_t5_error_rates(ax, sweep, intervals):
    metrics = (("fpr", "FPR"), ("fnr", "FNR"), ("ppv", "PPV"))
    x = np.arange(len(metrics))
    for offset, group in zip((-0.08, 0.08), GROUPS):
        points, lower_errors, upper_errors = [], [], []
        row = one_row(
            sweep,
            "threshold_sweep_results.csv",
            group=group,
            threshold=5,
        )
        for key, _ in metrics:
            point = float(row[key])
            lower, upper = bootstrap_interval(intervals, 5, f"{key} ({group})")
            points.append(point)
            lower_errors.append(point - lower)
            upper_errors.append(upper - point)
        ax.errorbar(
            x + offset,
            points,
            yerr=[lower_errors, upper_errors],
            fmt="o",
            capsize=4,
            label=group,
        )
    ax.set_xticks(x)
    ax.set_xticklabels([label for _, label in metrics])
    ax.set_ylabel("Rate")
    ax.set_ylim(0, 0.75)
    ax.set_title("Error and predictive-value rates at the t = 5 cutoff")
    ax.legend(frameon=False)


def plot_score_distribution(ax, prepared):
    for recorded_race, label in (
        ("African-American", "Black"),
        ("Caucasian", "White"),
    ):
        scores = prepared.loc[prepared["race"] == recorded_race, "score"]
        proportions = (
            scores.value_counts(normalize=True)
            .sort_index()
            .reindex(range(1, 11), fill_value=0)
        )
        ax.plot(proportions.index, proportions.values, marker="o", label=label)
    ax.set_xticks(range(1, 11))
    ax.set_xlabel("COMPAS general-recidivism decile score")
    ax.set_ylabel("Within-group proportion")
    ax.set_title("Distribution of COMPAS decile scores by recorded race")
    ax.legend(frameon=False)


def plot_rearrest_by_score(ax, calibration, intervals):
    for group, q_column in (("Black", "q_black"), ("White", "q_white")):
        points, lower_errors, upper_errors = [], [], []
        for _, row in calibration.iterrows():
            score_label = f"Score_{int(row['score'])}"
            lower, upper = bootstrap_interval(
                intervals,
                score_label,
                f"Calibration ({group})",
            )
            point = float(row[q_column])
            points.append(point)
            lower_errors.append(point - lower)
            upper_errors.append(upper - point)
        ax.errorbar(
            calibration["score"],
            points,
            yerr=[lower_errors, upper_errors],
            marker="o",
            capsize=3,
            label=group,
        )
    ticklabels = [
        f"{int(score)}\n{int(n_black)}/{int(n_white)}"
        for score, n_black, n_white in zip(
            calibration["score"],
            calibration["n_black"],
            calibration["n_white"],
        )
    ]
    ax.set_xticks(calibration["score"])
    ax.set_xticklabels(ticklabels)
    ax.set_xlabel("COMPAS decile score\nBlack/White cell counts shown under each score")
    ax.set_ylabel("Observed two-year rearrest rate")
    ax.set_ylim(0, 1)
    ax.set_title("Observed two-year rearrest rate within each score")
    ax.legend(frameon=False)


def plot_consequence(ax, sweep, metric, ylabel):
    for group in GROUPS:
        rows = sweep[sweep["group"] == group].sort_values("threshold")
        ax.plot(rows["threshold"], rows[metric], marker="o", label=group)
    mark_reference_ticks(ax)
    ax.set_xlabel("Common threshold t (higher risk if score ≥ t)")
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, 1)
    ax.set_title(f"{ylabel} across common COMPAS thresholds")
    ax.legend(frameon=False)


def plot_gap(ax, gap, intervals, metric, interval_metric, ylabel):
    rows = gap.sort_values("threshold")
    points, lower_errors, upper_errors = [], [], []
    for _, row in rows.iterrows():
        threshold = int(row["threshold"])
        point = float(row[metric])
        lower, upper = bootstrap_interval(intervals, threshold, interval_metric)
        points.append(point)
        lower_errors.append(point - lower)
        upper_errors.append(upper - point)
    ax.errorbar(
        rows["threshold"],
        points,
        yerr=[lower_errors, upper_errors],
        marker="o",
        capsize=3,
    )
    ax.axhline(0, color="black", linewidth=0.8)
    mark_reference_ticks(ax)
    ax.set_xlabel("Common threshold t (higher risk if score ≥ t)")
    ax.set_ylabel(ylabel)
    ax.set_title(f"{ylabel} across thresholds\n95% pointwise bootstrap intervals")


def plot_loss_surface(fig, ax, cost):
    pivot = (
        cost.pivot(index="threshold", columns="lambda", values="L_t_Sample_C")
        .sort_index()
        .sort_index(axis=1)
    )
    image = ax.imshow(
        pivot.to_numpy(),
        aspect="auto",
        origin="lower",
        extent=[
            pivot.columns.min(),
            pivot.columns.max(),
            pivot.index.min() - 0.5,
            pivot.index.max() + 0.5,
        ],
    )
    ax.set_xlabel("False-positive weight λ")
    ax.set_ylabel("Common threshold t")
    ax.set_yticks(THRESHOLDS)
    ax.set_title("Aggregate weighted error loss across λ and threshold")
    fig.colorbar(image, ax=ax, label="Per-defendant weighted error loss")


def plot_primary_optima(ax, primary_minima):
    ax.scatter(primary_minima["lambda"], primary_minima["threshold"], s=18)
    ax.set_xlabel("False-positive weight λ")
    ax.set_ylabel("Loss-minimizing common threshold")
    ax.set_yticks(THRESHOLDS)
    ax.set_ylim(0.5, 11.5)
    ax.set_title("Complete aggregate loss-minimizing threshold set")


def focal_loss_rows(cost):
    records = []
    for lmbda in FOCAL_LAMBDAS:
        rows = cost[
            np.isclose(cost["lambda"], lmbda) & cost["is_primary_minimizer"]
        ]
        for _, row in rows.iterrows():
            records.append(
                {
                    "lambda": lmbda,
                    "threshold": int(row["threshold"]),
                    "Black": float(row["L_g_Black"]),
                    "White": float(row["L_g_White"]),
                }
            )
    return pd.DataFrame(records)


def plot_group_loss(ax, focal):
    x = np.arange(len(focal))
    width = 0.32
    ax.bar(x - width / 2, focal["Black"], width, label="Black")
    ax.bar(x + width / 2, focal["White"], width, label="White")
    ax.set_xticks(x)
    ax.set_xticklabels(
        [
            f"λ={row['lambda']:.2f}\noptimum t={int(row['threshold'])}"
            for _, row in focal.iterrows()
        ]
    )
    ax.set_ylabel("Group-specific weighted error loss")
    ax.set_title("Modeled error-loss distribution at focal aggregate optima")
    ax.legend(frameon=False)


def plot_bootstrap_membership(ax, optfreq):
    # membership frequencies can sum above 100% when a replicate has tied minimizers.
    for lmbda in FOCAL_LAMBDAS:
        rows = optfreq[np.isclose(optfreq["lambda"], lmbda)].sort_values("threshold")
        ax.plot(
            rows["threshold"],
            rows["membership_frequency"],
            marker="o",
            label=f"λ = {lmbda:.2f}",
        )
    ax.set_xticks(THRESHOLDS)
    ax.set_xlabel("Threshold")
    ax.set_ylabel("Bootstrap minimizing-set membership frequency")
    ax.set_ylim(0, 1.05)
    ax.set_title("Sampling stability of focal loss-minimizing thresholds")
    ax.legend(frameon=False)


def plot_robustness_optima(ax, primary_minima, robustness_minima):
    # hollow circles keep coincident primary and robustness minima visible.
    ax.scatter(
        primary_minima["lambda"],
        primary_minima["threshold"],
        s=28,
        facecolors="none",
        edgecolors="C0",
        linewidths=1.1,
        label="Per-defendant loss",
    )
    ax.scatter(
        robustness_minima["lambda"],
        robustness_minima["threshold"],
        s=22,
        color="C1",
        marker="x",
        linewidths=1.0,
        label="Class-conditional loss",
    )
    ax.set_xlabel("False-positive weight λ")
    ax.set_ylabel("Loss-minimizing threshold")
    ax.set_yticks(THRESHOLDS)
    ax.set_ylim(0.5, 11.5)
    ax.set_title("Robustness check: optimal threshold under two loss normalizations")
    ax.legend(frameon=False)


def main():
    sweep = pd.read_csv(os.path.join(TABLE_DIR, "threshold_sweep_results.csv"))
    calibration = pd.read_csv(os.path.join(TABLE_DIR, "calibration_diagnostics.csv"))
    intervals = pd.read_csv(os.path.join(TABLE_DIR, "bootstrap_intervals.csv"))
    optfreq = pd.read_csv(
        os.path.join(TABLE_DIR, "bootstrap_optimal_threshold_frequencies.csv")
    )
    cost = pd.read_csv(os.path.join(TABLE_DIR, "deterministic_cost_grid.csv"))
    validate_tables(sweep, calibration, intervals, optfreq, cost)

    # Figure 2A needs validated row-level scores rather than an aggregated output table.
    prepared = load_and_prepare()
    require_columns(prepared, "prepared COMPAS data", {"race", "score"})
    calibration = calibration.sort_values("score").reset_index(drop=True)
    black_white = sweep[sweep["group"].isin(GROUPS)].copy()
    gap = sweep[sweep["group"] == "Gap (Black - White)"].copy()
    # keep all flagged rows because one lambda can have multiple tied minimizers.
    primary_minima = cost[cost["is_primary_minimizer"]].copy()
    robustness_minima = cost[cost["is_robustness_minimizer"]].copy()
    focal = focal_loss_rows(cost)

    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    plot_t5_error_rates(ax, sweep, intervals)
    save_figure(
        fig,
        (PANEL_DIR, "figure1_t5_error_rates"),
        (FIGURE_DIR, "figure1"),
    )

    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    plot_score_distribution(ax, prepared)
    save_figure(fig, (PANEL_DIR, "figure2a_score_distribution"))

    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    plot_rearrest_by_score(ax, calibration, intervals)
    save_figure(fig, (PANEL_DIR, "figure2b_rearrest_by_score"))

    consequence_specs = (
        ("fpr", "False-positive rate", "figure3a_fpr_by_threshold"),
        ("fnr", "False-negative rate", "figure3b_fnr_by_threshold"),
        (
            "selection_rate",
            "Higher-risk classification rate",
            "figure3c_selection_by_threshold",
        ),
        ("ppv", "Positive predictive value", "figure3d_ppv_by_threshold"),
    )
    for metric, ylabel, stem in consequence_specs:
        fig, ax = plt.subplots(figsize=(7.2, 4.8))
        plot_consequence(ax, black_white, metric, ylabel)
        save_figure(fig, (PANEL_DIR, stem))

    gap_specs = (
        ("fpr", "fpr Gap (B-W)", "Black − White FPR gap", "figure4a_fpr_gap"),
        ("fnr", "fnr Gap (B-W)", "Black − White FNR gap", "figure4b_fnr_gap"),
        ("ppv", "ppv Gap (B-W)", "Black − White PPV gap", "figure4c_ppv_gap"),
    )
    for metric, interval_metric, ylabel, stem in gap_specs:
        fig, ax = plt.subplots(figsize=(7.2, 4.8))
        plot_gap(ax, gap, intervals, metric, interval_metric, ylabel)
        save_figure(fig, (PANEL_DIR, stem))

    fig, ax = plt.subplots(figsize=(8.0, 5.2))
    plot_loss_surface(fig, ax, cost)
    save_figure(fig, (PANEL_DIR, "figure5a_primary_loss_surface"))

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    plot_primary_optima(ax, primary_minima)
    save_figure(fig, (PANEL_DIR, "figure5b_primary_optimal_threshold_map"))

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    plot_group_loss(ax, focal)
    save_figure(fig, (PANEL_DIR, "figure5c_group_loss_at_focal_optima"))

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    plot_bootstrap_membership(ax, optfreq)
    save_figure(
        fig,
        (PANEL_DIR, "supplement_bootstrap_optimal_membership"),
        (FIGURE_DIR, "supplement_bootstrap_optimal_membership"),
    )

    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    plot_robustness_optima(ax, primary_minima, robustness_minima)
    save_figure(
        fig,
        (PANEL_DIR, "supplement_robustness_optimal_thresholds"),
        (FIGURE_DIR, "supplement_robustness_optimal_thresholds"),
    )

    # panels are replotted so the composite PDFs remain vector graphics.
    fig, axes = plt.subplots(1, 2, figsize=(15.0, 5.2))
    plot_score_distribution(axes[0], prepared)
    plot_rearrest_by_score(axes[1], calibration, intervals)
    for label, ax in zip("AB", axes):
        mark_panel(ax, label)
    save_figure(fig, (FIGURE_DIR, "figure2"))

    fig, axes = plt.subplots(2, 2, figsize=(14.0, 9.2))
    for label, ax, (metric, ylabel, _) in zip("ABCD", axes.flat, consequence_specs):
        plot_consequence(ax, black_white, metric, ylabel)
        mark_panel(ax, label)
    save_figure(fig, (FIGURE_DIR, "figure3"))

    fig, axes = plt.subplots(1, 3, figsize=(20.0, 5.0))
    for label, ax, (metric, interval_metric, ylabel, _) in zip(
        "ABC", axes, gap_specs
    ):
        plot_gap(ax, gap, intervals, metric, interval_metric, ylabel)
        mark_panel(ax, label)
    save_figure(fig, (FIGURE_DIR, "figure4"))

    fig, axes = plt.subplots(1, 3, figsize=(20.0, 5.2))
    plot_loss_surface(fig, axes[0], cost)
    plot_primary_optima(axes[1], primary_minima)
    plot_group_loss(axes[2], focal)
    for label, ax in zip("ABC", axes):
        mark_panel(ax, label)
    save_figure(fig, (FIGURE_DIR, "figure5"))

    check_figure_outputs()
    print(
        f"[FIGURES] Wrote {len(EXPECTED_PANELS)} panel pairs to {PANEL_DIR} "
        f"and {len(EXPECTED_PAPER_FIGURES)} paper-figure pairs to {FIGURE_DIR}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"\n[FATAL ERROR] {err}", file=sys.stderr)
        sys.exit(1)
