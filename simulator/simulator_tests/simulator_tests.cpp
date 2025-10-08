#include "WaferSimulator.h"
#include <gtest/gtest.h>

// Test constructor and getters
TEST(WaferSimulatorTest, ConstructorAndGetters) {
    WaferSimulator wafer(0.1, 1.0);
    EXPECT_DOUBLE_EQ(wafer.getPosition(), 0.0);
    EXPECT_DOUBLE_EQ(wafer.getLimit(), 1.0);
}

// Test setting speed
TEST(WaferSimulatorTest, SetSpeed) {
    WaferSimulator wafer(0.1, 1.0);
    wafer.setSpeed(0.5);
    wafer.update();
    EXPECT_DOUBLE_EQ(wafer.getPosition(), 0.05); // deltaT * speed
}

// Test update clamps at limit
TEST(WaferSimulatorTest, UpdateClampsLimit) {
    WaferSimulator wafer(0.5, 1.0);
    wafer.setSpeed(5.0);
    wafer.update();
    EXPECT_DOUBLE_EQ(wafer.getPosition(), 1.0); // clamped at limit

    wafer.setSpeed(-10.0);
    wafer.update();
    EXPECT_DOUBLE_EQ(wafer.getPosition(), -1.0); // clamped at -limit
}
