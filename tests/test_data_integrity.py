"""
Phase 1B test: Pytest wrapper for schema validation and integrity.
Date: August 2026
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.prepare_data import load_and_prepare

def test_data_integrity():
    df = load_and_prepare()
    assert len(df) == 7214
    assert 'row_key' in df.columns
    assert df['row_key'].nunique() == 7214