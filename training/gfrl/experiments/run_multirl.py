"""A simple example of setting up a multi-agent version of GFootball with rllib.
"""

import os
import tempfile

import argparse
# import gfootball.env as football_env
import gym
import ray
from ray import tune
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from ray.tune.registry import register_env
from ray.rllib.models import ModelCatalog

from gfrl.common.nature_cnn import NatureCNN
from scenic.simulators.gfootball.rl.gfScenicEnv_v3 import GFScenicEnv_v3
from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario

class RllibGFootball(MultiAgentEnv):
    """An example of a wrapper for GFootball to make it compatible with rllib."""

    def __init__(self, scenario_file, num_left_to_be_controlled):
        # self.env = football_env.create_environment(
        #     env_name='academy_pass_and_shoot_with_keeper', stacked=True,
        #     representation='extracted',
        #     logdir=os.path.join(tempfile.gettempdir(), 'rllib_test'),
        #     write_goal_dumps=False, write_full_episode_dumps=False, render=True,
        #     dump_frequency=0,
        #     number_of_left_players_agent_controls=num_agents,
        #     channel_dimensions=(42, 42)
        # )
        gf_env_settings = {
            "stacked": True,
            "rewards": 'scoring',
            "representation": 'extracted',
            "real_time": True,
            "dump_frequency": 0,
            # "channel_dimensions": (42, 42)
        }
        scenario = buildScenario(scenario_file)

        self.env = GFScenicEnv_v3(initial_scenario=scenario, num_left_controlled=num_left_to_be_controlled,
                                  gf_env_settings=gf_env_settings, allow_render=False)

        self.action_space = gym.spaces.Discrete(self.env.action_space.nvec[1])
        self.observation_space = gym.spaces.Box(
            low=self.env.observation_space.low[0],
            high=self.env.observation_space.high[0],
            dtype=self.env.observation_space.dtype)
        self.num_agents = num_left_to_be_controlled
        print(self.num_agents)

    def reset(self):
        original_obs = self.env.reset()
        obs = {}
        for x in range(self.num_agents):
            if self.num_agents > 1:
                obs['agent_%d' % x] = original_obs[x]
            else:
                obs['agent_%d' % x] = original_obs
        return obs

    def step(self, action_dict):
        actions = []
        for key, value in sorted(action_dict.items()):
            actions.append(value)
        o, r, d, i = self.env.step(actions)
        rewards = {}
        obs = {}
        infos = {}
        for pos, key in enumerate(sorted(action_dict.keys())):
            infos[key] = i
            if self.num_agents > 1:
                rewards[key] = r[pos]
                obs[key] = o[pos]
            else:
                rewards[key] = r
                obs[key] = o
        dones = {'__all__': d}
        return obs, rewards, dones, infos



# running exps
parser = argparse.ArgumentParser()

parser.add_argument('--scenario-file', type=str, default="/home/mark/workplace/gf/scenic4rl/training/gfrl/_scenarios/grf/run_pass_shoot.scenic")
parser.add_argument('--num-agents', type=int, default=2)
parser.add_argument('--num-policies', type=int, default=2)
parser.add_argument('--num-steps', type=int, default=5000000)

parser.add_argument('--simple', action='store_true')

if __name__ == '__main__':
    args = parser.parse_args()
    ray.init(num_gpus=1)

    # Simple environment with `num_agents` independent players
    register_env('gfootball', lambda _: RllibGFootball(args.scenario_file, args.num_agents))
    single_env = RllibGFootball(args.scenario_file, args.num_agents)
    obs_space = single_env.observation_space
    act_space = single_env.action_space


    def gen_policy(_):
        return (None, obs_space, act_space, {})


    # Setup PPO with an ensemble of `num_policies` different policies
    policies = {
        'policy_{}'.format(i): gen_policy(i) for i in range(args.num_policies)
    }
    policy_ids = list(policies.keys())

    # set up model
    ModelCatalog.register_custom_model("nature_cnn", NatureCNN)

    # set up config
    rl_trainer_config = {
        'env': 'gfootball',
        "framework": "torch",
        'lambda': 0.95,
        'kl_coeff': 0.27,
        'clip_rewards': False,
        'vf_clip_param': 10.0,
        'entropy_coeff': 0.01,
        'train_batch_size': 1000,
        # 'sample_batch_size': 100,
        'sgd_minibatch_size': 500,
        'num_sgd_iter': 10,
        'num_workers': 1,
        'num_envs_per_worker': 1,
        'batch_mode': 'truncate_episodes',
        'observation_filter': 'NoFilter',
        'vf_share_layers': 'true',
        'num_gpus': 1,
        'lr': 0.00008,
        'log_level': 'INFO',
        'simple_optimizer': args.simple,
        # All model-related settings go into this sub-dict.
        "model": {
            "custom_model": "nature_cnn",
            "custom_model_config": {},
            # params for default network
            # "conv_filters": [[32, [8, 8], 4],
            #                  [64, [4, 4], 2],
            #                  [32, [3, 3], 1],
            #                  [1, [7, 10], 10],
            #                  ],
            # "post_fcnet_hiddens": [512],
        },
        'multiagent': {
            'policies': policies,
            'policy_mapping_fn': tune.function(
                lambda agent_id, episode, worker, **kwargs: policy_ids[int(agent_id[6:])]),
        }
    }

    tune.run(
        'PPO',
        name="285_passshoot_2left",
        stop={'timesteps_total': args.num_steps},
        checkpoint_freq=50,
        config=rl_trainer_config,
    )
