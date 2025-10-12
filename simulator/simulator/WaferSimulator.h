#pragma once
#include <Eigen/Dense>

class WaferSimulator {
public:
    WaferSimulator(double deltaT, double limitX, double limitY, double mass = 1.0, double dragCoeff = 0.05);

    // physics update
    void update();

    // apply a force (will overwrite existing force for this step)
    void setForce(const Eigen::Vector2d& newForce);

    // resets position, velocity, and force
    void reset();

    // getters
    Eigen::Vector2d getPosition() const;
    Eigen::Vector2d getVelocity() const;
    Eigen::Vector2d getForce() const;
    Eigen::Vector2d getLimits() const;

private:
    Eigen::Vector2d position;   // current position
    Eigen::Vector2d velocity;   // current velocity
    Eigen::Vector2d force;      // current applied force
    Eigen::Vector2d limits;     // ±x, ±y bounds

    double deltaT;              // time step
    double mass;                // wafer mass
    double dragCoeff;           // air friction coefficient
};
