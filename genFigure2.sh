#!/bin/bash

pushd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/diffDeltaDs

echo "Running code to generate figure 2. This should all take around 3 mins."

echo "Running runAEBSDiffDeltaDs_baseline.py. This should take around 2 mins"
python3 runAEBSDiffDeltaDs_baseline.py
echo "Running runAEBSDiffDeltaDs_trimmedbaseline.py. This should take around 30 seconds"
python3 runAEBSDiffDeltaDs_trimmedbaseline.py
echo "Saving figure to /ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/diffDeltaDs_MC/plots/AEBSDiffDeltaDsPlot.png"
python3 visAEBSDiffDeltaDsResults.py
echo "Done"

popd
