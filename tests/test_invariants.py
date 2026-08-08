"""
Phase 2 tests: Invariant and endpoint testing before Bootstrap.
Date: August 2026
"""

import os
import sys
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.prepare_data import load_and_prepare
from src.metrics import classification_metrics


def test_sample_sizes():
    df = load_and_prepare()
    assert len(df) == 7214
    assert len(df[df['race'].isin(['African-American', 'Caucasian'])]) == 6150
    assert len(df[df['race'] == 'African-American']) == 3696
    assert len(df[df['race'] == 'Caucasian']) == 2454


def test_endpoints_and_invariants():
    df = load_and_prepare()
    y_true = df['two_year_recid']

    # t=1: everyone is flagged
    y_pred_1 = df['score'] >= 1
    res_1 = classification_metrics(y_true, y_pred_1)
    assert res_1['selection_rate'] == 1.0
    assert math.isnan(res_1['npv'])

    # t=11: no one is flagged
    y_pred_11 = df['score'] >= 11
    res_11 = classification_metrics(y_true, y_pred_11)
    assert res_11['selection_rate'] == 0.0
    assert math.isnan(res_11['ppv'])

    # Mathematical invariant
    assert abs(res_1['overall_error'] - (1.0 - res_1['accuracy'])) < 1e-9