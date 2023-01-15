#!/bin/bash

set -e

echo "Running at NERSC on" $NERSC_HOST

# Load desc-python Conda environment.
source /global/common/software/lsst/common/miniconda/setup_current_python.sh

# Install mydescpackage package.
python3 -m pip install .

# Run tests.
pytest ./tests
