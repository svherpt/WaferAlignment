#include "WaferSimulator.h"
#include <iostream>

int main() {
    WaferSimulator sim(0.01, 10.0, 10.0, 1.0, 1.0, 0.05, 0.02);

    // Apply a force off-centre (local coordinates), should cause spin
    sim.applyForceAtPoint(Eigen::Vector2d(5.0, 0.0), Eigen::Vector2d(0.0, 0.5), ForceMode2D::Local);

    for (int i = 0; i < 200; ++i) {
        sim.update();
        std::cout << "t=" << i * 0.01
            << " pos=" << sim.getPosition().transpose()
            << " vel=" << sim.getVelocity().transpose()
            << " theta=" << sim.getOrientation()
            << " omega=" << sim.getAngularVelocity()
            << "\n";

        // Continuously apply small central force forward in local frame
        sim.applyForce(Eigen::Vector2d(0.0, 0.0)); // no extra for now
    }

    return 0;
}
