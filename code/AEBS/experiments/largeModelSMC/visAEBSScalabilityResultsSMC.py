import numpy as np
import os

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def main():

    ## This code needs to be run on a machine where you can run plt.show() to move the 3-d plots around for best visualization

    # load data
    RESULTS_FOLDER_BASELINE = '../../../../results/AEBS/largeModel_SMC/baseline/'
    RESULTS_FOLDER_TRIMMED_BASELINE = '../../../../results/AEBS/largeModel_SMC/trimmedBaseline_SMC/'
    RESULTS_FOLDER_TRIMMED_BASELINE_FEW_SCH = '../../../../results/AEBS/largeModel_SMC/trimmedBaseline_SMC_fewSchSamples/'
    # RESULTS_FOLDER_NEG_TRIMMED_BASELINE = '../../../../results/AEBS/largeModel_SMC/trimmedBaseline_MC_negMoS/'

    IMAGES_FOLDER = '../../../../results/AEBS/largeModel_SMC/plots'
    try:
        os.makedirs(IMAGES_FOLDER)
    except OSError as e:
        pass

    run_times_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "runtimesAEBSBaseline.npy")
    safety_probs_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "safetyProbsAEBSBaseline.npy")

    run_times_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "runtimesAEBSBaseline.npy")
    safety_probs_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "safetyProbsAEBSBaseline.npy")

    run_times_trimmed_few = np.load(RESULTS_FOLDER_TRIMMED_BASELINE_FEW_SCH + "runtimesAEBSBaseline.npy")
    safety_probs_trimmed_few = np.load(RESULTS_FOLDER_TRIMMED_BASELINE_FEW_SCH + "safetyProbsAEBSBaseline.npy")

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

    print("Trimmed Few Sch")
    print(safety_probs_trimmed_few_average)
    print(run_times_trimmed_few_average)
    
    init_dists = np.load(RESULTS_FOLDER_BASELINE + "/initDists.npy")
    init_vels = np.load(RESULTS_FOLDER_BASELINE + "/initVels.npy")


    X,Y = np.meshgrid(init_vels,init_dists)


    ## plot safety chances
    ax = plt.axes(projection='3d')
    ax.scatter3D(Y, X, safety_probs_untrimmed_average, color='green')
    ax.scatter3D(Y, X, safety_probs_trimmed_average, color='red')
    ax.scatter3D(Y, X, safety_probs_trimmed_few_average, color='orange')
    # ax.scatter3D(Y, X, safety_probs_neg_trimmed, color='blue')

    plt.xlabel('Initial Distance (m)',fontsize=12)
    plt.ylabel('Initial Speed (m/s)',fontsize=12)
    ax.set_zlabel('Safety Probability',fontsize=12)
    plt.savefig(IMAGES_FOLDER + '/safetyProbsPlot_withFew.png')
    plt.show()
    plt.clf()

    ## plot runtimes
    ax2 = plt.axes(projection='3d')
    ax2.scatter3D(Y, X, np.log10(run_times_untrimmed_average), color='green')
    ax2.scatter3D(Y, X, np.log10(run_times_trimmed_average), color='red')
    ax2.scatter3D(Y, X, np.log10(run_times_trimmed_few_average), color='orange')

    plt.xlabel('Initial Distance (m)',fontsize=12)
    plt.ylabel('Initial Speed (m/s)',fontsize=12)
    ax2.set_zlabel('Runtime (log(s))',fontsize=12)
    plt.savefig(IMAGES_FOLDER + '/runTimesPlot_withFew.png')
    plt.show()
    plt.clf()


    ## plot safety chances
    ax = plt.axes(projection='3d')
    ax.scatter3D(Y, X, safety_probs_untrimmed_var, color='green')
    ax.scatter3D(Y, X, safety_probs_trimmed_var, color='red')
    ax.scatter3D(Y, X, safety_probs_trimmed_few_var, color='orange')
    # ax.scatter3D(Y, X, safety_probs_neg_trimmed, color='blue')

    plt.xlabel('Initial Distance (m)',fontsize=12)
    plt.ylabel('Initial Speed (m/s)',fontsize=12)
    ax.set_zlabel('Safety Probability Variance',fontsize=12)
    plt.savefig(IMAGES_FOLDER + '/safetyProbsVariancePlot_withFew.png')
    plt.show()
    plt.clf()



if __name__ == "__main__":
    main()