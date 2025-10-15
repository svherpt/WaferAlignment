import gymnasium as gym
import numpy as np
from simulator import wafer_simulator

class WaferBasicMotionEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, dt=0.05, limit=10.0, size=1.0):
        super().__init__()
        self.sim = wafer_simulator.WaferSimulator(dt, limit, limit, size)
        self.action_scale = 10.0   # scale RL actions -> Newtons
        # observation: x, y, vx, vy, target_dx, target_dy
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32)
        # action: continuous fx, fy in [-1,1] then scaled
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        self.target = np.zeros(2)
        self.reset()

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.sim.reset()
        self.target = np.random.uniform(-2.0, 2.0, size=2)
        return self._get_obs(), {}

    def _get_obs(self):
        pos = np.array(self.sim.getPosition())
        vel = np.array(self.sim.getVelocity())
        # concat pos, vel, and target vector (target - pos)
        return np.concatenate([pos, vel, self.target - pos]).astype(np.float32)

    def step(self, action):
        # clip and scale action
        fx, fy = np.clip(action, -1.0, 1.0) * self.action_scale
        self.sim.applyForce(float(fx), float(fy))
        self.sim.update()

        pos = np.array(self.sim.getPosition())
        vel = np.array(self.sim.getVelocity())
        dist = np.linalg.norm(self.target - pos)

        # Reward: positive for getting closer. use delta-distance or negative distance
        reward = -dist - 0.001 * np.linalg.norm([fx, fy])   # punish large forces
        done = bool(dist < 0.05)

        if done:
            reward += 5.0
            # sample new target for continuing training episodes
            self.target = np.random.uniform(-2.0, 2.0, size=2)

        obs = np.concatenate([pos, vel, self.target - pos]).astype(np.float32)
        return obs, float(reward), done, False, {}
