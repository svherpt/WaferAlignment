from src.simulator import wafer_simulator
import pytest

def test_wafer_simulator_basic():
    # Create a simulator with deltaT=0.1 and X/Y limits 10
    # Purpose is to just check if the build process works
    sim = wafer_simulator.WaferSimulator(0.1, 10.0, 10.0, 1.0, 0.0)

    # Initial state
    assert sim.getPosition() == (0.0, 0.0)
    limits = sim.getLimits()
    assert limits == (10.0, 10.0)
