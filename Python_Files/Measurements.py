import numpy
import sys
import Methods

# Measurement methods go in here


# Calculates infected fraction of state
def infected_fraction(state):
    width = len(state)
    height = len(state[0])
    infect_count = 0
    for i in range(0, width):
        for j in range(0, height):
            if Methods.get_cell(state, i, j) == 1:
                infect_count += 1

    return infect_count / float(width * height)


def write_all_to_file(p1_list, p3_list, average_infected_fraction_list, infected_fraction_variance_list, p1, p2, p3, immune):

    # declare files
    if immune == 0:
        p1_inf = open("infection_fraction.txt", "w")
    elif immune == 1:
        p1_inf = open("immune_fraction.txt", "w")

    for x in range(0, len(p1_list)):
        a = average_infected_fraction_list[x]
        b = p1_list[x]
        c = p3_list[x]
        d = infected_fraction_variance_list[x]
        p1_inf.write('%s' % a)
        p1_inf.write(' ')
        p1_inf.write('%s' % b)
        p1_inf.write(' ')
        p1_inf.write('%s' % c)
        p1_inf.write(' ')
        p1_inf.write('%s \n' % d)

    p1_inf.close()

def generate_stats(infected_fraction_list, average_infection_fraction_list, variance_list, num_readings_per_instance):

    num_instances = len(infected_fraction_list) / (num_readings_per_instance+1)
    pos = 0
    I_avg = 0
    I_avg_2 = 0
    I2_avg = 0
    counter = 1

    while True:

        # out of bounds
        if pos >= len(infected_fraction_list):
            return

        # blank line
        if isinstance(infected_fraction_list[pos], basestring):

            # put blank line in lists
            average_infection_fraction_list.append(' ')
            variance_list.append(' ')

            print(I_avg_2, I2_avg, I_avg, counter)

            I_avg_2 = 0
            I2_avg = 0
            I_avg = 0

        # end of block of constant p1 and p3
        if counter == num_readings_per_instance:

            # calculate <I>
            I_avg /= float(num_readings_per_instance)

            # calculate <I>^2
            I_avg_2 /= float(num_readings_per_instance)
            I_avg_2 **= 2

            # calculate <I^2>
            I2_avg /= float(num_readings_per_instance)

            # variance = <I^2> - <I>^2 / N
            var = abs(I_avg_2 - I2_avg) / float(num_readings_per_instance)

            # append to lists
            variance_list.append(var)
            average_infection_fraction_list.append(I_avg)

            I_avg_2 = 0
            I2_avg = 0
            I_avg = 0
            counter = 0

        # regular stuff
        if isinstance(infected_fraction_list[pos], basestring) == False:

            # sum I
            I_avg += infected_fraction_list[pos]

            # Sum I
            I_avg_2 += infected_fraction_list[pos]

            # Sum I^2
            I2_avg += infected_fraction_list[pos] ** 2
            counter += 1



        pos += 1

