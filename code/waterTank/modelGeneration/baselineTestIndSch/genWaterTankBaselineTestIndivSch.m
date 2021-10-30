%% This script builds the lattice
% The lattice is a 1-d array of custom structs
% Each struct contains the water level (and unique id), along with a map struct that maps 
% Ns to an array which corresonds to the lattice points that the K value
% associated with the array index maps to

clear; close all;
format long

%% Define hyper parameters
inflow = 5.5;
outflow = 2.1;
deltawl = 5;
wlMax=26;
baseline = initWaterTankBaseline(wlMax,deltawl);

%% Untrimmed model
N=1;
trimmed=0;
lattice = addWaterTankBaselineTransitions(baseline,N,deltawl,inflow,outflow,trimmed);
modelFolder = '../../../../models/waterTank/BaselineTestIndivSchOneTank/if' + string(inflow) + '_of' + string(outflow) + '_deltawl' + string(deltawl) + '_wlmax' + string(wlMax);
mkdir(modelFolder)
modelFile = '../../../../models/waterTank/BaselineTestIndivSchOneTank/if' + string(inflow) + '_of' + string(outflow) + '_deltawl' + string(deltawl) + '_wlmax' + string(wlMax) + '/waterTankBaseline.prism';
convertWaterTankBaselineToPRISMModelMultiTank(lattice,N,modelFile,deltawl,trimmed,1);