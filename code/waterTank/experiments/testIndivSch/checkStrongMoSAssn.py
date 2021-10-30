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



    RESULTS_FOLDER = "../../../../results/waterTank/testIndivSchOneTank/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "_wlmax" + str(wlMax) + "/"
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass
    try:
        os.makedirs(RESULTS_FOLDER + "probs")
    except OSError as e:
        pass

    RESULTS_FILE = open(RESULTS_FOLDER + "checkStrongMoSAssn.txt","w")

    ## Iterate over initial conditions
    next_states = np.load(RESULTS_FOLDER + "trimming_state_hist.npy")

    # load non-det counts from disk
    nondet_counts = np.load(RESULTS_FOLDER + "nondet_counts.npy")

    probs_MOS_over_scheds = []
    probs_s1_mins_s2_over_scheds = []

    for next_state in next_states:
        print(next_state)
        wlids2 = next_state[0]
        wlids1 = next_state[1]


        s2_less_safe_count = 0
        s1_minus_s2_running_sum = 0

        ## NEED TO UN HARDCODE THIS AND ALLOW FOR MORE THAN 2 TRANSITIONS PER NONDET

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
            
            # string_list[5] = "const int wlidMax = " + str(wlids2) + ";\n"
            consts = "wlidInit1=" + str(wlids2) + ",initContAction1=0"

            ## save to temporary file
            my_file = open(MODEL_FILE_WATER_TANK_TO_RUN, "w")
            new_file_contents = "".join(string_list)
            my_file.write(new_file_contents)
            my_file.close()


            ## call prism
            proc = subprocess.run([PRISM_PATH, MODEL_FILE_WATER_TANK_TO_RUN, PROPS_FILE,'-const', consts], stdout=PIPE, stderr=PIPE)
            if proc.returncode == 0:
                ans = parsePRISMOutput(proc.stdout)
            else:
                ans = 1
            print(proc.stdout)
            s2_safe_prob = 1-ans

            # string_list[5] = "const int wlidMax = " + str(wlids1) + ";\n"
            consts = "wlidInit1=" + str(wlids1) + ",initContAction1=0"

            ## save to temporary file
            my_file = open(MODEL_FILE_WATER_TANK_TO_RUN, "w")
            new_file_contents = "".join(string_list)
            my_file.write(new_file_contents)
            my_file.close()


            ## call prism
            proc = subprocess.run([PRISM_PATH, MODEL_FILE_WATER_TANK_TO_RUN, PROPS_FILE,'-const', consts], stdout=PIPE, stderr=PIPE)
            if proc.returncode == 0:
                ans = parsePRISMOutput(proc.stdout)
            else:
                ans = 1
                print(proc.stdout)
            s1_safe_prob = 1-ans

            if s2_safe_prob <= s1_safe_prob:
                s2_less_safe_count+=1
            s1_minus_s2_running_sum = s1_minus_s2_running_sum + (s1_safe_prob - s2_safe_prob)

        # print("next state: " + str(next_state))
        # print("Prob MoS Holds over schs: " + str(s2_less_safe_count/tot_sch_count))
        # print("s1-s2 running sum: " + str(s1_minus_s2_running_sum))

        RESULTS_FILE.write("next state: " + str(next_state) + "\n")
        RESULTS_FILE.write("Prob MoS Holds over schs: " + str(s2_less_safe_count/tot_sch_count) + "\n")
        RESULTS_FILE.write("s1-s2 running sum: " + str(s1_minus_s2_running_sum) + "\n")

        probs_MOS_over_scheds.append(s2_less_safe_count/tot_sch_count)
        probs_s1_mins_s2_over_scheds.append(s1_minus_s2_running_sum)
    
    np.save(RESULTS_FOLDER + "/probs_MOS_over_scheds.npy",probs_MOS_over_scheds)
    np.save(RESULTS_FOLDER + "/s1_mins_s2_over_scheds.npy",probs_s1_mins_s2_over_scheds)


    RESULTS_FILE.close()

if __name__ == "__main__":
    main()
