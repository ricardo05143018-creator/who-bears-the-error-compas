"""
Phase 3 & 4: Full Bootstrap, Calibration CIs, and Comprehensive Cost Analysis.
Date: August 2026
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) != "src":
    raise RuntimeError("Place this script inside the project's src directory before running it.")

PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.append(PROJECT_ROOT)

from src.prepare_data import load_and_prepare
from src.metrics import classification_metrics

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "tables")
B = 5000
SEED = 20260807
RACE_STRATA = ["African-American", "Caucasian", "Hispanic", "Other", "Asian", "Native American"]
THRESHOLDS = np.arange(1, 12)
FOCAL_LAMBDAS = (0.25, 0.50, 0.75)
LAMBDA_GRID = np.arange(101) / 100
MINIMIZER_ATOL = 1e-12

BOOTSTRAP_INTERVALS_FILE = "bootstrap_intervals.csv"
DETERMINISTIC_COST_GRID_FILE = "deterministic_cost_grid.csv"
OPTIMAL_THRESHOLD_FREQUENCIES_FILE = "bootstrap_optimal_threshold_frequencies.csv"
POPULATION_ROBUSTNESS_FILE = "population_robustness.csv"


def safe_auc(y, pred):
    if len(np.unique(y)) == 2:
        return roc_auc_score(y, pred)
    return float('nan')


def get_ci(dist):
    valid_rate = np.mean(~np.isnan(dist))
    if valid_rate < 0.95:
        return float('nan'), float('nan')
    return np.nanpercentile(dist, 2.5), np.nanpercentile(dist, 97.5)


def minimizer_mask(values):
    #return membership in the full minimizing set, including numerical ties
    values = np.asarray(values, dtype=float)
    mask = np.zeros(values.shape, dtype=bool)
    finite = np.isfinite(values)
    if finite.any():
        minimum = np.nanmin(values)
        mask[finite] = np.isclose(
            values[finite], minimum, rtol=0.0, atol=MINIMIZER_ATOL
        )
    return mask


def threshold_set(mask):
    return tuple(int(t) for t in THRESHOLDS[np.asarray(mask, dtype=bool)])


def format_threshold_set(values):
    return "|".join(str(value) for value in values)


def append_ci_record(records, analysis_point, metric, distribution):
    lower, upper = get_ci(distribution)
    records.append({
        'threshold': analysis_point,
        'metric': metric,
        'ci_lower': lower,
        'ci_upper': upper,
    })


def run_full_pipeline():
    print(f"[BOOT] Output directory: {OUTPUT_DIR}")
    df = load_and_prepare()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rng = np.random.Generator(np.random.PCG64(SEED))
    race_positions = {r: np.flatnonzero(df["race"].to_numpy() == r) for r in RACE_STRATA}

    metrics_to_track = ['fpr', 'fnr', 'ppv', 'npv', 'tpr_recall', 'tnr_spec', 'accuracy', 'balanced_accuracy',
                        'overall_error', 'selection_rate']

    # arrays for Primary Metrics
    dist_b = {m: np.full((B, 11), np.nan) for m in metrics_to_track}
    dist_w = {m: np.full((B, 11), np.nan) for m in metrics_to_track}
    dist_gap = {m: np.full((B, 11), np.nan) for m in metrics_to_track}

    auc_b_dist, auc_w_dist, auc_r_dist = np.full(B, np.nan), np.full(B, np.nan), np.full(B, np.nan)

    # arrays for Calibration CIs
    cal_b_dist = np.full((B, 10), np.nan)
    cal_w_dist = np.full((B, 10), np.nan)
    cal_gap_dist = np.full((B, 10), np.nan)

    # arrays for Cost Analysis Optimal Frequencies
    optimal_t_counts = {lmbda: np.zeros(len(THRESHOLDS)) for lmbda in FOCAL_LAMBDAS}

    print(f"[PHASE 3] Starting {B} replicates for CIs and Uncertainty...")

    for i in range(B):
        if (i + 1) % 1000 == 0: print(f"  ...completed {i + 1}/{B} replicates")

        boot_idx = np.concatenate([rng.choice(idx, size=len(idx), replace=True) for idx in race_positions.values()])
        y_b = df['two_year_recid'].values[boot_idx]
        s_b = df['score'].values[boot_idx]
        r_b = df['race'].values[boot_idx]

        mask_b, mask_w = r_b == 'African-American', r_b == 'Caucasian'
        mask_c = mask_b | mask_w

        auc_b_dist[i] = safe_auc(y_b[mask_b], s_b[mask_b])
        auc_w_dist[i] = safe_auc(y_b[mask_w], s_b[mask_w])
        auc_r_dist[i] = safe_auc(y_b, s_b)

        # threshold Metrics & Cost Frequencies
        cost_for_t = {lmbda: np.full(len(THRESHOLDS), np.nan) for lmbda in FOCAL_LAMBDAS}
        for t_idx, t in enumerate(THRESHOLDS):
            pred_b = s_b >= t
            res_b, res_w = classification_metrics(y_b[mask_b], pred_b[mask_b]), classification_metrics(y_b[mask_w],
                                                                                                       pred_b[mask_w])

            for m in metrics_to_track:
                dist_b[m][i, t_idx] = res_b[m]
                dist_w[m][i, t_idx] = res_w[m]
                dist_gap[m][i, t_idx] = res_b[m] - res_w[m]

            res_c = classification_metrics(y_b[mask_c], pred_b[mask_c])
            if res_c['n'] > 0:
                for lmbda in FOCAL_LAMBDAS:
                    cost_for_t[lmbda][t_idx] = (lmbda * res_c['fp'] + (1.0 - lmbda) * res_c['fn']) / res_c['n']

        for lmbda in FOCAL_LAMBDAS:
            if not np.isnan(cost_for_t[lmbda]).all():
                optimal_t_counts[lmbda][minimizer_mask(cost_for_t[lmbda])] += 1

        # calibration Bootstrapping
        for s_idx, s in enumerate(range(1, 11)):
            mask_s = s_b == s
            n_b_s, n_w_s = mask_s & mask_b, mask_s & mask_w
            q_black = y_b[n_b_s].mean() if n_b_s.sum() > 0 else float('nan')
            q_white = y_b[n_w_s].mean() if n_w_s.sum() > 0 else float('nan')

            cal_b_dist[i, s_idx] = q_black
            cal_w_dist[i, s_idx] = q_white
            cal_gap_dist[i, s_idx] = q_black - q_white if (n_b_s.sum() > 0 and n_w_s.sum() > 0) else float('nan')

    print("[PHASE 4] Generating Full Lambda Cost Grid...")

    # deterministic grid logic on the primary and robustness populations
    y_orig = df['two_year_recid'].values
    s_orig = df['score'].values
    r_orig = df['race'].values
    m_b = r_orig == 'African-American'
    m_w = r_orig == 'Caucasian'
    m_c = m_b | m_w
    n_c = m_c.sum()
    n_b_orig = m_b.sum()
    n_w_orig = m_w.sum()

    grid_records = []
    population_records = []
    for lmbda in LAMBDA_GRID:
        costs = []
        for t in THRESHOLDS:
            pred_orig = s_orig >= t

            res_r = classification_metrics(y_orig, pred_orig)
            res_c = classification_metrics(y_orig[m_c], pred_orig[m_c])
            res_b = classification_metrics(y_orig[m_b], pred_orig[m_b])
            res_w = classification_metrics(y_orig[m_w], pred_orig[m_w])

            fp, fn = res_c['fp'], res_c['fn']
            L_t = (lmbda * fp + (1.0 - lmbda) * fn) / n_c if n_c > 0 else float('nan')
            L_t_r = (lmbda * res_r['fp'] + (1.0 - lmbda) * res_r['fn']) / res_r['n']

            fp_b, fn_b = res_b['fp'], res_b['fn']
            fp_w, fn_w = res_w['fp'], res_w['fn']

            costs.append({
                'lambda': lmbda, 'threshold': t, 'L_t_Sample_C': L_t,
                'L_t_Sample_R': L_t_r,
                'L_g_Black': (lmbda * fp_b + (1.0 - lmbda) * fn_b) / n_b_orig if n_b_orig > 0 else float('nan'),
                'L_g_White': (lmbda * fp_w + (1.0 - lmbda) * fn_w) / n_w_orig if n_w_orig > 0 else float('nan'),
                'L_tilde_t': lmbda * res_c['fpr'] + (1.0 - lmbda) * res_c['fnr']
            })

        # Preserve every minimizing set before applying the display convention.
        costs_df = pd.DataFrame(costs)
        costs_df['is_primary_minimizer'] = minimizer_mask(costs_df['L_t_Sample_C'].to_numpy())
        costs_df['is_sample_r_minimizer'] = minimizer_mask(costs_df['L_t_Sample_R'].to_numpy())
        costs_df['is_robustness_minimizer'] = minimizer_mask(costs_df['L_tilde_t'].to_numpy())

        sample_c_set = threshold_set(costs_df['is_primary_minimizer'])
        sample_r_set = threshold_set(costs_df['is_sample_r_minimizer'])
        population_records.append({
            'lambda': lmbda,
            'sample_c_minimizing_set': format_threshold_set(sample_c_set),
            'sample_r_minimizing_set': format_threshold_set(sample_r_set),
            'same_minimizing_set': sample_c_set == sample_r_set,
            'sample_c_display_threshold': max(sample_c_set),
            'sample_r_display_threshold': max(sample_r_set),
            'sample_r_minus_c_display_threshold': max(sample_r_set) - max(sample_c_set),
            'sample_c_min_loss': costs_df['L_t_Sample_C'].min(),
            'sample_r_min_loss': costs_df['L_t_Sample_R'].min(),
        })
        grid_records.extend(costs_df.to_dict('records'))

    cost_grid_df = pd.DataFrame(grid_records)
    expected_grid_rows = len(LAMBDA_GRID) * len(THRESHOLDS)
    if len(cost_grid_df) != expected_grid_rows:
        raise RuntimeError(
            f"Deterministic cost grid has {len(cost_grid_df)} rows; expected {expected_grid_rows}."
        )
    for flag in ('is_primary_minimizer', 'is_sample_r_minimizer', 'is_robustness_minimizer'):
        if not cost_grid_df.groupby('lambda')[flag].any().all():
            raise RuntimeError(f"At least one lambda has no {flag}.")
    cost_grid_df.to_csv(
        os.path.join(OUTPUT_DIR, DETERMINISTIC_COST_GRID_FILE), index=False
    )

    population_df = pd.DataFrame(population_records)
    if len(population_df) != len(LAMBDA_GRID):
        raise RuntimeError(
            f"Population robustness table has {len(population_df)} rows; expected {len(LAMBDA_GRID)}."
        )
    focal_rows = []
    for lmbda in FOCAL_LAMBDAS:
        match = np.isclose(population_df['lambda'], lmbda, rtol=0.0, atol=MINIMIZER_ATOL)
        if match.sum() != 1:
            raise RuntimeError(f"Expected one population robustness row at lambda={lmbda:.2f}.")
        row = population_df.loc[match].iloc[0]
        if not row['sample_c_minimizing_set'] or not row['sample_r_minimizing_set']:
            raise RuntimeError(f"Empty focal minimizing set at lambda={lmbda:.2f}.")
        focal_rows.append(row)
    population_df.to_csv(
        os.path.join(OUTPUT_DIR, POPULATION_ROBUSTNESS_FILE), index=False
    )
    print(f"[WRITE] {os.path.join(OUTPUT_DIR, POPULATION_ROBUSTNESS_FILE)}")

    # save CIs
    ci_recs = []
    for t_idx, t in enumerate(THRESHOLDS):
        for m in metrics_to_track:
            append_ci_record(ci_recs, t, f'{m} (Black)', dist_b[m][:, t_idx])
            append_ci_record(ci_recs, t, f'{m} (White)', dist_w[m][:, t_idx])
            append_ci_record(ci_recs, t, f'{m} Gap (B-W)', dist_gap[m][:, t_idx])

    for s_idx, s in enumerate(range(1, 11)):
        append_ci_record(ci_recs, f'Score_{s}', 'Calibration (Black)', cal_b_dist[:, s_idx])
        append_ci_record(ci_recs, f'Score_{s}', 'Calibration (White)', cal_w_dist[:, s_idx])
        append_ci_record(ci_recs, f'Score_{s}', 'Calibration Gap (B-W)', cal_gap_dist[:, s_idx])

    append_ci_record(ci_recs, 'threshold_independent', 'AUC (Black)', auc_b_dist)
    append_ci_record(ci_recs, 'threshold_independent', 'AUC (White)', auc_w_dist)
    append_ci_record(ci_recs, 'threshold_independent', 'AUC (Sample R)', auc_r_dist)
    append_ci_record(ci_recs, 'threshold_independent', 'AUC Gap (B-W)', auc_b_dist - auc_w_dist)

    bootstrap_intervals_df = pd.DataFrame(ci_recs)
    expected_auc_metrics = {
        'AUC (Black)', 'AUC (White)', 'AUC (Sample R)', 'AUC Gap (B-W)'
    }
    if not expected_auc_metrics.issubset(set(bootstrap_intervals_df['metric'])):
        raise RuntimeError("One or more required AUC bootstrap intervals are missing.")
    bootstrap_intervals_df.to_csv(
        os.path.join(OUTPUT_DIR, BOOTSTRAP_INTERVALS_FILE), index=False
    )

    opt_recs = [
        {
            'lambda': lmbda,
            'threshold': t,
            'loss': 'primary_L_t',
            'membership_frequency': optimal_t_counts[lmbda][i] / B,
        }
        for lmbda in FOCAL_LAMBDAS
        for i, t in enumerate(THRESHOLDS)
    ]
    pd.DataFrame(opt_recs).to_csv(
        os.path.join(OUTPUT_DIR, OPTIMAL_THRESHOLD_FREQUENCIES_FILE), index=False
    )

    print(f"[CHECK] Deterministic cost grid: {len(cost_grid_df)} rows")
    differing_populations = population_df.loc[~population_df['same_minimizing_set']]
    print(
        f"[CHECK] Sample R and Sample C minimizing sets differ at "
        f"{len(differing_populations)}/{len(population_df)} lambda values"
    )
    for row in focal_rows:
        sample_c_set = str(row['sample_c_minimizing_set']).replace('|', ',')
        sample_r_set = str(row['sample_r_minimizing_set']).replace('|', ',')
        print(
            f"[RESULT] lambda={row['lambda']:.2f}: "
            f"Sample C=({sample_c_set}), Sample R=({sample_r_set})"
        )
    print("[CHECK] Bootstrap intervals include all four AUC rows")
    print("[CHECK] Sample C, Sample R, and class-conditional minimizing sets are present for every lambda")
    print("[NOTE] Tied-minimizer membership frequencies need not sum to 100%")
    print("[SUCCESS] Phase 3 & 4 Fully Completed and strictly saved to output/tables/")


if __name__ == "__main__":
    try:
        run_full_pipeline()
    except Exception as err:
        print(f"\n[FATAL ERROR] {err}", file=sys.stderr)
        sys.exit(1)
