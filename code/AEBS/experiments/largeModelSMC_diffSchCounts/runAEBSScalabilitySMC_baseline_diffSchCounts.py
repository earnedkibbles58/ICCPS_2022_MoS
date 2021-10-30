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


    MODEST_PATH = "../../../../modest/Modest/modest"

    # Save results
    RESULTS_FOLDER = '../../../../results/AEBS/largeModel_SMC_diffSchCounts/baseline/'
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass

    init_dist = 160
    init_vel = 14

    sch_counts = [10,25,50,75,100,150,200,250,300]

    delta_d = 1
    delta_v = 0.4

    N=1
    H=3
    L=3

    run_times=[]
    safety_probs=[]
    sch_tested=[]

    iter_per_init = 10

    for sch_count in sch_counts:


        run_times_temp = []
        safety_probs_temp = []


        for i in range(iter_per_init):
            print(sch_count)
            print(i)

            AEBS_BASELINE_FOLDER = "../../../../models/AEBS/baseline/H" + str(H) + "L" + str(L) + "/N_" + str(N) + "/dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(delta_d) + "_deltav_" + str(delta_v) + "/"
            MODEL_FILE = AEBS_BASELINE_FOLDER + 'AEBSbaseline.modest'

            ## call modest
            start_time = time.time()
            proc = subprocess.run([MODEST_PATH, 'simulate',MODEL_FILE,'--lss','Sequential','-L',str(sch_count),'-C','0.8','-W','0.05'], stdout=PIPE, stderr=PIPE)
            duration = time.time() - start_time
            if proc.returncode == 0:
                crash_chance = parseMODESTOutput(proc.stdout)
            else:
                crash_chance = 1
                print("Bad")
            safety_chance = 1-crash_chance

            run_times_temp.append(duration)
            safety_probs_temp.append(safety_chance)

        sch_tested.append(sch_count)
        run_times.append(run_times_temp)
        safety_probs.append(safety_probs_temp)


        # save result eachIter
        np.save(RESULTS_FOLDER + "/runtimesAEBSBaseline.npy",run_times)
        np.save(RESULTS_FOLDER + "/safetyProbsAEBSBaseline.npy",safety_probs)
        np.save(RESULTS_FOLDER + "/schCounts.npy",sch_tested)


    np.save(RESULTS_FOLDER + "/runtimesAEBSBaseline.npy",run_times)
    np.save(RESULTS_FOLDER + "/safetyProbsAEBSBaseline.npy",safety_probs)
    np.save(RESULTS_FOLDER + "/schCounts.npy",sch_tested)



if __name__ == "__main__":
    main()