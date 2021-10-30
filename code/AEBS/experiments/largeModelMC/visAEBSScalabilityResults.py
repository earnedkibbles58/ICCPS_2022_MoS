import numpy as np
import os

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def main():

    ## This code needs to be run on a machine where you can run plt.show() to move the 3-d plots around for best visualization

    # load data
    RESULTS_FOLDER_BASELINE = '../../../../results/AEBS/largeModel_MC/baseline/'
    RESULTS_FOLDER_TRIMMED_BASELINE = '../../../../results/AEBS/largeModel_MC/trimmedBaseline_MC/'
    RESULTS_FOLDER_NEG_TRIMMED_BASELINE = '../../../../results/AEBS/largeModel_MC/trimmedBaseline_MC_negMoS/'

    IMAGES_FOLDER = '../../../../results/AEBS/largeModel_MC/plots'
    try:
        os.makedirs(IMAGES_FOLDER)
    except OSError as e:
        pass

    run_times_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "runtimesAEBSBaseline.npy")
    safety_probs_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "safetyProbsAEBSBaseline.npy")

    run_times_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "runtimesAEBSTrimmedBaselineMC.npy")
    safety_probs_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "safetyProbsAEBSTrimmedBaselineMC.npy")

    run_times_neg_trimmed = np.load(RESULTS_FOLDER_NEG_TRIMMED_BASELINE + "runtimesAEBSTrimmedBaselineMCNegMoS.npy")
    safety_probs_neg_trimmed = np.load(RESULTS_FOLDER_NEG_TRIMMED_BASELINE + "safetyProbsAEBSTrimmedBaselineMCNegMoS.npy")


    init_dists = np.load(RESULTS_FOLDER_BASELINE + "/initDists.npy")
    init_vels = np.load(RESULTS_FOLDER_BASELINE + "/initVels.npy")


    X,Y = np.meshgrid(init_vels,init_dists)


    ## plot safety chances
    ax = plt.axes(projection='3d')
    ax.scatter3D(Y, X, safety_probs_untrimmed, color='green')
    ax.scatter3D(Y, X, safety_probs_trimmed, color='red')
    ax.scatter3D(Y, X, safety_probs_neg_trimmed, color='blue')

    plt.xlabel('Initial Distance (m)',fontsize=12)
    plt.ylabel('Initial Speed (m/s)',fontsize=12)
    ax.set_zlabel('Safety Probability',fontsize=12)
    # plt.savefig(IMAGES_FOLDER + '/safetyProbsPlotWithNeg.png')
    plt.show()
    plt.clf()

    ## plot runtimes
    ax2 = plt.axes(projection='3d')
    ax2.scatter3D(Y, X, np.log10(run_times_untrimmed), color='green')
    ax2.scatter3D(Y, X, np.log10(run_times_trimmed), color='red')
    # ax2.scatter3D(Y, X, np.log10(run_times_neg_trimmed), color='blue')

    plt.xlabel('Initial Distance (m)',fontsize=12)
    plt.ylabel('Initial Speed (m/s)',fontsize=12)
    ax2.set_zlabel('Runtime (log(s))',fontsize=12)
    # plt.savefig(IMAGES_FOLDER + '/runTimesPlotWithNeg.png')
    plt.show()
    plt.clf()



if __name__ == "__main__":
    main()