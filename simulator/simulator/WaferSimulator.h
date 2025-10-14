#pragma once
#include <Eigen/Dense>
#include <cmath>

constexpr double PI = 3.14159265358979323846;


enum class ForceMode2D {
    Local,
    World
};

class WaferSimulator {
public:
    WaferSimulator(double deltaT, double limitX, double limitY, double size,
        double mass = 1.0, double dragCoeff = 0.05, double rotDragCoeff = 0.02);

    void update();
    void reset();

    void applyForce(const Eigen::Vector2d& force);
    void applyForceAtPoint(const Eigen::Vector2d& force, const Eigen::Vector2d& point, ForceMode2D mode = ForceMode2D::Local);
    void applyTorque(double torque);

    Eigen::Vector2d getPosition() const;
    Eigen::Vector2d getVelocity() const;
    double getOrientation() const;
    double getAngularVelocity() const;
    Eigen::Vector2d getLimits() const;

private:
    Eigen::Vector2d position;
    Eigen::Vector2d velocity;
    double orientation;
    double angularVelocity;
    Eigen::Vector2d accumulatedForce;
    double accumulatedTorque;

    Eigen::Vector2d limits;
    double deltaT;
    double mass;
    double size;
    double inertia;
    double dragCoeff;
    double rotDragCoeff;

    double wrapAngle(double angle);
};
