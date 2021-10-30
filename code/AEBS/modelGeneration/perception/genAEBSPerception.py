import numpy as np
import csv
import math
import os

distDiscs = [0.25,0.3,0.4,0.5,0.6,0.7,0.75,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2]

H = 3
L=3
folderToSave = "models/H" + str(H) + "L" + str(L)
try:
    os.makedirs(folderToSave)
except OSError as e:
    pass

safetyThresh=5
for distDisc in distDiscs:
    speedDisc = 0.4
    B1=int(4/speedDisc)
    B2=int(8/speedDisc)

    # modelFile = open("windowed/diffDistDiscsNew/lecBaselineMajVoteFilterH" + str(H) + "L" + str(L) + "DistDisc" + str(distDisc) + ".prism",'w')

    modelFile = open("models/H" + str(H) + "L" + str(L) + "/distDisc" + str(distDisc) + ".txt",'w')

    # modelFile.write("mdp\n\n")
    # modelFile.write("const int B1=" + str(B1) + ";\n")
    # modelFile.write("const int B2=" + str(B2) + ";\n")
    # modelFile.write("const int TTCThresh = 6;\n")
    # modelFile.write("const int xwarning = 1;\n")
    # modelFile.write("const int freq = 10;\n")
    # modelFile.write("const int fmu=1;\n")
    # modelFile.write("const int Thd=2;\n")

    # modelFile.write("const int initPos;\n")
    # modelFile.write("const int initSpeed;\n")

    # modelFile.write("const int initBrakingFlag;\n")
    # modelFile.write("const int initBraking;\n \n")

    # modelFile.write("const int didThresh;\n\n")

    # modelFile.write("module LECMarkovChain\n\n")

    # modelFile.write("    s : [0..1] init 1;  // 0 is detect, 1 is misdetect\n")
    # modelFile.write("	s2 : [0..1] init 1;\n")
    # if(H==3):
    #     modelFile.write("	s3 : [0..1] init 1;\n\n")
    # if(H==4):
    #     modelFile.write("	s3 : [0..1] init 1;\n\n")
    #     modelFile.write("	s4 : [0..1] init 1;\n\n")
    # if(H==5):
    #     modelFile.write("	s3 : [0..1] init 1;\n\n")
    #     modelFile.write("	s4 : [0..1] init 1;\n\n")
    #     modelFile.write("	s5 : [0..1] init 1;\n\n")
    # if(H==6):
    #     modelFile.write("	s3 : [0..1] init 1;\n\n")
    #     modelFile.write("	s4 : [0..1] init 1;\n\n")
    #     modelFile.write("	s5 : [0..1] init 1;\n\n")
    #     modelFile.write("	s6 : [0..1] init 1;\n\n")
    # if(H==7):
    #     modelFile.write("	s3 : [0..1] init 1;\n\n")
    #     modelFile.write("	s4 : [0..1] init 1;\n\n")
    #     modelFile.write("	s5 : [0..1] init 1;\n\n")
    #     modelFile.write("	s6 : [0..1] init 1;\n\n")
    #     modelFile.write("	s7 : [0..1] init 1;\n\n")

    # modelFile.write("    carSpeed : [0 .. initSpeed] init initSpeed;\n")
    # modelFile.write("    did : [0..initPos] init initPos;\n\n")

    # modelFile.write("    currN : [0..2] init initBrakingFlag;\n")  
    # modelFile.write("    contRegion : [0..2] init 0;\n\n")

    # modelFile.write("    //TTC = did/carSpeed;")
    # modelFile.write("    //xwarning = (did-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)\n")
    # modelFile.write("    // compute controller region\n")
    # modelFile.write("    [] currN=0&((did-" + str(int(safetyThresh/distDisc)) + ")/(carSpeed*" + str(speedDisc/distDisc) + "))>TTCThresh&((" + str(distDisc/speedDisc) + ")*(did-" + str(int(safetyThresh/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)>xwarning ->   (currN'=1)&(contRegion'=0); // safe region\n")
    # modelFile.write("    [] currN=0&((did-" + str(int(safetyThresh/distDisc)) + ")/(carSpeed*" + str(speedDisc/distDisc) + "))>TTCThresh&((" + str(distDisc/speedDisc) + ")*(did-" + str(int(safetyThresh/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)<=xwarning ->  (currN'=1)&(contRegion'=1); // braking region\n")
    # modelFile.write("    [] currN=0&((did-" + str(int(safetyThresh/distDisc)) + ")/(carSpeed*" + str(speedDisc/distDisc) + "))<=TTCThresh&((" + str(distDisc/speedDisc) + ")*(did-" + str(int(safetyThresh/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)>xwarning ->  (currN'=1)&(contRegion'=1); // braking region\n")
    # modelFile.write("    [] currN=0&((did-" + str(int(safetyThresh/distDisc)) + ")/(carSpeed*" + str(speedDisc/distDisc) + "))<=TTCThresh&((" + str(distDisc/speedDisc) + ")*(did-" + str(int(safetyThresh/distDisc)) + ")-fmu*pow(carSpeed,2)/(2*B2))/(carSpeed*Thd)<=xwarning -> (currN'=1)&(contRegion'=2); // collision mitigation region\n\n")

    probs = []
    with open('perceptionData/lecStatefulAverages.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        print(csv_reader)
        for row in csv_reader:
            row = [float(row_) for row_ in row]
            print(row)
            probs.append(row)
    print(probs)




    maxDist = 200/distDisc
    minDist = 0/distDisc
    LECInvervalLen = 10/distDisc


    index = 0
    for prob in probs:

        numHist = math.log(len(prob),2)
        distLower = int((index*LECInvervalLen))
        distUpper = int(((index+1)*LECInvervalLen))

        det_index = 0
        for detProb in prob:
            detProb = abs(detProb)
            s1 = 1-(det_index % 2)
            s2 = 1-(math.floor((det_index/2)) % 2)
            s3 = 1-(math.floor((det_index/4)) % 2)
            s4 = 1-(math.floor((det_index/8)) % 2)
            s5 = 1-(math.floor((det_index/16)) % 2)
            s6 = 1-(math.floor((det_index/32)) % 2)
            s7 = 1-(math.floor((det_index/64)) % 2)

            #modelLine = "    [] currN=0&did<" + str(distUpper) + "&did>=" + str(distLower)+ " -> " + str(detProb) + ":(s'=0)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(currN'=1);\n"
            print(numHist)
            if(numHist==3):
                if(H==2):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(currN'=1);\n"
                if(H==3):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=((0+s2+s3<=2)?1:0)) + " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=((1+s2+s3<=2)?1:0));\n"
                if(H==4):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1);\n"
                if(H==5):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1);\n"
                if(H==6):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1);\n"
                if(H==7):
                    modelLine = "    [] currN=0&s3=" + str(s3) + "&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1);\n"
            elif(numHist==2):
                if(H==2):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(currN'=1);\n"
                if(H==3):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=((0+s2+s3<=2)?1:0)) + " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=((1+s2+s3<=2)?1:0));\n"
                if(H==4):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1);\n"
                if(H==5):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1);\n"
                if(H==6):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1);\n"
                if(H==7):
                    modelLine = "    [] currN=0&s2=" + str(s2) + "&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1);\n"
            elif(numHist==1):
                if(H==2):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(currN'=1);\n"
                if(H==3):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=((0+s2+s3<=2)?1:0)) + " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=((1+s2+s3<=2)?1:0));\n"
                if(H==4):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1);\n"
                if(H==5):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1);\n"
                if(H==6):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1);\n"
                if(H==7):
                    modelLine = "    [] currN=0&s=" + str(s1) + "&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1);\n"
            else:
                if(H==2):
                    modelLine = "    [] currN=0&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(currN'=1);\n"
                if(H==3):
                    modelLine = "    [] currN=0&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=((0+s2+s3<=2)?1:0)) + " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(currN'=1)&(currK'=((1+s2+s3<=2)?1:0));\n"
                if(H==4):
                    modelLine = "    [] currN=0&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(currN'=1);\n"
                if(H==5):
                    modelLine = "    [] currN=0&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(currN'=1);\n"
                if(H==6):
                    modelLine = "    [] currN=0&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(currN'=1);\n"
                if(H==7):
                    modelLine = "    [] currN=0&did<" + str(distUpper) + "&did>=" + str(distLower) + " -> " + str(detProb) + ":(s'=0)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1)+ " + str(1-detProb) + ":(s'=1)&(s2'=s)&(s3'=s2)&(s4'=s3)&(s5'=s4)&(s6'=s5)&(s7'=s6)&(currN'=1);\n"

            #print(modelLine)
            modelFile.write(modelLine)
            det_index+=1
        index+=1


    # if(H==2):
    #     modelFile.write("    // compute did, carSpeed\n")
    #     modelFile.write("    [] currN=2&(s+s2<=0)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq)))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2<=0)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq)))&(carSpeed'=max(0,ceil(carSpeed-(B1/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2<=0)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq)))&(carSpeed'=max(0,ceil(carSpeed-(B2/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2>0)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq)))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2>0)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq)))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2>0)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq)))&(currN'=0);\n\n")
    

    # if(H==3):
    #     modelFile.write("    // compute did, carSpeed\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3<=1)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3<=1)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0,ceil(carSpeed-(B1/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3<=1)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0,ceil(carSpeed-(B2/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3>1)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3>1)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3>1)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n\n")
    
    # if(H==4):
    #     modelFile.write("    // compute did, carSpeed\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4<=1)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4<=1)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0,ceil(carSpeed-(B1/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4<=1)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0,ceil(carSpeed-(B2/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4>1)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4>1)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4>1)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n\n")

    # if(H==5):
    #     modelFile.write("    // compute did, carSpeed\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5<=2)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5<=2)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0,ceil(carSpeed-(B1/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5<=2)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0,ceil(carSpeed-(B2/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5>2)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5>2)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5>2)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n\n")
    # if(H==6):
    #     modelFile.write("    // compute did, carSpeed\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6<=3)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6<=3)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0,ceil(carSpeed-(B1/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6<=3)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0,ceil(carSpeed-(B2/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6>3)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6>3)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6>3)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n\n")

    # if(H==7):
    #     modelFile.write("    // compute did, carSpeed\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6+s7<=3)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6+s7<=3)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0,ceil(carSpeed-(B1/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6+s7<=3)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(carSpeed'=max(0,ceil(carSpeed-(B2/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6+s7>3)&contRegion=0&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6+s7>3)&contRegion=1&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n")
    #     modelFile.write("    [] currN=2&(s+s2+s3+s4+s5+s6+s7>3)&contRegion=2&carSpeed>0&did>0 -> (did'=max(0,floor(did-" + str(speedDisc/distDisc) + "*(carSpeed/freq))))&(currN'=0);\n\n")

    modelFile.write("endmodule")
    modelFile.close()



