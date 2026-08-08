"""
Phase 1.5: Descriptive discrimination and calibration diagnostics.
Protocol Sections 7.3 and 7.4
Date: August 2026
"""

import os
import sys
import pandas as pd
from sklearn.metrics import roc_auc_score

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.prepare_data import load_and_prepare

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "tables")


def run_diagnostics():
    df = load_and_prepare()
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("\n--- 7.3 Threshold-independent discrimination (ROC AUC) ---")
    auc_r = roc_auc_score(df['two_year_recid'], df['score'])
    print(f"Sample R Overall AUC: {auc_r:.4f}")

    mask_b = df['race'] == 'African-American'
    mask_w = df['race'] == 'Caucasian'

    auc_b = roc_auc_score(df.loc[mask_b, 'two_year_recid'], df.loc[mask_b, 'score'])
    auc_w = roc_auc_score(df.loc[mask_w, 'two_year_recid'], df.loc[mask_w, 'score'])

    print(f"Black AUC:            {auc_b:.4f}")
    print(f"White AUC:            {auc_w:.4f}")
    print(f"AUC Gap (B - W):      {auc_b - auc_w:.4f}\n")

    cal_records = []
    for s in range(1, 11):
        mask_s = df['score'] == s
        n_b = mask_s & mask_b
        n_w = mask_s & mask_w

        # calculate score-level base rates
        q_b = df.loc[n_b, 'two_year_recid'].mean() if n_b.sum() > 0 else float('nan')
        q_w = df.loc[n_w, 'two_year_recid'].mean() if n_w.sum() > 0 else float('nan')

        cal_records.append({
            'score': s,
            'n_black': int(n_b.sum()),
            'q_black': q_b,
            'n_white': int(n_w.sum()),
            'q_white': q_w,
            'q_gap': q_b - q_w if n_b.sum() > 0 and n_w.sum() > 0 else float('nan')
        })

    cal_df = pd.DataFrame(cal_records)
    out_path = os.path.join(OUTPUT_DIR, "calibration_diagnostics.csv")
    cal_df.to_csv(out_path, index=False)

    print("--- 7.4 Score-level calibration diagnostic ---")
    print(f"Saved score-level rates to {out_path}\n")


if __name__ == "__main__":
    try:
        run_diagnostics()
    except Exception as err:
        print(f"\n[FATAL ERROR] {err}", file=sys.stderr)
        sys.exit(1)