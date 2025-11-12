from stable_baselines3.common.callbacks import BaseCallback

from stable_baselines3.common.callbacks import BaseCallback

from stable_baselines3.common.callbacks import BaseCallback

class EpisodeMetricsLogger(BaseCallback):
    def __init__(self, metrics: list, verbose=1):
        super().__init__(verbose)
        self.metrics = metrics
        self.episode_data = {key: [] for key in metrics}

    def _on_step(self) -> bool:
        infos = self.locals.get("infos", [])

        for info in infos:
            for key in self.metrics:
                if key in info:
                    self.episode_data[key].append(info[key])
        return True

    def _on_rollout_end(self) -> None:
        for key, values in self.episode_data.items():
            if values:
                mean_val = sum(values) / len(values)
                self.logger.record(f"rollout/{key}", mean_val)

        # flush to logger to see in TensorBoard / console
        self.logger.dump(self.num_timesteps)
        # reset for next rollout
        self.episode_data = {key: [] for key in self.metrics}
