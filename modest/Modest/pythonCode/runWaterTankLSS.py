import os
import numpy as np
import subprocess
from subprocess import PIPE, STDOUT
import math

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
    WT_PATH_WR = "/data2/mcleav/modest/Modest/waterTank/nonIntVals/withRounding.modest"
    WT_PATH_NR = "/data2/mcleav/modest/Modest/waterTank/nonIntVals/noRounding.modest"
    OUTPUT_FILE = "/data2/mcleav/modest/Modest/pythonCode/modestOutputFiles/tempLSSRes_waterTank.txt"
    RES_FILE_WR = "/data2/mcleav/modest/Modest/pythonCode/modestOutputFiles/WaterTank_WR_LSSRes.txt"
    RES_FILE_NR = "/data2/mcleav/modest/Modest/pythonCode/modestOutputFiles/WaterTank_NR_LSSRes.txt"

    runWR = True
    runNR = True

    # empty files
    if runWR:
        with open(RES_FILE_WR,"w"):
            pass
    if runNR:
        with open(RES_FILE_NR,"w"):
            pass
    
    initWLs = [10,25,50,75,90]

    delwl = 4

    for initwl1 in initWLs:
        for initwl2 in initWLs:
            wl1idInit = math.ceil(initwl1/delwl)
            wl2idInit = math.ceil(initwl2/delwl)

            proc = None
            # proc = subprocess.run([MODEST_PATH, 'simulate', AEBS_PATH,'--lss', 'smart', '-O', OUTPUT_FILE,'-W','0.005','-L','1000','-E',"didInit=" + str(didInit) + ",vidInit=" + str(vidInit)], stdout=PIPE, stderr=PIPE)
            
            if runWR:
                proc = subprocess.Popen([MODEST_PATH, 'simulate', WT_PATH_WR,'--unsafe','--lss', 'smart','-O', OUTPUT_FILE,'-Y','-W','0.005','-E',"wlidInit1=" + str(wl1idInit) + ",wlidInit2=" + str(wl2idInit) + ",initContAction1=0,initContAction2=0"])

                try:
                    proc.wait()
                    # out, err = proc.communicate()
                    # print(out)
                    # print(err)
                    # proc = subprocess.run([MODEST_PATH,'simulate', WT_PATH_WR,'-N', '1','-R','Uniform','-O', OUTPUT_FILE,'-Y','-W','0.005','-L','1000','-E',"didInit=" + str(didInit) + ",vidInit=" + str(vidInit)]
                    prob,time = parseLSSFile(OUTPUT_FILE)
                    strToSave = "wlidInit1=" + str(wl1idInit) + ",wlidInit2=" + str(wl2idInit) + ",initContAction1=0,initContAction2=0" + ",prob=" + str(prob) + ",time=" + str(time) + "\n"
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
                proc = subprocess.Popen([MODEST_PATH, 'simulate', WT_PATH_NR,'--unsafe','--lss', 'smart','-O', OUTPUT_FILE,'-Y','-W','0.005','-E',"wlidInit1=" + str(wl1idInit) + ",wlidInit2=" + str(wl2idInit) + ",initContAction1=0,initContAction2=0"])

                try:
                    proc.wait()
                    # out, err = proc.communicate()
                    # print(out)
                    # print(err)
                    # proc = subprocess.run([MODEST_PATH,'simulate', WT_PATH_WR,'-N', '1','-R','Uniform','-O', OUTPUT_FILE,'-Y','-W','0.005','-L','1000','-E',"didInit=" + str(didInit) + ",vidInit=" + str(vidInit)]
                    prob,time = parseLSSFile(OUTPUT_FILE)
                    strToSave = "wlidInit1=" + str(wl1idInit) + ",wlidInit2=" + str(wl2idInit) + ",initContAction1=0,initContAction2=0" + ",prob=" + str(prob) + ",time=" + str(time) + "\n"
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



