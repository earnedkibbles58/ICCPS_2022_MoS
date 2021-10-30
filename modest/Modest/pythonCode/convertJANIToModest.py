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

    MODEST_PATH = "../modest"

    MODEL_ROOT_FOLDER = "../../../models/"

    for subdir, dirs, files in os.walk(MODEL_ROOT_FOLDER):
        for file in files:
            if file.endswith('.jani'):
                print(os.path.join(subdir, file))
                print(subdir)

                modest_file = os.path.join(subdir, file.replace(".jani",".modest"))
                proc = subprocess.Popen([MODEST_PATH, 'convert', os.path.join(subdir,file),'-O', modest_file], stdout=PIPE, stderr=PIPE)

                if proc.returncode == 0:
                    pass
                else:
                    print(proc.stdout)

if __name__ == "__main__":
    main()



