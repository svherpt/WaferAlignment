
import numpy as np
from simulator import wafer_simulator

sim = wafer_simulator.WaferSimulator(0.001, 100.0, 100.0)
# Check initial position
print("Position:", sim.getPosition())

# Set a force and update
sim.setForce(1.0, 2.0)
sim.update()

# Print the type of the position
print(np.array(sim.getPosition()))

# Check new position and velocity
print("Position after update:", sim.getPosition())
print("Velocity after update:", sim.getVelocity())

# Check limits
print("Limits:", sim.getLimits())
