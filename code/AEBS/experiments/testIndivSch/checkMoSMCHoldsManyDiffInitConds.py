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

    # Save results
    RESULTS_FOLDER = '../../../../results/AEBS/testIndivSch/'
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass


    # dists = [10,11,12,13,14,15,16,17,18,19,20]
    # speeds = [1,1.4,1.8,2.2,2.6,3,3.4,3.8,4.2,4.6,5]
    # MoS_holds_file = open("/data2/mcleav/latticeScalability/testIndivSchedulers/code/MoSMCassnHolds.txt",'w')
    # MoS_not_holds_file = open("/data2/mcleav/latticeScalability/testIndivSchedulers/code/MoSMCassnNotHolds.txt",'w')

    # large dists and speeds
    # dists = [10]
    # while not (dists[-1] == 150):
    #     dists.append(dists[-1]+5)

    # speeds = [2]
    # while not (speeds[-1] == 20):
    #     speeds.append(speeds[-1]+2)

    
    # small dists and speeds
    dists = [6,7,8,9,10]
    speeds = [0.4,0.8,1.2,1.6,2]

    # large dists and speeds
    # MoS_holds_file = open(RESULTS_FOLDER + "/MoSMCassnHolds_largelDistSpeeds.txt",'w')
    # MoS_not_holds_file = open(RESULTS_FOLDER + "/MoSMCassnNotHolds_largelDistSpeeds.txt",'w')

    # small dists and speeds
    MoS_holds_file = open(RESULTS_FOLDER + "/MoSMCassnHolds_smallDistSpeeds.txt",'w')
    MoS_not_holds_file = open(RESULTS_FOLDER + "/MoSMCassnNotHolds_smallDistSpeeds.txt",'w')



    deltad = 1
    deltav = 0.4

    N=1
    H=3
    L=3

    for init_dist in dists:
        for init_vel in speeds:

            AEBS_BASELINE_FOLDER = "../../../../models/AEBS/baselineTestIndivSch/H" + str(H) + "L" + str(L) + "/N_" + str(N) + "/dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(deltad) + "_deltav_" + str(deltav) + "/"
            AEBS_TRIMMED_BASELINE_FOLDER = "../../../../models/AEBS/trimmedBaselineTestIndivSch/H" + str(H) + "L" + str(L) + "/N_" + str(N) + "/dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(deltad) + "_deltav_" + str(deltav) + "/"


            MODEL_FILE_OB = AEBS_BASELINE_FOLDER + 'AEBSbaseline.prism'
            MODEL_FILE_OB_TRIMMED = AEBS_TRIMMED_BASELINE_FOLDER + 'AEBSbaseline.prism'
            


            ## call prism on untrimmed model
            proc = subprocess.run([PRISM_PATH, MODEL_FILE_OB, PROPS_FILE], stdout=PIPE, stderr=PIPE)
            if proc.returncode == 0:
                # print(proc.stdout.decode("utf-8"))
                prob_safe_untrimmed = 1-parsePRISMOutput(proc.stdout)
            else:
                # print('Timeout!')
                # print(proc.stdout.decode("utf-8"))
                # print(proc.stderr)
                prob_safe_untrimmed = 1
            


            ## call prism on untrimmed model
            proc = subprocess.run([PRISM_PATH, MODEL_FILE_OB_TRIMMED, PROPS_FILE], stdout=PIPE, stderr=PIPE)
            if proc.returncode == 0:
                # print(proc.stdout.decode("utf-8"))
                prob_safe_trimmed = 1-parsePRISMOutput(proc.stdout)
            else:
                # print('Timeout!')
                # print(proc.stdout.decode("utf-8"))
                # print(proc.stderr)
                prob_safe_trimmed = 1
            
            # print("dist_" + str(dist) + "_vel_" + str(speed) + "_deltad_" + str(deltad) + "_deltav_" + str(deltav) + ": " + str([prob_safe_untrimmed,prob_safe_trimmed]))
            if prob_safe_trimmed > prob_safe_untrimmed and (abs(prob_safe_trimmed-prob_safe_untrimmed)>(10**-6)):
                print("MoS does not hold")
                MoS_not_holds_file.write("dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(deltad) + "_deltav_" + str(deltav) + " prob diff: " + str(prob_safe_trimmed-prob_safe_untrimmed) +  "\n")
            else:
                print("MoS holds")
                MoS_holds_file.write("dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(deltad) + "_deltav_" + str(deltav) + "\n")

    MoS_holds_file.close()
    MoS_not_holds_file.close()



if __name__ == "__main__":
    main()
