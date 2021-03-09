import socket
import warnings
from typing import Union
import gym
from scenic.simulators.gfootball.rl.UnifromTeacherEnvironment import UnifromTeacherEnvironment
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import datetime
import numpy as np
from gfootball_impala_cnn import GfootballImpalaCNN
import train_template


def train(target_scenario, subtask_scenarios, n_eval_episodes, total_training_timesteps, eval_freq, save_dir, logdir, rewards):
    gf_env_settings = {
        "stacked": True,
        "rewards": 'scoring,checkpoints',
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": False,
        "action_set": "default"
    }

    env = UnifromTeacherEnvironment(target_task=target_scenario, sub_tasks=subtask_scenarios, gf_env_settings=gf_env_settings)
    features_extractor_class = GfootballImpalaCNN

    #rl_interface.run_built_in_ai_game_with_rl_env(env, trials=50)


    train_template.train(env=env, ALGO=PPO, features_extractor_class = features_extractor_class,
          scenario_name=target_scenario, n_eval_episodes=n_eval_episodes,
          total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
          save_dir=save_dir, logdir=logdir, dump_info={"rewards": rewards})




if __name__ == "__main__":

    import os
    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    target_task = f"{cwd}/exp_0_2/academy_rps_only_keeper.scenic"
    subtasks = [
        f"{cwd}/exp_0_2/no_keeper.scenic",
        f"{cwd}/exp_0_2/no_keeper_close.scenic",
        f"{cwd}/exp_0_2/no_keeper_no_pass.scenic",
        f"{cwd}/exp_0_2/rps_with_keeper_close.scenic"
    ]

    scenario_file = f"{cwd}/exp_0_0/academy_rps_only_keeper.scenic"
    n_eval_episodes = 5
    total_training_timesteps = 10000
    eval_freq = 2000

    save_dir = f"{cwd}/saved_models"
    logdir = f"{cwd}/tboard"
    rewards = 'scoring,checkpoints'
    print(save_dir, logdir)

    train(target_task, subtasks, n_eval_episodes = n_eval_episodes,
          total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
          save_dir=save_dir, logdir=logdir, rewards=rewards)
