import numpy as np
import os

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def main():

    ## This code needs to be run on a machine where you can run plt.show() to move the 3-d plots around for best visualization
    inflow = 13.5
    outflow = 4.3
    deltawl = 5
    numSteps = 10
    
    # load data
    RESULTS_FOLDER_BASELINE = "../../../../results/waterTank/largeModel_SMC/baseline/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "/"
    RESULTS_FOLDER_TRIMMED_BASELINE = "../../../../results/waterTank/largeModel_SMC/trimmedBaselineSMC/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "/"
    RESULTS_FOLDER_TRIMMED_BASELINE_FEW = "../../../../results/waterTank/largeModel_SMC/trimmedBaselineSMC_fewSchSamples/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "/"

    IMAGES_FOLDER = "../../../../results/waterTank/largeModel_SMC/plots/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl)  + "_numSteps" + str(numSteps) + "/"
    try:
        os.makedirs(IMAGES_FOLDER)
    except OSError as e:
        pass

    run_times_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "runtimesAEBSBaseline.npy")
    safety_probs_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "safetyProbsAEBSBaseline.npy")

    run_times_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "runtimesAEBSBaseline.npy")
    safety_probs_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "safetyProbsAEBSBaseline.npy")

    run_times_trimmed_few = np.load(RESULTS_FOLDER_TRIMMED_BASELINE_FEW + "runtimesAEBSBaseline.npy")
    safety_probs_trimmed_few = np.load(RESULTS_FOLDER_TRIMMED_BASELINE_FEW + "safetyProbsAEBSBaseline.npy")

    run_times_untrimmed_average = np.average(run_times_untrimmed,2)
    safety_probs_untrimmed_average = np.average(safety_probs_untrimmed,2)
    safety_probs_untrimmed_var = np.var(safety_probs_untrimmed,2)

    run_times_trimmed_average = np.average(run_times_trimmed,2)
    safety_probs_trimmed_average = np.average(safety_probs_trimmed,2)
    safety_probs_trimmed_var = np.var(safety_probs_trimmed,2)

    run_times_trimmed_few_average = np.average(run_times_trimmed_few,2)
    safety_probs_trimmed_few_average = np.average(safety_probs_trimmed_few,2)
    safety_probs_trimmed_few_var = np.var(safety_probs_trimmed_few,2)


    # run_times_neg_trimmed = np.load(RESULTS_FOLDER_NEG_TRIMMED_BASELINE + "runtimesAEBSTrimmedBaselineMCNegMoS.npy")
    # safety_probs_neg_trimmed = np.load(RESULTS_FOLDER_NEG_TRIMMED_BASELINE + "safetyProbsAEBSTrimmedBaselineMCNegMoS.npy")
    
    print("Untrimmed 10 Sch")
    print(safety_probs_untrimmed_average)
    print(run_times_untrimmed_average)

    print("Trimmed 10 Sch")
    print(safety_probs_trimmed_average)
    print(run_times_trimmed_average)

    print("Trimmed 1 Sch")
    print(safety_probs_trimmed_few_average)
    print(run_times_trimmed_few_average)
    # init_wls = np.load(RESULTS_FOLDER_BASELINE + "/initwls.npy")
    # X,Y = np.meshgrid(init_wls,init_wls)


    # ## plot safety chances
    # ax = plt.axes(projection='3d')
    # ax.scatter3D(Y, X, safety_probs_untrimmed_average, color='green')
    # ax.scatter3D(Y, X, safety_probs_trimmed_average, color='red')
    # ax.scatter3D(Y, X, safety_probs_trimmed_few_average, color='orange')
    # # ax.scatter3D(Y, X, safety_probs_neg_trimmed, color='blue')

    # plt.xlabel('Initial Tank 1 Water Level',fontsize=12)
    # plt.ylabel('Initial Tank 2 Water Level',fontsize=12)
    # ax.set_zlabel('Safety Probability',fontsize=12)
    # # plt.savefig(IMAGES_FOLDER + '/safetyProbsPlot_withFew.png')
    # plt.show()
    # plt.clf()

    # ## plot runtimes
    # ax2 = plt.axes(projection='3d')
    # ax2.scatter3D(Y, X, np.log10(run_times_untrimmed_average), color='green')
    # ax2.scatter3D(Y, X, np.log10(run_times_trimmed_average), color='red')
    # ax2.scatter3D(Y, X, np.log10(run_times_trimmed_few_average), color='orange')

    # plt.xlabel('Initial Tank 1 Water Level',fontsize=12)
    # plt.ylabel('Initial Tank 2 Water Level',fontsize=12)
    # ax2.set_zlabel('Runtime (log(s))',fontsize=12)
    # # plt.savefig(IMAGES_FOLDER + '/runTimesPlot_withFew.png')
    # plt.show()
    # plt.clf()


    # ## plot safety chances
    # ax = plt.axes(projection='3d')
    # ax.scatter3D(Y, X, safety_probs_untrimmed_var, color='green')
    # ax.scatter3D(Y, X, safety_probs_trimmed_var, color='red')
    # ax.scatter3D(Y, X, safety_probs_trimmed_few_var, color='orange')
    # # ax.scatter3D(Y, X, safety_probs_neg_trimmed, color='blue')

    # plt.xlabel('Initial Distance (m)',fontsize=12)
    # plt.ylabel('Initial Speed (m/s)',fontsize=12)
    # ax.set_zlabel('Safety Probability Variance',fontsize=12)
    # # plt.savefig(IMAGES_FOLDER + '/safetyProbsVariancePlot_withFew.png')
    # plt.show()
    # plt.clf()



if __name__ == "__main__":
    main()