"""
    Main driver program for the CoppeliaSim Demo
"""

from time import *
from linkStart import *
import threading
NUM_ROBOTS = 2 # Defines how many threads we create based on the number of robots in the scene

def main():
    threads = [] # Stores the simulation threads

    for i in range(NUM_ROBOTS):
        """Setting up the connection threads for each robot"""
        robotName = "/dr20[" + str(i) + "]"
        routine = subroutine(i, robotName)
        simThread = threading.Thread(target=routine.driver())
        threads.append(simThread)
        print(f"Main: starting subroutine {i}")
        sleep(.1)

if __name__ == "__main__":
    main()
