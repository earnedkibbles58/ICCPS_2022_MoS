import os
import numpy as np
import subprocess
from subprocess import PIPE, STDOUT

def parseLSSFile(OUTPUT_FILE):
    f = open(OUTPUT_FILE,"r")
    tmp = f.read()
    lines = tmp.splitlines()
    probLine = lines[7]
    prob = float(probLine.split(" ")[-1])

    timeLine = lines[4]
    time = float(timeLine.split(" ")[-1].split('\u202f')[0])

    print(prob)
    print(time)

    return prob,time

def main():

    MODEST_PATH = "/data2/mcleav/modest/Modest/modest"
    AEBS_PATH_WR = "/data2/mcleav/modest/Modest/AEBS/olegBaselines/withRounding/dist_60.000000_vel_20.000000_deltad_0.500000_deltav_0.400000/latticeForSMC.modest"
    AEBS_PATH_NR = "/data2/mcleav/modest/Modest/AEBS/olegBaselines/noRounding/dist_60.000000_vel_20.000000_deltad_0.500000_deltav_0.400000/latticeForSMC.modest"
    OUTPUT_FILE = "/data2/mcleav/modest/Modest/pythonCode/modestOutputFiles/tempLSSRes.txt"
    RES_FILE_WR = "/data2/mcleav/modest/Modest/pythonCode/modestOutputFiles/AEBS_WR_LSSRes.txt"
    RES_FILE_NR = "/data2/mcleav/modest/Modest/pythonCode/modestOutputFiles/AEBS_NR_LSSRes.txt"

    runWR = True
    runNR = False

    # empty files
    if runWR:
        with open(RES_FILE_WR,"w"):
            pass
    if runNR:
        with open(RES_FILE_NR,"w"):
            pass
    
    initDs = [40,45,50,55]
    initVs = [10,15]

    deld = 0.5
    delv = 0.4

    for initd in initDs:
        for initv in initVs:

            didInit = int(initd/deld)+1
            vidInit = int(initv/delv)+1

            proc = None
            # proc = subprocess.run([MODEST_PATH, 'simulate', AEBS_PATH,'--lss', 'smart', '-O', OUTPUT_FILE,'-W','0.005','-L','1000','-E',"didInit=" + str(didInit) + ",vidInit=" + str(vidInit)], stdout=PIPE, stderr=PIPE)
            
            if runWR:
                proc = subprocess.Popen([MODEST_PATH, 'simulate', AEBS_PATH_WR,'--lss', 'smart','-O', OUTPUT_FILE,'-Y','-W','0.005','-E',"didInit=" + str(didInit) + ",vidInit=" + str(vidInit)])

                try:
                    proc.wait()
                    # out, err = proc.communicate()
                    # print(out)
                    # print(err)
                    # proc = subprocess.run([MODEST_PATH,'simulate', AEBS_PATH_WR,'-N', '1','-R','Uniform','-O', OUTPUT_FILE,'-Y','-W','0.005','-L','1000','-E',"didInit=" + str(didInit) + ",vidInit=" + str(vidInit)]
                    prob,time = parseLSSFile(OUTPUT_FILE)
                    strToSave = "initd=" + str(initd) + ",initv=" + str(initv) + ",prob=" + str(prob) + ",time=" + str(time) + "\n"
                    print(strToSave)
                    with open(RES_FILE_WR,"a") as myfile:
                        myfile.write(strToSave)
                except KeyboardInterrupt:
                    try:
                        proc.kill()
                        print("Killed by user")
                    except OSError:
                        pass
                    # proc.wait()

            if runNR:
                proc = subprocess.Popen([MODEST_PATH, 'simulate', AEBS_PATH_NR,'--lss', 'smart','-O', OUTPUT_FILE,'-Y','-W','0.005','-E',"didInit=" + str(didInit) + ",vidInit=" + str(vidInit)])

                try:
                    proc.wait()
                    # out, err = proc.communicate()
                    # print(out)
                    # print(err)
                    # proc = subprocess.run([MODEST_PATH,'simulate', AEBS_PATH_WR,'-N', '1','-R','Uniform','-O', OUTPUT_FILE,'-Y','-W','0.005','-L','1000','-E',"didInit=" + str(didInit) + ",vidInit=" + str(vidInit)]
                    prob,time = parseLSSFile(OUTPUT_FILE)
                    strToSave = "initd=" + str(initd) + ",initv=" + str(initv) +",prob=" + str(prob) + ",time=" + str(time) + "\n"
                    print(strToSave)
                    with open(RES_FILE_NR,"a") as myfile:
                        myfile.write(strToSave)
                except KeyboardInterrupt:
                    try:
                        proc.kill()
                        print("Killed by user")
                    except OSError:
                        pass
                    # proc.wait()

if __name__ == "__main__":
    main()



