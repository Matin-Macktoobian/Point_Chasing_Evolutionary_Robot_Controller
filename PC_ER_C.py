from math import sqrt
from random import random, randint, seed
import matplotlib.pyplot as plt

class Robot:
    def __init__(self, position, target_position, step_size):
        self.position = position
        self.target_position = target_position
        self.step_size = step_size

    def move(self, individual):
        self.position[0] += individual.velocity[0] * self.step_size
        self.position[1] += individual.velocity[1] * self.step_size

    def get_distance(self):
        return sqrt(pow(self.position[0] - self.target_position[0], 2) + pow(self.position[1] - self.target_position[1], 2))

class Individual:
    EPSILON = 0.001
    VELOCITY_MULTIPLIER = 0.1
    MUTATION_RATE = 0.01

    def __init__(self):
        self.velocity = [self.VELOCITY_MULTIPLIER * random(), self.VELOCITY_MULTIPLIER * random()]

    def compute_fitness(self, robot):
        temp_robot = Robot(robot.position.copy(), robot.target_position, robot.step_size)
        temp_robot.move(self)
        return 1 / (self.EPSILON + temp_robot.get_distance())

    def mutate(self):
        if random() > self.MUTATION_RATE:
            self.velocity += [
                self.VELOCITY_MULTIPLIER * self.MUTATION_RATE * random(),
                self.VELOCITY_MULTIPLIER * self.MUTATION_RATE * random(),
            ]

def evolve(population, robot, number_of_generations,reproduction_size):
    best_fitness = 0
    for current_index in range(number_of_generations):
        population.sort(key=lambda x: x.compute_fitness(robot), reverse=True)
        num_to_breed = int(len(population) * reproduction_size)
        for current_id in range(num_to_breed, len(population)):
            parent_id_1 = randint(0, num_to_breed - 1)
            parent_id_2 = randint(0, num_to_breed - 1)
            temp_robot = Robot(robot.position.copy(), robot.target_position, robot.step_size)
            temp_robot.move(population[current_id])
            population[current_id].velocity[0] = (population[parent_id_1].velocity[0] + population[parent_id_2].velocity[0]) / 2
            population[current_id].velocity[1] = (population[parent_id_1].velocity[1] + population[parent_id_2].velocity[1]) / 2
            population[current_id].mutate()
        temp_best_fitness = population[0].compute_fitness(robot)
        if temp_best_fitness > best_fitness:
            best_fitness = temp_best_fitness
        else:
            break
        fitness_list.append(population[0].compute_fitness(robot))
        #print("The best fitness of generation {0}: {1:.4f}".format(current_index, best_fitness))
        robot.move(population[0])
        convergence_list.append(robot.get_distance())


def render(fitness_list, convergence_list, robot):
    reference_list = [x for x in range(NUMBER_OF_GENERATIONS)]
    figure, axis = plt.subplots(1, 2, figsize=(12, 6)) 
    axis[0].plot(reference_list[:len(fitness_list)], fitness_list) 
    axis[0].set_title("Fitness dynamics") 
    axis[0].set_xlabel("Generation")
    axis[0].set_ylabel("Fitness value")
    axis[0].text(0.1, 0.9, "The maximum fitness yields \n in the generation #{0}".format(convergence_list.index(convergence_list[-1])), 
                                                                                   transform=axis[0].transAxes,
                                                                                   bbox = dict(facecolor = 'red', alpha = 0.4))
    axis[1].plot(reference_list[:len(fitness_list)], convergence_list) 
    axis[1].set_title("Convergence dynamics") 
    axis[1].set_xlabel("Generation")
    axis[1].set_ylabel("Deviation from the target position ({0},{1})".format(robot.target_position[0], robot.target_position[1]))
    axis[1].text(0.4, 0.9, "Final positioning error:\n ({0:0.2f}, {1:0.2f})".format(robot.target_position[0] - robot.position[0], 
                                                                            robot.position[1] - robot.target_position[1]), 
                                                                            transform=axis[1].transAxes,
                                                                            bbox = dict(facecolor = 'red', alpha = 0.4))
    plt.show()

###############################################

SEED = 0
position = [0, 0]
TARGET_POSITION = [10, 10]
STEP_SIZE = 2
POPULATION_SIZE = 100
NUMBER_OF_GENERATIONS = 60
REPRODUCTION_RATE = 0.2

seed(SEED)
robot = Robot(position, TARGET_POSITION, STEP_SIZE)
population = [Individual() for _ in range(POPULATION_SIZE)]
fitness_list = []
convergence_list = []

evolve(population, robot, NUMBER_OF_GENERATIONS, REPRODUCTION_RATE)
render(fitness_list, convergence_list, robot)