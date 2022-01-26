#!/bin/bash

pushd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/largeModelSMC/

echo "Running code to generate figure 6. This should all take around 21 mins."

echo "Running runAEBSScalabilitySMC_baseline.py. This should take around 4.5 hours."
python3 runAEBSScalabilitySMC_baseline.py
echo "Running runAEBSScalabilitySMC_trimmedbaseline.py. This should take around 2.5 hours."
python3 runAEBSScalabilitySMC_trimmedbaseline.py
echo "Running runAEBSScalabilitySMCFewSchSamples_trimmedbaseline.py. This should take around 10 mins."
python3 runAEBSScalabilitySMCFewSchSamples_trimmedbaseline.py
echo "Saving figures to /ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_SMC/plots/if13.5_of4.3_deltawl5_numSteps10/runTimesPlot_withFew.png"
echo "and /ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_SMC/plots/if13.5_of4.3_deltawl5_numSteps10/safetyProbsPlot_withFew.png"
python3 visAEBSScalabilityResultsSMC.py

echo "Done"

popd
