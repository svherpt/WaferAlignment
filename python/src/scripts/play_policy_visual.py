import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from stable_baselines3 import PPO
from envs.basic_motion_env import WaferBasicMotionEnv
from simulator import visualiser, data_storage

# ---------- Setup environment and model ----------
env = WaferBasicMotionEnv()
model = PPO.load("logs/basic_motion/ppo_wafer_final.zip")

# Initialize trajectory tracking for visualisation
data_storage.init_trajectory(env.sim, key="wafer1")

# ---------- Setup figure ----------
fig, ax = plt.subplots()
wafer_patch, trail_line = visualiser.init_visuals(env.sim, ax, key="wafer1")

target_marker = plt.Circle(env.target, radius=0.05, color='green', alpha=0.8)
ax.add_patch(target_marker)

# Reset environment
obs, _ = env.reset()

# ---------- Animation / update function ----------
def animate(frame):
    global obs
    # Use trained policy
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _, _ = env.step(action)

    # Update trajectory storage
    data_storage.update_trajectory(env.sim, key="wafer1")
    visualiser.update_visuals(env.sim, key="wafer1")

    target_marker.center = env.target

    # Reset if episode done
    if done:
        obs, _ = env.reset()
        data_storage.init_trajectory(env.sim, key="wafer1")

    return visualiser.trail_dict["wafer1"], visualiser.patch_dict["wafer1"]

# ---------- Create animation ----------
ani = FuncAnimation(fig, animate, frames=1000, interval=20, blit=False)
plt.show()
