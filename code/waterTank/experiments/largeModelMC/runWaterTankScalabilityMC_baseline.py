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
    print(output_str_split)
    line_to_get = None
    for item in output_str_split:
        if "Result:" in item:
            line_to_get = item
            print(item)
    ans = line_to_get.split(" ")[1]
    return float(ans)




def main():

    PRISM_PATH = "../../../../prism/prism-4.5/prism/bin/prism"
    PROPS_FILE = "../../../../models/waterTank/tankPropsSink.props"

    ## Define experiment parameters
    init_wls = list(range(10,100,10))
    # init_wls = list(range(10,100,6))

    inflow = 13.5
    outflow = 4.3
    deltawl = 5
    numSteps = 10

    init_prev_cont_action = 0

    run_times=[]
    safety_probs = []

    # Run PRISM
    for init_wl1 in init_wls:
        run_times_temp = []
        safety_probs_temp = []

        for init_wl2 in init_wls:


            WATER_TANK_BASELINE_FOLDER = "../../../../models/waterTank/baseline/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "/"
            MODEL_FILE = WATER_TANK_BASELINE_FOLDER + 'waterTankBaseline' + str(numSteps) + 'Steps.prism'

            init_wlid1 = math.ceil(init_wl1/deltawl)
            init_wlid2 = math.ceil(init_wl2/deltawl)
            
            ## define consts
            consts = "wlidInit1=" + str(init_wlid1) + ",wlidInit2=" + str(init_wlid2) + ",initContAction1=" + str(init_prev_cont_action) + ",initContAction2=" + str(init_prev_cont_action)

            ## call prism
            start_time = time.time()
            proc = subprocess.run([PRISM_PATH, MODEL_FILE, PROPS_FILE,'-const', consts], stdout=PIPE, stderr=PIPE)
            duration = time.time() - start_time
            print(proc.stdout)
            if proc.returncode == 0:
                crash_chance = parsePRISMOutput(proc.stdout)
            else:
                crash_chance = 1
                print(proc.stdout)
                print("Bad")
            safety_chance = 1-crash_chance

            print(WATER_TANK_BASELINE_FOLDER + MODEL_FILE)
            print(duration)

            run_times_temp.append(duration)
            safety_probs_temp.append(safety_chance)

        run_times.append(run_times_temp)
        safety_probs.append(safety_probs_temp)

    # Save results
    RESULTS_FOLDER = "../../../../results/waterTank/largeModel_MC/baseline/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "/"
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass

    np.save(RESULTS_FOLDER + "/runtimesWaterTankBaseline.npy",run_times)
    np.save(RESULTS_FOLDER + "/safetyProbsWaterTankBaseline.npy",safety_probs)
    np.save(RESULTS_FOLDER + "/initwls.npy",init_wls)


if __name__ == "__main__":
    main()