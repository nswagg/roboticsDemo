#include "RemoteAPIClient.h"
#include <iostream>
#include <iomanip>

int main()
{
    RemoteAPIClient client;
    client.setStepping(true);
    client.call("sim.startSimulation", nullptr);
    float simTime=0.0f;
    while (simTime<3.0f)
    {
        std::cout << "Simulation time: " << std::setprecision(3) << simTime << " [s]" << std::endl;
        client.step();
        simTime=client.call("sim.getSimulationTime")[0].as<float>();
    }    
    client.call("sim.stopSimulation", nullptr);

    return 0;
}
