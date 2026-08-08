"""
Phase 1B test: Validation of ProPublica threshold mapping rules.
Date: August 2026
"""

import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.prepare_data import load_and_prepare


def test_threshold_mappings():
    df = load_and_prepare()

    # verify rule: 1-4 Low, 5-7 Medium, 8-10 High
    assert np.array_equal(df["score"] >= 5, df["score_text"] != "Low")
    assert np.array_equal(df["score"] >= 8, df["score_text"] == "High")

    # endpoints behavior
    assert (df["score"] >= 1).all()
    assert not (df["score"] >= 11).any()