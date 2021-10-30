import numpy as np
import csv
import math
import os
import time

import subprocess
from subprocess import PIPE





def parsePRISMOutput(output):
    output_str = output.decode("utf-8") 
    output_str_split = output_str.splitlines()
    line_to_get = None
    for item in output_str_split:
        if "Result:" in item:
            line_to_get = item
    ans = line_to_get.split(" ")[1]
    return float(ans)




def main():

    PRISM_PATH = "../../../../prism/prism-4.5/prism/bin/prism"
    PROPS_FILE = "../../../../models/AEBS/propsAEBS.props"

    ## Define experiment parameters
    delta_ds = [0.25, 0.5, 0.75, 1, 1.5]

    init_dist = 160
    init_vel = 20
    delta_v = 0.4

    N=1
    H=3
    L=3

    run_times=[]
    safety_probs = []

    # Run PRISM
    for delta_d in delta_ds:



        AEBS_BASELINE_FOLDER = "../../../../models/AEBS/baseline_diffDeltads/H" + str(H) + "L" + str(L) + "/N_" + str(N) + "/dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(delta_d) + "_deltav_" + str(delta_v) + "/"
        MODEL_FILE = AEBS_BASELINE_FOLDER + 'AEBSbaseline.prism'

        ## call prism
        start_time = time.time()
        proc = subprocess.run([PRISM_PATH, MODEL_FILE, PROPS_FILE], stdout=PIPE, stderr=PIPE)
        duration = time.time() - start_time
        if proc.returncode == 0:
            crash_chance = parsePRISMOutput(proc.stdout)
        else:
            crash_chance = 1
            print("Bad")
        safety_chance = 1-crash_chance

        run_times.append(duration)
        safety_probs.append(safety_chance)

    # Save results
    RESULTS_FOLDER = '../../../../results/AEBS/diffDeltaDs_MC/baseline/'
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass

    np.save(RESULTS_FOLDER + "/runtimesAEBSBaseline.npy",run_times)
    np.save(RESULTS_FOLDER + "/safetyProbsAEBSBaseline.npy",safety_probs)
    np.save(RESULTS_FOLDER + "/deltaDs.npy",delta_ds)


if __name__ == "__main__":
    main()