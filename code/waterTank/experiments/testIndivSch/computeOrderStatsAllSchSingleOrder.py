#!/usr/bin/python

import subprocess
from subprocess import PIPE
import os
import time
import math
from shutil import copyfile
import numpy as np

import matplotlib.pyplot as plt
import itertools

import computeOrderStats as c



def computeOrderStatGivenTrimmings(probs,sch,N,nondet_counts,running_nondet_counts):

    temp_probs = []

    for i,prob in enumerate(probs):

        use_prob = True
        for j,_ in enumerate(sch):
            trans_ind_to_use = math.floor(i/running_nondet_counts[j]) % nondet_counts[j]
            # curr_sch_bool = (sch[j] == trans_ind_to_use) or (sch[j]==-1)
            curr_sch_bool = not (str(trans_ind_to_use) in sch[j])
            if not curr_sch_bool:
                use_prob = False
                break

        ## compute each sch bool by hand
        # sch_0_bool = (sch[0]==2) or (sch[0]==0 and i%2 == 0) or (sch[0]==1 and i%2 == 1)
        # sch_1_bool = (sch[1]==2) or (sch[1]==0 and i%4 <= 1) or (sch[1]==1 and i%4 > 1)
        # sch_2_bool = (sch[2]==2) or (sch[2]==0 and i%8 <= 3) or (sch[2]==1 and i%8 > 3)
        # sch_3_bool = (sch[3]==2) or (sch[3]==0 and i%16 <= 7) or (sch[3]==1 and i%16 > 7)
        # sch_4_bool = (sch[4]==2) or (sch[4]==0 and i%32 <= 15) or (sch[4]==1 and i%32 > 15)
        # sch_5_bool = (sch[5]==2) or (sch[5]==0 and i%64 <= 31) or (sch[5]==1 and i%64 > 31)
        # sch_6_bool = (sch[6]==2) or (sch[6]==0 and i%128 <= 63) or (sch[6]==1 and i%128 > 63)
        # sch_7_bool = (sch[7]==2) or (sch[7]==0 and i%256 <= 127) or (sch[7]==1 and i%256 > 127)
        # sch_8_bool = (sch[8]==2) or (sch[8]==0 and i%512 <= 255) or (sch[8]==1 and i%512 > 255)
        # sch_9_bool = (sch[9]==2) or (sch[9]==0 and i%1024 <= 511) or (sch[9]==1 and i%1024 > 511)

        if use_prob:
            temp_probs.append(prob)

    temp_probs.sort()

    os_vals,os_probs = c.computeZeroOrderStatDiscreteUnif(temp_probs,N)


    return os_vals,os_probs


def computeUnifPDFGivenTrimmings(probs,sch,nondet_counts,running_nondet_counts):

    temp_probs = []

    for i,prob in enumerate(probs):

        use_prob = True
        for j,_ in enumerate(sch):
            trans_ind_to_use = math.floor(i/running_nondet_counts[j]) % nondet_counts[j]
            # curr_sch_bool = (sch[j] == trans_ind_to_use) or (sch[j]==-1)
            curr_sch_bool = not (str(trans_ind_to_use) in sch[j])
            if not curr_sch_bool:
                use_prob = False
                break

        if use_prob:
            temp_probs.append(prob)


    temp_probs.sort()

    pdf_vals,pdf_probs = c.consolidateDataDiscreteUnifs(temp_probs)

    return pdf_vals,pdf_probs



def computeAllSchProbsGivenTrimmings(probs,sch,nondet_counts,running_nondet_counts):
    temp_probs = []

    for i,prob in enumerate(probs):

        use_prob = True
        for j,_ in enumerate(sch):
            trans_ind_to_use = math.floor(i/running_nondet_counts[j]) % nondet_counts[j]
            # curr_sch_bool = (sch[j] == trans_ind_to_use) or (sch[j]==-1)
            curr_sch_bool = not (str(trans_ind_to_use) in sch[j])
            if not curr_sch_bool:
                use_prob = False
                break

        if use_prob:
            temp_probs.append(prob)

    return temp_probs


def computeAreaUnderCDF(cdfProbs,cdfVals,maxVal=1):
    runningArea = 0
    
    for i,_ in enumerate(cdfVals):
        currProb = cdfProbs[i]
        currVal = cdfVals[i]

        if i == (len(cdfVals)-1):
            # edge case
            nextVal = maxVal
        else:
            ## common case
            nextVal = cdfVals[i+1]

        assert nextVal >= currVal
        termToAdd = currProb * (nextVal - currVal)
        runningArea += termToAdd
    
    return runningArea

