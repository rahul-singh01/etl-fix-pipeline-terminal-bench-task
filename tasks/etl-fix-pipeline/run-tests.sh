#!/usr/bin/env bash
set -euo pipefail

# Install python test deps
python3 -m pip install --user -r requirements.txt >/dev/null 2>&1 || true

# Run pytest
python3 -m pytest -q tests/test_outputs.py
