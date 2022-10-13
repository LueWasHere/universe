# Simulating the entire fucking universe (maybe someday...)


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
width, height = 100, 100

surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Gravity Simulation")
done = False
mass_input = ""


class Particle:
    particle_types = ["electron+", "electron-", "neutron", "proton"]
    def __init__(self, mass: float, pos: list, vel: list, density: float, is_energy: bool=False, particle_type: str="electron-") -> None:
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.density = density
        self.is_energy = is_energy
        self.particle_type = particle_type


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
    ),
    Particle(
        uniform(0, 10),
        [uniform(width * -1, width), uniform(height * -1, height)],
        [uniform(0, 10), uniform(0, 10)],
        floor(uniform(4, 10)),
        is_energy=True,
    ),
    Particle(
        uniform(0, 10),
        [uniform(width * -1, width), uniform(height * -1, height)],
        [uniform(0, 10), uniform(0, 10)],
        floor(uniform(4, 10)),
        particle_type=Particle.particle_types[0] # electron+
    ),
    Particle(
        uniform(0, 10),
        [uniform(width * -1, width), uniform(height * -1, height)],
        [uniform(0, 10), uniform(0, 10)],
        floor(uniform(4, 10)),
        is_energy=True,
    )
]

#   Execution   #
clock = pygame.time.Clock()
while not done:
    if bigG == 0:
        bigG = 0.000000000000001
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
                pygame.K_PERIOD,
            ]:
                mass_input += ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ][
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
                        pygame.K_PERIOD,
                    ].index(event.key)
                ]
            if event.key == pygame.K_KP_PLUS:
                universe.append(
                    Particle(
                        uniform(0, 100),
                        [uniform(width * -1, width), uniform(height * -1, height)],
                        [uniform(0, 10), uniform(0, 10)],
                        floor(uniform(4, 10)),
                    )
                )
        if event.type == pygame.MOUSEBUTTONUP and mass_input != "":
            if float(mass_input) == 0:
                mass_input = "0.000000001"
            universe.append(
                Particle(
                    float(mass_input),
                    [
                        pygame.mouse.get_pos()[0] - width / 2,
                        height / 2 - pygame.mouse.get_pos()[1],
                    ],
                    [0, 0],
                    floor(uniform(4, 10)),
                )
            )
            mass_input = ""
    if bigG == 0:
        bigG = 0.000000000000001
    surface.fill((0, 0, 0))
    for i in range(0, len(universe)):
        try:
            for j in range(0, len(universe)):
                if universe[i].pos[0] == universe[j].pos[0] or universe[i].pos[0]+universe[i].mass == universe[j].pos[0] or universe[i].pos[0]-universe[i].mass == universe[j].pos[0]:
                    if universe[i].particle_type == "electron-" and universe[i].particle_type == "electron+":
                        universe[i].is_energy = True
                        universe[j].is_energy = True
                    elif universe[i].particle_type == "electron+" and universe[i].particle_type == "electron-":
                        universe[i].is_energy = True
                        universe[j].is_energy = True
                    elif universe[i].particle_type == "proton" and universe[i].particle_type == "neutron":
                        pass # create an atom
                    elif universe[i].particle_type == "neutron" and universe[i].particle_type == "proton":
                        pass # create an atom
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
        except IndexError:
            pass
    
    for i in range(0, len(universe)):
        universe[i].pos[0] += universe[i].vel[0]
        universe[i].pos[1] += universe[i].vel[1]

        if not universe[i].is_energy:
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
            if universe[i].mass / universe[i].density < 1 and not universe[i].is_energy:
                pygame.draw.circle(
                    surface,
                    (255, 255, 255),
                    (width / 2 + universe[i].pos[0], height / 2 - universe[i].pos[1]),
                    universe[i].density,
                    width=1,
                )
            if universe[i].vel[0] > sqrt((2*universe[i].mass*bigG)/universe[i].density):
                universe[i].vel[0] = sqrt((2*universe[i].mass*bigG)/universe[i].density)
            elif universe[i].vel[0] < sqrt((2*universe[i].mass*bigG)/universe[i].density)*-1:
                universe[i].vel[0] = sqrt((2*universe[i].mass*bigG)/universe[i].density)*-1
            if universe[i].vel[1] > sqrt((2*universe[i].mass*bigG)/universe[i].density):
                universe[i].vel[1] = sqrt((2*universe[i].mass*bigG)/universe[i].density)
            elif universe[i].vel[1] < sqrt((2*universe[i].mass*bigG)/universe[i].density)*-1:
                universe[i].vel[1] = sqrt((2*universe[i].mass*bigG)/universe[i].density)*-1
        else:
            universe[i].vel[0] += universe[i].vel[0]/2
            universe[i].vel[1] += universe[i].vel[1]/2
            pygame.draw.circle(
                    surface,
                    (0, 255, 0),
                    (width / 2 + universe[i].pos[0], height / 2 - universe[i].pos[1]),
                    universe[i].density,
                    width=1,
                )
        print(
            f"Particle {i}: Mass {universe[i].mass}; Velocity: {universe[i].vel} ({(fabs(universe[i].vel[0])+fabs(universe[i].vel[1])/sqrt((2*universe[i].mass*bigG)/universe[i].density))*100}% of term vel: {sqrt((2*universe[i].mass*bigG)/universe[i].density)}); Position: ({universe[i].pos[0]}, {universe[i].pos[1]}); Density: {universe[i].density} (Resulting size: {universe[i].mass/universe[i].density}px); Is energy: {universe[i].is_energy}; Type: {universe[i].particle_type}; G: {bigG}"
        )
    sleep(0.1)
    pygame.display.flip()
    width, height = pygame.display.get_window_size()
    pygame.display.set_caption(f"Gravity Simulation. FPS: {clock.get_fps()}")
    clock.tick(120)
