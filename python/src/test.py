
from envs.basic_motion_env import WaferBasicMotionEnv
import matplotlib.pyplot as plt


env = WaferBasicMotionEnv()
obs, _ = env.reset()
for _ in range(200):
    action = env.action_space.sample()  # or from your policy
    obs, reward, terminated, truncated, _ = env.step(action)
    env.render()
    if terminated or truncated:
        obs, _ = env.reset()
plt.show()