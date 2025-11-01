import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecMonitor
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
import gymnasium as gym
from envs.basic_motion_env import WaferBasicMotionEnv


def make_env():
    """Factory that creates a monitored environment instance."""
    def _thunk():
        env = WaferBasicMotionEnv(dt=0.05, limit=10.0, size=1.0)
        env = Monitor(env) 
        return env
    return _thunk


if __name__ == "__main__":
    logdir = "logs/basic_motion"
    os.makedirs(logdir, exist_ok=True)

    n_envs = 1   # increase for parallel sampling
    if n_envs == 1:
        env = DummyVecEnv([make_env()])
        env = VecMonitor(env)
    else:
        env = SubprocVecEnv([make_env() for _ in range(n_envs)])
        env = VecMonitor(env)

    # PPO model
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1, 
        tensorboard_log=logdir,
        policy_kwargs=dict(net_arch=[64, 64,64])
    )

    # Checkpoint callback
    checkpoint_callback = CheckpointCallback(
        save_freq=10000,
        save_path=logdir,
        name_prefix="ppo_wafer"
    )

    # Train
    model.learn(
        total_timesteps=1_000_000,
        callback=checkpoint_callback
    )

    # Save final model
    model.save(os.path.join(logdir, "ppo_wafer_final"))
