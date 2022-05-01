from HelperFunctions import *
from zmqRemoteApi.clients.python.zmqRemoteApi import RemoteAPIClient
from time import *
from dr20 import *
import threading
NUM_ROBOTS = 4 # Defines how many threads we create

def main():
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    startSimulationEnv(sim)

    for i in range(NUM_ROBOTS):
        robotName = "/dr20[" + str(i) + "]"
        robot = dr20(sim, robotName, i)
        thread = threading.Thread(target=robot.randomlyExploreForSetTime)
        thread.start()

    sleep(2)
    sim.stopSimulation()


if __name__ == "__main__":
    main()
