#pragma once

class WaferSimulator {
private:
    double position;
    double currSpeed;
    double deltaT;
    double limit;  // maximum absolute position

public:
    WaferSimulator(double deltaT, double limit);

    void update();
    void setSpeed(double newSpeed);
    void reset();
    double getPosition() const;
    double getLimit() const;
};

