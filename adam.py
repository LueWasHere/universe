# Simulating the entire fucking universe


# Imports #

from math import sqrt, fabs
from time import sleep
from subprocess import check_call
import sys

try:
    import pygame
except ModuleNotFoundError:
    check_call([sys.executable, "-m", "pip", "install", "pygame"])

#     Setup     #


pygame.init()

bigG: float = 1  # true constant: 6.67430 * (10**-11)
width, height = 600, 500

surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Pygame Window")
done = False


class Particle:
    def __init__(self, mass: float, pos: list, vel: list) -> None:
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.heat = [0, 0, 0]


def acc_gravity(mass1: float, mass2: float, distance: float, G: float) -> float:
    try:
        return (G * mass1 * mass2) / distance**2
    except ZeroDivisionError:
        return 0


def calc_dist(point1: list, point2: list) -> float:
    return sqrt(fabs((point1[0] - point2[0]) ** 2) + fabs((point1[1] - point2[1])))


universe = [
    Particle(1, [10, 10], [0, 0]),
    Particle(1, [50, 50], [0, 0]),
    Particle(1, [20, -50], [0, 0]),
]

#   Execution   #

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                bigG += 1
            elif event.key == pygame.K_s:
                bigG -= 1
    surface.fill((0, 0, 0))
    for i in range(0, len(universe)):
        for j in range(0, len(universe)):
            if universe[i].pos[0] > universe[j].pos[0]:
                universe[i].vel[0] -= acc_gravity(
                    universe[j].mass,
                    universe[i].mass,
                    calc_dist(universe[j].pos, universe[i].pos),
                    bigG,
                )
            else:
                universe[i].vel[0] += acc_gravity(
                    universe[j].mass,
                    universe[i].mass,
                    calc_dist(universe[j].pos, universe[i].pos),
                    bigG,
                )
            if universe[i].pos[1] > universe[j].pos[1]:
                universe[i].vel[1] -= acc_gravity(
                    universe[j].mass,
                    universe[i].mass,
                    calc_dist(universe[j].pos, universe[i].pos),
                    bigG,
                )
            else:
                universe[i].vel[1] += acc_gravity(
                    universe[j].mass,
                    universe[i].mass,
                    calc_dist(universe[j].pos, universe[i].pos),
                    bigG,
                )
    for i in range(0, len(universe)):
        print(f"{i}: {universe[i].vel}; ({universe[i].pos[0]}, {universe[i].pos[1]}); {universe[i].heat}; G: {bigG}")
        universe[i].heat = ((universe[i].vel[0]*universe[i].vel[1])/100, 0, 0)
        if universe[i].heat[0] > 255:
            universe[i].heat[0] = 255
        universe[i].pos[0] += universe[i].vel[0]
        universe[i].pos[1] += universe[i].vel[1]
        if universe[i].pos[0] < (width / 2)*-1:
            universe[i].pos[0] = (width / 2)*-1
            universe[i].vel[0] = universe[i].vel[0]*-1
        elif universe[i].pos[0] > (width / 2):
            universe[i].pos[0] = (width / 2)
            universe[i].vel[0] = universe[i].vel[0]*-1
        if universe[i].pos[1] < (height / 2)*-1:
            universe[i].pos[1] = (height / 2)*-1
            universe[i].vel[1] = universe[i].vel[1]*-1
        elif universe[i].pos[1] > (height / 2):
            universe[i].pos[1] = (height / 2)
            universe[i].vel[1] = universe[i].vel[1]*-1
        pygame.draw.circle(
            surface,
            universe[i].heat,
            (width / 2 + universe[i].pos[0], height / 2 - universe[i].pos[1]),
            10,
        )
    sleep(0.1)
    pygame.display.flip()
    width, height = pygame.display.get_window_size()
