import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from simulator import wafer_simulator
from simulator import visualiser
from simulator import data_storage

# ---------- Setup simulator ----------
sim = wafer_simulator.WaferSimulator(0.05, 10.0, 10.0, 1.0)

# Apply some initial forces if desired
sim.applyForce(1.0, 0.5)

# Initialize trajectory tracking
data_storage.init_trajectory(sim, key="wafer1")

# ---------- Setup figure ----------
fig, ax = plt.subplots()
wafer_patch, trail_line = visualiser.init_visuals(sim, ax, key="wafer1")

# ---------- Animation / update loop ----------
def animate(frame):
    sim.applyTorque(0.5)
    sim.applyForce(1.0, 0.0)
    
    sim.update()
    data_storage.update_trajectory(sim, key="wafer1")
    visualiser.update_visuals(sim, key="wafer1")
    
    # Instead of returning old handles, return the objects from the visualiser dict
    return visualiser.trail_dict["wafer1"], visualiser.patch_dict["wafer1"]


ani = FuncAnimation(fig, animate, frames=500, interval=20, blit=False)
plt.show()
