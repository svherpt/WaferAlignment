import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from simulator.data_storage import get_trajectory

patch_dict = {}
trail_dict = {}
corner_dict = {}

def init_visuals(sim, ax, key="default"):
    size = sim.getSize()
    half = size / 2
    
    # Define corners centered at origin
    corners = np.array([[-half, -half],
                        [ half, -half],
                        [ half,  half],
                        [-half,  half]])
    corner_dict[key] = corners
    
    wafer_patch = Polygon(corners, fc='r', ec='k', alpha=0.6)
    ax.add_patch(wafer_patch)
    patch_dict[key] = wafer_patch
    
    trail_line, = ax.plot([], [], 'b-', lw=1)
    trail_dict[key] = trail_line
    
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-sim.getLimits()[0], sim.getLimits()[0])
    ax.set_ylim(-sim.getLimits()[1], sim.getLimits()[1])
    
    return wafer_patch, trail_line

def update_visuals(sim, key="default"):
    wafer_patch = patch_dict[key]
    trail_line = trail_dict[key]
    corners = corner_dict[key]
    
    # Rotate corners
    x, y = sim.getPosition()
    theta = sim.getOrientation()
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    rotated = (R @ corners.T).T + np.array([x, y])
    wafer_patch.set_xy(rotated)
    
    # Update trail if trajectory stored
    traj = get_trajectory(key)
    if traj:
        xs, ys = zip(*traj)
        trail_line.set_data(xs, ys)
