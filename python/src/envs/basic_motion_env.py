import gymnasium as gym
import numpy as np
from simulator import wafer_simulator

class WaferBasicMotionEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, dt=0.05, limit=10.0, size=1.0):
        
        self.dt = dt

        max_steps = 10 * int(1.0 / self.dt)

        super().__init__()
        self.limit = limit
        self.sim = wafer_simulator.WaferSimulator(self.dt, limit, limit, size)
        self.action_scale = 10.0
        self.max_steps = max_steps
        self.current_step = 0

        # observation: x, y, vx, vy, target_dx, target_dy
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        self.target = np.zeros(2)
        self.reset()

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.sim.reset()
        self._set_random_target()
        self.current_step = 0
        self.lastObs = self._get_obs()
        self.targets_reached = 0  # Initialize targets reached counter
        return self.lastObs, {}
    
    def step(self, action):
        self.current_step += 1

        fx, fy = np.clip(action, -1.0, 1.0) * self.action_scale
        self.sim.applyForce(float(fx), float(fy))
        self.sim.update()

        obs = self._get_obs()
        pos = obs[0:2]
        dist = np.linalg.norm(self.target - pos)

        rewardScaler = 0.01 / self.dt
        reward = self._get_reward(obs, self.lastObs) * rewardScaler

        reachedDist = 1.0
        reached = dist < reachedDist
        if reached:
            reward += 1.0
            self.targets_reached += 1
            self._set_random_target()

        self.lastObs = obs
        done = self.current_step >= self.max_steps

        # always return info dict with targets_reached

        info = {}
        if done:
            info["targets_reached"] = self.targets_reached

        info["test_metric"] = 42  # Example of another metric

        return obs, float(reward), done, False, info  # Gymnasium format




    def _set_random_target(self):
        self.target = np.random.uniform(-9.0, 9.0, size=2)
    
    def _get_obs(self):
        pos = np.array(self.sim.getPosition())
        vel = np.array(self.sim.getVelocity())
        return np.concatenate([pos, vel, self.target - pos]).astype(np.float32)

    def _get_reward(self, current_obs, previous_obs):
        pos = current_obs[0:2]
        previous_pos = previous_obs[0:2]
        target_vector = self.target - pos
        previous_target_vector = self.target - previous_pos
        dist = np.linalg.norm(target_vector)
        previous_dist = np.linalg.norm(previous_target_vector)
        return previous_dist - dist
