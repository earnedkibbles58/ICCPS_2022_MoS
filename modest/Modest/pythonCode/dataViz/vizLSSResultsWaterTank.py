
import math
import numpy as np
import os


import matplotlib.pyplot as plt




initWLs = [10,25,50,75,90]

delwl = 4


def PARSE_RES_FILE(RES_FILE):

    global initWLs,delwl

    DATA_PROBS = []
    DATA_TIMES = []

    TEMP_DATA_PROBS = []
    TEMP_DATA_TIMES = []

    numWLsPerLine = 5
    counter = 0
    f = open(RES_FILE,"r")
    lines = f.readlines()
    for line in lines:
        counter+=1
        temp_line = line.split(",")
        print(temp_line)

        wl1id_line = temp_line[0]
        wl1id = float(wl1id_line.split("=")[1])
        print(wl1id)

        wl2id_line = temp_line[1]
        wl2id = float(wl2id_line.split("=")[1])
        print(wl2id)

        prob_line = temp_line[4]
        prob = float(prob_line.split("=")[1])
        print(prob)

        time_line = temp_line[5]
        time = float(time_line.split("=")[1].splitlines()[0])
        print(time)

        TEMP_DATA_PROBS.append(prob)
        TEMP_DATA_TIMES.append(time)

        if counter == numWLsPerLine:
            DATA_PROBS.append(TEMP_DATA_PROBS)
            DATA_TIMES.append(TEMP_DATA_TIMES)

            TEMP_DATA_PROBS = []
            TEMP_DATA_TIMES = []
            counter = 0
    return DATA_PROBS,DATA_TIMES

def main():
    RES_FILE_WR = "/data2/mcleav/modest/Modest/pythonCode/modestOutputFiles/WaterTank_WR_LSSRes.txt"
    RES_FILE_NR = "/data2/mcleav/modest/Modest/pythonCode/modestOutputFiles/WaterTank_NR_LSSRes.txt"


    # load data
    data_wr_probs,data_wr_times = PARSE_RES_FILE(RES_FILE_WR)
    data_nr_probs,data_nr_times = PARSE_RES_FILE(RES_FILE_NR)

    initWLs = [10,25,50,75,90]

    ## plot probabilities
    X,Y = np.meshgrid(initWLs,initWLs)

    ax = plt.axes(projection='3d')
    ax.scatter3D(Y, X, data_nr_probs, color='green')
    ax.scatter3D(Y, X, data_wr_probs, color='red')
    plt.xlabel('Tank 1 Initial Water Level',fontsize=12)
    plt.ylabel('Tank 2 Initial Water Level',fontsize=12)
    ax.set_zlabel('Crash Chance',fontsize=12)
    # plt.zlabel('Crash Chance')
    # plt.title('Computed Crash Probabilities')
    # plt.show()
    plt.savefig('results/waterTankResults/crashChancesLSS.png')
    plt.clf()

    ## plot probabilities
    ax = plt.axes(projection='3d')
    ax.scatter3D(Y, X, data_nr_times, color='green')
    ax.scatter3D(Y, X, data_wr_times, color='red')
    plt.xlabel('Tank 1 Initial Water Level',fontsize=12)
    plt.ylabel('Tank 2 Initial Water Level',fontsize=12)
    ax.set_zlabel('SMC Runtimes',fontsize=12)
    # plt.zlabel('Crash Chance')
    # plt.title('Computed Crash Probabilities')
    # plt.show()
    plt.savefig('results/waterTankResults/runTimesLSS.png')


if __name__ == "__main__":
    main()



