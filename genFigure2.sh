#!/bin/bash

pushd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/diffDeltaDs

python3 runAEBSDiffDeltaDs_baseline.py
python3 runAEBSDiffDeltaDs_trimmedbaseline.py
python3 visAEBSDiffDeltaDsResults.py

popd
