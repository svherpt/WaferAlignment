// simulator_app.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "WaferSimulator.h"

int main() {
    WaferSimulator wafer(0.1f, 1.0); // deltaT=0.1, speed=0.5, limit=1.0


    wafer.setSpeed(1.0);
    for (int i = 0; i < 30; ++i) {
        wafer.update();
        std::cout << "Step " << i << ": position = " << wafer.getPosition() << '\n';
    }

    return 0;
}