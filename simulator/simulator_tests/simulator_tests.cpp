#include "WaferSimulator.h"
#include <gtest/gtest.h>
#include <Eigen/Dense>

constexpr double EPS = 1e-9;

// Test initial state and parameters
TEST(WaferSimulatorTest, ConstructorInitialState) {
    WaferSimulator wafer(0.1, 1.0, 2.0, 1.0, 0.1, 0.05, 0.02);

    auto pos = wafer.getPosition();
    auto vel = wafer.getVelocity();
    auto lim = wafer.getLimits();

    EXPECT_NEAR(pos.x(), 0.0, EPS);
    EXPECT_NEAR(pos.y(), 0.0, EPS);

    EXPECT_NEAR(vel.x(), 0.0, EPS);
    EXPECT_NEAR(vel.y(), 0.0, EPS);

    EXPECT_NEAR(lim.x(), 1.0, EPS);
    EXPECT_NEAR(lim.y(), 2.0, EPS);

    EXPECT_NEAR(wafer.getOrientation(), 0.0, EPS);
    EXPECT_NEAR(wafer.getAngularVelocity(), 0.0, EPS);
}

// Applying force should accelerate linearly
TEST(WaferSimulatorTest, LinearForceProducesAcceleration) {
    WaferSimulator wafer(0.1, 10.0, 10.0, 1.0, 1.0);

    Eigen::Vector2d force(1.0, 0.0);
    wafer.applyForce(force);
    wafer.update();

    Eigen::Vector2d vel = wafer.getVelocity();
    // a = F / m = 1, so v = a * dt = 0.1
    EXPECT_NEAR(vel.x(), 0.1, 1e-6);
    EXPECT_NEAR(vel.y(), 0.0, 1e-6);
}

// Off-centre force should produce torque and rotation
TEST(WaferSimulatorTest, OffCentreForceProducesRotation) {
    WaferSimulator wafer(0.01, 10.0, 10.0, 1.0, 1.0);

    // Apply upward force on right edge in local coordinates
    wafer.applyForceAtPoint(Eigen::Vector2d(0.0, 10.0), Eigen::Vector2d(0.5, 0.0), ForceMode2D::Local);
    wafer.update();

    EXPECT_NEAR(wafer.getOrientation(), 0.0, 0.1);
    EXPECT_NE(wafer.getAngularVelocity(), 0.0);
}

// Apply torque directly and test angular acceleration
TEST(WaferSimulatorTest, ApplyTorque) {
    WaferSimulator wafer(0.1, 10.0, 10.0, 1.0, 2.0);

    EXPECT_NEAR(wafer.getAngularVelocity(), 0.0, EPS);

    wafer.applyTorque(1.0);
    wafer.update();

    // alpha = tau / I = 1 / (1/6 * 1 * 2^2) = 1 / 0.6666 = 1.5
    // omega = alpha * dt = 0.15
    EXPECT_NE(wafer.getAngularVelocity(), 0.0);
}

// Reset should clear all motion and orientation
TEST(WaferSimulatorTest, ResetResetsAll) {
    WaferSimulator wafer(0.1, 10.0, 10.0, 1.0, 1.0);
    wafer.applyForce(Eigen::Vector2d(1.0, 0.0));
    wafer.applyTorque(2.0);
    wafer.update();
    wafer.reset();

    EXPECT_NEAR(wafer.getPosition().x(), 0.0, EPS);
    EXPECT_NEAR(wafer.getPosition().y(), 0.0, EPS);
    EXPECT_NEAR(wafer.getVelocity().x(), 0.0, EPS);
    EXPECT_NEAR(wafer.getVelocity().y(), 0.0, EPS);
    EXPECT_NEAR(wafer.getOrientation(), 0.0, EPS);
    EXPECT_NEAR(wafer.getAngularVelocity(), 0.0, EPS);
}
