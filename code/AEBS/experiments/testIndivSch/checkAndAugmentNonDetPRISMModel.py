#!/usr/bin/python

import subprocess
from subprocess import PIPE
import time
import math
from shutil import copyfile
import numpy as np
import os
import re

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


def getdidvidFromPISMLine(line):
    # get did
    did_str_1 = "did'="
    did_str_2 = "\)"
    pattern = did_str_1 + "(.*?)" + did_str_2
    did_str = re.search(pattern, line).group(1)
    # print(did_str)



    # get vid
    vid_str_1 = "vid'="
    vid_str_2 = "\)"
    pattern = vid_str_1 + "(.*?)" + vid_str_2
    vid_str = re.search(pattern, line).group(1)
    # print(vid_str)


    return int(did_str),int(vid_str)


def getBlockOfLines(string_list,start_ind,transition_substr):
    curr_ind = start_ind

    for line in string_list[curr_ind:]:
        if not transition_substr in line:
            break
        curr_ind +=1
    # print(curr_ind)
    # print(string_list[start_ind:curr_ind])
    return string_list[start_ind:curr_ind]


def parseBlockOfNondet(string_list,start_ind,end_ind,nondet_count,nondet_counts):
    next_states = []
    # print("Parsing nondet")
    # print(string_list[start_ind:end_ind])
    currK = 0
    num_lines_at_current_K = 0
    currK_str = 'currK=' + str(currK)
    currK_start_ind = start_ind
    for line in string_list[start_ind:end_ind]:
        assert line == string_list[currK_start_ind + num_lines_at_current_K] # sanity check
        if currK_str in line:
            num_lines_at_current_K+=1
        else:
            if num_lines_at_current_K >=2:
                ## found nondet, need to augment with flags
                for i in range(num_lines_at_current_K):
                    curr_line = string_list[currK_start_ind+i]
                    # print(curr_line)
                    flag_str = 'SCHED_' + str(nondet_count) + '_' + str(i)
                    new_line = flag_str + curr_line
                    string_list[currK_start_ind+i] = new_line
                nondet_count+=1
                nondet_counts.append(num_lines_at_current_K)
            
            
            currK_start_ind = currK_start_ind + num_lines_at_current_K
            num_lines_at_current_K = 1
            currK+=1
            currK_str = 'currK=' + str(currK)


    if num_lines_at_current_K >=2:
        ## found nondet, need to augment with flags
        for i in range(num_lines_at_current_K):
            curr_line = string_list[currK_start_ind+i]
            if i==0:
                # print(curr_line)
                nextdid_s2,nextvid_s2 = getdidvidFromPISMLine(curr_line)
            else:
                nextdid_s1,nextvid_s1 = getdidvidFromPISMLine(curr_line)
                next_states.append([nextdid_s2,nextvid_s2,nextdid_s1,nextvid_s1])
            flag_str = 'SCHED_' + str(nondet_count) + '_' + str(i)
            new_line = flag_str + curr_line
            string_list[currK_start_ind+i] = new_line
        nondet_count+=1
        nondet_counts.append(num_lines_at_current_K)


    return string_list,nondet_count,nondet_counts,next_states


                    
        

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
    

    AEBS_BASELINE_FOLDER = "../../../../models/AEBS/baselineTestIndivSch/H" + str(H) + "L" + str(L) + "/N_" + str(N) + "/dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(deltad) + "_deltav_" + str(deltav) + "/"
    MODEL_FILE_AEBS = AEBS_BASELINE_FOLDER + 'AEBSbaseline.prism'
    MODEL_FILE_AEBS_TO_AUGMENT = AEBS_BASELINE_FOLDER + 'AEBSbaseline_augmented.prism'


    # Save results
    RESULTS_FOLDER = "../../../../results/AEBS/testIndivSch/H" + str(H) + "L" + str(L) + "/N_" + str(N) + "/dist_" + str(init_dist) + "_vel_" + str(init_vel) + "_deltad_" + str(deltad) + "_deltav_" + str(deltav) + "/"
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass



    print("Counting non-det on file")


    ## STEPS TO IMPLEMENT
    transition_substr = '[]'
    nondet_count = 0
    standard_block_size = N+1
    nondet_counts = []
    tot_sch = 1
    next_states = []

    # load file lines all at once
    copyfile(MODEL_FILE_AEBS, MODEL_FILE_AEBS_TO_AUGMENT)
    my_file = open(MODEL_FILE_AEBS_TO_AUGMENT)
    string_list = my_file.readlines()
    my_file.close()

    # find first line of bulk of PRISM code by looking for '[]' substring
    curr_line = 0
    while curr_line < len(string_list):
        for line in string_list[curr_line:]:
            if transition_substr in line:
                break
            curr_line+=1
        if curr_line >= len(string_list):
            break
        # print(curr_line)
        # print(string_list[curr_line])

        curr_block = getBlockOfLines(string_list,curr_line,transition_substr)

        if len(curr_block) > standard_block_size:
            # print("FOUND NONDET! NEED TO PARSE")
            # print(curr_block)
            
            string_list,nondet_count,nondet_counts,temp_next_states = parseBlockOfNondet(string_list,curr_line,curr_line+len(curr_block),nondet_count,nondet_counts)
            for n in temp_next_states:
                next_states.append(n)

        curr_line += len(curr_block)
    
    for count in nondet_counts:
        tot_sch = tot_sch * count
            
            

    print(nondet_count)
    # print(nondet_counts)
    print(tot_sch)
    # print(next_states)

    np.save(RESULTS_FOLDER + "/nondet_counts.npy",nondet_counts)
    np.save(RESULTS_FOLDER + "/trimming_state_hist.npy",next_states)

    my_file = open(MODEL_FILE_AEBS_TO_AUGMENT, "w")
    new_file_contents = "".join(string_list)
    my_file.write(new_file_contents)
    my_file.close()



    return



if __name__ == "__main__":
    main()
