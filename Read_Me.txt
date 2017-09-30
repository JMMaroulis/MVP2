Quick Running notes:

Main_Experiment_Run:
Arguments: width, height, p1, p2, p3, equilibration_time, num_readings_per_instance, correlation_buffer, visualisation, increment

width : width of grid
height : height of grid
p1 : Infection Probability start value
p2 : Recovery Probability start value
p3 : Susceptibility Probability start value
equilibration_time : number of sweeps for each p1 - p3 combination to equilibrate before measurements get taken
num_readings_per_instance : number of measurements per p1 - p3 combination
correlation_buffer : number of sweeps between measurements
visualisation : 1 = on, 2 = off
increment : amount by which p1/p3 increase per loop

data gets placed in "infection_fraction.txt"

----

Immune_Experiment_Run : 
Arguments: width, height, p1, p2, p3, equilibration_time, num_readings_per_instance, correlation_buffer, visualisation, increment, p_immune

Same as Main_Experiemtn_Run, with one exception;
p_immune : chance of cell being immune. Informs number of immune cells.

data gets placed in "immune_fraction.txt"

----

Visulisation:

For both of the above, to see visualisation without measurements and such causing stuttering, just set the 
equilibration time to be arbitrarily long on your probabilities of choice.

For main;
S - Blue
I - green
R - Red

For Immune;
S - Dark Blue
I - Light Blue
R - Yellow
Immune - Red

----

data output structure:

average_infection_fraction, p1, (p3/p_immune respectively), average_infection_fraction_variance.
Apologies for the odd data structure.
Irritatingly, I couldn't save the contour plots in ideal format, only with screenshots;
To recreate original in gnuplot:
>set palette
>set pm3d
>splot "data_file.txt" using 3:2:4:1 with pm3d
Results in height being variance, colouration being average infection.

Arguments used for each data file and contour plot:

Main:
50 50 0.025 0.5 0.025 500 50 20 0 0.025

Immune:
50 50 0.025 0.5 0.5 500 50 20 1 0.025 0.025

----

The three .png files have the plots for the absorbing state, dynamic equilibrium, and the waves.

Parameters for each:

Absorbing State:
p1: 0.5, p2: 0.2, p3: 0.01.

Dynamic equilibrium:
p1 = p2 = p3 = 0.5

Waves:
P1: 0.8, p2: 0.1, p3: 0.01

Wave periodicity estimate:
Approximately 150 sweeps between each wave peak.


