import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecMonitor
from stable_baselines3.common.callbacks import CheckpointCallback, BaseCallback
from envs.basic_motion_env import WaferBasicMotionEnv
from scripts.callbacks import EpisodeMetricsLogger

# Environment setup
DT = 0.01
logdir = "logs/basic_motion"
os.makedirs(logdir, exist_ok=True)

def make_env():
    """Factory for the WaferBasicMotionEnv"""
    def _thunk():
        env = WaferBasicMotionEnv(dt=DT, limit=10.0, size=1.0)
        return env
    return _thunk

# Single environment
env = DummyVecEnv([make_env()])
# VecMonitor handles logging and works with PPO
env = VecMonitor(env)

# PPO model setup
model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    tensorboard_log=logdir,
    n_steps=int(512 * (0.05 / DT)),  # scale n_steps for dt
    policy_kwargs=dict(net_arch=[128, 128, 128])
)

checkpoint_callback = CheckpointCallback(
    save_freq=10000,
    save_path=logdir,
    name_prefix="ppo_wafer"
)
metrics_callback = EpisodeMetricsLogger(metrics=["targets_reached"])

# Train
model.learn(
    total_timesteps=1_000_000,
    # callback=[checkpoint_callback]
    callback=[checkpoint_callback, metrics_callback]
)

# Save final model
model.save(os.path.join(logdir, "ppo_wafer_final"))
