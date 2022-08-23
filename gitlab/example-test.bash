#!/bin/bash

set -e

echo "Running at NERSC on" $NERSC_HOST

# Load desc-python Conda environment.
source /global/common/software/lsst/common/miniconda/setup_current_python.sh

# Run tests.
pytest ./python
