"""
Phase 1C test: Hard gate replication of core contingency tables.
Date: August 2026
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.prepare_data import load_and_prepare
from src.metrics import confusion_counts


def test_propublica_replication():
    df = load_and_prepare()
    y_true = df['two_year_recid']
    y_pred = df['score'] >= 5

    expected = {
        'All': (2681, 1282, 1216, 2035),
        'African-American': (990, 805, 532, 1369),
        'Caucasian': (1139, 349, 461, 505)
    }

    assert confusion_counts(y_true, y_pred) == expected['All']

    mask_b = df['race'] == 'African-American'
    assert confusion_counts(y_true[mask_b], y_pred[mask_b]) == expected['African-American']

    mask_w = df['race'] == 'Caucasian'
    assert confusion_counts(y_true[mask_w], y_pred[mask_w]) == expected['Caucasian']