#include "WaferSimulator.h"
#include <algorithm> // for std::clamp

WaferSimulator::WaferSimulator(double deltaT, double limitX, double limitY, double mass, double dragCoeff)
    : position(Eigen::Vector2d::Zero()),
    velocity(Eigen::Vector2d::Zero()),
    force(Eigen::Vector2d::Zero()),
    limits(limitX, limitY),
    deltaT(deltaT),
    mass(mass),
    dragCoeff(dragCoeff)
{
}

void WaferSimulator::update() {
    // Compute acceleration = (force - drag * velocity) / mass
    Eigen::Vector2d acceleration = (force - dragCoeff * velocity) / mass;

    // Integrate velocity and position
    velocity += acceleration * deltaT;
    position += velocity * deltaT;

    // Boundary check
    position.x() = std::clamp(position.x(), -limits.x(), limits.x());
    position.y() = std::clamp(position.y(), -limits.y(), limits.y());

    // Simple boundary collision (reverse velocity on hit)
    if (position.x() == -limits.x() || position.x() == limits.x()) velocity.x() *= -0.5;
    if (position.y() == -limits.y() || position.y() == limits.y()) velocity.y() *= -0.5;
}

void WaferSimulator::setForce(const Eigen::Vector2d& newForce) {
    force = newForce;
}

void WaferSimulator::reset() {
    position.setZero();
    velocity.setZero();
    force.setZero();
}

Eigen::Vector2d WaferSimulator::getPosition() const {
    return position;
}

Eigen::Vector2d WaferSimulator::getVelocity() const {
    return velocity;
}

Eigen::Vector2d WaferSimulator::getForce() const {
    return force;
}

Eigen::Vector2d WaferSimulator::getLimits() const {
    return limits;
}
