#!/bin/bash

pushd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/diffWLDeltas

echo "Running code to generate figure 4. This should all take around 45 mins."

echo "Running runWaterTankDiffDeltaWLs_baseline.py. This should take around 2 mins"
python3 runWaterTankDiffDeltaWLs_baseline.py
echo "Running runWaterTankDiffDeltaWLs_trimmedBaseline.py. This should take around 30 seconds"
python3 runWaterTankDiffDeltaWLs_trimmedBaseline.py
echo "Saving figure to  /ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/diffWLDeltas/plots/if13.5_of4.3_numSteps10/waterTankDiffWLsPlot.png"
python3 visWaterTankDiffDeltaWLs.py
echo "Done"

popd
