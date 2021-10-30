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
    RESULTS_FOLDER_BASELINE = "../../../../results/waterTank/largeModel_SMC_diffSchCounts/baseline/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "/"
    RESULTS_FOLDER_TRIMMED_BASELINE = "../../../../results/waterTank/largeModel_SMC_diffSchCounts/trimmedBaselineSMC/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl) + "_numSteps" + str(numSteps) + "/"
    # RESULTS_FOLDER_NEG_TRIMMED_BASELINE = '../../../../results/waterTank/largeModel_SMC/trimmedBaseline_MC_negMoS/'

    IMAGES_FOLDER = "../../../../results/waterTank/largeModel_SMC_diffSchCounts/plots/if" + str(inflow) + "_of" + str(outflow) + "_deltawl" + str(deltawl)  + "_numSteps" + str(numSteps) + "/"
    try:
        os.makedirs(IMAGES_FOLDER)
    except OSError as e:
        pass

    run_times_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "runtimesAEBSBaseline.npy")
    safety_probs_untrimmed = np.load(RESULTS_FOLDER_BASELINE + "safetyProbsAEBSBaseline.npy")

    run_times_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "runtimesAEBSBaseline.npy")
    safety_probs_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "safetyProbsAEBSBaseline.npy")

    print(safety_probs_untrimmed)

    run_times_untrimmed_average = np.average(run_times_untrimmed,1)
    safety_probs_untrimmed_average = np.average(safety_probs_untrimmed,1)
    safety_probs_untrimmed_var = np.var(safety_probs_untrimmed,1)

    run_times_trimmed_average = np.average(run_times_trimmed,1)
    safety_probs_trimmed_average = np.average(safety_probs_trimmed,1)
    safety_probs_trimmed_var = np.var(safety_probs_trimmed,1)

    # run_times_neg_trimmed = np.load(RESULTS_FOLDER_NEG_TRIMMED_BASELINE + "runtimesAEBSTrimmedBaselineMCNegMoS.npy")
    # safety_probs_neg_trimmed = np.load(RESULTS_FOLDER_NEG_TRIMMED_BASELINE + "safetyProbsAEBSTrimmedBaselineMCNegMoS.npy")

    print(safety_probs_untrimmed)
    print(safety_probs_trimmed)

    sch_counts_baseline = np.load(RESULTS_FOLDER_BASELINE + "/schCounts.npy")
    sch_counts_trimmed = np.load(RESULTS_FOLDER_TRIMMED_BASELINE + "/schCounts.npy")



    plt.plot(sch_counts_baseline,safety_probs_untrimmed_average,color='green')
    plt.plot(sch_counts_trimmed,safety_probs_trimmed_average,color='red')
    plt.xlabel('Schedulers Per LSS',fontsize=12)
    plt.ylabel('Average Safety Probability',fontsize=12)
    plt.savefig(IMAGES_FOLDER + '/safetyProbsPlot.png')
    plt.show()
    plt.clf()



    plt.plot(sch_counts_baseline,safety_probs_untrimmed_var,color='green')
    plt.plot(sch_counts_trimmed,safety_probs_trimmed_var,color='red')
    plt.xlabel('Schedulers Per LSS',fontsize=12)
    plt.ylabel('Safety Probability Variance',fontsize=12)
    plt.savefig(IMAGES_FOLDER + '/safetyProbsVarPlot.png')
    plt.show()
    plt.clf()



    plt.plot(sch_counts_baseline,run_times_untrimmed_average,color='green')
    plt.plot(sch_counts_trimmed,run_times_trimmed_average,color='red')
    plt.xlabel('Schedulers Per LSS',fontsize=12)
    plt.ylabel('Average Run Time',fontsize=12)
    plt.savefig(IMAGES_FOLDER + '/runTimesPlot.png')
    plt.show()
    plt.clf()




if __name__ == "__main__":
    main()