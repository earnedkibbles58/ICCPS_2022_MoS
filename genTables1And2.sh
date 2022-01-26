#!/bin/bash

pushd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/largeModelSMC

echo "Running code to generate tables 1 and 2. This should all take around 7 hours."

echo "Running runAEBSScalabilitySMC_baseline.py. This should take around 4.5 hours."
python3 runAEBSScalabilitySMC_baseline.py
echo "Running runAEBSScalabilitySMC_trimmedbaseline.py. This should take around 2.5 hours."
python3 runAEBSScalabilitySMC_trimmedbaseline.py
echo "Running runAEBSScalabilitySMCFewSchSamples_trimmedbaseline.py. This should take around 10 mins."
python3 runAEBSScalabilitySMCFewSchSamples_trimmedbaseline.py
echo "Saving results to /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/largeModelSMC/tempOutput.txt"
python3 visAEBSScalabilityResultsSMC.py > tempOutput.txt

echo "Done"

popd
