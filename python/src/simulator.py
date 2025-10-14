import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon
from simulator import wafer_simulator
import numpy as np

# ---------- Simulation Setup ----------
sim = wafer_simulator.WaferSimulator(0.05, 10.0, 10.0, 1.0)
sim.applyForce(1.0, 0.5)
trajectory = []

limitX, limitY = sim.getLimits()
size = sim.getSize()
half_size = size / 2

# ---------- Figure Setup ----------
fig, ax = plt.subplots()
ax.set_xlim(-limitX, limitX)
ax.set_ylim(-limitY, limitY)
ax.set_xlabel("X position")
ax.set_ylabel("Y position")
ax.set_title("Wafer Simulator with Rotating Square")
ax.set_aspect('equal', adjustable='box')  # square aspect ratio


# Polygon for wafer
corners = np.array([[-half_size, -half_size],
                    [ half_size, -half_size],
                    [ half_size,  half_size],
                    [-half_size,  half_size]])
wafer_patch = Polygon(corners, fc='r', ec='k', alpha=0.6)
ax.add_patch(wafer_patch)

# Trail line
trail_line, = ax.plot([], [], 'b-', lw=1)

# ---------- Helper Functions ----------
def update_trail():
    if trajectory:
        xs, ys = zip(*trajectory)
        trail_line.set_data(xs, ys)

def update_wafer_patch():
    x, y = sim.getPosition()
    theta = sim.getOrientation()
    
    # Rotation matrix
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    
    # Rotate and translate corners
    rotated = (R @ corners.T).T + np.array([x, y])
    wafer_patch.set_xy(rotated)

# ---------- Animation Step ----------
def animate(frame):
    # Apply a constant torque every frame
    
    
    # Step the simulation
    sim.update()
    
    # Store trajectory
    trajectory.append(sim.getPosition())
    
    # Update visuals
    update_trail()
    update_wafer_patch()
    
    return trail_line, wafer_patch


# ---------- Run Animation ----------

sim.applyForce(1.0, 0.0)  # along world X
sim.applyTorque(5)  # positive value → clockwise rotation


ani = animation.FuncAnimation(fig, animate, frames=500, interval=20, blit=True)
plt.show()
