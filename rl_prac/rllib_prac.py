from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
from ray.tune.registry import register_env
"""
tune.run(PPOTrainer, config={"env": "CartPole-v0", "framework": "torch"})  # "log_level": "INFO" for verbose,
                                                     # "framework": "tfe"/"tf2" for eager,
                                                     # "framework": "torch" for PyTorch
"""

import gym, ray
from ray.rllib.agents import ppo
from scenic.simulators.gfootball.rl_interface import GFScenicEnv

def env_creator(env_config):

    gf_env_settings = {
                "stacked": True,
                "rewards": 'scoring,checkpoints',
                "representation": 'extracted',
                "players": [f"agent:left_players=1"],
                "real_time": False,
                "action_set": "default"
            }

    from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
    scenario_file = f"academy_empty_goal_close.scenic"
    scenario = buildScenario(scenario_file)
    env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)
    print("env instance created")
    return env 

ray.init()
register_env("my_env", env_creator)
#trainer = ppo.PPOTrainer(env="my_env")
trainer = ppo.PPOTrainer(env="my_env", config={

    'model': {
                'dim':96,
              'conv_filters': [
                  [96,16,96]
              ],
              'fcnet_hiddens': [256, 256],
              'use_lstm': False,
          }
    
})

for i in range(10):
    print("training loop iter: ", i)
    trainer.train()
