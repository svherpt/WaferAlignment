#include "WaferSimulator.h"
#include <gtest/gtest.h>


// Test reset
TEST(WaferSimulatorTest, Reset) {
    WaferSimulator wafer(0.1, 1.0);
    wafer.setSpeed(0.5);
    wafer.update();
    wafer.reset();
    EXPECT_DOUBLE_EQ(wafer.getPosition(), 0.0);
    EXPECT_DOUBLE_EQ(wafer.getLimit(), 1.0);
}
