# ICCPS_2022


This repo contains the code for reproducing the experiments for the ICCPS 2022 paper "Monotonic Safety for
Scalable and Data-Efficient Probabilistic Safety Analysis"



The first step to reproduce the experiments is to obtain the docker image from ADD DOCKER LINK HERE!!!!!


The experiments have 3 components to them:
1) Model generation: The code for generating the models is located in the */ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/modelGeneration* and */ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/modelGeneration* directories. However, we don't consider this to be part of the repeatability package, so please ignore them.
2) Model checking: The code for model checking (both probabilistic model checking and statistical model checking) is located in */ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments* and */ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments*.
3) Vizualization: The code for visualizing the model checking results is located in */ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments* and */ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments*.



Caveats: 
1) Figures 3, 5, and 6 all use 3-d plots. To get as good of a 2-d view of these 3-d plots, we didn't save the figure directly in the script. Instead, we visualized the 3-d plot in an interactive pyplot figure window and then manually found the best view. Due to the use of docker, this is not possible in this package. So the viewpoints of figures 3, 5, and 6 from the paper will be different than those generated as a part of the repeatability pacakge.
2) Due to differences in computing power, the absolute runtimes of the PRISM and Modest model checking tools will be different. However, the rleative runtimes should be similar (i.e. the untrimmed models should take longer to run than the trimmed models and the ratios of these runtimes should be close to those of the results reported in the paper).
3) The Modest tool (used for table 1, table 2 and figure 6) ilikes to use as many cpus as possible while performing statistical model checking. To limit the number of cores it uses, see the '-J','2' parameter in the python3 scripts, which tells the tool to only use at most 2 cores. For example, to limit Modest to only using 1 core replace '2' with '1'. Note that this will increase the runtime of the code.
4) We formatted the figure windows for figures 2 and 4, so the saved figures will have different spacing than those in the paper.


ADD IN RUNTIME OF AEBS MOS ASSUMPTION!!!!!!

We have divided the instructions for the reproducability package by each figure/table. The parentheses indicate the expected runtime of each script. The visualization scripts all have negligible runtimes.

Figure 2:

`cd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/diffDeltaDs
python3 runAEBSDiffDeltaDs_baseline.py (2 mins)
python3 runAEBSDiffDeltaDs_trimmedbaseline.py (30 seconds)
python3 visAEBSDiffDeltaDsResults.py
`

The one plot that gets saved is
*/ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/diffDeltaDs_MC/plots/AEBSDiffDeltaDsPlot.png*


Figure 3:
`
cd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/largeModelMC/
python3 runAEBSScalabilityMC_baseline.py (7 mins)
python3 runAEBSScalabilityMC_trimmedBaseline.py (3 mins)
python3 runAEBSScalabilityMC_trimmedBaseline_negMoS.py (6 mins)
python3 visAEBSScalabilityResults.py
`
The two plots that get saved are
*/ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/largeModel_MC/plots/runTimesPlotWithNeg.png*
*/ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/largeModel_MC/plots/safetyProbsPlotWithNeg.png*

Figure 4:
`
cd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/diffWLDeltas/
python3 runWaterTankDiffDeltaWLs_baseline.py (30 mins)
python3 runWaterTankDiffDeltaWLs_trimmedBaseline.py (17 mins)
python3 visWaterTankDiffDeltaWLs.py
`
The one plot that get saved is
*/ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/diffWLDeltas/plots/if13.5_of4.3_numSteps10/waterTankDiffWLsPlot.png*


Figure 5:
`
cd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/largeModelMC/
python3 runWaterTankScalabilityMC_baseline.py (18 hours)
python3 runWaterTankScalabilityMC_trimmedbaseline.py (73 mins)
python3 runWaterTankScalabilityMC_trimmedbaseline_negMoS.py (9 mins)
python3 visWaterTankScalabilityResults.py
`
The two plots that get saved are:
*/ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_MC/plots/if13.5_of4.3_deltawl5_numSteps10/runTimesPlotWithNeg.png*
*/ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_MC/plots/if13.5_of4.3_deltawl5_numSteps10/safetyProbsPlotWithNeg.png*

Tables 1 and 2:
These scripts run 10 times for each model and number of schedulers. If they are taking too long, feel free to lower that number by changing the iter_per_init variable in each of the runAEBSScalability*.py scripts. However, the results are technically random so it is recomended to run no fewer than 3 iterations. Because the results are random, the safety probabilities will not exactly match those reported in the paper, but they should be very similar.
`
cd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/largeModelSMC/
python3 runAEBSScalabilitySMC_baseline.py (4.5 hours)
python3 runAEBSScalabilitySMC_trimmedbaseline.py (2.5 hours)
python3 runAEBSScalabilitySMCFewSchSamples_trimmedbaseline.py (10 mins)
python3 visAEBSScalabilityResultsSMC.py > tempOutput.txt
`
The results will be saved to
*/ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/largeModelSMC/tempOutput.txt*

Figure 6:
These experiments run 10 times for each model and number of schedulers. If they are taking too long, feel free to lower that number by changing the iter_per_init variable in each of the runAEBSScalability*.py scripts. However, the results are technically random so it is recomended to run no fewer than 3 iterations. Because the results are random, the safety probabilities will not exactly match those reported in the paper, but they should be very similar.
`
cd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/largeModelSMC/
python3 runAEBSScalabilitySMC_baseline.py (9 mins)
python3 runAEBSScalabilitySMC_trimmedbaseline.py (9 mins)
python3 runAEBSScalabilitySMCFewSchSamples_trimmedbaseline.py (3 mins)
python3 visAEBSScalabilityResultsSMC.py
`
The two plots at get saved are
*/ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_SMC/plots/if13.5_of4.3_deltawl5_numSteps10/runTimesPlot_withFew.png*
*/ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_SMC/plots/if13.5_of4.3_deltawl5_numSteps10/safetyProbsPlot_withFew.png*

Section 6.4 text:

cd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/testIndivSch/
python3 checkStrongMoSAssn.py (FIGURE OUT THIS RUNTIME. It will be painfully long...)

The results will be printed in 
*/ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/testIndivSch/H3L3/N_1/dist_9_vel_1.2_deltad_1_deltav_0.4/checkStrongMoSAssn.txt*

The 'next state:' line of the file indicates the state pairs being compared ([d1 v1 d2 v2]) and the 'Prob MoS Holds over sch:' line gives the proportion of schedulers over which MoS holds for that state pair. To see what this file should contain after running the experiment, see
*/ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/testIndivSch/H3L3/N_1/dist_9_vel_1.2_deltad_1_deltav_0.4/fullStrongMoSAssn.txt*


Table 3:

cd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/testIndivSch/
python3 checkStrongMoSAssn.py (3 hours)

The results will be printed in */ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/testIndivSchOneTank/if5.5_of2.1_deltawl5_numSteps10_wlmax26/checkStrongMoSAssn.txt*

The 'next state:' line of the file indicates the state pair being compared ([wl1 wl2]) and the 'Prob MoS Holds over sch:' gives the proportion of schedulers over which MoS holds for that state pair. To see what this file should contain after running the experiment, see the file contents before running checkStrongMoSAssn.py

