#!/bin/bash

pushd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/diffDeltaDs

echo "Running runAEBSDiffDeltaDs_baseline.py. This should take around 2 mins"
python3 runAEBSDiffDeltaDs_baseline.py
echo "Running runAEBSDiffDeltaDs_trimmedbaseline.py. This should take around 30 seconds"
python3 runAEBSDiffDeltaDs_trimmedbaseline.py
echo "Visualizing"
python3 visAEBSDiffDeltaDsResults.py
echo "Done"

popd
