# Simulating the entire fucking universe


# Imports #

from math import sqrt, fabs, floor
from time import sleep
from subprocess import check_call
import sys
from random import uniform

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
mass_input = ""


class Particle:
    def __init__(self, mass: float, pos: list, vel: list, density: float) -> None:
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.density = density


def acc_gravity(mass1: float, mass2: float, distance: float, G: float) -> float:
    try:
        return (G * mass1 * mass2) / distance**2
    except ZeroDivisionError:
        return 0


def calc_dist(point1: list, point2: list) -> float:
    return sqrt(fabs((point1[0] - point2[0]) ** 2) + fabs((point1[1] - point2[1])))


universe = [
    Particle(
        uniform(0, 10),
        [uniform(width * -1, width), uniform(height * -1, height)],
        [uniform(0, 10), uniform(0, 10)],
        floor(uniform(4, 10)),
    )
    for i in range(0, 10)
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
            if event.key in [
                pygame.K_0,
                pygame.K_1,
                pygame.K_2,
                pygame.K_3,
                pygame.K_4,
                pygame.K_5,
                pygame.K_6,
                pygame.K_7,
                pygame.K_8,
                pygame.K_9,
            ]:
                mass_input += ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"][
                    [
                        pygame.K_0,
                        pygame.K_1,
                        pygame.K_2,
                        pygame.K_3,
                        pygame.K_4,
                        pygame.K_5,
                        pygame.K_6,
                        pygame.K_7,
                        pygame.K_8,
                        pygame.K_9,
                    ].index(event.key)
                ]
            if event.key == pygame.K_KP_PLUS:
                universe.append(
                    Particle(
                        uniform(0, 100),
                        [uniform(width * -1, width), uniform(height * -1, height)],
                        [uniform(0, 10), uniform(0, 10)],
                        floor(uniform(1, 10)),
                    )
                )
        if event.type == pygame.MOUSEBUTTONUP and mass_input != "":
            universe.append(
                Particle(
                    int(mass_input),
                    [
                        pygame.mouse.get_pos()[0] - width / 2,
                        height / 2 - pygame.mouse.get_pos()[1],
                    ],
                    [0, 0],
                )
            )
            mass_input = ""
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
        print(
            f"{i}: {universe[i].mass}; {universe[i].vel}; ({universe[i].pos[0]}, {universe[i].pos[1]}); G: {bigG}"
        )
        universe[i].pos[0] += universe[i].vel[0]
        universe[i].pos[1] += universe[i].vel[1]
        if universe[i].pos[0] < (width / 2) * -1:
            universe[i].pos[0] = (width / 2) * -1
            universe[i].vel[0] = universe[i].vel[0] * -1
        elif universe[i].pos[0] > (width / 2):
            universe[i].pos[0] = width / 2
            universe[i].vel[0] = universe[i].vel[0] * -1
        if universe[i].pos[1] < (height / 2) * -1:
            universe[i].pos[1] = (height / 2) * -1
            universe[i].vel[1] = universe[i].vel[1] * -1
        elif universe[i].pos[1] > (height / 2):
            universe[i].pos[1] = height / 2
            universe[i].vel[1] = universe[i].vel[1] * -1
        pygame.draw.circle(
            surface,
            (255, 255, 0),
            (width / 2 + universe[i].pos[0], height / 2 - universe[i].pos[1]),
            universe[i].mass / universe[i].density,
        )
    sleep(0.1)
    pygame.display.flip()
    width, height = pygame.display.get_window_size()
