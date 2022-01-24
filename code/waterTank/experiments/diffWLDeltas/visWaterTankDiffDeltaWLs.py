import numpy as np
import os

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def main():

    inflow = 13.5
    outflow = 4.3
    numSteps = 10

    # load data
    RESULTS_FOLDER_BASELINE = "../../../../results/waterTank/diffWLDeltas/baseline/if" + str(inflow) + "_of" + str(outflow) + "_numSteps" + str(numSteps) + "/"
    RESULTS_FOLDER_TRIMMED_BASELINE = "../../../../results/waterTank/diffWLDeltas/trimmedBaseline_MC/if" + str(inflow) + "_of" + str(outflow) + "_numSteps" + str(numSteps) + "/"


    IMAGES_FOLDER = "../../../../results/waterTank/diffWLDeltas/plots/if" + str(inflow) + "_of" + str(outflow) + "_numSteps" + str(numSteps) + "/"
    try:
        os.makedirs(IMAGES_FOLDER)
    except OSError as e:
        pass

    run_times_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "runtimesWaterTankBaseline.npy")[0:-1]
    safety_probs_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "safetyProbsWaterTankBaseline.npy")[0:-1]
    delta_wls_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "/deltaWLs.npy")[0:-1]

    run_times_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "runtimesWaterTankBaseline.npy")[0:-1]
    safety_probs_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "safetyProbsWaterTankBaseline.npy")[0:-1]

    print(delta_wls_untrimmed)
    print(safety_probs_untrimmed)
    print(safety_probs_trimmed)

    print(run_times_untrimmed)
    print(run_times_trimmed)

    plt.scatter(run_times_untrimmed,safety_probs_untrimmed,color='green',marker='s',s=100)
    plt.scatter(run_times_trimmed,safety_probs_trimmed,color='red',marker='o',s=100)

    # plt.legend(fontsize=40)
    plt.legend(['Baseline','Trimmed'],loc='lower right',fontsize = 20)

    ax = plt.gca()
    ax.set_ylim([0,1])
    # xs = np.arange(0.05,6500,1)

    ax.set_xscale('log')
    ax.set_xlim([10,2000])
    plt.xlabel('Run time (s)',fontsize=20)
    plt.ylabel('Safety Probability',fontsize=20)
    plt.savefig(IMAGES_FOLDER + '/waterTankDiffWLsPlot.png')
    # plt.show()
    plt.clf()




if __name__ == "__main__":
    main()