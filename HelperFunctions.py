from time import *
import math


# Ensure that a fresh simulation is running
def startSimulationEnv(sim):

    try:
        sim.stopSimulation()
        sleep(0.3)
        simHandle = sim.startSimulation()
        print(f"Simulation environment successfully started with handle {simHandle}")
        return simHandle

    except:
        print(f"Simulation was unable to be started")


def convertCurrentAngleTo360(currentAngle):
    oldMin = -270
    oldMax = 90
    newMin = 0
    newMax = 360

    return (((currentAngle - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin


def calculateAngleBetweenTwoPoints(startX, startY, goalX, goalY):
    return round(math.atan2(startY - goalY, startX - goalX) * 180 / math.pi)
