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

    PRISM_PATH = "../../../../prism/prism-4.5/prism/bin/prism"
    PROPS_FILE = "../../../../models/AEBS/propsAEBS.props"


    deltad = 1
    deltav = 0.4

    N=1
    H=3
    L=3

    init_dist = 9
    init_vel = 1.2


    # Save results
    RESULTS_FOLDER = "../../../../results/AEBS/testIndivSch/H" + str(H) + "L" + str(L) + "/N_" + str(N) + "/dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(deltad) + "_deltav_" + str(deltav) + "/"
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass
    try:
        os.makedirs(RESULTS_FOLDER + "probs")
    except OSError as e:
        pass

    AEBS_BASELINE_FOLDER = "../../../../models/AEBS/baselineTestIndivSch/H" + str(H) + "L" + str(L) + "/N_" + str(N) + "/dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(deltad) + "_deltav_" + str(deltav) + "/"
    MODEL_FILE_AEBS = AEBS_BASELINE_FOLDER + 'AEBSbaseline_augmented.prism'
    MODEL_FILE_AEBS_TO_RUN = AEBS_BASELINE_FOLDER + 'AEBSbaseline_toRun.prism'


    RESULTS_FILE = open(RESULTS_FOLDER + "checkStrongMoSAssn.txt","w")

    ## Iterate over initial conditions
    next_states = np.load(RESULTS_FOLDER + "trimming_state_hist.npy")

    # load non-det counts from disk
    nondet_counts = np.load(RESULTS_FOLDER + "nondet_counts.npy")

    probs_MOS_over_scheds = []
    probs_s1_mins_s2_over_scheds = []

    for next_state in next_states:
        print(next_state)
        dids2 = next_state[0]
        vids2 = next_state[1]
        dids1 = next_state[2]
        vids1 = next_state[3]


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
            copyfile(MODEL_FILE_AEBS, MODEL_FILE_AEBS_TO_RUN)
            my_file = open(MODEL_FILE_AEBS_TO_RUN)
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
            
            string_list[3] = "const int didMax = " + str(dids2) + ";\n"
            string_list[4] = "const int vidMax = " + str(vids2) + ";\n"

            ## save to temporary file
            my_file = open(MODEL_FILE_AEBS_TO_RUN, "w")
            new_file_contents = "".join(string_list)
            my_file.write(new_file_contents)
            my_file.close()


            ## call prism
            proc = subprocess.run([PRISM_PATH, MODEL_FILE_AEBS_TO_RUN, PROPS_FILE], stdout=PIPE, stderr=PIPE)
            if proc.returncode == 0:
                ans = parsePRISMOutput(proc.stdout)
            else:
                ans = 1
                print("Bad")
            # print(proc.stdout)
            s2_safe_prob = 1-ans

            string_list[3] = "const int didMax = " + str(dids1) + ";\n"
            string_list[4] = "const int vidMax = " + str(vids1) + ";\n"

            ## save to temporary file
            my_file = open(MODEL_FILE_AEBS_TO_RUN, "w")
            new_file_contents = "".join(string_list)
            my_file.write(new_file_contents)
            my_file.close()


            ## call prism
            proc = subprocess.run([PRISM_PATH, MODEL_FILE_AEBS_TO_RUN, PROPS_FILE], stdout=PIPE, stderr=PIPE)
            if proc.returncode == 0:
                ans = parsePRISMOutput(proc.stdout)
            else:
                ans = 1
                print("Bad")
                # print(proc.stdout)
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
