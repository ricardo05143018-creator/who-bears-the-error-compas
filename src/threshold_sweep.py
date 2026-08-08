"""
Phase 2: Threshold sweep over COMPAS decile scores.
Date: August 2026
"""

import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.prepare_data import load_and_prepare
from src.metrics import classification_metrics

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "tables")


def run_threshold_sweep():
    df = load_and_prepare()

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    records = []

    mask_r = pd.Series(True, index=df.index)
    # restrict Sample C to the focal Black and White groups
    mask_c = df['race'].isin(['African-American', 'Caucasian'])
    mask_b = df['race'] == 'African-American'
    mask_w = df['race'] == 'Caucasian'

    groups = {
        'Sample R': mask_r,
        'Sample C': mask_c,
        'Black': mask_b,
        'White': mask_w
    }

    for t in range(1, 12):
        y_pred = df['score'] >= t
        t_metrics = {}

        for g_name, mask in groups.items():
            y_true_g = df.loc[mask, 'two_year_recid']
            y_pred_g = y_pred[mask]

            res = classification_metrics(y_true_g, y_pred_g)
            res['threshold'] = t
            res['group'] = g_name

            t_metrics[g_name] = res
            records.append(res)

        b = t_metrics['Black']
        w = t_metrics['White']

        # explicitly compute Black-White gaps per stratum
        gap_record = {'threshold': t, 'group': 'Gap (Black - White)', 'n': float('nan')}
        for k in ['tp', 'fp', 'tn', 'fn']:
            gap_record[k] = float('nan')

        metric_keys = [
            'fpr', 'fnr', 'ppv', 'npv', 'tpr_recall', 'tnr_spec',
            'accuracy', 'balanced_accuracy', 'overall_error', 'selection_rate'
        ]
        for k in metric_keys:
            gap_record[k] = b[k] - w[k]

        records.append(gap_record)

    results_df = pd.DataFrame(records)
    output_path = os.path.join(OUTPUT_DIR, "threshold_sweep_results.csv")
    results_df.to_csv(output_path, index=False)

    print("[SWEEP] Thresholds 1-11 evaluated for Sample R, Sample C, Black, and White.")
    print(f"[SWEEP] Output strictly saved to {output_path}\n")


if __name__ == "__main__":
    try:
        run_threshold_sweep()
    except Exception as err:
        print(f"\n[FATAL ERROR] {err}", file=sys.stderr)
        sys.exit(1)