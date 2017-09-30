import random

import numpy

width = int()
height = int()


# transfer things into Methods class for weird reasons
def set_things(w, h):
    global width, height
    width = w
    height = h


# element getter, can deal with looping edges
def get_cell(state, x_pos, y_pos):
    return state[x_pos % width, y_pos % height]


# element setter, can deal with looping edges
def set_cell(state, x_pos, y_pos, new_value):
    state[x_pos % width, y_pos % height] = new_value


# Overwrite grid with immune fraction
def vaccinate(state, p_immune):

    n_immune = int(width * height * p_immune)

    if p_immune > 1:
        return

    print (n_immune)
    count = 0

    # generate immune sites
    while count != n_immune:

        x_pos = numpy.random.randint(0, width, 1, int)
        y_pos = numpy.random.randint(0, height, 1, int)

        z = get_cell(state, x_pos, y_pos)

        # set immunity, check for copies
        if z != 3:
            set_cell(state, x_pos, y_pos, 3)
            count += 1


# chance of 0 -> 1 (if neighbours infected)
def infect(state, new, x_pos, y_pos, p1):
    # check neighbours for infection
    if get_cell(state, x_pos + 1, y_pos) == 1 \
            or get_cell(state, x_pos - 1, y_pos) == 1 \
            or get_cell(state, x_pos, y_pos + 1) == 1 \
            or get_cell(state, x_pos, y_pos - 1) == 1:

        # execute infection
        r = random.random()
        if r <= p1:
            set_cell(new, x_pos, y_pos, 1)


# chance of 1 -> 2
def recover(new, x_pos, y_pos, p2):
    r = random.random()
    if r <= p2:
        set_cell(new, x_pos, y_pos, 2)


# chance of 2 -> 0
def susceptible(new, x_pos, y_pos, p3):
    r = random.random()
    if r <= p3:
        set_cell(new, x_pos, y_pos, 0)


# determine what type a cell is, run necessary SIRS cell change based on rules and probabilities
def update_cell(state, new, x_pos, y_pos, p1, p2, p3):
    # check cell value, run appropriate update
    cell_value = get_cell(state, x_pos, y_pos)
    if cell_value == 0:
        infect(state, new, x_pos, y_pos, p1)
    elif cell_value == 1:
        recover(new, x_pos, y_pos, p2)
    elif cell_value == 2:
        susceptible(new, x_pos, y_pos, p3)


# do all necessary changes, store in new state
def sweep_fully_parallel(current, new, p1, p2, p3):

    # update all cells
    for i in range(0, width):
        for j in range(0, height):
            update_cell(current, new, i, j, p1, p2, p3)


# update n^2 randomly chosen cells
def sweep_n2_cells(current, p1, p2, p3):

    for n in range(0, width*height):
        # select random cell
        x_pos = numpy.random.randint(0, width, 1, int)
        y_pos = numpy.random.randint(0, height, 1, int)

        # update chosen cell
        update_cell(current, current, x_pos, y_pos, p1, p2, p3)

