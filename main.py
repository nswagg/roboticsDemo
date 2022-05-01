"""
    Main driver program for the CoppeliaSim Demo. Creates a process for each Sim subroutine and then
    threads within the process
"""
from linkStart import *
import multiprocessing as mproc

NUM_ROBOTS = 6  # Defines how many threads we create based on the number of robots in the scene


def main():
    processes = []  # Stores the simulation processes

    # Set up 1 wanderer
    if NUM_ROBOTS == 1:
        robotName = "/dr20"  # for only 1 robot
    else:
        robotName = "/dr20[0]"
    routine = subroutine(0, robotName, "wanderer")
    simProc = mproc.Process(target=routine.driver())
    processes.append(simProc)

    for i in range(1, NUM_ROBOTS):
        """Setting up the connection threads for each robot in excess of 1"""
        robotName = "/dr20[" + str(i) + "]"

        routine = subroutine(i, robotName, "wanderer")
        simProc = mproc.Process(target=routine.driver())
        processes.append(simProc)
        print(f"Main: starting subroutine {i}")
        simProc.start()
        sleep(.1)


if __name__ == "__main__":
    main()
