"""
Phase 1B: Schema validation and minimal data preparation.
Date: August 2026
"""

import os
import sys
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
INPUT_FILE = os.path.join(DATA_DIR, "compas-scores-two-years.csv")

def load_and_prepare():
    if not os.path.exists(INPUT_FILE):
        raise RuntimeError(f"Missing {INPUT_FILE}.")

    df = pd.read_csv(INPUT_FILE)

    if df.shape != (7214, 53):
        raise RuntimeError(f"Shape mismatch! Expected (7214, 53), got {df.shape}")

    # ensure duplicate general recidivism score columns match before dropping one.
    if not df['decile_score'].equals(df['decile_score.1']):
        raise RuntimeError("Duplicate decile_score columns are not identical.")

    req_cols = ['id', 'race', 'decile_score', 'score_text', 'two_year_recid']
    if df[req_cols].isnull().any().any():
        raise RuntimeError("Missing values found in required columns.")

    if df['id'].nunique() != len(df):
        raise RuntimeError("Column 'id' is not unique.")

    if not df['decile_score'].isin(range(1, 11)).all():
        raise RuntimeError("decile_score contains values outside 1-10.")

    if not df['two_year_recid'].isin([0, 1]).all():
        raise RuntimeError("two_year_recid contains values other than 0 and 1.")

    expected_race_counts = {
        "African-American": 3696, "Caucasian": 2454, "Hispanic": 637,
        "Other": 377, "Asian": 32, "Native American": 18
    }
    if df['race'].value_counts().to_dict() != expected_race_counts:
        raise RuntimeError("Race counts mismatch.")

    expected_outcome_counts = {0: 3963, 1: 3251}
    if df['two_year_recid'].value_counts().to_dict() != expected_outcome_counts:
        raise RuntimeError("Outcome counts mismatch.")

    expected_texts = df['decile_score'].map(
        lambda x: "Low" if x <= 4 else ("Medium" if x <= 7 else "High")
    )
    if not expected_texts.equals(df['score_text']):
        raise RuntimeError("score_text mapping does not match 1-4/5-7/8-10 rule.")

    clean_df = pd.DataFrame({
        'row_key': np.arange(len(df)),
        'race': df['race'],
        'score': df['decile_score'],
        'score_text': df['score_text'],
        'two_year_recid': df['two_year_recid']
    })

    return clean_df

if __name__ == "__main__":
    try:
        load_and_prepare()
        print("[CHECK] Phase 1B Schema validation and data integrity: PASS")
    except RuntimeError as err:
        print(f"[FATAL ERROR] {err}", file=sys.stderr)
        sys.exit(1)