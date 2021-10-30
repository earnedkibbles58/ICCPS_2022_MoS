#!/usr/bin/python

import subprocess
from subprocess import PIPE
import time
import math
from shutil import copyfile
import numpy as np
import os

import matplotlib.pyplot as plt



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

    print("Running OB indiv schedulers")

    inflow = 5.5
    outflow = 2.1
    deltawl = 5
    numSteps = 10
    wlMax = 26

    PRISM_PATH = "../../../../prism/prism-4.5/prism/bin/prism"
    PROPS_FILE = "../../../../models/waterTank/tankPropsSink.props"

    WATER_TANK_BASELINE_FOLDER = "../../../../models/waterTank/BaselineTestIndivSchOneTank/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_wlmax" + str(wlMax) + "/"

    MODEL_FILE_WATER_TANK = WATER_TANK_BASELINE_FOLDER + 'waterTankBaseline_augmented.prism'
    MODEL_FILE_WATER_TANK_TO_RUN = WATER_TANK_BASELINE_FOLDER + 'waterTankBaseline_augmented_toRun.prism'

    # Save results
    RESULTS_FOLDER = "../../../../results/waterTank/testIndivSchOneTank/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "_wlmax" + str(wlMax) + "/"
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass
    try:
        os.makedirs(RESULTS_FOLDER + "probs")
    except OSError as e:
        pass


    # load non-det counts from disk
    nondet_counts = np.load(RESULTS_FOLDER + "nondet_counts.npy")

    probs_safe = []
    probs_unsafe = []

    tot_sch_count = 1
    for c in nondet_counts:
        tot_sch_count = tot_sch_count*c


    running_nondet_counts = [1]
    for i,c in enumerate(nondet_counts):
        if i != 1:
            running_nondet_counts.append(running_nondet_counts[-1]*c)
    assert running_nondet_counts[-1]*nondet_counts[-1] == tot_sch_count
        
    for total_counter in range(tot_sch_count):
        copyfile(MODEL_FILE_WATER_TANK, MODEL_FILE_WATER_TANK_TO_RUN)
        my_file = open(MODEL_FILE_WATER_TANK_TO_RUN)
        string_list = my_file.readlines()
        my_file.close()

        for sch_counter,count in enumerate(nondet_counts):
            trans_ind_to_use = math.floor(total_counter/running_nondet_counts[sch_counter]) % count
            for trans_counter in range(count):
                sch_str = "SCHED_" + str(sch_counter) + "_" + str(trans_counter)
                str_to_repl = "" if trans_counter==trans_ind_to_use else "//"

                ## REPLACE ALL INSTANCES OF sch_str with str_to_repl in string_list
                for i,s in enumerate(string_list):
                    string_list[i] = s.replace(sch_str,str_to_repl)
        
        ## save to temporary file
        my_file = open(MODEL_FILE_WATER_TANK_TO_RUN, "w")
        new_file_contents = "".join(string_list)
        my_file.write(new_file_contents)
        my_file.close()

        consts = "wlidInit1=3,initContAction1=0"
        ## call prism
        proc = subprocess.run([PRISM_PATH, MODEL_FILE_WATER_TANK_TO_RUN, PROPS_FILE,'-const', consts], stdout=PIPE, stderr=PIPE)
        if proc.returncode == 0:
            ans = parsePRISMOutput(proc.stdout)
        else:
            print("Bad!")
            print(proc.stdout)
            ans = 1
        print(ans)
        probs_safe.append(1-ans) # prism computes crash chance, but we want safety chance
        probs_unsafe.append(ans)

    np.save(RESULTS_FOLDER + "probs/probs_safe.npy",probs_safe)
    np.save(RESULTS_FOLDER + "probs/probs_unsafe.npy",probs_unsafe)

    folder_to_save = RESULTS_FOLDER + "figures/"
    try:
        os.makedirs(folder_to_save)
    except OSError:
        pass

    plt.hist(probs_safe,bins=50)
    plt.savefig(folder_to_save + 'probsSafeHist.png')
    plt.clf()

    plt.hist(probs_unsafe,bins=50)
    plt.savefig(folder_to_save + 'probsUnsafeHist.png')
    plt.clf()




if __name__ == "__main__":
    main()
