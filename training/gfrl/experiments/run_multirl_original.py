"""A simple example of setting up a multi-agent version of GFootball with rllib.
"""

import os
import tempfile

import argparse
import gfootball.env as football_env
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

    def __init__(self, num_left_to_be_controlled, env_config=None):
        gf_env_settings = {
            "stacked": True,
            "rewards": 'scoring',
            "representation": 'extracted',
            "real_time": True,
            "dump_frequency": 0,
            # "channel_dimensions": (42, 42)
        }

        self.env = football_env.create_environment(
            env_name='academy_3_vs_1_with_keeper', 
            stacked=True,
            representation='extracted',
            rewards='scoring',
            logdir=os.path.join(tempfile.gettempdir(), 'rllib_test'),
            write_goal_dumps=False, write_full_episode_dumps=False, render=False,
            dump_frequency=0,
            number_of_left_players_agent_controls=num_left_to_be_controlled,
        )

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

# parser.add_argument('--scenario-file', type=str, default="/home/qcwu/gf/scenic4rl/training/gfrl/_scenarios/grf/pass_n_shoot.scenic")
parser.add_argument('--num-agents', type=int, default=3)
parser.add_argument('--num-policies', type=int, default=3)
parser.add_argument('--num-steps', type=int, default=5000000)

parser.add_argument('--simple', action='store_true')

if __name__ == '__main__':
    args = parser.parse_args()
    ray.init(num_gpus=1)

    # Simple environment with `num_agents` independent players
    register_env('gfootball', lambda config: RllibGFootball(args.num_agents, config))
    single_env = RllibGFootball(args.num_agents)
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
        # Discount factor of the MDP.
        "gamma": 0.993,
        # Should use a critic as a baseline (otherwise don't use value baseline;
        # required for using GAE).
        "use_critic": True,
        # If true, use the Generalized Advantage Estimator (GAE)
        # with a value function, see https://arxiv.org/pdf/1506.02438.pdf.
        "use_gae": True,
        # The GAE (lambda) parameter.
        "lambda": 0.95,
        # Initial coefficient for KL divergence.
        "kl_coeff": 0.2,
        # Size of batches collected from each worker.
        "rollout_fragment_length": 200,
        # Number of timesteps collected for each SGD round. This defines the size
        # of each SGD epoch.
        "train_batch_size": 4000,
        # Total SGD batch size across all devices for SGD. This defines the
        # minibatch size within each epoch.
        "sgd_minibatch_size": 1000,
        # Whether to shuffle sequences in the batch when training (recommended).
        "shuffle_sequences": True,
        # Number of SGD iterations in each outer loop (i.e., number of epochs to
        # execute per train batch).
        "num_sgd_iter": 10,
        # Stepsize of SGD. 2.5e-4
        "lr": 0.00008,
        # Learning rate schedule.
        "lr_schedule": None,
        # Coefficient of the value function loss. IMPORTANT: you must tune this if
        # you set vf_share_layers=True inside your model's config.
        "vf_loss_coeff": 0.5,
        # Coefficient of the entropy regularizer.
        "entropy_coeff": 0.01,
        # Decay schedule for the entropy regularizer.
        "entropy_coeff_schedule": None,
        # PPO clip parameter.
        "clip_param": 0.27,
        # Clip param for the value function. Note that this is sensitive to the
        # scale of the rewards. If your expected V is large, increase this.
        "vf_clip_param": 10.0,
        # If specified, clip the global norm of gradients by this amount.
        "grad_clip": 0.5,
        # Target value for KL divergence.
        "kl_target": 0.01,
        # Whether to rollout "complete_episodes" or "truncate_episodes".
        "batch_mode": "truncate_episodes",
        # Which observation filter to apply to the observation.
        "observation_filter": "NoFilter",
        'num_gpus': 1,
        'num_workers': 15,
        'num_envs_per_worker': 1,
        'log_level': 'INFO',
        'simple_optimizer': args.simple,
        # All model-related settings go into this sub-dict.
        "model": {
            "custom_model": "nature_cnn",
            "custom_model_config": {},
        },
        'multiagent': {
            'policies': policies,
            'policy_mapping_fn': tune.function(
                lambda agent_id, episode, worker, **kwargs: policy_ids[int(agent_id[6:])]),
        }
    }

    tune.run(
        'PPO',
        name="original_3v1_3left_naturecnn",
        stop={'timesteps_total': args.num_steps},
        checkpoint_freq=50,
        config=rl_trainer_config,
    )
