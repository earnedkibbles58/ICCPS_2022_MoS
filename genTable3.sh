#!/bin/bash

pushd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/testIndivSch

echo "Running code to generate table 3. This should all take around 3 hours."

echo "Running checkStrongMoSAssn.py. This should take around 3 hours."
echo "The results are saved in /ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/testIndivSchOneTank/if5.5_of2.1_deltawl5_numSteps10_wlmax26/checkStrongMoSAssn.txt"
python3 checkStrongMoSAssn.py
echo "Done"

popd
