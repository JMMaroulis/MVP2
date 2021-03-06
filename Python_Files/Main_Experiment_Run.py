import Methods
import Measurements
import numpy
import random
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import gc
import cProfile
import time
import copy

# disable garbage collection; makes life a *lot* faster
gc.disable()

# SIRS
# S = 0
# I = 1
# R = 2
# p1 = p(S -> I)
# p2 = p(I -> R)
# p3 = p(R -> S)
width = int(sys.argv[1])
height = int(sys.argv[2])
p1 = float(sys.argv[3])
p2 = float(sys.argv[4])
p3 = float(sys.argv[5])
equilibration_time = int(sys.argv[6])
num_readings_per_instance = int(sys.argv[7])
correlation_buffer = int(sys.argv[8])
visualisation = int(sys.argv[9])
increment = float(sys.argv[10])

# VARIOUS P1 P2 P3 SETTINGS
# WAVES SETTING:
# 0.8 0.1 0.01
# DYNAMIC EQUILIBRIUM SETTING:
# 0.5 0.5 0.5
# ABSORBING STATE:
# 0.5 0.5 0.01

# TIME-BASED RANDOM SEED
random.seed()

# INITIALISE GRIDS
# define two n by m grids;
# 'current' for storing current state,
# 'next' for storing changes during parallel updates
numbers = [0, 1, 2]
current_state = numpy.array([[random.choice(numbers) for a in range(height)] for b in range(width)])
next_state = numpy.array([[random.choice(numbers) for c in range(height)] for d in range(width)])

# pass things to Methods
Methods.set_things(width, height)

# Measurement list
infected_fraction_list = list()
average_infection_fraction_list = list()
p1_list = list()
p3_list = list()
infected_fraction_variance_list = list()
sweep_count = 0
num_readings = 0
p1_changes = 0
p3_changes = 0

# ANIMATION ATTEMPT

"""

# uses parallel updates
def generate_data_SIRS():
    global current_state, next_state, p1, p2, p3, sweep_count, num_readings

    print(sweep_count, equilibration_time)

    # give system time to equilibrate
    if sweep_count <= equilibration_time:
        Methods.sweep_fully_parallel(current_state, next_state, p1, p2, p3)

    # updates/measurements after equilibration
    if sweep_count > equilibration_time:

        # correlation buffer
        for p in range(0, correlation_buffer):
            Methods.sweep_fully_parallel(current_state, next_state, p1, p2, p3)

        # take measurement
        infected_fraction_list.append(Measurements.infected_fraction(current_state))
        num_readings += 1
        print('num_readings', num_readings)

    # increment p1 after sufficient readings; reset sweep_count
    if num_readings == num_readings_per_instance:
        num_readings = 0
        sweep_count = 0
        p1 += 0.05
        print(p1, p3)
        # randomise state
        next_state = numpy.array([[random.choice(numbers) for a in range(height)] for b in range(width)])

    # increment p3 after sufficient p1 increments; reset p1
    if p1 > 1.0:
        p1 = 0.05
        p3 += 0.05
        print(p1, p3)
        # randomise state
        next_state = numpy.array([[random.choice(numbers) for a in range(height)] for b in range(width)])

    current_state = copy.deepcopy(next_state)
    sweep_count += 1
    return current_state

"""


# uses monte-carlo updates
def generate_data_SIRS():
    global current_state, p1, p2, p3, sweep_count, num_readings

    # define conditional return statement
    def ret():

        if visualisation == 1:
            return current_state
        else:
            return

    # t0 = time.time()
    # print t0 - time.time()

    # CONDITIONAL EXITS

    # increment p1 after sufficient readings; reset sweep_count
    if num_readings == num_readings_per_instance:
        num_readings = 0
        sweep_count = 0
        if p1 <= 1.0 and p3 <= 1.0:
            p1_list.append(p1)
            p3_list.append(p3)
        p1 += increment
        print(p1, p3)
        # randomise state
        current_state = numpy.array([[random.choice(numbers) for a in range(height)] for b in range(width)])
        return ret()

    # increment p3 after sufficient p1 increments; reset p1, reset sweep count
    if p1 > 1.0:
        if p1 <= 1.0 and p3 <= 1.0:
            p1_list.append(p1)
            p3_list.append(p3)

        p1 = increment
        p3 += increment
        infected_fraction_list.append(' ')
        p1_list.append(' ')
        p3_list.append(' ')

        print(p1, p3)
        # randomise state
        current_state = numpy.array([[random.choice(numbers) for a in range(height)] for b in range(width)])
        return ret()

    # escape if <I> = 0, should save a lot of time
    if Measurements.infected_fraction(current_state) == 0.0:
        print('KILL')
        while num_readings != num_readings_per_instance:
            # pretend to do sweeps
            infected_fraction_list.append(0.0)
            num_readings += 1
        return ret()

    # END OF CONDITIONAL EXITS
    # BEGINNING OF ACTUAL PROCESS

    # give system time to equilibrate
    if sweep_count <= equilibration_time:
        Methods.sweep_n2_cells(current_state, p1, p2, p3)
        sweep_count += 1
        return ret()

    # updates/measurements after equilibration
    if sweep_count > equilibration_time:

        # correlation buffer
        for p in range(0, correlation_buffer):
            Methods.sweep_n2_cells(current_state, p1, p2, p3)

        # take measurement
        infected_fraction_list.append(Measurements.infected_fraction(current_state))
        num_readings += 1

        return ret()


# keeps animation happy
def update(state):
    mat.set_data(state)
    return mat


# generator to keep animation happy
def data_gen_SIRS():
    while True:
        yield generate_data_SIRS()

# either visualise whilst taking measurements:
if visualisation == 1:
    # code animates happily until visualisation stopped manually
    fig, ax = plt.subplots()
    mat = ax.matshow(generate_data_SIRS())
    plt.colorbar(mat)
    ani = animation.FuncAnimation(fig, update, data_gen_SIRS, interval=50)

    plt.show()

# or don't visualise whilst taking measurements
elif visualisation == 0:
    while p3 <= 1.0:
        generate_data_SIRS()

else:
    print("choose to visualise or not, please.")
    sys.exit()

# re-enable garbage collection
gc.enable()


# generate average list, variance list
Measurements.generate_stats(infected_fraction_list, average_infection_fraction_list, infected_fraction_variance_list,
                            num_readings_per_instance)

# debug
print('FINISHED')
print(len(p1_list))
print(len(p3_list))
print(len(average_infection_fraction_list))
print(len(infected_fraction_variance_list))

# put in files
Measurements.write_all_to_file(p1_list, p3_list, average_infection_fraction_list, infected_fraction_variance_list, p1, p2, p3, 0)







