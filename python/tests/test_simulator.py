from src.simulator import wafer_simulator
import pytest

def test_wafer_simulator_basic():
    # Create a simulator with deltaT=0.1 and limit=10
    sim = wafer_simulator.WaferSimulator(0.1, 10.0)

    # Initial state
    assert sim.getPosition() == 0.0
    assert sim.getLimit() == 10.0

    # Set speed and update
    sim.setSpeed(50.0)
    assert sim.getSpeed() == 50.0

    sim.update()
    # position = 0.0 + 0.1 * 50.0 = 5.0
    assert sim.getPosition() == 5.0

    # Update again
    sim.update()
    # position = 5.0 + 0.1 * 50.0 = 10.0 (clamped)
    assert sim.getPosition() == 10.0

    # Set negative speed and update
    sim.setSpeed(-200.0)
    sim.update()
    # position = 10.0 + 0.1 * (-200.0) = -10.0 (clamped)
    assert sim.getPosition() == -10.0

    # Reset simulator
    sim.reset()
    assert sim.getPosition() == 0.0
    assert sim.getLimit() == 10.0
