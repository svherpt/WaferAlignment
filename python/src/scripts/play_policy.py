import time
from stable_baselines3 import PPO
import numpy as np
from envs.basic_motion_env import WaferBasicMotionEnv

model = PPO.load("logs/basic_motion/ppo_wafer_final.zip")
env = WaferBasicMotionEnv()
obs, _ = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _, _ = env.step(action)

    pos = env.sim.getPosition()
    rot = env.sim.getOrientation()

    print("pos", pos, "rot", rot, "reward", reward)
    if done:
        obs, _ = env.reset()
    time.sleep(env.sim.getLimits()[0] * 0.0)  # no busy sleep necessary
