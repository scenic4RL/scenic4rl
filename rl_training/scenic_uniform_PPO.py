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


def train(target_scenario, subtask_scenarios, n_eval_episodes, total_training_timesteps, eval_freq, save_dir, logdir, tracedir, rewards, params):
    gf_env_settings = {
        "stacked": True,
        "rewards": rewards,
        "representation": 'extracted',
        "players": [f"agent:left_players=1"],
        "real_time": False,
        "action_set": "default",
        "dump_full_episodes": False,
        "dump_scores": False,
        "write_video": False, 
        "tracesdir": tracedir, 
        "write_full_episode_dumps": False,
        "write_goal_dumps": False,
        "render": False
    }

    env = UnifromTeacherEnvironment(target_task=target_scenario, sub_tasks=subtask_scenarios, gf_env_settings=gf_env_settings)
    features_extractor_class = GfootballImpalaCNN

    #rl_interface.run_built_in_ai_game_with_rl_env(env, trials=50)


    train_template.train(env=env, ALGO=PPO, features_extractor_class = features_extractor_class,
          scenario_name=target_scenario, n_eval_episodes=n_eval_episodes,
          total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
          save_dir=save_dir, logdir=logdir, dump_info={"rewards": rewards, "uniform curriculum": "True"}, 
          override_params=params)




if __name__ == "__main__":

    import os
    cwd = os.getcwd()
    print("Current working Directory: ", cwd)

    target_task = f"{cwd}/exp_0_4/academy_run_to_score.scenic"
    subtasks = [
        f"{cwd}/exp_0_4/sub0.scenic",
        f"{cwd}/exp_0_4/sub1.scenic",
        f"{cwd}/exp_0_4/sub2.scenic",
        f"{cwd}/exp_0_4/sub3.scenic"
    ]

    scenario_file = f"{cwd}/exp_0_0/academy_run_pass_and_shoot_with_keeper.scenic"
    n_eval_episodes = 10
    total_training_timesteps = 10000
    eval_freq = 5000
    override_params = {"n_steps": 4096, "batch_size": 1024}

    save_dir = f"{cwd}/saved_models"
    logdir = f"{cwd}/tboard"
    tracedir = f"{cwd}/game_trace"
    rewards = 'scoring' #'scoring,checkpoints'
    print("model, tf logs, game trace are saved in: ", save_dir, logdir, tracedir)

    train(target_task, subtasks, n_eval_episodes = n_eval_episodes,
          total_training_timesteps=total_training_timesteps, eval_freq=eval_freq,
          save_dir=save_dir, logdir=logdir, tracedir=tracedir, rewards=rewards, params=override_params)
