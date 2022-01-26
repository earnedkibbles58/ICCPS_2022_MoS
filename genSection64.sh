#!/bin/bash

pushd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/testIndivSch

echo "Running code to generate section 6.4 text. This should all take around 5 days."
echo "To stop the code early, press ctrl-C and examine the output file for the partial results."

echo "Running checkStrongMoSAssn.py. This should take around 5 days."
echo "The results are saved in /ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/testIndivSch/H3L3/N_1/dist_9_vel_1.2_deltad_1_deltav_0.4/checkStrongMoSAssn.txt"
python3 checkStrongMoSAssn.py
echo "Done"

popd
