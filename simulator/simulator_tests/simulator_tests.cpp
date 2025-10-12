#include "WaferSimulator.h"
#include <gtest/gtest.h>
#include <Eigen/Dense>

// Test constructor and getters
TEST(WaferSimulatorTest, ConstructorAndGetters) {
    WaferSimulator wafer(0.1, 1.0, 2.0, 1.0, 0.1);
    auto pos = wafer.getPosition();
    auto vel = wafer.getVelocity();
    auto lim = wafer.getLimits();
    auto f = wafer.getForce();

    EXPECT_DOUBLE_EQ(pos.x(), 0.0);
    EXPECT_DOUBLE_EQ(pos.y(), 0.0);

    EXPECT_DOUBLE_EQ(vel.x(), 0.0);
    EXPECT_DOUBLE_EQ(vel.y(), 0.0);

    EXPECT_DOUBLE_EQ(lim.x(), 1.0);
    EXPECT_DOUBLE_EQ(lim.y(), 2.0);

    EXPECT_DOUBLE_EQ(f.x(), 0.0);
    EXPECT_DOUBLE_EQ(f.y(), 0.0);
}

// Test simple force application and update
TEST(WaferSimulatorTest, ForceUpdate) {
    WaferSimulator wafer(0.1, 10.0, 10.0, 1.0, 0.0); // no drag
    wafer.setForce(Eigen::Vector2d(1.0, 2.0));
    wafer.update();

    auto pos = wafer.getPosition();
    auto vel = wafer.getVelocity();

    // Acceleration = force / mass = (1,2)/1 = (1,2)
    // Velocity += a*dt = 0 + (1,2)*0.1 = (0.1,0.2)
    // Position += v*dt = 0 + (0.1,0.2)*0.1 = (0.01,0.02)
    EXPECT_NEAR(vel.x(), 0.1, 1e-9);
    EXPECT_NEAR(vel.y(), 0.2, 1e-9);
    EXPECT_NEAR(pos.x(), 0.01, 1e-9);
    EXPECT_NEAR(pos.y(), 0.02, 1e-9);
}

// Test drag effect
TEST(WaferSimulatorTest, DragEffect) {
    WaferSimulator wafer(0.1, 10.0, 10.0, 1.0, 1.0); // dragCoeff = 1.0
    wafer.setForce(Eigen::Vector2d(1.0, 0.0));
    wafer.update();

    auto vel = wafer.getVelocity();
    // Acceleration = (force - drag*velocity)/mass = (1-0)/1 = 1
    EXPECT_NEAR(vel.x(), 0.1, 1e-9);
    EXPECT_NEAR(vel.y(), 0.0, 1e-9);

    // Next update: a = (1 - 1*0.1)/1 = 0.9
    wafer.update();
    vel = wafer.getVelocity();
    EXPECT_NEAR(vel.x(), 0.1 + 0.09, 1e-9); // 0.19
}


// Test reset
TEST(WaferSimulatorTest, Reset) {
    WaferSimulator wafer(0.1, 1.0, 1.0, 1.0, 0.1);
    wafer.setForce(Eigen::Vector2d(1.0, -1.0));
    wafer.update();
    wafer.reset();

    auto pos = wafer.getPosition();
    auto vel = wafer.getVelocity();
    auto f = wafer.getForce();

    EXPECT_DOUBLE_EQ(pos.x(), 0.0);
    EXPECT_DOUBLE_EQ(pos.y(), 0.0);
    EXPECT_DOUBLE_EQ(vel.x(), 0.0);
    EXPECT_DOUBLE_EQ(vel.y(), 0.0);
    EXPECT_DOUBLE_EQ(f.x(), 0.0);
    EXPECT_DOUBLE_EQ(f.y(), 0.0);
}

// Test multiple sequential updates
TEST(WaferSimulatorTest, SequentialUpdates) {
    WaferSimulator wafer(0.1, 5.0, 5.0, 1.0, 0.0);
    wafer.setForce(Eigen::Vector2d(1.0, 1.0));

    for (int i = 0; i < 10; ++i) {
        wafer.update();
    }

    auto pos = wafer.getPosition();
    auto vel = wafer.getVelocity();

    // After 10 updates, velocity = a*dt*10 = 1*0.1*10=1
    // Position = sum(vel*dt) = sum(i*0.1*0.1) = 0.55
    EXPECT_NEAR(vel.x(), 1.0, 1e-9);
    EXPECT_NEAR(vel.y(), 1.0, 1e-9);
    EXPECT_NEAR(pos.x(), 0.55, 1e-9);
    EXPECT_NEAR(pos.y(), 0.55, 1e-9);
}
