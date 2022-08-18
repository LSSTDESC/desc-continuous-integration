#!/bin/bash

set -e

echo "Running at NERSC on" $NERSC_HOST

echo "Contents of /global/cfs/cdirs/lsst"
runls=$(ls /global/cfs/cdirs/lsst/)
echo $runls

exit 0


