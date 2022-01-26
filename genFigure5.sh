#!/bin/bash

pushd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/largeModelMC

echo "Running code to generate figure 3. This should all take around 19 hours."

echo "Running runWaterTankScalabilityMC_baseline.py. This should take around 18 hours."
python3 runWaterTankScalabilityMC_baseline.py
echo "Running runWaterTankScalabilityMC_trimmedbaseline.py. This should take around 1 hour."
python3 runWaterTankScalabilityMC_trimmedbaseline.py
echo "Running runWaterTankScalabilityMC_trimmedbaseline_negMoS.py. This should take around 9 mins."
python3 runWaterTankScalabilityMC_trimmedbaseline_negMoS.py
echo "Saving figures to /ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_MC/plots/if13.5_of4.3_deltawl5_numSteps10/runTimesPlotWithNeg.png"
echo "and /ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_MC/plots/if13.5_of4.3_deltawl5_numSteps10/safetyProbsPlotWithNeg.png"
python3 visWaterTankScalabilityResults.py

echo "Done"

popd