def compareDiscreteCDFsAreas(cdf1probs,cdf1vals,cdf2probs,cdf2vals,maxVal=1):

    # CDF 1 is before trimming
    areaUnderCDF1 = computeAreaUnderCDF(cdf1probs,cdf1vals,maxVal=maxVal)
    # CDF 2 is after trimming
    areaUnderCDF2 = computeAreaUnderCDF(cdf2probs,cdf2vals,maxVal=maxVal)

    return areaUnderCDF2 - areaUnderCDF1



def computeCDFFromPDF(probs,vals):

    cdfProbs = []
    cdfVals = []

    cdfProbs = [probs[0]]
    for j,prob in enumerate(probs):
        if j==0:
            continue
        cdfProbs.append(cdfProbs[-1] + prob)

    for val in vals:
        cdfVals.append(val)

    return cdfProbs,cdfVals

def main():

    inflow = 5.5
    outflow = 2.1
    deltawl = 5
    numSteps = 10
    wlMax = 26

    savefigs = True

    # Save results
    RESULTS_FOLDER = "../../../../results/waterTank/testIndivSchOneTank/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "_wlmax" + str(wlMax) + "/"
    try:
        os.makedirs(RESULTS_FOLDER)
    except OSError as e:
        pass

    probs_file = RESULTS_FOLDER + "probs/probs_safe.npy"
    probs = np.load(probs_file)

    nondet_counts = np.load(RESULTS_FOLDER + "nondet_counts.npy")

    running_nondet_counts = [1]
    for i,c in enumerate(nondet_counts):
        if i != 1:
            running_nondet_counts.append(running_nondet_counts[-1]*c)


    N = 5 ## number of samples to use for order stat

    x_lim_lower = 0
    x_lim_upper = 1

    ## trimming order
    trimming_order = [0,1,2,3,4,5,6,7,8,9] # array of numbers from 0-9, indicating the order of trimming on the model



    order_str = "order"
    for t in trimming_order:
        order_str = order_str + str(t)
    order_str = order_str + "_N_" + str(N) # name of folder to save plots to
    print(order_str)

    trimmings = []

    ## sch is an array of numbers: each number corresponds to a trimmed transition, if -1 then use any of the transitions, otherwise the number corresponds to the index of the transitions to use. Note that 0 corresponds to the MoS-worst transition
    sch = []
    for i in range(len(nondet_counts)):
        # trimming_order.append(i)
        trimmings.append(0)
        # sch.append(-1)
        sch.append("")




    min_safety_probs = []
    os_area_diffs = []

    os_vals_temp,os_probs_temp = computeOrderStatGivenTrimmings(probs,sch,N,nondet_counts,running_nondet_counts)
    pdf_vals_temp,pdf_probs_temp = computeUnifPDFGivenTrimmings(probs,sch,nondet_counts,running_nondet_counts)
    allSch_vals_temp = computeAllSchProbsGivenTrimmings(probs,sch,nondet_counts,running_nondet_counts)

    ## compute CDF of OS
    prevCDFProbs,prevCDFVals = computeCDFFromPDF(os_probs_temp,os_vals_temp)

    min_safety_probs.append(min(os_vals_temp))

    os_valss = [os_vals_temp]
    os_probss = [os_probs_temp]

    pdf_valss = [pdf_vals_temp]
    pdf_probss = [pdf_probs_temp]

    allSch_valss = [allSch_vals_temp]

    
    for i in range(len(trimming_order)):
        
        for j in range(1,nondet_counts[trimming_order[i]]):
            
            sch[trimming_order[i]] += str(j)
            # print(sch)
        
        
            # sch[trimming_order[i]] = trimmings[trimming_order[i]]

            os_vals_temp,os_probs_temp = computeOrderStatGivenTrimmings(probs,sch,N,nondet_counts,running_nondet_counts)
            pdf_vals_temp,pdf_probs_temp = computeUnifPDFGivenTrimmings(probs,sch,nondet_counts,running_nondet_counts)
            allSch_vals_temp = computeAllSchProbsGivenTrimmings(probs,sch,nondet_counts,running_nondet_counts)

            currCDFProbs,currCDFVals = computeCDFFromPDF(os_probs_temp,os_vals_temp)
            osCDFAreaDiff = compareDiscreteCDFsAreas(prevCDFProbs,prevCDFVals,currCDFProbs,currCDFVals)
            prevCDFProbs = currCDFProbs
            prevCDFVals = currCDFVals

            os_valss.append(os_vals_temp)
            os_probss.append(os_probs_temp)

            pdf_valss.append(pdf_vals_temp)
            pdf_probss.append(pdf_probs_temp)

            allSch_valss.append(allSch_vals_temp)

            min_safety_probs.append(min(os_vals_temp))
            os_area_diffs.append(osCDFAreaDiff)
    print(os_area_diffs)
    
    print(min_safety_probs)

    if savefigs:

        folder_to_save = RESULTS_FOLDER + '/figures/schHists/' + order_str
        try:
            os.makedirs(folder_to_save)
        except OSError:
            pass
        try:
            os.makedirs(folder_to_save + '/CDFs')
        except:
            pass
        try:
            os.makedirs(folder_to_save + '/schHists')
        except:
            pass


        # gen scheduler pdf histogram
        for i in range(len(allSch_valss)):
            vals_to_plot = allSch_valss[i]

            plt.hist(vals_to_plot,bins=50)
            plt.xlabel('PDF of Crash Probability (from Uniformly Sampling Schedulers)')
            plt.ylabel('Safety Probability (Order Statistic)')
            plt.title('Histogram of Scheduler Probabilites After Trimming ' + str(i))
            plt.xlim([x_lim_lower, x_lim_upper])
            plt.savefig(folder_to_save +  '/schHists/sch_hist_trimming' + str(i) + '.png')
            plt.clf()


        # gen order stat histograms
        for i in range(len(os_valss)):
            vals_to_plot = os_valss[i]
            probs_to_plot = os_probss[i]

            plt.plot(vals_to_plot,probs_to_plot,'x')
            plt.xlabel('Order Stat Crash Probability')
            plt.ylabel('Safety Probability (Order Statistic)')
            plt.xlim([x_lim_lower, x_lim_upper])
            plt.title('Order Stat PDF After Trimming ' + str(i))
            plt.savefig(folder_to_save + '/trimming' + str(i) + '.png')
            plt.clf()
        
        # plot min probabilities over the course of trimming
        plt.plot(min_safety_probs,'x')
        plt.xlabel('Trimming Number')
        plt.ylabel('Safety Probability (min)')
        plt.title('Min Safety Probabilities Over Trimming')
        plt.savefig(folder_to_save + '/minSafetyProbs.png')
        plt.clf()


        # plot CDFS of order stats
        cdf_valss = []
        for i in range(len(os_valss)):
            vals_to_plot = os_valss[i]
            probs_to_plot = os_probss[i]

            cdf_vals = [0]
            for j,prob in enumerate(probs_to_plot):
                cdf_vals.append(cdf_vals[-1] + prob)
            cdf_valss.append(cdf_vals)

            temp_vals_to_plot = [vals_to_plot[0]]
            for val in vals_to_plot:
                temp_vals_to_plot.append(val)

            plt.plot(temp_vals_to_plot,cdf_vals)
            plt.xlabel('Order Statistic Value')
            plt.ylabel('Cumulative Probabilty')
            plt.title('Order Statistic CDF')
            plt.xlim([x_lim_lower, x_lim_upper])
            plt.savefig(folder_to_save + '/CDFs/cdf_trimming' + str(i) + '.png')
            plt.clf()

            # if i==5:
            #     print(temp_vals_to_plot)
            #     print(cdf_vals)

        # plot all CDFs at once
        for j,cdf_val in enumerate(cdf_valss):
            # if j >= 2:
            #     continue
            vals_to_plot = os_valss[j]
            temp_vals_to_plot = [vals_to_plot[0]]
            for val in vals_to_plot:
                temp_vals_to_plot.append(val)
            plt.plot(temp_vals_to_plot,cdf_val,label='trimming ' + str(j))
        plt.xlabel('Order Statistic Value')
        plt.ylabel('Cumulative Probabilty')
        plt.title('Order Statistic CDF')
        plt.legend(loc='lower right')
        plt.xlim([x_lim_lower, x_lim_upper])
        plt.savefig(folder_to_save + '/CDFs/allCDFs.png')





if __name__ == "__main__":
    main()
