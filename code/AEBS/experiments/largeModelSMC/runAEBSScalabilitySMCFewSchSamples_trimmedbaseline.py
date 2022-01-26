import numpy as np
import csv
import math
import os
import time

import subprocess
from subprocess import PIPE





def parseMODESTOutput(output):
    output_str = output.decode("utf-8") 
    output_str_split = output_str.splitlines()
    line_to_get = None
    for item in output_str_split:
        if "Estimated" in item and "probability:" in item:
            print(item)
            line_to_get = item
    ans = line_to_get.split(" ")[-1]
    return float(ans)




def main():

    PRISM_PATH = "../../../../prism/prism-4.5/prism/bin/prism"
    PROPS_FILE = "../../../../models/AEBS/propsAEBS.props"

    MODEST_PATH = "../../../../modest/Modest/modest"
    ## Define experiment parameters
    # init_dists = list(range(100,200+5,5))
    # init_vels = list(range(10,22+4,4))

    init_dists = [130,160]
    init_vels = [14,18]
    delta_d = 1
    delta_v = 0.4

    N=1
    H=3
    L=3

    run_times=[]
    safety_probs = []

    iter_per_init = 10

    for init_dist in init_dists:
        run_times_temp = []
        safety_probs_temp = []

        for init_vel in init_vels:

            run_times_temp_temp = []
            safety_probs_temp_temp = []


            for i in range(iter_per_init):
                print(init_dist)
                print(init_vel)
                print(i)

                AEBS_BASELINE_FOLDER = "../../../../models/AEBS/trimmedBaseline_SMC/H" + str(H) + "L" + str(L) + "/N_" + str(N) + "/dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(delta_d) + "_deltav_" + str(delta_v) + "/"
                MODEL_FILE = AEBS_BASELINE_FOLDER + 'AEBSbaseline_withSMCRounding.modest'


                ## call modest
                start_time = time.time()
                proc = subprocess.run([MODEST_PATH, 'simulate',MODEL_FILE,'--lss','Sequential','-L','1','-C','0.8','-W','0.05','-J','2'], stdout=PIPE, stderr=PIPE)
                duration = time.time() - start_time
                if proc.returncode == 0:
                    crash_chance = parseMODESTOutput(proc.stdout)
                else:
                    crash_chance = 1
                    print("Bad")
                safety_chance = 1-crash_chance
                print(safety_chance)

                run_times_temp_temp.append(duration)
                safety_probs_temp_temp.append(safety_chance)

            run_times_temp.append(run_times_temp_temp)
            safety_probs_temp.append(safety_probs_temp_temp)

        run_times.append(run_times_temp)
        safety_probs.append(safety_probs_temp)

    # Save results
    RESULTS_FOLDER = '../../../../results/AEBS/largeModel_SMC/trimmedBaseline_SMC_fewSchSamples/'
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass

    np.save(RESULTS_FOLDER + "/runtimesAEBSBaseline.npy",run_times)
    np.save(RESULTS_FOLDER + "/safetyProbsAEBSBaseline.npy",safety_probs)
    np.save(RESULTS_FOLDER + "/initDists.npy",init_dists)
    np.save(RESULTS_FOLDER + "/initVels.npy",init_vels)


if __name__ == "__main__":
    main()