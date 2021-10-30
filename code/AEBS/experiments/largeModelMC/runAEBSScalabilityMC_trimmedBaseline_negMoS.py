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
    init_dists = list(range(100,200+5,5))
    init_vels = list(range(10,22+4,4))

    delta_d = 1
    delta_v = 0.4

    N=1
    H=3
    L=3

    run_times=[]
    safety_probs = []

    # Run PRISM
    for init_dist in init_dists:
        run_times_temp = []
        safety_probs_temp = []

        for init_vel in init_vels:


            AEBS_BASELINE_FOLDER = "../../../../models/AEBS/trimmedBaseline_MC_negMoS/H" + str(H) + "L" + str(L) + "/N_" + str(N) + "/dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(delta_d) + "_deltav_" + str(delta_v) + "/"
            MODEL_FILE = AEBS_BASELINE_FOLDER + 'AEBSbaseline_withNegMCRounding.prism'

            ## call prism
            start_time = time.time()
            proc = subprocess.run([PRISM_PATH, MODEL_FILE, PROPS_FILE], stdout=PIPE, stderr=PIPE)
            duration = time.time() - start_time
            print(proc.stdout)
            if proc.returncode == 0:
                crash_chance = parsePRISMOutput(proc.stdout)
            else:
                crash_chance = 1
                print(proc.stdout)
                print("Bad")
            safety_chance = 1-crash_chance

            run_times_temp.append(duration)
            safety_probs_temp.append(safety_chance)

        run_times.append(run_times_temp)
        safety_probs.append(safety_probs_temp)

    # Save results
    RESULTS_FOLDER = '../../../../results/AEBS/largeModel_MC/trimmedBaseline_MC_negMoS/'
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass

    np.save(RESULTS_FOLDER + "/runtimesAEBSTrimmedBaselineMCNegMoS.npy",run_times)
    np.save(RESULTS_FOLDER + "/safetyProbsAEBSTrimmedBaselineMCNegMoS.npy",safety_probs)
    np.save(RESULTS_FOLDER + "/initDists.npy",init_dists)
    np.save(RESULTS_FOLDER + "/initVels.npy",init_vels)


if __name__ == "__main__":
    main()