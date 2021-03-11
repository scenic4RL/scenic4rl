from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import gfootball


import time
import numpy as np
import matplotlib.pyplot as plt

import gym
from scenic.simulators.gfootball.rl_interface import GFScenicEnv
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv


def make_env(env_id, rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """

    def _init():
        env = gym.make(env_id)
        # Important: use a different seed for each environment
        env.seed(seed + rank)
        return env

    return _init
env_id = 'CartPole-v1'
total_procs= 0
n_procs = 2
train_env = SubprocVecEnv([make_env(env_id, i+total_procs) for i in range(n_procs)], start_method='spawn')

"""
def make_env(rank, seed=0):

    print("here")
    def _init():
        gf_env_settings = {
            "stacked": True,
            "rewards": 'scoring,checkpoints',
            "representation": 'extracted',
            "players": [f"agent:left_players=1"],
            "real_time": False,
            "action_set": "default"
        }

        from scenic.simulators.gfootball.utilities.scenic_helper import buildScenario
        #scenario_file = f"{cwd}/exp_0_0/academy_rps_only_keeper.scenic"
        #scenario = buildScenario(scenario_file)
        #env = GFScenicEnv(initial_scenario=scenario, gf_env_settings=gf_env_settings)
        print("h1")
        env = gym.make('CartPole-v0')
        print("h2")

        # Important: use a different seed for each environment
        env.seed(seed + rank)
        return env

    return _init


import os
cwd = os.getcwd()

n_procs=2
env_list = [make_env(rank=i) for i in range(n_procs)]
print("h3")
env = SubprocVecEnv(env_list) #start_method='spawn'
"""

"""rllib links"""
"""
https://docs.ray.io/en/master/rllib-training.html#scaling-guide
about parallelization and vec env: https://docs.ray.io/en/master/rllib-env.html#
custom vector env: https://github.com/ray-project/ray/blob/master/rllib/env/vector_env.py 

"""