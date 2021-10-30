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
    init_wls = [25,50,75]
    # init_wls = list(range(10,100,6))

    inflow = 13.5
    outflow = 4.3
    deltawl = 5
    numSteps = 10
    iter_per_init = 10


    run_times=[]
    safety_probs = []

    # Run PRISM
    for init_wl1 in init_wls:
        run_times_temp = []
        safety_probs_temp = []

        for init_wl2 in init_wls:

            run_times_temp_temp = []
            safety_probs_temp_temp = []

            init_wlid1 = math.ceil(init_wl1/deltawl)
            init_wlid2 = math.ceil(init_wl2/deltawl)

            for i in range(iter_per_init):
                print(init_wl1)
                print(init_wl2)
                print(i)

                WATER_TANK_BASELINE_FOLDER = "../../../../models/waterTank/trimmedBaselineSMC/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "/"
                MODEL_FILE = WATER_TANK_BASELINE_FOLDER + 'waterTankBaselineSMC' + str(numSteps) + 'Steps.modest'

                ## call modest
                start_time = time.time()
                proc = subprocess.run([MODEST_PATH, 'simulate',MODEL_FILE,'--lss','Sequential','-L','10','-C','0.8','-W','0.05','-E',"wlidInit1=" + str(init_wlid1) + ",wlidInit2=" + str(init_wlid2) + ",initContAction1=0,initContAction2=0"], stdout=PIPE, stderr=PIPE)
                duration = time.time() - start_time
                if proc.returncode == 0:
                    crash_chance = parseMODESTOutput(proc.stdout)
                else:
                    crash_chance = 1
                    print("Bad")
                safety_chance = 1-crash_chance

                run_times_temp_temp.append(duration)
                safety_probs_temp_temp.append(safety_chance)

            run_times_temp.append(run_times_temp_temp)
            safety_probs_temp.append(safety_probs_temp_temp)

        run_times.append(run_times_temp)
        safety_probs.append(safety_probs_temp)

    # Save results
    RESULTS_FOLDER = "../../../../results/waterTank/largeModel_SMC/trimmedBaselineSMC/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "/"
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass

    np.save(RESULTS_FOLDER + "/runtimesAEBSBaseline.npy",run_times)
    np.save(RESULTS_FOLDER + "/safetyProbsAEBSBaseline.npy",safety_probs)
    np.save(RESULTS_FOLDER + "/initwls.npy",init_wls)


if __name__ == "__main__":
    main()