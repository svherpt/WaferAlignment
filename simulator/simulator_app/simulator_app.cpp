// simulator_app.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "WaferSimulator.h"

int main() {
    WaferSimulator sim(0.01, 10.0, 10.0);

    sim.setForce(Eigen::Vector2d(1.0, 0.5));

    for (int i = 0; i < 100; ++i) {
        sim.update();
        std::cout << "t=" << i * 0.01
            << " pos=" << sim.getPosition().transpose()
            << " vel=" << sim.getVelocity().transpose() << "\n";
    }

    return 0;
}