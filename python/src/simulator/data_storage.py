# Tracks trajectory of a WaferSimulator object

trajectory_dict = {}

def init_trajectory(sim, key="default"):
    trajectory_dict[key] = []

def update_trajectory(sim, key="default"):
    pos = sim.getPosition()
    trajectory_dict[key].append(pos)

def get_trajectory(key="default"):
    return trajectory_dict.get(key, [])
