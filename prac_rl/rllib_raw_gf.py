from ray import tune
from ray.rllib.agents.ppo import PPOTrainer

from ray.rllib.models import ModelCatalog
from ray.rllib.models.preprocessors import Preprocessor

import gfootball

#env = gfootball.env.create_environment("academy_empty_goal", number_of_left_players_agent_controls=1, render=False)

from ray.tune.registry import register_env
register_env('gfootball', lambda _: gfootball.env.create_environment("academy_empty_goal", number_of_left_players_agent_controls=1, render=False))

"""
tune.run(PPOTrainer, config={"env": env, "framework": "torch"})  # "log_level": "INFO" for verbose,
                                                     # "framework": "tfe"/"tf2" for eager,
                                                     # "framework": "torch" for PyTorch
"""

class PLEPreprocessor(Preprocessor):
    def _init(self):
        self.shape = self._obs_space.shape
    def transform(self, observation):
        observation = observation / 255.0
        return observation

ModelCatalog.register_custom_preprocessor("ple_prep", PLEPreprocessor)

tune.run(
    'PPO',
    stop={'training_iteration': 10},
    checkpoint_freq=50,
    config={
        'env': 'gfootball',
        'lambda': 0.95,
        'kl_coeff': 0.2,
        'lr': 2.5e-4,
        'log_level': 'DEBUG',

    },
    #"framework": "torch",
    
)

"""
        'model':{
                "custom_preprocessor": "ple_prep"
        }
"""