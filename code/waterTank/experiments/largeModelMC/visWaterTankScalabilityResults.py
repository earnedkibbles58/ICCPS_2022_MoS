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
    RESULTS_FOLDER_BASELINE = "../../../../results/waterTank/largeModel_MC/baseline/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "/"
    RESULTS_FOLDER_TRIMMED_BASELINE = "../../../../results/waterTank/largeModel_MC/trimmedBaseline_MC/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "/"
    RESULTS_FOLDER_NEG_TRIMMED_BASELINE = "../../../../results/waterTank/largeModel_MC/trimmedBaseline_MC_negMoS/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "/"


    IMAGES_FOLDER = "../../../../results/waterTank/largeModel_MC/plots/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl)  + "_numSteps" + str(numSteps) + "/"
    try:
        os.makedirs(IMAGES_FOLDER)
    except OSError as e:
        pass

    run_times_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "runtimesWaterTankBaseline.npy")
    safety_probs_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "safetyProbsWaterTankBaseline.npy")

    run_times_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "runtimesWaterTankTrimmedBaseline.npy")
    safety_probs_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "safetyProbsWaterTankTrimmedBaseline.npy")

    run_times_trimmed_negMoS = np.load(RESULTS_FOLDER_NEG_TRIMMED_BASELINE + "runtimesWaterTankTrimmedBaseline_negMoS.npy")
    safety_probs_trimmed_negMoS = np.load(RESULTS_FOLDER_NEG_TRIMMED_BASELINE + "safetyProbsWaterTankTrimmedBaseline_negMoS.npy")

    init_wls = np.load(RESULTS_FOLDER_BASELINE + "/initwls.npy")

    # print(run_times_untrimmed)
    # print(run_times_trimmed)

    # print(safety_probs_untrimmed)
    # print(safety_probs_trimmed)
    
    # print(np.amax(run_times_untrimmed))

    X,Y = np.meshgrid(init_wls,init_wls)


    ## plot safety chances
    ax = plt.axes(projection='3d')
    ax.scatter3D(Y, X, safety_probs_untrimmed, color='green')
    ax.scatter3D(Y, X, safety_probs_trimmed, color='red')
    ax.scatter3D(Y, X, safety_probs_trimmed_negMoS, color='blue')

    plt.xlabel('Initial Tank 1 Water Level',fontsize=12)
    plt.ylabel('Initial Tank 2 Water Level',fontsize=12)
    ax.set_zlabel('Safety Probability',fontsize=12)
    plt.savefig(IMAGES_FOLDER + '/safetyProbsPlotWithNeg.png')
    # plt.show()
    plt.clf()

    ## plot runtimes
    ax2 = plt.axes(projection='3d')
    ax2.scatter3D(Y, X, np.log10(run_times_untrimmed), color='green')
    ax2.scatter3D(Y, X, np.log10(run_times_trimmed), color='red')
    # ax2.scatter3D(Y, X, np.log10(run_times_trimmed_negMoS), color='blue')

    plt.xlabel('Initial Tank 1 Water Level',fontsize=12)
    plt.ylabel('Initial Tank 2 Water Level',fontsize=12)
    ax2.set_zlabel('Runtime (log(s))',fontsize=12)
    plt.savefig(IMAGES_FOLDER + '/runTimesPlotWithNeg.png')
    # plt.show()
    plt.clf()



if __name__ == "__main__":
    main()