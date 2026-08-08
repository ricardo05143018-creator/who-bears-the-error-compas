"""
Phase 1A: Fetch and validate the ProPublica COMPAS two-year recidivism dataset.
Date: August 2026
"""

import hashlib
import os
import sys
import urllib.request

TARGET_URL = "https://raw.githubusercontent.com/propublica/compas-analysis/bafff5da3f2e45eca6c2d5055faad269defd135a/compas-scores-two-years.csv"
EXPECTED_SHA256 = "c451db85908b2f7fef1d83203bedf6b71ecda0d5af468d82ae62178f91d0cc7d"
EXPECTED_ROWS = 7214

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "compas-scores-two-years.csv")


def fetch_and_validate():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    try:
        response = urllib.request.urlopen(TARGET_URL)
        raw_data = response.read()
    except Exception as e:
        raise RuntimeError(f"Network error during data acquisition: {e}")

    print("[DATA] Download complete")

    hasher = hashlib.sha256()
    hasher.update(raw_data)
    actual_sha256 = hasher.hexdigest()

    # Discrepancy block analysis per protocol
    if actual_sha256 != EXPECTED_SHA256:
        raise RuntimeError(f"SHA256 checksum mismatch! Expected {EXPECTED_SHA256}, got {actual_sha256}")

    print(f"[CHECK] rows expected: {EXPECTED_ROWS}")
    print("[CHECK] SHA256: PASS")

    try:
        with open(OUTPUT_FILE, "wb") as f:
            f.write(raw_data)
    except Exception as e:
        raise RuntimeError(f"Failed to write data to {OUTPUT_FILE}: {e}")


if __name__ == "__main__":
    try:
        fetch_and_validate()
    except RuntimeError as err:
        print(f"RuntimeError: {err}", file=sys.stderr)
        sys.exit(1)