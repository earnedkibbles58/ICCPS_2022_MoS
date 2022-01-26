#!/bin/bash

pushd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/largeModelMC

echo "Running code to generate figure 3. This should all take around 16 mins."

echo "Running runAEBSScalabilityMC_baseline.py. This should take around 7 mins."
python3 runAEBSScalabilityMC_baseline.py
echo "Running runAEBSScalabilityMC_trimmedBaseline.py. This should take around 3 mins."
python3 runAEBSScalabilityMC_trimmedBaseline.py
echo "Running runAEBSScalabilityMC_trimmedBaseline_negMoS.py. This should take around 6 mins."
python3 runAEBSScalabilityMC_trimmedBaseline_negMoS.py
echo "Saving figures to /ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/largeModel_MC/plots/runTimesPlotWithNeg.png"
echo "and /ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/largeModel_MC/plots/safetyProbsPlotWithNeg.png"
python3 visAEBSScalabilityResults.py

echo "Done"

popd
