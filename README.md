# ICCPS_2022


This repo contains the code for reproducing the experiments for the ICCPS 2022 paper "Monotonic Safety for
Scalable and Data-Efficient Probabilistic Safety Analysis"

Dependencies and Requirements: This package requires docker, linux screen (or mac/windows equivalent) and a machine with an x86 processor and 16Gb of RAM.

The first step to reproduce the experiments is to obtain the docker rar file provided in the REP.


The experiments have 3 components to them:
1) Model generation: The code for generating the models is located in the */ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/modelGeneration* and */ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/modelGeneration* directories. However, we don't consider this to be part of the repeatability package, so please ignore them.
2) Model checking: The code for model checking (both probabilistic model checking and statistical model checking) is located in */ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments* and */ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments*.
3) Vizualization: The code for visualizing the model checking results is located in */ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments* and */ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments*.



Caveats: 
1) Figures 3, 5, and 6 all use 3-d plots. To get as good of a 2-d view of these 3-d plots, we didn't save the figure directly in the script. Instead, we visualized the 3-d plot in an interactive pyplot figure window and then manually found the best view. Due to the use of docker, this is not possible in this package. So the viewpoints of figures 3, 5, and 6 from the paper will be different than those generated as a part of the repeatability pacakge.
2) Due to differences in computing power, the absolute runtimes of the PRISM and Modest model checking tools will be different. However, the rleative runtimes should be similar (i.e. the untrimmed models should take longer to run than the trimmed models and the ratios of these runtimes should be close to those of the results reported in the paper).
3) We formatted the figure windows for figures 2 and 4, so the saved figures will have different spacing than those in the paper.


# Reproducability Instructions

The first step is to get the docker setup. Due to the long runtimes of some of the reproducability scripts, it is recommended to utilize the linux screen function to allow the scripts to run in the background. Navigate to the same directory as the Dockerfile provided and run:

```
docker build . -t iccps_2022mos:latest
screen -S iccps_2022mos
docker run --name iccps_2022mos_container -it iccps_2022mos:latest
```

This should result in a command line within the docker. While some of the longer running scripts are running you can detatch the screen by pressing ctrl-A,ctrl-D and reattatch the screen by running

```
screen -r iccps_2022mos
```

We have divided the instructions for the reproducability package by each figure/table. The parentheses indicate the expected runtime of each script. The visualization scripts all have negligible runtimes.

Figure 2: Expected runtime 3 mins.

```
cd /ICCPS_2022_MoS-repeatabilityPackage
./genFigure2.sh
```

The one plot that gets saved is
*/ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/diffDeltaDs_MC/plots/AEBSDiffDeltaDsPlot.png*


Figure 3: Expected runtime 16 mins.

```
cd /ICCPS_2022_MoS-repeatabilityPackage
./genFigure3.sh
```
The two plots that get saved are
*/ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/largeModel_MC/plots/runTimesPlotWithNeg.png*
*/ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/largeModel_MC/plots/safetyProbsPlotWithNeg.png*

Figure 4: Expected runtime 45 mins.

```
cd /ICCPS_2022_MoS-repeatabilityPackage
./genFigure4.sh
```
The one plot that get saved is
*/ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/diffWLDeltas/plots/if13.5_of4.3_numSteps10/waterTankDiffWLsPlot.png*


Figure 5: Expected runtime 19 hours.

```
cd /ICCPS_2022_MoS-repeatabilityPackage
./genFigure5.sh
```
The two plots that get saved are:
*/ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_MC/plots/if13.5_of4.3_deltawl5_numSteps10/runTimesPlotWithNeg.png*
*/ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_MC/plots/if13.5_of4.3_deltawl5_numSteps10/safetyProbsPlotWithNeg.png*

Tables 1 and 2: Expected runtime 7 hours.

These scripts run 10 times for each model and number of schedulers. If they are taking too long, feel free to lower that number by changing the iter_per_init variable in each of the runAEBSScalability*.py scripts. However, the results are random so it is recomended to run no fewer than 3 iterations. Because the results are random, the safety probabilities will not exactly match those reported in the paper, but they should be very similar.
```
cd /ICCPS_2022_MoS-repeatabilityPackage
./genTables1And2.sh
```
The results will be saved to
*/ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/largeModelSMC/tempOutput.txt*

Figure 6: Expected runtime 21 mins.

These experiments run 10 times for each model and number of schedulers. If they are taking too long, feel free to lower that number by changing the iter_per_init variable in each of the runAEBSScalability*.py scripts. However, the results are technically random so it is recomended to run no fewer than 3 iterations. Because the results are random, the safety probabilities will not exactly match those reported in the paper, but they should be very similar.
```
cd /ICCPS_2022_MoS-repeatabilityPackage
./genFigure6.sh
```
The two plots at get saved are
*/ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_SMC/plots/if13.5_of4.3_deltawl5_numSteps10/runTimesPlot_withFew.png*
*/ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/largeModel_SMC/plots/if13.5_of4.3_deltawl5_numSteps10/safetyProbsPlot_withFew.png*

Section 6.4.1 text: Expected runtime 5 days.

This section takes several days to generate, since it requires running an instance of model checking for every scheduler of the model across 17 pairs of initial conditions. The script runs the state pairs sequentially, saving the results as it goes. In lieu of running the code for all of the 17 state pairs, one could run the code for less time, interrupt the srcipt by pressing ctrl-C, and check that those results match what is reported in the paper. 
```
cd /ICCPS_2022_MoS-repeatabilityPackage
./genSection64.sh
```
The results will be printed in 
*/ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/testIndivSch/H3L3/N_1/dist_9_vel_1.2_deltad_1_deltav_0.4/checkStrongMoSAssn.txt*

The 'next state:' line of the file indicates the state pairs being compared ([d1 v1 d2 v2]) and the 'Prob MoS Holds over sch:' line gives the proportion of schedulers over which MoS holds for that state pair. To see what this file should contain after running the experiment, see
*/ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/testIndivSch/H3L3/N_1/dist_9_vel_1.2_deltad_1_deltav_0.4/fullStrongMoSAssn.txt*


Table 3: Expected runtime 3 hours.

```
cd /ICCPS_2022_MoS-repeatabilityPackage
./genTable3.sh
```
The results will be printed in */ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/testIndivSchOneTank/if5.5_of2.1_deltawl5_numSteps10_wlmax26/checkStrongMoSAssn.txt*

The 'next state:' line of the file indicates the state pair being compared ([wl1 wl2]) and the 'Prob MoS Holds over sch:' gives the proportion of schedulers over which MoS holds for that state pair. To see what this file should contain after running the experiment, see */ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/testIndivSchOneTank/if5.5_of2.1_deltawl5_numSteps10_wlmax26/checkStrongMoSAssn_orig.txt*


The figures and tables and files are contained in the docker container. To extract them to one's own machine exit the docker and copy the */ICCPS_2022_MoS-repeatabilityPackage/results* from the container to one's own file system and examine the figures.

```
exit
docker cp iccps_2022_container:/ICCPS_2022_MoS-repeatabilityPackage/results .
```

Finally, remove the docker

```
docker rm iccps_2022_container
```

