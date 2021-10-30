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

    ## Define experiment parameters
    init_wl1 = 50
    init_wl2 = 50


    inflow = 13.5
    outflow = 4.3
    deltawl = 5
    numSteps = 10
    iter_per_init = 10

    # Save results
    RESULTS_FOLDER = "../../../../results/waterTank/largeModel_SMC_diffSchCounts/trimmedBaselineSMC/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "/"
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass

    # sch_counts = [10,25,50,75,100,150,200,250,300]
    sch_counts = [500,1000]

    run_times=np.load(RESULTS_FOLDER + "runtimesAEBSBaseline.npy").tolist()
    safety_probs=np.load(RESULTS_FOLDER + "safetyProbsAEBSBaseline.npy").tolist()
    sch_tested=np.load(RESULTS_FOLDER + "/schCounts.npy").tolist()

    # run_times=[]
    # safety_probs = []
    # sch_tested=[]

    for sch_count in sch_counts:

        run_times_temp = []
        safety_probs_temp = []

        init_wlid1 = math.ceil(init_wl1/deltawl)
        init_wlid2 = math.ceil(init_wl2/deltawl)

        for i in range(iter_per_init):
            print(sch_count)
            print(i)


            WATER_TANK_BASELINE_FOLDER = "../../../../models/waterTank/trimmedBaselineSMC/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "/"
            MODEL_FILE = WATER_TANK_BASELINE_FOLDER + 'waterTankBaselineSMC' + str(numSteps) + 'Steps.modest'

            ## call modest
            start_time = time.time()
            proc = subprocess.run([MODEST_PATH, 'simulate',MODEL_FILE,'--lss','Sequential','-L',str(sch_count),'-C','0.8','-W','0.05','-E',"wlidInit1=" + str(init_wlid1) + ",wlidInit2=" + str(init_wlid2) + ",initContAction1=0,initContAction2=0"], stdout=PIPE, stderr=PIPE)
            duration = time.time() - start_time
            if proc.returncode == 0:
                crash_chance = parseMODESTOutput(proc.stdout)
            else:
                crash_chance = 1
                print("Bad")
            safety_chance = 1-crash_chance

            run_times_temp.append(duration)
            safety_probs_temp.append(safety_chance)



        run_times.append(run_times_temp)
        safety_probs.append(safety_probs_temp)
        sch_tested.append(sch_count)

        np.save(RESULTS_FOLDER + "/runtimesAEBSBaseline.npy",run_times)
        np.save(RESULTS_FOLDER + "/safetyProbsAEBSBaseline.npy",safety_probs)
        np.save(RESULTS_FOLDER + "/schCounts.npy",sch_tested)

    np.save(RESULTS_FOLDER + "/runtimesAEBSBaseline.npy",run_times)
    np.save(RESULTS_FOLDER + "/safetyProbsAEBSBaseline.npy",safety_probs)
    np.save(RESULTS_FOLDER + "/schCounts.npy",sch_tested)


if __name__ == "__main__":
    main()