#include "WaferSimulator.h"
#include <algorithm> // for std::clamp

WaferSimulator::WaferSimulator(double deltaT, double limit)
    : position(0.0), currSpeed(0.0), deltaT(deltaT), limit(limit) {
}

void WaferSimulator::update() {
    position += deltaT * currSpeed;
    position = std::clamp(position, -limit, limit);
}

void WaferSimulator::setSpeed(double newSpeed)
{
    currSpeed = newSpeed;
}

void WaferSimulator::reset() {
    position = 0.0;
    currSpeed = 0.0;
}

double WaferSimulator::getPosition() const {
    return position;
}


double WaferSimulator::getSpeed() const {
    return currSpeed;
}

double WaferSimulator::getLimit() const {
    return limit;
}