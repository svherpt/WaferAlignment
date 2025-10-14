import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from simulator import wafer_simulator
import numpy as np

# ---------- Simulation Setup ----------
sim = wafer_simulator.WaferSimulator(0.05, 10.0, 10.0, 1.0)

# Apply a constant centre-of-mass force
sim.applyForce(1.0, 0.5)

# Trajectory storage
trajectory = []

limitX, limitY = sim.getLimits()

# ---------- Figure Setup ----------
fig, ax = plt.subplots()
ax.set_xlim(-limitX, limitX)
ax.set_ylim(-limitY, limitY)
ax.set_xlabel("X position")
ax.set_ylabel("Y position")
ax.set_title("Wafer Simulator with Rotating Square")

# Plot elements
trail_line, = ax.plot([], [], 'b-', lw=1)
wafer_patch = Rectangle((0, 0), sim.getSize(), sim.getSize(), fc='r', ec='k', alpha=0.6)
ax.add_patch(wafer_patch)

# ---------- Helper Functions ----------
def update_trail():
    xs, ys = zip(*trajectory)
    trail_line.set_data(xs, ys)

def update_wafer_patch():
    x, y = sim.getPosition()
    theta = sim.getOrientation()
    
    # Rectangle patch expects bottom-left corner; compute from center
    half_size = sim.getSize() / 2
    wafer_patch.set_xy((x - half_size, y - half_size))
    
    # Rotate about center
    wafer_patch.angle = np.degrees(theta)

# ---------- Animation Step ----------
def animate(frame):
    sim.update()
    
    # Store trajectory
    trajectory.append(sim.getPosition())
    
    # Update visuals
    update_trail()
    update_wafer_patch()
    
    return trail_line, wafer_patch

# ---------- Run Animation ----------
ani = animation.FuncAnimation(fig, animate, frames=500, interval=20, blit=True)
plt.show()
