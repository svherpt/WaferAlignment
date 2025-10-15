import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
import gymnasium as gym
from envs.basic_motion_env import WaferBasicMotionEnv

def make_env():
    def _thunk():
        return WaferBasicMotionEnv(dt=0.05, limit=10.0, size=1.0)
    return _thunk

if __name__ == "__main__":
    logdir = "logs/basic_motion"
    os.makedirs(logdir, exist_ok=True)

    n_envs = 1   # start with 1 or 4; increase for faster sampling
    if n_envs == 1:
        env = DummyVecEnv([make_env()])
    else:
        env = SubprocVecEnv([make_env() for _ in range(n_envs)])

    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir,
                policy_kwargs=dict(net_arch=[256, 256]))
    checkpoint_callback = CheckpointCallback(save_freq=10000, save_path=logdir, name_prefix="ppo_wafer")
    model.learn(total_timesteps=1_000_000, callback=checkpoint_callback)
    model.save(os.path.join(logdir, "ppo_wafer_final"))
