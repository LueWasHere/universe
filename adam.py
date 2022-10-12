#####   Imports     #####
import math
from time import sleep

#####   Constants   #####
bigG: float = 9.8

#####   Variables   #####
particleOneMass: float = 1
partcileTwoMass: float = 1
distance: float = 20 # metres

#####   Functions   #####
def calculateGravityAttraction(particleOneMass: float, partcileTwoMass: float, gravitationalConstant: float, distance: float):
    return math.fabs(distance-gravitationalConstant*((particleOneMass*partcileTwoMass)/math.sqrt(distance)))

#####   Execution   #####
for i in range(10):
    distance = calculateGravityAttraction(particleOneMass, partcileTwoMass, bigG, distance)
    print(distance)
    sleep(1)
