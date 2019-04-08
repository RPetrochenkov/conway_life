from tkinter import *
import random
import time

FIRST_GEN_CHANCE = 0.2
PIXEL_SIZE = 2**3
POPULATION_SIZE = int (512 / PIXEL_SIZE)
MUTATION_CHANCE = 1 / 100000
TIMER = 0.2

WIDTH = PIXEL_SIZE * POPULATION_SIZE
HEIGHT = PIXEL_SIZE * POPULATION_SIZE

STATE_RULES = {0: 0, 1: 0, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}


def draw_canvas(window):
    canvas = Canvas(window, width=WIDTH, height=HEIGHT, background ="white")
    canvas.grid(row=0, column=0)
    return canvas


def draw_population(canvas, population, generation = None, mutation_count = None, mutation_last_step = None):
    canvas.delete("all")
    count = 0
    for x, x_array in enumerate(population):
        for y, dot_state in enumerate(x_array):
            color = "black"
            if dot_state == 0:
                continue
            if dot_state > 0:
                count += 1
            if dot_state == 2:
                color = "orange"
            if dot_state < 0:
                color = "grey"
            canvas.create_rectangle(x * PIXEL_SIZE, y * PIXEL_SIZE, (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE, fill=color)

    text = ""
    if generation:
        text += "Genration: " + str(generation) + "\n"
    if mutation_count:
        text += "Mutations total: " + str(mutation_count) + "\n"
    if mutation_last_step is not None:
        text += "Mutation last gen: " + str(mutation_last_step) + "\n"

    text += "Population: " + str(count)
    canvas.create_text(30, 40, anchor=W, font="Purisa", text=text)
    return


def create_starting_population():
    return [[1 if random.random() < FIRST_GEN_CHANCE else 0 for _ in range(0, POPULATION_SIZE)] for _ in range(0, POPULATION_SIZE)]



def if_dot_exists(x,y):
    if 0 <= x < POPULATION_SIZE:
        if 0 <= y < POPULATION_SIZE:
            return True
    return False


# def count_neighbours(population, x, y):
#     count = 0
#
#     for x_dif in [-1, 0, 1]:
#         for y_dif in [-1, 0, 1]:
#             if x_dif == 0 and y_dif == 0:
#                 continue
#             elif if_dot_exists(x + x_dif, y + y_dif) and population[x + x_dif][y + y_dif] > 0:
#                 count += 1
#     return count


def neighbours_coords(x,y):
    neighbours_coords = list()
    for x_dif in [-1, 0, 1]:
        for y_dif in [-1, 0, 1]:
            if x_dif == 0 and y_dif == 0:
                continue
            if if_dot_exists(x + x_dif, y + y_dif):
                neighbours_coords.append([x + x_dif,y + y_dif])
    return neighbours_coords

def pre_count_neighbours(population):
    neighbours = [[0 for _ in range(0, POPULATION_SIZE)] for _ in range(0, POPULATION_SIZE)]

    for x, x_array in enumerate(population):
        for y, state in enumerate(x_array):
            if state < 1:
                continue
            for [n_x, n_y] in neighbours_coords(x, y):
                neighbours[n_x][n_y] += 1
    return neighbours

def next_generation(population):
    new_population = list()
    neighbours = pre_count_neighbours(population)
    for x, x_array in enumerate(population):
        line = list()
        for y, y_array in enumerate(x_array):
            state = y_array
            neighbours_count = neighbours[x][y]

            if state > 1:
                state = 1
            if state < 0:
                state = 0

            if MUTATION_CHANCE > 0 and random.random() < MUTATION_CHANCE and neighbours_count > 0:
                if population[x][y]:
                    state = -1
                else:
                    state = 2
                line.append(state)
                continue

            state = state if neighbours_count not in STATE_RULES.keys() else STATE_RULES[neighbours_count]

            line.append(state)
        new_population.append(line)

    return new_population


def count_mutations(population):
    count = 0
    for x in population:
        for y in x:
            if y < 0 or y > 1:
                count += 1
    return count

def stable_population_example():
    population = [[0 for _ in range(0, POPULATION_SIZE)] for _ in range(0, POPULATION_SIZE)]
    population[20][20] = 1
    population[20][21] = 1
    population[20][22] = 1
    return population


def conway():
    main_window = Tk()
    canvas = draw_canvas(main_window)
    population = create_starting_population()

    generation_counter = 0
    mutations_counter = 0
    while True:
        generation_counter += 1
        this_step_mutations = count_mutations(population)
        draw_population(canvas, population, generation=generation_counter,
                        mutation_last_step=this_step_mutations, mutation_count=mutations_counter)
        mutations_counter += this_step_mutations
        main_window.update()
        population = next_generation(population)

        time.sleep(TIMER)


def main():
    conway()


if __name__ == "__main__":
    main()
