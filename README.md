# ICCPS_2022


This repo contains the code for reproducing the experiments for the ICCPS 2022 paper "Monotonic Safety for
Scalable and Data-Efficient Probabilistic Safety Analysis"



The first step to reproduce the experiments is to obtain the docker image from ADD DOCKER LINK HERE!!!!!


The experiments have 3 components to them:
1) Model generation: The code for generating the models is located in the code/AEBS/modelGeneration and code/waterTank/modelGeneration directories. However, we don't consider this to be part of the repeatability package, so please ignore them.
2) Model checking: The code for model checking (both probabilistic model checking and statistical model checking) is located in code/AEBS/experiments and code/waterTank/experiments.
3) Vizualization: The code for visualizing the model checking results is located in code/AEBS/experiments and code/waterTank/experiments.



Caveats: 
1) Figures 3, 5, and 6 all use 3-d plots. To get as good of a 2-d view of these 3-d plots, we didn't save the figure directly in the script. Instead, we visualized the 3-d plot in an interactive pyplot figure window and then manually found the best view. Due to the use of docker, this is not possible in this package. So the viewpoints of figures 3, 5, and 6 from the paper will be different than those generated as a part of the repeatability pacakge.
2) Due to differences in computing power, the absolute runtimes of the PRISM and Modest model checking tools will be different. However, the rleative runtimes should be similar (i.e. the untrimmed models should take longer to run than the trimmed models and the ratios of these runtimes should be close to those of the results reported in the paper).
3) The Modest tool (used for table 1, table 2 and figure 6) likes to use as many cpus as possible while performing statistical model checking. To limit the number of cores it uses, see the '-J','40' parameter in the python3 scripts. For example, to limit Modest to only using 1 core replace '40' with '1'. Note that this will greatly increase the runtime of the code.




We have divided the instructions for the reproducability package by each figure/table.

Figure 2:

cd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/diffDeltaDs
python3 runAEBSDiffDeltaDs_baseline.py
python3 runAEBSDiffDeltaDs_trimmedbaseline.py
python3 visAEBSDiffDeltaDsResults.py



Figure 3:

cd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/largeModelMC/
python3 runAEBSScalabilityMC_baseline.py
python3 runAEBSScalabilityMC_trimmedBaseline.py
python3 runAEBSScalabilityMC_trimmedBaseline_negMoS.py
python3 visAEBSScalabilityResults.py



Figure 4:

cd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/diffWLDeltas/
python3 runWaterTankDiffDeltaWLs_baseline.py
python3 runWaterTankDiffDeltaWLs_trimmedBaseline.py
python3 visWaterTankDiffDeltaWLs.py



Figure 5:

cd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/largeModelMC/
python3 runWaterTankScalabilityMC_baseline.py
python3 runWaterTankScalabilityMC_trimmedbaseline.py
python3 runWaterTankScalabilityMC_trimmedbaseline_negMoS.py
python3 visWaterTankScalabilityResults.py



Tables 1 and 2:
These experiments run 10 times for each model and number of schedulers. If they are taking too long, feel free to lower that number by changing the iter_per_init variable in each of the runAEBSScalability*.py scripts.

cd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/largeModelSMC/
python3 runAEBSScalabilitySMC_baseline.py
python3 runAEBSScalabilitySMC_trimmedbaseline.py
python3 runAEBSScalabilitySMCFewSchSamples_trimmedbaseline.py
python3 visAEBSScalabilityResultsSMC.py


Figure 6:
These experiments run 10 times for each model and number of schedulers. If they are taking too long, feel free to lower that number by changing the iter_per_init variable in each of the runAEBSScalability*.py scripts.

cd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/largeModelSMC/
python3 runAEBSScalabilitySMC_baseline.py
python3 runAEBSScalabilitySMC_trimmedbaseline.py
python3 runAEBSScalabilitySMCFewSchSamples_trimmedbaseline.py
python3 visAEBSScalabilityResultsSMC.py


Section 6.4 text:

cd /ICCPS_2022_MoS-repeatabilityPackage/code/AEBS/experiments/testIndivSch/
python3 checkStrongMoSAssn.py

The results will be printed in /ICCPS_2022_MoS-repeatabilityPackage/results/AEBS/testIndivSch/H3L3/N_1/dist_9_vel_1.2_deltad_1_deltav_0.4/checkStrongMoSAssn.txt

ADD PARAGRAPH EXPLAINING THE FORMAT OF THE RESULTS!!!!!!!

Table 3:

cd /ICCPS_2022_MoS-repeatabilityPackage/code/waterTank/experiments/testIndivSch/
python3 checkStrongMoSAssn.py

The results will be printed in /ICCPS_2022_MoS-repeatabilityPackage/results/waterTank/testIndivSchOneTank/if5.5_of2.1_deltawl5_numSteps10_wlmax26/checkStrongMoSAssn.txt

ADD PARAGRAPH EXPLAINING THE FORMAT OF THE RESULTS!!!!!!!
