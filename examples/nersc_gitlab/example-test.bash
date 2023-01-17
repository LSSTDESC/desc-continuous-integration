#!/bin/bash

set -e

echo "Running at NERSC on" $NERSC_HOST

# Load desc-python Conda environment.
source /global/common/software/lsst/common/miniconda/setup_current_python.sh

# Install mydescpackage package in a venv.
python3 -m venv my_ci_venv
source my_ci_venv/bin/activate
python3 -m pip install .[ci]

# Run tests.
pytest ./tests



