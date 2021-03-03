from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import gfootball

import parallel_train_template
from gfootball_impala_cnn import GfootballImpalaCNN

import time
import numpy as np
import matplotlib.pyplot as plt

import gym

from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.cmd_util import make_vec_env

def make_env(scenario_name, rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """

    def _init():
        env = gfootball.env.create_environment(scenario_name, number_of_left_players_agent_controls=1, render=False, representation="extracted",
                                               stacked=True, rewards=rewards)
        # Important: use a different seed for each environment
        env.seed(seed + rank)
        return env

    return _init


def train(scenario_name, n_eval_episodes, total_training_timesteps, eval_freq, save_dir, logdir, rewards, n_procs):

    env = SubprocVecEnv([make_env(scenario_name=scenario_name, rank=i) for i in range(n_procs)], start_method='spawn')

    #env = Monitor(env)
    features_extractor_class = GfootballImpalaCNN
    eval_env = make_env(scenario_name=scenario_name, rank=n_procs)()

    parallel_train_template.train(env=env, eval_env=eval_env, ALGO=PPO, features_extractor_class = features_extractor_class,
          scenario_name=scenario_name, n_eval_episodes=n_eval_episodes,
          total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
          save_dir=save_dir, logdir=logdir, n_procs=n_procs, dump_info={"rewards": rewards, "n_procs": n_procs})



if __name__ == "__main__":
    import os
    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    n_eval_episodes = 10
    total_training_timesteps = 1000000
    eval_freq = 2000

    save_dir = f"{cwd}/saved_models"
    logdir = f"{cwd}/tboard"
    rewards = 'scoring,checkpoints'

    n_procs = 16 

    train(scenario_name="academy_empty_goal_close", n_eval_episodes = n_eval_episodes,
          total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
          save_dir=save_dir, logdir=logdir, rewards=rewards, n_procs=n_procs)

