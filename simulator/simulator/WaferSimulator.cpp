#include "WaferSimulator.h"
#include <algorithm>

WaferSimulator::WaferSimulator(double deltaT, double limitX, double limitY, double size,
    double mass, double dragCoeff, double rotDragCoeff)
    : position(Eigen::Vector2d::Zero()),
    velocity(Eigen::Vector2d::Zero()),
    orientation(0.0),
    angularVelocity(0.0),
    accumulatedForce(Eigen::Vector2d::Zero()),
    accumulatedTorque(0.0),
    limits(limitX, limitY),
    deltaT(deltaT),
    mass(mass),
    size(size),
    dragCoeff(dragCoeff),
    rotDragCoeff(rotDragCoeff)
{
    inertia = (1.0 / 6.0) * mass * size * size;
}

void WaferSimulator::update() {
    Eigen::Vector2d dragForce = -dragCoeff * velocity;
    double dragTorque = -rotDragCoeff * angularVelocity;

    Eigen::Vector2d acceleration = (accumulatedForce + dragForce) / mass;
    double angularAcceleration = (accumulatedTorque + dragTorque) / inertia;

    velocity += acceleration * deltaT;
    position += velocity * deltaT;

    angularVelocity += angularAcceleration * deltaT;
    orientation = wrapAngle(orientation + angularVelocity * deltaT);

    position.x() = std::clamp(position.x(), -limits.x(), limits.x());
    position.y() = std::clamp(position.y(), -limits.y(), limits.y());

    accumulatedForce.setZero();
    accumulatedTorque = 0.0;
}

void WaferSimulator::reset() {
    position.setZero();
    velocity.setZero();
    orientation = 0.0;
    angularVelocity = 0.0;
    accumulatedForce.setZero();
    accumulatedTorque = 0.0;
}

void WaferSimulator::applyForce(const Eigen::Vector2d& force) {
    accumulatedForce += force;
}

void WaferSimulator::applyForceAtPoint(const Eigen::Vector2d& force, const Eigen::Vector2d& point, ForceMode2D mode) {
    Eigen::Vector2d worldPoint = point;

    if (mode == ForceMode2D::Local) {
        double cosA = std::cos(orientation);
        double sinA = std::sin(orientation);
        Eigen::Matrix2d R;
        R << cosA, -sinA, sinA, cosA;
        worldPoint = position + R * point;
    }

    Eigen::Vector2d r = worldPoint - position;
    double torque = r.x() * force.y() - r.y() * force.x();

    accumulatedForce += force;
    accumulatedTorque += torque;
}

void WaferSimulator::applyTorque(double torque) {
    accumulatedTorque += torque;
}

Eigen::Vector2d WaferSimulator::getPosition() const { return position; }
Eigen::Vector2d WaferSimulator::getVelocity() const { return velocity; }
double WaferSimulator::getOrientation() const { return orientation; }
double WaferSimulator::getAngularVelocity() const { return angularVelocity; }
double WaferSimulator::getSize() const { return size; }
Eigen::Vector2d WaferSimulator::getLimits() const { return limits; }

double WaferSimulator::wrapAngle(double angle) {
    while (angle > PI) angle -= 2.0 * PI;
    while (angle < -PI) angle += 2.0 * PI;
    return angle;
}
