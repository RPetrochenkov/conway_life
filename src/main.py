from tkinter import *
import random
import time

FIRST_GEN_CHANCE = 0.2
PIXEL_SIZE = 4
POPULATION_SIZE = int (1024 / PIXEL_SIZE)
MUTATION_CHANCE = 1 / 100000
TIMER = 0.07

WIDTH = PIXEL_SIZE * POPULATION_SIZE
HEIGHT = PIXEL_SIZE * POPULATION_SIZE

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
    canvas.create_text(30, 40, anchor=W, font="Purisa",
                           text=text)
    return


def create_starting_population():
    population = list()
    for x in range(0, int(WIDTH / PIXEL_SIZE)):
        line = list()
        for y in range(0, int(HEIGHT / PIXEL_SIZE)):
            line.append(1 if random.random() < FIRST_GEN_CHANCE else 0)
        population.append(line)

    return population


def if_dot_exists(x,y):
    if 0 <= x < POPULATION_SIZE:
        if 0 <= y < POPULATION_SIZE:
            return True
    return False


def count_neighbours(population, x, y):
    count = 0

    for x_dif in [-1, 0, 1]:
        for y_dif in [-1, 0, 1]:
            if x_dif == 0 and y_dif == 0:
                continue
            elif if_dot_exists(x + x_dif, y + y_dif) and population[x + x_dif][y + y_dif] > 0:
                count += 1
    return count

def next_generation(population):
    new_population = list()

    for x, x_array in enumerate(population):
        line = list()
        for y, y_array in enumerate(x_array):

            state = population[x][y]
            neighbours = count_neighbours(population, x, y)

            if state > 1:
                state = 1
            if state < 0:
                state = 0

            if MUTATION_CHANCE > 0 and random.random() < MUTATION_CHANCE and neighbours > 0:
                if population[x][y]:
                    state = -1
                else:
                    state = 2
                line.append(state)
                continue

            if neighbours > 3 or neighbours < 2:
                state = 0

            if neighbours == 3:
                state = 1

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