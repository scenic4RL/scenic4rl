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

    def __init__(self, scenario_file, player_control_mode, env_config=None):
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
            # "real_time": True,
            "dump_frequency": 0,
            # "channel_dimensions": (42, 42)
        }
        scenario = buildScenario(scenario_file)

        # rank is used to discern env across workers
        # Notice env_config may appear empty {} but always contains worker_index
        rank = env_config.worker_index if env_config is not None else 100

        self.env = GFScenicEnv_v3(initial_scenario=scenario, player_control_mode=player_control_mode,
                                  gf_env_settings=gf_env_settings, allow_render=False, rank=rank)

        self.action_space = gym.spaces.Discrete(self.env.action_space.nvec[1])
        self.observation_space = gym.spaces.Box(
            low=self.env.observation_space.low[0],
            high=self.env.observation_space.high[0],
            dtype=self.env.observation_space.dtype)
        
        self.num_agents = self.env.num_left_controlled

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


# scenario mapping
scenario_name_to_file = {
    "offense_avoid_pass_shoot":"/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/demonstration/offense_avoid_pass_shoot.scenic",
}


# running exps
parser = argparse.ArgumentParser()

parser.add_argument('--scenario', type=str)
parser.add_argument('--mode', type=str, default="allNonGK")
parser.add_argument('--num-steps', type=int, default=2000000)

if __name__ == '__main__':
    args = parser.parse_args()
    assert args.scenario in scenario_name_to_file, "invalid scenario name"
    scenario_file = scenario_name_to_file[args.scenario]

    ray.init(num_gpus=1)
    # Simple environment with input multi agent control mode
    register_env('gfootball', lambda config: RllibGFootball(scenario_file, args.mode, config))
    single_env = RllibGFootball(scenario_file, args.mode)
    obs_space = single_env.observation_space
    act_space = single_env.action_space
    num_policies = single_env.num_agents


    def gen_policy(_):
        return (None, obs_space, act_space, {})


    # Setup PPO with an ensemble of `num_policies` different policies
    policies = {
        'policy_{}'.format(i): gen_policy(i) for i in range(num_policies)
    }
    policy_ids = list(policies.keys())

    # set up model
    ModelCatalog.register_custom_model("nature_cnn", NatureCNN)

    # set up config
    rl_trainer_config = {
        'env': 'gfootball',
        "framework": "torch",
        # === Input settings ===
        "input": "/home/qcwu/gf/scenic4rl/training/gfrl/experiments/remove_noinfo_offline_avoid_pass_shoot",
        # "input_config": {},

        # === Postprocessing/accum., discounted return calculation ===
        "use_gae": True,
        "input_evaluation": [],
        "postprocess_inputs": False,

        # === Training ===
        # Scaling of advantages in exponential terms.
        # When beta is 0.0, MARWIL is reduced to behavior cloning
        # (imitation learning); see bc.py algorithm in this same directory.
        "beta": 0.0,
        # Balancing value estimation loss and policy optimization loss.
        "vf_coeff": 1.0,
        # If specified, clip the global norm of gradients by this amount.
        "grad_clip": None,
        # Learning rate for Adam optimizer.
        "lr": 1e-4,
        # The squared moving avg. advantage norm (c^2) update rate
        # (1e-8 in the paper).
        "moving_average_sqd_adv_norm_update_rate": 1e-8,
        # Starting value for the squared moving avg. advantage norm (c^2).
        "moving_average_sqd_adv_norm_start": 100.0,
        # Number of (independent) timesteps pushed through the loss
        # each SGD round.
        "train_batch_size": 2000,
        # Size of the replay buffer in (single and independent) timesteps.
        # The buffer gets filled by reading from the input files line-by-line
        # and adding all timesteps on one line at once. We then sample
        # uniformly from the buffer (`train_batch_size` samples) for
        # each training step.
        "replay_buffer_size": 10000,
        # Number of steps to read before learning starts.
        "learning_starts": 0,

        # === Parallelism ===
        # Which observation filter to apply to the observation.
        "observation_filter": "NoFilter",
        'num_gpus': 1,
        'num_workers': 14,
        'num_envs_per_worker': 1,
        'log_level': 'INFO',
        "evaluation_num_workers": 1,
        "evaluation_interval": 100,
        "evaluation_config": {"input": "sampler"},


        # All model-related settings go into this sub-dict.
        "model": {
            "custom_model": "nature_cnn",
            "custom_model_config": {},
        },
        'multiagent': {
            'policies': policies,
            'policy_mapping_fn':
                lambda agent_id, episode, worker, **kwargs: policy_ids[int(agent_id[6:])],
        }
    }

    tune.run(
        'BC',
        name=f"bc_{args.scenario}_{args.mode}_0",
        stop={'timesteps_total': args.num_steps},
        checkpoint_freq=50,
        config=rl_trainer_config,
        checkpoint_at_end=True
    )
