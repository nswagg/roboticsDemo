"""
    This is the main driver for the individual robot's subroutine. Each robot must be operated in the simulation
    with its own connection to prevent ZeroMQ from deadlocking

    NOTE::
    ZMQ has a bug that causes sockets to freak if not enough time has passed between starting the threads
"""

from zmqRemoteApi.clients.python.zmqRemoteApi import RemoteAPIClient
from dr20 import *
import threading


class subroutine:
    def __init__(self, ID, robotName, subtype):
        self.ID = ID
        self.name = robotName
        self.type = subtype
        self.client = RemoteAPIClient()  # establishes client connection through socket
        self.sim = self.client.getObject('sim')
        self.sim.addLog(self.sim.verbosity_scriptinfos, f"Initializing Subroutine {self.ID}")
        self.threads = []  # Keeps track of the subroutines created threads. Should only be 1 thread

    def startRoutine(self):
        # Starts the socket connection
        print(f"Starting Subroutine {self.ID}")
        startSimulationEnv(self.sim)

    def connectObject(self):
        # Creates a thread for a single robot.
        if self.type == "wanderer":
            self.robot = wanderer(self.sim, self.name, self.ID)  # Initializes a new wanderer
        elif self.type == "seeker":
            self.robot = seeker(self.sim, self.name, self.ID)  # Initializes a new seeker robot
        else:
            self.robot = dr20(self.sim, self.name, self.ID)  # Initializes default Robot
        # Setting Robot in motion with automated script
        self.rThread = threading.Thread(target=self.robot.randomlyExploreForSetTime)
        self.threads.append(self.rThread)
        self.rThread.start()
        sleep(.1)

    def endRoutine(self):
        # End the socket connection
        for thread in self.threads:
            thread.join()
        print(f"Threads in routing {self.ID} rejoined")
        sleep(1)
        self.sim.stopSimulation()
        print(f"Routine {self.ID} completed and exited.")

    def driver(self):
        # This is the threaded function.
        self.startRoutine()
        self.connectObject()
