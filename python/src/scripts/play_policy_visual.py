import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from stable_baselines3 import PPO
from envs.basic_motion_env import WaferBasicMotionEnv
from simulator import visualiser, data_storage

DT = 0.01

# ---------- Setup environment and model ----------
env = WaferBasicMotionEnv(dt=DT, limit=10.0, size=1.0)


# model = "ppo_wafer_final.zip"
model = "ppo_wafer_40000_steps.zip"

model = PPO.load(f'logs/basic_motion/{model}')

# Initialize trajectory tracking for visualisation
data_storage.init_trajectory(env.sim, key="wafer1")

# ---------- Setup figure ----------
fig, ax = plt.subplots()
wafer_patch, trail_line = visualiser.init_visuals(env.sim, ax, key="wafer1")

target_marker = plt.Circle(env.target, radius=0.05, color='green', alpha=0.8)
ax.add_patch(target_marker)

# Reset environment
obs, _ = env.reset()

total_rewards = 0.0
# ---------- Animation / update function ----------
def animate(frame):
    global obs
    global total_rewards

    # Use trained policy
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _, _ = env.step(action)

    # Update trajectory storage
    data_storage.update_trajectory(env.sim, key="wafer1")
    visualiser.update_visuals(env.sim, key="wafer1")

    target_marker.center = env.target
    total_rewards += reward
    
    # Reset if episode done
    if done:
        # Print final reward
        print(f"Episode done, final reward: {total_rewards:.2f}")
        
        obs, _ = env.reset()
        data_storage.init_trajectory(env.sim, key="wafer1")
        total_rewards = 0.0

    return visualiser.trail_dict["wafer1"], visualiser.patch_dict["wafer1"]

# ---------- Create animation ----------
ani = FuncAnimation(fig, animate, frames=1000, interval=20, blit=False)
plt.show()
