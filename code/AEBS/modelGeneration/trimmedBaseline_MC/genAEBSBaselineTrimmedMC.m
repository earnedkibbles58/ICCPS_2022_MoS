
clear; close all;
format long

%% Define hyper parameters

deltav=0.4;

B1=4;
B2=8;
fmu=1;
amax=B2;
Thd=2;
xThresh=1;
TTCThresh=6;
freq=10;

numDPerCell=10;
numVPerCell=10;

trimmed = 1;
trimming = 1;

deltad=1;
dists = 100:5:200;
speeds = 10:4:26;
% dists = 10;
% speeds = 2;
N=1;
safetyThresh=5;

H=3;
L=3;
for i=1:length(dists)
    for j=1:length(speeds)
        dist = dists(i);
        speed = speeds(j);
        
        baseline = initAEBSBaseline(dist,speed,deltad,deltav);
        
        %% Add N transitions
        nMax=0;
        
        lattice = addAEBSBaselineTransitions(baseline,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh,numDPerCell,numVPerCell,trimmed);
        nMax = max(nMax,N);
        

        folderName = sprintf('../../../../models/AEBS/trimmedBaseline_MC/H%sL%s/N_%i/dist_%s_vel_%s_deltad_%s_deltav_%s', string(H),string(L),N,string(dist),string(speed),string(deltad),string(deltav));
        fileName = sprintf('../../../../models/AEBS/trimmedBaseline_MC/H%sL%s/N_%i/dist_%s_vel_%s_deltad_%s_deltav_%s/AEBSbaseline_withMCRounding.prism', string(H),string(L),N,string(dist),string(speed),string(deltad),string(deltav));

        mkdir(folderName)
        
        convertAEBSBaselineToPRISMModel(lattice,nMax,fileName,deltad,deltav,amax,trimming,safetyThresh,H,L);

    end
end