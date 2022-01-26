#!/bin/bash

pushd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/largeModelSMC/

echo "Running code to generate figure 6. This should all take around 21 mins."

echo "Running runWaterTankScalabilitySMC_baseline.py. This should take around 9 mins."
python3 runWaterTankScalabilitySMC_baseline.py
echo "Running runWaterTankScalabilitySMC_trimmedbaseline.py. This should take around 9 mins."
python3 runWaterTankScalabilitySMC_trimmedbaseline.py
echo "Running runWaterTankScalabilitySMCFewSchSamples_trimmedbaseline.py. This should take around 3 mins."
python3 runWaterTankScalabilitySMCFewSchSamples_trimmedbaseline.py
echo "Saving figures to /ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_SMC/plots/if13.5_of4.3_deltawl5_numSteps10/runTimesPlot_withFew.png"
echo "and /ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_SMC/plots/if13.5_of4.3_deltawl5_numSteps10/safetyProbsPlot_withFew.png"
python3 visWaterTankScalabilitySMC.py

echo "Done"

popd
